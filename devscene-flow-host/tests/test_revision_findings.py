"""The rule this file exists to enforce: branch `b`'s kept findings files — `flow-walker.sh`'s
`revision_findings` key — are kept in their own file,
`<stateDir>/.flow_walker_state/revision_findings/<quote(b, safe="")>.json`, as
`{"version": 1, "files": [...]}`; an absent file reads as no files; a document not in that shape
is refused with a `ValueError` naming the file; and nothing the store writes lands outside
`revision_findings/`.

Every file is planted under `tmp_path`; every expected value is a literal written from the rules.
After every case, `_only_revision_files` checks that the walk's directory holds nothing but
`revision_findings/` and the one branch's file.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest

from devscene_flow_host.host.revision_findings import (
    RevisionFindingsStore,
    revision_findings_path,
)

_FILE = "feat%2Fx.json"
_DIRECTORY = ("state", ".flow_walker_state", "revision_findings")


@pytest.fixture(autouse=True)
def _only_revision_files(tmp_path: Path) -> Iterator[None]:
    yield
    walk_directory = tmp_path / "state" / ".flow_walker_state"
    kept = walk_directory / "revision_findings"
    for path in tmp_path.rglob("*"):
        if path in (tmp_path / "state", walk_directory, kept):
            continue
        assert path.parent == kept, path
        assert path.name == _FILE, path


def _store(tmp_path: Path) -> RevisionFindingsStore:
    return RevisionFindingsStore(tmp_path, "state", "feat/x")


def _plant(tmp_path: Path, text: str) -> Path:
    path = tmp_path.joinpath(*_DIRECTORY, _FILE)
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_a_slash_is_encoded_under_the_revision_findings_directory(tmp_path: Path) -> None:
    assert revision_findings_path(tmp_path, "state", "feat/x") == (
        tmp_path / "state" / ".flow_walker_state" / "revision_findings" / "feat%2Fx.json"
    )


def test_an_empty_branch_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        revision_findings_path(tmp_path, "state", "")
    assert str(raised.value) == "a walk's branch is empty"


def test_an_absent_file_reads_as_no_files(tmp_path: Path) -> None:
    assert _store(tmp_path).read() == ()


def test_a_write_reads_back(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(("state/ui_test_plan_reviews/feat_x/review_0.md",))
    assert store.read() == ("state/ui_test_plan_reviews/feat_x/review_0.md",)
    store.write(("a.md", "b.md"))
    assert store.read() == ("a.md", "b.md")


def test_the_written_document_has_the_stated_shape(tmp_path: Path) -> None:
    _store(tmp_path).write(("a.md", "b.md"))
    assert tmp_path.joinpath(*_DIRECTORY, _FILE).read_text(encoding="utf-8") == (
        '{"version": 1, "files": ["a.md", "b.md"]}'
    )


def test_clear_removes_the_file_and_a_second_clear_is_harmless(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(("a.md",))
    store.clear()
    assert not revision_findings_path(tmp_path, "state", "feat/x").exists()
    store.clear()
    assert store.read() == ()


_MALFORMED = [
    ("not json", "not valid JSON"),
    ("[]", "the document is not an object"),
    ('{"version": 2, "files": []}', "version 2 is not 1"),
    ('{"version": "1", "files": []}', 'version "1" is not 1'),
    ('{"version": true, "files": []}', "version true is not 1"),
    ('{"version": 1}', "the document has no files"),
    ('{"files": []}', "the document has no version"),
    ('{"version": 1, "files": [], "extra": 0}', 'the document has an unexpected key "extra"'),
    ('{"version": 1, "files": "a.md"}', "files is not a list"),
    ('{"version": 1, "files": ["a.md", 1]}', "files[1] is not a string"),
]


@pytest.mark.parametrize(("text", "reason"), _MALFORMED)
def test_a_malformed_document_is_refused_naming_the_file(
    tmp_path: Path, text: str, reason: str
) -> None:
    path = _plant(tmp_path, text)
    with pytest.raises(ValueError) as raised:
        _store(tmp_path).read()
    assert str(raised.value) == f"{path}: {reason}"


def test_everything_written_stays_inside_the_revision_findings_directory(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(("a.md",))
    store.write(("b.md",))
    assert {path.name for path in tmp_path.joinpath(*_DIRECTORY).iterdir()} == {_FILE}
