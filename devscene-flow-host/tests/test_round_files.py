"""The rule this file exists to enforce: a reviewer's round file is read as the bash walker reads
it — `review_verdict` as `fw_review_verdict`, `round_file_problem` as `fw_round_file_check` with
its exact reason texts and precedence, `next_review_index` as `fw_next_review_index`,
`fail_count` as `fw_fail_count`, and `round_file_path` as `flow-walker.sh`'s `round_file_path`.

Every file is planted under `tmp_path`; every expected value is a literal written from the rules
in the task plan, never taken from the output of the code under test.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

from pathlib import Path

from devscene_flow_host.records.round_files import (
    fail_count,
    next_review_index,
    review_verdict,
    round_file_path,
    round_file_problem,
)
from round_fixtures import FAIL_BODY, PASS_BODY, plant_review

# `flow-walker.sh` → REPRO's `bad.md`.
_BAD_MD = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Failure:** x\n"


def _plant(tmp_path: Path, data: bytes) -> Path:
    path = tmp_path / "review_0.md"
    path.write_bytes(data)
    return path


def test_a_single_pass_line_reads_pass(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"# Review\nverdict: PASS\n")) == "PASS"


def test_a_single_fail_line_reads_fail(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"verdict: FAIL\n## Must Fix\n")) == "FAIL"


def test_a_crlf_verdict_line_reads_as_its_verdict(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"verdict: PASS\r\n")) == "PASS"


def test_a_file_that_is_not_utf8_is_read_without_decoding(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"\xff\xfe junk\nverdict: PASS\n\x80\n")) == "PASS"


def test_two_verdict_lines_read_as_none(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"verdict: PASS\nverdict: FAIL\n")) is None


def test_no_verdict_line_reads_as_none(tmp_path: Path) -> None:
    assert review_verdict(_plant(tmp_path, b"verdict:  PASS\nverdict: pass\n")) is None


def test_an_absent_path_reads_as_none(tmp_path: Path) -> None:
    assert review_verdict(tmp_path / "missing.md") is None


def test_a_directory_reads_as_none(tmp_path: Path) -> None:
    assert review_verdict(tmp_path) is None


def test_no_single_verdict_line_is_the_first_reason(tmp_path: Path) -> None:
    assert round_file_problem(_plant(tmp_path, b"## Must Fix\n1. x\n")) == "no single verdict line"
    assert round_file_problem(tmp_path / "missing.md") == "no single verdict line"


def test_a_fail_with_no_entry_is_refused(tmp_path: Path) -> None:
    assert round_file_problem(_plant(tmp_path, b"verdict: FAIL\n")) == (
        "verdict: FAIL with no numbered entry under ## Must Fix"
    )


def test_a_fail_whose_entries_lie_outside_must_fix_is_refused(tmp_path: Path) -> None:
    body = b"verdict: FAIL\n## Should Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"
    assert round_file_problem(_plant(tmp_path, body)) == (
        "verdict: FAIL with no numbered entry under ## Must Fix"
    )


def test_a_pass_with_an_entry_is_refused(tmp_path: Path) -> None:
    body = b"verdict: PASS\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"
    assert round_file_problem(_plant(tmp_path, body)) == (
        "verdict: PASS with a numbered entry under ## Must Fix"
    )


def test_an_entry_without_a_class_is_refused(tmp_path: Path) -> None:
    assert round_file_problem(_plant(tmp_path, _BAD_MD.encode())) == (
        "Must Fix entry 1 lacks **Class:**"
    )


def test_an_entry_without_a_failure_is_refused(tmp_path: Path) -> None:
    body = b"verdict: FAIL\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:**   \n"
    assert round_file_problem(_plant(tmp_path, body)) == "Must Fix entry 1 lacks **Failure:**"


def test_entries_count_across_repeated_sections_and_the_first_problem_wins(
    tmp_path: Path,
) -> None:
    body = (
        b"verdict: FAIL\n"
        b"## Must Fix\n1. **a**\n   **Class:** c\n   **Failure:** x\n"
        b"## Notes\n1. not an entry\n"
        b"## Must Fix\r\n1. **b**\n   **Class:** c\n"
        b"2. **c**\n   **Failure:** x\n"
    )
    assert round_file_problem(_plant(tmp_path, body)) == "Must Fix entry 2 lacks **Failure:**"


def test_a_valid_fail_may_be_used(tmp_path: Path) -> None:
    assert round_file_problem(_plant(tmp_path, FAIL_BODY.encode())) is None


def test_a_valid_pass_may_be_used(tmp_path: Path) -> None:
    assert round_file_problem(_plant(tmp_path, b"verdict: PASS\n## Must Fix\nNone.\n")) is None


def test_the_next_index_is_one_past_the_highest(tmp_path: Path) -> None:
    folder = tmp_path / "f"
    plant_review(folder, 0, "")
    plant_review(folder, 3, "")
    (folder / "review_9.txt").write_text("")
    (folder / "review_x.md").write_text("")
    (folder / "review_.md").write_text("")
    assert next_review_index(folder) == 4


def test_the_index_reads_digits_as_base_ten_and_counts_directories(tmp_path: Path) -> None:
    folder = tmp_path / "f"
    plant_review(folder, 0, "")
    (folder / "review_007.md").write_text("")
    assert next_review_index(folder) == 8
    (folder / "review_12.md").mkdir()
    assert next_review_index(folder) == 13


def test_an_absent_folder_has_index_zero(tmp_path: Path) -> None:
    assert next_review_index(tmp_path / "nope") == 0


def test_fail_count_counts_only_fail_round_files(tmp_path: Path) -> None:
    folder = tmp_path / "g"
    plant_review(folder, 0, FAIL_BODY)
    plant_review(folder, 1, PASS_BODY)
    plant_review(folder, 2, "verdict: FAIL\n")
    plant_review(folder, 3, "verdict: FAIL\nverdict: FAIL\n")
    (folder / "notes.md").write_text(FAIL_BODY)
    assert fail_count(folder) == 2


def test_fail_count_of_an_absent_folder_is_zero(tmp_path: Path) -> None:
    assert fail_count(tmp_path / "nope") == 0


def test_a_relative_round_file_path_resolves_under_the_root(tmp_path: Path) -> None:
    assert round_file_path(tmp_path, "g/review_0.md") == tmp_path / "g" / "review_0.md"


def test_an_absolute_round_file_path_is_kept(tmp_path: Path) -> None:
    assert round_file_path(tmp_path, "/elsewhere/review_0.md") == Path("/elsewhere/review_0.md")
