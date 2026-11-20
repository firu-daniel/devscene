### Task 3 — Add `graphscene.vocabulary.vocabulary_violations`, the used-against-declared names check, with its fixtures and tests

**Goal:** Give the library the check that JSON Schema cannot express: every name a format-4 graph uses is one it declares under `vocabulary`, and each binding is used where its primitive allows. The format-4 equivalents of the v3 negatives `flow-graph-schema-unknown-outcome.json`, `-unknown-binding.json` and `-ask-without-resume.json` are therefore rejected here, not by the schema.

**Depends on:** Task 2, which produces `graphscene/src/graphscene/schemas/flow-graph.schema.json` and `graphscene/tests/fixtures/flow_graph/valid_generic.json`. The shape this check reads is that schema's, restated here so this file is complete on its own:

- `vocabulary.outcomes` maps a name to `{}`, `{ "verdict": "pass" | "fail" }` or `{ "held": true }`.
- `vocabulary.bindings` maps `<name>` to `{ "primitive": "interrupt", "resumeOutcome" }`, `{ "primitive": "stop", "reasons": [...] }` or `{ "primitive": "end" }`.
- `vocabulary.predicates` maps a name to `{ "records", "inRoundCounts" }`.
- A node's `outcomes` maps an outcome name to an edge. An edge either has `to` (and optionally `onCap: { "binding", "reason", … }`) or has `binding` (with optional `resume`, `reason`, …).
- A terminal node has `binding`. A dispatch node's `skip` is a list of `{ "when", "to", "report"? }`.

**Where this layer stops.** The check takes an already schema-valid graph as a parsed mapping and returns violation strings. It reads no file and runs no schema validation. It does not check node-id references, reachability or caps, which belong to a static checker this branch does not build. It is stdlib-only and names nothing of the harness: a harness-side caller can call it later, but nothing in this branch calls it outside the tests. `scripts/generate-flow-graph-v3.mjs` (Task 4) maps names on its own and does not call this module.

### Targets

- `graphscene/src/graphscene/vocabulary.py` (new) — the check.
- `graphscene/src/graphscene/__init__.py` — export `vocabulary_violations`.
- `graphscene/tests/fixtures/flow_graph/vocabulary_negative_*.json` (new) — schema-valid, vocabulary-invalid fixtures.
- `graphscene/tests/test_vocabulary.py` (new) — the check's tests.
- `graphscene/README.md` — `## What it is`.

**Work:**

- [ ] `graphscene/src/graphscene/vocabulary.py` — the module docstring states what the module owns and its rule, *"every name a flow graph uses is one it declares, and each binding is used where its primitive allows"*, plus what it deliberately does not check (above). Public `vocabulary_violations(graph: Mapping[str, object]) -> list[str]`, narrowing with `isinstance` under mypy `strict`, with no `Any` leak. Violations come in document order: nodes in key order, and within a node its `outcomes` in key order (each edge, then its `onCap`), then its `skip` entries, then a terminal's `binding`. Each violation is one string of the exact form `<path>: <reason>`, where `<path>` is a dotted path like `nodes.<id>.outcomes.<name>`, with `[<i>]` for a skip index:
  1. An undeclared outcome key on any node: `nodes.<id>.outcomes.<name>: outcome '<name>' is not declared in vocabulary.outcomes`.
  2. A round whose two outcome keys are not one declared with `verdict: pass` and one with `verdict: fail`: `nodes.<id>.outcomes: a round routes on one outcome declaring verdict pass and one declaring verdict fail`. Emit this once per round, and only when clause 1 found nothing undeclared on that round.
  3. An undeclared binding on an edge, an `onCap` or a terminal: `<path>.binding: binding '<b>' is not declared in vocabulary.bindings`.
  4. An edge's binding whose primitive is `end`: `<path>.binding: binding '<b>' is an end; only a terminal node takes one`. A terminal whose binding is not an `end`: `nodes.<id>.binding: binding '<b>' is not an end`.
  5. An `interrupt` edge with no `resume`: `<path>: binding '<b>' is an interrupt and needs resume`. A `resume` on a non-interrupt edge: `<path>.resume: binding '<b>' is not an interrupt`.
  6. A `stop` edge or an `onCap` with no `reason`, or a `reason` its binding does not declare: `<path>.reason: '<r>' is not a reason binding '<b>' declares` (use `<path>: binding '<b>' is a stop and needs reason` when `reason` is absent). A `reason` on an `interrupt` edge: `<path>.reason: binding '<b>' is not a stop`. An `onCap` whose binding is not a `stop`: `<path>.onCap.binding: binding '<b>' is not a stop`.
  7. An undeclared skip predicate: `nodes.<id>.skip[<i>].when: predicate '<p>' is not declared in vocabulary.predicates`.

  Clauses 4–6 apply only to a declared binding, because an undeclared one is clause 3 alone.
- [ ] `graphscene/src/graphscene/__init__.py`: `from graphscene.vocabulary import vocabulary_violations` and `__all__: list[str] = ["vocabulary_violations"]` (`.claude/context/graphscene.md` → `## Naming and layout`). Keep the module docstring's boundary paragraph as it is. The import must stay in bounds: `graphscene/tests/test_boundary.py` → `test_the_real_library_stays_inside_its_boundary` scans the new module.
- [ ] **Vocabulary negatives** — each is a copy of `valid_generic.json` with one change, and each must stay **schema-valid**:
  - `vocabulary_negative_unknown_outcome.json` — a dispatch node routes an undeclared outcome.
  - `vocabulary_negative_unknown_binding.json` — an edge names an undeclared binding.
  - `vocabulary_negative_interrupt_without_resume.json` — a `<pause>` edge with no `resume`.
  - `vocabulary_negative_undeclared_reason.json` — a `<halt>` edge whose `reason` is not in its `reasons`.
  - `vocabulary_negative_round_without_fail_verdict.json` — the round's two outcomes both declared with `verdict: pass`.
  - `vocabulary_negative_end_on_an_edge.json` — an edge bound to `<finish>`.
  - `vocabulary_negative_unknown_predicate.json` — a skip whose `when` is undeclared.
- [ ] `graphscene/tests/test_vocabulary.py` — module docstring opening *"The rule this file exists to enforce"*, with a *"Deliberately not covered:"* list repeating the module's. Annotate every case `-> None`. Following `.claude/context/graphscene.md` → `## Tests` (*"a planted case per clause, each asserting the exact violation text, plus one clean case and one run against the real tree"*):
  - one in-test dict case per clause 1–7, including both arms of clauses 4, 5 and 6, each asserting the exact list returned;
  - `valid_generic.json` returns `[]`;
  - each `vocabulary_negative_*.json`, named in an explicit list and never a glob, returns exactly its one expected string;
  - one case asserting document order across two violations in one graph.

  Fixtures are read from `Path(__file__).parent / "fixtures" / "flow_graph"`, and no file is written anywhere.
- [ ] `graphscene/README.md` → `## What it is`: replace *"It has no engine code yet and no runtime dependency"* with a sentence saying the package has no engine code yet and still declares no runtime dependency, but carries the generic flow-graph schema (format 4) and the vocabulary check. Add two rows to the path table: `src/graphscene/schemas/flow-graph.schema.json` (the format-4 schema, shipped as package data) and `src/graphscene/vocabulary.py` (`vocabulary_violations`, the used-against-declared names check JSON Schema cannot express). Name no harness file.

**Verification:**

- `graphscene/tests/test_vocabulary.py`, this task's own test file, passes through `scripts/python-service.sh`. `.claude/context/graphscene.md` → `## Not determined` records that no single-file command is stated for this layer yet, so where none can be run the unit records the skip as the test-run rule provides.
- `node schemas/validate.mjs validate -s graphscene/src/graphscene/schemas/flow-graph.schema.json -d <every vocabulary_negative_*.json>` exits 0: each negative is schema-valid, so the vocabulary check is the only thing rejecting it.
- `vocabulary.py` and `test_vocabulary.py` carry full annotations with no `Any` and no `# type: ignore`, because mypy `strict` covers `src` and `tests` (`graphscene/pyproject.toml` → `[tool.mypy]`). Gate 13's legs grade that in the Run gates round, not this unit.
- `git grep -n -i -e devscene -- graphscene/src` prints nothing, and `git grep -n -F -e '<ask>' -e '"PASS"' -e '"FAIL"' -e "'PASS'" -e "'FAIL'" -- graphscene/src` prints nothing. The second is case-sensitive and fixed-string on purpose: the generic `pass`/`fail` verdict values — the schema's enum and the violation strings clause 2 requires, such as *"a round routes on one outcome declaring verdict pass and one declaring verdict fail"* — must not match; only the harness's quoted `PASS`/`FAIL` outcome names and its `<ask>` binding must.
- **Deviations from plan:**
  - The ordering rule did not say where clause 2 goes. It is emitted first among a round's violations, before its `outcomes` entries, because its path `nodes.<id>.outcomes` is their parent. The module docstring says so.
  - Clause 6's "not a stop" arm is applied to a `reason` on any non-stop edge, which covers an `end` edge as well as an `interrupt` one. An `onCap` whose binding is not a stop gets only `.onCap.binding: … is not a stop`, never clause 4's end text, and its `reason` is not checked.
  - Evidence downgrade: the claim that mypy `strict` and ruff pass on `vocabulary.py` and `test_vocabulary.py` was not run. It rests on reading the code and on a probe (`grep -nE '^.{101,}'` over the three Python files) that found no line over 100 characters. Deferred to the Run gates phase (gate 13's legs), as the plan states.
