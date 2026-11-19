# Story: GraphScene starts as an isolated Python library inside this repository

## Context

This branch creates GraphScene, the flow-graph navigation library of `ROADMAP.md` → `## Scene products`, as its own Python package at `graphscene/`, with its toolchain and gates in place before any engine code is written. It holds no engine code. It holds the package's manifest, an empty typed package `graphscene`, a boundary test that keeps the library generic, a README, the package's row in `scripts/python-service.sh`'s table with its `uv.lock`, gate 13's three new legs in `scripts/run-gates.sh`, the `cli` suite that pins the wrapper's new row, and the documentation of the gate. Part of #376. It depends on #411, which has landed: `scripts/python-service.sh` already serves a closed package table selected with `--package <dir>`, keeps each package's environment in `<package>/.venv`, and `provision` syncs every row at a run copy's bootstrap. A new package therefore joins as one more table row and does not get a second wrapper.

**The decisions this plan takes.** The prompt's leads are starting points. These are what the plan holds to:

1. **The library is `graphscene/`, set up like `docs-retrieval-service/`.** The distribution and its import package are both named `graphscene`, in a `src/` layout. It requires Python `>=3.11`, declares **no runtime dependency**, and has a `dev` group of `ruff`, `mypy` and `pytest`. It uses the same `ruff`, strict `mypy` and `pytest` settings as `docs-retrieval-service/pyproject.toml`, without that package's `container` marker, `models` extra or `torch` index. It declares no console script and no compose file. It is not part of the npm package (`cli/package.json` → `files`), so no adopter receives it. Task 1.
2. **The harness side lives outside `graphscene/`, and the dependency points from the harness to the library only.** The harness-specific code the walker port will need is config reading, the `claude` executor and the planning hooks. None of it exists yet, and this branch writes none. When it is written, it goes in its own distribution outside `graphscene/`, named with a `devscene` prefix (import name `devscene_…`), and that distribution depends on `graphscene`. `graphscene` never depends on it. Extraction then means moving one directory.
3. **The boundary is enforced by a test inside the library, so the rule travels with it when it is extracted.** `graphscene/tests/test_boundary.py` parses every module under `src/graphscene/` with `ast` and flags four things: an import (static, `importlib.import_module` or `__import__` with a constant name) of anything that is not the standard library, `graphscene` itself or a declared runtime dependency; any `devscene`-prefixed module; any string constant carrying `devscene.config.json`; and any declared dependency in `graphscene/pyproject.toml` whose name starts with `devscene`. Planted violations prove that each rule fires. Gate 13's new test leg runs it in every Run gates round. Task 1.
4. **The gates are gate 13's legs, not a seventeenth gate.** Gate 13 becomes *the Python packages*. 13a–13d stay the docs-retrieval service's legs, and three new legs run `lint`, `typecheck` and `test` with `--package graphscene`: **13e**, **13f** and **13g**. They reuse gate 13's existing `BLOCKED` grading, so `docs/development.md` § 5's count of sixteen gates, nine of them unattended, still holds. Task 3 adds the legs, and Task 5 documents them.
5. **A table row serves only the sub-commands it can.** `graphscene` has no console script and no compose file. So `run` and `container-test` on that row exit `2` with a line naming the package and what it lacks, and they never reach `uv` or `docker`. Task 2 adds this, and Task 4 pins it.
6. **The layer is a manual action owed after merge.** A `graphscene` row in `devscene.config.json` → `layers` needs a conventions document, and its `CLAUDE.md` row is under `.claude/`. Neither is work a run plans. The run reports it as an `undescribed-layer` staleness entry, and the steps are listed under **Manual setup required** below.

**What no unit runs.** `## The test-run rule` forbids running a gate script or a test file outside `<test_file_cmd>`, so no task runs the new package's `pytest`, `ruff` or `mypy`. Their evidence is gate 13's legs 13e–13g in the Run gates round. Those legs grade `BLOCKED`, not failed, until the run copy is provisioned with the new row. This branch's copy was bootstrapped with the one-row wrapper. The first manual step below provisions it at Task 2's park, so that the round grades the legs for real. Without that step, the first real grading is the first hand run after merge. That step has now been taken (clarification Q1), so this run's Run gates round is expected to grade 13e–13g rather than report them `BLOCKED`.

**Ship order.** The three `general` tasks come first, because they create what is pinned: the package (Task 1), its wrapper row and lock (Task 2), and the gate legs (Task 3). The `cli` suite that pins the wrapper row follows (Task 4). The catch-all documentation task comes last (Task 5). This puts `cli` after `general` for the test task, against the configured layer order, because a suite cannot pin a table row that does not exist yet. `harness-runs/story_plans/fix_python_gate_run_copies_story_plan.md` ordered its wrapper and that wrapper's suite the same way.

**Top risks:**

- **The lock.** The lock is the plan's sharpest edge. `uv lock` reaches PyPI and writes the shared `uv` cache, and the run's sandbox most likely allows neither. A branch merged with the `graphscene` row but no `graphscene/uv.lock` makes `provision`'s `uv sync --frozen` fail for that row. That would fail the bootstrap of every later run copy. Task 2 owns the row and the lock together, and returns a blocker naming the manual step rather than landing the row alone. Its Verification requires `graphscene/uv.lock` to be present in the same change.
- **Python that has never run.** The new Python may first run only after merge, failing `ruff format --check` or strict `mypy`. Task 1 prescribes typing and layout matching the house settings, and the first manual step provisions the run copy so that 13e–13g grade before merge.
- **A boundary test that passes vacuously** because it scans the wrong directory. Task 1's planted-violation cases guard it, along with its assertion that the real `src/graphscene/__init__.py` is among the files scanned.

**Manual setup required:**

- **When Task 2 parks on the lock** (expected in a sandboxed run), run these two commands from an ordinary unsandboxed terminal at the run copy's root, then resume the run. Depends on Task 2. **Done for this run:** Task 2 parked as expected (clarification Q1), and the user answered "lock produced". Both commands exited 0, `lock` resolving 14 packages and `provision` syncing both rows. `graphscene/uv.lock` is left untracked for Task 2's commit. The resumed Task 2 re-runs neither command; see its file's resume bullet.

  ```
  bash scripts/python-service.sh --package graphscene lock
  ```

  ```
  bash scripts/python-service.sh provision
  ```

  The first writes `graphscene/uv.lock`, which Task 2 then commits. The second syncs both packages, so that the Run gates round grades 13e–13g rather than reporting them `BLOCKED`.
- **After this branch merges**, run this once in the main checkout and in any working copy made by hand, from an unsandboxed terminal, so that a hand run of the gates grades 13e–13g. Run copies get it at bootstrap. Depends on Task 2.

  ```
  bash scripts/python-service.sh provision
  ```

- **After this branch merges**, add the `graphscene` layer:
  1. Run `/devscene:analyze` in this repository, answering `skip` for every document that is already filled. Never use the `--yes` spelling. This writes the new layer's conventions document.
  2. Add the layer with `npx devscene config set layers`, with name `graphscene` and path `graphscene`.
  3. Add its row to `.claude/CLAUDE.md`'s `## Context files (read on demand)` table by hand.

  Until this is done, the architecture reviewer sees `graphscene/` only as part of the catch-all `general` layer. Depends on Task 1.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. In an index a run is iterating, an implementer never changes a marker here and never edits any other line of this section. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational progress markers for the implementer. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_graphscene_package_skeleton/task_<K>_plan.md` file.

1. [x] **Task 1** — Create the `graphscene/` package: manifest, empty typed `graphscene` package, the import-boundary test and its README _(layer: general)_ _(points: 20)_
2. [x] **Task 2** — Add `graphscene` to `scripts/python-service.sh`'s package table, refuse `run` and `container-test` on a row without them, and lock the package _(layer: general)_ _(points: 10)_
3. [x] **Task 3** — Add gate 13's GraphScene legs 13e–13g to `scripts/run-gates.sh` and retitle gate 13 as the Python packages _(layer: general)_ _(points: 10)_
4. [x] **Task 4** — Pin the `graphscene` row, its two refusals and the two-row `provision` in `cli/test/python-service.test.mjs` _(layer: cli)_ _(points: 15)_
5. [x] **Task 5** — Document gate 13's GraphScene legs in `docs/development.md` and move GraphScene's roadmap row to in progress _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"creates GraphScene as an isolated Python library inside this repository, with its toolchain and gates, before any engine code."* The corpus sites are every durable document that describes gate 13, the Python wrapper's package table, or GraphScene.

**Derivation entry A — gate 13 and the wrapper (command).** Re-run verbatim from the repository root: `git grep -lE 'python-service\.sh|[Gg]ate 13|\b13[a-d]\b|Python docs-retrieval service' -- '*.md' ':!harness-runs'`

**Derivation entry B — GraphScene (command).** Re-run verbatim from the repository root: `git grep -liE 'graphscene' -- '*.md' ':!harness-runs'`

**Derivation entry C — standing-artifact rows (procedure).**
- **First step, runnable:** `grep -niE 'python-service|gate 13|graphscene|[^a-z]uv[^a-z]' harness-runs/lessons.md harness-runs/improvement_suggestions.md`
- **Artifact:** the two standing ledgers under the state directory, `harness-runs/lessons.md` and `harness-runs/improvement_suggestions.md`.
- **Traversal:** each ledger's headings in file order, then the one-line entries under each.
- **Decision rule:** an entry is reached when it names gate 13, `python-service.sh`, `uv` or GraphScene.

When this plan was written, the procedure reached no entry, so it contributes no row.

**Closure invariant:** every site that any derivation entry reaches appears as a row below. After the branch's edits, each command's output is still ⊆ the files named in the rows.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `docs/development.md` → `**Gate 13 — the Python docs-retrieval service.**` paragraph, and the paragraph that closes gate 13 ("The wrapper's `--package <dir>` selects a row of a closed package table, so a later Python package joins the same wrapper as one more row") | — | entry A, `Gate 13`, `13a`–`13d`, `python-service.sh` | `change` | Task 5 — retitles the gate as the Python packages, adds 13e–13g, and names `graphscene` as the second row |
| 2 | `docs/development.md` → § 5's opening paragraph "Nine of the sixteen run unattended" ("Gate 13 is reported on the same terms in two ways") | — | entry A, `Gate 13` | `no-change` | Its count and its `BLOCKED` / `SKIPPED` terms are unchanged: the new legs grade `BLOCKED` on the same condition, and 13d is still the only container leg |
| 3 | `docs/development.md` → `**Gate 6 — self-containment.**`'s exclusion sentence ("`docs-retrieval-service` turns it off with `-p no:cacheprovider`, so that flag is a backstop for a later package") | — | entry A, `gate 13`, `python-service.sh` | `no-change` | Still true: `graphscene`'s `pyproject.toml` (Task 1) also carries `-p no:cacheprovider`, and the four excluded directory names cover every package |
| 4 | `docs-retrieval-service/README.md` → its setup paragraph and `## Testing` ("The suite is gate 13 in `scripts/run-gates.sh`") | — | entry A, `python-service.sh`, `gate 13` | `no-change` | Describes that package's own legs, whose commands keep their meaning under the default package |
| 5 | `docs/cli.md` → the `docs-retrieval-service/tests/test_launcher_e2e.py` bullet ("run by gate 13's leg 13d … leg 13c") | — | entry A, `gate 13`, `13d` | `no-change` | Which leg runs which case is unchanged |
| 6 | `docs/retrieval-eval.md` (the Python arm's `python-service.sh` commands and `WHERE IT WRITES` citation) | — | entry A, `python-service.sh` | `no-change` | Its commands keep their meaning under the default package |
| 7 | `evals/docs-retrieval/README.md` → the `python-backend.mjs` row | — | entry A, `python-service.sh` | `no-change` | The route it names is unchanged under the default package |
| 8 | `docs/retrieval-eval-results.md` | — | entry A, `python-service.sh` | `no-change` | Measured records of past runs |
| 9 | `docs/sandbox-verification.md` → the 2026-10-14 unsandboxed run ("Gate 13 is `BLOCKED`") | — | entry A, `Gate 13` | `no-change` | A dated measurement record |
| 10 | `docs/rag-extraction-research/01-current-mechanism.md` | — | entry A, `python-service.sh` | `no-change` | A dated research record of the tree as it stood |
| 11 | `docs/rag-extraction-research/07-extraction-plan.md` | — | entry A, `python-service.sh` | `no-change` | A dated research record, as row 10 |
| 12 | `docs/rag-extraction-research/reviews/01-current-mechanism.md` | — | entry A | `no-change` | A review of a dated research record, as row 10 |
| 13 | `docs/rag-extraction-research/reviews/04-engine-architecture.md` | — | entry A | `no-change` | A review of a dated research record, as row 10 |
| 14 | `docs/rag-extraction-research/reviews/07-extraction-plan.md` | — | entry A, `python-service.sh` | `no-change` | A review of a dated research record, as row 10 |
| 15 | `ROADMAP.md` → `## Scene products`, the `GraphScene` row ("The flow-graph navigation extracted from the harness … Open") | — | entry B, `GraphScene` | `change` | Task 5 — status to in progress, naming what has shipped and what is left |
| 16 | `ROADMAP.md` → the index row `\| 14 \| [GraphScene](#scene-products) \|` | — | entry B, `GraphScene` | `no-change` | An anchor link into the table; neither its number nor its target moves |
| 17 | `graphscene/README.md` (new) | — | entry B, after this branch's edits | `change` | Task 1 |
