# Test Fix Plan: feat_flow_walker_uv_shipping — task round 2

## Context

- **Branch:** `feat_flow_walker_uv_shipping`
- **Log:** `harness-runs/test_run_logs/feat_flow_walker_uv_shipping/task_round_2.log` (earlier: `harness-runs/test_run_logs/feat_flow_walker_uv_shipping/task_round_1.log`)
- **Summary:** The typecheck gate passed and every round-1 failure now passes, but gate 4's full `npm test` run failed one test: the source scan in `cli/test/main-anchor-isolation.test.mjs` found an unguarded `process.env` spread that the round-1 fix added to `cli/test/python-packages-staged.test.mjs`.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. `[ ]` markers anywhere else in this plan or its per-finding files are informational only.

1. [x] **Finding 1** — Blank the main-checkout anchor in the npm pack test's environment. _(layer: cli)_

## Must Fix

### 1. Blank the main-checkout anchor in the npm pack test's environment

→ [finding_1.md](feat_flow_walker_uv_shipping_task_round_2/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck`** — exited 0. No failures.
- **Gate `test`, gate 4 `npm test`** (exit 1) — `not ok 717 - every process.env spread in a test source blanks the anchor in the same object` → **Finding 1**. Class: **new this round** — absent from the round-1 log; a regression from round 1's fix to `npm pack lists the staged Python files` (commit `b9aeeb56`, "npm pack test uses its own npm cache"), which added the spread the scan reports.
