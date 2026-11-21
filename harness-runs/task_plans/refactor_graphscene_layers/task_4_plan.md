### Task 4 — Repoint the root documents at the layered modules and register `tests/test_layers.py` as a tree guard

**Goal:** Bring the documents at the repository root in line with the layered package, so none of them points at a module or test file Task 1 deleted. Also register Task 2's contract test as a tree guard, so a unit that changes GraphScene's source or its contracts runs that test.

**Depends on:**

- **Task 1**, which moves the vocabulary check to `graphscene.engine.vocabulary.vocabulary_violations`, still exported as `graphscene.vocabulary_violations`. Its test moves to `graphscene/tests/engine/test_vocabulary.py`. The loader's fixture cases move to `graphscene/tests/facade/test_loading.py`, still calling `graphscene.load_graph`. `graphscene/src/graphscene/vocabulary.py` and `graphscene/tests/test_loader.py` no longer exist.
- **Task 2**, which adds `graphscene/tests/test_layers.py`. That test reads every module under `graphscene/src/graphscene/` and the contracts in `graphscene/pyproject.toml`. Task 2's file names this task as its registering task (`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 8).
- **Task 3**, which states the layer rules in `graphscene/README.md` → `## The layers`. This task cites that section and does not restate the rules.

**Where this task stops.** It changes no file under `graphscene/`. It does not edit `.claude/context/graphscene.md`, `.claude/context/conventions.md` or `.claude/CLAUDE.md`. Each still names the flat layout or `graphscene/tests/test_vocabulary.py`, and each is a supervised follow-up after merge (the story index's `## Scope register`, rows 9–14). `package.json` is unchanged, because the fixtures did not move.

**How this task's implementer reads the conventions.** This is the catch-all task (the `layers[]` row whose `path` is `"."`). Read `.claude/context/conventions.md` for this layer's own rules. Read `.claude/context/graphscene.md` for the package these documents describe.

### Targets

- `docs/development.md` — three sentences.
- `docs/flow-graph-walker.md` — one sentence.
- `devscene.config.json` — two `treeGuards` entries.

**Work:**

- [ ] **`docs/development.md`, the Gate 3 format-4 paragraph** (the one opening *"The last three lines, legs `3g`, `3h` and `3i`"*): replace `` `graphscene/tests/test_loader.py` `` with `` `graphscene/tests/facade/test_loading.py` ``. The rest of the sentence stays as it is: it still passes the same fixtures through `graphscene.load_graph`, which is still the public name.
- [ ] **`docs/development.md`, the paragraph opening *"The check that every name a format-4 graph uses is one it declares has two homes"***: name the generic home `graphscene.engine.vocabulary.vocabulary_violations`, exported as `graphscene.vocabulary_violations`, tested by `graphscene/tests/engine/test_vocabulary.py`. Add one clause citing `graphscene/README.md` → `## The layers` for where it sits among the library's layers. Leave the `graphscene.load_graph` and `graphscene.Violation` clauses and the harness-side sentence unchanged.
- [ ] **`docs/development.md`, **Gate 13 — the Python packages.***: extend the 13g clause *"which includes its import-boundary test, `graphscene/tests/test_boundary.py`"* to also name its layer-contract test, `graphscene/tests/test_layers.py`. That test runs the `import-linter` contracts in `graphscene/pyproject.toml` with no cache, so it writes nothing into the checkout. Leave every other leg and sentence of the paragraph unchanged.
- [ ] **`docs/flow-graph-walker.md`, the **Decision.** paragraph**: replace `` `graphscene.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/vocabulary.py`) `` with `` `graphscene.engine.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/engine/vocabulary.py`) ``. This is the one sentence that says where the check lives. The decision the paragraph records is unchanged, and so is every other sentence in it.
- [ ] **`devscene.config.json` → `treeGuards`**: append two entries after the existing ones, leaving every existing entry and every other key unchanged: `{ "test": "tests/test_layers.py", "covers": "graphscene/src/graphscene/**" }` and `{ "test": "tests/test_layers.py", "covers": "graphscene/pyproject.toml" }`. The `test` value is spelled as the `graphscene` layer's single-file command takes it, relative to `graphscene/` (`.claude/context/graphscene.md` → `## Tests`: `bash scripts/python-service.sh --package graphscene test tests/<test_file>.py`). The schema's `treeGuards.items.test` description allows exactly that, and `doctor`'s `tree-guards` check resolves it under the `graphscene` layer path. `layers` stays as it is, with `graphscene` as one layer.

**Verification:**

- Neither document names a deleted path. `git grep -nE 'graphscene\.vocabulary\b|graphscene/src/graphscene/vocabulary\.py|graphscene/tests/test_(loader|vocabulary)\.py' -- docs/development.md docs/flow-graph-walker.md` prints nothing.
- Every path the edited sentences name exists. `git ls-files graphscene/tests/facade/test_loading.py graphscene/tests/engine/test_vocabulary.py graphscene/tests/test_layers.py graphscene/src/graphscene/engine/vocabulary.py` lists each one.
- `git diff -- docs/development.md docs/flow-graph-walker.md` touches only the four sentences named under **Work:**. `git diff -- devscene.config.json` adds only the two `treeGuards` entries. Each entry carries exactly the keys `test` and `covers`, as `schemas/devscene.config.schema.json` → `treeGuards.items` requires (`additionalProperties: false`).
- No deleted path form survives in the files this task edits. Run `git grep -nE 'graphscene\.(loader|model|errors|vocabulary)([^A-Za-z0-9_]|$)|graphscene/src/graphscene/(loader|model|errors|vocabulary)\.py|graphscene/tests/test_(errors|vocabulary|model|loader)\.py' -- docs/development.md docs/flow-graph-walker.md devscene.config.json`. It must print nothing. The pattern matches only the forms Task 1 deleted, which are the flat module paths, their dotted module names and the flat test files directly under `graphscene/tests/`. It does not match their moved forms (`graphscene/tests/engine/test_vocabulary.py`, `graphscene.engine.vocabulary`), the exported name `graphscene.vocabulary_violations`, or a package-wide test file that stays put. Before this task runs, every line it prints is a sentence one of the **Work:** bullets rewrites. This check replaces the story index's entry A, which is unanchored and also matches moved paths.
