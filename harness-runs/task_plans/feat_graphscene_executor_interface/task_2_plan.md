### Task 2 — Add `return_violations`, checking an executor's return against a JSON Schema it names

**Goal:** Give any executor a standard way to check a structured return against a JSON Schema the executor names. An executor that gets back a non-empty list of violations returns `Failed("undelivered", …)`. The check lives in `adapters`, the only layer that may import `jsonschema` (`.claude/context/graphscene.md` → `## The internal layers`, contract `graphscene-jsonschema-in-adapters-only`).

**Depends on:** Task 1, which declares the result this check feeds: `Failed(failure: FailureClass, reason: str)` with `FailureClass = Literal["infra", "agent", "undelivered"]`, in `graphscene/src/graphscene/model/execution.py`. A return failing its named schema is `undelivered` by Task 1's definition. This module returns violations and builds no `Failed`. Choosing the class and wording the `reason` is the executor's job.

**Where this task stops.** It adds no runtime dependency and changes no existing behaviour of `schema_violations`. Exporting `return_violations` from `graphscene` and its README row are **Task 4's**.

### Targets

- `graphscene/src/graphscene/adapters/return_schema.py` (new): `return_violations`.
- `graphscene/tests/adapters/test_return_schema.py` (new): this module's own suite.

**The contract this task defines.** Task 4 exports it under this name:

```python
def return_violations(document: object, schema: Mapping[str, object]) -> list[Violation]: ...
```

`Violation` is the existing `graphscene.model.errors.Violation(path, reason)`.

**Work:**

- [ ] **`return_schema.py`, the validator.**
  - Pick the validator class with `jsonschema.validators.validator_for(schema, default=Draft7Validator)`. That honours a declared `$schema` and defaults to draft-07, the draft both the shipped `flow-graph.schema.json` and the harness's `plugin/schemas/*.return.json` declare.
  - Call that class's `check_schema` first. Turn a `jsonschema.exceptions.SchemaError` into `ValueError("return schema: <message>")`, so no `jsonschema` exception type crosses the boundary.
- [ ] **`return_schema.py`, the ECMA-262 patterns.**
  - Rewrite the schema's `pattern` keywords with the translator `graphscene/src/graphscene/adapters/schema.py` already owns, `_ecma_patterns`. Import it from that module; never copy it.
  - Render paths with the same module's `_render`, so a path reads as `schema_violations`' paths do: dotted keys, `[i]` indices, `""` for the root.
  - A pattern outside the translator's set raises the translator's own `ValueError` naming the pattern's schema path. This is the rule in `harness-runs/lessons.md` → *"A shim that makes one engine read a shared contract as another engine does lists the constructs it supports and refuses every other one"*.
- [ ] **`return_schema.py`, the result and the docstring.**
  - Return every violation as `Violation(path, error.message)`, sorted by path then reason, as `schema_violations` does. Return `[]` for a valid document.
  - The module docstring states what the module owns.
  - A *"The rule:"* paragraph covers the draft choice, the pattern translation and the sorted result. It also says a non-empty result is what Task 1's `undelivered` class means by *"failed the schema the executor names"*, citing `graphscene.model.execution`.
  - A *"Deliberately not covered:"* list says the module neither parses text into a document nor chooses a failure class: both are the executor's. It also says the schema is the caller's, never loaded from a repository path.
- [ ] **`tests/adapters/test_return_schema.py`.**
  - The module docstring opens *"The rule this file exists to enforce"*. Use plain `-> None` test functions. Each schema is planted in the test as a dict literal, and every expected `Violation` is written by hand.
  - Cases:
    - A valid document gives `[]`.
    - A missing required key gives its exact `Violation` at path `""`.
    - Two violations come back sorted by path.
    - A nested array item's path renders with `[i]`.
    - An invalid schema (for example `{"type": 5}`) raises `ValueError` whose message opens `return schema: `.
    - A pattern with `$` follows ECMA-262: `"a\n"` fails `{"type": "string", "pattern": "^a$"}`.
    - A pattern using an untranslated construct (for example `\d`) raises the translator's `ValueError`.
    - A schema declaring draft 2020-12 in `$schema` is validated by that draft. Use a `prefixItems` case, which draft-07 ignores.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_return_schema.py` passes.
- `commands.typecheck` passes.
- `return_schema.py` contains no copy of the pattern translator or of `_render`: grep it for `def _ecma` and `def _render` and find neither.
- `graphscene/pyproject.toml` is unchanged: no dependency is added.
