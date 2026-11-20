"""Loading a declared flow graph: turning parsed or on-disk data into the typed `FlowGraph` model,
or into a `GraphError` whose violations name the node and the field.

The rule: a returned graph has passed the format-4 schema this package ships
(`schemas/flow-graph.schema.json`), then the vocabulary check, in that order. A graph failing the
schema never reaches the vocabulary check.

Deliberately not checked:
- Node-id references: `to`, `resume`, `gates`, `writer`, `start`, `entries`, `roundCounts` and a
  skip's `to` may name a node that does not exist. That is a static checker's job.
- The names a graph gives its counters, paths, report slots and prompts, where they are used.
- Reachability and counter caps.
- Duplicate JSON keys, which `json.loads` collapses to the last.
"""

import json
import os
from collections.abc import Iterable
from functools import cache
from importlib.resources import files

from jsonschema import Draft7Validator

from graphscene.errors import GraphError, Violation
from graphscene.model import FlowGraph, build_flow_graph
from graphscene.vocabulary import vocabulary_violations


@cache
def _validator() -> Draft7Validator:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    return Draft7Validator(json.loads(resource.read_text(encoding="utf-8")))


def _render(path: Iterable[str | int]) -> str:
    rendered = ""
    for part in path:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered = f"{rendered}.{part}" if rendered else part
    return rendered


def load_graph(graph: object) -> FlowGraph:
    """Validate `graph`, JSON-shaped data as `json.loads` returns it, and build its typed model."""
    schema_violations = sorted(
        (
            Violation(_render(error.absolute_path), error.message)
            for error in _validator().iter_errors(graph)
        ),
        key=lambda violation: (violation.path, violation.reason),
    )
    if schema_violations:
        raise GraphError("schema", schema_violations)
    assert isinstance(graph, dict)
    found = vocabulary_violations(graph)
    if found:
        raise GraphError("vocabulary", found)
    return build_flow_graph(graph)


def load_graph_file(path: str | os.PathLike[str]) -> FlowGraph:
    """Read `path` as UTF-8 JSON and load it; a file that is not UTF-8 or not JSON is a parse-stage
    `GraphError`, and an `OSError` propagates unchanged."""
    with open(path, "rb") as handle:
        data = handle.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        reason = f"not valid UTF-8: {error.reason} (byte {error.start})"
        raise GraphError("parse", [Violation("", reason)]) from error
    try:
        parsed: object = json.loads(text)
    except json.JSONDecodeError as error:
        reason = f"not valid JSON: {error.msg} (line {error.lineno}, column {error.colno})"
        raise GraphError("parse", [Violation("", reason)]) from error
    return load_graph(parsed)
