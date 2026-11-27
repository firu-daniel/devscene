"""The rule this file exists to enforce: `write_park` writes `question_<n>.md`, `<n>` one past the
highest existing question, with the exact bytes `prl_park` wrote — a `## Q1` section added only
when the body carries no `## Q<digit>` line — at mode `0o644`, and refuses a path already taken;
`write_pause` appends `prl_pause`'s block to `PAUSE_PROGRESS.md` and writes `PAUSE_ACK`, both with
exact bytes; and nothing either writes lands outside `<stateDir>`.

Every record is planted under `tmp_path`; every expected value is a literal written from the task
plan's rules, never taken from the output of the code under test.

Deliberately not covered:
- An `OSError` other than a taken path, which propagates unwrapped: no portable way to plant one
  under `tmp_path`.
"""

import os
import stat
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from devscene_flow_host.host.run_records import write_park, write_pause
from devscene_flow_host.records.errors import RecordError

_QUESTIONS = Path("state", "clarifications", "feat_x")
_NOW = datetime(2026, 11, 27, 9, 5, 3, tzinfo=UTC)


def _park(root: Path, body: str) -> str:
    return write_park(
        root, "state", "feat_x", raised_by="plan-writer", title="Which store?", body=body
    )


def _all_files(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}


def test_a_park_into_an_empty_directory_writes_question_1(tmp_path: Path) -> None:
    assert _park(tmp_path, "Pick one.\n") == "state/clarifications/feat_x/question_1.md"
    assert (tmp_path / _QUESTIONS / "question_1.md").read_bytes() == (
        b"# Which store?\n"
        b"\n"
        b"Raised by: plan-writer (script-driven planning)\n"
        b"\n"
        b"## Q1 \xe2\x80\x94 Which store?\n"
        b"\n"
        b"Pick one.\n"
    )


def test_a_park_after_question_2_writes_question_3(tmp_path: Path) -> None:
    (tmp_path / _QUESTIONS).mkdir(parents=True)
    (tmp_path / _QUESTIONS / "question_2.md").write_bytes(b"# earlier\n")
    assert _park(tmp_path, "Pick one.\n") == "state/clarifications/feat_x/question_3.md"
    assert (tmp_path / _QUESTIONS / "question_3.md").is_file()


def test_a_body_carrying_its_own_q_section_gets_none_added(tmp_path: Path) -> None:
    _park(tmp_path, "Intro.\n## Q1 — Own heading\n\nPick one.\n")
    assert (tmp_path / _QUESTIONS / "question_1.md").read_bytes() == (
        b"# Which store?\n"
        b"\n"
        b"Raised by: plan-writer (script-driven planning)\n"
        b"\n"
        b"Intro.\n"
        b"## Q1 \xe2\x80\x94 Own heading\n"
        b"\n"
        b"Pick one.\n"
    )


def test_the_question_file_mode_is_0o644(tmp_path: Path) -> None:
    _park(tmp_path, "Pick one.\n")
    mode = stat.S_IMODE((tmp_path / _QUESTIONS / "question_1.md").stat().st_mode)
    assert mode == 0o644


def test_a_taken_question_path_raises(tmp_path: Path) -> None:
    (tmp_path / _QUESTIONS).mkdir(parents=True)
    os.symlink("missing.md", tmp_path / _QUESTIONS / "question_1.md")
    with pytest.raises(RecordError) as raised:
        _park(tmp_path, "Pick one.\n")
    assert str(raised.value) == "'state/clarifications/feat_x/question_1.md' already exists"


def test_a_pause_appends_its_block_and_writes_the_ack(tmp_path: Path) -> None:
    (tmp_path / "state").mkdir()
    (tmp_path / "state" / "PAUSE_PROGRESS.md").write_bytes(b"# Pause progress\n")
    write_pause(
        tmp_path, "state", "feat_x", phase="task-plan", next_step="resume round 2", now=_NOW
    )
    assert (tmp_path / "state" / "PAUSE_PROGRESS.md").read_bytes() == (
        b"# Pause progress\n"
        b"\n"
        b"## 2026-11-27T09:05:03Z \xe2\x80\x94 feat_x paused (script-driven planning)\n"
        b"- phase: task-plan\n"
        b"- next step: resume round 2\n"
    )
    assert (tmp_path / "state" / "PAUSE_ACK").read_bytes() == b"2026-11-27T09:05:03Z\n"


def test_a_pause_time_is_written_in_utc(tmp_path: Path) -> None:
    now = datetime(2026, 11, 27, 11, 5, 3, tzinfo=timezone(timedelta(hours=2)))
    write_pause(tmp_path, "state", "feat_x", phase="p", next_step="n", now=now)
    assert (tmp_path / "state" / "PAUSE_ACK").read_bytes() == b"2026-11-27T09:05:03Z\n"


def test_everything_written_stays_under_the_state_dir(tmp_path: Path) -> None:
    _park(tmp_path, "Pick one.\n")
    write_pause(tmp_path, "state", "feat_x", phase="p", next_step="n", now=_NOW)
    assert _all_files(tmp_path) == {
        "state/clarifications/feat_x/question_1.md",
        "state/PAUSE_PROGRESS.md",
        "state/PAUSE_ACK",
    }
