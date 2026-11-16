# Test Fix Plan: fix_planning_node_tool_check — task round 1

## Context

- **Branch:** `fix_planning_node_tool_check`
- **Log:** `harness-runs/test_run_logs/fix_planning_node_tool_check/task_round_1.log`
- **Summary:** The typecheck gate passed, and the test gate failed on one run-gates check alone, `6a no machine paths`, because the tracked task prompt quotes an absolute home-directory path.

The log also reports gate 13 (`13a`, `13b`, `13c`) as BLOCKED, with the remedy `bash scripts/python-service.sh sync`, and `13d` and `14d` as SKIPPED. `run-gates` does not count these as failures (`run-gates: 1 failed, 23 passed`), so they get no finding and are not listed below.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. Any `[ ]` markers elsewhere, in this index or in a per-finding file, are informational only.

1. [x] **Finding 1** — Task prompt names an absolute home-directory path. _(layer: general)_

## Must Fix

### 1. Task prompt names an absolute home-directory path
→ [finding_1.md](fix_planning_node_tool_check_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **typecheck gate:** exited 0. No failure.
- **test gate:** exited 1.
  - `6a no machine paths` → **Finding 1**. Class: first round, with no earlier logs to compare.
