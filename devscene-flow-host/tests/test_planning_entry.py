"""The rule this file exists to enforce: `decide_planning_entry` decides where a planning walk
enters as `planning-driver-lib.sh` → `pd_entry` does — planning done when `P1`–`P3` are resolved;
a usable saved dispatch continued, carrying the writer pairs only to a writer; a usable parked
`<ask>` continued with `answered` only when there are writer pairs, so the writer keeps its saved
variant (#325); otherwise a start at the first of its six entries that holds — with the pairs
`pd_pairs` keeps, the usability `pd_walk_usable` and `pd_block_usable` test, and the ledger loops
derived from the graph.

Every configuration, ledger, index and clarification pair is planted under `tmp_path`; the graph
is the real `cli/templates/scripts/flows/task_plan_writing.graph.json`, read only, and every saved
walk is produced by driving the real `Walker`. Every expected value is a literal written from the
task plan's contract and `pd_entry`, never taken from the code under test.
"""

import json
import os
from pathlib import Path
from typing import Final

import pytest
from graphscene import (
    Dispatch,
    FlowGraph,
    Interrupt,
    RoundResume,
    Stop,
    Walker,
    load_graph_file,
)

from devscene_flow_host.host.planning_entry import (
    CONVERGENCE_ENTRY,
    PLAN_ROUND_ENTRY,
    PLAN_WRITER_ENTRY,
    STORY_INDEX_PATH,
    UI_REVIEW_ENTRY,
    UI_WRITER_ENTRY,
    ContinueWalk,
    PlanningDone,
    StartWalk,
    _ledger_loop,
    decide_planning_entry,
)
from devscene_flow_host.host.planning_hooks import UI_TEST_INDEX_PATH
from devscene_flow_host.host.walking import open_walker
from devscene_flow_host.records.clarifications import AnsweredPair
from round_fixtures import FAIL_BODY, commit, init_repo, plant_review

_GRAPH: Final = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_BRANCH: Final = "feat_x"
_STATE_DIR: Final = "state"
_STORY_INDEX: Final = "state/story_plans/feat_x_story_plan.md"
_UI_TEST_INDEX: Final = "state/ui_test_plans/feat_x_ui_test_plan.md"
_CLARIFICATIONS: Final = "state/clarifications/feat_x"
_PLAN_REVIEW_0: Final = "state/task_plan_reviews/feat_x/review_0.md"
_ARCH_REVIEW_0: Final = "state/architecture_reviews/feat_x/review_0.md"
_LEDGER_TEMPLATE: Final = (
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


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _plant(
    root: Path,
    *,
    p1: str = " ",
    p2: str = " ",
    p3: str = " ",
    story: bool = False,
    ui_index: bool = False,
) -> Walker:
    """Parity off and QA on, so a plan round's set is `architecture_review` and `plan_review`
    and `ui_writer` is dispatched rather than skipped."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": _STATE_DIR,
                "phases": {"parity": False, "qa": True},
            }
        ),
        encoding="utf-8",
    )
    ledger = root / "state" / "flow_progress" / "feat_x_progress.md"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(_LEDGER_TEMPLATE.format(p1=p1, p2=p2, p3=p3), encoding="utf-8")
    for wanted, relative in ((story, _STORY_INDEX), (ui_index, _UI_TEST_INDEX)):
        if wanted:
            _write(root / relative, "index\n")
    return open_walker(root, _BRANCH, _graph())


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _pair(root: Path, n: int, raised_by: str) -> AnsweredPair:
    _write(root / _CLARIFICATIONS / f"question_{n}.md", f"Raised by: {raised_by}\n## Question\nq\n")
    _write(root / _CLARIFICATIONS / f"answer_{n}.md", "a\n")
    return AnsweredPair(
        index=n,
        question=f"{_CLARIFICATIONS}/question_{n}.md",
        answer=f"{_CLARIFICATIONS}/answer_{n}.md",
        raised_by=raised_by,
    )


def _decide(walker: Walker, root: Path) -> object:
    return decide_planning_entry(walker, root, _STATE_DIR, _BRANCH)


def _revision_of_plan_writer(walker: Walker, findings: str) -> Dispatch:
    """Round 0 closes FAIL on `findings`, so `plan_writer` is dispatched with `revision`."""
    walker.start(PLAN_WRITER_ENTRY)
    walker.next("returned")
    walker.next("PASS", "architecture_review", _ARCH_REVIEW_0)
    step = walker.next("FAIL", "plan_review", findings)
    assert isinstance(step, Dispatch), step
    assert (step.node, step.prompt) == ("plan_writer", "revision")
    return step


# --- The decision order ------------------------------------------------------------------------


def test_p1_p2_and_p3_resolved_is_planning_done(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x", p2="-", p3="x")
    walker.start(PLAN_WRITER_ENTRY)
    _pair(tmp_path, 1, "task-plan-writer")
    assert _decide(walker, tmp_path) == PlanningDone()


def test_a_usable_pending_writer_dispatch_is_continued_with_the_pairs(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    walker.start(PLAN_WRITER_ENTRY)
    pair = _pair(tmp_path, 1, "task-plan-writer")
    assert _decide(walker, tmp_path) == ContinueWalk(None, (pair,))


def test_a_usable_pending_gate_set_is_continued_without_the_pairs(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    walker.start(PLAN_ROUND_ENTRY)
    _pair(tmp_path, 1, "task-plan-writer")
    assert _decide(walker, tmp_path) == ContinueWalk(None, ())


def test_an_answered_park_after_a_revision_resumes_the_writer_with_revision(
    tmp_path: Path,
) -> None:
    walker = _plant(tmp_path, story=True)
    _revision_of_plan_writer(walker, _PLAN_REVIEW_0)
    parked = walker.next("questions")
    assert isinstance(parked, Interrupt), parked
    pair = _pair(tmp_path, 1, "task-plan-writer")

    assert _decide(walker, tmp_path) == ContinueWalk("answered", (pair,))
    resumed = walker.next("answered")
    assert isinstance(resumed, Dispatch), resumed
    assert (resumed.node, resumed.prompt) == ("plan_writer", "revision")


def test_a_parked_walk_with_no_pairs_falls_through_to_a_start(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    walker.start(PLAN_WRITER_ENTRY)
    assert isinstance(walker.next("questions"), Interrupt)
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, ())


def test_a_stopped_walk_falls_through_to_a_start(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    walker.start(PLAN_WRITER_ENTRY)
    assert isinstance(walker.next("error"), Stop)
    pair = _pair(tmp_path, 1, "task-plan-writer")
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, (pair,))


def test_writer_pairs_start_at_plan_writer(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x", story=True)
    pair = _pair(tmp_path, 1, "task-plan-reviewer")
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, (pair,))


def test_a_ui_pair_starts_at_ui_writer(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    first = _pair(tmp_path, 1, "task-plan-writer")
    second = _pair(tmp_path, 2, "ui-tests-plan-reviewer (round 1)")
    assert _decide(walker, tmp_path) == StartWalk(UI_WRITER_ENTRY, None, (first, second))


def test_p1_done_and_p2_resolved_starts_at_convergence(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x", p2="-")
    assert _decide(walker, tmp_path) == StartWalk(CONVERGENCE_ENTRY, None, ())


def test_p1_done_with_the_ui_test_index_starts_at_ui_review(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x", ui_index=True)
    assert _decide(walker, tmp_path) == StartWalk(UI_REVIEW_ENTRY, None, ())


def test_p1_done_alone_starts_at_ui_writer(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x")
    assert _decide(walker, tmp_path) == StartWalk(UI_WRITER_ENTRY, None, ())


def test_the_story_index_alone_starts_at_plan_round(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    assert _decide(walker, tmp_path) == StartWalk(PLAN_ROUND_ENTRY, None, ())


def test_nothing_on_disk_starts_fresh_at_plan_writer(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, ())


def test_a_start_carries_round_resumes_resume_for_its_entry(tmp_path: Path) -> None:
    """A writer entry over a round-0 review file resumes `plan_round` at round 1."""
    init_repo(tmp_path)
    walker = _plant(tmp_path, story=True)
    review = plant_review(tmp_path / "state" / "task_plan_reviews" / "feat_x", 0, FAIL_BODY)
    commit(tmp_path, [tmp_path / _STORY_INDEX, review], "round 0")
    pair = _pair(tmp_path, 1, "task-plan-writer")
    assert _decide(walker, tmp_path) == StartWalk(
        PLAN_WRITER_ENTRY, RoundResume("plan_round", 1), (pair,)
    )


def test_phase_g_and_screen_pairs_are_left_out(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    _pair(tmp_path, 1, "Phase G (implementation review)")
    _pair(tmp_path, 2, "prompt-injection-reviewer (prompt-injection screen) of question_1.md")
    assert _decide(walker, tmp_path) == StartWalk(PLAN_ROUND_ENTRY, None, ())


def test_a_left_out_ui_origin_does_not_send_the_entry_to_ui_writer(tmp_path: Path) -> None:
    walker = _plant(tmp_path)
    _pair(tmp_path, 1, "Phase G ui-tests-plan-writer")
    kept = _pair(tmp_path, 2, "task-plan-writer")
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, (kept,))


# --- Usability ---------------------------------------------------------------------------------


def test_p1_done_makes_a_p1_loop_step_unusable(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x")
    walker.start(PLAN_WRITER_ENTRY)
    assert _decide(walker, tmp_path) == StartWalk(UI_WRITER_ENTRY, None, ())


def test_p2_resolved_makes_a_p2_loop_step_unusable(tmp_path: Path) -> None:
    walker = _plant(tmp_path, p1="x", p2="-", story=True)
    walker.start(UI_WRITER_ENTRY)
    assert _decide(walker, tmp_path) == StartWalk(CONVERGENCE_ENTRY, None, ())


def test_p1_open_makes_a_p2_loop_step_without_the_p1_passage_unusable(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    walker.start(UI_WRITER_ENTRY)
    assert _decide(walker, tmp_path) == StartWalk(PLAN_ROUND_ENTRY, None, ())


def test_p1_open_keeps_a_p2_loop_step_carrying_the_p1_passage_usable(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    walker.start(PLAN_ROUND_ENTRY)
    walker.next("PASS", "architecture_review", _ARCH_REVIEW_0)
    step = walker.next("PASS", "plan_review", _PLAN_REVIEW_0)
    assert isinstance(step, Dispatch), step
    assert step.node == "ui_writer"
    pair = _pair(tmp_path, 1, "ui-tests-plan-writer")
    assert _decide(walker, tmp_path) == ContinueWalk(None, (pair,))


def test_a_missing_story_index_makes_a_gate_set_unusable(tmp_path: Path) -> None:
    walker = _plant(tmp_path, story=True)
    walker.start(PLAN_ROUND_ENTRY)
    (tmp_path / _STORY_INDEX).unlink()
    assert _decide(walker, tmp_path) == StartWalk(PLAN_WRITER_ENTRY, None, ())


def test_a_missing_findings_file_makes_a_revision_unusable(tmp_path: Path) -> None:
    """No review file of the closed round is on disk, so the start has no resume."""
    walker = _plant(tmp_path, story=True)
    _revision_of_plan_writer(walker, _PLAN_REVIEW_0)
    assert _decide(walker, tmp_path) == StartWalk(PLAN_ROUND_ENTRY, None, ())


def test_present_findings_files_keep_a_revision_usable(tmp_path: Path) -> None:
    """The closed round carries both gates' files, so both must be on disk."""
    walker = _plant(tmp_path, story=True)
    _revision_of_plan_writer(walker, _PLAN_REVIEW_0)
    _write(tmp_path / _PLAN_REVIEW_0, FAIL_BODY)
    _write(tmp_path / _ARCH_REVIEW_0, "verdict: PASS\n")
    assert _decide(walker, tmp_path) == ContinueWalk(None, ())


# --- The derived loops and the constants -------------------------------------------------------


def test_the_ledger_loops_are_derived_from_the_real_graph() -> None:
    graph = _graph()
    assert _ledger_loop(graph, "P1") == {
        "plan_round",
        "business_parity_review",
        "architecture_review",
        "plan_review",
        "plan_writer",
    }
    assert _ledger_loop(graph, "P2") == {"ui_writer", "ui_review"}


def test_every_entry_and_path_constant_is_in_the_real_graph() -> None:
    graph = _graph()
    for entry in (
        PLAN_WRITER_ENTRY,
        PLAN_ROUND_ENTRY,
        UI_WRITER_ENTRY,
        UI_REVIEW_ENTRY,
        CONVERGENCE_ENTRY,
    ):
        assert entry in graph.entries, entry
    assert STORY_INDEX_PATH in graph.paths
    assert UI_TEST_INDEX_PATH in graph.paths
