"""The rule this file exists to enforce: every node, counter, path, report-slot and prompt name a
built flow graph uses exists, `start` is listed in `entries`, and each violation's reason opens
with its check id (`graphscene.engine.references.reference_violations`).

Each planted graph is a complete format-5 mapping built with
`graphscene.adapters.builder.build_flow_graph`, so the check reads what the builder produces.
Each id position has a planted case asserting the exact list returned, and a round declaring no
`writer` and no `counter` has one asserting neither is reported; `valid_generic.json`
returns nothing; and each `static_negative_*.json` fixture in `_NEGATIVES`, a schema-valid copy of
it with one change, returns exactly its one violation. Expected values are hand-written from
reading each planted graph.

Deliberately not covered:
- Binding, outcome and predicate names: the vocabulary check's
  (`graphscene/tests/engine/test_vocabulary.py`).
- Reachability, termination, caps and round shape: the graph checks of
  `graphscene.engine.static_check`.
"""

import json
from pathlib import Path

from graphscene.adapters.builder import build_flow_graph
from graphscene.engine.references import reference_violations
from graphscene.model.errors import Violation

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"

_NEGATIVES: list[tuple[str, Violation]] = [
    (
        "static_negative_node_known.json",
        Violation("nodes.draft.outcomes.done.to", "node-known: 'review' is not a node"),
    ),
]


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
        "gates": ["a"],
        "writer": "a",
        "counter": "n",
        "convergingFrom": 1,
        "outcomes": {"approved": {"to": "t"}, "rejected": {"to": "a"}},
    }
    node.update(overrides)
    return node


_TERMINAL: dict[str, object] = {"kind": "terminal", "binding": "<finish>"}


def _graph(nodes: dict[str, object], **overrides: object) -> dict[str, object]:
    graph: dict[str, object] = {
        "formatVersion": 5,
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


def _a(outcomes: dict[str, object], **extra: object) -> dict[str, object]:
    """Node `a`, a dispatch node declaring the prompt `first`."""
    return _dispatch(outcomes, prompts=["first"], **extra)


def _check(graph: dict[str, object]) -> list[Violation]:
    return reference_violations(build_flow_graph(graph))


def _load(name: str) -> dict[str, object]:
    parsed: object = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def test_the_planted_base_graph_has_no_violation() -> None:
    graph = _graph(
        {"a": _a({"done": {"to": "t"}, "rejected": {"to": "a", "prompt": "first"}}), "t": _TERMINAL}
    )
    assert _check(graph) == []


def test_node_known_an_unknown_start_is_reported_once_as_node_known() -> None:
    graph = _graph({"a": _a({"done": {"to": "t"}}), "t": _TERMINAL}, start="zz")
    assert _check(graph) == [Violation("start", "node-known: 'zz' is not a node")]


def test_node_known_an_unknown_entry_is_named() -> None:
    graph = _graph({"a": _a({"done": {"to": "t"}}), "t": _TERMINAL}, entries=["a", "zz"])
    assert _check(graph) == [Violation("entries[1]", "node-known: 'zz' is not a node")]


def test_node_known_an_unknown_gate_and_writer_are_named() -> None:
    graph = _graph(
        {
            "a": _a({"done": {"to": "r"}}),
            "r": _round(gates=["a", "zz"], writer="yy"),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.r.gates[1]", "node-known: 'zz' is not a node"),
        Violation("nodes.r.writer", "node-known: 'yy' is not a node"),
    ]


def test_a_plain_round_declaring_no_writer_and_no_counter_reports_neither() -> None:
    plain = _round()
    for key in ("writer", "counter", "convergingFrom"):
        del plain[key]
    graph = _graph({"a": _a({"done": {"to": "r"}}), "r": plain, "t": _TERMINAL})
    assert _check(graph) == []


def test_node_known_an_unknown_route_to_is_named() -> None:
    graph = _graph({"a": _a({"done": {"to": "zz"}}), "t": _TERMINAL})
    assert _check(graph) == [
        Violation("nodes.a.outcomes.done.to", "node-known: 'zz' is not a node")
    ]


def test_node_known_an_unknown_interrupt_resume_is_named() -> None:
    graph = _graph(
        {
            "a": _a({"done": {"to": "t"}, "crashed": {"binding": "<pause>", "resume": "zz"}}),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.a.outcomes.crashed.resume", "node-known: 'zz' is not a node")
    ]


def test_node_known_an_unknown_skip_to_is_named() -> None:
    graph = _graph(
        {
            "a": _a(
                {"done": {"to": "t"}},
                skip=[{"when": "off", "to": "t"}, {"when": "off", "to": "zz"}],
            ),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [Violation("nodes.a.skip[1].to", "node-known: 'zz' is not a node")]


def test_node_known_an_unknown_round_count_is_named_on_an_edge_and_an_on_cap() -> None:
    graph = _graph(
        {
            "a": _a(
                {
                    "crashed": {
                        "binding": "<halt>",
                        "reason": "crash",
                        "roundCounts": ["a", "zz"],
                    },
                    "rejected": {
                        "to": "a",
                        "increment": "n",
                        "onCap": {"binding": "<halt>", "reason": "limit", "roundCounts": ["yy"]},
                    },
                }
            ),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.a.outcomes.crashed.roundCounts[1]", "node-known: 'zz' is not a node"),
        Violation(
            "nodes.a.outcomes.rejected.onCap.roundCounts[0]", "node-known: 'yy' is not a node"
        ),
    ]


def test_counter_known_an_unknown_increment_and_reset_are_named() -> None:
    graph = _graph(
        {
            "a": _a({"done": {"to": "t", "reset": "m"}, "rejected": {"to": "a", "increment": "k"}}),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.a.outcomes.done.reset", "counter-known: 'm' is not declared in counters"),
        Violation(
            "nodes.a.outcomes.rejected.increment", "counter-known: 'k' is not declared in counters"
        ),
    ]


def test_counter_known_an_unknown_round_counter_is_named() -> None:
    graph = _graph({"a": _a({"done": {"to": "r"}}), "r": _round(counter="m"), "t": _TERMINAL})
    assert _check(graph) == [
        Violation("nodes.r.counter", "counter-known: 'm' is not declared in counters")
    ]


def test_path_known_an_unknown_plan_entry_and_revision_note_are_named() -> None:
    graph = _graph(
        {
            "a": _a({"done": {"to": "r"}}),
            "r": _round(plan=["p", "q"], revisionNote="s"),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.r.plan[1]", "path-known: 'q' is not declared in paths"),
        Violation("nodes.r.revisionNote", "path-known: 's' is not declared in paths"),
    ]


def test_path_known_an_unknown_evidence_is_named_on_an_edge_and_an_on_cap() -> None:
    graph = _graph(
        {
            "a": _a(
                {
                    "crashed": {"binding": "<halt>", "reason": "crash", "evidence": "q"},
                    "rejected": {
                        "to": "a",
                        "increment": "n",
                        "onCap": {"binding": "<halt>", "reason": "limit", "evidence": "s"},
                    },
                }
            ),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation("nodes.a.outcomes.crashed.evidence", "path-known: 'q' is not declared in paths"),
        Violation(
            "nodes.a.outcomes.rejected.onCap.evidence", "path-known: 's' is not declared in paths"
        ),
    ]


def test_report_slot_known_an_unknown_slot_is_named_on_an_edge_and_a_skip_entry() -> None:
    graph = _graph(
        {
            "a": _a(
                {"done": {"to": "t", "report": {"slot": "x", "other": "y"}}},
                skip=[{"when": "off", "to": "t", "report": {"gone": "z"}}],
            ),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation(
            "nodes.a.outcomes.done.report.other",
            "report-slot-known: 'other' is not declared in reports",
        ),
        Violation(
            "nodes.a.skip[0].report.gone", "report-slot-known: 'gone' is not declared in reports"
        ),
    ]


def test_prompt_known_a_target_lacking_the_prompt_is_named() -> None:
    graph = _graph({"a": _a({"done": {"to": "a", "prompt": "rework"}}), "t": _TERMINAL})
    assert _check(graph) == [
        Violation(
            "nodes.a.outcomes.done.prompt",
            "prompt-known: 'rework' is not a prompt node 'a' declares",
        )
    ]


def test_prompt_known_a_target_dispatch_node_with_no_prompts_is_named() -> None:
    graph = _graph(
        {
            "a": _a({"done": {"to": "b", "prompt": "first"}}),
            "b": _dispatch({"done": {"to": "t"}}),
            "t": _TERMINAL,
        }
    )
    assert _check(graph) == [
        Violation(
            "nodes.a.outcomes.done.prompt",
            "prompt-known: 'first' is not a prompt node 'b' declares",
        )
    ]


def test_prompt_known_a_target_round_node_is_named() -> None:
    graph = _graph(
        {"a": _a({"done": {"to": "r", "prompt": "first"}}), "r": _round(), "t": _TERMINAL}
    )
    assert _check(graph) == [
        Violation(
            "nodes.a.outcomes.done.prompt",
            "prompt-known: 'first' is not a prompt node 'r' declares",
        )
    ]


def test_an_unknown_to_carrying_a_prompt_reports_node_known_alone() -> None:
    graph = _graph({"a": _a({"done": {"to": "zz", "prompt": "first"}}), "t": _TERMINAL})
    assert _check(graph) == [
        Violation("nodes.a.outcomes.done.to", "node-known: 'zz' is not a node")
    ]


def test_start_in_entries_a_start_missing_from_entries_is_named() -> None:
    graph = _graph({"a": _a({"done": {"to": "t"}}), "t": _TERMINAL}, entries=["t"])
    assert _check(graph) == [
        Violation("entries", "start-in-entries: start 'a' is not listed in entries")
    ]


def test_violations_come_in_document_order() -> None:
    graph = _graph(
        {
            "r": _round(
                writer="zz",
                revisionNote="s",
                outcomes={
                    "approved": {"to": "t"},
                    "rejected": {
                        "to": "a",
                        "increment": "m",
                        "prompt": "nope",
                        "report": {"zeta": "x", "slot": "y", "alpha": "z"},
                    },
                },
            ),
            "a": _a({"done": {"to": "r"}}, skip=[{"when": "off", "to": "yy"}]),
            "t": _TERMINAL,
        },
        start="a",
        entries=["r", "xx"],
    )
    assert _check(graph) == [
        Violation("entries[1]", "node-known: 'xx' is not a node"),
        Violation("entries", "start-in-entries: start 'a' is not listed in entries"),
        Violation("nodes.r.writer", "node-known: 'zz' is not a node"),
        Violation("nodes.r.revisionNote", "path-known: 's' is not declared in paths"),
        Violation(
            "nodes.r.outcomes.rejected.increment", "counter-known: 'm' is not declared in counters"
        ),
        Violation(
            "nodes.r.outcomes.rejected.prompt",
            "prompt-known: 'nope' is not a prompt node 'a' declares",
        ),
        Violation(
            "nodes.r.outcomes.rejected.report.zeta",
            "report-slot-known: 'zeta' is not declared in reports",
        ),
        Violation(
            "nodes.r.outcomes.rejected.report.alpha",
            "report-slot-known: 'alpha' is not declared in reports",
        ),
        Violation("nodes.a.skip[0].to", "node-known: 'yy' is not a node"),
    ]


def test_the_valid_generic_fixture_has_no_violation() -> None:
    assert _check(_load("valid_generic.json")) == []


def test_each_static_negative_fixture_returns_its_one_violation() -> None:
    for name, expected in _NEGATIVES:
        assert _check(_load(name)) == [expected], name
