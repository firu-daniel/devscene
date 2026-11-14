# Test Fix Plan: feat_parallel_plan_reviews — task round 1

## Context

- **Branch:** `feat_parallel_plan_reviews`
- **Log:** `harness-runs/test_run_logs/feat_parallel_plan_reviews/task_round_1.log`
- **Summary:** The typecheck gate passed; the test gate failed on exactly one sub-gate, 6f (`shipped files pass typos`), because `typos` flags the local variable `fo` that Task 3 introduced in `record_in_set()` of `cli/templates/scripts/flow-walker.sh`, at four sites.

The log also reports 13a, 13b and 13c as `BLOCKED`, and 13d and 14d as `SKIPPED`. Those are not failures: the runner counts them under `gates this script cannot run` and reports `run-gates: 1 failed, 23 passed`. They get no finding here.

## Phase 2 Readiness — Ordered Fix List

The fix loop walks this list, and it is the **single source of truth** for that loop. A `[ ]` marker anywhere else in this plan or its finding files is informational only.

1. [x] **Finding 1** — Rename the `fo` local in `record_in_set()` so typos stops flagging it. _(layer: cli, general)_

## Must Fix

### 1. Rename the `fo` local in `record_in_set()` so typos stops flagging it

→ [finding_1.md](feat_parallel_plan_reviews_task_round_1/finding_1.md)

## Not fixable on this branch

None. Every failing gate in the log has its cause in the tree.

## Source failures

- **Gate typecheck** (`commands.typecheck`): exited 0. No failures.
- **Gate test** (`commands.test`): exited 1.
  - `6f shipped files pass typos`: four hits of `check-typos: cli/templates/scripts/flow-walker.sh — fo`. → **Finding 1**. Class: no earlier logs were given, so it cannot be marked new or persisting. This is round 1.
