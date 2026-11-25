"""The rule this file exists to enforce: `graphscene.engine.static_check.static_violations` returns
the reference violations alone when there are any, and otherwise the violations of checks 1
(`reachable-from-start`), 2 (`reaches-terminal`), 3 (`fail-cycle-capped`), 8 (`gate-in-round`)
and 9 (`round-fan-out`), in that order and in the report order `graphscene.engine.static_check`
states, each reason opening with its check id.

Each planted graph is a complete format-4 mapping built with
`graphscene.adapters.builder.build_flow_graph`. `_base` is a clean one-round graph; each case
changes it, or plants its own graph, so that one clause fires, and asserts the exact list
returned. Each review-loop clause of checks 8 and 9 is planted on both kinds of round: on a review
loop it fires, and on a plain round (`_plain_round`, no `writer`) the same graph returns nothing,
while the round rules fire on both. Check 8's graph-wide clause is planted on a graph declaring a
review loop, where it fires, and on one declaring none, where it does not run. A fail cycle closed
through a plain round's fan-out is planted on a graph declaring no review loop, where check 3
names it.
`valid_generic.json` and `valid_plain_round.json` return nothing, and each
`static_negative_*.json` fixture in `_NEGATIVES`, a schema-valid copy of `valid_generic.json` with
one change, returns exactly its one violation. Expected values are hand-written from reading each
graph.

Deliberately not covered:
- Checks 4–7: they read a host's own documents, and belong to the host, not to this package.
- What runs a node: a harness check, outside this package.
"""

import json
from pathlib import Path

from graphscene.adapters.builder import build_flow_graph
from graphscene.engine.static_check import static_violations
from graphscene.model.errors import Violation

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"

_NEGATIVES: list[tuple[str, Violation]] = [
    (
        "static_negative_reachable_from_start.json",
        Violation(
            "nodes.orphan", "reachable-from-start: node 'orphan' is not reached from start 'draft'"
        ),
    ),
    (
        "static_negative_reaches_terminal.json",
        Violation(
            "nodes.published",
            "reaches-terminal: node 'published' reaches no terminal node and no stop binding",
        ),
    ),
    (
        "static_negative_fail_cycle_capped.json",
        Violation(
            "nodes.review_round.outcomes.rejected",
            "fail-cycle-capped: outcome 'rejected' routes 'review_round' -> 'draft' with no "
            "increment, and 'draft' reaches 'review_round' again",
        ),
    ),
    (
        "static_negative_gate_in_round.json",
        Violation(
            "nodes.review_round.gates[1]",
            "gate-in-round: round 'review_round' names 'published' as a gate, which is not a "
            "dispatch node",
        ),
    ),
    (
        "static_negative_round_fan_out.json",
        Violation(
            "nodes.edit_check.outcomes.approved",
            "round-fan-out: gate 'edit_check' of round 'review_round' does not route outcome "
            "'approved' to the round",
        ),
    ),
]

_HALT_ON_CAP: dict[str, object] = {"binding": "<halt>", "reason": "limit"}
_TERMINAL: dict[str, object] = {"kind": "terminal", "binding": "<finish>"}


def _vocabulary() -> dict[str, object]:
    return {
        "outcomes": {
            "done": {},
            "approved": {"verdict": "pass"},
            "rejected": {"verdict": "fail"},
            "crashed": {"held": True},
        },
        "bindings": {
            "<pause>": {"primitive": "interrupt", "resumeOutcome": "done"},
            "<halt>": {"primitive": "stop", "reasons": ["limit", "crash"]},
            "<finish>": {"primitive": "end"},
        },
        "predicates": {"off": {"records": "bypassed", "inRoundCounts": False}},
    }


def _dispatch(outcomes: dict[str, object], **extra: object) -> dict[str, object]:
    return {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "[work] → worker",
        "outcomes": outcomes,
        **extra,
    }


def _round(**overrides: object) -> dict[str, object]:
    node: dict[str, object] = {
        "kind": "round",
        "parallel": False,
        "gates": ["g"],
        "writer": "a",
        "counter": "n",
        "convergingFrom": 1,
        "outcomes": {
            "approved": {"to": "t"},
            "rejected": {"to": "a", "increment": "n", "onCap": _HALT_ON_CAP},
        },
    }
    node.update(overrides)
    return node


def _plain_round(**overrides: object) -> dict[str, object]:
    node = _round()
    for key in ("writer", "counter", "convergingFrom"):
        del node[key]
    node.update(overrides)
    return node


def _gate(**overrides: object) -> dict[str, object]:
    node = _dispatch({"approved": {"to": "r"}, "rejected": {"to": "r"}})
    node.update(overrides)
    return node


def _base() -> dict[str, dict[str, object]]:
    """Writer `a` routes to round `r`, whose one gate `g` routes both verdicts back to it; `r`
    approves to terminal `t` and rejects to `a` with an increment."""
    return {
        "a": _dispatch({"done": {"to": "r"}}),
        "g": _gate(),
        "r": _round(),
        "t": _TERMINAL,
    }


def _graph(nodes: dict[str, dict[str, object]], **overrides: object) -> dict[str, object]:
    graph: dict[str, object] = {
        "formatVersion": 4,
        "flow": "planted",
        "description": "A planted graph.",
        "vocabulary": _vocabulary(),
        "start": "a",
        "entries": ["a"],
        "counters": {"n": {"cap": 2}},
        "paths": {"p": "{state_dir}/p.md"},
        "reports": ["slot"],
        "nodes": nodes,
    }
    graph.update(overrides)
    return graph


def _check(nodes: dict[str, dict[str, object]], **overrides: object) -> list[Violation]:
    return static_violations(build_flow_graph(_graph(nodes, **overrides)))


def _load(name: str) -> dict[str, object]:
    parsed: object = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def test_the_planted_base_graph_has_no_violation() -> None:
    assert _check(_base()) == []


def test_reachable_from_start_a_node_reached_only_by_fan_out_is_reached() -> None:
    # In `_base`, gate `g` is reached only by `r`'s fan-out.
    assert _check(_base()) == []


def test_reachable_from_start_a_node_reached_only_by_an_interrupt_resume_is_reached() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"binding": "<pause>", "resume": "h"}})
    nodes["h"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes) == []


def test_reachable_from_start_a_node_reached_only_by_a_skip_is_reached() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}}, skip=[{"when": "off", "to": "h"}])
    nodes["h"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes) == []


def test_reachable_from_start_an_unreached_node_is_named() -> None:
    nodes = _base()
    nodes["z"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes) == [
        Violation("nodes.z", "reachable-from-start: node 'z' is not reached from start 'a'")
    ]


def test_reaches_terminal_a_stop_binding_edge_makes_a_sink() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"to": "h"}})
    nodes["h"] = _dispatch({"crashed": {"binding": "<halt>", "reason": "crash"}})
    assert _check(nodes) == []


def test_reaches_terminal_an_on_cap_stop_makes_a_sink() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch({"done": {"to": "a", "increment": "n", "onCap": _HALT_ON_CAP}})
    }
    assert _check(nodes) == []


def test_reaches_terminal_an_interrupt_binding_edge_does_not_make_a_sink() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch({"done": {"to": "t"}, "crashed": {"to": "h"}}),
        "h": _dispatch({"crashed": {"binding": "<pause>", "resume": "h"}}),
        "t": _TERMINAL,
    }
    assert _check(nodes) == [
        Violation(
            "nodes.h", "reaches-terminal: node 'h' reaches no terminal node and no stop binding"
        )
    ]


def test_fail_cycle_capped_an_uncapped_fail_edge_closing_a_cycle_is_named() -> None:
    nodes = _base()
    nodes["r"] = _round(outcomes={"approved": {"to": "t"}, "rejected": {"to": "a"}})
    assert _check(nodes) == [
        Violation(
            "nodes.r.outcomes.rejected",
            "fail-cycle-capped: outcome 'rejected' routes 'r' -> 'a' with no increment, and 'a' "
            "reaches 'r' again",
        )
    ]


def test_fail_cycle_capped_a_fail_edge_carrying_an_increment_is_exempt() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch(
            {
                "done": {"to": "t"},
                "rejected": {"to": "a", "increment": "n", "onCap": _HALT_ON_CAP},
            }
        ),
        "t": _TERMINAL,
    }
    assert _check(nodes) == []


def test_fail_cycle_capped_a_cycle_closed_only_through_fan_out_is_not_reported() -> None:
    # In `_base`, `g` rejects to `r` with no increment, and `r` reaches `g` only by fan-out.
    assert _check(_base()) == []


def test_fail_cycle_capped_a_cycle_closed_only_through_a_resume_is_not_reported() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch({"crashed": {"binding": "<pause>", "resume": "b"}}),
        "b": _dispatch({"done": {"to": "r"}}),
        "g": _gate(),
        "r": _round(writer="b", outcomes={"approved": {"to": "t"}, "rejected": {"to": "a"}}),
        "t": _TERMINAL,
    }
    assert _check(nodes) == []


def test_fail_cycle_capped_a_cycle_through_a_plain_rounds_fan_out_is_named() -> None:
    # `a` is no gate; it rejects into plain round `r` with no increment, and gate `g`'s held
    # outcome routes back to `a`, so the cycle closes through `r`'s fan-out.
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "rejected": {"to": "r"}})
    nodes["g"] = _gate(
        outcomes={"approved": {"to": "r"}, "rejected": {"to": "r"}, "crashed": {"to": "a"}}
    )
    nodes["r"] = _plain_round()
    assert _check(nodes) == [
        Violation(
            "nodes.a.outcomes.rejected",
            "fail-cycle-capped: outcome 'rejected' routes 'a' -> 'r' with no increment, and 'r' "
            "reaches 'a' again",
        )
    ]


def test_gate_in_round_a_gate_in_zero_rounds_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "rejected": {"to": "t"}})
    assert _check(nodes) == [
        Violation(
            "nodes.a",
            "gate-in-round: node 'a' routes a fail verdict with no increment and is a gate of 0 "
            "round nodes, not exactly one",
        )
    ]


def test_gate_in_round_a_graph_declaring_no_review_loop_runs_no_graph_wide_clause() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch({"done": {"to": "t"}, "rejected": {"to": "t"}}),
        "t": _TERMINAL,
    }
    assert _check(nodes) == []


def test_gate_in_round_a_plain_round_runs_no_graph_wide_clause() -> None:
    # The graph of `test_gate_in_round_a_gate_in_zero_rounds_is_named`, with `r` a plain round.
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "rejected": {"to": "t"}})
    nodes["r"] = _plain_round()
    assert _check(nodes) == []


def test_gate_in_round_a_plain_round_naming_a_non_dispatch_gate_is_named() -> None:
    nodes = _base()
    nodes["r"] = _plain_round(gates=["g", "t"])
    assert _check(nodes) == [
        Violation(
            "nodes.r.gates[1]",
            "gate-in-round: round 'r' names 't' as a gate, which is not a dispatch node",
        )
    ]


def test_gate_in_round_a_gate_in_two_rounds_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "approved": {"to": "r2"}})
    nodes["r2"] = _round()
    assert _check(nodes) == [
        Violation(
            "nodes.g",
            "gate-in-round: node 'g' routes a fail verdict with no increment and is a gate of 2 "
            "round nodes, not exactly one",
        ),
        Violation(
            "nodes.g.outcomes.approved",
            "round-fan-out: gate 'g' of round 'r2' does not route outcome 'approved' to the round",
        ),
        Violation(
            "nodes.g.outcomes.rejected",
            "round-fan-out: gate 'g' of round 'r2' does not route outcome 'rejected' to the round",
        ),
    ]


def test_gate_in_round_an_incrementing_fail_edge_is_not_selected() -> None:
    nodes: dict[str, dict[str, object]] = {
        "a": _dispatch(
            {
                "done": {"to": "t"},
                "rejected": {"to": "t", "increment": "n", "onCap": _HALT_ON_CAP},
            }
        ),
        "t": _TERMINAL,
    }
    assert _check(nodes) == []


def test_gate_in_round_a_non_dispatch_gate_is_named() -> None:
    nodes = _base()
    nodes["r"] = _round(gates=["g", "t"])
    assert _check(nodes) == [
        Violation(
            "nodes.r.gates[1]",
            "gate-in-round: round 'r' names 't' as a gate, which is not a dispatch node",
        )
    ]


def test_gate_in_round_a_non_dispatch_writer_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "t"}})
    nodes["r"] = _round(writer="t")
    assert _check(nodes, start="r", entries=["r"]) == [
        Violation(
            "nodes.r.writer",
            "gate-in-round: round 'r' names 't' as its writer, which is not a dispatch node",
        )
    ]


def test_round_fan_out_i_a_verdict_route_edge_not_to_the_round_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(outcomes={"approved": {"to": "t"}, "rejected": {"to": "r"}})
    assert _check(nodes) == [
        Violation(
            "nodes.g.outcomes.approved",
            "round-fan-out: gate 'g' of round 'r' does not route outcome 'approved' to the round",
        )
    ]


def test_round_fan_out_i_a_verdict_outcome_that_is_a_binding_edge_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(
        outcomes={
            "approved": {"binding": "<halt>", "reason": "crash"},
            "rejected": {"to": "r"},
        }
    )
    assert _check(nodes) == [
        Violation(
            "nodes.g.outcomes.approved",
            "round-fan-out: gate 'g' of round 'r' does not route outcome 'approved' to the round",
        )
    ]


def test_round_fan_out_ii_a_gate_with_no_pass_outcome_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(outcomes={"rejected": {"to": "r"}})
    assert _check(nodes) == [
        Violation(
            "nodes.g.outcomes",
            "round-fan-out: gate 'g' of round 'r' routes no outcome declaring verdict pass",
        )
    ]


def test_round_fan_out_i_a_plain_round_gate_routing_a_verdict_elsewhere_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(outcomes={"approved": {"to": "t"}, "rejected": {"to": "r"}})
    nodes["r"] = _plain_round()
    assert _check(nodes) == [
        Violation(
            "nodes.g.outcomes.approved",
            "round-fan-out: gate 'g' of round 'r' does not route outcome 'approved' to the round",
        )
    ]


def test_round_fan_out_ii_a_plain_round_gate_with_no_pass_outcome_is_not_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(outcomes={"rejected": {"to": "r"}})
    nodes["r"] = _plain_round()
    assert _check(nodes) == []


def test_round_fan_out_iii_a_gate_skipping_elsewhere_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(skip=[{"when": "off", "to": "t"}])
    assert _check(nodes) == [
        Violation(
            "nodes.g.skip[0].to",
            "round-fan-out: gate 'g' of round 'r' skips to 't', not to the round",
        )
    ]


def test_round_fan_out_iii_a_plain_round_gate_skipping_elsewhere_is_named() -> None:
    nodes = _base()
    nodes["g"] = _gate(skip=[{"when": "off", "to": "t"}])
    nodes["r"] = _plain_round()
    assert _check(nodes) == [
        Violation(
            "nodes.g.skip[0].to",
            "round-fan-out: gate 'g' of round 'r' skips to 't', not to the round",
        )
    ]


def test_round_fan_out_iv_a_writer_routing_nothing_to_the_round_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes, start="r", entries=["r"]) == [
        Violation(
            "nodes.r.writer",
            "round-fan-out: writer 'a' of round 'r' routes no outcome to the round",
        )
    ]


def test_round_fan_out_v_a_route_from_another_node_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"to": "h"}})
    nodes["h"] = _dispatch({"done": {"to": "r"}})
    assert _check(nodes) == [
        Violation(
            "nodes.h.outcomes.done",
            "round-fan-out: round 'r' is targeted by 'h' outcome 'done', which is neither a "
            "verdict edge of one of its gates nor an edge of its writer",
        )
    ]


def test_round_fan_out_v_a_resume_into_the_round_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"to": "h"}})
    nodes["h"] = _dispatch({"crashed": {"binding": "<pause>", "resume": "r"}})
    assert _check(nodes) == [
        Violation(
            "nodes.h.outcomes.crashed",
            "round-fan-out: round 'r' is targeted by 'h' outcome 'crashed', which is neither a "
            "verdict edge of one of its gates nor an edge of its writer",
        )
    ]


def test_round_fan_out_v_a_skip_from_a_node_that_is_not_a_gate_is_named() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"to": "h"}})
    nodes["h"] = _dispatch({"done": {"to": "t"}}, skip=[{"when": "off", "to": "r"}])
    assert _check(nodes) == [
        Violation(
            "nodes.h.skip[0]",
            "round-fan-out: round 'r' is targeted by a skip of 'h', which is not one of its gates",
        )
    ]


def test_round_fan_out_v_a_plain_round_admits_a_route_from_a_node_that_is_no_writer() -> None:
    # On a review loop `a` is the writer; on a plain round it is only another node routing in.
    nodes = _base()
    nodes["r"] = _plain_round()
    assert _check(nodes) == []


def test_a_reference_violation_is_returned_alone() -> None:
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "crashed": {"to": "zz"}})
    nodes["z"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes) == [
        Violation("nodes.a.outcomes.crashed.to", "node-known: 'zz' is not a node")
    ]


def test_two_checks_firing_come_back_in_check_order() -> None:
    nodes = _base()
    nodes["g"] = _gate(outcomes={"approved": {"to": "t"}, "rejected": {"to": "r"}})
    nodes["z"] = _dispatch({"done": {"to": "t"}})
    assert _check(nodes) == [
        Violation("nodes.z", "reachable-from-start: node 'z' is not reached from start 'a'"),
        Violation(
            "nodes.g.outcomes.approved",
            "round-fan-out: gate 'g' of round 'r' does not route outcome 'approved' to the round",
        ),
    ]


def test_the_valid_generic_graph_has_no_violation() -> None:
    assert static_violations(build_flow_graph(_load("valid_generic.json"))) == []


def test_the_valid_plain_round_graph_has_no_violation() -> None:
    assert static_violations(build_flow_graph(_load("valid_plain_round.json"))) == []


def test_each_static_negative_fixture_returns_exactly_its_one_violation() -> None:
    for name, expected in _NEGATIVES:
        assert static_violations(build_flow_graph(_load(name))) == [expected], name
