# Test Fix Plan: feat_committer_as_script — task round 1

## Context

- **Branch:** `feat_committer_as_script`
- **Test log:** `harness-runs/test_run_logs/feat_committer_as_script/task_round_1.log` (round 1; no earlier logs)
- **Summary:** The typecheck gate passed, and the test gate failed on one file: `cli/test/gate12-sandbox-round-full-run.test.mjs` crashes when it loads, because it looks for the commit wrapper's refusals in their old source spelling.

The suite totals are `# tests 4091`, `# pass 4065`, `# fail 1`, `# cancelled 0`, `# skipped 25`. `run-gates` reports `1 failed, 23 passed`, and the one failure is `4 npm test`.

The log also reports gates 13a–13c as `BLOCKED`, because the Python environment is not provisioned. Gates 13d and 14d are `SKIPPED`. `run-gates` counts none of them as failures, so this plan carries none of them.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. `[ ]` markers anywhere else in this plan or its per-finding files are informational only.

1. [ ] **Finding 1** — Gate-12 full-run suite looks for the commit wrapper's refusals in their old `echo … >&2` spelling. _(layer: cli)_

## Must Fix

### 1. Gate-12 full-run suite still looks for the commit wrapper's refusals in their old `echo … >&2` spelling
→ [finding_1.md](feat_committer_as_script_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

Every failure below is classed **first round**. No earlier log exists, so none can be classed as new or persisting.

- **Gate `typecheck`:** exited 0, with no failures.
- **Gate `test`** (exited 1; `run-gates` failure `4 npm test`):
  - `not ok 49 - test/gate12-sandbox-round-full-run.test.mjs` → **Finding 1** (first round)
