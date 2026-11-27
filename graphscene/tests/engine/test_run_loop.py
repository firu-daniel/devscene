"""The rule this file exists to enforce: `start_run` and `continue_run` run each step the walker
returns through `execute_set`, record every record of the result through the walker in order (a
gate with its detail, a lone dispatch without), and return the first `Refused`, having still
recorded every record after it, else the `SetResult.halt`, else carry on from the last record's
step until an `End`, `Stop`, `Interrupt` or `Refused`; each call builds its own book and breaker
before touching the walker, calls the store only off the event loop's thread, and on cancellation
re-raises with nothing of the set recorded, and a saved `Wait` pending is refused rather than
looped on; a graph naming a hook the host cannot run is refused before the store is read, and the
declared hooks run at each taken step, before each attempt and after each recorded record, in
that order, a hook's exception propagating with the walk as saved (`graphscene.engine.run_loop`).

Every case drives `StubExecutor` with `backoff_seconds=0` through `asyncio.run`, over a `Walker`
on a graph planted through `graphscene/tests/engine/walk_support.py` → `planted` and an in-test
`MemoryStore` satisfying `StateStore` that logs each call's thread id. `Signals`, `Counter` and
`Sink` satisfy `RunSignals`, `DispatchCounter` and `LaunchSink` structurally, and `Hooks`
satisfies `HookHost`. Every expected value is hand-written from the planted graph and the script,
never from the code's output.
"""

import asyncio
import contextlib
import dataclasses
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
from graphscene.model.hooks import (
    AfterDispatch,
    AfterRound,
    BeforeDispatch,
    BeforeEnd,
    BeforeRound,
    HookCall,
)
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
    Wait,
)
from graphscene.model.walk_state import RoundResume, WalkState

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
        prompt_variant=None,
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
        prompt_variant=None,
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


def test_a_saved_wait_pending_is_refused_instead_of_looping() -> None:
    store = MemoryStore()
    walker = _walker(store)
    assert isinstance(walker.start("review_round"), DispatchSet)
    assert store.state is not None
    store.state = dataclasses.replace(
        store.state,
        pending=Wait("review_round", recorded=GateRecord("g1", "approved", None), pending=("g2",)),
    )
    writes = store.writes
    assert _continue(walker, _stub({})) == Refused(
        "the saved walk's pending action is a wait, which names no dispatch"
    )
    assert store.writes == writes


_HookLine = tuple[str, str, str, object]


def _line(hook: str, call: HookCall) -> _HookLine:
    if isinstance(call, BeforeDispatch):
        return (hook, call.kind, call.dispatch.node, call.attempt)
    if isinstance(call, AfterDispatch):
        return (hook, call.kind, call.record.node, f"{call.record.outcome}->{call.step.kind}")
    if isinstance(call, BeforeRound):
        dispatch_set = call.dispatch_set
        gates = ",".join(d.node for d in dispatch_set.dispatches)
        return (hook, call.kind, dispatch_set.round, f"{dispatch_set.number}:{gates}")
    if isinstance(call, AfterRound):
        passage = call.passage
        return (hook, call.kind, passage.round, f"{passage.number}:{passage.verdict}")
    assert isinstance(call, BeforeEnd)
    return (hook, call.kind, call.end.node, None)


class Hooks:
    """A `HookHost` providing every hook, or only `provided` when given, logging each run as
    `(hook, call.kind, node-or-round, detail)` and each call whole; `raise_on` names a hook whose
    first run raises `RuntimeError` after it is logged."""

    def __init__(self, provided: frozenset[str] | None = None, raise_on: str | None = None) -> None:
        self._provided = provided
        self._raise_on = raise_on
        self.lines: list[_HookLine] = []
        self.calls: list[HookCall] = []

    def provides(self, hook: str) -> bool:
        return self._provided is None or hook in self._provided

    async def run(self, hook: str, call: HookCall) -> None:
        self.lines.append(_line(hook, call))
        self.calls.append(call)
        if hook == self._raise_on:
            self._raise_on = None
            raise RuntimeError(f"hook '{hook}' failed")


def _hooked_graph(cap: int = 3) -> FlowGraph:
    """`_graph` with `vocabulary.hooks`: `draft` and `g1` run `prep` before and `log` after,
    `review_round` runs `open` before and `close` after, and `published` runs `publish` before;
    `rejected` stops on `<halt>` (`limit`) once `attempt` reaches `cap`."""
    return planted(
        {
            "draft": {
                "kind": "dispatch",
                "agent": "article-writer",
                "heartbeat": "beat",
                "outcomes": {
                    "done": {"to": "review_round"},
                    "crashed": {"binding": "<halt>", "reason": "crash"},
                },
                "before": ["prep"],
                "after": ["log"],
            },
            "g1": {**_gate(), "before": ["prep"], "after": ["log"]},
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
                    "rejected": {
                        "to": "draft",
                        "increment": "attempt",
                        "prompt": "rework",
                        "onCap": {"binding": "<halt>", "reason": "limit"},
                    },
                },
                "before": ["open"],
                "after": ["close"],
            },
            "published": {"kind": "terminal", "binding": "<finish>", "before": ["publish"]},
        },
        vocabulary={
            "outcomes": {
                "done": {},
                "approved": {"verdict": "pass"},
                "rejected": {"verdict": "fail"},
                "crashed": {"held": True},
            },
            "bindings": {
                "<pause>": {"primitive": "interrupt", "resumeOutcome": "resumed"},
                "<halt>": {"primitive": "stop", "reasons": ["limit", "crash"]},
                "<finish>": {"primitive": "end"},
            },
            "predicates": {},
            "hooks": {name: {} for name in ("prep", "log", "open", "close", "publish")},
        },
        counters={"attempt": {"cap": cap}},
    )


def _start_hooked(
    walker: Walker,
    stub: StubExecutor,
    hooks: Hooks | None,
    *,
    entry: str | None = None,
    resume: RoundResume | None = None,
) -> RunExit:
    return asyncio.run(
        start_run(
            walker,
            stub,
            signals=Signals(),
            counter=Counter(),
            sink=Sink(),
            limits=_limits(),
            failure_outcome=_FAILED,
            entry=entry,
            resume=resume,
            hooks=hooks,
        )
    )


def _continue_hooked(walker: Walker, stub: StubExecutor, hooks: Hooks) -> RunExit:
    return asyncio.run(
        continue_run(
            walker,
            stub,
            signals=Signals(),
            counter=Counter(),
            sink=Sink(),
            limits=_limits(),
            failure_outcome=_FAILED,
            hooks=hooks,
        )
    )


def test_a_whole_walk_runs_every_declared_hook_at_its_point_in_order() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done"), ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("rejected"), ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved"), ScriptedOutcome("approved")],
        }
    )
    hooks = Hooks()
    assert _start_hooked(_walker(MemoryStore(), _hooked_graph()), stub, hooks) == End(
        "<finish>", "published", reports=(), passed=(RoundPassage("review_round", 1, "pass"),)
    )
    assert hooks.lines == [
        ("prep", "before_dispatch", "draft", 1),
        ("log", "after_dispatch", "draft", "done->set"),
        ("open", "before_round", "review_round", "0:g1,g2"),
        ("prep", "before_dispatch", "g1", 1),
        ("log", "after_dispatch", "g1", "rejected->wait"),
        ("close", "after_round", "review_round", "0:fail"),
        ("prep", "before_dispatch", "draft", 1),
        ("log", "after_dispatch", "draft", "done->set"),
        ("open", "before_round", "review_round", "1:g1,g2"),
        ("prep", "before_dispatch", "g1", 1),
        ("log", "after_dispatch", "g1", "approved->wait"),
        ("close", "after_round", "review_round", "1:pass"),
        ("publish", "before_end", "published", None),
    ]


def test_an_infrastructure_retry_runs_the_before_dispatch_hook_again_on_attempt_two() -> None:
    stub = _stub(
        {
            "draft": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    hooks = Hooks()
    assert _start_hooked(_walker(MemoryStore(), _hooked_graph()), stub, hooks) == _END
    drafts = [
        c for c in hooks.calls if isinstance(c, BeforeDispatch) and c.dispatch.node == "draft"
    ]
    assert [(c.seq, c.attempt) for c in drafts] == [(1, 1), (2, 2)]


def test_a_hooked_graph_without_a_hook_host_is_refused_with_the_store_unread() -> None:
    store = MemoryStore()
    with pytest.raises(ValueError) as raised:
        _start_hooked(_walker(store, _hooked_graph()), _stub({}), None)
    assert str(raised.value) == "the graph names hook 'prep' and no hook host was given"
    assert store.calls == []


def test_a_hook_the_host_does_not_provide_is_refused_with_the_store_unread() -> None:
    store = MemoryStore()
    hooks = Hooks(provided=frozenset({"prep", "log", "open", "publish"}))
    with pytest.raises(ValueError) as raised:
        _continue_hooked(_walker(store, _hooked_graph()), _stub({}), hooks)
    assert str(raised.value) == "the graph names hook 'close', which the hook host does not provide"
    assert store.calls == []
    assert hooks.lines == []


def test_a_graph_with_no_hooks_runs_with_no_hook_host() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    assert _start_hooked(_walker(MemoryStore()), stub, None) == _END


def test_a_hook_raising_after_a_round_closes_propagates_and_continue_run_re_runs_it() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("approved")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    walker = _walker(MemoryStore(), _hooked_graph())
    with pytest.raises(RuntimeError) as raised:
        _start_hooked(walker, stub, Hooks(raise_on="close"))
    assert str(raised.value) == "hook 'close' failed"
    hooks = Hooks()
    assert _continue_hooked(walker, stub, hooks) == _END
    assert hooks.lines == [
        ("close", "after_round", "review_round", "0:pass"),
        ("publish", "before_end", "published", None),
    ]


def test_a_resumed_round_runs_its_before_hooks_once_with_only_the_due_gate() -> None:
    stub = _stub({"g2": [ScriptedOutcome("approved")]})
    hooks = Hooks()
    resume = RoundResume("review_round", 0, (GateRecord("g1", "approved", None),))
    walker = _walker(MemoryStore(), _hooked_graph())
    assert _start_hooked(walker, stub, hooks, entry="review_round", resume=resume) == _END
    assert hooks.lines == [
        ("open", "before_round", "review_round", "0:g2"),
        ("close", "after_round", "review_round", "0:pass"),
        ("publish", "before_end", "published", None),
    ]


def test_a_stop_reached_by_a_cap_first_runs_the_closed_rounds_after_hooks() -> None:
    stub = _stub(
        {
            "draft": [ScriptedOutcome("done")],
            "g1": [ScriptedOutcome("rejected")],
            "g2": [ScriptedOutcome("approved")],
        }
    )
    hooks = Hooks()
    assert _start_hooked(_walker(MemoryStore(), _hooked_graph(cap=1)), stub, hooks) == Stop(
        binding="<halt>",
        node="review_round",
        agent=None,
        reason="limit",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(),
        closed_round=(GateRecord("g1", "rejected", None), GateRecord("g2", "approved", None)),
        passed=(RoundPassage("review_round", 0, "fail"),),
    )
    assert hooks.lines[-2:] == [
        ("log", "after_dispatch", "g1", "rejected->wait"),
        ("close", "after_round", "review_round", "0:fail"),
    ]
