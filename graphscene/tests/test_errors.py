"""The rule this file exists to enforce: one error shape for every stage of loading a flow graph,
each violation rendered as `<path>: <reason>` (`graphscene.errors`).

One case per clause of the contract, each asserting the exact text; and one case rendering the
vocabulary check's `Violation` values back to the strings it returned before it used them.
"""

import dataclasses

import pytest

from graphscene.errors import GraphError, Violation
from graphscene.vocabulary import vocabulary_violations


def test_a_violation_renders_as_path_colon_reason() -> None:
    assert str(Violation("nodes.draft.agent", "x")) == "nodes.draft.agent: x"


def test_a_violation_at_the_root_renders_its_path_as_root() -> None:
    assert str(Violation("", "x")) == "(root): x"


def test_a_violation_is_frozen() -> None:
    violation = Violation("nodes.draft.agent", "x")
    with pytest.raises(dataclasses.FrozenInstanceError):
        violation.path = "nodes.other"  # type: ignore[misc]


def test_a_graph_error_carries_its_stage_and_violations_and_renders_them() -> None:
    first = Violation("nodes.a", "first reason")
    second = Violation("", "second reason")
    error = GraphError("schema", [first, second])
    assert error.stage == "schema"
    assert error.violations == (first, second)
    assert isinstance(error.violations, tuple)
    assert str(error) == (
        "flow graph failed the schema check:\nnodes.a: first reason\n(root): second reason"
    )


def test_a_graph_error_is_a_value_error() -> None:
    assert isinstance(GraphError("parse", [Violation("", "x")]), ValueError)


def test_a_graph_error_without_violations_is_refused() -> None:
    with pytest.raises(ValueError) as raised:
        GraphError("vocabulary", [])
    assert str(raised.value) == "a GraphError carries at least one violation"


def test_vocabulary_violations_render_to_the_strings_the_check_returned_before() -> None:
    graph: dict[str, object] = {
        "vocabulary": {"outcomes": {"done": {}}, "bindings": {}, "predicates": {}},
        "nodes": {
            "a": {
                "kind": "dispatch",
                "outcomes": {"stalled": {"to": "a"}},
                "skip": [{"when": "never", "to": "a"}],
            }
        },
    }
    assert [str(v) for v in vocabulary_violations(graph)] == [
        "nodes.a.outcomes.stalled: outcome 'stalled' is not declared in vocabulary.outcomes",
        "nodes.a.skip[0].when: predicate 'never' is not declared in vocabulary.predicates",
    ]
