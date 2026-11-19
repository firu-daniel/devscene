# Code Review: feat_graphscene_package_skeleton

## Context

**Branch:** `feat_graphscene_package_skeleton`
**Date:** 2026-11-19
**Reviewed:** the whole branch diff against `origin/dev`. This review was two-pass mode, but Pass 2 was a no-op: the supplied `per_task_findings_root`, `harness-runs/task_plan_point_reviews/feat_graphscene_package_skeleton_task_plan/`, does not exist, so there were no per-unit findings to carry over. The diff covers 11 files:
- the new `graphscene/` package: `pyproject.toml`, `uv.lock`, the empty typed `src/graphscene/`, `tests/test_boundary.py` and `README.md` (Task 1, Task 2's lock);
- the `graphscene` row and the `run` / `container-test` refusals in `scripts/python-service.sh` (Task 2);
- gate 13's new legs 13e–13g in `scripts/run-gates.sh` (Task 3);
- `cli/test/python-service.test.mjs` (Task 4);
- `docs/development.md` and `ROADMAP.md` (Task 5).

15 run-artifact files were excluded from the reviewed diff.

**Headline conclusions:**
- **Tests.** Every accompanying test the conventions documents require is present: the `cli` suite pins the new row, both refusals and the two-row `provision`. The new package ships its own boundary test. This review ran no suite; whether the tests pass is the Run gates phase's to establish, including gate 13's legs 13e–13g.
- **Pass 0 sweep.** `review-sweep.sh` exited `0` with 0 hits, so 0 findings came from it. The new-exported-symbol caller check found no new exported symbol under any layer path: `graphscene/src/graphscene/__init__.py` exports `__all__: list[str] = []`, and the `cli` change adds only a module-local constant.
- **Parity.** Not applicable: `phases.parity` is `false`.
- **What holds.** The package's `ruff`, `mypy` and `pytest` settings match `docs-retrieval-service/pyproject.toml`. The root `.gitignore` already covers `graphscene/.venv`, `.ruff_cache`, `.mypy_cache` and `__pycache__` (checked with `git check-ignore`). The gate-13 retitle reached every live `.sh` and `.md` site the scope register named.
- **Findings.** No finding is a Must Fix. The three Should Fix items are:
  - `sync --with-models` is the one row-specific sub-command the new row does not refuse;
  - the nightly `uv-audit` job does not cover the new lockfile;
  - the boundary test's dependency rule has no planted case.

  One Nice to Have is a docstring gap.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Name the unrecognised dynamic-import forms in the boundary test's "Deliberately not covered" list _(layer: general)_
2. [x] **Finding 3** — Add a planted `pyproject.toml` case for the boundary test's dependency rule and PEP 508 name parsing _(layer: general)_
3. [x] **Finding 1** — Refuse `sync --with-models` with exit 2 on a row that has no `models` extra, and pin it in the `cli` suite _(layer: cli, general)_
4. [ ] **Finding 2** — Audit `graphscene/uv.lock` in the nightly `uv-audit` job and document it in §8 _(layer: general)_

---

## Must Fix

None.

---

## Should Fix

### 1. `sync --with-models` under `--package graphscene` is not refused, although the row has no `models` extra
→ [finding_1.md](feat_graphscene_package_skeleton_code_review/finding_1.md)

### 2. The nightly `uv-audit` job does not audit the new `graphscene/uv.lock`
→ [finding_2.md](feat_graphscene_package_skeleton_code_review/finding_2.md)

### 3. The boundary test's dependency rule and its PEP 508 name parsing have no planted case
→ [finding_3.md](feat_graphscene_package_skeleton_code_review/finding_3.md)

---

## Nice to Have

### 4. The boundary test's "Deliberately not covered" list omits the dynamic-import forms its scanner cannot see
→ [finding_4.md](feat_graphscene_package_skeleton_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None. `phases.parity` is `false`, so there is no reference implementation to diverge from.
