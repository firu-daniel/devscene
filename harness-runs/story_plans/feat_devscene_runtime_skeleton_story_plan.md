# Story: `devscene-runtime/`, DevScene's own Python package, with its toolchain, gates and import boundary and no behaviour yet

## Context

This branch creates `devscene-runtime/`, DevScene's own Python runtime, at the repository root beside `graphscene/` and `docs-retrieval-service/`. Its import name is `devscene_runtime`. It holds no behaviour. It holds the package manifest, an empty typed package, an import-boundary test, a dependency test that proves `graphscene` resolves from the package's own environment, a README, the package's row in `scripts/python-service.sh`'s table with its `uv.lock`, gate 13's three new legs, the nightly audit of its lock, its tree-guard registration, the `cli` suite that pins the wrapper's new row, and the documentation of all of it. Part of #376. Issue #418 then builds the harness's walker host in this package; this branch exists so that #418's code lands under a layer of its own rather than under the catch-all `general` layer. `graphscene` went the same way (#412, then #430), and this plan follows `harness-runs/story_plans/feat_graphscene_package_skeleton_story_plan.md`'s shape: package, wrapper row with its lock, gate legs, the `cli` pin, then documentation.

**The decisions this plan takes.** The prompt's leads are starting points. These are what the plan holds to:

1. **The package is `devscene-runtime/`, set up like `graphscene/`.** The distribution is `devscene-runtime` and the import package `devscene_runtime`, in a `src/` layout, `hatchling`-built, Python `>=3.11`. It uses the same `ruff`, strict `mypy` and `pytest` settings as `graphscene/pyproject.toml` (`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `-p no:cacheprovider` included), with a `dev` group of `ruff`, `mypy` and `pytest`. There is no `import-linter`, no `[tool.importlinter]` contract and no internal layer folder: the task prompt rules them out for the skeleton, and #418 decides the internal structure. No console script, no compose file. It is not part of the npm package (`cli/package.json` → `files` names neither it nor `graphscene/`). Task 1.
2. **Its one runtime dependency is `graphscene`, reached as an editable `uv` path dependency on `../graphscene`.** `[project] dependencies = ["graphscene"]` and `[tool.uv.sources] graphscene = { path = "../graphscene", editable = true }`. Editable, so the package's environment always reads the sibling checkout's current `graphscene/src/graphscene/` rather than a copy built at sync time: `uv run --frozen --no-sync` never re-syncs, so a non-editable copy would go stale silently on the next GraphScene change. No release is needed while both live here. Task 1 declares it; Task 2 locks it.
3. **The boundary.** `devscene_runtime` imports only the standard library, itself and its declared runtime dependencies, and reaches `graphscene` through its public surface only: `import graphscene` / `from graphscene import <name in graphscene.__all__>`, never `graphscene.engine`, `graphscene.facade` or any other submodule. `devscene-runtime/tests/test_boundary.py` enforces it, the counterpart of `graphscene/tests/test_boundary.py`, which already refuses any `devscene*` import under `graphscene/src/` and is not changed. GraphScene never imports this package. Task 1.
4. **The lock is coupled to GraphScene's declared dependencies, and a test says so.** `devscene-runtime/uv.lock` pins `graphscene`'s own runtime dependencies (today `jsonschema`) as resolved through the path source. A later change to `graphscene/pyproject.toml` → `[project] dependencies` leaves that lock stale, and `uv sync --frozen` installs the stale set without complaint. `devscene-runtime/tests/test_graphscene_dependency.py` compares the lock's `graphscene` entry against `graphscene/pyproject.toml`, offline, so gate 13's `13j` fails on the first GraphScene dependency change that did not re-lock this package. The same file proves the lead's run-copy question: `import graphscene` from this package's environment resolves to this checkout's own `graphscene/src/graphscene/`. Task 2.
5. **The gates are gate 13's legs 13h–13j**, `lint`, `typecheck` and `test` with `--package devscene-runtime`, on the existing `BLOCKED` grading, so `docs/development.md` § 5's count of sixteen gates, nine unattended, still holds. `commands.typecheck` picks the package up with no edit, because `scripts/typecheck.sh` runs `bash scripts/python-service.sh check`, which iterates the wrapper's table. Task 3 adds the legs, Task 5 documents them.
6. **Where the package reads the repository from is not settled here.** No code in this branch reads the repository, and the task prompt allows the skeleton to leave it. The first reader — #418's walker host — chooses between a bare `git rev-parse --show-toplevel` and an argument, with code that uses it. Nothing in this branch writes a promise about it.
7. **The layer is a manual action owed after merge**, as #430 did for `graphscene`: a `devscene-runtime` entry in `devscene.config.json` → `layers`, its conventions document through `/devscene:analyze`, and its `.claude/CLAUDE.md` row. None of that is work a run plans (`.claude/` is refused by the tool layer, and a conventions document is never a target). The run reports it as an `undescribed-layer` staleness entry, and the steps are under **Manual setup required** below. #418 is queued only after that.

**What no unit runs.** `## The test-run rule` forbids a gate script or a test file outside a unit's own, and this run copy's environment holds no `devscene-runtime` row until the lock exists and `provision` has run. Tasks 1 and 2 therefore write Python that satisfies the house settings by construction, and their evidence is gate 13's legs 13h–13j in the Run gates round. Those legs grade `BLOCKED`, not failed, until this run copy is provisioned with the new row — the first manual step below does that at Task 2's park.

**Ship order.** The three `general` tasks come first, because they create what is pinned: the package (Task 1), its wrapper row, lock and dependency test (Task 2), and the gate legs, the nightly audit step and the tree-guard registration (Task 3). The `cli` suite that pins the wrapper's third row follows (Task 4), against the configured layer order, because a suite cannot pin a table row that does not exist yet — the order `feat_graphscene_package_skeleton` used for the same pair. The catch-all documentation task comes last (Task 5).

**Top risks:**

- **The lock.** `uv lock` reaches PyPI and writes the shared `uv` cache, and the run's sandbox is expected to refuse both. A branch merged with the `devscene-runtime` row and no `devscene-runtime/uv.lock` makes `provision`'s `uv sync --frozen` fail for that row, and so the bootstrap of every later run copy. Task 2 owns the row and the lock together, and returns a blocker naming the manual step rather than landing the row alone.
- **A boundary test that passes vacuously**, because the real package imports nothing from `graphscene` yet. Task 1's planted case per clause, each asserting its exact violation line, and its real-tree assertion that `src/devscene_runtime/__init__.py` is among the files visited, guard it.
- **An editable install that resolves the wrong GraphScene** — another checkout's, or a copy that does not track the source. Task 2's dependency test asserts the resolved `graphscene/__init__.py` is this checkout's own file, and gate 13's `13j` runs it in this run copy.

**Manual setup required:**

- **When Task 2 parks on the lock** (expected in a sandboxed run), run these two commands, one after the other, from an ordinary unsandboxed terminal at the run copy's root, then resume the run. Depends on Task 2.

  ```
  bash scripts/python-service.sh --package devscene-runtime lock
  ```

  ```
  bash scripts/python-service.sh provision
  ```

  The first writes `devscene-runtime/uv.lock`, which Task 2 then commits. The second syncs every row, so that the Run gates round grades 13h–13j rather than reporting them `BLOCKED`.
- **After this branch merges**, run this once in the main checkout and in any working copy made by hand, from an unsandboxed terminal, so that a hand run of the gates grades 13h–13j. Run copies get it at bootstrap. Depends on Task 2.

  ```
  bash scripts/python-service.sh provision
  ```

- **After this branch merges**, add the `devscene-runtime` layer, before #418 is queued. Depends on Task 1.
  1. Run `/devscene:analyze` in this repository, answering `skip` for every document that is already filled. Never use the `--yes` spelling. This writes the new layer's conventions document.
  2. Add the layer with `npx devscene config set layers`, with name `devscene-runtime` and path `devscene-runtime`.
  3. Add its row to `.claude/CLAUDE.md`'s `## Context files (read on demand)` table by hand, and name the third package in that file's **Python packages sit beside the two halves** paragraph.

  Until this is done, a unit that changes `devscene-runtime/src/` is a `general`-layer unit, and the tree guard Task 3 registers is run through that layer's test-file command, which cannot run a `pytest` file.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none — so in an index a run is iterating, an implementer never changes a marker here and never edits any other line of this section. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational progress markers for the implementer; they are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_devscene_runtime_skeleton/task_<K>_plan.md` file.

1. [x] **Task 1** — Create the `devscene-runtime/` package: manifest with the `graphscene` path dependency, empty typed `devscene_runtime`, its import-boundary test and README _(layer: general)_ _(points: 20)_
2. [x] **Task 2** — Add `devscene-runtime` to `scripts/python-service.sh`'s package table, lock the package, and test that `graphscene` resolves and the lock tracks it _(layer: general)_ _(points: 15)_
3. [ ] **Task 3** — Add gate 13's legs 13h–13j, the nightly `uv audit` step for the new lock, and the boundary test's tree-guard entry _(layer: general)_ _(points: 10)_
4. [ ] **Task 4** — Pin the `devscene-runtime` row, its refusals and the three-row `provision` and `check` in `cli/test/python-service.test.mjs` _(layer: cli)_ _(points: 15)_
5. [ ] **Task 5** — Document gate 13's `devscene-runtime` legs and its audited lock in `docs/development.md`, and record the package in `ROADMAP.md` _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"`feat_devscene_runtime_skeleton` creates `devscene-runtime/`, DevScene's own Python package, with its toolchain, gates and import boundary, and no behaviour yet."* The corpus sites are every durable document that describes gate 13 or the Python wrapper's package table, the harness-side package, the set of Python packages, or the audited Python locks.

**Derivation entry A — gate 13 and the wrapper (command).** Re-run verbatim from the repository root: `git grep -lE 'python-service\.sh|[Gg]ate 13|\b13[e-g]\b' -- '*.md' '*.yml' ':!harness-runs'`

**Derivation entry B — the harness-side package (command).** Re-run verbatim from the repository root: `git grep -lniE 'harness-side (package|distribution|code)|devscene-prefixed distribution|devscene-prefixed' -- '*.md' ':!harness-runs'`

**Derivation entry C — the set of Python packages (command).** Re-run verbatim from the repository root: `git grep -lniE 'python packages|python layers' -- '*.md' ':!harness-runs'`

**Derivation entry D — the audited locks (command).** Re-run verbatim from the repository root: `git grep -lE 'uv\.lock' -- '*.md' '*.yml' ':!harness-runs'`

**Derivation entry E — standing-artifact rows (procedure).**
- **First step, runnable:** `grep -niE 'python-service|gate 13|graphscene|[^a-z]uv[^a-z]|devscene-runtime|harness-side' harness-runs/lessons.md harness-runs/improvement_suggestions.md`
- **Artifact:** the two standing ledgers under the state directory, `harness-runs/lessons.md` and `harness-runs/improvement_suggestions.md`.
- **Traversal:** each ledger's headings in file order, then the one-line entries under each.
- **Decision rule:** an entry is reached when its rule text — not its `_(taught by: …)_` attribution — names gate 13, `python-service.sh`, `uv`, GraphScene or a harness-side package.

When this plan was written, the procedure's first step matched one line, `harness-runs/lessons.md`'s shim rule, on its attribution `feat_graphscene_graph_model` only, so the decision rule reaches no entry and the procedure contributes no row.

**Closure invariant:** every site any derivation entry reaches appears as a row below. After the branch's edits, each command's output is still ⊆ the files named in the rows.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## The stack, in the words the rules below use` ("The Python layers — `docs-retrieval-service/` and `graphscene/`"), `## Shared code, and where it lives` ("share a toolchain runner … and no code"), `## The layers` and `### Where a new responsibility goes` (the harness-side distribution rows) | — | entries A, B, C, D | `no-change` | A conventions document is never a target. The branch's work falsifies the two-package list and "no code" (`devscene-runtime` depends on `graphscene` by path), and gives the harness-side row a home; recorded as a `stale-rule` entry in `corpus_staleness` |
| 2 | `.claude/context/graphscene.md` → `## What it may depend on`, `## What accompanies a new module` ("A new runtime dependency lands with …") and `## Tests` (legs `13e`–`13g`) | — | entries A, B, D | `no-change` | A conventions document is never a target. The dependency bullet no longer lists everything a new GraphScene runtime dependency needs — `devscene-runtime/uv.lock` must be re-locked too; recorded as a `stale-rule` entry in `corpus_staleness`. The boundary and the legs it names stay true |
| 3 | `.claude/context/docs-retrieval.md` (its `python-service.sh` commands and `uv.lock`) | — | entries A, D | `no-change` | A conventions document; describes only that package's own route and lock, both unchanged under the default package |
| 4 | `.claude/CLAUDE.md` → **Python packages sit beside the two halves** paragraph | — | entry C | `no-change` | Under `.claude/`, which the tool layer refuses; naming the third package there is the third manual-setup step |
| 5 | `.claude/review-sweep.md` → its closing `_Written by …_` line | — | entry C | `no-change` | An attribution line recording what a past sweep read |
| 6 | `ROADMAP.md` → `## Scene products`, the `GraphScene` row ("Left: the walker's port onto the engine, and the harness-side package; …") | — | entries A, B, D | `change` | Task 5 — names the harness-side package's skeleton as shipped and leaves the walker's port on the left |
| 7 | `ROADMAP.md` → the `Nightly supply-chain audit` row ("the Python service's `uv.lock`") | — | entry D | `no-change` | Records what that row shipped; the audited set of record is `docs/development.md`'s `uv-audit` table row (row 13), which Task 5 changes |
| 8 | `docs/development.md` → **Gate 13 — the Python packages.** paragraph ("`docs-retrieval-service/` through 13a–13d and `graphscene/` through 13e–13g"; "Every unit runs 13a, 13b, 13e and 13f's checks too") | — | entries A, C | `change` | Task 5 — adds `devscene-runtime/` through 13h–13j and its two unit-run checks |
| 9 | `docs/development.md` → the gate 13 closing paragraph ("`graphscene` is that second row; it has no console script and no compose project") | — | entry A | `change` | Task 5 — names `devscene-runtime` as the third row, with the same refusals and its editable path dependency |
| 10 | `docs/development.md` → § 5's opening paragraph "Nine of the sixteen run unattended" ("Gate 13 is reported on the same terms in two ways") | — | entry A | `no-change` | Its count and its `BLOCKED` / `SKIPPED` terms are unchanged: the new legs grade `BLOCKED` on the same condition, and 13d stays the only container leg |
| 11 | `docs/development.md` → the `scripts/typecheck.sh` bullet ("since gates 16 and 13 added two hand-written steps to it") | — | entry C | `no-change` | `check` iterates the wrapper's table, so the step is unchanged |
| 12a | `docs/development.md` → **Gate 3**'s format-4 paragraphs (leg `13g` running `graphscene/tests/facade/test_loading.py`, `test_vocabulary.py`, `test_references.py` and `test_static_check.py`) | — | entry A | `no-change` | Which leg runs which GraphScene suite is unchanged |
| 12b | `docs/development.md` → gate 6a's paragraph (the skipped tool-cache directories) | — | entry A | `no-change` | `devscene-runtime`'s `pyproject.toml` (Task 1) carries `-p no:cacheprovider` too, and its `.venv`, `.ruff_cache` and `.mypy_cache` are the same names, so the skipped set still covers every package |
| 12c | `docs/development.md` → the `probe` example (`bash scripts/python-service.sh --package graphscene probe …`) | — | entry A | `no-change` | It is one valid spelling of the package-selected form, and stays one |
| 13 | `docs/development.md` → § 8's job table, the `uv-audit` row ("Every package `docs-retrieval-service/uv.lock` or `graphscene/uv.lock` pins") | — | entry D | `change` | Task 5 — adds `devscene-runtime/uv.lock` to the audited set Task 3's step audits |
| 14 | `docs/development.md` → the dated audit table's row **C** `docs-retrieval-service/uv.lock` | — | entry D | `no-change` | A dated measurement record |
| 15 | `.github/workflows/supply-chain.yml` → its header ("vulnerabilities in docs-retrieval-service/uv.lock and graphscene/uv.lock") and the `uv-audit` job's steps | — | entry D | `change` | Task 3 — adds the `devscene-runtime` step and names its lock in the header |
| 16 | `graphscene/README.md` (`## The boundary`, `## Running the toolchain`, `## Gating`) | — | entry A | `no-change` | Its boundary ("harness-specific code … goes in its own distribution outside `graphscene/`, named with a `devscene` prefix") is what this branch obeys, and it is the extractable library's own document, which names no harness package |
| 17 | `docs-retrieval-service/README.md` (its setup paragraph and `## Testing`) | — | entry A | `no-change` | Describes that package's own legs, whose commands keep their meaning under the default package |
| 18 | `docs/cli.md` → the `docs-retrieval-service/tests/test_launcher_e2e.py` bullet | — | entry A | `no-change` | Which leg runs which case is unchanged |
| 19 | `docs/retrieval-eval.md` | — | entry A | `no-change` | Its commands keep their meaning under the default package |
| 20 | `docs/retrieval-eval-results.md` | — | entry A | `no-change` | Measured records of past runs |
| 21 | `docs/sandbox-verification.md` → the 2026-10-14 unsandboxed run | — | entry A | `no-change` | A dated measurement record |
| 22 | `evals/docs-retrieval/README.md` → the `python-backend.mjs` row | — | entry A | `no-change` | The route it names is unchanged under the default package |
| 23 | `docs/rag-extraction-research/01-current-mechanism.md` | — | entries A, D | `no-change` | A dated research record of the tree as it stood |
| 24 | `docs/rag-extraction-research/03-sources-database-security.md` | — | entry D | `no-change` | A dated research record, as row 23 |
| 25 | `docs/rag-extraction-research/07-extraction-plan.md` | — | entries A, D | `no-change` | A dated research record, as row 23 |
| 26 | `docs/rag-extraction-research/reviews/01-current-mechanism.md` | — | entries A, D | `no-change` | A review of a dated research record, as row 23 |
| 27 | `docs/rag-extraction-research/reviews/03-sources-database-security.md` | — | entry D | `no-change` | A review of a dated research record, as row 23 |
| 28 | `docs/rag-extraction-research/reviews/04-engine-architecture.md` | — | entry A | `no-change` | A review of a dated research record, as row 23 |
| 29 | `docs/rag-extraction-research/reviews/07-extraction-plan.md` | — | entry A | `no-change` | A review of a dated research record, as row 23 |
| 30 | `devscene-runtime/README.md` (new) | — | entries A and D, after this branch's edits | `change` | Task 1 |
