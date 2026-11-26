# Test Fix Plan: feat_graphscene_run_mode — task round 1

## Context

- **Branch:** `feat_graphscene_run_mode`
- **Log:** `harness-runs/test_run_logs/feat_graphscene_run_mode/task_round_1.log`
- **Summary:** The typecheck gate passed (`exited 0`). The test gate exited 1 because one CLI suite, `cli/test/gate12-sandbox-round-full-run.test.mjs`, was cancelled at the runner's 1800000 ms file timeout; every other test passed (`# pass 4729`, `# fail 0`, `# cancelled 1`).

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. `[ ]` markers anywhere else in this plan or its finding files are informational only.

1. [x] **Finding 1** — Bound the full-run grade suite's driver call so a hang fails one case instead of the whole file. _(layer: cli)_

## Must Fix

### 1. Bound the full-run grade suite's driver call so a hang fails one case instead of the whole file

→ [finding_1.md](feat_graphscene_run_mode_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck`** — passed (`== run-test-suite.sh: gate typecheck exited 0 ==`); no failure.
- **Gate `test`** (`== run-test-suite.sh: gate test exited 1 ==`), through run-gates gate `4 npm test` (`FAIL  4 npm test (exit 1, 2411 s)`):
  - `not ok 58 - test/gate12-sandbox-round-full-run.test.mjs` — `failureType: 'testTimeoutFailure'`, `error: 'test timed out after 1800000ms'` → **Finding 1**. Class: *new this round* (round 1; no earlier log to compare against).
- The run-gates SKIPPED lines (`13d`, `14d`) are not failures and map to no finding.
