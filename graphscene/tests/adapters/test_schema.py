"""The rule this file exists to enforce: the shipped schema is a valid draft-7 schema, and the
ECMA-262 translator (`graphscene.adapters.schema._ecma_patterns`) translates every shipped schema
`pattern`, rewrites only `$` and `.` in the constructs it supports, and refuses a `pattern` using
a construct it does not handle, naming its schema path.
"""

import json
from importlib.resources import files

import pytest
from jsonschema import Draft7Validator

from graphscene.adapters.schema import _ecma_patterns


def test_the_shipped_schema_is_a_valid_draft_7_schema() -> None:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    Draft7Validator.check_schema(json.loads(resource.read_text(encoding="utf-8")))


def _refusal(path: str, pattern: str, construct: str) -> str:
    return (
        f"{path}: schema pattern {pattern!r} uses {construct!r}, "
        "which _ecma_pattern does not translate to ECMA-262"
    )


def test_every_shipped_schema_pattern_is_translatable() -> None:
    resource = files("graphscene") / "schemas" / "flow-graph.schema.json"
    _ecma_patterns(json.loads(resource.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    ("pattern", "construct"),
    [
        ("^\\d+$", "\\d"),
        ("^\\w+$", "\\w"),
        ("^\\s$", "\\s"),
        ("\\bx", "\\b"),
        ("^\\p{L}$", "\\p"),
        ("(?<=a)b", "(?<"),
        ("(?i)abc", "(?i"),
        ("^[[:alpha:]]$", "["),
        ("^a{x$", "{"),
        ("^a{,3}$", "{"),
        ("^a}$", "}"),
        ("^a]$", "]"),
        ("^[]a]$", "[]"),
        ("^[^]a]$", "[^]"),
        ("a\\", "\\"),
    ],
)
def test_an_untranslatable_pattern_construct_is_refused(pattern: str, construct: str) -> None:
    with pytest.raises(ValueError) as raised:
        _ecma_patterns({"definitions": {"x": {"pattern": pattern}}})
    assert str(raised.value) == _refusal("definitions.x.pattern", pattern, construct)


def test_a_refusal_names_a_nested_schema_path() -> None:
    with pytest.raises(ValueError) as raised:
        _ecma_patterns({"anyOf": [{"properties": {"name": {"pattern": "\\d"}}}]})
    assert str(raised.value) == _refusal("anyOf[0].properties.name.pattern", "\\d", "\\d")


def test_a_property_named_pattern_is_recursed_as_a_subschema() -> None:
    with pytest.raises(ValueError) as raised:
        _ecma_patterns({"properties": {"pattern": {"pattern": "\\d"}}})
    assert str(raised.value) == _refusal("properties.pattern.pattern", "\\d", "\\d")


def test_supported_constructs_translate_unchanged_but_for_dollar_and_dot() -> None:
    dot = "[^\\n\\r\\u2028\\u2029]"
    cases = {
        "^\\{state_dir\\}/.+/$": f"^\\{{state_dir\\}}/{dot}+/\\Z",
        "^[A-Za-z0-9][A-Za-z0-9.]*$": "^[A-Za-z0-9][A-Za-z0-9.]*\\Z",
        "^(?:ab|c){2,3}$": "^(?:ab|c){2,3}\\Z",
        "^[^\\]a-z]?$": "^[^\\]a-z]?\\Z",
    }
    schema = {"definitions": {str(index): {"pattern": p} for index, p in enumerate(cases)}}
    assert _ecma_patterns(schema) == {
        "definitions": {
            str(index): {"pattern": translated} for index, translated in enumerate(cases.values())
        }
    }
