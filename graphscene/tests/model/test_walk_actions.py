"""The rule this file exists to enforce: a walk step and every passage it records are immutable
plain types, each variant naming itself by a class-level `kind` that is never a field
(`graphscene.model.walk_actions`).
"""

import dataclasses
from types import MappingProxyType

import pytest

from graphscene.model.walk_actions import (
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Interrupt,
    LedgerPassage,
    Refused,
    RoundPassage,
    SkipPassage,
    Stop,
    Wait,
)

_RECORD = GateRecord("review", "pass", "harness-runs/findings/review_0.md")
_SKIP = SkipPassage("draft", "skipped")
_ROUND = RoundPassage("review_round", 1, "fail")
_LEDGER = LedgerPassage("round 1 closed")
_DISPATCH = Dispatch(
    node="draft",
    agent="writer",
    prompt_variant="initial",
    counters=MappingProxyType({"rounds": 1}),
    round_number=None,
    converging=None,
    closed_round=(_RECORD,),
    passed=(_SKIP, _ROUND, _LEDGER),
)
_SET = DispatchSet("review_round", 2, (_DISPATCH,), (_LEDGER,))
_WAIT = Wait("review_round", _RECORD, ("parity",))
_INTERRUPT = Interrupt("ask", "draft", "writer", "draft", "answered", ())
_STOP = Stop(
    binding="halt",
    node="review_round",
    agent=None,
    reason="cap",
    summary=None,
    evidence="findings",
    round_counts=("review_round",),
    held=(_RECORD,),
    closed_round=(),
    passed=(),
)
_END = End("done", "finish", (("plan", "written"),), ())
_REFUSED = Refused("no pending action")

_EVERY_INSTANCE: tuple[object, ...] = (
    _RECORD,
    _SKIP,
    _ROUND,
    _LEDGER,
    _DISPATCH,
    _SET,
    _WAIT,
    _INTERRUPT,
    _STOP,
    _END,
    _REFUSED,
)

_KINDS: tuple[tuple[type, str], ...] = (
    (SkipPassage, "skip"),
    (RoundPassage, "round"),
    (LedgerPassage, "ledger"),
    (Dispatch, "dispatch"),
    (DispatchSet, "set"),
    (Wait, "wait"),
    (Interrupt, "interrupt"),
    (Stop, "stop"),
    (End, "end"),
    (Refused, "refused"),
)


@pytest.mark.parametrize("instance", _EVERY_INSTANCE, ids=lambda i: type(i).__name__)
def test_every_class_is_frozen(instance: object) -> None:
    first_field = dataclasses.fields(instance)[0].name  # type: ignore[arg-type]
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, first_field, "changed")


@pytest.mark.parametrize(("cls", "kind"), _KINDS, ids=[kind for _, kind in _KINDS])
def test_each_kind_is_its_literal_and_a_class_attribute_not_a_field(cls: type, kind: str) -> None:
    assert cls.kind == kind  # type: ignore[attr-defined]
    assert "kind" not in {f.name for f in dataclasses.fields(cls)}


def test_dispatch_counters_given_as_a_mapping_proxy_stay_read_only() -> None:
    with pytest.raises(TypeError):
        _DISPATCH.counters["rounds"] = 2  # type: ignore[index]
    assert _DISPATCH.counters == {"rounds": 1}
