# Skeptic Review: feat_graphscene_package_skeleton

## Context

**Branch:** `feat_graphscene_package_skeleton`
**Date:** 2026-11-19
**Reviewed:** the whole branch diff against `origin/dev`. No local `dev` ref exists in this checkout, so `origin/dev` was the diff base. The diff covers 12 files: the new `graphscene/` package (`pyproject.toml`, `uv.lock`, `src/graphscene/__init__.py`, `py.typed`, `tests/test_boundary.py`, `README.md`), the `graphscene` row and its refusals in `scripts/python-service.sh`, gate 13's legs 13e–13g in `scripts/run-gates.sh`, the second `uv-audit` step in `.github/workflows/supply-chain.yml`, `cli/test/python-service.test.mjs`, `docs/development.md` and `ROADMAP.md`. 20 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/feat_graphscene_package_skeleton_code_review.md` and its four findings, all four applied on the branch. No parity review exists because `phases.parity` is `false`. No end-of-branch architecture review exists for this branch. The planning rounds under `harness-runs/task_plan_reviews/feat_graphscene_package_skeleton/` and `harness-runs/architecture_reviews/feat_graphscene_package_skeleton/` carry no `## Incidental findings (not gating)` section, so there were no leads to check. `harness-runs/lessons.md` has no entry on gate 13, the wrapper or GraphScene.

**What was checked and holds:**
- **Check 1, wiring.** Legs 13e–13g are wired into the round: they are in `gr_run_round`'s unit list and have `run_unit` arms. They are correctly absent from `GR_PREREQUISITES`, because none of them reads `cli/dist`. They are graded by `python_gate`, so a missing environment is reported `BLOCKED` and named in the closing line. `provision` syncs the new row because it loops over `PACKAGES`. `require_env` checks each package's own `<package>/.venv/pyvenv.cfg`. The boundary test's real-tree case asserts that `src/graphscene/__init__.py` is among the files it scanned. No other script enumerates gate ids or package directories: the sandboxed launcher, gate 6a's base-name exclusions and gate 6f's typos scope were all checked.
- **Check 2, runtime address.** The parity leg does not apply. The new `uv-audit` step's `working-directory: graphscene` resolves to the committed `graphscene/uv.lock`, which locks `graphscene` as `editable = "."`.
- **Check 3, citations.** Every anchor the new text cites resolves: `docs/development.md` → `## 5. Verifying a change`, `scripts/python-service.sh` → `WHERE IT WRITES`, and `tests/test_boundary.py` from the package docstring. The story's claims check out against the tree: the gate count stays at sixteen with nine unattended, the package is not in the npm `files`, and the three legs have no `cli/dist` dependency.
- **Check 4.** No divergence is marked intentional.

**Headline:** no Must Fix. One Should Fix, which none of the committed reviews raised: rule (b) of the boundary test flags a *relative* dynamic import, a form the static path deliberately accepts.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Skip a relative dynamic import in the boundary test's rule (b), as the static path already skips a relative `from` import _(layer: general)_

---

## Must Fix

None.

---

## Should Fix

### 1. The boundary test flags a relative dynamic import as an outside import with an empty name
→ [finding_1.md](feat_graphscene_package_skeleton_skeptic_review/finding_1.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None. `phases.parity` is `false`, and no divergence on this branch is marked intentional.
