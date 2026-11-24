"""The rule this file exists to enforce: a round's evidence is read as the bash walker's
`fw_round_evidence` reads it — the highest round number over the gate folders, each gate's status
at that number, the next revision note, and the plan's freshness asked of `git` — and a root `git`
cannot answer in is a `RecordError` reading `git cannot answer in <root>`.

Every repository is planted under `tmp_path` through `round_fixtures`; every expected value is a
literal written from `fw_round_evidence`'s `REPRO` lines, never taken from the output of the code
under test. `git` runs with the machine's configuration shut out, as `round_fixtures` runs it.

Deliberately not covered:
- A missing `git` binary: no portable way to remove it from a test's `PATH` while the fixtures
  still need it.
"""

import os
from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.round_evidence import (
    GateEvidence,
    RoundEvidence,
    read_round_evidence,
)
from round_fixtures import FAIL_BODY, PASS_BODY, commit, init_repo, plant_review

# `flow-walker.sh` → REPRO's `bad.md`: a FAIL with no numbered entry under `## Must Fix`.
_REFUSED_BODY = "verdict: FAIL\n"


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _repro(root: Path) -> None:
    """REPRO's `round verdicts` setup: `g/review_0.md` FAIL and `plan.md`, committed together."""
    init_repo(root)
    (root / "plan.md").write_text("", encoding="utf-8")
    plant_review(root / "g", 0, FAIL_BODY)
    commit(root, [root / "g" / "review_0.md", root / "plan.md"], "r")


def _read(root: Path, *gates: tuple[str, Path]) -> RoundEvidence:
    return read_round_evidence(root, str(root / "n_{round}.md"), [root / "plan.md"], gates)


def test_no_review_file_is_round_none(tmp_path: Path) -> None:
    _repro(tmp_path)
    assert _read(tmp_path, ("b", tmp_path / "h")) == RoundEvidence(None, (), False, "unknown")


def test_round_zero_with_one_gate_fail_and_one_missing(tmp_path: Path) -> None:
    _repro(tmp_path)
    assert _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h")) == RoundEvidence(
        0,
        (
            GateEvidence("a", "FAIL", tmp_path / "g" / "review_0.md"),
            GateEvidence("b", "missing", tmp_path / "h" / "review_0.md"),
        ),
        False,
        "not-newer",
    )


def test_the_next_note_and_an_uncommitted_plan_edit(tmp_path: Path) -> None:
    _repro(tmp_path)
    (tmp_path / "n_1.md").write_text("", encoding="utf-8")
    with (tmp_path / "plan.md").open("a", encoding="utf-8") as plan:
        plan.write("x\n")
    evidence = _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h"))
    assert (evidence.note_present, evidence.plan) == (True, "newer")


def test_a_plan_commit_after_the_rounds_files_is_newer(tmp_path: Path) -> None:
    _repro(tmp_path)
    (tmp_path / "plan.md").write_text("x\n", encoding="utf-8")
    commit(tmp_path, [tmp_path / "plan.md"], "plan")
    evidence = _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h"))
    assert (evidence.note_present, evidence.plan) == (False, "newer")


def test_a_present_uncommitted_review_file_is_unknown(tmp_path: Path) -> None:
    _repro(tmp_path)
    plant_review(tmp_path / "h", 0, PASS_BODY)
    assert _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h")) == RoundEvidence(
        0,
        (
            GateEvidence("a", "FAIL", tmp_path / "g" / "review_0.md"),
            GateEvidence("b", "PASS", tmp_path / "h" / "review_0.md"),
        ),
        False,
        "unknown",
    )


def test_a_present_file_the_check_refuses_is_unreadable(tmp_path: Path) -> None:
    _repro(tmp_path)
    plant_review(tmp_path / "h", 0, _REFUSED_BODY)
    commit(tmp_path, [tmp_path / "h" / "review_0.md"], "h")
    assert _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h")).gates == (
        GateEvidence("a", "FAIL", tmp_path / "g" / "review_0.md"),
        GateEvidence("b", "unreadable", tmp_path / "h" / "review_0.md"),
    )


def test_a_valid_pass_at_the_round_another_gate_reached_is_pass(tmp_path: Path) -> None:
    _repro(tmp_path)
    plant_review(tmp_path / "g", 1, FAIL_BODY)
    plant_review(tmp_path / "h", 1, PASS_BODY)
    commit(tmp_path, [tmp_path / "g" / "review_1.md", tmp_path / "h" / "review_1.md"], "r1")
    assert _read(tmp_path, ("a", tmp_path / "g"), ("b", tmp_path / "h")) == RoundEvidence(
        1,
        (
            GateEvidence("a", "FAIL", tmp_path / "g" / "review_1.md"),
            GateEvidence("b", "PASS", tmp_path / "h" / "review_1.md"),
        ),
        False,
        "not-newer",
    )


def test_a_root_git_cannot_answer_in_is_a_record_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "not_a_repo"
    plant_review(root / "g", 0, FAIL_BODY)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    with pytest.raises(RecordError) as raised:
        _read(root, ("a", root / "g"))
    assert str(raised.value) == f"git cannot answer in {root}"
