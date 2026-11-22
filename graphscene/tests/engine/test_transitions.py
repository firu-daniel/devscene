"""The rule this file exists to enforce: the walk's transitions move a draft from node to node by
the graph's declared primitives alone — skips asked of the host on every arrival, counters reset
before they increment and capped at `>= cap`, a binding routed on its class, a round dispatched as
one set of its unskipped gates and closed on its gates' verdicts (`graphscene.engine.transitions`).

Every case drives the functions on a `WalkDraft.fresh` over a graph planted through
`graphscene/tests/engine/walk_support.py` → `planted`, answered by an `AnswerTable`, and every
expected value is hand-written from reading the planted graph.

Deliberately not covered:

- Recording a gate's outcome and the held join: `graphscene/tests/engine/test_rounds.py`'s. The
  close-on-fail case plants the open round's record by hand instead.
- Validating a caller's step and reading or writing state: the walker's suite.
"""

from types import MappingProxyType

from graphscene.engine.transitions import (
    WalkDraft,
    arrive,
    close_round,
    follow_edge,
    open_round,
    take_binding,
)
from graphscene.model.flow_graph import Edge, FlowGraph, RouteEdge, TerminalNode
from graphscene.model.walk_actions import (
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Interrupt,
    Refused,
    RoundPassage,
    SkipPassage,
    Stop,
)
from graphscene.model.walk_state import OpenRound

from .walk_support import AnswerTable, planted

_NO_ANSWERS = AnswerTable({})


def _dispatch(outcomes: dict[str, object], **extra: object) -> dict[str, object]:
    return {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "beat",
        "outcomes": outcomes,
        **extra,
    }


def _skip(to: str, **extra: object) -> list[dict[str, object]]:
    return [{"when": "stage_disabled", "to": to, **extra}]


def _round(gates: list[str], outcomes: dict[str, object]) -> dict[str, object]:
    return {
        "kind": "round",
        "parallel": True,
        "gates": gates,
        "writer": "draft",
        "counter": "attempt",
        "convergingFrom": 1,
        "outcomes": outcomes,
    }


_TERMINAL = {"kind": "terminal", "binding": "<finish>"}

_REJECTED = {
    "to": "draft",
    "increment": "attempt",
    "prompt": "rework",
    "onCap": {
        "binding": "<halt>",
        "reason": "limit",
        "summary": "no convergence in {cap} attempts; open: {open_gates}",
        "roundCounts": ["g1", "g2"],
        "evidence": "article",
    },
}


def _article() -> FlowGraph:
    """A writer, two gates in one round, and a terminal: `g1` may be skipped, `g2` may not."""
    return planted(
        {
            "draft": {
                "kind": "dispatch",
                "agent": "article-writer",
                "heartbeat": "beat",
                "outcomes": {"done": {"to": "review_round"}},
            },
            "g1": _dispatch(
                {"approved": {"to": "review_round"}, "rejected": {"to": "review_round"}},
                skip=_skip("review_round", report={"edit_check": "bypassed"}),
            ),
            "g2": _dispatch(
                {"approved": {"to": "review_round"}, "rejected": {"to": "review_round"}}
            ),
            "review_round": _round(
                ["g1", "g2"],
                {"approved": {"to": "published", "reset": "attempt"}, "rejected": _REJECTED},
            ),
            "published": _TERMINAL,
        }
    )


def _edge(graph: FlowGraph, node_id: str, outcome: str) -> Edge:
    node = graph.nodes[node_id]
    assert not isinstance(node, TerminalNode)
    return node.outcomes[outcome]


def _route(graph: FlowGraph, node_id: str, outcome: str) -> RouteEdge:
    edge = _edge(graph, node_id, outcome)
    assert isinstance(edge, RouteEdge)
    return edge


def test_arrival_at_a_dispatch_node_dispatches_it_with_its_writer_round_number() -> None:
    graph = _article()
    draft = WalkDraft.fresh(graph)
    step = arrive(graph, _NO_ANSWERS, draft, "draft")
    expected = Dispatch(
        node="draft",
        agent="article-writer",
        prompt=None,
        counters=MappingProxyType({"attempt": 0}),
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )
    assert step == expected
    assert (draft.node, draft.awaiting, draft.pending) == ("draft", "dispatch", expected)


def test_a_skip_chain_records_each_report_and_passage_and_dispatches_where_it_ends() -> None:
    graph = planted(
        {
            "a": _dispatch({"done": {"to": "c"}}, skip=_skip("b", report={"edit_check": "off"})),
            "b": _dispatch({"done": {"to": "c"}}, skip=_skip("c")),
            "c": _dispatch({"done": {"to": "t"}}),
            "t": _TERMINAL,
        },
        start="a",
        entries=["a"],
    )
    host = AnswerTable({("stage_disabled", "a"): True, ("stage_disabled", "b"): True})
    draft = WalkDraft.fresh(graph)
    step = arrive(graph, host, draft, "a")
    assert step == Dispatch(
        node="c",
        agent="worker",
        prompt=None,
        counters=MappingProxyType({"attempt": 0}),
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(SkipPassage("a", "bypassed"), SkipPassage("b", "bypassed")),
    )
    assert draft.reports == {"edit_check": "off"}
    assert draft.skipped == {"a": "stage_disabled", "b": "stage_disabled"}
    assert draft.node == "c"


def test_a_skip_loop_is_refused_with_the_exact_text() -> None:
    graph = planted(
        {
            "a": _dispatch({"done": {"to": "t"}}, skip=_skip("b")),
            "b": _dispatch({"done": {"to": "t"}}, skip=_skip("a")),
            "t": _TERMINAL,
        },
        start="a",
        entries=["a"],
    )
    host = AnswerTable({("stage_disabled", "a"): True, ("stage_disabled", "b"): True})
    step = arrive(graph, host, WalkDraft.fresh(graph), "a")
    assert step == Refused("skip entries loop through node 'a'")


def test_a_predicate_the_host_cannot_answer_is_refused_with_the_exact_text() -> None:
    graph = planted(
        {"a": _dispatch({"done": {"to": "t"}}, skip=_skip("t")), "t": _TERMINAL},
        start="a",
        entries=["a"],
    )
    step = arrive(graph, AnswerTable({("stage_disabled", "a"): None}), WalkDraft.fresh(graph), "a")
    assert step == Refused("the host cannot answer predicate 'stage_disabled' for node 'a'")


def test_reset_runs_before_increment_on_one_edge() -> None:
    graph = planted(
        {
            "a": _dispatch(
                {
                    "rejected": {
                        "to": "b",
                        "reset": "attempt",
                        "increment": "attempt",
                        "onCap": {"binding": "<halt>", "reason": "limit"},
                    }
                }
            ),
            "b": _dispatch({"done": {"to": "t"}}),
            "t": _TERMINAL,
        },
        start="a",
        entries=["a"],
    )
    draft = WalkDraft.fresh(graph)
    draft.counters["attempt"] = 2
    step = follow_edge(graph, _NO_ANSWERS, draft, "a", _route(graph, "a", "rejected"))
    assert isinstance(step, Dispatch)
    assert step.node == "b"
    assert step.counters == {"attempt": 1}


def test_one_below_the_cap_the_routed_edge_advances_the_round_and_arrives() -> None:
    graph = _article()
    draft = WalkDraft.fresh(graph)
    draft.counters["attempt"] = 1
    edge = _route(graph, "review_round", "rejected")
    step = follow_edge(graph, _NO_ANSWERS, draft, "review_round", edge, advance="review_round")
    assert step == Dispatch(
        node="draft",
        agent="article-writer",
        prompt="rework",
        counters=MappingProxyType({"attempt": 2}),
        round_number=1,
        converging=None,
        closed_round=(),
        passed=(),
    )


def test_at_the_cap_on_cap_stops_with_the_summary_filled_and_the_round_not_advanced() -> None:
    graph = _article()
    draft = WalkDraft.fresh(graph)
    draft.counters["attempt"] = 2
    edge = _route(graph, "review_round", "rejected")
    step = follow_edge(
        graph,
        _NO_ANSWERS,
        draft,
        "review_round",
        edge,
        advance="review_round",
        open_gates=("g1", "g2"),
    )
    expected = Stop(
        binding="<halt>",
        node="review_round",
        agent=None,
        reason="limit",
        summary="no convergence in 3 attempts; open: g1, g2",
        evidence="article",
        round_counts=("g1", "g2"),
        held=(),
        closed_round=(),
        passed=(),
    )
    assert step == expected
    assert (draft.awaiting, draft.pending, draft.node) == ("done", expected, "review_round")
    assert draft.round_numbers == {"review_round": 0}
    assert draft.counters == {"attempt": 3}
    assert "draft" not in draft.prompts


def test_round_counts_drop_a_skipped_node_whose_predicate_is_not_counted() -> None:
    vocabulary = {
        "outcomes": {"done": {}},
        "bindings": {"<halt>": {"primitive": "stop", "reasons": ["limit"]}},
        "predicates": {
            "stage_disabled": {"records": "bypassed", "inRoundCounts": False},
            "already_done": {"records": "reused", "inRoundCounts": True},
        },
    }
    graph = planted(
        {"a": _dispatch({"done": {"to": "a"}})}, vocabulary=vocabulary, start="a", entries=["a"]
    )
    draft = WalkDraft.fresh(graph)
    draft.skipped.update({"x": "stage_disabled", "y": "already_done"})
    step = take_binding(
        graph,
        draft,
        "a",
        "<halt>",
        reason="limit",
        resume=None,
        summary="open: {open_gates}; cap {cap}",
        round_counts=("x", "y", "z"),
        evidence=None,
    )
    assert isinstance(step, Stop)
    assert step.round_counts == ("y", "z")
    assert step.summary == "open: ; cap {cap}"
    assert step.agent == "worker"


def test_an_interrupt_edge_pauses_at_its_node() -> None:
    graph = planted(
        {"a": _dispatch({"crashed": {"binding": "<pause>", "resume": "a"}})},
        start="a",
        entries=["a"],
    )
    draft = WalkDraft.fresh(graph)
    step = follow_edge(graph, _NO_ANSWERS, draft, "a", _edge(graph, "a", "crashed"))
    expected = Interrupt("<pause>", "a", "worker", "a", "resumed", ())
    assert step == expected
    assert (draft.awaiting, draft.pending, draft.node) == ("interrupt", expected, "a")


def test_a_stop_edge_ends_the_walk_carrying_held_and_closed_records() -> None:
    graph = planted(
        {"a": _dispatch({"crashed": {"binding": "<halt>", "reason": "crash"}})},
        start="a",
        entries=["a"],
    )
    held = (GateRecord("a", "crashed", None),)
    closed = (GateRecord("b", "approved", "b.md"),)
    draft = WalkDraft.fresh(graph)
    edge = _edge(graph, "a", "crashed")
    step = follow_edge(graph, _NO_ANSWERS, draft, "a", edge, held=held, closed_round=closed)
    expected = Stop(
        binding="<halt>",
        node="a",
        agent="worker",
        reason="crash",
        summary=None,
        evidence=None,
        round_counts=(),
        held=held,
        closed_round=closed,
        passed=(),
    )
    assert step == expected
    assert (draft.awaiting, draft.pending) == ("done", expected)


def test_an_end_binding_on_an_edge_is_refused_with_the_exact_text() -> None:
    graph = planted({"a": _dispatch({"done": {"to": "a"}})}, start="a", entries=["a"])
    step = take_binding(
        graph,
        WalkDraft.fresh(graph),
        "a",
        "<finish>",
        reason=None,
        resume=None,
        summary=None,
        round_counts=None,
        evidence=None,
    )
    assert step == Refused("binding '<finish>' is an end; only a terminal node takes one")


def test_a_terminal_ends_with_its_reports_in_the_graphs_reports_order() -> None:
    graph = planted(
        {"a": _dispatch({"done": {"to": "t", "report": {"first": "done"}}}), "t": _TERMINAL},
        start="a",
        entries=["a"],
        reports=["second", "first", "unset"],
    )
    draft = WalkDraft.fresh(graph)
    draft.reports.update({"second": "written", "extra": "ignored"})
    step = follow_edge(graph, _NO_ANSWERS, draft, "a", _route(graph, "a", "done"))
    expected = End("<finish>", "t", (("second", "written"), ("first", "done")), ())
    assert step == expected
    assert (draft.awaiting, draft.pending, draft.node) == ("done", expected, "t")


def test_open_round_skips_one_gate_without_following_it_and_dispatches_the_other() -> None:
    graph = _article()
    draft = WalkDraft.fresh(graph)
    draft.counters["attempt"] = 1
    step = open_round(graph, AnswerTable({("stage_disabled", "g1"): True}), draft, "review_round")
    expected = DispatchSet(
        round="review_round",
        number=0,
        dispatches=(
            Dispatch(
                node="g2",
                agent="worker",
                prompt=None,
                counters=MappingProxyType({"attempt": 1}),
                round_number=0,
                converging=True,
                closed_round=(),
                passed=(),
            ),
        ),
        passed=(SkipPassage("g1", "bypassed"),),
    )
    assert step == expected
    assert draft.open_round == OpenRound("review_round", 0, ("g2",), MappingProxyType({}))
    assert (draft.node, draft.awaiting, draft.pending) == ("review_round", "set", expected)
    assert draft.skipped == {"g1": "stage_disabled"}
    assert draft.reports == {"edit_check": "bypassed"}


def test_an_all_skipped_round_closes_pass_at_once() -> None:
    graph = planted(
        {
            "draft": _dispatch({"done": {"to": "review_round"}}),
            "g1": _dispatch(
                {"approved": {"to": "review_round"}, "rejected": {"to": "review_round"}},
                skip=_skip("draft", report={"edit_check": "bypassed"}),
            ),
            "review_round": _round(
                ["g1"],
                {"approved": {"to": "published", "reset": "attempt"}, "rejected": _REJECTED},
            ),
            "published": _TERMINAL,
        }
    )
    draft = WalkDraft.fresh(graph)
    draft.counters["attempt"] = 2
    step = arrive(graph, AnswerTable({("stage_disabled", "g1"): True}), draft, "review_round")
    assert step == End(
        "<finish>",
        "published",
        (("edit_check", "bypassed"),),
        (SkipPassage("g1", "bypassed"), RoundPassage("review_round", 0, "pass")),
    )
    assert draft.open_round is None
    assert draft.counters == {"attempt": 0}
    assert draft.round_numbers == {"review_round": 0}


def test_close_round_on_fail_advances_the_round_and_hands_its_records_to_the_writer() -> None:
    graph = _article()
    draft = WalkDraft.fresh(graph)
    assert isinstance(open_round(graph, _NO_ANSWERS, draft, "review_round"), DispatchSet)
    rejected = GateRecord("g2", "rejected", "findings/g2.md")
    approved = GateRecord("g1", "approved", None)
    draft.open_round = OpenRound(
        "review_round", 0, ("g1", "g2"), MappingProxyType({"g2": rejected, "g1": approved})
    )
    step = close_round(graph, _NO_ANSWERS, draft, "review_round")
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
    assert draft.round_numbers == {"review_round": 1}
