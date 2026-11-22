"""Recording a gate's outcome while its round's set is out, and the join once every gate is in.

The rule: a gate's outcome is recorded once; a held outcome waits for the gates still out and
never cancels them; the join takes the first held gate's edge in the round's `gates` order, or
else closes the round through `graphscene.engine.transitions.close_round`. `record_gate` refuses,
in this order, a gate not due in the open round, a gate already recorded, an outcome its node
does not declare, and an outcome declaring neither a verdict nor held. A verdict outcome records
its edge's report; its edge's `to` is the round and is not followed.

Deliberately not covered:

- Whether a set is pending at all and whether a gate was named, and reading or writing state:
  `graphscene.engine.walker`'s. `record_gate` assumes `draft.open_round` is set.
"""

from types import MappingProxyType

from graphscene.engine.transitions import WalkDraft, close_round, follow_edge, take_binding
from graphscene.model.flow_graph import BindingEdge, FlowGraph, RoundNode, RouteEdge, TerminalNode
from graphscene.model.walk_actions import DispatchSet, GateRecord, Refused, Step, Wait
from graphscene.model.walk_state import OpenRound, PredicateHost


def record_gate(
    graph: FlowGraph,
    host: PredicateHost,
    draft: WalkDraft,
    gate: str,
    outcome: str,
    detail: str | None,
) -> Step:
    current = draft.open_round
    assert current is not None, "record_gate is called only while a round's set is out"
    number = current.number
    if gate not in current.due:
        return Refused(f"'{gate}' is not pending in round {number}")
    if gate in current.records:
        return Refused(f"an outcome for '{gate}' is already recorded in round {number}")
    node = graph.nodes[gate]
    assert not isinstance(node, TerminalNode)
    edge = node.outcomes.get(outcome)
    if edge is None:
        return Refused(f"outcome '{outcome}' is not declared by node '{gate}'")
    declared = graph.vocabulary.outcomes.get(outcome)
    if declared is None or (declared.verdict is None and not declared.held):
        return Refused(
            f"outcome '{outcome}' of round gate '{gate}' declares neither a verdict nor held"
        )

    record = GateRecord(gate, outcome, detail)
    records = MappingProxyType({**current.records, gate: record})
    opened = OpenRound(current.round, number, current.due, records)
    draft.open_round = opened
    if declared.verdict is not None and isinstance(edge, RouteEdge) and edge.report is not None:
        draft.reports.update(edge.report)

    round_node = graph.nodes[current.round]
    assert isinstance(round_node, RoundNode)
    gates_order = round_node.gates
    out = tuple(g for g in gates_order if g in current.due and g not in records)
    if out:
        stored = draft.pending
        assert isinstance(stored, DispatchSet)
        draft.pending = DispatchSet(
            stored.round,
            stored.number,
            tuple(d for d in stored.dispatches if d.node in out),
            stored.passed,
        )
        draft.awaiting = "set"
        return Wait(current.round, recorded=record, pending=out)

    held = tuple(
        records[g]
        for g in gates_order
        if g in records and graph.vocabulary.outcomes[records[g].outcome].held
    )
    if not held:
        return close_round(graph, host, draft, current.round)
    draft.open_round = None
    first = held[0]
    first_node = graph.nodes[first.gate]
    assert not isinstance(first_node, TerminalNode)
    held_edge = first_node.outcomes[first.outcome]
    if isinstance(held_edge, BindingEdge):
        return take_binding(
            graph,
            draft,
            first.gate,
            held_edge.binding,
            reason=held_edge.reason,
            resume=held_edge.resume,
            summary=held_edge.summary,
            round_counts=held_edge.round_counts,
            evidence=held_edge.evidence,
            held=held,
        )
    return follow_edge(graph, host, draft, first.gate, held_edge, held=held)
