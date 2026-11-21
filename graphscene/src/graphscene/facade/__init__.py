"""The `facade` layer: the composed public surface the package root re-exports.

The rule: this layer may import every layer below it — `graphscene.adapters`, `graphscene.engine`
and `graphscene.model` — and `__all__` holds exactly the package root's names, in its order.
"""

from graphscene.engine.vocabulary import vocabulary_violations
from graphscene.facade.loading import load_graph, load_graph_file
from graphscene.model.errors import GraphError, Stage, Violation
from graphscene.model.flow_graph import (
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
