# Test Fix Plan: feat_planning_driver_python_cutover — review_1 round 1

## Context

- **Branch:** `feat_planning_driver_python_cutover`
- **Log:** `harness-runs/test_run_logs/feat_planning_driver_python_cutover/review_1_round_1.log`
- **Summary:** The typecheck gate passed and the test gate failed on one check only, gate 6a (no machine paths), because the committed user-review fix plan names an absolute path under the home directory.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. `[ ]` markers anywhere else in this plan or its per-finding files are informational only.

1. [x] **Finding 1** — Replace the machine path in the user-review fix plan's `## Source observations` lead. _(layer: general)_

## Must Fix

### 1. Replace the machine path in the user-review fix plan's `## Source observations` lead

→ [finding_1.md](feat_planning_driver_python_cutover_review_1_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **typecheck gate:** exited 0. No failures.
- **test gate:** exited 1 (`run-gates: 1 failed, 30 passed`).
  - `6a no machine paths`: Finding 1. New this round (no earlier logs).
  - `13d Python container tests` and `14d zizmor over the rendered workflows` are reported `SKIPPED`. They are not failures, and no finding is raised for them.
