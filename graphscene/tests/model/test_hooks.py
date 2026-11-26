"""The rule this file exists to enforce: the five hook calls are immutable plain types, each naming
itself by a class-level `kind` that is never a field, and `HookHost` is a structural protocol a
caller satisfies without subclassing (`graphscene.model.hooks`).

The protocol case is graded by `mypy`, which checks the in-test class against the `HookHost`
parameter it is passed to; at run time it shows `run` receives the call it was given.
"""

import asyncio
import dataclasses
from types import MappingProxyType

import pytest

from graphscene.model.hooks import (
    AfterDispatch,
    AfterRound,
    BeforeDispatch,
    BeforeEnd,
    BeforeRound,
    HookCall,
    HookHost,
)
from graphscene.model.run_control import NodeRecord
from graphscene.model.walk_actions import Dispatch, DispatchSet, End, RoundPassage

_ROUND = RoundPassage("review_round", 1, "pass")
_DISPATCH = Dispatch(
    node="draft",
    agent="writer",
    prompt="Write the plan.",
    counters=MappingProxyType({"rounds": 1}),
    round_number=None,
    converging=None,
    closed_round=(),
    passed=(),
)
_SET = DispatchSet("review_round", 1, (_DISPATCH,), ())
_END = End("done", "finish", (("plan", "written"),), (_ROUND,))

_BEFORE_DISPATCH = BeforeDispatch(_DISPATCH, 3, 1)
_AFTER_DISPATCH = AfterDispatch(NodeRecord("draft", "written", "plan.md"), _SET)
_BEFORE_ROUND = BeforeRound(_SET)
_AFTER_ROUND = AfterRound(_ROUND, _END)
_BEFORE_END = BeforeEnd(_END)

_EVERY_CALL: tuple[HookCall, ...] = (
    _BEFORE_DISPATCH,
    _AFTER_DISPATCH,
    _BEFORE_ROUND,
    _AFTER_ROUND,
    _BEFORE_END,
)

_KINDS: tuple[tuple[type, str], ...] = (
    (BeforeDispatch, "before_dispatch"),
    (AfterDispatch, "after_dispatch"),
    (BeforeRound, "before_round"),
    (AfterRound, "after_round"),
    (BeforeEnd, "before_end"),
)


@pytest.mark.parametrize(("cls", "kind"), _KINDS, ids=[kind for _, kind in _KINDS])
def test_each_kind_is_its_literal_and_a_class_attribute_not_a_field(cls: type, kind: str) -> None:
    assert cls.kind == kind  # type: ignore[attr-defined]
    assert "kind" not in {f.name for f in dataclasses.fields(cls)}


@pytest.mark.parametrize("call", _EVERY_CALL, ids=lambda c: type(c).__name__)
def test_every_call_is_frozen(call: HookCall) -> None:
    first_field = dataclasses.fields(call)[0].name
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(call, first_field, "changed")


class _Recording:
    def __init__(self) -> None:
        self.calls: list[tuple[str, HookCall]] = []

    def provides(self, hook: str) -> bool:
        return hook == "announce"

    async def run(self, hook: str, call: HookCall) -> None:
        self.calls.append((hook, call))


def _run_one(host: HookHost, hook: str, call: HookCall) -> bool:
    asyncio.run(host.run(hook, call))
    return host.provides(hook)


def test_a_plain_class_with_provides_and_an_async_run_is_a_hook_host() -> None:
    host = _Recording()
    assert _run_one(host, "announce", _BEFORE_DISPATCH) is True
    assert host.calls == [("announce", BeforeDispatch(_DISPATCH, 3, 1))]
    assert host.provides("other") is False
