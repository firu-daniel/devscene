"""The rule this file exists to enforce: every return-document field the planning driver reads —
each `(node, field)` pair in `devscene_flow_host.host.run_exits` → `RETURN_FIELD_READS` — is
declared under `properties` by some `oneOf` variant of the return schema of that node's agent,
`plugin/schemas/<agent>.return.json`, the agent taken from the real planning graph
`cli/templates/scripts/flows/task_plan_writing.graph.json`. It replaces the retired
`agent-return-schemas.test.mjs` check that every `pd_ret_field` call named a declared field.

The pairs are imported from `run_exits`, never listed here, so a field the driver starts reading
is checked without editing this file. The graph and the two schemas are read only; the planted
cases write only under `tmp_path`.

Deliberately not covered:
- The type a schema gives the field, or whether the variant declaring it is the one the driver
  reads it under: the check is that the field is declared at all, as the retired one was.
- Fields the walk's other readers take from a return document: only `run_exits` lists its reads.
"""

import json
from pathlib import Path
from typing import Final

import pytest
from graphscene import DispatchNode, load_graph_file

from devscene_flow_host.host import run_exits

_CHECKOUT: Final = Path(__file__).resolve().parents[2]
_GRAPH: Final = (
    _CHECKOUT / "cli" / "templates" / "scripts" / "flows" / "task_plan_writing.graph.json"
)
_SCHEMAS: Final = _CHECKOUT / "plugin" / "schemas"
_READS: Final = run_exits.RETURN_FIELD_READS


def _violation(schema_file: Path, node: str, agent: str, field: str) -> str | None:
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    for variant in schema.get("oneOf", []):
        if field in variant.get("properties", {}):
            return None
    return (
        f"node {node!r} reads return field {field!r}, "
        f"which no oneOf variant of the return schema of agent {agent!r} declares"
    )


def _agent(node: str) -> str:
    graph_node = load_graph_file(_GRAPH).nodes[node]
    assert isinstance(graph_node, DispatchNode), f"node {node!r} is not a dispatch node"
    return graph_node.agent


def test_the_driver_reads_at_least_one_return_field() -> None:
    assert _READS


def test_every_questions_read_is_from_a_question_node() -> None:
    for node, field in _READS:
        if field == run_exits.QUESTIONS_FIELD:
            assert node in run_exits.QUESTION_NODES, node


@pytest.mark.parametrize(("node", "field"), _READS)
def test_every_field_the_driver_reads_is_declared_by_its_agents_schema(
    node: str, field: str
) -> None:
    agent = _agent(node)
    violation = _violation(_SCHEMAS / f"{agent}.return.json", node, agent, field)
    assert violation is None, violation


def test_a_planted_schema_declaring_the_field_passes(tmp_path: Path) -> None:
    schema = tmp_path / "planted.return.json"
    schema.write_text(
        '{"oneOf": [{"properties": {"outcome": {}}}, {"properties": {"tasks_count": {}}}]}',
        encoding="utf-8",
    )
    assert _violation(schema, "plan_writer", "planted", "tasks_count") is None


def test_a_planted_schema_lacking_the_field_fails_naming_node_agent_and_field(
    tmp_path: Path,
) -> None:
    schema = tmp_path / "planted.return.json"
    schema.write_text(
        '{"oneOf": [{"properties": {"outcome": {}}}, {"properties": {"tasks": {}}}]}',
        encoding="utf-8",
    )
    assert _violation(schema, "plan_writer", "planted", "tasks_count") == (
        "node 'plan_writer' reads return field 'tasks_count', "
        "which no oneOf variant of the return schema of agent 'planted' declares"
    )
