"""The rule this file exists to enforce: a gate's outcome is recorded once, in any order, while
its round's set is out; a held outcome waits for its siblings; the join takes the first held
gate's edge in `gates` order, or else closes the round on its gates' verdicts
(`graphscene.engine.rounds`).

Every case opens a two-gate round with `open_round` on a `WalkDraft.fresh` over a graph planted
through `graphscene/tests/engine/walk_support.py` → `planted`, answered by an `AnswerTable`, and
every expected value is hand-written from reading the planted graph.

Deliberately not covered:

- Whether a set is pending and whether a gate was named, and reading or writing state: the
  walker's suite.
"""

from types import MappingProxyType

from graphscene.engine.rounds import record_gate
from graphscene.engine.transitions import WalkDraft, open_round
from graphscene.model.flow_graph import FlowGraph
from graphscene.model.walk_actions import (
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Refused,
    RoundPassage,
    Step,
    Stop,
    Wait,
)

from .walk_support import AnswerTable, planted

_NO_ANSWERS = AnswerTable({})


def _gate(crash_reason: str) -> dict[str, object]:
    return {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "beat",
        "outcomes": {
            "approved": {"to": "review_round", "report": {"edit_check": "approved"}},
            "rejected": {"to": "review_round"},
            "done": {"to": "review_round"},
            "crashed": {"binding": "<halt>", "reason": crash_reason},
        },
    }


def _two_gates() -> FlowGraph:
    """A writer and a round of `g1` then `g2`; `g1` crashes with reason `crash`, `g2` with
    `limit`."""
    return planted(
        {
            "draft": {
                "kind": "dispatch",
                "agent": "article-writer",
                "heartbeat": "beat",
                "outcomes": {"done": {"to": "review_round"}},
            },
            "g1": _gate("crash"),
            "g2": _gate("limit"),
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


def _opened() -> tuple[FlowGraph, WalkDraft]:
    graph = _two_gates()
    draft = WalkDraft.fresh(graph)
    assert isinstance(open_round(graph, _NO_ANSWERS, draft, "review_round"), DispatchSet)
    return graph, draft


def _record(
    graph: FlowGraph, draft: WalkDraft, gate: str, outcome: str, detail: str | None = None
) -> Step:
    return record_gate(graph, _NO_ANSWERS, draft, gate, outcome, detail)


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


def test_a_gate_not_due_is_refused_with_the_exact_text() -> None:
    graph, draft = _opened()
    assert _record(graph, draft, "draft", "done") == Refused("'draft' is not pending in round 0")


def test_a_gate_recorded_twice_is_refused_with_the_exact_text() -> None:
    graph, draft = _opened()
    assert isinstance(_record(graph, draft, "g1", "approved"), Wait)
    assert _record(graph, draft, "g1", "rejected") == Refused(
        "an outcome for 'g1' is already recorded in round 0"
    )


def test_an_outcome_the_gate_does_not_declare_is_refused_with_the_exact_text() -> None:
    graph, draft = _opened()
    assert _record(graph, draft, "g1", "resumed") == Refused(
        "outcome 'resumed' is not declared by node 'g1'"
    )


def test_an_outcome_with_neither_verdict_nor_held_is_refused_with_the_exact_text() -> None:
    graph, draft = _opened()
    assert _record(graph, draft, "g1", "done") == Refused(
        "outcome 'done' of round gate 'g1' declares neither a verdict nor held"
    )


def test_the_first_record_waits_and_leaves_only_the_gate_still_out_to_reprint() -> None:
    graph, draft = _opened()
    step = _record(graph, draft, "g2", "approved", "g2.md")
    recorded = GateRecord("g2", "approved", "g2.md")
    assert step == Wait("review_round", recorded=recorded, pending=("g1",))
    assert draft.pending == DispatchSet("review_round", 0, (_gate_dispatch("g1"),), ())
    assert (draft.node, draft.awaiting) == ("review_round", "set")
    assert draft.open_round is not None
    assert draft.open_round.records == {"g2": recorded}
    assert draft.reports == {"edit_check": "approved"}


def test_recording_in_reverse_gates_order_closes_pass_once_both_are_in() -> None:
    graph, draft = _opened()
    assert isinstance(_record(graph, draft, "g2", "approved"), Wait)
    step = _record(graph, draft, "g1", "approved")
    assert step == End(
        "<finish>",
        "published",
        (("edit_check", "approved"),),
        (RoundPassage("review_round", 0, "pass"),),
    )
    assert draft.open_round is None


def test_a_held_outcome_waits_for_its_sibling_then_stops_at_the_held_gate() -> None:
    graph, draft = _opened()
    held = GateRecord("g1", "crashed", "g1.log")
    assert _record(graph, draft, "g1", "crashed", "g1.log") == Wait(
        "review_round", recorded=held, pending=("g2",)
    )
    step = _record(graph, draft, "g2", "approved")
    expected = Stop(
        binding="<halt>",
        node="g1",
        agent="worker",
        reason="crash",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(held,),
        closed_round=(),
        passed=(),
    )
    assert step == expected
    assert (draft.node, draft.awaiting, draft.pending) == ("g1", "done", expected)
    assert draft.open_round is None


def test_with_two_held_gates_the_first_in_gates_order_wins() -> None:
    graph, draft = _opened()
    assert isinstance(_record(graph, draft, "g2", "crashed"), Wait)
    step = _record(graph, draft, "g1", "crashed")
    assert isinstance(step, Stop)
    assert (step.node, step.reason) == ("g1", "crash")
    assert step.held == (GateRecord("g1", "crashed", None), GateRecord("g2", "crashed", None))


def test_an_all_verdict_join_closes_fail_with_the_records_in_gates_order_and_details() -> None:
    graph, draft = _opened()
    rejected = GateRecord("g2", "rejected", "findings/g2.md")
    approved = GateRecord("g1", "approved", None)
    assert isinstance(_record(graph, draft, "g2", "rejected", "findings/g2.md"), Wait)
    step = _record(graph, draft, "g1", "approved")
    assert step == Dispatch(
        node="draft",
        agent="article-writer",
        prompt="rework",
        counters=MappingProxyType({"attempt": 1}),
        round_number=1,
        converging=None,
        closed_round=(approved, rejected),
        passed=(RoundPassage("review_round", 0, "fail"),),
    )
    assert draft.open_round is None
