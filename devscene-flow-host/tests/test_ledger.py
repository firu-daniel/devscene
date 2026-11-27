"""The rule this file exists to enforce: `read_run_mode` reads the run mode's skipped ids as the
bash walker's `fw_run_mode_skipped` does — the ledger's `## Run mode` block wins, the caller's ids
are used only when no ledger exists, and neither answering is a `RunModeUnresolved` with one exact
reason — and `parse_skipped` reads a list as `fw_id_in_list` does; and `read_planning_marks` reads
the `P1`-`P3` marks as `pd_ledger_read` does — a line opening with a mark and `<entry>.` sets the
mark, the last such line wins, no such line is `None`, and an unreadable ledger is a `RecordError`
with one exact message; and `read_run_mode_entries` reads the `## Run mode` section's `- skipped:`
value and `- ignored:` entries as `pd_run_mode_line` did, and nothing outside that section; and
`require_ledger` passes an existing ledger and raises for a missing one with the message both
readers give.

Every ledger is planted under `tmp_path`; every expected value is written from the rules in the
task plan, never taken from the output of the code under test.

Deliberately not covered:
- An `OSError` other than a missing ledger, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.ledger import (
    IgnoredEntry,
    PlanningMarks,
    RunMode,
    RunModeEntries,
    RunModeUnresolved,
    ledger_path,
    parse_skipped,
    read_planning_marks,
    read_run_mode,
    read_run_mode_entries,
    require_ledger,
)

_NO_SKIPPED_LINE = RunModeUnresolved(
    "the flow-progress ledger for 'feat_x' has no '- skipped:' line under '## Run mode'"
)
_NO_RECORD = RunModeUnresolved(
    "no run-mode record: no flow-progress ledger for 'feat_x' and no skipped ids given"
)


def _plant(root: Path, data: bytes) -> Path:
    path = ledger_path(root, "state", "feat_x")
    path.parent.mkdir(parents=True)
    path.write_bytes(data)
    return path


def test_the_ledger_path_is_under_the_state_dir(tmp_path: Path) -> None:
    assert ledger_path(tmp_path, "state", "feat_x") == (
        tmp_path / "state" / "flow_progress" / "feat_x_progress.md"
    )


def test_the_ledger_as_the_harness_writes_it(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"## Run mode\n"
        b"Source: state/task_prompts/feat_x_task_prompt.md \xe2\x86\x92 `### Run mode`\n"
        b"- skipped: none\n"
        b"- phases: parity=false, qa=true, docs=false\n"
        b"\n"
        b"## Planning\n"
        b"- P1 done\n",
    )
    assert read_run_mode(tmp_path, "state", "feat_x", None) == RunMode(frozenset(), "ledger")


def test_the_ledger_wins_over_the_given_ids(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: parity, qa\n")
    assert read_run_mode(tmp_path, "state", "feat_x", "architecture") == RunMode(
        frozenset({"parity", "qa"}), "ledger"
    )


def test_trailing_whitespace_and_carriage_returns_are_tolerated(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode \r\n- skipped: qa\r\n")
    assert read_run_mode(tmp_path, "state", "feat_x", None) == RunMode(frozenset({"qa"}), "ledger")


def test_a_skipped_line_outside_the_run_mode_block_is_not_read(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Planning\n- skipped: qa\n")
    assert read_run_mode(tmp_path, "state", "feat_x", "qa") == _NO_SKIPPED_LINE


def test_a_run_mode_block_without_a_skipped_line_is_unresolved(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- phases: parity=false\n## Planning\n- skipped: qa\n")
    assert read_run_mode(tmp_path, "state", "feat_x", None) == _NO_SKIPPED_LINE


def test_an_empty_skipped_value_is_unresolved(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: \n")
    assert read_run_mode(tmp_path, "state", "feat_x", "qa") == _NO_SKIPPED_LINE


def test_without_a_ledger_the_given_ids_are_used(tmp_path: Path) -> None:
    assert read_run_mode(tmp_path, "state", "feat_x", "architecture") == RunMode(
        frozenset({"architecture"}), "argument"
    )


@pytest.mark.parametrize("skipped", [None, ""])
def test_without_a_ledger_or_ids_the_run_mode_is_unresolved(
    tmp_path: Path, skipped: str | None
) -> None:
    assert read_run_mode(tmp_path, "state", "feat_x", skipped) == _NO_RECORD


def test_a_ledger_that_is_not_utf8_raises(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Run mode\n- skipped: \xff\n")
    with pytest.raises(RecordError) as raised:
        read_run_mode(tmp_path, "state", "feat_x", None)
    assert str(raised.value) == f"{path}: not UTF-8 text"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("none", frozenset()),
        (" a , none, b ", frozenset({"a", "b"})),
        ("", frozenset()),
    ],
)
def test_parse_skipped(value: str, expected: frozenset[str]) -> None:
    assert parse_skipped(value) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"- [x] P1. a\n- [-] P2. b\n- [ ] P3. c\n", PlanningMarks(p1="x", p2="-", p3=" ")),
        (b"- [-] P1. a\n- [ ] P2. b\n- [x] P3. c\n", PlanningMarks(p1="-", p2=" ", p3="x")),
        (b"- [ ] P1. a\n- [x] P2. b\n- [-] P3. c\n", PlanningMarks(p1=" ", p2="x", p3="-")),
    ],
)
def test_each_mark_is_read_for_each_entry(
    tmp_path: Path, data: bytes, expected: PlanningMarks
) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: none\n\n## Planning\n" + data)
    assert read_planning_marks(tmp_path, "state", "feat_x") == expected


def test_an_entry_with_no_line_is_none(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Planning\n- [x] P1. plan\n- [x] P3. ui\n")
    assert read_planning_marks(tmp_path, "state", "feat_x") == PlanningMarks(
        p1="x", p2=None, p3="x"
    )


def test_the_last_line_for_an_entry_wins(tmp_path: Path) -> None:
    _plant(tmp_path, b"- [x] P2. first\n- [ ] P2. second\n")
    assert read_planning_marks(tmp_path, "state", "feat_x") == PlanningMarks(
        p1=None, p2=" ", p3=None
    )


def test_a_mark_after_leading_text_does_not_match(tmp_path: Path) -> None:
    _plant(tmp_path, b"note: - [x] P1. plan\n  - [x] P1. plan\n")
    assert read_planning_marks(tmp_path, "state", "feat_x") == PlanningMarks(
        p1=None, p2=None, p3=None
    )


def test_a_missing_ledger_raises_for_the_planning_marks(tmp_path: Path) -> None:
    path = tmp_path / "state" / "flow_progress" / "feat_x_progress.md"
    with pytest.raises(RecordError) as raised:
        read_planning_marks(tmp_path, "state", "feat_x")
    assert str(raised.value) == f"the flow-progress ledger '{path}' does not exist"


def test_a_ledger_that_is_not_utf8_raises_for_the_planning_marks(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"- [x] P1. \xff\n")
    with pytest.raises(RecordError) as raised:
        read_planning_marks(tmp_path, "state", "feat_x")
    assert str(raised.value) == f"{path}: not UTF-8 text"


def test_the_skipped_value_is_cut_before_its_comment(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: qa, docs   (from the task prompt)\n")
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="qa, docs", ignored=()
    )


def test_a_skipped_none_is_read_as_none(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: none\n")
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="none", ignored=()
    )


def test_no_skipped_line_reads_as_empty(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- phases: qa=true\n")
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="", ignored=()
    )


def test_a_later_skipped_line_overwrites_an_earlier_one(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\n- skipped: qa\n- skipped: docs\n")
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="docs", ignored=()
    )


def test_ignored_entries_split_at_the_last_reason(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"## Run mode\n"
        b"- skipped: none\n"
        b"- ignored: skip the (whole) review (not a directive (see run-mode))\n"
        b"- ignored: go fast\n",
    )
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="none",
        ignored=(
            IgnoredEntry(
                text="skip the (whole) review (not a directive",
                reason="see run-mode))",
            ),
            IgnoredEntry(text="go fast", reason=None),
        ),
    )


def test_lines_under_a_later_heading_are_not_read(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"- skipped: early\n"
        b"## Run mode\n"
        b"- skipped: qa\n"
        b"## Planning\n"
        b"- skipped: docs\n"
        b"- ignored: late\n",
    )
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="qa", ignored=()
    )


def test_a_crlf_ledger_is_read_without_its_carriage_returns(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Run mode\r\n- skipped: qa\r\n- ignored: go fast (vague)\r\n")
    assert read_run_mode_entries(tmp_path, "state", "feat_x") == RunModeEntries(
        skipped="qa", ignored=(IgnoredEntry(text="go fast", reason="vague)"),)
    )


def test_a_missing_ledger_raises_for_the_run_mode_entries(tmp_path: Path) -> None:
    path = tmp_path / "state" / "flow_progress" / "feat_x_progress.md"
    with pytest.raises(RecordError) as raised:
        read_run_mode_entries(tmp_path, "state", "feat_x")
    assert str(raised.value) == f"the flow-progress ledger '{path}' does not exist"


def test_a_ledger_that_is_not_utf8_raises_for_the_run_mode_entries(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Run mode\n- skipped: \xff\n")
    with pytest.raises(RecordError) as raised:
        read_run_mode_entries(tmp_path, "state", "feat_x")
    assert str(raised.value) == f"{path}: not UTF-8 text"


def test_an_existing_ledger_is_required_without_raising(tmp_path: Path) -> None:
    _plant(tmp_path, b"")
    require_ledger(tmp_path, "state", "feat_x")


def test_a_missing_ledger_raises_when_required(tmp_path: Path) -> None:
    path = tmp_path / "state" / "flow_progress" / "feat_x_progress.md"
    with pytest.raises(RecordError) as raised:
        require_ledger(tmp_path, "state", "feat_x")
    assert str(raised.value) == f"the flow-progress ledger '{path}' does not exist"
