"""The rule this file exists to enforce: the harness's own format-4 graph,
`cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, loads through every library check
and walks through `open_walker` on records planted under `tmp_path`: phases and the run mode
decide each skip, an unanswerable predicate refuses without writing, and each branch walks in
its own state file.

Every expected value is hand-written from reading the graph file and the engine's rules, never
taken from the walker's output.

Deliberately not covered:
- The walker's refusal texts and the state file's codec beyond the two refusals quoted here:
  GraphScene's own suites cover them.
"""

import json
from pathlib import Path

from graphscene import (
    Dispatch,
    DispatchSet,
    End,
    FlowGraph,
    LedgerPassage,
    Refused,
    RoundPassage,
    SkipPassage,
    Wait,
    load_graph_file,
)

from devscene_flow_host.host.predicates import HarnessPredicateHost
from devscene_flow_host.host.walking import open_walker

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.v4.graph.json"
)
_BRANCH = "feat_x"
_UNANSWERED_LEDGER_REASON = (
    "the flow-progress ledger for 'feat_x' has no '- skipped:' line under '## Run mode'"
)


def _plant(root: Path, phases: dict[str, bool], ledger: str | None = None) -> None:
    (root / "devscene.config.json").write_text(
        json.dumps({"stateDir": "state", "phases": phases}), encoding="utf-8"
    )
    if ledger is not None:
        path = root / "state" / "flow_progress" / f"{_BRANCH}_progress.md"
        path.parent.mkdir(parents=True)
        path.write_text(ledger, encoding="utf-8")


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _assert_plan_writer(step: object) -> None:
    """A first dispatch has no prompt: the engine sets one only from an arriving edge's `prompt`."""
    assert isinstance(step, Dispatch), step
    assert (step.node, step.agent, step.prompt) == ("plan_writer", "task-plan-writer", None)


def test_the_harness_graph_loads_through_every_check() -> None:
    assert _graph().flow == "task_plan_writing"


def test_phases_off_skip_parity_and_qa(tmp_path: Path) -> None:
    _plant(tmp_path, {"parity": False, "qa": False})
    walker = open_walker(tmp_path, _BRANCH, _graph(), skipped="none")

    _assert_plan_writer(walker.start())

    round_step = walker.next("returned")
    assert isinstance(round_step, DispatchSet), round_step
    assert (round_step.round, round_step.number) == ("plan_round", 0)
    assert [dispatch.node for dispatch in round_step.dispatches] == [
        "architecture_review",
        "plan_review",
    ]
    assert round_step.passed == (SkipPassage("business_parity_review", "skipped"),)

    assert isinstance(walker.next("PASS", node="architecture_review"), Wait)

    end = walker.next("PASS", node="plan_review")
    assert isinstance(end, End), end
    assert (end.node, end.binding) == ("convergence", "<terminal_handoff>")
    assert end.passed == (
        RoundPassage("plan_round", 0, "pass"),
        LedgerPassage("P1"),
        SkipPassage("ui_writer", "skipped"),
    )
    assert end.reports == (
        ("business_parity_review", "skipped"),
        ("architecture_review", "passed"),
        ("plan_review", "passed"),
        ("ui_test", "qa-phase-off"),
    )


def test_the_ledgers_run_mode_wins_over_phases_on_and_the_argument(tmp_path: Path) -> None:
    _plant(tmp_path, {"parity": True, "qa": True}, "## Run mode\n- skipped: parity, qa\n")
    walker = open_walker(tmp_path, _BRANCH, _graph(), skipped="none")

    _assert_plan_writer(walker.start())

    round_step = walker.next("returned")
    assert isinstance(round_step, DispatchSet), round_step
    assert round_step.passed == (SkipPassage("business_parity_review", "passed-by-exclusion"),)

    assert isinstance(walker.next("PASS", node="architecture_review"), Wait)

    end = walker.next("PASS", node="plan_review")
    assert isinstance(end, End), end
    assert end.passed == (
        RoundPassage("plan_round", 0, "pass"),
        LedgerPassage("P1"),
        SkipPassage("ui_writer", "passed-by-exclusion"),
    )
    assert end.reports == (
        ("business_parity_review", "passed-by-exclusion"),
        ("architecture_review", "passed"),
        ("plan_review", "passed"),
        ("ui_test", "run-mode-skipped"),
    )


def test_an_unanswerable_predicate_refuses_and_writes_nothing(tmp_path: Path) -> None:
    _plant(tmp_path, {"parity": True, "qa": True}, "## Run mode\n- directives: none\n")
    graph = _graph()
    walker = open_walker(tmp_path, _BRANCH, graph)

    _assert_plan_writer(walker.start())
    assert walker.next("returned") == Refused(
        "the host cannot answer predicate 'run_mode_skips_parity' for node 'business_parity_review'"
    )
    _assert_plan_writer(open_walker(tmp_path, _BRANCH, graph).current())
    assert (
        HarnessPredicateHost(tmp_path, _BRANCH).refusal_reason("run_mode_skips_parity")
        == _UNANSWERED_LEDGER_REASON
    )


def test_each_branch_walks_in_its_own_state_file(tmp_path: Path) -> None:
    _plant(tmp_path, {"parity": False, "qa": False})
    graph = _graph()

    _assert_plan_writer(open_walker(tmp_path, "feat/a", graph, skipped="none").start())

    assert open_walker(tmp_path, "feat/b", graph, skipped="none").current() == Refused(
        "no walk has started"
    )
    _assert_plan_writer(open_walker(tmp_path, "feat/a", graph, skipped="none").current())
    state_files = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*.json"))
    assert state_files == ["devscene.config.json", "state/.flow_walker_state/feat%2Fa.json"]
