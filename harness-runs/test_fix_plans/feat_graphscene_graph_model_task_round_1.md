# Test Fix Plan: feat_graphscene_graph_model — task round 1

## Context

**Branch:** `feat_graphscene_graph_model`
**Test log:** `harness-runs/test_run_logs/feat_graphscene_graph_model/task_round_1.log`
**Summary:** The typecheck gate passed and the test gate failed on one leg only, `13e GraphScene lint`: `ruff`'s import-block check (`I001`, "Organize imports") rejects `graphscene/src/graphscene/loader.py` because two blank lines, not one, separate its import block from the module-level assignment `_ECMA_DOT`; the other 32 legs passed.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the fix loop.** The loop walks the `[ ]` entries below top-to-bottom, and the commit step flips each one to `[x]` as that fix's commit lands. `[ ]` markers anywhere else — sub-step bullets inside a per-finding file included — are informational only and never an iteration target.

1. [ ] **Finding 1** — Drop the extra blank line after `loader.py`'s import block so `ruff` `I001` passes. _(layer: graphscene)_

---

## Must Fix

### 1. `loader.py` puts two blank lines between its imports and `_ECMA_DOT`, failing `ruff` `I001`
→ [finding_1.md](feat_graphscene_graph_model_task_round_1/finding_1.md)

---

## Not fixable on this branch

None.

---

## Source failures

- **Gate `test` (`commands.test`) — exited 1** (`run-gates: 1 failed, 32 passed`), from its one failing leg:
  - **`13e GraphScene lint`** (`FAIL  13e GraphScene lint (exit 1, 0 s)`) → **Finding 1**. Class: new this round (round 1, no earlier log).
- **Gate `typecheck` (`commands.typecheck`) — exited 0.** No failure.
