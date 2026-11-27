"""The rule this file exists to enforce: the execution-rule types in `graphscene.model.run_control`
are immutable plain types with fixed `kind` discriminators; `ExecutionLimits` defaults to
GraphScene's own values and refuses an out-of-range or NaN value with an exact `ValueError`;
`RunExit` is exactly the five things a run of a walk ends on; and `RunSignals`, `DispatchCounter`
and `LaunchSink` are structural protocols a host satisfies without subclassing.

The protocol cases are graded by `mypy`, which checks each in-test class against the annotated
local it is assigned to; at run time they show the calls return what the class answers.
"""

import dataclasses
import typing

import pytest

from graphscene.model.execution import Completed, Failed
from graphscene.model.run_control import (
    DispatchCounter,
    ExecutionLimits,
    Halt,
    Launch,
    LaunchSink,
    NodeRecord,
    Recorded,
    Redispatch,
    Retry,
    RunExit,
    RunSignals,
    SetResult,
)
from graphscene.model.walk_actions import End, Interrupt, Refused, Stop

_RECORD = NodeRecord("draft", "written", "plan.md")


@pytest.mark.parametrize(
    "instance",
    (
        ExecutionLimits(),
        Launch(1, "draft", "writer", 1, 3, Completed("written", "plan.md")),
        Halt("cap", "dispatch cap 10 reached"),
        _RECORD,
        Recorded(_RECORD),
        Retry("draft", 2, "crashed"),
        Redispatch("draft", "no result from the provider"),
        SetResult((_RECORD,), None),
    ),
    ids=lambda i: type(i).__name__,
)
def test_every_class_is_frozen(instance: object) -> None:
    first_field = dataclasses.fields(instance)[0].name  # type: ignore[arg-type]
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, first_field, "changed")


def test_each_variant_carries_its_kind() -> None:
    assert Halt.kind == "halt"
    assert Recorded.kind == "recorded"
    assert Retry.kind == "retry"
    assert Redispatch.kind == "redispatch"


def test_the_limits_default_to_graphscenes_own_values() -> None:
    assert ExecutionLimits() == ExecutionLimits(
        max_attempts=3,
        backoff_seconds=60.0,
        dispatch_cap=None,
        run_timeout_seconds=None,
        max_concurrent_dispatches=10,
    )
    assert [f.name for f in dataclasses.fields(ExecutionLimits)] == [
        "max_attempts",
        "backoff_seconds",
        "dispatch_cap",
        "run_timeout_seconds",
        "max_concurrent_dispatches",
    ]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    (
        ({"max_attempts": 0}, "ExecutionLimits: max_attempts must be >= 1, got 0"),
        ({"backoff_seconds": -1.0}, "ExecutionLimits: backoff_seconds must be >= 0, got -1.0"),
        ({"dispatch_cap": 0}, "ExecutionLimits: dispatch_cap must be >= 1, got 0"),
        ({"run_timeout_seconds": 0.0}, "ExecutionLimits: run_timeout_seconds must be > 0, got 0.0"),
        (
            {"max_concurrent_dispatches": 0},
            "ExecutionLimits: max_concurrent_dispatches must be >= 1, got 0",
        ),
        (
            {"backoff_seconds": float("nan")},
            "ExecutionLimits: backoff_seconds must be >= 0, got nan",
        ),
    ),
    ids=(
        "max_attempts",
        "backoff_seconds",
        "dispatch_cap",
        "run_timeout_seconds",
        "max_concurrent_dispatches",
        "nan",
    ),
)
def test_an_out_of_range_limit_is_refused(kwargs: dict[str, float], message: str) -> None:
    with pytest.raises(ValueError) as caught:
        ExecutionLimits(**kwargs)  # type: ignore[arg-type]
    assert str(caught.value) == message


def test_a_run_exit_is_one_of_the_five_ends() -> None:
    assert typing.get_args(RunExit) == (End, Stop, Interrupt, Halt, Refused)


class _Signals:
    def stop_requested(self) -> bool:
        return False

    def pause_requested(self) -> bool:
        return True


class _Counter:
    def __init__(self) -> None:
        self._launched = 0

    def total(self) -> int:
        return self._launched

    def increment(self) -> int:
        self._launched += 1
        return self._launched


class _Rows:
    def __init__(self) -> None:
        self.rows: list[Launch] = []

    def record(self, launch: Launch) -> None:
        self.rows.append(launch)


def test_a_plain_class_answering_both_signals_is_run_signals() -> None:
    signals: RunSignals = _Signals()
    assert signals.stop_requested() is False
    assert signals.pause_requested() is True


def test_a_plain_class_with_total_and_increment_is_a_dispatch_counter() -> None:
    counter: DispatchCounter = _Counter()
    assert counter.total() == 0
    assert counter.increment() == 1
    assert counter.total() == 1


def test_a_plain_class_with_record_is_a_launch_sink() -> None:
    rows = _Rows()
    sink: LaunchSink = rows
    launch = Launch(1, "review", "reviewer", 1, 3, Failed("infra", "crashed"))
    sink.record(launch)
    assert rows.rows == [launch]
