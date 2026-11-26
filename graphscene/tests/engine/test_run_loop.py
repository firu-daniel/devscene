"""The rule this file exists to enforce: `start_run` and `continue_run` run each step the walker
returns through `execute_set`, record every record of the result through the walker in order (a
gate with its detail, a lone dispatch without), and return the first `Refused`, having still
recorded every record after it, else the `SetResult.halt`, else carry on from the last record's
step until an `End`, `Stop`, `Interrupt` or `Refused`; each call builds its own book and breaker
before touching the walker, calls the store only off the event loop's thread, and on cancellation
re-raises with nothing of the set recorded (`graphscene.engine.run_loop`).

Every case drives `StubExecutor` with `backoff_seconds=0` through `asyncio.run`, over a `Walker`
on a graph planted through `graphscene/tests/engine/walk_support.py` → `planted` and an in-test
`MemoryStore` satisfying `StateStore` that logs each call's thread id. `Signals`, `Counter` and
`Sink` satisfy `RunSignals`, `DispatchCounter` and `LaunchSink` structurally. Every expected value
is hand-written from the planted graph and the script, never from the code's output.
"""

import asyncio
import contextlib
import threading
from collections.abc import Iterator, Mapping, Sequence
from types import MappingProxyType

import pytest

from graphscene.adapters.stub_executor import (
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    ScriptedStall,
    StubExecutor,
)
from graphscene.engine.run_loop import continue_run, start_run
from graphscene.engine.walker import Walker
from graphscene.model.execution import Completed
from graphscene.model.flow_graph import FlowGraph
from graphscene.model.run_control import ExecutionLimits, Halt, Launch, RunExit
from graphscene.model.walk_actions import (
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Interrupt,
    Refused,
    RoundPassage,
    Stop,
)
from graphscene.model.walk_state import WalkState

from .walk_support import AnswerTable, planted

_FAILED = "crashed"


class MemoryStore:
    """A `StateStore` holding one `WalkState | None`, logging `(call, thread id)` for each `read`,
    `write` and `lock`, and counting writes."""

    def __init__(self) -> None:
        self.state: WalkState | None = None
        self.writes = 0
        self.calls: list[tuple[str, int]] = []

    def read(self) -> WalkState | None:
        self.calls.append(("read", threading.get_ident()))
        return self.state

    def write(self, state: WalkState) -> None:
        self.calls.append(("write", threading.get_ident()))
        self.writes += 1
        self.state = state

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        self.calls.append(("lock", threading.get_ident()))
        yield


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
    def __init__(self) -> None:
        self._total = 0

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


def _gate() -> dict[str, object]:
    return {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "beat",
        "outcomes": {
            "approved": {"to": "review_round"},
            "rejected": {"to": "review_round"},
            "crashed": {"binding": "<halt>", "reason": "crash"},
        },
    }


def _graph(crash_pauses: bool = False) -> FlowGraph:
    """A writer `draft` (done → the round; crashed → `<halt>`, or `<pause>` resuming at `draft`)
    and a round of `g1` and `g2`; a pass reaches `published`."""
    crashed: dict[str, object] = (
        {"binding": "<pause>", "resume": "draft"}
        if crash_pauses
        else {"binding": "<halt>", "reason": "crash"}
    )
    return planted(
        {
            "draft": {
                "kind": "dispatch",
                "agent": "article-writer",
                "heartbeat": "beat",
                "outcomes": {"done": {"to": "review_round"}, "crashed": crashed},
            },
            "g1": _gate(),
            "g2": _gate(),
            "review_round": {
                "kind": "round",
                "parallel": True,
                "gates": ["g1", "g2"],
                "writer": "draft",
                "counter": "attempt",
                "convergingFrom": 1,
                "outcomes": {
                    "approved": {"to": "published", "reset": "attempt"},
                    "rejected": {"to": "draft", "increment": "attempt", "prompt": "rework"},
                },
            },
            "published": {"kind": "terminal", "binding": "<finish>"},
        }
    )


def _walker(store: MemoryStore, graph: FlowGraph | None = None) -> Walker:
    return Walker(graph if graph is not None else _graph(), store, AnswerTable({}))


def _writer() -> Dispatch:
    return Dispatch(
        node="draft",
        agent="article-writer",
        prompt=None,
        counters=MappingProxyType({"attempt": 0}),
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )


def _gate_dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent="worker",
        prompt=None,
        counters=MappingProxyType({"attempt": 0}),
        round_number=0,
        converging=False,
        closed_round=(),
        passed=(),
    )


_END = End("<finish>", "published", reports=(), passed=(RoundPassage("review_round", 0, "pass"),))

_DRAFT_STOP = Stop(
    binding="<halt>",
    node="draft",
    agent="article-writer",
    reason="crash",
    summary=None,
    evidence=None,
    round_counts=(),
    held=(),
    closed_round=(),
    passed=(),
)


def _limits(run_timeout_seconds: float | None = None) -> ExecutionLimits:
    return ExecutionLimits(backoff_seconds=0, run_timeout_seconds=run_timeout_seconds)


def _stub(script: Mapping[str, Sequence[Scripted]]) -> StubExecutor:
    return StubExecutor(script)


def _start(
    walker: Walker,
    stub: StubExecutor,
    *,
    signals: Signals | None = None,
    counter: Counter | None = None,
    sink: Sink | None = None,
    limits: ExecutionLimits | None = None,
    undelivered_limit: int = 3,
    entry: str | None = None,
) -> RunExit:
    return asyncio.run(
        start_run(
            walker,
            stub,
            signals=signals or Signals(),
            counter=counter or Counter(),
            sink=sink if sink is not None else Sink(),
            limits=limits or _limits(),
            failure_outcome=_FAILED,
            undelivered_limit=undelivered_limit,
            entry=entry,
        )
    )


def _continue(
    walker: Walker,
    stub: StubExecutor,
    *,
    counter: Counter | None = None,
    sink: Sink | None = None,
    outcome: str | None = None,
) -> RunExit:
    return asyncio.run(
        continue_run(
            walker,
            stub,
            signals=Signals(),
            counter=counter or Counter(),
            sink=sink if sink is not None else Sink(),
            limits=_limits(),
            failure_outcome=_FAILED,
            outcome=outcome,
        )
    )


def test_a_lone_dispatch_a_round_set_and_a_terminal_end_on_end() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    assert _start(_walker(MemoryStore()), stub) == _END
    assert stub.started == ("draft", "g1", "g2")


def test_a_lone_dispatchs_detail_is_not_recorded_and_the_launch_row_carries_it() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done", "notes.md")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    sink = Sink()
    assert _start(_walker(MemoryStore()), stub, sink=sink) == _END
    assert sink.rows[0] == Launch(1, "draft", "article-writer", 1, 3, Completed("done", "notes.md"))


def test_an_agent_failure_is_recorded_under_the_failure_outcome_and_stops_without_retry() -> None:
    stub = _stub({"draft": [ScriptedFailure("agent", "gave up")]})
    assert _start(_walker(MemoryStore()), stub) == _DRAFT_STOP
    assert stub.started == ("draft",)


def test_three_stalled_runs_past_the_timeout_are_recorded_as_failures_and_stop() -> None:
    stub = _stub({"draft": [ScriptedStall(), ScriptedStall(), ScriptedStall()]})
    result = _start(_walker(MemoryStore()), stub, limits=_limits(run_timeout_seconds=0.05))
    assert result == _DRAFT_STOP
    assert stub.cancelled == ("draft", "draft", "draft")


def test_a_stop_before_a_set_halts_launches_nothing_and_leaves_the_action_pending() -> None:
    stub = _stub({"draft": [ScriptedOutcome("done")]})
    walker = _walker(MemoryStore())
    assert _start(walker, stub, signals=Signals(stop_after=0)) == Halt(
        "stop", "stop requested before a set of 1"
    )
    assert stub.started == ()
    assert walker.current() == _writer()


def test_a_stop_on_a_retry_pass_saves_the_recorded_gate_and_continue_run_finishes() -> None:
    stub = _stub(
        {
            "g1": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    walker = _walker(MemoryStore())
    counter = Counter()
    # The first pass's clear asks STOP once per gate; the retry pass's first ask is the third.
    result = _start(
        walker, stub, signals=Signals(stop_after=2), counter=counter, entry="review_round"
    )
    assert result == Halt("stop", "stop requested before a set of 1")
    assert walker.current() == DispatchSet("review_round", 0, (_gate_dispatch("g1"),), ())
    sink = Sink()
    assert _continue(walker, stub, counter=counter, sink=sink) == _END
    assert sink.rows == [Launch(3, "g1", "worker", 1, 3, Completed("approved"))]


def test_an_undelivered_limit_of_one_halts_on_the_first_undelivered_set() -> None:
    stub = _stub({"draft": [ScriptedFailure("undelivered", "no result")]})
    walker = _walker(MemoryStore())
    assert _start(walker, stub, undelivered_limit=1) == Halt(
        "undelivered", "1 consecutive sets had an undelivered result"
    )
    assert walker.current() == _writer()


def test_an_interrupt_is_returned_and_continue_run_resumes_it_to_the_end() -> None:
    stub = _stub(
        {
            "draft": [ScriptedFailure("agent", "gave up"), ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    walker = _walker(MemoryStore(), _graph(crash_pauses=True))
    assert _start(walker, stub) == Interrupt(
        "<pause>", "draft", "article-writer", "draft", "resumed", (), ()
    )
    assert _continue(walker, stub, outcome="resumed") == _END
    assert stub.started == ("draft", "draft", "g1", "g2")


def test_an_undeclared_outcome_is_refused_with_the_exact_text_and_writes_nothing() -> None:
    stub = _stub({"draft": [ScriptedOutcome("approved")]})
    store = MemoryStore()
    assert _start(_walker(store), stub) == Refused(
        "outcome 'approved' is not declared by node 'draft'"
    )
    assert store.writes == 1


def test_continue_run_with_no_saved_walk_is_refused_with_the_exact_text() -> None:
    stub = _stub({})
    assert _continue(_walker(MemoryStore()), stub) == Refused("no walk has started")
    assert stub.started == ()


def test_an_undelivered_limit_of_zero_raises_with_the_store_untouched() -> None:
    store = MemoryStore()
    with pytest.raises(ValueError) as raised:
        _start(_walker(store), _stub({}), undelivered_limit=0)
    assert str(raised.value) == "UndeliveredBreaker: limit must be >= 1, got 0"
    assert store.calls == []


def test_every_store_call_runs_off_the_event_loops_thread() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    store = MemoryStore()
    walker = _walker(store)

    async def scenario() -> int:
        await start_run(
            walker,
            stub,
            signals=Signals(),
            counter=Counter(),
            sink=Sink(),
            limits=_limits(),
            failure_outcome=_FAILED,
        )
        return threading.get_ident()

    loop_thread = asyncio.run(scenario())
    assert store.calls
    assert all(thread != loop_thread for _, thread in store.calls)


def test_cancelling_a_stalled_start_run_re_raises_and_leaves_the_dispatch_pending() -> None:
    stub = _stub({"draft": [ScriptedStall()]})
    walker = _walker(MemoryStore())

    async def scenario() -> None:
        running = asyncio.create_task(
            start_run(
                walker,
                stub,
                signals=Signals(),
                counter=Counter(),
                sink=Sink(),
                limits=_limits(),
                failure_outcome=_FAILED,
            )
        )
        while not stub.started:
            await asyncio.sleep(0)
        running.cancel()
        with pytest.raises(asyncio.CancelledError):
            await running

    asyncio.run(scenario())
    assert stub.cancelled == ("draft",)
    assert walker.current() == _writer()


def test_a_gates_detail_is_recorded_with_its_outcome() -> None:
    stub = _stub(
        {
            "g1": [ScriptedOutcome("approved", "g1.md")],
            "g2": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("approved")],
        }
    )
    store = MemoryStore()
    # The first pass's clear asks STOP once per gate; the retry pass's first ask is the third.
    assert _start(
        _walker(store), stub, signals=Signals(stop_after=2), entry="review_round"
    ) == Halt("stop", "stop requested before a set of 1")
    assert store.state is not None and store.state.open_round is not None
    assert dict(store.state.open_round.records) == {"g1": GateRecord("g1", "approved", "g1.md")}


def test_a_refused_gate_record_does_not_stop_its_siblings_being_recorded() -> None:
    stub = _stub({"g1": [ScriptedOutcome("done")], "g2": [ScriptedOutcome("approved")]})
    store = MemoryStore()
    walker = _walker(store)
    assert _start(walker, stub, entry="review_round") == Refused(
        "outcome 'done' is not declared by node 'g1'"
    )
    assert store.state is not None and store.state.open_round is not None
    assert dict(store.state.open_round.records) == {"g2": GateRecord("g2", "approved", None)}
    assert walker.current() == DispatchSet("review_round", 0, (_gate_dispatch("g1"),), ())
