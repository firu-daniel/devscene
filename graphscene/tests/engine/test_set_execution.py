"""The rule this file exists to enforce: `execute_set` clears every pass through `clear_set`,
launches each dispatch concurrently under the optional run timeout, writes one `Launch` row per
launched session, settles results in finish order, never cancels a sibling, re-dispatches only the
retried and undelivered nodes as a new pass, halts through the breaker, and returns the outcomes
then the held failures; on its own cancellation or a defect out of `run` it cancels and awaits its
outstanding runs and re-raises (`graphscene.engine.set_execution`).

Each case drives `StubExecutor` through `asyncio.run` with `backoff_seconds=0`. `Signals`,
`Counter` and `Sink` are in-test classes satisfying `RunSignals`, `DispatchCounter` and
`LaunchSink` structurally. Order is asserted only through the stub's `started`, `finished` and
`cancelled` records and the sink's rows, never against the wall clock, and every expected value is
hand-written from the script.
"""

import asyncio
from collections.abc import Mapping, Sequence
from types import MappingProxyType

import pytest

from graphscene.adapters.stub_executor import (
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    ScriptedStall,
    StubExecutor,
)
from graphscene.engine.attempts import AttemptBook
from graphscene.engine.breaker import UndeliveredBreaker
from graphscene.engine.set_execution import execute_set
from graphscene.model.execution import Completed, Failed
from graphscene.model.run_control import (
    DispatchCounter,
    ExecutionLimits,
    Halt,
    Launch,
    LaunchSink,
    NodeRecord,
    RunSignals,
    SetResult,
)
from graphscene.model.walk_actions import Dispatch

_FAILED = "failed"


class Signals:
    """Asks STOP only once `stop_requested` has been called more than `stop_after` times."""

    def __init__(self, stop_after: int | None = None) -> None:
        self._stop_after = stop_after
        self._stop_calls = 0

    def stop_requested(self) -> bool:
        self._stop_calls += 1
        return self._stop_after is not None and self._stop_calls > self._stop_after

    def pause_requested(self) -> bool:
        return False


class Counter:
    def __init__(self, total: int = 0) -> None:
        self._total = total

    def total(self) -> int:
        return self._total

    def increment(self) -> int:
        self._total += 1
        return self._total


class Sink:
    def __init__(self) -> None:
        self.rows: list[Launch] = []

    def record(self, launch: Launch) -> None:
        self.rows.append(launch)


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent=f"{node}-agent",
        prompt=None,
        counters=MappingProxyType({}),
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


def _execute(
    nodes: Sequence[str],
    stub: StubExecutor,
    *,
    signals: Signals | None = None,
    counter: Counter | None = None,
    sink: Sink | None = None,
    breaker: UndeliveredBreaker | None = None,
    max_attempts: int = 3,
    dispatch_cap: int | None = None,
    run_timeout_seconds: float | None = None,
) -> SetResult:
    limits = ExecutionLimits(
        max_attempts=max_attempts,
        backoff_seconds=0,
        dispatch_cap=dispatch_cap,
        run_timeout_seconds=run_timeout_seconds,
    )
    return asyncio.run(
        execute_set(
            [_dispatch(node) for node in nodes],
            stub,
            signals=signals or Signals(),
            counter=counter or Counter(),
            sink=sink if sink is not None else Sink(),
            book=AttemptBook(),
            breaker=breaker or UndeliveredBreaker(),
            limits=limits,
            failure_outcome=_FAILED,
        )
    )


def _stub(script: Mapping[str, Sequence[Scripted]]) -> StubExecutor:
    return StubExecutor(script)


def test_the_in_test_classes_satisfy_the_protocols() -> None:
    signals: RunSignals = Signals()
    counter: DispatchCounter = Counter()
    sink: LaunchSink = Sink()
    assert (signals.stop_requested(), counter.increment()) == (False, 1)
    sink.record(Launch(1, "a", "a-agent", 1, 3, Completed("pass")))


def test_outcomes_are_recorded_in_finish_order_not_set_order() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass", delay=0.03)],
            "b": [ScriptedOutcome("pass", delay=0.01)],
            "c": [ScriptedOutcome("pass", delay=0.02)],
        }
    )
    sink = Sink()
    result = _execute(["a", "b", "c"], stub, sink=sink)
    assert stub.finished == ("b", "c", "a")
    assert result == SetResult(
        (
            NodeRecord("b", "pass", None),
            NodeRecord("c", "pass", None),
            NodeRecord("a", "pass", None),
        ),
        None,
    )
    assert [(row.node, row.seq) for row in sink.rows] == [("b", 2), ("c", 3), ("a", 1)]


def test_an_agent_failure_waits_for_its_siblings_and_is_listed_after_the_outcomes() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass", delay=0.02)],
            "b": [ScriptedFailure("agent", "gave up")],
            "c": [ScriptedOutcome("fail", "two issues", delay=0.01)],
        }
    )
    result = _execute(["a", "b", "c"], stub)
    assert stub.finished == ("b", "c", "a")
    assert stub.cancelled == ()
    assert stub.started == ("a", "b", "c")
    assert result == SetResult(
        (
            NodeRecord("c", "fail", "two issues"),
            NodeRecord("a", "pass", None),
            NodeRecord("b", _FAILED, "gave up"),
        ),
        None,
    )


def test_a_run_past_its_timeout_is_cancelled_and_retried_alone_while_siblings_run_once() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass")],
            "b": [ScriptedStall(), ScriptedOutcome("pass")],
            "c": [ScriptedOutcome("pass")],
        }
    )
    sink = Sink()
    result = _execute(["a", "b", "c"], stub, sink=sink, run_timeout_seconds=0.05)
    assert stub.started == ("a", "b", "c", "b")
    assert stub.cancelled == ("b",)
    assert result == SetResult(
        (
            NodeRecord("a", "pass", None),
            NodeRecord("c", "pass", None),
            NodeRecord("b", "pass", None),
        ),
        None,
    )
    assert sink.rows[2] == Launch(
        2, "b", "b-agent", 1, 3, Failed("infra", "timed out: no result within 0.05s")
    )
    assert sink.rows[3] == Launch(4, "b", "b-agent", 2, 3, Completed("pass"))


def test_three_infra_failures_produce_the_exhausted_detail() -> None:
    stub = _stub(
        {
            "a": [
                ScriptedFailure("infra", "crashed"),
                ScriptedFailure("infra", "timed out"),
                ScriptedFailure("infra", "bad return"),
            ]
        }
    )
    result = _execute(["a"], stub)
    assert result == SetResult(
        (
            NodeRecord(
                "a",
                _FAILED,
                "all 3 attempts failed for an infrastructure reason"
                "\nattempt 1 of 3: crashed"
                "\nattempt 2 of 3: timed out"
                "\nattempt 3 of 3: bad return",
            ),
        ),
        None,
    )


def test_an_undelivered_gate_is_redispatched_with_an_unchanged_attempt() -> None:
    stub = _stub(
        {
            "a": [
                ScriptedFailure("infra", "crashed"),
                ScriptedFailure("undelivered", "no result"),
                ScriptedOutcome("pass"),
            ]
        }
    )
    sink = Sink()
    result = _execute(["a"], stub, sink=sink)
    assert [row.attempt for row in sink.rows] == [1, 2, 2]
    assert result == SetResult((NodeRecord("a", "pass", None),), None)


def test_the_third_consecutive_undelivered_pass_halts_with_the_default_breaker() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass")],
            "b": [ScriptedFailure("undelivered", "no result")] * 3,
        }
    )
    result = _execute(["a", "b"], stub, breaker=UndeliveredBreaker())
    assert stub.started == ("a", "b", "b", "b")
    assert result == SetResult(
        (NodeRecord("a", "pass", None),),
        Halt("undelivered", "3 consecutive sets had an undelivered result"),
    )


def test_an_infra_retry_pass_between_undelivered_passes_leaves_the_strikes_unchanged() -> None:
    stub = _stub(
        {
            "b": [
                ScriptedFailure("undelivered", "no result"),
                ScriptedFailure("undelivered", "no result"),
                ScriptedFailure("infra", "crashed"),
                ScriptedFailure("undelivered", "no result"),
            ]
        }
    )
    result = _execute(["b"], stub, breaker=UndeliveredBreaker())
    assert stub.started == ("b", "b", "b", "b")
    assert result == SetResult(
        (), Halt("undelivered", "3 consecutive sets had an undelivered result")
    )


def test_the_hosts_breaker_limit_takes_effect() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass")],
            "b": [ScriptedFailure("undelivered", "no result")] * 3,
        }
    )
    result = _execute(["a", "b"], stub, breaker=UndeliveredBreaker(2))
    assert stub.started == ("a", "b", "b")
    assert result == SetResult(
        (NodeRecord("a", "pass", None),),
        Halt("undelivered", "2 consecutive sets had an undelivered result"),
    )


def test_a_retry_pass_that_would_pass_the_cap_halts_and_launches_nothing() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass")],
            "b": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("pass")],
        }
    )
    sink = Sink()
    result = _execute(["a", "b"], stub, sink=sink, dispatch_cap=2)
    assert stub.started == ("a", "b")
    assert len(sink.rows) == 2
    assert result == SetResult(
        (NodeRecord("a", "pass", None),),
        Halt("cap", "2 dispatched; a set of 1 (b) would pass the cap 2"),
    )


def test_a_stop_after_the_first_pass_lets_it_finish_and_halts_the_retry_pass() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass")],
            "b": [ScriptedFailure("infra", "crashed", delay=0.01), ScriptedOutcome("pass")],
        }
    )
    result = _execute(["a", "b"], stub, signals=Signals(stop_after=2))
    assert stub.started == ("a", "b")
    assert stub.finished == ("a", "b")
    assert result == SetResult(
        (NodeRecord("a", "pass", None),), Halt("stop", "stop requested before a set of 1")
    )


def test_the_sink_holds_one_row_per_launched_session() -> None:
    stub = _stub(
        {
            "a": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("pass")],
            "b": [ScriptedOutcome("pass", delay=0.01)],
        }
    )
    sink = Sink()
    _execute(["a", "b"], stub, sink=sink, counter=Counter(10), max_attempts=2)
    assert sink.rows == [
        Launch(11, "a", "a-agent", 1, 2, Failed("infra", "crashed")),
        Launch(12, "b", "b-agent", 1, 2, Completed("pass")),
        Launch(13, "a", "a-agent", 2, 2, Completed("pass")),
    ]


def test_a_defect_out_of_run_cancels_the_outstanding_runs_and_propagates() -> None:
    stub = _stub({"a": [ScriptedStall()]})
    with pytest.raises(LookupError) as raised:
        _execute(["a", "b"], stub)
    assert str(raised.value) == "b: the stub has no scripted run left"
    assert stub.cancelled == ("a",)


def test_cancelling_execute_set_cancels_its_runs_and_re_raises() -> None:
    stub = _stub({"a": [ScriptedStall()], "b": [ScriptedStall()]})

    async def scenario() -> None:
        running = asyncio.create_task(
            execute_set(
                [_dispatch("a"), _dispatch("b")],
                stub,
                signals=Signals(),
                counter=Counter(),
                sink=Sink(),
                book=AttemptBook(),
                breaker=UndeliveredBreaker(),
                limits=ExecutionLimits(backoff_seconds=0),
                failure_outcome=_FAILED,
            )
        )
        while len(stub.started) < 2:
            await asyncio.sleep(0)
        running.cancel()
        with pytest.raises(asyncio.CancelledError):
            await running

    asyncio.run(scenario())
    assert stub.cancelled == ("a", "b")
