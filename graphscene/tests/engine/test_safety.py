"""The rule this file exists to enforce: `clear_set` asks STOP once per dispatch before anything
else, then PAUSE once, then checks the whole set against the dispatch cap; it returns the first
failing check's `Halt` with its exact detail text, or `None`; it never calls `increment`; and it
refuses an empty set (`graphscene.engine.safety`).

`Signals` and `Counter` are in-test classes satisfying `RunSignals` and `DispatchCounter`
structurally and recording every call, and every expected value is hand-written.
"""

from types import MappingProxyType

import pytest

from graphscene.engine.safety import clear_set
from graphscene.model.run_control import DispatchCounter, ExecutionLimits, Halt, RunSignals
from graphscene.model.walk_actions import Dispatch


class Signals:
    def __init__(self, stop: bool = False, pause: bool = False) -> None:
        self.stop = stop
        self.pause = pause
        self.calls: list[str] = []

    def stop_requested(self) -> bool:
        self.calls.append("stop")
        return self.stop

    def pause_requested(self) -> bool:
        self.calls.append("pause")
        return self.pause


class Counter:
    def __init__(self, total: int) -> None:
        self._total = total
        self.calls: list[str] = []

    def total(self) -> int:
        self.calls.append("total")
        return self._total

    def increment(self) -> int:
        self.calls.append("increment")
        self._total += 1
        return self._total


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent="writer",
        prompt=None,
        counters=MappingProxyType({}),
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


_SET = (_dispatch("alpha"), _dispatch("beta"), _dispatch("gamma"))


def test_the_in_test_classes_satisfy_the_protocols() -> None:
    signals: RunSignals = Signals()
    counter: DispatchCounter = Counter(0)
    assert clear_set(_SET, signals, counter, ExecutionLimits()) is None


def test_stop_halts_and_asks_pause_nothing() -> None:
    signals = Signals(stop=True, pause=True)
    halt = clear_set(_SET, signals, Counter(0), ExecutionLimits())
    assert halt == Halt("stop", "stop requested before a set of 3")
    assert "pause" not in signals.calls


def test_stop_is_asked_once_per_dispatch() -> None:
    signals = Signals()
    clear_set(_SET, signals, Counter(0), ExecutionLimits())
    assert signals.calls == ["stop", "stop", "stop", "pause"]


def test_pause_halts_after_stop_is_clear() -> None:
    signals = Signals(pause=True)
    halt = clear_set(_SET, signals, Counter(0), ExecutionLimits())
    assert halt == Halt("pause", "pause requested before a set of 3")
    assert signals.calls == ["stop", "stop", "stop", "pause"]


def test_a_set_that_would_pass_the_cap_halts_and_counts_nothing() -> None:
    counter = Counter(8)
    halt = clear_set(_SET, Signals(), counter, ExecutionLimits(dispatch_cap=10))
    assert halt == Halt(
        "cap", "8 dispatched; a set of 3 (alpha, beta, gamma) would pass the cap 10"
    )
    assert "increment" not in counter.calls


def test_a_set_that_exactly_reaches_the_cap_clears() -> None:
    counter = Counter(7)
    assert clear_set(_SET, Signals(), counter, ExecutionLimits(dispatch_cap=10)) is None
    assert "increment" not in counter.calls


def test_no_cap_means_any_total_clears() -> None:
    assert clear_set(_SET, Signals(), Counter(1_000_000), ExecutionLimits()) is None


def test_an_empty_set_is_refused() -> None:
    with pytest.raises(ValueError) as raised:
        clear_set((), Signals(), Counter(0), ExecutionLimits())
    assert str(raised.value) == "clear_set: a set holds at least one dispatch"
