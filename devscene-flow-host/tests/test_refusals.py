"""The rule this file exists to enforce: branch `b`'s reviewer-file refusals are kept in their own
file, `<stateDir>/.flow_walker_state/round_refusals/<quote(b, safe="")>.json`; a count applies only
to the round and number it was recorded for, while the last step's `refused:` lines survive a
change of round; a document not in the store's shape is refused with a `ValueError` naming the
file; and nothing the store writes lands outside `round_refusals/`.

Every file is planted under `tmp_path`; every expected value is a literal written from the rules.
After every case, `_only_refusal_files` checks that the walk's directory holds nothing but
`round_refusals/` and the one branch's file and lock.

Deliberately not covered: a crash between this file's write and the walk's, which the module
docstring leaves out.
"""

import threading
from collections.abc import Iterator
from pathlib import Path

import pytest

from devscene_flow_host.host.refusals import (
    GateRefusals,
    Refusal,
    RefusalStore,
    RoundRefusals,
    refusals_path,
)

_FILE = "feat%2Fx.json"

_RECORD = RoundRefusals(
    round="code_review_round",
    number=2,
    gates={
        "code_review": GateRefusals(attempts=2, reason="no verdict line", redo=True),
        "qa_review": GateRefusals(attempts=3, reason="no numbered entry", redo=False),
    },
    announced=(Refusal(gate="code_review", attempt=2, reason="no verdict line"),),
)


@pytest.fixture(autouse=True)
def _only_refusal_files(tmp_path: Path) -> Iterator[None]:
    yield
    walk_directory = tmp_path / "state" / ".flow_walker_state"
    refusals = walk_directory / "round_refusals"
    for path in tmp_path.rglob("*"):
        if path in (tmp_path / "state", walk_directory, refusals):
            continue
        assert path.parent == refusals, path
        assert path.name in {_FILE, _FILE + ".lock"}, path


def _store(tmp_path: Path, *, lock_timeout: float = 120.0) -> RefusalStore:
    return RefusalStore(tmp_path, "state", "feat/x", lock_timeout=lock_timeout)


def _plant(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "state" / ".flow_walker_state" / "round_refusals" / _FILE
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_a_slash_is_encoded_under_the_refusals_directory(tmp_path: Path) -> None:
    assert refusals_path(tmp_path, "state", "feat/x") == (
        tmp_path / "state" / ".flow_walker_state" / "round_refusals" / "feat%2Fx.json"
    )


def test_an_empty_branch_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        refusals_path(tmp_path, "state", "")
    assert str(raised.value) == "a walk's branch is empty"


def test_the_empty_record_and_a_gates_refusal_line(tmp_path: Path) -> None:
    assert RoundRefusals.empty("r", 1) == RoundRefusals(round="r", number=1, gates={}, announced=())
    assert _RECORD.refusal("qa_review") == Refusal(
        gate="qa_review", attempt=3, reason="no numbered entry"
    )


def test_the_gates_are_a_read_only_copy(tmp_path: Path) -> None:
    source = {"g": GateRefusals(attempts=1, reason="r", redo=True)}
    record = RoundRefusals(round="r", number=1, gates=source, announced=())
    source["h"] = GateRefusals(attempts=1, reason="r", redo=True)
    assert list(record.gates) == ["g"]
    with pytest.raises(TypeError):
        record.gates["h"] = GateRefusals(attempts=1, reason="r", redo=True)  # type: ignore[index]


def test_an_absent_file_reads_as_empty(tmp_path: Path) -> None:
    store = _store(tmp_path)
    assert store.read("code_review_round", 2) == RoundRefusals(
        round="code_review_round", number=2, gates={}, announced=()
    )
    assert store.read_announced() == ()


def test_a_write_reads_back_with_its_announced_lines(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(_RECORD)
    assert store.read("code_review_round", 2) == _RECORD
    assert store.read_announced() == (
        Refusal(gate="code_review", attempt=2, reason="no verdict line"),
    )


def test_the_written_document_has_the_stated_shape(tmp_path: Path) -> None:
    _store(tmp_path).write(_RECORD)
    path = tmp_path / "state" / ".flow_walker_state" / "round_refusals" / _FILE
    assert path.read_text(encoding="utf-8") == (
        '{"version": 1, "round": "code_review_round", "number": 2, "gates": '
        '{"code_review": {"attempts": 2, "reason": "no verdict line", "redo": true}, '
        '"qa_review": {"attempts": 3, "reason": "no numbered entry", "redo": false}}, '
        '"announced": [{"gate": "code_review", "attempt": 2, "reason": "no verdict line"}]}'
    )


def test_another_number_reads_as_empty_but_keeps_the_announced_lines(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(_RECORD)
    assert store.read("code_review_round", 3) == RoundRefusals(
        round="code_review_round",
        number=3,
        gates={},
        announced=(Refusal(gate="code_review", attempt=2, reason="no verdict line"),),
    )
    assert store.read_announced() == (
        Refusal(gate="code_review", attempt=2, reason="no verdict line"),
    )


def test_another_round_reads_as_empty(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(_RECORD)
    assert store.read("plan_review_round", 2).gates == {}


def test_clear_removes_the_file_and_tolerates_its_absence(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.clear()
    store.write(_RECORD)
    store.clear()
    assert store.read_announced() == ()
    assert not refusals_path(tmp_path, "state", "feat/x").exists()


_GOOD_GATE = '{"attempts": 1, "reason": "r", "redo": true}'
_GOOD_ITEM = '{"gate": "g", "attempt": 1, "reason": "r"}'


def _document(
    *,
    version: str = "1",
    round: str = '"r"',
    number: str = "1",
    gates: str = '{"g": ' + _GOOD_GATE + "}",
    announced: str = "[" + _GOOD_ITEM + "]",
) -> str:
    return (
        f'{{"version": {version}, "round": {round}, "number": {number}, "gates": {gates}, '
        f'"announced": {announced}}}'
    )


_MALFORMED = [
    ("not json", "not valid JSON"),
    ("[]", "the document is not an object"),
    (_document(version="2"), "version 2 is not 1"),
    (_document(version='"1"'), 'version "1" is not 1'),
    (_document(version="true"), "version true is not 1"),
    ('{"version": 1, "round": "r", "number": 1, "gates": {}}', "the document has no announced"),
    (
        _document()[:-1] + ', "extra": 0}',
        'the document has an unexpected key "extra"',
    ),
    (_document(round="1"), "round is not a string"),
    (_document(number='"1"'), "number is not an integer"),
    (_document(number="true"), "number is not an integer"),
    (_document(gates="[]"), "gates is not an object"),
    (_document(gates='{"g": []}'), "gates.g is not an object"),
    (_document(gates='{"g": {"attempts": 1, "reason": "r"}}'), "gates.g has no redo"),
    (
        _document(gates='{"g": {"attempts": 1, "reason": "r", "redo": true, "x": 1}}'),
        'gates.g has an unexpected key "x"',
    ),
    (
        _document(gates='{"g": {"attempts": "1", "reason": "r", "redo": true}}'),
        "gates.g.attempts is not an integer",
    ),
    (
        _document(gates='{"g": {"attempts": 1, "reason": 1, "redo": true}}'),
        "gates.g.reason is not a string",
    ),
    (
        _document(gates='{"g": {"attempts": 1, "reason": "r", "redo": 1}}'),
        "gates.g.redo is not a boolean",
    ),
    (_document(announced="{}"), "announced is not a list"),
    (_document(announced='["x"]'), "announced[0] is not an object"),
    (_document(announced='[{"gate": "g", "attempt": 1}]'), "announced[0] has no reason"),
    (
        _document(announced='[{"gate": "g", "attempt": 1, "reason": "r", "y": 1}]'),
        'announced[0] has an unexpected key "y"',
    ),
    (
        _document(announced='[{"gate": 1, "attempt": 1, "reason": "r"}]'),
        "announced[0].gate is not a string",
    ),
    (
        _document(announced='[{"gate": "g", "attempt": 1.5, "reason": "r"}]'),
        "announced[0].attempt is not an integer",
    ),
    (
        _document(announced='[{"gate": "g", "attempt": 1, "reason": null}]'),
        "announced[0].reason is not a string",
    ),
]


@pytest.mark.parametrize(("text", "reason"), _MALFORMED)
def test_a_malformed_document_is_refused_naming_the_file(
    tmp_path: Path, text: str, reason: str
) -> None:
    path = _plant(tmp_path, text)
    store = _store(tmp_path)
    with pytest.raises(ValueError) as raised:
        store.read("r", 1)
    assert str(raised.value) == f"{path}: {reason}"
    with pytest.raises(ValueError) as raised_announced:
        store.read_announced()
    assert str(raised_announced.value) == f"{path}: {reason}"


def test_the_well_formed_planted_document_reads(tmp_path: Path) -> None:
    _plant(tmp_path, _document())
    assert _store(tmp_path).read("r", 1) == RoundRefusals(
        round="r",
        number=1,
        gates={"g": GateRefusals(attempts=1, reason="r", redo=True)},
        announced=(Refusal(gate="g", attempt=1, reason="r"),),
    )


def test_everything_written_stays_inside_the_refusals_directory(tmp_path: Path) -> None:
    store = _store(tmp_path)
    store.write(_RECORD)
    store.write(RoundRefusals.empty("r", 1))
    with store.lock():
        pass
    refusals = tmp_path / "state" / ".flow_walker_state" / "round_refusals"
    assert {path.name for path in refusals.iterdir()} == {_FILE, _FILE + ".lock"}


def test_a_second_lock_times_out_with_the_lock_named(tmp_path: Path) -> None:
    raised: list[BaseException] = []

    def contend() -> None:
        try:
            with _store(tmp_path, lock_timeout=0.2).lock():
                pass
        except BaseException as error:
            raised.append(error)

    with _store(tmp_path).lock():
        thread = threading.Thread(target=contend)
        thread.start()
        thread.join()
    lock_path = tmp_path / "state" / ".flow_walker_state" / "round_refusals" / (_FILE + ".lock")
    assert len(raised) == 1
    assert isinstance(raised[0], TimeoutError)
    assert str(raised[0]) == f"cannot lock {lock_path} within 0.2 s"


def test_the_lock_is_released_after_its_block(tmp_path: Path) -> None:
    with _store(tmp_path).lock():
        pass
    with _store(tmp_path, lock_timeout=0.2).lock():
        pass
