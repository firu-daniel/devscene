"""The rule this file exists to enforce: `PlanningHooks` makes the planning graph's commits and
ledger flips — `commit_plan_round` one `plan-round` commit per closed round, `flip_ledger` a flip
and a `ledger-flip` commit per planning `LedgerPassage` in the step, `commit_convergence` the
UI-test-plan commit when one was written, the task-plan commit and the `P3` flip — refuses a
misused call kind and an unknown hook with their exact messages, and lets a refused commit
propagate; walked in run mode over the real planning graph, the hooks fire in Override 6's order
and a resume after a refused commit re-issues it.

Every wrapper is a fake planted under `tmp_path` that logs each call's arguments after the
worktree and before `--push`, and exits by a scripted status; every configuration and ledger is
planted under `tmp_path`. Every expected value is a literal written from the task plan's contract
and the graph file, never taken from the code under test.

Deliberately not covered:
- The real `commit-on-branch.sh`, and `commit_artifact`'s own exit mapping:
  `tests/test_commit_points.py` and the wrapper's own suites.
"""

import asyncio
import json
from pathlib import Path

import pytest
from graphscene import (
    AfterRound,
    BeforeDispatch,
    BeforeEnd,
    Dispatch,
    End,
    ExecutionLimits,
    FlowGraph,
    Launch,
    LedgerPassage,
    Passage,
    RoundPassage,
    ScriptedOutcome,
    StubExecutor,
    continue_run,
    load_graph_file,
    start_run,
)

from devscene_flow_host.host.commit_points import CommitPointError
from devscene_flow_host.host.planning_hooks import PlanningHooks
from devscene_flow_host.host.walking import open_walker

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_BRANCH = "feat_x"
_STATE_DIR = "state"
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
_UI_TEST_INDEX = "state/ui_test_plans/feat_x_ui_test_plan.md"


def _plant_wrapper(tmp_path: Path, *, status: int = 0) -> Path:
    wrapper = tmp_path / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
        'args=("$@")\n'
        'call="${args[*]:3:$(($# - 4))}"\n'
        'printf \'%s\\n\' "$call" >>"$here/calls.log"\n'
        'printf \'%s\\n\' "$2" >>"$here/repo.log"\n'
        'if [ -f "$here/refuse.txt" ] && [ "$call" = "$(cat "$here/refuse.txt")" ]; then\n'
        "  echo 'error: refused'\n"
        "  exit 1\n"
        "fi\n"
        f"exit {status}\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


def _calls(wrapper: Path) -> list[str]:
    log = wrapper.parent / "calls.log"
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _ledger_file(root: Path) -> Path:
    return root / "state" / "flow_progress" / "feat_x_progress.md"


def _plant(root: Path, *, p1: str = " ", p2: str = " ", p3: str = " ") -> None:
    (root / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": _STATE_DIR,
                "phases": {"parity": False, "qa": False},
            }
        ),
        encoding="utf-8",
    )
    path = _ledger_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_LEDGER_TEMPLATE.format(p1=p1, p2=p2, p3=p3), encoding="utf-8")


def _ledger(root: Path) -> str:
    return _ledger_file(root).read_text(encoding="utf-8")


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _hooks(root: Path, wrapper: Path) -> PlanningHooks:
    return PlanningHooks(
        _graph(), repo_root=root, state_dir=_STATE_DIR, branch=_BRANCH, commit_wrapper=wrapper
    )


def _end(
    reports: tuple[tuple[str, str], ...] = (),
    passed: tuple[Passage, ...] = (),
) -> End:
    return End("<terminal_handoff>", "convergence", reports, passed)


def _dispatch() -> Dispatch:
    return Dispatch("plan_writer", "task-plan-writer", None, {}, None, None, (), ())


class _Signals:
    def stop_requested(self) -> bool:
        return False

    def pause_requested(self) -> bool:
        return False


class _Counter:
    def __init__(self) -> None:
        self._total = 0

    def total(self) -> int:
        return self._total

    def increment(self) -> int:
        self._total += 1
        return self._total


class _Sink:
    def __init__(self) -> None:
        self.launches: list[Launch] = []

    def record(self, launch: Launch) -> None:
        self.launches.append(launch)


def test_it_provides_exactly_the_planning_graphs_hooks(tmp_path: Path) -> None:
    hooks = _hooks(tmp_path, _plant_wrapper(tmp_path))
    names = ("commit_plan_round", "flip_ledger", "commit_convergence")
    assert [hooks.provides(name) for name in names] == [True, True, True]
    assert hooks.provides("commit_pause") is False


def test_commit_plan_round_commits_the_passages_round(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    call = AfterRound(RoundPassage("plan_round", 3, "fail"), _dispatch())
    asyncio.run(_hooks(tmp_path, wrapper).run("commit_plan_round", call))
    assert _calls(wrapper) == ["plan-round --round 3"]
    assert (wrapper.parent / "repo.log").read_text(encoding="utf-8") == f"{tmp_path}\n"


def test_flip_ledger_flips_and_commits_only_a_planning_entry(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    step = _end(
        passed=(RoundPassage("plan_round", 0, "pass"), LedgerPassage("P1"), LedgerPassage("A"))
    )
    call = AfterRound(RoundPassage("plan_round", 0, "pass"), step)
    asyncio.run(_hooks(tmp_path, wrapper).run("flip_ledger", call))
    assert _calls(wrapper) == ["ledger-flip --entry P1"]
    assert _ledger(tmp_path) == _LEDGER_TEMPLATE.format(p1="x", p2=" ", p3=" ")


def test_flip_ledger_commits_an_already_flipped_entry_again(tmp_path: Path) -> None:
    _plant(tmp_path, p1="x")
    wrapper = _plant_wrapper(tmp_path, status=3)
    call = BeforeEnd(_end(passed=(LedgerPassage("P1"),)))
    asyncio.run(_hooks(tmp_path, wrapper).run("flip_ledger", call))
    assert _calls(wrapper) == ["ledger-flip --entry P1"]
    assert _ledger(tmp_path) == _LEDGER_TEMPLATE.format(p1="x", p2=" ", p3=" ")


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("passed", ["ui-test-plan", "task-plan", "ledger-flip --entry P3"]),
        ("no_ui", ["task-plan", "ledger-flip --entry P3"]),
        ("qa-phase-off", ["task-plan", "ledger-flip --entry P3"]),
        ("run-mode-skipped", ["task-plan", "ledger-flip --entry P3"]),
    ],
)
def test_commit_convergence_follows_the_ui_test_report(
    tmp_path: Path, status: str, expected: list[str]
) -> None:
    _plant(tmp_path, p1="x")
    wrapper = _plant_wrapper(tmp_path)
    call = BeforeEnd(_end(reports=(("plan_review", "passed"), ("ui_test", status))))
    asyncio.run(_hooks(tmp_path, wrapper).run("commit_convergence", call))
    assert _calls(wrapper) == expected
    assert _ledger(tmp_path) == _LEDGER_TEMPLATE.format(p1="x", p2=" ", p3="x")


@pytest.mark.parametrize(
    ("index_on_disk", "expected"),
    [
        (True, ["ui-test-plan", "task-plan", "ledger-flip --entry P3"]),
        (False, ["task-plan", "ledger-flip --entry P3"]),
    ],
)
def test_without_a_ui_test_report_the_ledger_and_the_index_decide(
    tmp_path: Path, index_on_disk: bool, expected: list[str]
) -> None:
    _plant(tmp_path, p1="x", p2="x")
    if index_on_disk:
        index = tmp_path / _UI_TEST_INDEX
        index.parent.mkdir(parents=True)
        index.write_text("# UI-test plan\n", encoding="utf-8")
    wrapper = _plant_wrapper(tmp_path)
    asyncio.run(_hooks(tmp_path, wrapper).run("commit_convergence", BeforeEnd(_end())))
    assert _calls(wrapper) == expected


def test_an_open_p2_writes_no_ui_test_plan_even_with_the_index_on_disk(tmp_path: Path) -> None:
    _plant(tmp_path, p1="x")
    index = tmp_path / _UI_TEST_INDEX
    index.parent.mkdir(parents=True)
    index.write_text("# UI-test plan\n", encoding="utf-8")
    wrapper = _plant_wrapper(tmp_path)
    asyncio.run(_hooks(tmp_path, wrapper).run("commit_convergence", BeforeEnd(_end())))
    assert _calls(wrapper) == ["task-plan", "ledger-flip --entry P3"]


def test_a_hook_on_a_call_kind_it_does_not_take_is_refused(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    hooks = _hooks(tmp_path, wrapper)
    with pytest.raises(ValueError) as round_on_end:
        asyncio.run(hooks.run("commit_plan_round", BeforeEnd(_end())))
    assert str(round_on_end.value) == "hook 'commit_plan_round' does not run on before_end"
    with pytest.raises(ValueError) as flip_on_dispatch:
        asyncio.run(hooks.run("flip_ledger", BeforeDispatch(_dispatch(), 1, 1)))
    assert str(flip_on_dispatch.value) == "hook 'flip_ledger' does not run on before_dispatch"
    assert _calls(wrapper) == []


def test_an_unknown_hook_is_refused(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path)
    with pytest.raises(LookupError) as caught:
        asyncio.run(_hooks(tmp_path, wrapper).run("commit_pause", BeforeEnd(_end())))
    assert str(caught.value) == "PlanningHooks provides no hook 'commit_pause'"


def test_a_refused_commit_propagates(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    (wrapper.parent / "refuse.txt").write_text("plan-round --round 2\n", encoding="utf-8")
    call = AfterRound(RoundPassage("plan_round", 2, "pass"), _dispatch())
    with pytest.raises(CommitPointError) as caught:
        asyncio.run(_hooks(tmp_path, wrapper).run("commit_plan_round", call))
    assert str(caught.value) == "commit-on-branch.sh --artifact plan-round exited 1: refused"


def _executor() -> StubExecutor:
    findings = "state/task_plan_reviews/feat_x/round_0.md"
    return StubExecutor(
        {
            "plan_writer": [ScriptedOutcome("returned"), ScriptedOutcome("returned")],
            "architecture_review": [
                ScriptedOutcome("FAIL", detail=findings),
                ScriptedOutcome("PASS"),
            ],
            "plan_review": [ScriptedOutcome("FAIL", detail=findings), ScriptedOutcome("PASS")],
        }
    )


def _start(root: Path, executor: StubExecutor, hooks: PlanningHooks | None) -> object:
    return asyncio.run(
        start_run(
            open_walker(root, _BRANCH, _graph()),
            executor,
            signals=_Signals(),
            counter=_Counter(),
            sink=_Sink(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome="error",
            hooks=hooks,
        )
    )


_CONVERGED_CALLS = [
    "ledger-flip --entry P1",
    "ledger-flip --entry P1",
    "task-plan",
    "ledger-flip --entry P3",
]


def test_a_run_over_the_planning_graph_commits_in_override_6s_order(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    exit_ = _start(tmp_path, _executor(), _hooks(tmp_path, wrapper))
    assert isinstance(exit_, End), exit_
    assert (exit_.node, exit_.binding) == ("convergence", "<terminal_handoff>")
    assert _calls(wrapper) == ["plan-round --round 0", "plan-round --round 1", *_CONVERGED_CALLS]
    assert _ledger(tmp_path) == _LEDGER_TEMPLATE.format(p1="x", p2=" ", p3="x")


def test_a_run_naming_hooks_with_no_hook_host_is_refused(tmp_path: Path) -> None:
    _plant(tmp_path)
    with pytest.raises(ValueError) as caught:
        _start(tmp_path, _executor(), None)
    assert str(caught.value) == (
        "the graph names hook 'commit_plan_round' and no hook host was given"
    )


def test_a_resume_after_a_refused_commit_re_issues_it_first(tmp_path: Path) -> None:
    _plant(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    refuse = wrapper.parent / "refuse.txt"
    refuse.write_text("plan-round --round 1\n", encoding="utf-8")
    hooks = _hooks(tmp_path, wrapper)
    with pytest.raises(CommitPointError):
        _start(tmp_path, _executor(), hooks)
    assert _calls(wrapper) == ["plan-round --round 0", "plan-round --round 1"]

    refuse.unlink()
    exit_ = asyncio.run(
        continue_run(
            open_walker(tmp_path, _BRANCH, _graph()),
            StubExecutor({}),
            signals=_Signals(),
            counter=_Counter(),
            sink=_Sink(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome="error",
            hooks=hooks,
        )
    )
    assert isinstance(exit_, End), exit_
    assert _calls(wrapper) == [
        "plan-round --round 0",
        "plan-round --round 1",
        "plan-round --round 1",
        *_CONVERGED_CALLS,
    ]
    assert _ledger(tmp_path) == _LEDGER_TEMPLATE.format(p1="x", p2=" ", p3="x")
