### Task 5 — Record the Python loader in `docs/development.md` and the `ROADMAP.md` GraphScene row

**Goal:** Bring the root documents of record in line with what this branch shipped. The generic fixtures are now run through a Python loader as well as through `ajv`. The vocabulary check also runs inside `graphscene.load_graph`. The GraphScene roadmap row lists the graph model as shipped.

**Depends on:** Task 4, which makes the following importable from `graphscene` (listed in `graphscene.__all__`):

- `load_graph(graph: object) -> FlowGraph` and `load_graph_file(path)` (Task 3). They validate against `graphscene/src/graphscene/schemas/flow-graph.schema.json`, then run `vocabulary_violations`, then return the frozen typed model.
- `GraphError` (Task 1), a `ValueError` with `.stage`, one of `parse`, `schema` or `vocabulary`, and `.violations`, a tuple of `Violation(path, reason)`.
- `graphscene/tests/test_loader.py` (Task 3), which runs every `schema_negative_*.json` and `vocabulary_negative_*.json` under `graphscene/tests/fixtures/flow_graph/` through the loader. It asserts the stage and the path of each fixture's one change.

This task describes those facts and changes none of them. It is the **catch-all** task, the `layers[]` row whose `path` is `"."`, so it ships last, after the layer that built what it documents.

**How this task's implementer reads the conventions.** The catch-all layer has no single neighbouring layer, so read `.claude/context/conventions.md` in full: its `## Documents of record` binds both files. Also read `.claude/context/graphscene.md` for the package's own vocabulary.

### Targets

- `docs/development.md` — `## 5. Verifying a change`, **Gate 3**: two paragraphs.
- `ROADMAP.md` — the GraphScene row.

**Work:**

- [ ] **`docs/development.md` → Gate 3, the paragraph opening "The last three lines, legs `3g`, `3h` and `3i`".**
  - After its sentence on `npm run validate:graphscene-schema:negative` (`3h`), add one sentence. It says that `graphscene/tests/test_loader.py` runs the same `schema_negative_*.json` files, and the `vocabulary_negative_*.json` files, through the Python loader `graphscene.load_graph` under gate 13's leg `13g`. It asserts each is rejected at its stage, so the two validators are held to the same fixtures.
  - Leave the command lines above the paragraph unchanged.
- [ ] **`docs/development.md` → the paragraph opening "The check that every name a format-4 graph uses is one it declares has two homes".**
  - Extend its generic-graph sentence: `graphscene.load_graph` runs `vocabulary_violations` after validating against the format-4 schema, so a graph it returns has passed both. The check's findings are `graphscene.Violation` values naming the node and the field.
  - Keep the paragraph's harness-side sentence about `scripts/generate-flow-graph-v3.mjs` (`3i`) verbatim.
- [ ] **`ROADMAP.md` → the GraphScene row.**
  - Add a final clause to *Shipped:*, after the format-4 clause: the graph model, `load_graph`, which validates a parsed graph against the format-4 schema and the vocabulary check and returns it as typed objects, with one error type for every rejection.
  - Keep *Left:* and the status cell (`In progress`) unchanged: the engine, the walker's port, the harness-side package and the format-4 cutover are all still left.

**Verification:**

- **Both files.** Re-run the story index's `## Scope register` command entry verbatim:

  ```
  git grep -l -E 'vocabulary_violations|graphscene-schema|fixtures/flow_graph|no engine code' -- '*.md' ':!harness-runs/**' ':!examples/**'
  ```

  The invariant: its output ⊆ the register's rows. Rows 4, 6 and 7 (this task's) now read as their `change` dispositions describe.
- **`docs/development.md`.** Every name the new sentences cite resolves in the tree:
  - `graphscene/tests/test_loader.py` exists;
  - `grep -n 'load_graph' graphscene/src/graphscene/__init__.py` has a hit;
  - `grep -n 'Violation' graphscene/src/graphscene/__init__.py` has a hit.
- **`ROADMAP.md`.** The row is still one Markdown table row. `grep -n '^| GraphScene |' ROADMAP.md` matches a line that also carries `In progress |`, so no line break was introduced into the row.
