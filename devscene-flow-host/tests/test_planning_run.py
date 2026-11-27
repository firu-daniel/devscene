"""The rule this file exists to enforce: `run_planning` dispatches nothing when the main
checkout's kill switch or the worktree's STOP is present, refuses a missing ledger with its exact
message, reports `done` when `P1`–`P3` are resolved, and otherwise drives the planning walk once
to its `RunExit`: a fresh walk reaches the convergence `End` with the commit wrapper called in
Override 6's order, a planted PAUSE halts with the pending dispatch's round and node and the
planning core's cap of 40, the last dispatched round is reported, an answered pair is
spent on the writer and reported in `consumed`, no node session inherits `VIRTUAL_ENV` or
`PYTHONPATH`, and no more than 5 node sessions run at once.

The graph is `cli/templates/scripts/flows/task_plan_writing.graph.json` and the plugin directory
is this checkout's `plugin/`, both read-only. Every node session is `fake_planning_agent.py`, every
commit wrapper a fake planted under `tmp_path` logging its argv, as
`tests/test_planning_hooks.py` → `_plant_wrapper` does, and every configuration and ledger is
planted under `tmp_path`. Every expected value is a literal written from the task plan's contract
and the graph file, never taken from the code under test.

Deliberately not covered:
- Acting on the exit and the observation flush: Tasks 17 and 18's suites.
- The concurrency limit itself being reached: the planning graph's widest set is three gates, so
  only the bound is asserted, from the fake's recorded start and end order and no duration.
"""

import asyncio
import json
import os
from pathlib import Path

import pytest
from graphscene import End, Halt, load_graph_file

from devscene_flow_host.host.observations import Observations
from devscene_flow_host.host.planning_run import PlanningOutcome, PlanningRequest, run_planning
from devscene_flow_host.records.errors import RecordError
from fake_planning_agent import plant, read_calls

_ROOT = Path(__file__).resolve().parents[2]
_GRAPH = _ROOT / "cli" / "templates" / "scripts" / "flows" / "task_plan_writing.graph.json"
_PLUGIN_DIR = _ROOT / "plugin"
_BRANCH = "feat_x"
_LEDGER_TEMPLATE = (
    "# Flow progress\n"
    "\n"
    "## Run mode\n"
    "- skipped: none\n"
    "\n"
    "## Planning\n"
    "- [{p1}] P1. Task plan converged\n"
    "- [{p2}] P2. UI-test plan converged\n"
    "- [{p3}] P3. Planning committed\n"
)


def _plant_repo(
    root: Path, *, p1: str = " ", p2: str = " ", p3: str = " ", parity: bool = False
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": "state",
                "scriptsDir": "bin",
                "phases": {"parity": parity, "qa": False},
            }
        ),
        encoding="utf-8",
    )
    ledger = root / "state" / "flow_progress" / "feat_x_progress.md"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(_LEDGER_TEMPLATE.format(p1=p1, p2=p2, p3=p3), encoding="utf-8")


def _plant_wrapper(root: Path) -> Path:
    wrapper = root / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
        'args=("$@")\n'
        'call="${args[*]:3:$(($# - 4))}"\n'
        'printf \'%s\\n\' "$call" >>"$here/calls.log"\n'
        "exit 0\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


def _wrapper_calls(root: Path) -> list[str]:
    log = root / "bin" / "calls.log"
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _request(
    tmp_path: Path, root: Path, returns: dict[str, object] | None = None
) -> PlanningRequest:
    agent_dir = tmp_path / "agent"
    agent_dir.mkdir(exist_ok=True)
    scratch = tmp_path / "scratch"
    scratch.mkdir(exist_ok=True)
    logs = tmp_path / "logs"
    logs.mkdir(exist_ok=True)
    command = plant(
        agent_dir, {"calls_log": str(agent_dir / "calls.jsonl"), "returns": returns or {}}
    )
    return PlanningRequest(
        branch=_BRANCH,
        worktree=root,
        main_repo=root,
        plugin_dir=_PLUGIN_DIR,
        graph=load_graph_file(_GRAPH),
        log_path=logs / "planning.log",
        formatter="true",
        plugin_dir_added=False,
        command=command,
        shared_args=(),
        environ={
            "PATH": os.environ.get("PATH", ""),
            "VIRTUAL_ENV": str(tmp_path / "venv"),
            "PYTHONPATH": str(tmp_path / "pythonpath"),
        },
        venv=None,
        scratch=scratch,
        observations=Observations(),
        narrate=lambda _line: None,
    )


def _agent_calls(tmp_path: Path) -> list[dict[str, object]]:
    return read_calls(tmp_path / "agent" / "calls.jsonl")


def _run(request: PlanningRequest) -> PlanningOutcome:
    return asyncio.run(run_planning(request))


def test_the_kill_switch_dispatches_nothing(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    (root / "state" / "AUTONOMOUS_STOP").write_text("", encoding="utf-8")
    outcome = _run(_request(tmp_path, root))
    assert outcome == PlanningOutcome("kill_switch")
    assert _agent_calls(tmp_path) == []
    assert _wrapper_calls(root) == []


def test_stop_dispatches_nothing(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    (root / "state" / "STOP").write_text("", encoding="utf-8")
    outcome = _run(_request(tmp_path, root))
    assert outcome == PlanningOutcome("stop_file")
    assert _agent_calls(tmp_path) == []
    assert not (root / "state" / ".dispatch_counter").exists()


def test_a_missing_ledger_is_refused(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    ledger = root / "state" / "flow_progress" / "feat_x_progress.md"
    ledger.unlink()
    with pytest.raises(RecordError) as caught:
        _run(_request(tmp_path, root))
    assert str(caught.value) == (
        f"the flow-progress ledger '{ledger}' does not exist; the setup session creates it"
    )


def test_every_planning_entry_resolved_is_done(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root, p1="x", p2="-", p3="x")
    _plant_wrapper(root)
    outcome = _run(_request(tmp_path, root))
    assert outcome == PlanningOutcome("done")
    assert outcome.consumed == ()
    assert _agent_calls(tmp_path) == []


def test_a_fresh_walk_runs_to_the_end_committing_in_order(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    outcome = _run(_request(tmp_path, root))
    assert outcome.kind == "run"
    assert isinstance(outcome.exit, End), outcome.exit
    assert (outcome.exit.node, outcome.exit.binding) == ("convergence", "<terminal_handoff>")
    assert _wrapper_calls(root) == [
        "plan-round --round 0",
        "ledger-flip --entry P1",
        "ledger-flip --entry P1",
        "task-plan",
        "ledger-flip --entry P3",
    ]
    assert outcome.last_round == 0
    assert outcome.pending_round is None
    assert outcome.pending_nodes == ()
    assert outcome.dispatched_round == 0
    assert outcome.consumed == ()
    assert [call["agent"] for call in _agent_calls(tmp_path)][0] == "task-plan-writer"
    assert sorted(str(call["agent"]) for call in _agent_calls(tmp_path)[1:]) == [
        "architecture-reviewer",
        "task-plan-reviewer",
    ]
    assert outcome.sessions is not None
    assert len(outcome.sessions.rows) == 3
    assert (root / "state" / ".dispatch_counter").read_text(encoding="utf-8") == "3\n"


def test_a_planted_pause_halts_with_the_pending_round(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    (root / "state" / "PAUSE").write_text("", encoding="utf-8")
    outcome = _run(_request(tmp_path, root))
    assert outcome.kind == "run"
    assert isinstance(outcome.exit, Halt), outcome.exit
    assert outcome.exit.reason == "pause"
    assert outcome.pending_round == 0
    assert outcome.pending_nodes == ("plan_writer",)
    assert outcome.dispatched_round is None
    assert outcome.dispatch_cap == 40
    assert outcome.last_round is None
    assert _agent_calls(tmp_path) == []
    assert _wrapper_calls(root) == []


def test_an_answered_pair_is_consumed_and_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    pairs = root / "state" / "clarifications" / _BRANCH
    pairs.mkdir(parents=True)
    (pairs / "question_1.md").write_text(
        "Raised by: task-plan-writer\nWhich cache?\n", encoding="utf-8"
    )
    (pairs / "answer_1.md").write_text("Use the shared cache.\n", encoding="utf-8")
    outcome = _run(_request(tmp_path, root))
    assert outcome.consumed == (1,)
    writer = _agent_calls(tmp_path)[0]
    assert writer["agent"] == "task-plan-writer"
    assert "Use the shared cache." in str(writer["prompt"])
    assert "Which cache?" in str(writer["prompt"])


def test_no_node_session_inherits_the_flow_hosts_python_environment(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    _plant_wrapper(root)
    _run(_request(tmp_path, root))
    calls = _agent_calls(tmp_path)
    assert len(calls) == 3
    assert [(call["VIRTUAL_ENV"], call["PYTHONPATH"]) for call in calls] == [(None, None)] * 3


def test_at_most_five_node_sessions_run_at_once(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root, parity=True)
    _plant_wrapper(root)
    returns: dict[str, object] = {
        agent: [{"sleep": 0.2}]
        for agent in ("business-parity-reviewer", "architecture-reviewer", "task-plan-reviewer")
    }
    outcome = _run(_request(tmp_path, root, returns))
    assert isinstance(outcome.exit, End), outcome.exit
    calls = _agent_calls(tmp_path)
    assert len(calls) == 4
    events: list[tuple[int, int]] = []
    for call in calls:
        start, end = call["start"], call["end"]
        assert isinstance(start, int) and isinstance(end, int)
        events.extend(((start, 1), (end, -1)))
    running = peak = 0
    for _, change in sorted(events, key=lambda event: (event[0], event[1])):
        running += change
        peak = max(peak, running)
    assert peak <= 5
