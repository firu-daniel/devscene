### 1. `return_violations` silently validates a schema with an unrecognised `$schema` as draft-07, so the draft the schema declares is never applied

**File:** `graphscene/src/graphscene/adapters/return_schema.py` (`return_violations`) — "validator_class = validator_for(declared, default=Draft7Validator)"
**Class:** Wrong behaviour
**Failure:** If an executor calls `return_violations([5], {"$schema": "https://example.invalid/nope", "type": "array", "prefixItems": [{"type": "string"}]})`, then it gets `[]`. Draft-07 was applied and `prefixItems` was ignored, so a return that breaks the schema's own items rule is graded delivered rather than `undelivered`.

**Why this is a finding.** Two sources state the requirement:
- The module docstring's first `The rule:` bullet: *"The draft is the one the schema declares in `$schema`, and draft-07 when it declares none."*
- Task 2's plan (`harness-runs/task_plans/feat_graphscene_executor_interface/task_2_plan.md`): `validator_for(schema, default=Draft7Validator)` *"honours a declared `$schema` and defaults to draft-07"*.

That claim holds only for a `$schema` that jsonschema recognises. Here is jsonschema 4.26.0's `validator_for`, read through a probe with `inspect.getsource`:

```python
DefaultValidator = _LATEST_VERSION if default is _UNSET else default
if schema is True or schema is False or "$schema" not in schema:
    return DefaultValidator
if schema["$schema"] not in _META_SCHEMAS and default is _UNSET:
    warn(...)
return _META_SCHEMAS.get(schema["$schema"], DefaultValidator)
```

When `default` is passed, an unrecognised `$schema` returns that default **with no warning**. So a schema that declares a draft gets draft-07 instead. That includes a typo, a spelling jsonschema does not list (the probe shows `https://json-schema.org/draft-07/schema#` is one) and a draft newer than the installed jsonschema. Draft-07 does not know `prefixItems`, `dependentRequired`, `unevaluatedProperties` and similar keywords, so it skips them, and a non-conforming return passes. This is reachable from the public surface (`graphscene.return_violations`). The module's own contract already sends every schema problem through `ValueError("return schema: …")`, and the library never logs (`graphscene/README.md` → `## The layers`). So refusing is the only consistent outcome. The existing test `test_a_declared_draft_2020_12_is_the_draft_applied` covers only a recognised URI.

**Evidence (probe run).** `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_probe.py`, run against this branch's tree, printed:
- `unknown $schema -> [] []` for `return_violations([5], {"$schema": "https://example.invalid/nope", "type": "array", "prefixItems": [{"type": "string"}]})`. There was no violation and no warning.
- `validator_for({"$schema": "https://example.invalid/nope"}, default=None)` gave `None`, and so did `validator_for({"$schema": "https://json-schema.org/draft-07/schema#"}, default=None)`. Both are unrecognised.
- With a recognised URI, `https://json-schema.org/draft/2020-12/schema#`, the same document gave `[Violation(path='[0]', reason="5 is not of type 'string'")]`.

**Fix.**

1. In `graphscene/src/graphscene/adapters/return_schema.py`, change the import line `from jsonschema import Draft7Validator` to `from jsonschema import Draft4Validator, Draft7Validator`. Then, directly after `validator_class = validator_for(declared, default=Draft7Validator)` and before the `try:`, insert:

   ```python
       # `validator_for` returns its default, silently, for a `$schema` it does not recognise; asking
       # again with a different default tells a recognised declaration from an unrecognised one.
       if "$schema" in declared and validator_for(declared, default=Draft4Validator) is not validator_class:
           raise ValueError(
               f"return schema: $schema {declared['$schema']!r} names no draft jsonschema knows"
           )
   ```

   This check gives the right answer in each case:
   - A recognised URI returns the same class from both calls.
   - An unrecognised one returns `Draft7Validator` from the first call and `Draft4Validator` from the second.
   - A schema with no `$schema` skips the check.

   If the line is too long for `ruff`, wrap the condition in parentheses across lines. Keep the message text unchanged.

2. In the same file, replace the module docstring's first `The rule:` bullet with:
   *"The draft is the one the schema declares in `$schema`, and draft-07 when it declares none; a `$schema` that names no draft `jsonschema` knows raises `ValueError("return schema: $schema '<uri>' names no draft jsonschema knows")`. The schema itself is checked next, and an invalid one raises `ValueError("return schema: <message>")`, so no `jsonschema` exception type crosses this boundary."*

3. In `graphscene/tests/adapters/test_return_schema.py`, add two cases after `test_a_declared_draft_2020_12_is_the_draft_applied`. The expected values are hand-written:

   ```python
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
   ```

   Then extend that file's module docstring rule sentence. After *"by the draft that schema declares (draft-07 when it declares none)"*, add *", refuses a declared draft it does not recognise with a `ValueError` opening `return schema: `"*.

This test file is the one the fix edits, so it is the only test file the fix runs.
