### Task 4 — Rename the package in gate legs 13h–13j, `docs/development.md` and `ROADMAP.md`

**Goal:** Make the hand-written gate script, the documentation of record and the roadmap name the package `devscene-flow-host`. Gate 13h–13j then select the renamed table row, and every document reading the package's name or path states the tree as it now is. No gate changes what it runs or how it grades.

**Depends on:** Task 1, which renames the wrapper's third table row:

- The table row is now `devscene-flow-host` (`scripts/python-service.sh` → `PACKAGES`, `package_row`), so `--package devscene-runtime` exits `2` as an unknown package.
- The package's tests are now `devscene-flow-host/tests/test_boundary.py` and `devscene-flow-host/tests/test_graphscene_dependency.py`.
- Its manifest is `devscene-flow-host/pyproject.toml`, still sourcing `graphscene` through `[tool.uv.sources]`.
- Its lock is `devscene-flow-host/uv.lock`, re-made with `bash scripts/python-service.sh --package devscene-flow-host lock`.
- The package is the harness's GraphScene host, imported as `devscene_flow_host` (`devscene-flow-host/README.md` → `## What it is`).

This task restates those names and changes nothing under `devscene-flow-host/` or in `scripts/python-service.sh`.

**Where this task stops.** `docs/development.md` → `## 8. The nightly supply-chain audit` describes `.github/workflows/supply-chain.yml`. This task updates that section's prose and never edits the workflow file. No run-landed commit may change that file: the maintainer commits its edit at Task 5's park, to match the sentence this task writes (story index `## Context` → **The workflow edit, and why the run never commits it.**, manual step 1). Nothing under `.claude/` is touched: those sites are the maintainer's after-merge step 5.

**Wording.** Write each site as if the package had always had this name. Never "renamed from", "formerly" or the old name in any form (`harness-runs/lessons.md` → `## Adopter-facing documentation`, the rename lesson). Every command stays in its own fenced block, one command per line (the first lesson under the same heading).

### Targets

- `scripts/run-gates.sh`
- `docs/development.md`
- `ROADMAP.md`

**Work:**

- [ ] **`scripts/run-gates.sh`.**
  - Each of the three cases `13h)`, `13i)` and `13j)` changes in two places: the label (`"13h devscene-runtime lint"` → `"13h devscene-flow-host lint"`, and likewise for `typecheck` and `tests`) and the `--package devscene-runtime` argument → `--package devscene-flow-host`.
  - In the header comment, *"the DevScene runtime's legs 13h, 13i and 13j"* becomes *"the GraphScene host's legs 13h, 13i and 13j"*. Re-wrap the comment only if a line would otherwise exceed its neighbours' width.
  - Leave the leg ids, their order on the `gr_run_round` line and every other case unchanged.
- [ ] **`docs/development.md` → `## 5. Verifying a change`, **Gate 13**.** Replace every `devscene-runtime` with `devscene-flow-host` across the gate's two prose paragraphs and its re-lock code block:
  - the opening leg list (*"`devscene-runtime/` through 13h–13j"*);
  - the three **13h**/**13i**/**13j** commands, and the two test paths that sentence names;
  - the `addopts` sentence (*"`graphscene`'s and `devscene-runtime`'s `addopts`"*);
  - *"`devscene-runtime` is the third row"*;
  - the `[tool.uv.sources]` citation and *"re-locks `devscene-runtime` too"*;
  - the fenced block `bash scripts/python-service.sh --package devscene-flow-host lock`.

  Also change *"the DevScene runtime's `pytest` suite"* to *"the GraphScene host's `pytest` suite"*. Nothing else in the gate changes.
- [ ] **`docs/development.md` → `## 8. The nightly supply-chain audit`.** In the `uv-audit` table row, change `devscene-runtime/uv.lock` to `devscene-flow-host/uv.lock`. In the sentence *"`uv-audit`, once each from `docs-retrieval-service/`, `graphscene/` and `devscene-runtime/`:"*, change the last directory to `devscene-flow-host/`.
- [ ] **`ROADMAP.md` → the `GraphScene` row.** Rewrite the clause *"the harness-side package's skeleton at `devscene-runtime/`, DevScene's own Python runtime with no behaviour yet, … ([`devscene-runtime/README.md`](devscene-runtime/README.md))"* to read: *"the harness's GraphScene host's skeleton at `devscene-flow-host/`, with no behaviour yet, depending on GraphScene's public surface only, enforced by its own test, and gated by gate 13's legs 13h–13j ([`devscene-flow-host/README.md`](devscene-flow-host/README.md))"*. The rest of the row and its `In progress` status stay as they are.

**Verification:**

- `git grep -n -i -E "devscene[-_ ]runtime|DevScene.s own Python runtime" -- scripts/run-gates.sh docs/development.md ROADMAP.md` prints nothing.
- `git grep -n -E "devscene-flow-host" -- scripts/run-gates.sh` prints exactly the three `13h`/`13i`/`13j` case lines, each naming `devscene-flow-host` twice.
- Every link and path this task wrote resolves to a tracked file: `git ls-files devscene-flow-host/README.md devscene-flow-host/uv.lock devscene-flow-host/pyproject.toml devscene-flow-host/tests/test_boundary.py devscene-flow-host/tests/test_graphscene_dependency.py` lists all five.
- `git diff HEAD --stat -- scripts/run-gates.sh docs/development.md ROADMAP.md` shows changes in those three files only, and `git diff HEAD -- scripts/run-gates.sh` touches only the header comment and the three `13h`–`13j` lines.
