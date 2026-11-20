"""The rule this file exists to enforce: the loader (`graphscene.loader`) rejects every fixture
`ajv` rejects, at the schema stage, and every vocabulary negative, at the vocabulary stage; each
rejection names the node and the field where the fixture's one change sits; and
`valid_generic.json` loads.

Each expected path is hand-read from the fixture's one change against `valid_generic.json`, never
taken from the loader's output.
"""

import copy
import json
from importlib.resources import files
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

from graphscene.errors import GraphError, Violation
from graphscene.loader import load_graph, load_graph_file
from graphscene.model import FlowGraph

_FIXTURES = Path(__file__).parent / "fixtures" / "flow_graph"

_SCHEMA_NEGATIVES: list[tuple[str, str]] = [
    ("schema_negative_format_version_3.json", "formatVersion"),
    ("schema_negative_no_vocabulary.json", ""),
    ("schema_negative_unknown_primitive.json", "vocabulary.bindings.<finish>.primitive"),
    ("schema_negative_interrupt_without_resume_outcome.json", "vocabulary.bindings.<pause>"),
    ("schema_negative_outcome_verdict_and_held.json", "vocabulary.outcomes.approved"),
    ("schema_negative_skip_construct.json", "nodes.edit_check.skip[0]"),
    ("schema_negative_round_three_outcomes.json", "nodes.review_round.outcomes"),
]

_VOCABULARY_NEGATIVES: list[tuple[str, str]] = [
    ("vocabulary_negative_unknown_outcome.json", "nodes.draft.outcomes.finished"),
    ("vocabulary_negative_unknown_binding.json", "nodes.draft.outcomes.crashed.binding"),
    ("vocabulary_negative_interrupt_without_resume.json", "nodes.draft.outcomes.crashed"),
    ("vocabulary_negative_undeclared_reason.json", "nodes.draft.outcomes.crashed.reason"),
    ("vocabulary_negative_round_without_fail_verdict.json", "nodes.review_round.outcomes"),
    ("vocabulary_negative_end_on_an_edge.json", "nodes.draft.outcomes.crashed.binding"),
    ("vocabulary_negative_unknown_predicate.json", "nodes.edit_check.skip[0].when"),
]


def _parsed(name: str) -> dict[str, object]:
    loaded = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _node(graph: dict[str, object], node_id: str) -> dict[str, object]:
    nodes = graph["nodes"]
    assert isinstance(nodes, dict)
    node = nodes[node_id]
    assert isinstance(node, dict)
    return node


@pytest.mark.parametrize(("name", "path"), _SCHEMA_NEGATIVES)
def test_a_schema_negative_is_rejected_at_the_schema_stage(name: str, path: str) -> None:
    with pytest.raises(GraphError) as raised:
        load_graph(_parsed(name))
    assert raised.value.stage == "schema"
    assert path in [violation.path for violation in raised.value.violations]


@pytest.mark.parametrize(("name", "path"), _VOCABULARY_NEGATIVES)
def test_a_vocabulary_negative_is_rejected_at_the_vocabulary_stage(name: str, path: str) -> None:
    with pytest.raises(GraphError) as raised:
        load_graph(_parsed(name))
    assert raised.value.stage == "vocabulary"
    assert [violation.path for violation in raised.value.violations] == [path]


def test_the_valid_generic_graph_loads() -> None:
    loaded = load_graph(_parsed("valid_generic.json"))
    assert isinstance(loaded, FlowGraph)
    assert loaded.flow == "article_review"


def test_a_non_object_graph_is_rejected_at_the_root() -> None:
    with pytest.raises(GraphError) as raised:
        load_graph([])
    assert raised.value.stage == "schema"
    assert [violation.path for violation in raised.value.violations] == [""]


def test_a_missing_required_field_names_the_node() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    del _node(graph, "draft")["agent"]
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert raised.value.violations == (Violation("nodes.draft", "'agent' is a required property"),)


def test_schema_violations_come_back_sorted_by_path() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    del _node(graph, "edit_check")["agent"]
    del _node(graph, "draft")["agent"]
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert raised.value.violations == (
        Violation("nodes.draft", "'agent' is a required property"),
        Violation("nodes.edit_check", "'agent' is a required property"),
    )


def test_a_schema_failure_never_reaches_the_vocabulary_stage() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    del _node(graph, "draft")["agent"]
    outcomes = _node(graph, "edit_check")["outcomes"]
    assert isinstance(outcomes, dict)
    outcomes["finished"] = {"to": "review_round"}
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert raised.value.violations == (Violation("nodes.draft", "'agent' is a required property"),)


def test_loading_a_file_equals_loading_its_parsed_data() -> None:
    path = _FIXTURES / "valid_generic.json"
    assert load_graph_file(path) == load_graph(_parsed("valid_generic.json"))


def test_a_file_that_is_not_json_is_rejected_at_the_parse_stage(tmp_path: Path) -> None:
    path = tmp_path / "graph.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(GraphError) as raised:
        load_graph_file(path)
    assert raised.value.stage == "parse"
    assert raised.value.violations == (
        Violation(
            "",
            "not valid JSON: Expecting property name enclosed in double quotes (line 1, column 2)",
        ),
    )


def test_a_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_graph_file(tmp_path / "absent.json")


def test_the_shipped_schema_is_a_valid_draft_7_schema() -> None:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    Draft7Validator.check_schema(json.loads(resource.read_text(encoding="utf-8")))
