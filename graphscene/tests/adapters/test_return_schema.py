"""The rule this file exists to enforce: `return_violations` checks a document against the schema
it is handed, by the draft that schema declares (draft-07 when it declares none), refuses a
declared draft it does not recognise with a `ValueError` opening `return schema: `, matches a
`pattern` as ECMA-262 through the shared translator, returns every violation sorted by path then
reason with `schema_violations`' path rendering, and turns an invalid schema into a `ValueError`
opening `return schema: `. A `$ref` resolves inside the schema only: a remote one or one pointing
at nothing is refused with that `ValueError`, and nothing is retrieved. Each schema is planted
here and every expected `Violation` is hand-written from reading it.
"""

import re

import pytest

from graphscene.adapters.return_schema import return_violations
from graphscene.model.errors import Violation

_REPORT = {
    "type": "object",
    "required": ["status"],
    "properties": {"status": {"type": "string"}},
}


def test_a_valid_document_has_no_violation() -> None:
    assert return_violations({"status": "done"}, _REPORT) == []


def test_a_missing_required_key_is_reported_at_the_root() -> None:
    assert return_violations({}, _REPORT) == [Violation("", "'status' is a required property")]


def test_violations_are_sorted_by_path() -> None:
    schema = {
        "type": "object",
        "properties": {"b": {"type": "string"}, "a": {"type": "integer"}},
    }
    assert return_violations({"b": 1, "a": "x"}, schema) == [
        Violation("a", "'x' is not of type 'integer'"),
        Violation("b", "1 is not of type 'string'"),
    ]


def test_a_nested_array_item_path_renders_its_index() -> None:
    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "object", "properties": {"name": {"type": "string"}}},
            }
        },
    }
    document = {"items": [{"name": "x"}, {"name": 3}]}
    assert return_violations(document, schema) == [
        Violation("items[1].name", "3 is not of type 'string'")
    ]


def test_an_invalid_schema_raises_a_value_error() -> None:
    with pytest.raises(ValueError, match="^return schema: "):
        return_violations({}, {"type": 5})


def test_a_dollar_matches_only_at_the_very_end() -> None:
    schema = {"type": "string", "pattern": "^a$"}
    assert return_violations("a", schema) == []
    assert return_violations("a\n", schema) == [Violation("", "'a\\n' does not match '^a\\\\Z'")]


def test_an_untranslated_pattern_construct_is_refused() -> None:
    message = (
        "pattern: schema pattern '^\\\\d$' uses '\\\\d', "
        "which _ecma_pattern does not translate to ECMA-262"
    )
    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        return_violations("1", {"type": "string", "pattern": "^\\d$"})


def test_a_pattern_properties_dollar_matches_only_at_the_very_end() -> None:
    schema = {"type": "object", "patternProperties": {"^a$": {"type": "integer"}}}
    assert return_violations({"a\n": "x"}, schema) == []


def test_a_document_equal_to_a_const_carrying_pattern_is_valid() -> None:
    assert return_violations({"pattern": "a.b"}, {"const": {"pattern": "a.b"}}) == []


def test_a_declared_draft_2020_12_is_the_draft_applied() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "array",
        "prefixItems": [{"type": "string"}],
    }
    assert return_violations([5], schema) == [Violation("[0]", "5 is not of type 'string'")]


def test_an_unrecognised_declared_draft_is_refused() -> None:
    schema = {"$schema": "https://example.invalid/schema", "type": "array"}
    with pytest.raises(ValueError) as raised:
        return_violations([5], schema)
    assert str(raised.value) == (
        "return schema: $schema 'https://example.invalid/schema' names no draft jsonschema knows"
    )


def test_a_declared_draft_07_is_accepted() -> None:
    schema = {"$schema": "http://json-schema.org/draft-07/schema#", "type": "string"}
    assert return_violations(5, schema) == [Violation("", "5 is not of type 'string'")]


def test_a_local_ref_resolves_inside_the_schema() -> None:
    schema = {
        "definitions": {"word": {"type": "string"}},
        "properties": {"status": {"$ref": "#/definitions/word"}},
    }
    assert return_violations({"status": 1}, schema) == [
        Violation("status", "1 is not of type 'string'")
    ]


def test_a_ref_pointing_at_nothing_is_refused() -> None:
    schema = {"properties": {"status": {"$ref": "#/definitions/missing"}}}
    with pytest.raises(ValueError, match=r"^return schema: .*/definitions/missing"):
        return_violations({"status": "done"}, schema)


def test_a_remote_ref_is_refused_without_retrieving_it() -> None:
    # example.invalid is a reserved name that never resolves, so a retrieval attempt would fail
    # with a network error rather than this ValueError.
    schema = {"properties": {"status": {"$ref": "https://example.invalid/status.json"}}}
    with pytest.raises(
        ValueError, match=r"^return schema: .*https://example\.invalid/status\.json"
    ):
        return_violations({"status": "done"}, schema)
