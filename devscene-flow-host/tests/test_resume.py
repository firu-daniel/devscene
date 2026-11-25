"""The rule this file exists to enforce: a round's `RoundResume` is built from its files as
`flow-walker.sh`'s `start_round` builds the resumed state — one case per mapping row — on the
harness's own format-4 graph, `cli/templates/scripts/flows/task_plan_writing.graph.json`, and
with every round file PASS no resume carries records, so convergence is never inferred.

Review files and git history are planted under `tmp_path` through `round_fixtures`; the host is a
fixed answer table. Every expected value is a literal `RoundResume` written from `start_round`,
never taken from the output of the code under test.

Deliberately not covered:
- A host answering `None` for a skip predicate: the gate stays in, and `Walker.start` refuses the
  predicate, which is GraphScene's to test.
"""

import os
from collections.abc import Mapping
from pathlib import Path

import pytest
from graphscene import FlowGraph, GateRecord, RoundResume, load_graph_file

from devscene_flow_host.host.resume import round_resume
from devscene_flow_host.records.errors import RecordError
from round_fixtures import FAIL_BODY, PASS_BODY, commit, init_repo, plant_review

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_STATE = "state"
_BRANCH = "feat_x"
_PARITY = "state/business_parity_reviews/feat_x"
_ARCH = "state/architecture_reviews/feat_x"
_PLAN = "state/task_plan_reviews/feat_x"
_STORY_INDEX = "state/story_plans/feat_x_story_plan.md"
_TASK_FILE = "state/task_plans/feat_x/task_1_plan.md"
_NEXT_NOTE = "state/plan_revisions/feat_x/task_plan_revision_4.md"
# `flow-walker.sh` → REPRO's `bad.md`: a FAIL with no numbered entry under `## Must Fix`.
_REFUSED_BODY = "verdict: FAIL\n"


class _Host:
    def __init__(self, answers: Mapping[str, bool]) -> None:
        self._answers = answers

    def answer(self, predicate: str, node: str) -> bool | None:
        return self._answers.get(predicate, False)


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _resume(
    root: Path, entry: str, answers: Mapping[str, bool] | None = None
) -> RoundResume | None:
    return round_resume(_graph(), _Host(answers or {}), root, _STATE, _BRANCH, entry)


def _plant(root: Path, reviews: Mapping[str, str]) -> None:
    """A repository whose story index, task file and round-3 review files under `reviews`
    (folder → body) are committed together."""
    init_repo(root)
    planted = []
    for relative in (_STORY_INDEX, _TASK_FILE):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("plan\n", encoding="utf-8")
        planted.append(path)
    for folder, body in reviews.items():
        planted.append(plant_review(root / folder, 3, body))
    commit(root, planted, "round 3")


def test_no_round_file_has_no_resume(tmp_path: Path) -> None:
    _plant(tmp_path, {})
    assert _resume(tmp_path, "plan_round") is None


def test_the_writer_entry_after_round_3_opens_round_4(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY, _PLAN: PASS_BODY})
    assert _resume(tmp_path, "plan_writer") == RoundResume("plan_round", 4)


def test_consistent_missing_files_record_the_present_gates(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY})
    assert _resume(tmp_path, "plan_round") == RoundResume(
        "plan_round",
        3,
        (
            GateRecord(
                "business_parity_review", "PASS", "state/business_parity_reviews/feat_x/review_3.md"
            ),
            GateRecord(
                "architecture_review", "FAIL", "state/architecture_reviews/feat_x/review_3.md"
            ),
        ),
    )


def test_missing_files_after_a_later_plan_commit_open_the_whole_set(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY})
    (tmp_path / _STORY_INDEX).write_text("plan changed\n", encoding="utf-8")
    commit(tmp_path, [tmp_path / _STORY_INDEX], "plan")
    assert _resume(tmp_path, "plan_round") == RoundResume("plan_round", 3)


def test_missing_files_beside_an_unreadable_one_open_the_whole_set(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: _REFUSED_BODY})
    assert _resume(tmp_path, "plan_round") == RoundResume("plan_round", 3)


def test_a_complete_round_of_passes_is_reviewed_again_without_records(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: PASS_BODY, _PLAN: PASS_BODY})
    assert _resume(tmp_path, "plan_round") == RoundResume("plan_round", 3)


def test_a_fail_with_the_next_note_opens_the_next_round(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY, _PLAN: PASS_BODY})
    note = tmp_path / _NEXT_NOTE
    note.parent.mkdir(parents=True)
    note.write_text("note\n", encoding="utf-8")
    assert _resume(tmp_path, "plan_round") == RoundResume("plan_round", 4)


def test_a_fail_without_the_next_note_records_every_verdict(tmp_path: Path) -> None:
    _plant(tmp_path, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY, _PLAN: PASS_BODY})
    assert _resume(tmp_path, "plan_round") == RoundResume(
        "plan_round",
        3,
        (
            GateRecord(
                "business_parity_review", "PASS", "state/business_parity_reviews/feat_x/review_3.md"
            ),
            GateRecord(
                "architecture_review", "FAIL", "state/architecture_reviews/feat_x/review_3.md"
            ),
            GateRecord("plan_review", "PASS", "state/task_plan_reviews/feat_x/review_3.md"),
        ),
    )


def test_a_gate_skipped_on_this_arrival_is_left_out_of_the_evidence(tmp_path: Path) -> None:
    _plant(tmp_path, {_ARCH: FAIL_BODY, _PLAN: PASS_BODY})
    # A later parity file would raise the round to 5 if the skipped gate were read.
    plant_review(tmp_path / _PARITY, 5, PASS_BODY)
    assert _resume(tmp_path, "plan_round", {"phase_parity_off": True}) == RoundResume(
        "plan_round",
        3,
        (
            GateRecord(
                "architecture_review", "FAIL", "state/architecture_reviews/feat_x/review_3.md"
            ),
            GateRecord("plan_review", "PASS", "state/task_plan_reviews/feat_x/review_3.md"),
        ),
    )


def test_a_root_git_cannot_answer_in_names_the_round(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "not_a_repo"
    plant_review(root / _PLAN, 3, PASS_BODY)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    with pytest.raises(RecordError) as raised:
        _resume(root, "plan_round")
    assert str(raised.value) == (
        f"cannot read the round evidence of 'plan_round': git cannot answer in {root}"
    )
