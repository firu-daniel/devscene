# Story: Rename `devscene-runtime/` to `devscene-flow-host/` and narrow it to the harness's GraphScene host

## Context

This branch renames the Python package at `devscene-runtime/` to `devscene-flow-host/` (distribution `devscene-flow-host`, import name `devscene_flow_host`). It also narrows what the package may hold to **the harness's GraphScene host**: the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks, and the commands over it. Any other DevScene Python integration gets its own `devscene`-prefixed package. The package's `README.md` → `## What it is` is where that rule is stated. **No behaviour changes**: the package still holds only its skeleton, an empty `__all__`, its boundary test and its dependency test. Only live files move. Merged commits, closed issues and everything under `harness-runs/` keep the old name.

**What the run cannot do, and who does it instead.** Each item below was checked against the file that owns it:

- **The lock.** `uv.lock` is re-made only by `bash scripts/python-service.sh --package devscene-flow-host lock`, never edited by hand (`.claude/context/devscene-runtime.md` → `## What it may depend on`). That sub-command *"reaches the network"*, and inside a run's sandbox it *"fail[s] closed (no network, the shared `uv` cache not writable)"* (`scripts/python-service.sh` header → `lock` and `WHO RUNS lock, sync AND provision`). Task 1 therefore moves `uv.lock` byte for byte, and its root entry `name = "devscene-runtime"` stays stale until the maintainer re-locks (manual step 1 below).
- **The environment.** The run copy's environment was provisioned under `devscene-runtime/.venv` before Task 1 ran. A virtual environment is not relocatable, and a run never syncs its copy's environment. So from Task 1 onward, every `--package devscene-flow-host` leg in this run (the per-unit test runs, `commands.typecheck`'s `check`, and gate 13h–13j) exits `3` and is graded **`BLOCKED`, not passed** (`docs/development.md` → **Gate 13**). The Python edits are graded only by the static checks each task names, and then by the maintainer's provisioned run (manual step 3). Task 1 leaves the ignored `devscene-runtime/.venv`, `.ruff_cache` and `.mypy_cache` where they are. No tracked file sits beside them, and gate 6a skips them. For the same reason, Task 1 moves the eight tracked files one at a time and never `git mv`s the directory itself. A directory rename would carry the environment into `devscene-flow-host/.venv`, where its scripts' shebangs still point at the old path. Each leg would then *fail* rather than grade `BLOCKED`.
- **The workflow push.** `.github/workflows/supply-chain.yml` names the package. `push-branch.sh` refuses any unattended push whose commits change a path under `.github/workflows/` (`cli/templates/scripts/push-branch.sh` → `NO UNATTENDED PUSH CHANGES A WORKFLOW FILE`). So Task 5 ships last: once its commit lands, the run's push is refused, the run parks and asks the maintainer to push, and it resumes once the maintainer answers that the push is done. No task tries to push it or works around the refusal.
- **`.claude/**` and the `layers` row.** A run cannot write under `.claude/`, and the layer profile changes only through `devscene config set`. Every `.claude/` site that names the old package is recorded as `no-change` in the register below and is handed to the maintainer's after-merge steps. The two conventions documents are also reported as `stale-rule` entries.

**Task cut, and why the order is not the configured layer order.** Five tasks:

- **Task 1** moves and renames the package. It also updates the one script whose package table must name the new directory in the same commit: `scripts/python-service.sh` (`PACKAGES`, `package_row`). With the old row left in place, `commands.typecheck`'s `check` would run `--package devscene-runtime` legs against a directory with no `pyproject.toml`.
- **Task 2** updates `cli/test/python-service.test.mjs`, which asserts that table.
- **Task 3** points the two `treeGuards` entries at the new paths.
- **Task 4** updates the gate legs and the documentation of record.
- **Task 5** updates the workflow file and is the task that parks the run.

The configured order puts `cli` ahead of `general`. Here, though, the `cli` task tests a script the catch-all layer owns, so the producer (Task 1) must land first. `## The order files are created` in `.claude/context/conventions.md` says it directly: *"Contract before consumer, always"*. No task depends on a later one.

Task 1 is a catch-all (`general`) task, though half of what it touches sits under the `devscene-runtime` layer's path. A `git mv` cannot be split by layer. Only the catch-all dispatch has every layer path in scope, and the destination `devscene-flow-host/` is covered by no layer but the catch-all until the maintainer's `layers` step.

**The `treeGuards` question the task prompt raised.** A Run gates round does not read `treeGuards`. Only a unit's guard step does (`unit_loop_core.md` → `## The test-run rule` point 7), as does `doctor`, which checks only that each `test` value resolves (`cli/src/doctor/checks.ts` → `treeGuardTestResolves`). A `covers` glob naming a path that no longer exists fails nothing: it never matches a changed path, so the guard is silently never selected. That is why Task 3 moves both `covers` values to the new paths on this branch instead of leaving them to the maintainer. GraphScene's own boundary test needs no change. Its rule (c) flags any top-level import name starting with `devscene` (`graphscene/tests/test_boundary.py` → `_FORBIDDEN_PREFIX = "devscene"`), and `devscene_flow_host` starts with that prefix.

**Wording constraint on every task** (`harness-runs/lessons.md` → `## Adopter-facing documentation`, the rename lesson): no live file this branch writes says that a name changed, or names the old name as a former one. Each site is rewritten to read as if the package had always been called `devscene-flow-host`.

**Top risks:** First, a Python edit that breaks lint, type checking or the boundary test can pass unnoticed, because every `devscene-flow-host` leg grades `BLOCKED` in this run. Task 1 guards it with greps for leftover old names and a 100-column check on the lines it lengthens, and manual step 3 runs the real gate 13h–13j on a provisioned checkout before merge. Second, the stale root entry in the moved `uv.lock` makes every `uv sync --frozen` of the package fail once someone provisions it. Task 1 leaves the lock untouched rather than hand-editing it, and manual step 1 re-locks it at the park, before the push. Third, a site left naming the old directory, such as a gate leg or a workflow step, would fail only after merge. The scope register below lists every such site with its owning task, and each task's verification re-runs the grep over its own files.

**Manual setup required:**

1. **At the park after Task 5, before pushing:** in the branch's checkout, from the repository root and outside any sandbox, re-make the lock (depends on Task 1). Then commit only `devscene-flow-host/uv.lock`:

   ```
   bash scripts/python-service.sh --package devscene-flow-host lock
   ```
2. **Still at that park:** push the branch yourself, since the run's push of the Task 5 workflow commit is refused (depends on Task 5). Then answer the park that the push is done.
3. **Before merge, on a checkout of your own (never the run copy):** provision, then run gate 13h–13j, which this run could only grade `BLOCKED` (depends on Tasks 1 and 4):

   ```
   bash scripts/python-service.sh provision
   ```

   ```
   bash scripts/python-service.sh --package devscene-flow-host lint
   ```

   ```
   bash scripts/python-service.sh --package devscene-flow-host typecheck
   ```

   ```
   bash scripts/python-service.sh --package devscene-flow-host test
   ```
4. **After merge:** run `devscene config set layers` with the renamed row (`name: devscene-flow-host`, `path: devscene-flow-host`, `conventions: .claude/context/devscene-flow-host.md`), plus a `detection.review` record (depends on Task 1).
5. **After merge:** rename `.claude/context/devscene-runtime.md` to `.claude/context/devscene-flow-host.md` and replace the old name inside it. Replace it as well in `.claude/CLAUDE.md` (the Python-packages paragraph and the routing row), in `.claude/context/conventions.md`, and in `.claude/review-sweep.md` (the "GraphScene reached below its public surface" row's `Covers` and `Exempts`, its line in the exempt-site list, and the two non-row lines that name the package). In `.claude/context/conventions.md` → `## The layers`, add the cross-layer clause, worded so it holds after #419: adopters never import the package, and only the scripts `init` writes launch it. Drop the `## Not determined` entry the new README settles. Optionally, run `/devscene:analyze devscene-flow-host` afterwards (depends on Tasks 1–5).
6. **Optional tidy-up, outside any run:** delete the untracked, ignored `devscene-runtime/` remnant (`.venv`, `.ruff_cache`, `.mypy_cache`) in any checkout that had provisioned it.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom. **Only the committing role flips a marker to `[x]`**: in every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`; in the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational progress markers only. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/chore_rename_devscene_runtime/task_<K>_plan.md`. The ship order is by dependency, producer before consumer, with the catch-all layer's documentation and workflow tasks last (see `## Context` for why the `cli` task follows Task 1).

1. [ ] **Task 1** — Move the package to `devscene-flow-host/`, rename it `devscene_flow_host` and narrow its stated scope _(layer: general)_ _(points: 20)_
2. [ ] **Task 2** — Point the Python-service test's third package row at `devscene-flow-host` _(layer: cli)_ _(points: 5)_
3. [ ] **Task 3** — Point the two `devscene.config.json` tree guards at the renamed package paths _(layer: general)_ _(points: 5)_
4. [ ] **Task 4** — Rename the package in gate legs 13h–13j, `docs/development.md` and `ROADMAP.md` _(layer: general)_ _(points: 15)_
5. [ ] **Task 5** — Rename the package in the supply-chain workflow, then park for the maintainer's push _(layer: general)_ _(points: 5)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"Historical text keeps the old name: merged commits, closed issues, `harness-runs/`. Only live files move."* Together with the decision it serves: *"**The package holds only the harness's GraphScene host** … The package's `README.md` → `## What it is` says so."*

**Derivation entry A — files naming the package (command).** Re-run verbatim from the repository root, against the tree this plan was written on:

```
git grep -l -i -E "devscene[-_ ]runtime|DevScene.s own Python runtime" -- . ':!harness-runs'
```

**Derivation entry B — files carrying the scope wording this branch narrows (command).** Re-run verbatim from the repository root:

```
git grep -l -E "DevScene.s meanings|devscene.-prefixed (distribution|package)" -- . ':!harness-runs'
```

**Derivation entry C — standing-artifact rows (procedure).** **First step, runnable:**

```
grep -n -E '^\| |^- \*\*' .claude/review-sweep.md harness-runs/lessons.md
```

- **Artifacts:** the review-sweep matrix `.claude/review-sweep.md` and the lessons ledger `harness-runs/lessons.md`.
- **Traversal:** each file in that order, then its table rows and its bold-led bullet rules in line order.
- **Decision rule:** a row or rule is reached when its text names the package directory, its import name or the phrase "DevScene's own Python runtime", case-insensitively. The ledger reaches none.

**Closure invariant:** every site entries A, B and C reach appears as a row below. Row 20 is an extra, confirmed site that none of them reaches.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/CLAUDE.md`: the Python-packages paragraph and the `devscene-runtime` routing row | — | A | `no-change` | `.claude/**` is not writable by a run; the maintainer's after-merge step 5 |
| 2 | `.claude/context/conventions.md`: `## The stack…`, `## The layers` (table row and both bullets), `### Where a new responsibility goes`, `## Shared code…`, `## The testing bar`, `## What accompanies…`, `## Not determined` | — | A, B | `no-change` | A conventions document is never a plannable target. The branch falsifies the rules that name the package and the "DevScene's meanings" scope, and settles the second-distribution entry under `## Not determined`, so this is recorded as a `stale-rule` entry in `corpus_staleness`; after-merge step 5 |
| 3 | `.claude/context/devscene-runtime.md` (whole document) | — | A | `no-change` | Conventions document, recorded as a `stale-rule` entry; renamed and rewritten by the maintainer in after-merge step 5 |
| 4 | `.claude/review-sweep.md` (file; its rows are 17–19) | — | A | `no-change` | `.claude/**` is not writable by a run; after-merge step 5 |
| 5 | `.github/workflows/supply-chain.yml`: the header comment and the `uv-audit` job's `working-directory: devscene-runtime` step | — | A | `change` | Task 5 |
| 6 | `ROADMAP.md`: the `GraphScene` row ("the harness-side package's skeleton at `devscene-runtime/`, DevScene's own Python runtime…") | — | A | `change` | Task 4 |
| 7 | `cli/test/python-service.test.mjs`: `RUNTIME` and the `provisioned devscene-runtime` expected line | — | A | `change` | Task 2 |
| 8 | `devscene-runtime/README.md` (whole file, `## What it is` narrowed) | — | A, B | `change` | Task 1 |
| 9 | `devscene-runtime/pyproject.toml`: `[project] name`, `description`, `[tool.hatch.build.targets.wheel] packages` | — | A | `change` | Task 1 |
| 10 | `devscene-runtime/src/devscene_runtime/__init__.py`: the module docstring | — | A, B | `change` | Task 1 |
| 11 | `devscene-runtime/tests/test_boundary.py`: the module docstring, `_PACKAGE_DIR`, `_STDLIB_AND_SELF` | — | A | `change` | Task 1 |
| 12 | `devscene-runtime/tests/test_graphscene_dependency.py`: `_RELOCK` | — | A | `change` | Task 1 |
| 13 | `devscene-runtime/uv.lock`: the root `[[package]]` entry `name = "devscene-runtime"` | — | A | `change` | Task 1 moves the file byte for byte. The content is re-made by the maintainer's re-lock (manual step 1), never by hand |
| 14 | `devscene.config.json` → `treeGuards`: the two `tests/test_boundary.py` entries' `covers` | — | A | `change` | Task 3 |
| 15 | `devscene.config.json` → `layers` (the `devscene-runtime` row) and `detection.review.rationale` | — | A | `no-change` | The layer profile changes only through `devscene config set`. The maintainer's after-merge step 4 writes the renamed row and a new `detection.review` record, which replaces the rationale; until then the row keeps routing the run as configured |
| 16 | `docs/development.md`: **Gate 13** (the leg list, 13h–13j, the `addopts` sentence, the third-row sentence and the re-lock block) and `## 8. The nightly supply-chain audit` (the `uv-audit` table row and its `once each from …` sentence) | — | A | `change` | Task 4 |
| 17 | `.claude/review-sweep.md`: the "GraphScene reached below its public surface" table row (`Covers`, `Exempts`) | — | C | `no-change` | `.claude/**` is not writable by a run; after-merge step 5 |
| 18 | `.claude/review-sweep.md`: the **GraphScene reached below its public surface** exempt-site bullet | — | C | `no-change` | As row 17 |
| 19 | `.claude/review-sweep.md`: the two bold-led bullets **A class with nothing to verify a regex against has no row.** and **A rule about a file's presence, position or absence…**, both naming the package | — | C | `no-change` | As row 17 |
| 20 | `graphscene/tests/test_boundary.py`: `_FORBIDDEN_PREFIX = "devscene"`, rule (c) | — | confirmed by reading; no entry reaches it | `no-change` | Rule (c) flags every `devscene`-prefixed top-level import, so `devscene_flow_host` is covered with no edit |
| 21 | `scripts/python-service.sh`: the header's table paragraph and `WHERE IT WRITES` paragraph, `PACKAGES` and the `package_row` case | — | A | `change` | Task 1 |
| 22 | `scripts/run-gates.sh`: the header's gate-13 sentence, the `13h`, `13i` and `13j` cases | — | A | `change` | Task 4 |
