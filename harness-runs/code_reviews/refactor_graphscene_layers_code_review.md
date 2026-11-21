# Code Review: refactor_graphscene_layers

## Context

**Branch:** `refactor_graphscene_layers`
**Date:** 2026-11-21
**Reviewed:** the whole diff from `origin/dev` to the branch tip. This checkout has no local `dev`, so the review used `origin/dev`. The diff covers:
- the move of GraphScene's flat modules into the `model`, `engine`, `adapters` and `facade` subpackages, with `loader.py` split into `adapters/schema.py`, `adapters/json_file.py` and `facade/loading.py`, and `model.py` split into `model/flow_graph.py` and `adapters/builder.py` (Task 1);
- the two `import-linter` contracts in `graphscene/pyproject.toml` and `graphscene/tests/test_layers.py`, which runs them (Task 2);
- the layer table and rules in `graphscene/README.md` (Task 3);
- the repointed paths in `docs/development.md` and `docs/flow-graph-walker.md`, and the two `treeGuards` entries for `tests/test_layers.py` in `devscene.config.json` (Task 4).

14 run-artifact files were left out of the reviewed diff.

**Headline.**
- **Public surface:** unchanged. The root `__init__.py` re-exports from `graphscene.facade` only. `__all__` is the same list, name for name and in order, and `tests/test_public_surface.py` pins it. `_DEFINED_IN` now names the new defining modules.
- **Import direction:** no module under `graphscene/src/graphscene/` imports from the package root. `engine` and `adapters` import only `model` and the standard library, plus `jsonschema` in `adapters/schema.py`. Only `facade` combines them.
- **Translator:** the ECMA-262 pattern translator moved into `adapters/schema.py` unchanged, so the lessons-ledger rule about a shim's supported constructs and refusals still holds.
- **Tests:** every moved test kept its *"The rule this file exists to enforce"* docstring, now naming the new module. Every test that moved down a directory reads its fixtures from `Path(__file__).parents[1]`. Each test subdirectory has an `__init__.py`. `test_layers.py` covers each clause with a planted case that asserts the exact report text, plus one clean planted package and one run against the real package with no cache.
- **Tree-guard registration:** `test_layers.py` reads the package tree, and its `treeGuards` entries are in the branch diff. The entry's `test` path resolves under the `graphscene` layer path, as `doctor`'s `tree-guards` check resolves it.
- **No dead code:** Pass 0 half (b) found two new public functions, `read_json_file` and `schema_violations`. Both are called from `graphscene/src/graphscene/facade/loading.py`.
- **Not run:** this review ran no test suite and no typecheck. Whether they pass is for the Run gates phase to establish.

**Pass 0 sweep:** `review-sweep.sh` exited `0` with 0 hits, so no finding came from it. Parity is not applicable: `phases.parity` is `false`.

**Planning-round lead:** `harness-runs/task_plan_reviews/refactor_graphscene_layers/review_0.md` and `review_1.md` raised the `treeGuards` entry `test/no-container-home-paths.test.mjs` covering `**/*.md`. A `graphscene` unit that edits Markdown selects that entry and would run it through the Python single-file command. That entry is not in this branch's diff, so it is not a branch finding.

**Scope-register rows 9–11:** `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` (`_NEGATIVES` in `graphscene/tests/test_vocabulary.py`) and `.claude/context/graphscene.md` → `## Tests` (the fixtures bullet) still name the flat test paths. They are conventions documents, so this run cannot edit them, and they are raised in the return as a decision for the user rather than as a finding.

**Pass 2:** the per-unit findings root, `harness-runs/task_plan_point_reviews/refactor_graphscene_layers_task_plan/`, does not exist, so Pass 2 had nothing to reconcile.

One finding remains, a Nice to Have.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Parametrize the planted-violation cases in `tests/test_layers.py` so each contract clause is its own collected case _(layer: graphscene)_

---

## Must Fix

_None._

---

## Should Fix

_None._

---

## Nice to Have

### 1. `test_a_planted_violation_breaks_its_contract` runs all eight planted clauses in one test, so the first failing clause hides the rest
→ [finding_1.md](refactor_graphscene_layers_code_review/finding_1.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

_Empty: `phases.parity` is `false`, so there is no reference implementation to diverge from._
