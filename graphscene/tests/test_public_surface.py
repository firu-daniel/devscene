"""The rule this file exists to enforce: the package root exposes exactly the graph-model surface,
and each name it exposes is the object its own module defines.

`__all__` is compared as a list, so adding, removing or reordering a name is a reviewed change.
"""

import pytest

import graphscene
import graphscene.errors
import graphscene.loader
import graphscene.model
import graphscene.vocabulary

_EXPECTED: list[str] = [
    "load_graph",
    "load_graph_file",
    "GraphError",
    "Stage",
    "Violation",
    "vocabulary_violations",
    "FlowGraph",
    "NodeKind",
    "Primitive",
    "Verdict",
    "BindingDeclaration",
    "Edge",
    "Node",
    "OutcomeDeclaration",
    "InterruptBinding",
    "StopBinding",
    "EndBinding",
    "PredicateDeclaration",
    "Vocabulary",
    "CounterDeclaration",
    "OnCapEdge",
    "RouteEdge",
    "BindingEdge",
    "SkipEntry",
    "DispatchNode",
    "RoundNode",
    "TerminalNode",
]

_DEFINED_IN: dict[str, object] = {
    "load_graph": graphscene.loader,
    "load_graph_file": graphscene.loader,
    "GraphError": graphscene.errors,
    "Stage": graphscene.errors,
    "Violation": graphscene.errors,
    "vocabulary_violations": graphscene.vocabulary,
    **{name: graphscene.model for name in _EXPECTED[6:]},
}


def test_the_public_surface_is_exactly_the_graph_model() -> None:
    assert graphscene.__all__ == _EXPECTED


@pytest.mark.parametrize("name", _EXPECTED)
def test_each_public_name_is_the_object_its_module_defines(name: str) -> None:
    assert getattr(graphscene, name) is getattr(_DEFINED_IN[name], name)


def test_the_unvalidated_builder_is_not_exported() -> None:
    assert "build_flow_graph" not in graphscene.__all__


def test_the_named_examples_resolve_to_their_modules() -> None:
    assert graphscene.load_graph is graphscene.loader.load_graph
    assert graphscene.Violation is graphscene.errors.Violation
