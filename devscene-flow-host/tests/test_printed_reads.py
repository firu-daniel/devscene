"""The rule this file exists to enforce: `read_printed` does, for a step about to be printed,
exactly the disk reads `render` does — a non-round reviewer's next free index per dispatch, and a
cap's per-node FAIL counts and story-index evidence — and nothing for any other action; branch
`b`'s record of them is kept in its own file,
`<stateDir>/.flow_walker_state/printed_reads/<quote(b, safe="")>.json`, as
`{"version": 1, "review_iterations": [...], "round_counts": [...], "index_evidence": ...}`; an
absent file reads as `None`; a document not in that shape is refused with a `ValueError` naming
the file; and nothing the store writes lands outside `printed_reads/`.

Steps are built by hand from `graphscene`'s public dataclasses over the harness's own format-4
graph, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, read-only. Review folders
and the story index are planted under `tmp_path`. Every expected value is a literal written from
the rules, never taken from the output of the code under test. After every case,
`_only_printed_reads_files` checks that the walk's directory holds nothing but `printed_reads/`
and the one branch's file.
"""

from collections.abc import Iterator
from pathlib import Path
from typing import Final

import pytest
from graphscene import Dispatch, DispatchSet, FlowGraph, GateRecord, Stop, load_graph_file

from devscene_flow_host.host.printed_reads import (
    PrintedReads,
    PrintedReadsStore,
    printed_reads_path,
    read_printed,
)
from devscene_flow_host.records.index_evidence import IndexEvidence
from round_fixtures import FAIL_BODY, PASS_BODY, plant_review

_GRAPH: Final = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.v4.graph.json"
)
_STATE_DIR: Final = "state"
_BRANCH: Final = "feat/x"
_FILE: Final = "feat%2Fx.json"
_READ_BRANCH: Final = "feat_x"
_DIRECTORY: Final = ("state", ".flow_walker_state", "printed_reads")
# `flow-walker-gates.sh` → REPRO's `i.md`.
_STORY_INDEX_BODY: Final = (
    "## Rejected findings\n"
    "- **3** (rejected round 1; rebutted round 2 — call stands) — r\n"
    "- **5** (rejected round 2) — r\n"
    "## Scope register\n"
)
_REPRO_EVIDENCE: Final = IndexEvidence(True, ("- **5** (rejected round 2) — r",), True)


@pytest.fixture(autouse=True)
def _only_printed_reads_files(tmp_path: Path) -> Iterator[None]:
    yield
    walk_directory = tmp_path / "state" / ".flow_walker_state"
    kept = walk_directory / "printed_reads"
    for path in walk_directory.rglob("*"):
        if path == kept:
            continue
        assert path.parent == kept, path
        assert path.name == _FILE, path


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _store(tmp_path: Path) -> PrintedReadsStore:
    return PrintedReadsStore(tmp_path, _STATE_DIR, _BRANCH)


def _plant(tmp_path: Path, text: str) -> Path:
    path = tmp_path.joinpath(*_DIRECTORY, _FILE)
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    return path


def _dispatch(node: str, agent: str, round_number: int | None) -> Dispatch:
    return Dispatch(
        node=node,
        agent=agent,
        prompt=None,
        counters={"iteration": 1},
        round_number=round_number,
        converging=None if round_number is None else False,
        closed_round=(),
        passed=(),
    )


def _stop(reason: str, evidence: str | None, round_counts: tuple[str, ...]) -> Stop:
    return Stop(
        binding="<escalate>",
        node="plan_round",
        agent=None,
        reason=reason,
        summary=None,
        evidence=evidence,
        round_counts=round_counts,
        held=(),
        closed_round=(GateRecord("architecture_review", "FAIL", "f4.md"),),
        passed=(),
    )


def test_a_slash_is_encoded_under_the_printed_reads_directory(tmp_path: Path) -> None:
    assert printed_reads_path(tmp_path, "state", "feat/x") == (
        tmp_path / "state" / ".flow_walker_state" / "printed_reads" / "feat%2Fx.json"
    )


def test_an_empty_branch_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        printed_reads_path(tmp_path, "state", "")
    assert str(raised.value) == "a walk's branch is empty"


def test_an_absent_file_reads_as_none(tmp_path: Path) -> None:
    assert _store(tmp_path).read() is None


def test_a_write_reads_back(tmp_path: Path) -> None:
    store = _store(tmp_path)
    reads = PrintedReads(
        review_iterations=(("ui_review", 3),),
        round_counts=(("architecture_review", 5), ("plan_review", 0)),
        index_evidence=IndexEvidence(True, ("- **5** (rejected round 2) — r",), False),
    )
    store.write(reads)
    assert store.read() == PrintedReads(
        review_iterations=(("ui_review", 3),),
        round_counts=(("architecture_review", 5), ("plan_review", 0)),
        index_evidence=IndexEvidence(True, ("- **5** (rejected round 2) — r",), False),
    )
    store.write(PrintedReads())
    assert store.read() == PrintedReads()


def test_the_written_document_has_the_stated_shape(tmp_path: Path) -> None:
    _store(tmp_path).write(
        PrintedReads(
            review_iterations=(("ui_review", 1),),
            round_counts=(("plan_review", 2),),
            index_evidence=IndexEvidence(False, ("- a",), True),
        )
    )
    assert tmp_path.joinpath(*_DIRECTORY, _FILE).read_text(encoding="utf-8") == (
        '{"version": 1, "review_iterations": [["ui_review", 1]], '
        '"round_counts": [["plan_review", 2]], '
        '"index_evidence": {"rejected_findings": false, "open_rejections": ["- a"], '
        '"scope_register": true}}'
    )


_EMPTY: Final = '"review_iterations": [], "round_counts": [], "index_evidence": null'


def _document(
    version: str = "1", reviews: str = "[]", rounds: str = "[]", evidence: str = "null"
) -> str:
    return (
        f'{{"version": {version}, "review_iterations": {reviews}, '
        f'"round_counts": {rounds}, "index_evidence": {evidence}}}'
    )


def _evidence(rejected: str = "true", open_rejections: str = "[]", scope: str = "false") -> str:
    return (
        f'{{"rejected_findings": {rejected}, "open_rejections": {open_rejections}, '
        f'"scope_register": {scope}}}'
    )


_MALFORMED = [
    ("not json", "not valid JSON"),
    ("[]", "the document is not an object"),
    (
        '{"review_iterations": [], "round_counts": [], "index_evidence": null}',
        "the document has no version",
    ),
    (
        '{"version": 1, "round_counts": [], "index_evidence": null}',
        "the document has no review_iterations",
    ),
    (
        '{"version": 1, "review_iterations": [], "index_evidence": null}',
        "the document has no round_counts",
    ),
    (
        '{"version": 1, "review_iterations": [], "round_counts": []}',
        "the document has no index_evidence",
    ),
    ('{"version": 1, ' + _EMPTY + ', "extra": 0}', 'the document has an unexpected key "extra"'),
    (_document(version="2"), "version 2 is not 1"),
    (_document(version='"1"'), 'version "1" is not 1'),
    (_document(version="true"), "version true is not 1"),
    (_document(reviews="{}"), "review_iterations is not a list"),
    (_document(rounds="0"), "round_counts is not a list"),
    (_document(reviews='[["a", 1], ["b"]]'), "review_iterations[1] is not a [node, count] pair"),
    (_document(reviews="[[1, 1]]"), "review_iterations[0] is not a [node, count] pair"),
    (_document(rounds='[["a", true]]'), "round_counts[0] is not a [node, count] pair"),
    (_document(rounds='[["a", -1]]'), "round_counts[0] is not a [node, count] pair"),
    (_document(rounds='[["a", 1, 2]]'), "round_counts[0] is not a [node, count] pair"),
    (_document(evidence="[]"), "index_evidence is not an object or null"),
    (
        _document(evidence='{"rejected_findings": true, "open_rejections": []}'),
        "index_evidence has no scope_register",
    ),
    (
        _document(
            evidence='{"rejected_findings": true, "open_rejections": [], '
            '"scope_register": false, "extra": 0}'
        ),
        'index_evidence has an unexpected key "extra"',
    ),
    (
        _document(evidence=_evidence(rejected="1")),
        "index_evidence.rejected_findings is not a boolean",
    ),
    (
        _document(evidence=_evidence(scope="null")),
        "index_evidence.scope_register is not a boolean",
    ),
    (
        _document(evidence=_evidence(open_rejections='["a", 2]')),
        "index_evidence.open_rejections is not a list of strings",
    ),
    (
        _document(evidence=_evidence(open_rejections='"a"')),
        "index_evidence.open_rejections is not a list of strings",
    ),
]


@pytest.mark.parametrize(("text", "reason"), _MALFORMED)
def test_a_malformed_document_is_refused_naming_the_file(
    tmp_path: Path, text: str, reason: str
) -> None:
    path = _plant(tmp_path, text)
    with pytest.raises(ValueError) as raised:
        _store(tmp_path).read()
    assert str(raised.value) == f"{path}: {reason}"


def test_a_non_round_reviewer_reads_its_folders_next_free_index(tmp_path: Path) -> None:
    plant_review(tmp_path / "state" / "ui_test_plan_reviews" / "feat_x", 0, FAIL_BODY)
    action = _dispatch("ui_review", "ui-tests-plan-reviewer", None)
    assert read_printed(_graph(), tmp_path, _STATE_DIR, _READ_BRANCH, action) == PrintedReads(
        review_iterations=(("ui_review", 1),)
    )


def test_the_three_round_gates_read_nothing(tmp_path: Path) -> None:
    gates = (
        _dispatch("business_parity_review", "business-parity-reviewer", 0),
        _dispatch("architecture_review", "architecture-reviewer", 0),
        _dispatch("plan_review", "task-plan-reviewer", 0),
    )
    action = DispatchSet("plan_round", 0, gates, ())
    assert read_printed(_graph(), tmp_path, _STATE_DIR, _READ_BRANCH, action) == PrintedReads()


def test_the_plan_round_cap_reads_its_counts_and_evidence(tmp_path: Path) -> None:
    reviews = tmp_path / "state"
    for n in range(5):
        plant_review(reviews / "architecture_reviews" / "feat_x", n, FAIL_BODY)
        plant_review(
            reviews / "task_plan_reviews" / "feat_x", n, FAIL_BODY if n == 0 else PASS_BODY
        )
    index = tmp_path / "state" / "story_plans" / "feat_x_story_plan.md"
    index.parent.mkdir(parents=True)
    index.write_text(_STORY_INDEX_BODY, encoding="utf-8")
    action = _stop(
        "cap", "story_index", ("business_parity_review", "architecture_review", "plan_review")
    )
    assert read_printed(_graph(), tmp_path, _STATE_DIR, _READ_BRANCH, action) == PrintedReads(
        round_counts=(
            ("business_parity_review", 0),
            ("architecture_review", 5),
            ("plan_review", 1),
        ),
        index_evidence=_REPRO_EVIDENCE,
    )


def test_a_stop_that_is_not_a_cap_reads_nothing(tmp_path: Path) -> None:
    action = _stop("error", "story_index", ("architecture_review",))
    assert read_printed(_graph(), tmp_path, _STATE_DIR, _READ_BRANCH, action) == PrintedReads()


def test_a_counted_node_with_no_findings_folder_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        read_printed(
            _graph(), tmp_path, _STATE_DIR, _READ_BRANCH, _stop("cap", None, ("plan_round",))
        )
    assert str(raised.value) == "graph has no 'nodes.plan_round.findingsFolder'"


def test_an_evidence_name_with_no_path_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        read_printed(_graph(), tmp_path, _STATE_DIR, _READ_BRANCH, _stop("cap", "nowhere", ()))
    assert str(raised.value) == "graph has no 'paths.nowhere'"


def test_everything_written_stays_inside_the_printed_reads_directory(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(PrintedReads(review_iterations=(("ui_review", 0),)))
    store.write(PrintedReads())
    assert {path.name for path in tmp_path.joinpath(*_DIRECTORY).iterdir()} == {_FILE}
