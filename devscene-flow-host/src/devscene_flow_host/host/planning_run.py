"""`run_planning`: one drive of a branch's planning walk, composed from the host's pieces and run
with GraphScene's `start_run` / `continue_run` to its `RunExit`.

The rule: it does what the retired bash driver's `pd_main`, `pd_entry` and `pd_run_set` did
(`cli/templates/scripts/lib/planning-driver-lib.sh`, read in that file's history), in
`pd_main`'s order:
- the kill switch present in the main checkout is `kind="kill_switch"`, and the worktree's
  `<stateDir>/STOP` present is `kind="stop_file"`, each before anything is dispatched or written;
- a missing flow-progress ledger raises `RecordError`;
- then the dispatch counter is reset, the walker opened and `decide_planning_entry` asked:
  `PlanningDone` is `kind="done"`; a `StartWalk` runs `start_run` from its entry and resume, a
  `ContinueWalk` runs `continue_run` with its outcome;
- the executor is `ClaudeExecutor` wrapped in `PlanningExecutor`, with one agent contract per
  distinct agent of the graph's dispatch nodes, the entry's pairs given to `CorePromptBuilder`,
  and `NodeSessions` as both the usage sink and the launch sink;
- the hooks are `PlanningHooks` over `commit_wrapper_path(main_repo)`,
  wrapped so each `commit_plan_round` call, once it has run, records the passage's round as
  `last_round` and clears the kept revision findings, as `record_outcome` clears on a
  `RoundPassage`;
- a `Halt` exit carries the round of the walk's pending dispatch, the first dispatch's for a set,
  and the pending nodes: a dispatch's node, a set's nodes, a wait's pending gates;
- every `run` outcome carries the dispatch cap, and the round number of the last dispatch that
  carried one, as `dispatched_round`.
Every value read from `devscene.config.json` and `.mcp.json` comes through `records`.

Deliberately not covered:
- Acting on the exit — the hand-off narration, the pause files, the partial commit, the parks:
  `host/run_exits.py` (Task 17).
- Exit statuses and the observation flush: the command over this module (Task 18).
"""

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, TypeAlias

from graphscene import (
    AfterRound,
    Dispatch,
    DispatchNode,
    DispatchSet,
    Executor,
    FlowGraph,
    Halt,
    HookCall,
    NodeResult,
    RunExit,
    Wait,
    Walker,
    continue_run,
    start_run,
)

from devscene_flow_host.host.agent_flags import agent_args, session_args, session_env
from devscene_flow_host.host.agent_prompts import CorePromptBuilder
from devscene_flow_host.host.claude_executor import NODE_INACTIVITY_LIMIT_SECONDS, ClaudeExecutor
from devscene_flow_host.host.commit_points import commit_wrapper_path
from devscene_flow_host.host.node_sessions import NodeSessions
from devscene_flow_host.host.observations import Observations
from devscene_flow_host.host.planning_entry import (
    ContinueWalk,
    PlanningDone,
    decide_planning_entry,
)
from devscene_flow_host.host.planning_executor import PlanningExecutor, clear_revision_findings
from devscene_flow_host.host.planning_hooks import COMMIT_PLAN_ROUND, PlanningHooks
from devscene_flow_host.host.run_control import (
    UNDELIVERED_LIMIT,
    FileDispatchCounter,
    FileRunSignals,
    kill_switch_present,
    planning_limits,
)
from devscene_flow_host.host.walking import open_walker
from devscene_flow_host.records.config import read_config
from devscene_flow_host.records.core_limits import read_max_total_dispatches
from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.ledger import ledger_path
from devscene_flow_host.records.mcp_servers import read_mcp_servers
from devscene_flow_host.records.plugin_contracts import (
    AgentContract,
    read_agent_contract,
    read_plugin_name,
)

FAILURE_OUTCOME: Final = "error"

PlanningKind: TypeAlias = Literal["done", "kill_switch", "stop_file", "run"]


@dataclass(frozen=True)
class PlanningRequest:
    """`command` is the agent CLI's argv prefix; `venv` is the flow host's environment directory,
    or `None`."""

    branch: str
    worktree: Path
    main_repo: Path
    plugin_dir: Path
    graph: FlowGraph
    log_path: Path
    formatter: str
    plugin_dir_added: bool
    command: tuple[str, ...]
    shared_args: tuple[str, ...]
    environ: Mapping[str, str]
    venv: Path | None
    scratch: Path
    observations: Observations
    narrate: Callable[[str], None]


@dataclass(frozen=True)
class PlanningOutcome:
    kind: PlanningKind
    exit: RunExit | None = None
    consumed: tuple[int, ...] = ()
    last_round: int | None = None
    pending_round: int | None = None
    sessions: NodeSessions | None = None
    pending_nodes: tuple[str, ...] = ()
    dispatched_round: int | None = None
    dispatch_cap: int | None = None


class _RoundRecorder:
    def __init__(self, inner: Executor) -> None:
        self._inner = inner
        self.last_round: int | None = None

    async def run(self, dispatch: Dispatch) -> NodeResult:
        if dispatch.round_number is not None:
            self.last_round = dispatch.round_number
        return await self._inner.run(dispatch)


class _DrivenHooks:
    def __init__(self, inner: PlanningHooks, *, repo_root: Path, state_dir: str, branch: str):
        self._inner = inner
        self._repo_root = repo_root
        self._state_dir = state_dir
        self._branch = branch
        self.last_round: int | None = None

    def provides(self, hook: str) -> bool:
        return self._inner.provides(hook)

    async def run(self, hook: str, call: HookCall) -> None:
        await self._inner.run(hook, call)
        if hook == COMMIT_PLAN_ROUND and isinstance(call, AfterRound):
            self.last_round = call.passage.number
            await asyncio.to_thread(
                clear_revision_findings, self._repo_root, self._state_dir, self._branch
            )


async def run_planning(request: PlanningRequest) -> PlanningOutcome:
    if kill_switch_present(request.main_repo):
        return PlanningOutcome("kill_switch")
    worktree = request.worktree
    branch = request.branch
    state_dir = read_config(worktree).state_dir
    signals = FileRunSignals(worktree, state_dir)
    if signals.stop_requested():
        return PlanningOutcome("stop_file")
    ledger = ledger_path(worktree, state_dir, branch)
    if not ledger.is_file():
        rel = ledger.relative_to(worktree).as_posix()
        raise RecordError(
            f"the flow-progress ledger '{rel}' does not exist; the setup session creates it"
        )

    counter = FileDispatchCounter(worktree, state_dir)
    counter.reset()
    graph = request.graph
    walker = open_walker(worktree, branch, graph)
    entry = decide_planning_entry(walker, worktree, state_dir, branch)
    if isinstance(entry, PlanningDone):
        return PlanningOutcome("done")

    plugin_dir = request.plugin_dir
    builder = CorePromptBuilder(
        graph,
        plugin_dir=plugin_dir,
        repo_root=worktree,
        state_dir=state_dir,
        branch=branch,
        pairs=entry.pairs,
    )
    contracts = _contracts(graph, plugin_dir)
    sessions = NodeSessions(
        log_path=request.log_path,
        formatter=request.formatter,
        observations=request.observations,
        narrate=request.narrate,
    )
    claude = ClaudeExecutor(
        command=request.command,
        plugin_dir=plugin_dir,
        plugin_name=read_plugin_name(plugin_dir),
        cwd=worktree,
        contracts=contracts,
        inactivity_limit_seconds=NODE_INACTIVITY_LIMIT_SECONDS,
        usage_sink=sessions,
        agent_prompt_builder=builder,
        session_args=session_args(
            request.shared_args, plugin_dir, plugin_dir_added=request.plugin_dir_added
        ),
        agent_args=agent_args(contracts, read_mcp_servers(worktree), request.scratch),
        env=session_env(request.environ, venv=request.venv),
    )
    executor = _RoundRecorder(
        PlanningExecutor(
            claude, graph=graph, repo_root=worktree, state_dir=state_dir, branch=branch
        )
    )
    wrapper = commit_wrapper_path(request.main_repo)
    hooks = _DrivenHooks(
        PlanningHooks(
            graph,
            repo_root=worktree,
            state_dir=state_dir,
            branch=branch,
            commit_wrapper=wrapper,
        ),
        repo_root=worktree,
        state_dir=state_dir,
        branch=branch,
    )
    limits = planning_limits(read_max_total_dispatches(plugin_dir))

    exit_: RunExit
    if isinstance(entry, ContinueWalk):
        exit_ = await continue_run(
            walker,
            executor,
            signals=signals,
            counter=counter,
            sink=sessions,
            limits=limits,
            failure_outcome=FAILURE_OUTCOME,
            undelivered_limit=UNDELIVERED_LIMIT,
            outcome=entry.outcome,
            hooks=hooks,
        )
    else:
        exit_ = await start_run(
            walker,
            executor,
            signals=signals,
            counter=counter,
            sink=sessions,
            limits=limits,
            failure_outcome=FAILURE_OUTCOME,
            undelivered_limit=UNDELIVERED_LIMIT,
            entry=entry.entry,
            resume=entry.resume,
            hooks=hooks,
        )

    pending_round: int | None = None
    pending_nodes: tuple[str, ...] = ()
    if isinstance(exit_, Halt):
        pending_round, pending_nodes = await _pending(walker)
    return PlanningOutcome(
        "run",
        exit=exit_,
        consumed=builder.consumed,
        last_round=hooks.last_round,
        pending_round=pending_round,
        sessions=sessions,
        pending_nodes=pending_nodes,
        dispatched_round=executor.last_round,
        dispatch_cap=limits.dispatch_cap,
    )


def _contracts(graph: FlowGraph, plugin_dir: Path) -> dict[str, AgentContract]:
    contracts: dict[str, AgentContract] = {}
    for node in graph.nodes.values():
        if isinstance(node, DispatchNode) and node.agent not in contracts:
            contracts[node.agent] = read_agent_contract(plugin_dir, node.agent)
    return contracts


async def _pending(walker: Walker) -> tuple[int | None, tuple[str, ...]]:
    step = await asyncio.to_thread(walker.current)
    if isinstance(step, Dispatch):
        return step.round_number, (step.node,)
    if isinstance(step, DispatchSet):
        nodes = tuple(dispatch.node for dispatch in step.dispatches)
        return (step.dispatches[0].round_number if step.dispatches else None), nodes
    if isinstance(step, Wait):
        return None, step.pending
    return None, ()
