"""The rule this file exists to enforce: a story index's escalation evidence is read as the bash
walker's `fw_index_evidence` reads it — the `## Rejected findings` and `## Scope register`
headings compared with trailing spaces, tabs and `\\r` removed, and every `- ` entry under
`## Rejected findings` not containing `call stands` kept as read, byte-for-byte.

Every index is planted under `tmp_path`; every expected value is a literal written from
`fw_index_evidence`'s REPRO lines in `cli/templates/scripts/lib/flow-walker-gates.sh`, never
taken from the output of the code under test.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.index_evidence import IndexEvidence, read_index_evidence

# `flow-walker-gates.sh` → REPRO's `i.md`.
_REPRO_BODY = (
    "## Rejected findings\n"
    "- **3** (rejected round 1; rebutted round 2 — call stands) — r\n"
    "- **5** (rejected round 2) — r\n"
    "## Scope register\n"
)


def _plant(tmp_path: Path, data: bytes) -> Path:
    path = tmp_path / "i.md"
    path.write_bytes(data)
    return path


def test_the_repro_index_reads_as_its_evidence_lines(tmp_path: Path) -> None:
    path = _plant(tmp_path, _REPRO_BODY.encode("utf-8"))
    assert read_index_evidence(path) == IndexEvidence(
        True, ("- **5** (rejected round 2) — r",), True
    )


def test_an_absent_index_reads_as_none(tmp_path: Path) -> None:
    assert read_index_evidence(tmp_path / "absent.md") is None


def test_an_index_with_neither_heading_reads_as_no_evidence(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"# Story\n## Context\n- **1** (rejected round 1) - r\n")
    assert read_index_evidence(path) == IndexEvidence(False, (), False)


def test_headings_with_trailing_spaces_still_match(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Rejected findings  \t\n- **2** open\n## Scope register \n")
    assert read_index_evidence(path) == IndexEvidence(True, ("- **2** open",), True)


def test_an_open_entry_keeps_its_trailing_cr(tmp_path: Path) -> None:
    path = _plant(tmp_path, "## Rejected findings\r\n- **5** (rejected round 2) — r\r\n".encode())
    assert read_index_evidence(path) == IndexEvidence(
        True, ("- **5** (rejected round 2) — r\r",), False
    )


def test_a_repeated_heading_keeps_collecting(tmp_path: Path) -> None:
    body = b"## Rejected findings\n- a\n## Other\n- b\n## Rejected findings\n- c\n"
    assert read_index_evidence(_plant(tmp_path, body)) == IndexEvidence(True, ("- a", "- c"), False)


def test_an_index_that_is_not_utf8_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Rejected findings\n- \xff\n")
    with pytest.raises(RecordError) as caught:
        read_index_evidence(path)
    assert str(caught.value) == f"{path}: not UTF-8 text"
