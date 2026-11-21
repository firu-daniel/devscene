"""The rule this file exists to enforce: the format-4 flow-graph schema ships as `graphscene`
package data and names no harness vocabulary.

The schema is read through `importlib.resources`, as a consumer of the installed package reads it.
`harness_names` walks every string value in a parsed schema and returns each one that equals a
harness outcome, binding, phase or reason name, or contains the forbidden prefix.

Deliberately not covered:
- Schema validation itself: it runs in `tests/test_loader.py` through `graphscene.loader`, and
  through `ajv` from the repository root. This file only checks that each fixture parses.
- Key-name positions — the members of every `required` and `dependencies` array, and every
  `properties` key — are not walked for harness names, because they name the format's own keys,
  and a counter's `cap` is one of them.
"""

import json
from importlib.resources import files
from pathlib import Path

_FIXTURES = Path(__file__).parent / "fixtures" / "flow_graph"

_FIXTURE_NAMES = [
    "valid_generic.json",
    "schema_negative_format_version_3.json",
    "schema_negative_no_vocabulary.json",
    "schema_negative_unknown_primitive.json",
    "schema_negative_interrupt_without_resume_outcome.json",
    "schema_negative_outcome_verdict_and_held.json",
    "schema_negative_skip_construct.json",
    "schema_negative_round_three_outcomes.json",
]

_HARNESS_NAMES = frozenset(
    {
        "PASS",
        "FAIL",
        "returned",
        "questions",
        "no_ui",
        "error",
        "blocker",
        "<ask>",
        "<escalate>",
        "<terminal_handoff>",
        "parity",
        "qa",
        "docs",
        "cap",
        "skipped",
        "passedByExclusion",
    }
)
_FORBIDDEN_SUBSTRING = "devscene"

_KEY_NAME_ARRAYS = frozenset({"required"})


def _load_schema() -> object:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    loaded: object = json.loads(resource.read_text(encoding="utf-8"))
    return loaded


def harness_names(schema: object) -> list[str]:
    found: list[str] = []

    def walk(value: object) -> None:
        if isinstance(value, str):
            if value in _HARNESS_NAMES or _FORBIDDEN_SUBSTRING in value:
                found.append(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for key, child in value.items():
                if key in _KEY_NAME_ARRAYS:
                    continue
                if key == "properties" and isinstance(child, dict):
                    for member in child.values():
                        walk(member)
                elif key == "dependencies" and isinstance(child, dict):
                    for member in child.values():
                        if not isinstance(member, list):
                            walk(member)
                else:
                    walk(child)

    walk(schema)
    return found


def test_the_schema_parses_as_format_4() -> None:
    schema = _load_schema()
    assert isinstance(schema, dict)
    properties = schema["properties"]
    assert isinstance(properties, dict)
    format_version = properties["formatVersion"]
    assert isinstance(format_version, dict)
    assert format_version["const"] == 4


def test_node_kinds_stay_a_closed_engine_enum() -> None:
    schema = _load_schema()
    assert isinstance(schema, dict)
    node = schema["definitions"]["node"]
    assert node["properties"]["kind"]["enum"] == ["dispatch", "round", "terminal"]


def test_the_schema_names_no_harness_vocabulary() -> None:
    assert harness_names(_load_schema()) == []


def test_a_planted_harness_enum_member_is_named() -> None:
    assert harness_names({"properties": {"x": {"enum": ["PASS"]}}}) == ["PASS"]


def test_a_planted_harness_const_is_named() -> None:
    assert harness_names({"definitions": {"reason": {"const": "cap"}}}) == ["cap"]


def test_a_planted_forbidden_substring_is_named() -> None:
    planted = {"description": "read from devscene.config.json"}
    assert harness_names(planted) == ["read from devscene.config.json"]


def test_a_key_name_position_is_not_walked() -> None:
    assert harness_names({"required": ["cap"]}) == []
    planted = {
        "required": ["cap"],
        "properties": {"cap": {"type": "integer"}},
        "dependencies": {"cap": ["error"]},
    }
    assert harness_names(planted) == []


def test_every_fixture_parses_as_json() -> None:
    for name in _FIXTURE_NAMES:
        parsed: object = json.loads((_FIXTURES / name).read_text(encoding="utf-8"))
        assert isinstance(parsed, dict), name
