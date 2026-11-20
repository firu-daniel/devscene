"""Loading a declared flow graph: turning parsed or on-disk data into the typed `FlowGraph` model,
or into a `GraphError` whose violations name the node and the field.

The rule: a returned graph has passed the format-4 schema this package ships
(`schemas/flow-graph.schema.json`), then the vocabulary check, in that order. A graph failing the
schema never reaches the vocabulary check.

A schema `pattern` is matched as ECMA-262, as `ajv` matches it: its `$` only at the very end of
the string, never before a trailing newline, and its `.` against no line terminator.

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

_ECMA_DOT = "[^\\n\\r\\u2028\\u2029]"


def _ecma_pattern(pattern: str) -> str:
    """Rewrite `pattern` so Python's `re` reads it as ECMA-262 does: an unescaped `$` outside a
    character class matches only at the very end, and an unescaped `.` outside one matches no
    line terminator."""
    out: list[str] = []
    in_class = False
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "\\":
            out.append(pattern[index : index + 2])
            index += 2
            continue
        if in_class:
            in_class = char != "]"
            out.append(char)
        elif char == "[":
            in_class = True
            out.append(char)
        elif char == "$":
            out.append("\\Z")
        elif char == ".":
            out.append(_ECMA_DOT)
        else:
            out.append(char)
        index += 1
    return "".join(out)


def _ecma_patterns(node: object) -> object:
    """Return a copy of the schema `node` with every `pattern` keyword rewritten by
    `_ecma_pattern`."""
    if isinstance(node, dict):
        return {
            key: (
                _ecma_pattern(child)
                if key == "pattern" and isinstance(child, str)
                else _ecma_patterns(child)
            )
            for key, child in node.items()
        }
    if isinstance(node, list):
        return [_ecma_patterns(child) for child in node]
    return node


@cache
def _validator() -> Draft7Validator:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    schema = _ecma_patterns(json.loads(resource.read_text(encoding="utf-8")))
    assert isinstance(schema, dict)
    return Draft7Validator(schema)


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
