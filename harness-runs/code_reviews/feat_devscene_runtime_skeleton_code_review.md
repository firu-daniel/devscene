# Code Review: feat_devscene_runtime_skeleton

## Context

**Branch:** `feat_devscene_runtime_skeleton`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`, 14 files:
- Task 1: the new `devscene-runtime/` package — `pyproject.toml`, the empty typed `devscene_runtime`, `tests/test_boundary.py` and `README.md`.
- Task 2: the `devscene-runtime` row in `scripts/python-service.sh`, `uv.lock` and `tests/test_graphscene_dependency.py`.
- Task 3: gate 13's legs 13h–13j in `scripts/run-gates.sh`, the `uv-audit` step in `.github/workflows/supply-chain.yml`, and the two `treeGuards` entries in `devscene.config.json`.
- Task 4: the third-row pins in `cli/test/python-service.test.mjs`.
- Task 5: `docs/development.md` and `ROADMAP.md`.

13 run-artifact files excluded from the reviewed diff.

**Headline conclusions.**
- **Accompanying items.** Every test the touched conventions documents require is present. `test_boundary.py` reads the package tree and registers itself as a tree guard (`devscene.config.json` → `treeGuards`, both covers). `test_graphscene_dependency.py` reads only fixed files and owes no entry.
- **Tests not run.** This review runs no suite. The Python files were checked by reading: no line over 100 characters, imports ordered, test functions annotated. Gate 13's legs 13h–13j in the Run gates phase are what grade lint, types and tests.
- **Pass 0 sweep.** `review-sweep.sh` exited `0`: no hits, so no findings.
- **Pass 0 caller check.** The diff adds no new exported symbol under any layer path. `devscene_runtime.__all__` is empty by design, and the other new names are test-local. No dead-feature finding.
- **Parity.** `phases.parity` is `false`, so no parity review ran.
- **Planning leads.** No `## Incidental findings (not gating)` lead exists in the planning rounds' folders.
- **Pass 2.** The per-unit findings root, `harness-runs/task_plan_point_reviews/feat_devscene_runtime_skeleton_task_plan/`, does not exist, so Pass 2 had nothing to reconcile.
- **The new package's layer.** `devscene.config.json` → `layers` has no `devscene-runtime` entry. The story plan's decision 7 and its **Manual setup required** steps leave that entry, the conventions document and the `.claude/CLAUDE.md` row as a step for after merge. Until then the package's files fall under the `general` catch-all. That is raised as a question to the maintainer, not as a finding.

What remains: two Should Fix items, both about the strength of the new package's own tests, and two Nice to Have items.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the committing role flips each one to `[x]` as that fix's commit lands. Each entry resolves to `harness-runs/code_reviews/feat_devscene_runtime_skeleton_code_review/finding_<K>.md` through its `**Finding K**` reference. The leading number is the fix order. `K` is the finding's stable identity.

1. [x] **Finding 4** — Name `devscene-runtime` in gate 13's no-pytest-cache sentence in `docs/development.md` _(layer: general)_
2. [x] **Finding 3** — Add a planted-manifest case for `allowed_names` / `_declared_dependencies` to `devscene-runtime/tests/test_boundary.py` _(layer: general)_
3. [x] **Finding 2** — Move the duplicated requirement-name parser into `devscene-runtime/tests/requirement_names.py` and import it in both test files _(layer: general)_
4. [x] **Finding 1** — Compare GraphScene's version specifiers, not only names, in the lock-staleness test _(layer: general)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The lock-staleness test compares dependency names only, so a GraphScene specifier change that was never re-locked passes 13j
→ [finding_1.md](feat_devscene_runtime_skeleton_code_review/finding_1.md)

### 2. The requirement-name parser is copied into both `devscene-runtime` test files
→ [finding_2.md](feat_devscene_runtime_skeleton_code_review/finding_2.md)

---

## Nice to Have

### 3. The boundary test never exercises its allowed-set derivation against a planted manifest
→ [finding_3.md](feat_devscene_runtime_skeleton_code_review/finding_3.md)

### 4. Gate 13's cache sentence in `docs/development.md` still lists only two packages as writing no pytest cache
→ [finding_4.md](feat_devscene_runtime_skeleton_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section is empty.
