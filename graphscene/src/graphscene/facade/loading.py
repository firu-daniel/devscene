"""Loading a declared flow graph: turning parsed or on-disk data into the typed `FlowGraph` model,
or into a `GraphError` whose violations name the node and the field.

The rule: a returned graph has passed the format-4 schema this package ships
(`schemas/flow-graph.schema.json`), then the vocabulary check, in that order, and is then built. A
graph failing the schema never reaches the vocabulary check.

Deliberately not checked:
- Node-id references: `to`, `resume`, `gates`, `writer`, `start`, `entries`, `roundCounts` and a
  skip's `to` may name a node that does not exist. That is a static checker's job.
- The names a graph gives its counters, paths, report slots and prompts, where they are used.
- Reachability and counter caps.
- Duplicate JSON keys, which `json.loads` collapses to the last.
"""

import os

from graphscene.adapters.builder import build_flow_graph
from graphscene.adapters.json_file import read_json_file
from graphscene.adapters.schema import schema_violations
from graphscene.engine.vocabulary import vocabulary_violations
from graphscene.model.errors import GraphError
from graphscene.model.flow_graph import FlowGraph


def load_graph(graph: object) -> FlowGraph:
    """Validate `graph`, JSON-shaped data as `json.loads` returns it, and build its typed model."""
    found = schema_violations(graph)
    if found:
        raise GraphError("schema", found)
    assert isinstance(graph, dict)
    found = vocabulary_violations(graph)
    if found:
        raise GraphError("vocabulary", found)
    return build_flow_graph(graph)


def load_graph_file(path: str | os.PathLike[str]) -> FlowGraph:
    """Read `path` as UTF-8 JSON and load it; a file that is not UTF-8 or not JSON is a parse-stage
    `GraphError`, and an `OSError` propagates unchanged."""
    return load_graph(read_json_file(path))
