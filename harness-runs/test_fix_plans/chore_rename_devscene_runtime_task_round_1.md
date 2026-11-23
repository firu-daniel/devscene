# Test Fix Plan: chore_rename_devscene_runtime — task round 1

## Context

**Branch:** `chore_rename_devscene_runtime`
**Test log:** `harness-runs/test_run_logs/chore_rename_devscene_runtime/task_round_1.log`
**Summary:** The typecheck gate exited 0 and the test gate exited 1 on a single check, gate 6a (no machine paths), which flagged an absolute home-directory path in the tracked code-review artifact `harness-runs/code_reviews/chore_rename_devscene_runtime_code_review.md`.

The log's BLOCKED legs (typecheck's `devscene-flow-host lint` / `typecheck`, and gate 13h / 13i / 13j) and SKIPPED legs (13d, 14d) are not failures: the typecheck gate exited 0, and `run-gates` reports `1 failed, 32 passed`, naming only 6a. They yield no finding and are not listed under `## Source failures`.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the fix loop.** The loop walks the `[ ]` entries below top-to-bottom; `[ ]` markers anywhere else (for example sub-step bullets inside a per-finding file) are informational only and are never the iteration source.

1. [x] **Finding 1** — Replace the absolute machine paths in the code review's Pass 0 sweep line with repo-relative forms. _(layer: general)_

---

## Must Fix

### 1. Code review artifact carries absolute home-directory paths (gate 6a)
→ [finding_1.md](chore_rename_devscene_runtime_task_round_1/finding_1.md)

---

## Not fixable on this branch

None.

---

## Source failures

- **Gate `typecheck`** — exited 0; no failure.
- **Gate `test`** — exited 1:
  - `6a no machine paths` → **Finding 1**. New this round (no earlier logs; first round).
