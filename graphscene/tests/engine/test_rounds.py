"""The rule this file exists to enforce: a gate's outcome is recorded once, in any order, while
its round's set is out; a held outcome waits for its siblings; the join takes the first held
gate's edge in `gates` order, or else closes the round on its gates' verdicts; and `enter_round`
opens a round, refuses a record for a gate skipped on this arrival, records the rest in `gates`
order and returns the set still out or the join's step (`graphscene.engine.rounds`).

Every case opens a two-gate round, with `open_round` or `enter_round`, on a `WalkDraft.fresh`
over a graph planted through `graphscene/tests/engine/walk_support.py` → `planted`, answered by
an `AnswerTable`, and every expected value is hand-written from reading the planted graph.

Deliberately not covered:

- Whether a set is pending and whether a gate was named, and reading or writing state: the
  walker's suite.
- Refusing a record for a gate outside the round or a gate repeated in the records: the
  walker's suite.
"""

from types import MappingProxyType

from graphscene.engine.rounds import enter_round, record_gate
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
        "skip": [{"when": "stage_disabled", "to": "review_round"}],
        "outcomes": {
            "approved": {"to": "review_round", "report": {"edit_check": "approved"}},
            "rejected": {"to": "review_round"},
            "done": {"to": "review_round"},
            "crashed": {"binding": "<halt>", "reason": crash_reason},
        },
    }


def _two_gates() -> FlowGraph:
    """A writer and a round of `g1` then `g2`; `g1` crashes with reason `crash`, `g2` with
    `limit`; each gate is skipped when the host answers `stage_disabled` for it."""
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


def _gate_dispatch(node: str, number: int = 0) -> Dispatch:
    return Dispatch(
        node=node,
        agent="worker",
        prompt=None,
        counters=MappingProxyType({"attempt": 0}),
        round_number=number,
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


def _resumed() -> tuple[FlowGraph, WalkDraft]:
    graph = _two_gates()
    draft = WalkDraft.fresh(graph)
    draft.round_numbers["review_round"] = 2
    return graph, draft


def _enter(
    graph: FlowGraph,
    draft: WalkDraft,
    *records: GateRecord,
    host: AnswerTable = _NO_ANSWERS,
) -> Step:
    return enter_round(graph, host, draft, "review_round", records)


def test_entering_with_no_records_dispatches_the_whole_set_at_its_number() -> None:
    graph, draft = _resumed()
    assert _enter(graph, draft) == DispatchSet(
        "review_round", 2, (_gate_dispatch("g1", 2), _gate_dispatch("g2", 2)), ()
    )
    assert draft.open_round is not None
    assert (draft.open_round.number, draft.open_round.due) == (2, ("g1", "g2"))


def test_entering_with_one_verdict_record_dispatches_only_the_other_gate() -> None:
    graph, draft = _resumed()
    recorded = GateRecord("g1", "approved", "g1.md")
    step = _enter(graph, draft, recorded)
    assert step == DispatchSet("review_round", 2, (_gate_dispatch("g2", 2),), ())
    assert draft.pending == step
    assert draft.open_round is not None
    assert draft.open_round.due == ("g1", "g2")
    assert draft.open_round.records == {"g1": recorded}
    assert draft.reports == {"edit_check": "approved"}


def test_entering_with_both_verdicts_and_one_fail_closes_fail_and_advances_the_round() -> None:
    graph, draft = _resumed()
    rejected = GateRecord("g2", "rejected", "findings/g2.md")
    approved = GateRecord("g1", "approved", None)
    step = _enter(graph, draft, rejected, approved)
    assert step == Dispatch(
        node="draft",
        agent="article-writer",
        prompt="rework",
        counters=MappingProxyType({"attempt": 1}),
        round_number=3,
        converging=None,
        closed_round=(approved, rejected),
        passed=(RoundPassage("review_round", 2, "fail"),),
    )
    assert draft.round_numbers == {"review_round": 3}
    assert draft.open_round is None


def test_entering_with_both_passes_closes_pass() -> None:
    graph, draft = _resumed()
    step = _enter(
        graph, draft, GateRecord("g1", "approved", None), GateRecord("g2", "approved", None)
    )
    assert step == End(
        "<finish>",
        "published",
        (("edit_check", "approved"),),
        (RoundPassage("review_round", 2, "pass"),),
    )
    assert draft.open_round is None


def test_entering_with_a_held_and_a_verdict_record_stops_at_the_held_gate() -> None:
    graph, draft = _resumed()
    held = GateRecord("g1", "crashed", "g1.log")
    step = _enter(graph, draft, GateRecord("g2", "approved", None), held)
    assert step == Stop(
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
    assert draft.open_round is None


def test_entering_with_a_held_record_alone_waits_on_the_other_gate() -> None:
    graph, draft = _resumed()
    held = GateRecord("g1", "crashed", "g1.log")
    assert _enter(graph, draft, held) == DispatchSet(
        "review_round", 2, (_gate_dispatch("g2", 2),), ()
    )
    assert draft.open_round is not None
    assert draft.open_round.records == {"g1": held}


def test_entering_with_an_undeclared_outcome_is_refused_with_the_record_gate_text() -> None:
    graph, draft = _resumed()
    assert _enter(graph, draft, GateRecord("g1", "resumed", None)) == Refused(
        "outcome 'resumed' is not declared by node 'g1'"
    )


def test_entering_with_a_record_for_a_skipped_gate_is_refused_with_the_exact_text() -> None:
    graph, draft = _resumed()
    host = AnswerTable({("stage_disabled", "g1"): True})
    records = (GateRecord("g2", "approved", None), GateRecord("g1", "approved", None))
    assert _enter(graph, draft, *records, host=host) == Refused(
        "'g1' is skipped in round 2: a skipped gate carries no record"
    )


def test_entering_a_round_that_closes_at_once_refuses_any_record() -> None:
    graph, draft = _resumed()
    host = AnswerTable({("stage_disabled", "g1"): True, ("stage_disabled", "g2"): True})
    assert _enter(graph, draft, GateRecord("g2", "approved", None), host=host) == Refused(
        "'g2' is skipped in round 2: a skipped gate carries no record"
    )
