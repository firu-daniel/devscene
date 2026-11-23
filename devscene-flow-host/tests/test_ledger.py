"""The rule this file exists to enforce: `read_run_mode` reads the run mode's skipped ids as the
bash walker's `fw_run_mode_skipped` does — the ledger's `## Run mode` block wins, the caller's ids
are used only when no ledger exists, and neither answering is a `RunModeUnresolved` with one exact
reason — and `parse_skipped` reads a list as `fw_id_in_list` does.

Every ledger is planted under `tmp_path`; every expected value is written from the rules in the
task plan, never taken from `read_run_mode`'s output.

Deliberately not covered:
- An `OSError` other than a missing ledger, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.ledger import (
    RunMode,
    RunModeUnresolved,
    ledger_path,
    parse_skipped,
    read_run_mode,
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
