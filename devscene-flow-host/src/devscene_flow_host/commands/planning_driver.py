"""The `devscene-planning-driver` command: one drive of a branch's planning walk, launched by the
watcher, answering it with a status and one stdout line.

The rule: the command line is
`--branch --worktree --main-repo --plugin-dir --flows --log --formatter [--plugin-dir-added] --
<agent_cli> [<shared session flag>…]`, each named flag required with a non-empty value, a repeated
flag keeping its last value; the command answers:
- `0`: the run handed off. Stdout is exactly `consumed:`, then ` <i>` per consumed index, then a
  newline.
- `3`: a clean stop, its files written. Stdout is exactly `stopped: <kind>` and a newline, `<kind>`
  one of `STOP_WORDS`' values.
- `2`: a fault — a `UsageError`; a `RecordError`, `GraphError`, `CommitPointError` or `OSError`; a
  `ValueError` or `LookupError`; any other exception, as `internal error: <type>: <message>`.
  Stderr carries one `planning-driver: <cause>` line, a newline in the cause flattened, stdout
  nothing, and once `--log` is known the cause is narrated to it.
No exception but `KeyboardInterrupt` and `SystemExit` escapes `main`. The steps run in order: the
command line; `<flows>/task_plan_writing.graph.json`, loaded and declaring `FLOW`; the worktree's
`stateDir` and the main checkout's commit wrapper; a scratch directory, removed file by file and
then itself, never recursively; `run_planning`; `act_on_exit`; then always the session-table
observation, when any session ran, and `Observations.flush`. Narration is `[plan-drive] <line>`
appended to `--log`.

Deliberately not covered:
- Deciding any walk step or the run's entry: `host/planning_run.py`'s.
- Acting on a `RunExit` — narration, parks, pause files, partial commits: `host/run_exits.py`'s.
- Reading any record: `records`'.
"""

import asyncio
import contextlib
import os
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, TextIO

from graphscene import FlowGraph, GraphError, load_graph_file

from devscene_flow_host.host.commit_points import CommitPointError, commit_wrapper_path
from devscene_flow_host.host.observations import Observations
from devscene_flow_host.host.planning_run import PlanningRequest, run_planning
from devscene_flow_host.host.run_exits import StopKind, act_on_exit
from devscene_flow_host.records.config import read_config
from devscene_flow_host.records.errors import RecordError

PROGRAM: Final = "devscene-planning-driver"
PREFIX: Final = "planning-driver: "
NARRATION_PREFIX: Final = "[plan-drive] "
FLOW: Final = "task_plan_writing"
GRAPH_SUFFIX: Final = ".graph.json"
SEPARATOR: Final = "--"
PLUGIN_DIR_ADDED: Final = "--plugin-dir-added"
REQUIRED_FLAGS: Final = (
    "--branch",
    "--worktree",
    "--main-repo",
    "--plugin-dir",
    "--flows",
    "--log",
    "--formatter",
)
CONSUMED_LINE: Final = "consumed:"
STOPPED_LINE: Final = "stopped: {kind}"
STOP_WORDS: Final[Mapping[StopKind, str]] = {
    "park": "park",
    "pause": "pause",
    "undelivered": "undelivered",
    "stop": "stop",
    "cap": "cap",
    "kill_switch": "kill-switch",
}
HANDED_OFF_STATUS: Final = 0
FAULT_STATUS: Final = 2
STOPPED_STATUS: Final = 3
SESSIONS_CATEGORY: Final = "flow-efficiency"
SESSIONS_PROBLEM: Final = "Script-driven planning node sessions (" + PROGRAM + " returned {status})"
SESSIONS_EVIDENCE: Final = "seq node agent attempt result duration cost: {rows}"
SESSIONS_COST: Final = "{count} node session(s)"
ROW_SEPARATOR: Final = "; "


class UsageError(Exception):
    """A refused command line; its message is the cause without `PREFIX`."""


@dataclass(frozen=True)
class Invocation:
    branch: str
    worktree: Path
    main_repo: Path
    plugin_dir: Path
    flows: Path
    log: Path
    formatter: str
    plugin_dir_added: bool
    command: tuple[str, ...]
    shared_args: tuple[str, ...]


def parse(argv: Sequence[str]) -> Invocation:
    values: dict[str, str] = {}
    added = False
    rest = list(argv)
    while rest and rest[0] != SEPARATOR:
        flag = rest.pop(0)
        if flag == PLUGIN_DIR_ADDED:
            added = True
            continue
        if flag not in REQUIRED_FLAGS:
            raise UsageError(f"unknown flag '{flag}'")
        if not rest or rest[0] == SEPARATOR:
            raise UsageError(f"{flag} needs a value")
        values[flag] = rest.pop(0)
    if not rest:
        raise UsageError(f"missing '{SEPARATOR}' and the agent CLI after it")
    rest.pop(0)
    if not rest or not rest[0]:
        raise UsageError(f"missing the agent CLI after '{SEPARATOR}'")
    for flag in REQUIRED_FLAGS:
        if flag not in values:
            raise UsageError(f"missing {flag}")
        if not values[flag]:
            raise UsageError(f"{flag} needs a non-empty value")
    return Invocation(
        branch=values["--branch"],
        worktree=Path(values["--worktree"]),
        main_repo=Path(values["--main-repo"]),
        plugin_dir=Path(values["--plugin-dir"]),
        flows=Path(values["--flows"]),
        log=Path(values["--log"]),
        formatter=values["--formatter"],
        plugin_dir_added=added,
        command=(rest[0],),
        shared_args=tuple(rest[1:]),
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = sys.stdout if stdout is None else stdout
    err = sys.stderr if stderr is None else stderr
    arguments = list(sys.argv[1:] if argv is None else argv)
    narrate: Callable[[str], None] | None = None
    try:
        invocation = parse(arguments)
        narrate = _narrator(invocation.log)
        status, text = _run(invocation, narrate)
    except Exception as error:
        cause = " ".join(failure(error).splitlines())
        if narrate is not None:
            with contextlib.suppress(OSError):
                narrate(cause)
        err.write(PREFIX + cause + "\n")
        return FAULT_STATUS
    out.write(text)
    return status


def failure(error: BaseException) -> str:
    if isinstance(error, GraphError):
        return str(error.violations[0])
    if isinstance(
        error, (UsageError, RecordError, CommitPointError, OSError, ValueError, LookupError)
    ):
        return str(error)
    return f"internal error: {type(error).__name__}: {error}"


def answer(kind: StopKind, consumed: Sequence[int]) -> tuple[int, str]:
    if kind == "handed_off":
        return HANDED_OFF_STATUS, CONSUMED_LINE + "".join(f" {i}" for i in consumed) + "\n"
    return STOPPED_STATUS, STOPPED_LINE.format(kind=STOP_WORDS[kind]) + "\n"


def _narrator(log: Path) -> Callable[[str], None]:
    def narrate(line: str) -> None:
        with log.open("a", encoding="utf-8") as handle:
            handle.write(NARRATION_PREFIX + line + "\n")

    return narrate


def _run(invocation: Invocation, narrate: Callable[[str], None]) -> tuple[int, str]:
    graph = _graph(invocation.flows)
    state_dir = read_config(invocation.worktree).state_dir
    wrapper = commit_wrapper_path(invocation.main_repo)
    scratch = Path(tempfile.mkdtemp(prefix=PROGRAM + "."))
    try:
        return asyncio.run(_drive(invocation, graph, state_dir, wrapper, scratch, narrate))
    finally:
        _remove_scratch(scratch)


async def _drive(
    invocation: Invocation,
    graph: FlowGraph,
    state_dir: str,
    wrapper: Path,
    scratch: Path,
    narrate: Callable[[str], None],
) -> tuple[int, str]:
    observations = Observations()
    request = PlanningRequest(
        branch=invocation.branch,
        worktree=invocation.worktree,
        main_repo=invocation.main_repo,
        plugin_dir=invocation.plugin_dir,
        graph=graph,
        log_path=invocation.log,
        formatter=invocation.formatter,
        plugin_dir_added=invocation.plugin_dir_added,
        command=invocation.command,
        shared_args=invocation.shared_args,
        environ=os.environ,
        venv=Path(sys.prefix) if sys.prefix != sys.base_prefix else None,
        scratch=scratch,
        observations=observations,
        narrate=narrate,
    )
    rows: tuple[str, ...] = ()
    status = FAULT_STATUS
    try:
        outcome = await run_planning(request)
        if outcome.sessions is not None:
            rows = outcome.sessions.rows
        kind = await act_on_exit(
            outcome,
            graph=graph,
            repo_root=invocation.worktree,
            main_repo=invocation.main_repo,
            state_dir=state_dir,
            branch=invocation.branch,
            wrapper=wrapper,
            observations=observations,
            narrate=narrate,
            now=datetime.now(UTC),
        )
        status, text = answer(kind, outcome.consumed)
        return status, text
    finally:
        if rows:
            observations.add(
                SESSIONS_CATEGORY,
                SESSIONS_PROBLEM.format(status=status),
                SESSIONS_EVIDENCE.format(rows=ROW_SEPARATOR.join(rows)),
                SESSIONS_COST.format(count=len(rows)),
            )
        await observations.flush(
            repo_root=invocation.worktree,
            main_repo=invocation.main_repo,
            state_dir=state_dir,
            branch=invocation.branch,
            wrapper=wrapper,
            home=os.environ.get("HOME"),
            now=datetime.now(UTC),
            log=narrate,
        )


def _graph(flows: Path) -> FlowGraph:
    path = flows / (FLOW + GRAPH_SUFFIX)
    if not path.is_file():
        raise FileNotFoundError(f"no planning graph at {path}")
    try:
        graph = load_graph_file(path)
    except GraphError as error:
        raise ValueError(f"cannot load {path}: {failure(error)}") from None
    if graph.flow != FLOW:
        raise ValueError(f"graph {path} declares flow '{graph.flow}', not '{FLOW}'")
    return graph


def _remove_scratch(scratch: Path) -> None:
    with contextlib.suppress(OSError):
        for entry in scratch.iterdir():
            with contextlib.suppress(OSError):
                entry.unlink()
        scratch.rmdir()


if __name__ == "__main__":
    raise SystemExit(main())
