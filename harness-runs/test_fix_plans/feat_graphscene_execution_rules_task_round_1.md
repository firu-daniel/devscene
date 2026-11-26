# Test Fix Plan: feat_graphscene_execution_rules — task round 1

## Context

- **Branch:** `feat_graphscene_execution_rules`
- **Log:** `harness-runs/test_run_logs/feat_graphscene_execution_rules/task_round_1.log`
- **Summary:** the typecheck gate passed (`exited 0`) and the test gate failed (`exited 1`) on one check only, `6a no machine paths`, because two committed plan-revision notes name the checkout by its absolute machine path.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: walk it top to bottom, first `[ ]` entry first. `[ ]` markers anywhere else in this plan or its per-finding files are informational only.

1. [x] **Finding 1** — Make the two plan-revision notes' review paths repo-relative. _(layer: general)_

## Must Fix

### 1. Make the two plan-revision notes' review paths repo-relative

→ [finding_1.md](feat_graphscene_execution_rules_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **gate `typecheck` (`commands.typecheck`)** — `exited 0`: no failure.
- **gate `test` (`commands.test`)** — `exited 1`; `run-gates: 1 failed, 30 passed`. New this round (no earlier logs).
  - `FAIL  6a no machine paths (printed output, which is the finding, 2 s)` → **Finding 1**. New this round.
- Not failures, no finding: `SKIPPED 13d Python container tests` (not opted in) and `SKIPPED 14d zizmor over the rendered workflows` (zizmor 1.30.1 not available); the `gates this script cannot run` list.
