### 1. The pattern translator `return_violations` reuses ignores keyword position: `patternProperties` keys pass through untranslated, and data under `const` / `enum` / `default` / `examples` gets rewritten

**File:** `graphscene/src/graphscene/adapters/schema.py` (`_ecma_patterns`) — "if key == \"pattern\" and isinstance(child, str)"
**Class:** Broken contract
**Failure:** If an executor calls `return_violations({"a\n": "x"}, {"type": "object", "patternProperties": {"^a$": {"type": "integer"}}})`, then it gets `[Violation("a\n", "'x' is not of type 'integer'")]`, a violation that an ECMA-262 reading of `^a$` does not produce. And if it calls `return_violations({"pattern": "a.b"}, {"const": {"pattern": "a.b"}})`, then it gets a violation for a document that equals the schema's `const`.

**Why this is a finding.** `return_violations` (`graphscene/src/graphscene/adapters/return_schema.py`) hands every executor-named schema to `_ecma_patterns`. Before this branch, `_ecma_patterns` only ever saw the shipped flow-graph schema, which has no `patternProperties` and no `pattern` key inside data. The branch made it reachable for any schema. `_ecma_patterns` rewrites every dict key spelled `pattern` that holds a string, and recurses everywhere else without regard to keyword position. That produces two defects.

1. **`patternProperties` keys are regexes, and they are neither translated nor refused.** `jsonschema` matches them with Python `re.search`. So `$` matches before a trailing newline, `.` matches the line terminators ECMA-262 excludes, and an unsupported construct such as `\d` is silently accepted. This is the escape the lessons ledger forbids: `harness-runs/lessons.md` → `## Ports and parallel implementations`, *"A shim that makes one engine read a shared contract as another engine does lists the constructs it supports and refuses every other one, naming where it occurs. It never passes an unhandled construct through untranslated."* (taught by `feat_graphscene_graph_model`). The story plan's scope register row 20 says Task 2 honours that rule by reusing `_ecma_patterns`. For `patternProperties` it does not.
2. **Data keywords are rewritten as if they were schemas.** A `pattern` key inside `const`, `enum`, `default` or `examples` holds instance data, not a regex. It gets rewritten (`a.b` becomes `a[^\n\r  ]b`), so a document equal to the declared `const` is reported as a violation. Or it gets refused: `{"enum": [{"pattern": "\\d"}]}` raises the translator's `ValueError`.

**Evidence (probe run).** `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_probe.py`, run against this branch's tree with jsonschema 4.26.0, printed:
- `patternProperties {"^a$": …}` with document `{"a\n": "x"}` gave `[Violation(path='a\n', reason="'x' is not of type 'integer'")]`. The key matched.
- `patternProperties {"^\\d+$": …}` with document `{"1": "x"}` gave `[Violation(path='1', …)]`. `\d` was used with no refusal.
- `{"const": {"pattern": "a.b"}}` with document `{"pattern": "a.b"}` gave `[Violation(path='', reason="{'pattern': 'a[^\\\\n\\\\r\\\\u2028\\\\u2029]b'} was expected")]`.
- `{"enum": [{"pattern": "\\d"}]}` raised `ValueError: enum[0].pattern: schema pattern '\\d' uses '\\d', which _ecma_pattern does not translate to ECMA-262`.

**Fix.** Make `_ecma_patterns` walk by keyword position. Replace its body in `graphscene/src/graphscene/adapters/schema.py` with the version below, and add the two constants above it:

```python
# Keywords whose value is instance data, never a schema: copied unchanged.
_DATA_KEYWORDS = frozenset({"const", "enum", "default", "examples"})
# Keywords whose value maps a name (not a keyword) to a subschema.
_NAMED_SUBSCHEMAS = frozenset(
    {"properties", "definitions", "$defs", "dependentSchemas", "dependencies"}
)


def _ecma_patterns(node: object, path: tuple[str | int, ...] = ()) -> object:
    """Return a copy of the schema `node`, found at `path`, with every `pattern` keyword and every
    `patternProperties` key rewritten by `_ecma_pattern`; instance data under `const`, `enum`,
    `default` and `examples` is copied unchanged."""
    if isinstance(node, list):
        return [_ecma_patterns(child, path + (index,)) for index, child in enumerate(node)]
    if not isinstance(node, dict):
        return node
    copied: dict[object, object] = {}
    for key, child in node.items():
        here = path + (key,)
        if key in _DATA_KEYWORDS:
            copied[key] = child
        elif key == "pattern" and isinstance(child, str):
            copied[key] = _ecma_pattern(child, here)
        elif key == "patternProperties" and isinstance(child, dict):
            copied[key] = {
                _ecma_pattern(name, here + (name,)): _ecma_patterns(sub, here + (name,))
                for name, sub in child.items()
            }
        elif key in _NAMED_SUBSCHEMAS and isinstance(child, dict):
            copied[key] = {name: _ecma_patterns(sub, here + (name,)) for name, sub in child.items()}
        else:
            copied[key] = _ecma_patterns(child, here)
    return copied
```

Under a named-subschema map, each name is treated as a property or definition name, never as a keyword. So the existing case `test_a_property_named_pattern_is_recursed_as_a_subschema` (`{"properties": {"pattern": {"pattern": "\\d"}}}`) still refuses at `properties.pattern.pattern`, and a property named `const` is still recursed as a schema. The shipped schema has no `patternProperties` and no `pattern` under a data keyword, so `test_every_shipped_schema_pattern_is_translatable` and `test_supported_constructs_translate_unchanged_but_for_dollar_and_dot` are unaffected.

Then:

- In `graphscene/src/graphscene/adapters/return_schema.py`, change the module docstring's second `The rule:` bullet to read: *"A schema `pattern`, and every `patternProperties` key, is matched as ECMA-262 through `graphscene.adapters.schema`'s translator, and one outside its supported set raises that translator's `ValueError`, naming its schema path. Instance data under `const`, `enum`, `default` and `examples` is never translated."*
- In `graphscene/tests/adapters/test_schema.py`, add three cases, each with its expected value hand-written:
  - `_ecma_patterns({"patternProperties": {"^a$": {"type": "integer"}}}) == {"patternProperties": {"^a\\Z": {"type": "integer"}}}`
  - `_ecma_patterns({"patternProperties": {"^\\d$": {}}})` raises `ValueError` with exactly `_refusal("patternProperties.^\\d$", "^\\d$", "\\d")`
  - `_ecma_patterns({"const": {"pattern": "a.b"}, "enum": [{"pattern": "\\d"}]}) == {"const": {"pattern": "a.b"}, "enum": [{"pattern": "\\d"}]}`

  Also extend the module docstring's rule sentence to cover `patternProperties` keys and the data keywords.
- In `graphscene/tests/adapters/test_return_schema.py`, add two cases:
  - `return_violations({"a\n": "x"}, {"type": "object", "patternProperties": {"^a$": {"type": "integer"}}}) == []`
  - `return_violations({"pattern": "a.b"}, {"const": {"pattern": "a.b"}}) == []`

The two test files above are the ones this fix edits, so they are the only test files the fix runs.
