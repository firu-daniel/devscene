"""The rule this file exists to enforce: every name a flow graph uses is one it declares, and each
binding is used where its primitive allows (`graphscene.engine.vocabulary.vocabulary_violations`).

The check reads the built model: every graph here goes through
`graphscene.adapters.builder.build_flow_graph` first, and the check returns `Violation` values
(`graphscene.model.errors.Violation`). Each clause has a planted in-test graph asserting the exact
list returned; `valid_generic.json` returns nothing; and each `vocabulary_negative_*.json` fixture,
a schema-valid copy of it with one change, returns exactly its one violation. One case renders the
check's `Violation` values back to the strings it returned before it used them.

Deliberately not covered:
- Schema validity: the fixtures are validated against the schema from the repository root, and the
  check assumes a schema-valid graph.
- Node-id references, reachability and counter caps: the static checker's
  (`graphscene.engine.static_check`).
"""

import json
from pathlib import Path

from graphscene.adapters.builder import build_flow_graph
from graphscene.engine.vocabulary import vocabulary_violations
from graphscene.model.errors import Violation
from graphscene.model.flow_graph import FlowGraph

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"

_NEGATIVES: list[tuple[str, Violation]] = [
    (
        "vocabulary_negative_unknown_outcome.json",
        Violation(
            "nodes.draft.outcomes.finished",
            "outcome 'finished' is not declared in vocabulary.outcomes",
        ),
    ),
    (
        "vocabulary_negative_unknown_binding.json",
        Violation(
            "nodes.draft.outcomes.crashed.binding",
            "binding '<abort>' is not declared in vocabulary.bindings",
        ),
    ),
    (
        "vocabulary_negative_interrupt_without_resume.json",
        Violation(
            "nodes.draft.outcomes.crashed", "binding '<pause>' is an interrupt and needs resume"
        ),
    ),
    (
        "vocabulary_negative_undeclared_reason.json",
        Violation(
            "nodes.draft.outcomes.crashed.reason",
            "'timeout' is not a reason binding '<halt>' declares",
        ),
    ),
    (
        "vocabulary_negative_round_without_fail_verdict.json",
        Violation(
            "nodes.review_round.outcomes",
            "a round routes on one outcome declaring verdict pass and one declaring verdict fail",
        ),
    ),
    (
        "vocabulary_negative_end_on_an_edge.json",
        Violation(
            "nodes.draft.outcomes.crashed.binding",
            "binding '<finish>' is an end; only a terminal node takes one",
        ),
    ),
    (
        "vocabulary_negative_unknown_predicate.json",
        Violation(
            "nodes.edit_check.skip[0].when",
            "predicate 'stage_off' is not declared in vocabulary.predicates",
        ),
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


def _graph(nodes: dict[str, object], vocabulary: dict[str, object] | None = None) -> FlowGraph:
    return build_flow_graph(
        {
            "formatVersion": 5,
            "flow": "planted",
            "description": "a planted graph",
            "vocabulary": _vocabulary() if vocabulary is None else vocabulary,
            "start": "a",
            "entries": ["a"],
            "counters": {},
            "paths": {},
            "reports": [],
            "nodes": nodes,
        }
    )


def _dispatch(outcomes: dict[str, object], **extra: object) -> dict[str, object]:
    return {
        "kind": "dispatch",
        "agent": "worker",
        "heartbeat": "beat",
        "outcomes": outcomes,
        **extra,
    }


def _round(outcomes: dict[str, object]) -> dict[str, object]:
    return {
        "kind": "round",
        "parallel": False,
        "gates": [],
        "writer": "w",
        "counter": "n",
        "convergingFrom": 1,
        "outcomes": outcomes,
    }


def _load(name: str) -> FlowGraph:
    parsed: object = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return build_flow_graph(parsed)


def test_clause_1_an_undeclared_outcome_is_named() -> None:
    graph = _graph({"a": _dispatch({"stalled": {"to": "a"}})})
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.a.outcomes.stalled", "outcome 'stalled' is not declared in vocabulary.outcomes"
        )
    ]


def test_clause_2_a_round_without_a_pass_and_a_fail_verdict_is_named_once() -> None:
    graph = _graph({"r": _round({"approved": {"to": "r"}, "done": {"to": "r"}})})
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.r.outcomes",
            "a round routes on one outcome declaring verdict pass and one declaring verdict fail",
        )
    ]


def test_clause_2_is_not_reported_when_a_round_outcome_is_undeclared() -> None:
    graph = _graph({"r": _round({"approved": {"to": "r"}, "stalled": {"to": "r"}})})
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.r.outcomes.stalled", "outcome 'stalled' is not declared in vocabulary.outcomes"
        )
    ]


def test_clause_3_an_undeclared_binding_is_named_on_an_edge_an_on_cap_and_a_terminal() -> None:
    graph = _graph(
        {
            "a": _dispatch(
                {
                    "done": {"binding": "<abort>", "reason": "crash"},
                    "rejected": {
                        "to": "a",
                        "increment": "n",
                        "onCap": {"binding": "<quit>", "reason": "limit"},
                    },
                }
            ),
            "t": {"kind": "terminal", "binding": "<gone>"},
        }
    )
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.a.outcomes.done.binding",
            "binding '<abort>' is not declared in vocabulary.bindings",
        ),
        Violation(
            "nodes.a.outcomes.rejected.onCap.binding",
            "binding '<quit>' is not declared in vocabulary.bindings",
        ),
        Violation("nodes.t.binding", "binding '<gone>' is not declared in vocabulary.bindings"),
    ]


def test_clause_4_an_end_on_an_edge_is_named() -> None:
    graph = _graph({"a": _dispatch({"done": {"binding": "<finish>"}})})
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.a.outcomes.done.binding",
            "binding '<finish>' is an end; only a terminal node takes one",
        )
    ]


def test_clause_4_a_terminal_binding_that_is_not_an_end_is_named() -> None:
    graph = _graph({"t": {"kind": "terminal", "binding": "<halt>"}})
    assert vocabulary_violations(graph) == [
        Violation("nodes.t.binding", "binding '<halt>' is not an end")
    ]


def test_clause_5_an_interrupt_without_resume_is_named() -> None:
    graph = _graph({"a": _dispatch({"done": {"binding": "<pause>"}})})
    assert vocabulary_violations(graph) == [
        Violation("nodes.a.outcomes.done", "binding '<pause>' is an interrupt and needs resume")
    ]


def test_clause_5_a_resume_on_a_non_interrupt_edge_is_named() -> None:
    edge = {"binding": "<halt>", "reason": "crash", "resume": "a"}
    graph = _graph({"a": _dispatch({"done": edge})})
    assert vocabulary_violations(graph) == [
        Violation("nodes.a.outcomes.done.resume", "binding '<halt>' is not an interrupt")
    ]


def test_clause_6_a_stop_without_reason_is_named() -> None:
    graph = _graph({"a": _dispatch({"done": {"binding": "<halt>"}})})
    assert vocabulary_violations(graph) == [
        Violation("nodes.a.outcomes.done", "binding '<halt>' is a stop and needs reason")
    ]


def test_clause_6_an_undeclared_reason_is_named_on_an_edge_and_an_on_cap() -> None:
    graph = _graph(
        {
            "a": _dispatch(
                {
                    "done": {"binding": "<halt>", "reason": "timeout"},
                    "rejected": {
                        "to": "a",
                        "increment": "n",
                        "onCap": {"binding": "<halt>", "reason": "tired"},
                    },
                }
            )
        }
    )
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.a.outcomes.done.reason", "'timeout' is not a reason binding '<halt>' declares"
        ),
        Violation(
            "nodes.a.outcomes.rejected.onCap.reason",
            "'tired' is not a reason binding '<halt>' declares",
        ),
    ]


def test_clause_6_a_reason_on_an_interrupt_edge_is_named() -> None:
    edge = {"binding": "<pause>", "resume": "a", "reason": "x"}
    graph = _graph({"a": _dispatch({"done": edge})})
    assert vocabulary_violations(graph) == [
        Violation("nodes.a.outcomes.done.reason", "binding '<pause>' is not a stop")
    ]


def test_clause_6_an_on_cap_whose_binding_is_not_a_stop_is_named() -> None:
    graph = _graph(
        {
            "a": _dispatch(
                {
                    "rejected": {
                        "to": "a",
                        "increment": "n",
                        "onCap": {"binding": "<pause>", "reason": "limit"},
                    }
                }
            )
        }
    )
    assert vocabulary_violations(graph) == [
        Violation("nodes.a.outcomes.rejected.onCap.binding", "binding '<pause>' is not a stop")
    ]


def test_clause_7_an_undeclared_skip_predicate_is_named() -> None:
    graph = _graph(
        {
            "a": _dispatch(
                {"done": {"to": "a"}},
                skip=[{"when": "off", "to": "a"}, {"when": "never", "to": "a"}],
            )
        }
    )
    assert vocabulary_violations(graph) == [
        Violation(
            "nodes.a.skip[1].when", "predicate 'never' is not declared in vocabulary.predicates"
        )
    ]


def test_violations_come_in_document_order() -> None:
    graph = _graph(
        {
            "b": _dispatch({"zeta": {"to": "a"}}, skip=[{"when": "never", "to": "a"}]),
            "a": _dispatch({"done": {"binding": "<halt>"}}),
        }
    )
    assert vocabulary_violations(graph) == [
        Violation("nodes.b.outcomes.zeta", "outcome 'zeta' is not declared in vocabulary.outcomes"),
        Violation(
            "nodes.b.skip[0].when", "predicate 'never' is not declared in vocabulary.predicates"
        ),
        Violation("nodes.a.outcomes.done", "binding '<halt>' is a stop and needs reason"),
    ]


def test_the_valid_generic_fixture_has_no_violation() -> None:
    assert vocabulary_violations(_load("valid_generic.json")) == []


def test_each_vocabulary_negative_fixture_returns_its_one_violation() -> None:
    for name, expected in _NEGATIVES:
        assert vocabulary_violations(_load(name)) == [expected], name


def test_vocabulary_violations_render_to_the_strings_the_check_returned_before() -> None:
    graph = _graph(
        {"a": _dispatch({"stalled": {"to": "a"}}, skip=[{"when": "never", "to": "a"}])},
        vocabulary={"outcomes": {"done": {}}, "bindings": {}, "predicates": {}},
    )
    assert [str(v) for v in vocabulary_violations(graph)] == [
        "nodes.a.outcomes.stalled: outcome 'stalled' is not declared in vocabulary.outcomes",
        "nodes.a.skip[0].when: predicate 'never' is not declared in vocabulary.predicates",
    ]
