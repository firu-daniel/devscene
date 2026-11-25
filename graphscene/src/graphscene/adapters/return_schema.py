"""The return check: `return_violations` validates an executor's structured return, JSON-shaped
data as `json.loads` returns it, against a JSON Schema the executor names, and returns every
violation.

The rule:

- The draft is the one the schema declares in `$schema`, and draft-07 when it declares none.
  The schema itself is checked first, and an invalid one raises `ValueError("return schema:
  <message>")`, so no `jsonschema` exception type crosses this boundary.
- A schema `pattern`, and every `patternProperties` key, is matched as ECMA-262 through
  `graphscene.adapters.schema`'s translator, and one outside its supported set raises that
  translator's `ValueError`, naming its schema path. Instance data under `const`, `enum`,
  `default` and `examples` is never translated.
- Violations are sorted by path then reason, with paths rendered as `schema_violations` renders
  them; `[]` for a valid document. A non-empty result is what `graphscene.model.execution` means
  by an `undelivered` return that "failed the schema the executor names".

Deliberately not covered:

- Parsing text into a document, and choosing a failure class or wording its reason: both are
  the executor's.
- Finding the schema: it is the caller's, never loaded from a repository path.
"""

from collections.abc import Mapping
from typing import Any

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

from graphscene.adapters.schema import _ecma_patterns, _render
from graphscene.model.errors import Violation


def return_violations(document: object, schema: Mapping[str, object]) -> list[Violation]:
    """Return every violation of `schema` in `document`, sorted by path then reason; `[]` for a
    valid document. Raises `ValueError` for an invalid schema or an untranslatable pattern."""
    declared = dict(schema)
    validator_class = validator_for(declared, default=Draft7Validator)
    try:
        validator_class.check_schema(declared)
    except SchemaError as error:
        raise ValueError(f"return schema: {error.message}") from None
    translated = _ecma_patterns(declared)
    assert isinstance(translated, dict)
    # The `Validator` protocol's stub narrows `instance` to JSON types; the runtime accepts any
    # object, and reports a non-JSON value only where a keyword such as `type` checks it.
    instance: Any = document
    return sorted(
        (
            Violation(_render(error.absolute_path), error.message)
            for error in validator_class(translated).iter_errors(instance)
        ),
        key=lambda violation: (violation.path, violation.reason),
    )
