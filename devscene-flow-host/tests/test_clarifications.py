"""The rule this file exists to enforce: `read_answered_pairs` returns a branch's top-level
answered clarification pairs as `hr_top_level_answered_pairs` selects and orders them, each with the
`Raised by: ` origin `pd_raised_by` reads off its question, and never opens an answer file;
`read_pair_text` returns one pair file's text unchanged. Each unreadable shape raises `RecordError`
with one exact line.

Every case plants files under `tmp_path`. Every expected value is written from the task plan's
rules, never taken from the reader's output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant one
  under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.clarifications import (
    AnsweredPair,
    read_answered_pairs,
    read_pair_text,
)
from devscene_flow_host.records.errors import RecordError

_STATE = "harness-runs"
_BRANCH = "feat_x"
_REL = "harness-runs/clarifications/feat_x"


def _plant(repo_root: Path, name: str, data: bytes) -> Path:
    path = repo_root / _REL / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _pair(index: int, raised_by: str | None) -> AnsweredPair:
    return AnsweredPair(
        index=index,
        question=f"{_REL}/question_{index}.md",
        answer=f"{_REL}/answer_{index}.md",
        raised_by=raised_by,
    )


def test_pairs_come_in_numeric_order_not_lexical(tmp_path: Path) -> None:
    for n in ("10", "2"):
        _plant(tmp_path, f"question_{n}.md", f"Raised by: Phase {n}\n\n## Question\n".encode())
        _plant(tmp_path, f"answer_{n}.md", b"yes\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == (
        _pair(2, "Phase 2"),
        _pair(10, "Phase 10"),
    )


def test_a_question_with_no_answer_is_left_out(tmp_path: Path) -> None:
    _plant(tmp_path, "question_1.md", b"Raised by: Phase A\n")
    _plant(tmp_path, "question_3.md", b"Raised by: Phase B\n")
    _plant(tmp_path, "answer_3.md", b"yes\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == (_pair(3, "Phase B"),)


def test_a_question_whose_number_is_not_all_digits_is_left_out(tmp_path: Path) -> None:
    _plant(tmp_path, "question_x.md", b"Raised by: Phase A\n")
    _plant(tmp_path, "answer_x.md", b"yes\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == ()


def test_a_pair_under_answered_is_left_out(tmp_path: Path) -> None:
    _plant(tmp_path, "answered/question_1.md", b"Raised by: Phase A\n")
    _plant(tmp_path, "answered/answer_1.md", b"yes\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == ()


def test_a_raised_by_line_after_the_first_heading_gives_none(tmp_path: Path) -> None:
    _plant(tmp_path, "question_1.md", b"# Q\n\n## Question\n\nRaised by: Phase A\n")
    _plant(tmp_path, "answer_1.md", b"yes\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == (_pair(1, None),)


def test_a_crlf_question_has_its_trailing_cr_stripped(tmp_path: Path) -> None:
    _plant(tmp_path, "question_1.md", b"# Q\r\nRaised by: Phase G\r\n\r\n## Question\r\n")
    _plant(tmp_path, "answer_1.md", b"yes\r\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == (_pair(1, "Phase G"),)


def test_a_missing_directory_gives_no_pairs(tmp_path: Path) -> None:
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == ()


def test_a_question_that_is_not_utf8_raises(tmp_path: Path) -> None:
    question = _plant(tmp_path, "question_1.md", b"Raised by: \xff\xfe\n")
    _plant(tmp_path, "answer_1.md", b"yes\n")
    with pytest.raises(RecordError) as caught:
        read_answered_pairs(tmp_path, _STATE, _BRANCH)
    assert str(caught.value) == f"{question}: not UTF-8 text"


def test_an_answer_with_unreadable_bytes_still_yields_its_pair(tmp_path: Path) -> None:
    _plant(tmp_path, "question_1.md", b"Raised by: Phase G\n")
    _plant(tmp_path, "answer_1.md", b"\xff\xfe\xfd\n")
    assert read_answered_pairs(tmp_path, _STATE, _BRANCH) == (_pair(1, "Phase G"),)


def test_read_pair_text_returns_the_file_text_unchanged(tmp_path: Path) -> None:
    _plant(tmp_path, "answer_1.md", b"Use the second option.\r\n\nThanks\n")
    assert read_pair_text(tmp_path, f"{_REL}/answer_1.md") == "Use the second option.\r\n\nThanks\n"


def test_read_pair_text_on_a_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as caught:
        read_pair_text(tmp_path, f"{_REL}/answer_9.md")
    assert str(caught.value) == (
        "the clarification file 'harness-runs/clarifications/feat_x/answer_9.md' cannot be read"
    )


def test_read_pair_text_on_a_non_utf8_file_raises(tmp_path: Path) -> None:
    answer = _plant(tmp_path, "answer_1.md", b"\xff\n")
    with pytest.raises(RecordError) as caught:
        read_pair_text(tmp_path, f"{_REL}/answer_1.md")
    assert str(caught.value) == f"{answer}: not UTF-8 text"
