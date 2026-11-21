"""The rule this file exists to enforce: loading (`graphscene.facade.loading`) rejects every
fixture `ajv` rejects, at the schema stage, and every vocabulary negative, at the vocabulary
stage; each rejection names the node and the field where the fixture's one change sits;
`valid_generic.json` loads; a number the schema accepts as an integer, written `3.0`, loads as
an `int`; a schema `pattern` is matched as ECMA-262 matches it, so a trailing newline or a `.`
against a line terminator is rejected; and a file that is not UTF-8 or not JSON is rejected at the
parse stage.

Each expected path is hand-read from the fixture's one change against `valid_generic.json`, never
taken from the loader's output. The public names are imported from `graphscene`, as a caller
imports them.
"""

import copy
import json
from pathlib import Path

import pytest

from graphscene import FlowGraph, GraphError, RoundNode, Violation, load_graph, load_graph_file

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"

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


def test_an_integral_float_where_the_schema_takes_an_integer_loads_as_an_int() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    counters = graph["counters"]
    assert isinstance(counters, dict)
    counters["attempt"]["cap"] = 3.0
    _node(graph, "review_round")["convergingFrom"] = 1.0
    loaded = load_graph(graph)
    assert type(loaded.counters["attempt"].cap) is int
    assert loaded.counters["attempt"].cap == 3
    review_round = loaded.nodes["review_round"]
    assert isinstance(review_round, RoundNode)
    assert type(review_round.converging_from) is int
    assert review_round.converging_from == 1


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


def test_a_trailing_newline_does_not_satisfy_an_anchored_pattern() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    graph["flow"] = "article_review\n"
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert [violation.path for violation in raised.value.violations] == ["flow"]


def test_a_pattern_dot_does_not_match_a_line_terminator() -> None:
    graph = copy.deepcopy(_parsed("valid_generic.json"))
    _node(graph, "draft")["findingsFolder"] = "{state_dir}/a\rb/"
    with pytest.raises(GraphError) as raised:
        load_graph(graph)
    assert raised.value.stage == "schema"
    assert [violation.path for violation in raised.value.violations] == [
        "nodes.draft.findingsFolder"
    ]


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


def test_a_file_that_is_not_utf_8_is_rejected_at_the_parse_stage(tmp_path: Path) -> None:
    path = tmp_path / "graph.json"
    path.write_bytes(b'{"flow": "\xe9"}')
    with pytest.raises(GraphError) as raised:
        load_graph_file(path)
    assert raised.value.stage == "parse"
    assert raised.value.violations == (
        Violation("", "not valid UTF-8: invalid continuation byte (byte 10)"),
    )


def test_a_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_graph_file(tmp_path / "absent.json")
