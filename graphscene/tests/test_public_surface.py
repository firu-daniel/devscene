"""The rule this file exists to enforce: the package root exposes exactly the graph-model and
checker surface, and each name it exposes is the object its own module defines.

`__all__` is compared as a list, so adding, removing or reordering a name is a reviewed change.
"""

import pytest

import graphscene
import graphscene.engine.static_check
import graphscene.engine.vocabulary
import graphscene.facade
import graphscene.facade.loading
import graphscene.model.errors
import graphscene.model.flow_graph

_EXPECTED: list[str] = [
    "load_graph",
    "load_graph_file",
    "GraphError",
    "Stage",
    "Violation",
    "vocabulary_violations",
    "static_violations",
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
    "load_graph": graphscene.facade.loading,
    "load_graph_file": graphscene.facade.loading,
    "GraphError": graphscene.model.errors,
    "Stage": graphscene.model.errors,
    "Violation": graphscene.model.errors,
    "vocabulary_violations": graphscene.engine.vocabulary,
    "static_violations": graphscene.engine.static_check,
    **{name: graphscene.model.flow_graph for name in _EXPECTED[7:]},
}


def test_the_public_surface_is_exactly_the_graph_model() -> None:
    assert graphscene.__all__ == _EXPECTED


@pytest.mark.parametrize("name", _EXPECTED)
def test_each_public_name_is_the_object_its_module_defines(name: str) -> None:
    assert getattr(graphscene, name) is getattr(_DEFINED_IN[name], name)


def test_the_unvalidated_builder_is_not_exported() -> None:
    assert "build_flow_graph" not in graphscene.__all__


def test_the_named_examples_resolve_to_their_modules() -> None:
    assert graphscene.load_graph is graphscene.facade.loading.load_graph
    assert graphscene.Violation is graphscene.model.errors.Violation


def test_the_facade_exposes_exactly_the_root_surface() -> None:
    assert graphscene.facade.__all__ == graphscene.__all__
