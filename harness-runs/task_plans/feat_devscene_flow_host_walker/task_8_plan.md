### Task 8 — Register `tests/test_layers.py` as a tree guard and update gate 13j and the roadmap row

**Goal:** Wire up and record at the root what the package tasks built. Register the host's layer-contract test as a tree guard, so every later change to the package's source or manifest runs it. Make `docs/development.md`'s gate 13 paragraph name the host's whole suite, and make `ROADMAP.md`'s GraphScene row say what the host now ships.

**Depends on:** Tasks 1–7. Task 1 creates `devscene-flow-host/tests/test_layers.py`, which runs the `import-linter` contracts in `devscene-flow-host/pyproject.toml` over the package tree and names this task as its registering task (`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 8). Tasks 2–6 add the suites `tests/test_config.py`, `tests/test_ledger.py`, `tests/test_predicates.py`, `tests/test_store.py` and `tests/test_walking.py`. Task 7 documents all of it in `devscene-flow-host/README.md`. This task changes nothing under `devscene-flow-host/`.

**This is the catch-all task.** Its targets sit at the repository root, under the `general` layer (`path` `"."`), so its implementer reads every configured layer's conventions document, `.claude/context/conventions.md` first. `.claude/` is not a target: the tool layer refuses edits there.

### Targets

- `devscene.config.json` — two `treeGuards` entries.
- `docs/development.md` — the **Gate 13 — the Python packages.** paragraph, its 13j clause.
- `ROADMAP.md` — the `GraphScene` row.

**Work:**

- [ ] **`devscene.config.json` → `treeGuards`**: add two entries directly after the two existing `tests/test_boundary.py` entries that cover `devscene-flow-host/…`. They follow the same shape as the `graphscene` layer-test pair: `{"test": "tests/test_layers.py", "covers": "devscene-flow-host/src/devscene_flow_host/**"}` and `{"test": "tests/test_layers.py", "covers": "devscene-flow-host/pyproject.toml"}`. Change no other key, and keep the file's two-space indentation.
- [ ] **`docs/development.md` → Gate 13**: in the clause *"**13j** runs `bash scripts/python-service.sh --package devscene-flow-host test`, the GraphScene host's `pytest` suite, which is its boundary test, `devscene-flow-host/tests/test_boundary.py`, and its dependency test, `devscene-flow-host/tests/test_graphscene_dependency.py`"*, name what the suite now holds. That is the boundary test, the dependency test, and its layer-contract test, `devscene-flow-host/tests/test_layers.py`, which runs the `import-linter` contracts in `devscene-flow-host/pyproject.toml` with no cache, so it writes nothing into the checkout — the wording the same paragraph already uses for 13g. It also holds the suites of its records, its predicate host, its walk store and its walk of the harness's format-4 planning graph. Name each of those by file. Change nothing else in the paragraph.
- [ ] **`ROADMAP.md` → the `GraphScene` row**: replace *"the harness's GraphScene host's skeleton at `devscene-flow-host/`, with no behaviour yet, depending on GraphScene's public surface only, enforced by its own test, and gated by gate 13's legs 13h–13j"*. The new text states the host at `devscene-flow-host/` with its three layers held by `import-linter` contracts. It reads `devscene.config.json` and the flow-progress ledger, answers the planning graph's phase and run-mode predicates, and keeps each branch's walk in its own file. It loads and walks the harness's format-4 graph through GraphScene's `Walker` in its own suite, with no command line yet. Keep the existing link to `devscene-flow-host/README.md`, the public-surface dependency and the gate 13h–13j clause. Leave the row's `Left:` list and its status cell unchanged.

**Verification:**

- `node -e "JSON.parse(require('fs').readFileSync('devscene.config.json','utf8'))"` exits zero.
- `git diff -- devscene.config.json` shows exactly the two added `treeGuards` entries.
- Every test file `docs/development.md`'s 13j clause names exists: check each with `ls devscene-flow-host/tests/`.
- The derivation commands of the story index's `## Scope register` (entries A and B), re-run verbatim, print no file outside the register's rows.
