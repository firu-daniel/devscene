"""The rule this file exists to enforce: `graphscene.adapters.check_json.check_document` encodes a
`GraphError`, or its absence, as `{"stage", "violations": [{"path", "check", "reason"}]}` in that
key order and in the error's violation order, splitting a reason into its check id and its text
only at stage `static`, and keeping `path` the library's own, `""` for the root.

Every expected document is hand-written from reading the planted `GraphError`, never taken from
the encoder's output.
"""

from graphscene.adapters.check_json import check_document
from graphscene.model.errors import GraphError, Violation


def _violations(document: dict[str, object]) -> list[dict[str, object]]:
    violations = document["violations"]
    assert isinstance(violations, list)
    return violations


def _assert_key_order(document: dict[str, object]) -> None:
    assert list(document) == ["stage", "violations"]
    for violation in _violations(document):
        assert list(violation) == ["path", "check", "reason"]


def test_a_clean_load_is_the_empty_document() -> None:
    document = check_document(None)

    assert document == {"stage": None, "violations": []}
    _assert_key_order(document)


def test_a_static_violation_is_split_into_its_check_and_reason() -> None:
    error = GraphError("static", [Violation("nodes.a.to", "node-known: 'b' is not a node")])

    document = check_document(error)

    assert document == {
        "stage": "static",
        "violations": [
            {"path": "nodes.a.to", "check": "node-known", "reason": "'b' is not a node"}
        ],
    }
    _assert_key_order(document)


def test_two_static_violations_keep_their_order_and_are_each_split() -> None:
    error = GraphError(
        "static",
        [
            Violation("nodes.z.to", "node-known: 'y' is not a node"),
            Violation("nodes.a", "reachable: 'a' is not reachable from the start node"),
        ],
    )

    document = check_document(error)

    assert document == {
        "stage": "static",
        "violations": [
            {"path": "nodes.z.to", "check": "node-known", "reason": "'y' is not a node"},
            {
                "path": "nodes.a",
                "check": "reachable",
                "reason": "'a' is not reachable from the start node",
            },
        ],
    }
    _assert_key_order(document)


def test_a_schema_violation_keeps_its_reason_verbatim() -> None:
    error = GraphError("schema", [Violation("nodes.a", "'kind' is a required property")])

    document = check_document(error)

    assert document == {
        "stage": "schema",
        "violations": [
            {"path": "nodes.a", "check": None, "reason": "'kind' is a required property"}
        ],
    }
    _assert_key_order(document)


def test_a_vocabulary_reason_containing_the_separator_is_not_split() -> None:
    error = GraphError(
        "vocabulary",
        [Violation("nodes.a.binding", "binding 'x' is not declared: declare it under bindings")],
    )

    document = check_document(error)

    assert document == {
        "stage": "vocabulary",
        "violations": [
            {
                "path": "nodes.a.binding",
                "check": None,
                "reason": "binding 'x' is not declared: declare it under bindings",
            }
        ],
    }
    _assert_key_order(document)


def test_a_parse_violation_at_the_root_keeps_the_empty_path() -> None:
    error = GraphError("parse", [Violation("", "Expecting value: line 1 column 1 (char 0)")])

    document = check_document(error)

    assert document == {
        "stage": "parse",
        "violations": [
            {"path": "", "check": None, "reason": "Expecting value: line 1 column 1 (char 0)"}
        ],
    }
    _assert_key_order(document)


def test_a_static_reason_without_the_separator_keeps_check_none() -> None:
    error = GraphError("static", [Violation("nodes.a", "built in code with no check id")])

    document = check_document(error)

    assert document == {
        "stage": "static",
        "violations": [
            {"path": "nodes.a", "check": None, "reason": "built in code with no check id"}
        ],
    }
    _assert_key_order(document)
