"""The rule this file exists to enforce: only `start` replaces a saved walk, with every counter and
round number at 0; `start` and `next` step under the store's lock and write only a step that is
not `Refused`; `next` refuses, with exact text, a step the saved walk cannot take; `current` takes
no lock, writes nothing and re-returns the saved pending action (`graphscene.engine.walker`).

Every case drives a `Walker` over a `MemoryStore` and a graph planted through
`graphscene/tests/engine/walk_support.py` → `planted`, answered by an `AnswerTable`, and every
expected value is hand-written from reading the planted graph.

Deliberately not covered:

- The file-backed store and concurrent callers: the adapters' and the facade's suites.
"""

import contextlib
from collections.abc import Iterator
from types import MappingProxyType

from graphscene.engine.walker import Walker
from graphscene.model.flow_graph import FlowGraph
from graphscene.model.walk_actions import (
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Interrupt,
    Passage,
    Refused,
    RoundPassage,
    Stop,
    Wait,
)
from graphscene.model.walk_state import WalkState

from .walk_support import AnswerTable, planted

_NO_ANSWERS = AnswerTable({})


class MemoryStore:
    """A `StateStore` holding one `WalkState | None`, logging each `enter`, `read`, `write` and
    `exit`, and counting writes."""

    def __init__(self) -> None:
        self.state: WalkState | None = None
        self.writes = 0
        self.events: list[str] = []

    def read(self) -> WalkState | None:
        self.events.append("read")
        return self.state

    def write(self, state: WalkState) -> None:
        self.events.append("write")
        self.writes += 1
        self.state = state

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        self.events.append("enter")
        try:
            yield
        finally:
            self.events.append("exit")


def _gate(skip: bool = False) -> dict[str, object]:
    gate: dict[str, object] = {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "beat",
        "outcomes": {
            "approved": {"to": "review_round"},
            "rejected": {"to": "review_round"},
            "crashed": {"binding": "<halt>", "reason": "crash"},
        },
    }
    if skip:
        gate["skip"] = [{"when": "stage_disabled", "to": "review_round"}]
    return gate


def _graph(skip: bool = False, **overrides: object) -> FlowGraph:
    """A writer `draft` (done → the round; crashed → `<pause>` resuming at `draft`) and a round of
    `g1` then `g2`; a fail sends `draft` the `rework` prompt, a pass reaches `published`."""
    return planted(
        {
            "draft": {
                "kind": "dispatch",
                "agent": "article-writer",
                "heartbeat": "beat",
                "outcomes": {
                    "done": {"to": "review_round"},
                    "crashed": {"binding": "<pause>", "resume": "draft"},
                },
            },
            "g1": _gate(skip),
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
        },
        **overrides,
    )


def _walker(store: MemoryStore, graph: FlowGraph | None = None) -> Walker:
    return Walker(graph if graph is not None else _graph(), store, _NO_ANSWERS)


def _writer(
    prompt: str | None,
    attempt: int,
    number: int,
    closed_round: tuple[GateRecord, ...] = (),
    passed: tuple[Passage, ...] = (),
) -> Dispatch:
    return Dispatch(
        node="draft",
        agent="article-writer",
        prompt=prompt,
        counters=MappingProxyType({"attempt": attempt}),
        round_number=number,
        converging=None,
        closed_round=closed_round,
        passed=passed,
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


_SET = DispatchSet("review_round", 0, (_gate_dispatch("g1"), _gate_dispatch("g2")), ())


def _rejected_once(store: MemoryStore) -> Walker:
    """Walk to the writer's second dispatch: `g1` rejected and `g2` approved in round 0."""
    walker = _walker(store)
    walker.start()
    walker.next("done")
    walker.next("rejected", node="g1")
    walker.next("approved", node="g2")
    return walker


# start


def test_start_dispatches_the_graph_start_and_saves_it() -> None:
    store = MemoryStore()
    assert _walker(store).start() == _writer(None, 0, 0)
    assert store.writes == 1
    assert store.state is not None
    assert (store.state.node, store.state.awaiting) == ("draft", "dispatch")


def test_start_at_a_round_entry_opens_its_set() -> None:
    store = MemoryStore()
    assert _walker(store).start("review_round") == _SET
    assert store.state is not None
    assert (store.state.node, store.state.awaiting, store.state.pending) == (
        "review_round",
        "set",
        _SET,
    )


def test_start_replaces_a_saved_walk_mid_loop_with_every_counter_back_to_zero() -> None:
    store = MemoryStore()
    walker = _rejected_once(store)
    assert store.state is not None
    assert dict(store.state.counters) == {"attempt": 1}
    assert dict(store.state.round_numbers) == {"review_round": 1}
    assert walker.start() == _writer(None, 0, 0)
    assert dict(store.state.counters) == {"attempt": 0}
    assert dict(store.state.round_numbers) == {"review_round": 0}
    assert dict(store.state.prompts) == {}


def test_start_at_a_node_that_is_not_an_entry_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    assert _walker(store).start("published") == Refused(
        "'published' is not an entry of flow 'article_review'"
    )
    assert store.writes == 0


def test_start_at_a_gate_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    graph = _graph(entries=["draft", "review_round", "g1"])
    assert _walker(store, graph).start("g1") == Refused(
        "'g1' is a gate of round 'review_round': enter at the round"
    )
    assert store.writes == 0


def test_a_refused_arrival_at_start_writes_nothing() -> None:
    store = MemoryStore()
    walker = Walker(_graph(skip=True), store, AnswerTable({("stage_disabled", "g1"): None}))
    assert walker.start("review_round") == Refused(
        "the host cannot answer predicate 'stage_disabled' for node 'g1'"
    )
    assert store.writes == 0


# next


def test_next_before_any_walk_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    assert _walker(store).next("done") == Refused("no walk has started")
    assert store.writes == 0


def test_next_on_another_flows_walk_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    _walker(store, _graph(flow="other_flow")).start()
    assert _walker(store).next("done") == Refused(
        "the saved walk is of flow 'other_flow', not 'article_review'"
    )
    assert store.writes == 1


def test_next_with_a_set_pending_and_no_gate_named_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start("review_round")
    assert walker.next("approved") == Refused(
        "a round's set is pending at 'review_round': name the gate with node"
    )
    assert store.writes == 1


def test_a_gate_refusal_from_the_round_writes_nothing() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start("review_round")
    assert walker.next("done", node="draft") == Refused("'draft' is not pending in round 0")
    assert store.writes == 1


def test_next_naming_a_node_other_than_the_pending_one_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    assert walker.next("done", node="g1") == Refused("'g1' is not the pending node 'draft'")
    assert store.writes == 1


def test_next_with_a_detail_outside_an_open_round_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    assert walker.next("done", detail="notes.md") == Refused(
        "detail is recorded only for a gate of an open round"
    )
    assert store.writes == 1


def test_an_outcome_the_pending_node_does_not_declare_is_refused_with_the_exact_text() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    assert walker.next("approved") == Refused("outcome 'approved' is not declared by node 'draft'")
    assert store.writes == 1


def test_next_follows_the_declared_edge_and_saves_the_step() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    assert walker.next("done", node="draft") == _SET
    assert store.writes == 2


def test_a_recorded_gate_waits_and_current_returns_only_the_unrecorded_gates_set() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start("review_round")
    assert walker.next("rejected", node="g1", detail="g1.md") == Wait(
        "review_round", recorded=GateRecord("g1", "rejected", "g1.md"), pending=("g2",)
    )
    assert walker.current() == DispatchSet("review_round", 0, (_gate_dispatch("g2"),), ())


def test_a_failed_round_sends_the_writer_its_rework_prompt() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    walker.next("done")
    walker.next("rejected", node="g1")
    closed = (GateRecord("g1", "rejected", None), GateRecord("g2", "approved", None))
    assert walker.next("approved", node="g2") == _writer(
        "rework",
        1,
        1,
        closed_round=closed,
        passed=(RoundPassage("review_round", 0, "fail"),),
    )


def test_an_interrupt_resumes_only_on_its_resume_outcome_with_the_stored_prompt() -> None:
    store = MemoryStore()
    walker = _rejected_once(store)
    closed = (GateRecord("g1", "rejected", None), GateRecord("g2", "approved", None))
    assert walker.next("crashed") == Interrupt(
        "<pause>", "draft", "article-writer", "draft", "resumed", (), closed
    )
    writes = store.writes
    assert walker.next("done") == Refused(
        "the walk is interrupted at 'draft': resume with outcome 'resumed'"
    )
    assert store.writes == writes
    assert walker.next("resumed") == _writer("rework", 1, 1, closed_round=closed)
    assert store.writes == writes + 1


def test_a_stop_is_final_and_current_still_returns_it() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start("review_round")
    walker.next("crashed", node="g1", detail="g1.md")
    stop = Stop(
        binding="<halt>",
        node="g1",
        agent="worker",
        reason="crash",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(GateRecord("g1", "crashed", "g1.md"),),
        closed_round=(),
        passed=(),
    )
    assert walker.next("approved", node="g2") == stop
    writes = store.writes
    assert walker.next("done") == Refused("the walk has finished")
    assert store.writes == writes
    assert walker.current() == stop


def test_an_end_is_final_and_current_still_returns_it() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start("review_round")
    walker.next("approved", node="g1")
    end = End(
        "<finish>", "published", reports=(), passed=(RoundPassage("review_round", 0, "pass"),)
    )
    assert walker.next("approved", node="g2") == end
    writes = store.writes
    assert walker.next("approved", node="g1") == Refused("the walk has finished")
    assert store.writes == writes
    assert walker.current() == end


# current


def test_current_before_any_walk_is_refused() -> None:
    assert _walker(MemoryStore()).current() == Refused("no walk has started")


def test_current_on_another_flows_walk_is_refused() -> None:
    store = MemoryStore()
    _walker(store, _graph(flow="other_flow")).start()
    assert _walker(store).current() == Refused(
        "the saved walk is of flow 'other_flow', not 'article_review'"
    )
    assert store.writes == 1


# the lock


def test_start_and_next_hold_the_lock_and_current_takes_none() -> None:
    store = MemoryStore()
    walker = _walker(store)
    walker.start()
    assert store.events == ["enter", "write", "exit"]
    store.events.clear()
    walker.next("done")
    assert store.events == ["enter", "read", "write", "exit"]
    store.events.clear()
    walker.next("approved")
    assert store.events == ["enter", "read", "exit"]
    store.events.clear()
    walker.current()
    assert store.events == ["read"]
