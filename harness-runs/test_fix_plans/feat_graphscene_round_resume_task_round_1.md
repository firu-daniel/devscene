# Test Fix Plan: feat_graphscene_round_resume — task round 1

## Context

**Branch:** `feat_graphscene_round_resume`
**Test log:** `harness-runs/test_run_logs/feat_graphscene_round_resume/task_round_1.log`
**Earlier logs:** none.

The typecheck gate passed (`gate typecheck exited 0`); the test gate exited 1 on one failing check, gate 6a *no machine paths*, because the committed code review `harness-runs/code_reviews/feat_graphscene_round_resume_code_review.md` quotes the review-sweep command with two absolute machine paths in its `**Pass 0.**` paragraph. The two `SKIPPED` lines (13d, 14d) and the `gates this script cannot run` list are not failures and yield no finding.

---

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: it walks these entries in order and flips each `[ ]` itself. Any `[ ]` marker elsewhere in this plan or its per-finding files is informational only.

1. [ ] **Finding 1** — Remove the machine paths from the code review's Pass 0 line. _(layer: general)_

---

## Must Fix

### 1. Remove the machine paths from the code review's Pass 0 line

→ [finding_1.md](feat_graphscene_round_resume_task_round_1/finding_1.md)

---

## Not fixable on this branch

None.

---

## Source failures

- **gate typecheck** — exited 0; no failure.
- **gate test** — exited 1 (`run-gates: 1 failed, 32 passed`):
  - `6a no machine paths` → **Finding 1**. Class: new this round (no earlier round's log exists).
