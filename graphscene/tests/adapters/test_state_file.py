"""The rule this file exists to enforce: `graphscene.adapters.state_file.FileStateStore` reads
`None` for an absent file, round-trips a `WalkState`, names its file in a malformed-document
`ValueError`, replaces the file atomically so a failed write leaves the previous one intact and no
temporary file behind, and holds an exclusive, bounded lock on `<path>.lock` that another thread
cannot take and that is released on every exit path.

Every file is planted under `tmp_path`. The cross-process half of the lock is not exercised here:
`flock` treats two open file descriptions alike whichever process holds them, and the threads below
each hold their own.
"""

import dataclasses
import os
import pathlib
import stat
import threading
from types import MappingProxyType

import pytest

from graphscene.adapters.state_file import FileStateStore
from graphscene.model.walk_actions import End, GateRecord, SkipPassage
from graphscene.model.walk_state import OpenRound, WalkState

_STATE = WalkState(
    flow="plan",
    node="finish",
    awaiting="done",
    pending=End(
        binding="done",
        node="finish",
        reports=(("summary", "written"),),
        passed=(SkipPassage("parity", "no_parity"),),
    ),
    counters=MappingProxyType({"rounds": 2}),
    round_numbers=MappingProxyType({"review_round": 2}),
    open_round=OpenRound(
        round="review_round",
        number=2,
        due=("review",),
        records=MappingProxyType({"review": GateRecord("review", "pass", None)}),
    ),
    prompts=MappingProxyType({"draft": "revise"}),
    reports=MappingProxyType({"summary": "written"}),
    skipped=MappingProxyType({"parity": "no_parity"}),
)


def _try_lock(store: FileStateStore) -> BaseException | None:
    """Take and release `store`'s lock on another thread; return what it raised, if anything."""
    raised: list[BaseException] = []

    def attempt() -> None:
        try:
            with store.lock():
                pass
        except BaseException as error:
            raised.append(error)

    worker = threading.Thread(target=attempt)
    worker.start()
    worker.join()
    return raised[0] if raised else None


def test_reading_an_absent_file_is_none(tmp_path: pathlib.Path) -> None:
    assert FileStateStore(tmp_path / "state.json").read() is None


def test_a_written_state_reads_back_equal(tmp_path: pathlib.Path) -> None:
    store = FileStateStore(tmp_path / "walk" / "state.json")
    store.write(_STATE)
    assert store.read() == _STATE


def test_a_malformed_file_raises_a_value_error_naming_the_file(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "state.json"
    path.write_text('{"version": 2}', encoding="utf-8")
    with pytest.raises(ValueError) as caught:
        FileStateStore(path).read()
    assert str(caught.value) == f"{path}: version: unsupported version 2"


def test_a_failed_write_leaves_the_previous_file_and_no_temporary(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "state.json"
    store = FileStateStore(path)
    store.write(_STATE)
    before = path.read_bytes()
    changed = dataclasses.replace(_STATE, node="elsewhere")
    mode = stat.S_IMODE(os.stat(tmp_path).st_mode)
    os.chmod(tmp_path, stat.S_IRUSR | stat.S_IXUSR)
    try:
        with pytest.raises(OSError):
            store.write(changed)
    finally:
        os.chmod(tmp_path, mode)
    assert path.read_bytes() == before
    assert sorted(entry.name for entry in tmp_path.iterdir()) == ["state.json"]


def test_a_second_lock_times_out_while_the_first_is_held(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "state.json"
    store = FileStateStore(path, lock_timeout=0.3)
    with store.lock():
        raised = _try_lock(store)
    assert isinstance(raised, TimeoutError)
    assert str(raised).startswith(f"{tmp_path / 'state.json.lock'}: ")
    assert _try_lock(store) is None


def test_the_lock_is_released_when_the_body_raises(tmp_path: pathlib.Path) -> None:
    store = FileStateStore(tmp_path / "state.json", lock_timeout=0.3)
    with pytest.raises(RuntimeError):
        with store.lock():
            raise RuntimeError("body failed")
    assert _try_lock(store) is None
