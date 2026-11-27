"""The rule this file exists to enforce: `execute_set` clears every pass through `clear_set`,
launches each dispatch concurrently under the optional run timeout, at most
`max_concurrent_dispatches` at once in set order, writes one `Launch` row per
launched session carrying the breaker's strikes as its pass was cleared, settles results in
finish order, never cancels a sibling, re-dispatches only the retried and undelivered nodes as a
new pass, halts through the breaker, and returns the outcomes then the held failures; on its own
cancellation or a defect out of `run` it cancels and awaits its outstanding runs and re-raises; a
given `before_dispatch` is awaited once per attempt, before the run and outside its timeout, and
an exception from it propagates like one out of `run` (`graphscene.engine.set_execution`).

Each case drives `StubExecutor` or `Gated` through `asyncio.run` with `backoff_seconds=0`.
`Signals`, `Counter` and `Sink` are in-test classes satisfying `RunSignals`, `DispatchCounter` and
`LaunchSink` structurally, and `Gated` satisfies `Executor` the same way. `Hook` is the recording
`before_dispatch`. Order is asserted only
through the stub's `started`, `finished` and `cancelled` records, `Gated`'s log and the sink's
rows, never against the wall clock, and every expected value is hand-written from the script.
"""

import asyncio
from collections.abc import Awaitable, Callable, Mapping, Sequence
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
from graphscene.model.execution import Completed, Executor, Failed, NodeResult
from graphscene.model.hooks import BeforeDispatch
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


class Gated:
    """Holds each node's run until the test opens that node's gate, logging starts and ends."""

    def __init__(self, nodes: Sequence[str]) -> None:
        self._gates = {node: asyncio.Event() for node in nodes}
        self.events: list[tuple[str, str]] = []
        self.in_flight = 0
        self.peak = 0

    def open(self, node: str) -> None:
        self._gates[node].set()

    async def run(self, dispatch: Dispatch) -> NodeResult:
        node = dispatch.node
        self.events.append(("start", node))
        self.in_flight += 1
        self.peak = max(self.peak, self.in_flight)
        await self._gates[node].wait()
        self.in_flight -= 1
        self.events.append(("end", node))
        return Completed("pass")


async def _until(condition: Callable[[], bool]) -> None:
    while not condition():
        await asyncio.sleep(0)


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent=f"{node}-agent",
        prompt_variant=None,
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
    max_concurrent_dispatches: int = 10,
    before_dispatch: Callable[[BeforeDispatch], Awaitable[None]] | None = None,
) -> SetResult:
    limits = ExecutionLimits(
        max_attempts=max_attempts,
        backoff_seconds=0,
        dispatch_cap=dispatch_cap,
        run_timeout_seconds=run_timeout_seconds,
        max_concurrent_dispatches=max_concurrent_dispatches,
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
            before_dispatch=before_dispatch,
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


def test_each_row_carries_the_strikes_its_pass_was_cleared_with() -> None:
    breaker = UndeliveredBreaker()
    first = Sink()
    _execute(
        ["a"],
        _stub({"a": [ScriptedFailure("undelivered", "x"), ScriptedOutcome("pass")]}),
        sink=first,
        breaker=breaker,
    )
    second = Sink()
    _execute(["a"], _stub({"a": [ScriptedOutcome("pass")]}), sink=second, breaker=breaker)
    assert first.rows == [
        Launch(1, "a", "a-agent", 1, 3, Failed("undelivered", "x"), 0),
        Launch(2, "a", "a-agent", 1, 3, Completed("pass"), 1),
    ]
    assert second.rows == [Launch(1, "a", "a-agent", 1, 3, Completed("pass"), 0)]


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


def _launch(
    nodes: Sequence[str],
    executor: Executor,
    *,
    sink: Sink,
    counter: Counter,
    limits: ExecutionLimits,
) -> asyncio.Task[SetResult]:
    return asyncio.create_task(
        execute_set(
            [_dispatch(node) for node in nodes],
            executor,
            signals=Signals(),
            counter=counter,
            sink=sink,
            book=AttemptBook(),
            breaker=UndeliveredBreaker(),
            limits=limits,
            failure_outcome=_FAILED,
        )
    )


def test_a_set_of_eight_under_a_limit_of_five_starts_the_sixth_when_one_finishes() -> None:
    nodes = ["n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8"]
    gated = Gated(nodes)
    sink = Sink()

    async def scenario() -> SetResult:
        running = _launch(
            nodes,
            gated,
            sink=sink,
            counter=Counter(),
            limits=ExecutionLimits(backoff_seconds=0, max_concurrent_dispatches=5),
        )
        await _until(lambda: len(gated.events) >= 5)
        gated.open("n3")
        await _until(lambda: ("start", "n6") in gated.events)
        for node in ["n1", "n2", "n4", "n5", "n6", "n7", "n8"]:
            gated.open(node)
        return await running

    result = asyncio.run(scenario())
    assert gated.peak == 5
    assert gated.events[:7] == [
        ("start", "n1"),
        ("start", "n2"),
        ("start", "n3"),
        ("start", "n4"),
        ("start", "n5"),
        ("end", "n3"),
        ("start", "n6"),
    ]
    assert sorted((row.node, row.seq) for row in sink.rows) == [
        ("n1", 1),
        ("n2", 2),
        ("n3", 3),
        ("n4", 4),
        ("n5", 5),
        ("n6", 6),
        ("n7", 7),
        ("n8", 8),
    ]
    assert result.halt is None
    assert len(result.records) == 8


def test_the_default_window_is_ten() -> None:
    nodes = [f"n{i}" for i in range(1, 13)]
    gated = Gated(nodes)

    async def scenario() -> None:
        running = _launch(
            nodes,
            gated,
            sink=Sink(),
            counter=Counter(),
            limits=ExecutionLimits(backoff_seconds=0),
        )
        await _until(lambda: len(gated.events) >= 10)
        for node in nodes:
            gated.open(node)
        await running

    asyncio.run(scenario())
    assert gated.peak == 10


def test_a_queued_dispatch_is_not_charged_the_wait_against_the_run_timeout() -> None:
    stub = _stub(
        {
            "a": [ScriptedOutcome("pass", delay=0.06)],
            "b": [ScriptedOutcome("pass", delay=0.06)],
        }
    )
    sink = Sink()
    result = _execute(
        ["a", "b"], stub, sink=sink, run_timeout_seconds=0.1, max_concurrent_dispatches=1
    )
    assert stub.started == ("a", "b")
    assert result == SetResult((NodeRecord("a", "pass", None), NodeRecord("b", "pass", None)), None)
    assert sink.rows == [
        Launch(1, "a", "a-agent", 1, 3, Completed("pass")),
        Launch(2, "b", "b-agent", 1, 3, Completed("pass")),
    ]


def test_a_stop_raised_mid_pass_still_sends_the_queued_dispatches() -> None:
    stub = _stub(
        {
            "n1": [ScriptedOutcome("pass")],
            "n2": [ScriptedOutcome("pass")],
            "n3": [ScriptedOutcome("pass")],
        }
    )
    result = _execute(
        ["n1", "n2", "n3"], stub, signals=Signals(stop_after=3), max_concurrent_dispatches=1
    )
    assert stub.started == ("n1", "n2", "n3")
    assert result == SetResult(
        (
            NodeRecord("n1", "pass", None),
            NodeRecord("n2", "pass", None),
            NodeRecord("n3", "pass", None),
        ),
        None,
    )


def test_cancelling_execute_set_never_starts_a_queued_dispatch() -> None:
    stub = _stub({"n1": [ScriptedStall()], "n2": [ScriptedOutcome("pass")]})
    sink = Sink()
    counter = Counter()

    async def scenario() -> None:
        running = _launch(
            ["n1", "n2"],
            stub,
            sink=sink,
            counter=counter,
            limits=ExecutionLimits(backoff_seconds=0, max_concurrent_dispatches=1),
        )
        await _until(lambda: len(stub.started) >= 1)
        running.cancel()
        with pytest.raises(asyncio.CancelledError):
            await running

    asyncio.run(scenario())
    assert stub.started == ("n1",)
    assert stub.cancelled == ("n1",)
    assert counter.total() == 1
    assert sink.rows == []


class Hook:
    """Records each call with the stub's `started` at that moment; sleeps `delay`, then raises
    `RuntimeError` for a node in `refuse`."""

    def __init__(
        self, stub: StubExecutor, *, delay: float = 0.0, refuse: Sequence[str] = ()
    ) -> None:
        self._stub = stub
        self._delay = delay
        self._refuse = tuple(refuse)
        self.calls: list[BeforeDispatch] = []
        self.started_at_call: list[tuple[str, ...]] = []

    async def __call__(self, call: BeforeDispatch) -> None:
        self.calls.append(call)
        self.started_at_call.append(self._stub.started)
        if self._delay > 0:
            await asyncio.sleep(self._delay)
        if call.dispatch.node in self._refuse:
            raise RuntimeError(f"{call.dispatch.node}: hook refused")


def test_a_set_of_two_runs_the_hook_once_per_dispatch_with_its_own_seq() -> None:
    stub = _stub({"a": [ScriptedOutcome("pass")], "b": [ScriptedOutcome("pass")]})
    hook = Hook(stub)
    result = _execute(["a", "b"], stub, before_dispatch=hook)
    assert hook.calls == [
        BeforeDispatch(_dispatch("a"), 1, 1),
        BeforeDispatch(_dispatch("b"), 2, 1),
    ]
    assert result == SetResult((NodeRecord("a", "pass", None), NodeRecord("b", "pass", None)), None)


def test_an_infra_retry_runs_the_hook_again_with_the_next_attempt_and_a_new_seq() -> None:
    stub = _stub({"a": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("pass")]})
    hook = Hook(stub)
    sink = Sink()
    _execute(["a"], stub, sink=sink, before_dispatch=hook)
    assert hook.calls == [
        BeforeDispatch(_dispatch("a"), 1, 1),
        BeforeDispatch(_dispatch("a"), 2, 2),
    ]
    assert [(row.seq, row.attempt) for row in sink.rows] == [(1, 1), (2, 2)]


def test_the_hook_is_awaited_before_its_nodes_run_starts() -> None:
    stub = _stub({"a": [ScriptedOutcome("pass")], "b": [ScriptedOutcome("pass")]})
    hook = Hook(stub)
    _execute(["a", "b"], stub, before_dispatch=hook)
    assert hook.started_at_call == [(), ("a",)]
    assert stub.started == ("a", "b")


def test_a_hook_that_raises_propagates_and_its_dispatch_writes_no_row() -> None:
    stub = _stub({"a": [ScriptedStall()], "b": [ScriptedOutcome("pass")]})
    hook = Hook(stub, refuse=["b"])
    sink = Sink()
    counter = Counter()
    with pytest.raises(RuntimeError) as raised:
        _execute(["a", "b"], stub, sink=sink, counter=counter, before_dispatch=hook)
    assert str(raised.value) == "b: hook refused"
    assert stub.started == ("a",)
    assert stub.cancelled == ("a",)
    assert counter.total() == 2
    assert sink.rows == []


def test_a_slow_hook_does_not_count_against_the_run_timeout() -> None:
    stub = _stub({"a": [ScriptedOutcome("pass")]})
    hook = Hook(stub, delay=0.1)
    sink = Sink()
    result = _execute(["a"], stub, sink=sink, run_timeout_seconds=0.05, before_dispatch=hook)
    assert result == SetResult((NodeRecord("a", "pass", None),), None)
    assert sink.rows == [Launch(1, "a", "a-agent", 1, 3, Completed("pass"))]


def test_with_no_hook_the_rows_are_unchanged() -> None:
    stub = _stub(
        {
            "a": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("pass")],
            "b": [ScriptedOutcome("pass", delay=0.01)],
        }
    )
    sink = Sink()
    _execute(["a", "b"], stub, sink=sink, before_dispatch=None)
    assert sink.rows == [
        Launch(1, "a", "a-agent", 1, 3, Failed("infra", "crashed")),
        Launch(2, "b", "b-agent", 1, 3, Completed("pass")),
        Launch(3, "a", "a-agent", 2, 3, Completed("pass")),
    ]
