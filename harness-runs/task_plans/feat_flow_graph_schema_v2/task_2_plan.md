### Task 2 — Add the generic format-4 flow-graph schema to `graphscene` with its generic and schema-negative fixtures

**Goal:** Ship the generic flow-graph schema, format 4, as `graphscene` package data, so it travels with the library. In format 4 a graph declares its own outcomes, bindings and skip predicates, each mapped to an engine primitive, and the schema names none of the harness's names.

**Depends on:** Task 1, but only as a cross-check: the harness's format-4 graph at `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` must validate against this schema. This task's own fixtures carry no harness name.

**Where this layer stops.** The schema checks shape only. Whether every name a graph uses is declared, and whether a binding's primitive fits where it is used, is **Task 3's** `graphscene.vocabulary.vocabulary_violations`, because draft-07 cannot take an enum from the document's own data. Wiring the fixtures into npm scripts and gate 3 is **Task 5's**. This task names in its own files which fixture is meant to pass and which to fail, so that Task 5 can list them. Nothing under `graphscene/src/graphscene/` may name `devscene`, the harness's configuration file, a harness outcome (`PASS`, `FAIL`, `returned`, `no_ui`, …), a binding (`<ask>`, `<escalate>`, `<terminal_handoff>`), a phase (`parity`, `qa`, `docs`) or a reason (`cap`, `error`, `blocker`) (`.claude/context/graphscene.md` → `## What it may depend on`).

### Targets

- `graphscene/src/graphscene/schemas/flow-graph.schema.json` (new) — the format-4 schema.
- `graphscene/tests/fixtures/flow_graph/valid_generic.json` (new) — a small schema-valid graph in a non-harness vocabulary.
- `graphscene/tests/fixtures/flow_graph/schema_negative_*.json` (new) — the shape negatives listed below.
- `graphscene/tests/test_flow_graph_schema.py` (new) — the schema's own test.

**Work:**

- [ ] **The schema** — draft-07, `"$schema": "http://json-schema.org/draft-07/schema#"`. It must compile under `schemas/validate.mjs`'s `new Ajv()` with strict mode on, as `schemas/flow-graph.schema.json` does, so follow that file's `if`/`then`/`else` and `definitions` idioms. Its top-level `description` states that the schema checks shape only, and that the names a graph uses are checked against the names it declares by `graphscene.vocabulary`. Carry the v3 schema's descriptions over where the key is unchanged, minus every harness-specific sentence (any naming `scripts/check-flow-graph.sh`, a plugin document, a mode fork or `run-mode`).
  - **Top level:** `required` is `formatVersion` (`const: 4`), `flow`, `description`, `vocabulary`, `start`, `entries`, `counters`, `paths`, `reports`, `nodes`, with `additionalProperties: false`. `start`, `entries`, `counters`, `paths`, `reports` and `nodes` keep their v3 shapes.
  - **`vocabulary`:** `required` is `outcomes`, `bindings`, `predicates`, with `additionalProperties: false`.
    - `outcomes`: `minProperties: 1`, `propertyNames` `^[A-Za-z][A-Za-z0-9_]*$`. Each value is an object with `additionalProperties: false`, an optional `verdict` (`enum: ["pass", "fail"]`), an optional `held` (`const: true`), and `"not": { "required": ["verdict", "held"] }`.
    - `bindings`: `minProperties: 1`, `propertyNames` `^<[a-z][a-z0-9_]*>$`. Each value carries a required `primitive` (`enum: ["interrupt", "stop", "end"]`), and an `if`/`then` chain on `primitive` fixes the rest: `interrupt` requires `resumeOutcome` (`^[A-Za-z][A-Za-z0-9_]*$`); `stop` requires `reasons` (`array`, `minItems: 1`, `uniqueItems`, items `^[a-z][a-z0-9_]*$`); `end` takes nothing else. Each variant has `additionalProperties: false`.
    - `predicates`: `propertyNames` `^[a-z][a-z0-9_-]*$`. Each value requires `records` (`^[a-z][a-z-]*$`) and `inRoundCounts` (`boolean`), with `additionalProperties: false`. The `description` says the host answers each predicate true, false or "cannot answer", that "cannot answer" refuses, and that the graph never reads configuration.
  - **Nodes:**
    - `kind` stays `enum: ["dispatch", "round", "terminal"]`.
    - A dispatch node keeps v3's keys (`agent`, `heartbeat`, `prompts`, `findingsFolder`, `skip`, `outcomes`). Its `outcomes` `propertyNames` is the outcome-name pattern, with no enum.
    - A `skip` item is `{ "when", "to", "report"? }` (`required: ["when", "to"]`, `additionalProperties: false`, `when` the predicate-name pattern).
    - A round node keeps v3's keys. Its `outcomes` is `minProperties: 2`, `maxProperties: 2`, with outcome-name `propertyNames` and edge values, and no `PASS`/`FAIL` literal.
    - A terminal node is `{ "kind", "binding" }` with the binding-name pattern.
  - **Edges:** `edge` keeps v3's `if: { required: ["binding"] }` split.
    - An ordinary edge keeps `to`, `increment`, `reset`, `prompt`, `ledger`, `report` and `onCap` with v3's `increment`↔`onCap` dependency.
    - `onCap` is `{ "binding", "reason", "summary"?, "roundCounts"?, "evidence"? }`, `required: ["binding", "reason"]`.
    - A binding edge is `{ "binding", "resume"?, "reason"?, "summary"?, "roundCounts"?, "evidence"? }`, `required: ["binding"]`, `additionalProperties: false`, with the binding-name pattern and `reason` `^[a-z][a-z0-9_]*$`.
- [ ] **`valid_generic.json`** — a schema-valid, vocabulary-clean graph of about five nodes in a vocabulary that shares no name with the harness. It has outcomes `done`, `approved`, `rejected`, `crashed` (`approved` verdict `pass`, `rejected` verdict `fail`, `crashed` held); bindings `<pause>` (interrupt, `resumeOutcome: "resumed"`), `<halt>` (stop, `reasons: ["limit", "crash"]`) and `<finish>` (end); and one predicate, `stage_disabled`. It contains one dispatch writer, one gate in a round whose two outcomes are `approved`/`rejected`, one skip, one `onCap`, and a terminal. Task 3's vocabulary negatives are copies of this file with one change each, so keep it small.
- [ ] **Schema negatives** — each is a copy of `valid_generic.json` with one change, and each must be rejected by the schema:
  - `schema_negative_format_version_3.json` — `formatVersion` 3.
  - `schema_negative_no_vocabulary.json` — the `vocabulary` key removed.
  - `schema_negative_unknown_primitive.json` — a binding with `"primitive": "park"`.
  - `schema_negative_interrupt_without_resume_outcome.json` — `<pause>` without `resumeOutcome`.
  - `schema_negative_outcome_verdict_and_held.json` — one outcome carrying both `verdict` and `held`.
  - `schema_negative_skip_construct.json` — a skip entry in v3's `{ "construct", "phase", "to" }` form.
  - `schema_negative_round_three_outcomes.json` — the round with a third outcome key.
- [ ] `graphscene/tests/test_flow_graph_schema.py` — module docstring opening *"The rule this file exists to enforce"*: the schema ships as package data and names no harness vocabulary. Annotate every case `-> None`. Read the schema through `importlib.resources.files("graphscene") / "schemas" / "flow-graph.schema.json"`. Cases:
  - It parses, and its `properties.formatVersion` is `{"const": 4, …}`.
  - `kind`'s enum is exactly `["dispatch", "round", "terminal"]`.
  - Walking every string anywhere in the schema, none equals any of `PASS`, `FAIL`, `returned`, `questions`, `no_ui`, `error`, `blocker`, `<ask>`, `<escalate>`, `<terminal_handoff>`, `parity`, `qa`, `docs`, `cap`, `skipped`, `passedByExclusion`, and none contains `devscene`. Pass the schema as a parsed value, so a planted case can feed it a dict carrying `"PASS"` and assert the exact offending string.
  - `valid_generic.json` and every `schema_negative_*.json` named above parse as JSON. Name them in an explicit list, never a glob.
  - A *"Deliberately not covered:"* list notes that schema validation itself runs through `ajv` from the repository root (Task 5's npm scripts) because the package declares no JSON Schema runtime dependency.

**Verification:**

- `node schemas/validate.mjs validate -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d graphscene/tests/fixtures/flow_graph/valid_generic.json -d cli/templates/scripts/flows/task_plan_writing.v4.graph.json` exits 0. `schemas/validate.mjs` → `parseArgs` takes one data file per `-d` flag, so each file carries its own `-d`. The schema compiles under strict mode and accepts both the generic graph and the harness's.
- `node schemas/validate.mjs test -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d <each schema_negative_*.json> --invalid` passes for every negative above, and each prints a keyword path that names the constraint that negative exists to prove.
- `graphscene/tests/test_flow_graph_schema.py`, this task's own test file, passes through `scripts/python-service.sh`. `.claude/context/graphscene.md` → `## Not determined` records that no single-file command is yet stated for this layer, so where none can be run the unit records the skip as the test-run rule provides.
- `git grep -n -i -e devscene -- graphscene/src` prints nothing, and `git grep -n -F -e '<ask>' -e '"PASS"' -e '"FAIL"' -- graphscene/src` prints nothing. The second is case-sensitive and fixed-string on purpose: the schema's own `verdict` enum `["pass", "fail"]` is generic and must not match.
