"""The rule this file exists to enforce: a walk's saved position, and the `RoundResume` a host hands
`start`, are immutable plain types, and `StateStore` and `PredicateHost` are structural protocols a
caller satisfies without subclassing (`graphscene.model.walk_state`).

The protocol cases are graded by `mypy`, which checks each in-test class against the annotated
local it is assigned to; at run time they only show the classes construct.
"""

import contextlib
import dataclasses
from collections.abc import Iterator
from types import MappingProxyType

import pytest

from graphscene.model.walk_actions import End, GateRecord
from graphscene.model.walk_state import (
    OpenRound,
    PredicateHost,
    RoundResume,
    StateStore,
    WalkState,
)

_RECORD = GateRecord("review", "pass", None)
_OPEN_ROUND = OpenRound(
    round="review_round",
    number=1,
    due=("review", "parity"),
    records=MappingProxyType({"review": _RECORD}),
)
_RESUME = RoundResume(round="review_round", number=2, records=(_RECORD,))
_STATE = WalkState(
    flow="plan",
    node="review_round",
    awaiting="set",
    pending=End("done", "finish", (), ()),
    counters=MappingProxyType({"rounds": 1}),
    round_numbers=MappingProxyType({"review_round": 1}),
    open_round=_OPEN_ROUND,
    prompts=MappingProxyType({"draft": "first"}),
    reports=MappingProxyType({"plan": "written"}),
    skipped=MappingProxyType({"parity": "no_parity"}),
)


@pytest.mark.parametrize("instance", (_OPEN_ROUND, _RESUME, _STATE), ids=lambda i: type(i).__name__)
def test_every_class_is_frozen(instance: object) -> None:
    first_field = dataclasses.fields(instance)[0].name  # type: ignore[arg-type]
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, first_field, "changed")


def test_a_round_resume_defaults_to_no_records() -> None:
    assert RoundResume("review_round", 0).records == ()


class _MemoryStore:
    def __init__(self) -> None:
        self._state: WalkState | None = None

    def read(self) -> WalkState | None:
        return self._state

    def write(self, state: WalkState) -> None:
        self._state = state

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        yield


class _NeverSkips:
    def answer(self, predicate: str, node: str) -> bool | None:
        return False


def test_a_plain_class_with_read_write_and_lock_is_a_state_store() -> None:
    store: StateStore = _MemoryStore()
    assert store.read() is None
    store.write(_STATE)
    with store.lock():
        assert store.read() is _STATE


def test_a_plain_class_with_answer_is_a_predicate_host() -> None:
    host: PredicateHost = _NeverSkips()
    assert host.answer("no_parity", "parity") is False
