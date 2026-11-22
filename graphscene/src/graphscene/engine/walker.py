"""The walk's driver, `Walker`: it reads the saved walk from a `StateStore`, steps it through
`graphscene.engine.transitions` and `graphscene.engine.rounds`, and writes the result back.

The rule:

- Only `start` replaces a saved walk, and it sets every counter and round number to 0.
- `start` and `next` hold the store's lock from before the read until after the write.
- `next` and `current` refuse a walk of another flow.
- `current` takes no lock and changes nothing: it re-returns the saved pending action.
- A `Refused` leaves the store unwritten.

Deliberately not covered:

- Reading round evidence at `start`: the host's.
- The review loop's rules: the host's.
"""

from graphscene.engine.rounds import record_gate
from graphscene.engine.transitions import WalkDraft, arrive, follow_edge
from graphscene.model.flow_graph import (
    BindingEdge,
    DispatchNode,
    FlowGraph,
    InterruptBinding,
    RoundNode,
)
from graphscene.model.walk_actions import Dispatch, GateRecord, Interrupt, Refused, Step
from graphscene.model.walk_state import PredicateHost, StateStore, WalkState


class Walker:
    def __init__(self, graph: FlowGraph, store: StateStore, host: PredicateHost) -> None:
        self.graph = graph
        self.store = store
        self.host = host

    def start(self, entry: str | None = None) -> Step:
        graph = self.graph
        e = entry or graph.start
        with self.store.lock():
            if e not in graph.entries:
                return Refused(f"'{e}' is not an entry of flow '{graph.flow}'")
            for node in graph.nodes.values():
                if isinstance(node, RoundNode) and e in node.gates:
                    return Refused(f"'{e}' is a gate of round '{node.id}': enter at the round")
            draft = WalkDraft.fresh(graph)
            step = arrive(graph, self.host, draft, e)
            if not isinstance(step, Refused):
                self.store.write(draft.freeze())
            return step

    def next(self, outcome: str, node: str | None = None, detail: str | None = None) -> Step:
        with self.store.lock():
            state = self.store.read()
            refused = self._foreign(state)
            if refused is not None:
                return refused
            assert state is not None
            draft = WalkDraft.from_state(state)
            step = self._step(state, draft, outcome, node, detail)
            if not isinstance(step, Refused):
                self.store.write(draft.freeze())
            return step

    def current(self) -> Step:
        state = self.store.read()
        refused = self._foreign(state)
        if refused is not None:
            return refused
        assert state is not None
        return state.pending

    def _foreign(self, state: WalkState | None) -> Refused | None:
        if state is None:
            return Refused("no walk has started")
        if state.flow != self.graph.flow:
            return Refused(f"the saved walk is of flow '{state.flow}', not '{self.graph.flow}'")
        return None

    def _step(
        self,
        state: WalkState,
        draft: WalkDraft,
        outcome: str,
        node: str | None,
        detail: str | None,
    ) -> Step:
        graph, host = self.graph, self.host
        if state.awaiting == "done":
            return Refused("the walk has finished")
        if state.awaiting == "set":
            if node is None:
                return Refused(
                    f"a round's set is pending at '{state.node}': name the gate with node"
                )
            return record_gate(graph, host, draft, node, outcome, detail)
        if node is not None and node != state.node:
            return Refused(f"'{node}' is not the pending node '{state.node}'")
        if detail is not None:
            return Refused("detail is recorded only for a gate of an open round")
        pending = state.pending
        if isinstance(pending, Interrupt):
            # The resume outcome is consumed by the interrupt, never looked up in the vocabulary.
            if outcome != pending.resume_outcome:
                return Refused(
                    f"the walk is interrupted at '{state.node}': "
                    f"resume with outcome '{pending.resume_outcome}'"
                )
            return arrive(graph, host, draft, pending.resume, closed_round=pending.closed_round)
        dispatch_node = graph.nodes[state.node]
        assert isinstance(dispatch_node, DispatchNode)
        edge = dispatch_node.outcomes.get(outcome)
        if edge is None:
            return Refused(f"outcome '{outcome}' is not declared by node '{state.node}'")
        carried: tuple[GateRecord, ...] = ()
        if (
            isinstance(edge, BindingEdge)
            and isinstance(graph.vocabulary.bindings[edge.binding], InterruptBinding)
            and isinstance(pending, Dispatch)
        ):
            carried = pending.closed_round
        return follow_edge(graph, host, draft, state.node, edge, closed_round=carried)
