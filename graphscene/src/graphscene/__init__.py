"""GraphScene, a generic flow-graph navigation library.

It exposes loading a declared flow graph into its typed model (`load_graph`, `load_graph_file`,
`FlowGraph` and the objects it holds), and `GraphError`, the error every rejection raises.

The boundary: this package imports only the standard library, itself and its declared runtime
dependencies, and it never reads the harness's configuration file. Harness integration lives in a
separate distribution that depends on this one, never the reverse (`tests/test_boundary.py`).
"""

from graphscene.errors import GraphError, Stage, Violation
from graphscene.loader import load_graph, load_graph_file
from graphscene.model import (
    BindingDeclaration,
    BindingEdge,
    CounterDeclaration,
    DispatchNode,
    Edge,
    EndBinding,
    FlowGraph,
    InterruptBinding,
    Node,
    NodeKind,
    OnCapEdge,
    OutcomeDeclaration,
    PredicateDeclaration,
    Primitive,
    RoundNode,
    RouteEdge,
    SkipEntry,
    StopBinding,
    TerminalNode,
    Verdict,
    Vocabulary,
)
from graphscene.vocabulary import vocabulary_violations

__all__: list[str] = [
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
