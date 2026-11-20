# Test Fix Plan: feat_flow_graph_schema_v2 — task round 1

## Context

- **Branch:** `feat_flow_graph_schema_v2`
- **Log:** `harness-runs/test_run_logs/feat_flow_graph_schema_v2/task_round_1.log`
- **Summary:** The typecheck gate passed; the test gate failed on two `run-gates.sh` legs, 6a (a committed plan review names an absolute machine path) and 13f (`mypy` strict rejects a variable re-binding in `graphscene/src/graphscene/vocabulary.py`).

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: it is walked top to bottom, and only its markers record progress. Any `[ ]` marker elsewhere in this plan or in a per-finding file is informational only.

1. [x] **Finding 1** — Rewrite the two absolute plugin paths in the round-1 task plan review. _(layer: general)_
2. [ ] **Finding 2** — Stop re-binding the loop variable `name` to `object` in `_node_violations`. _(layer: graphscene)_

## Must Fix

### 1. Gate 6a: `review_1.md` names an absolute machine path
→ [finding_1.md](feat_flow_graph_schema_v2_task_round_1/finding_1.md)

### 2. Gate 13f: `mypy` rejects `name = node.get("binding")` in `vocabulary.py`
→ [finding_2.md](feat_flow_graph_schema_v2_task_round_1/finding_2.md)

## Not fixable on this branch

None. The two `SKIPPED` legs (13d, 14d) and the `gates this script cannot run` list are not failures and yield no finding.

## Source failures

No earlier-round log exists, so every failure below is from the first round; none can be classified as a regression or as persisting.

- **Gate `typecheck` (`commands.typecheck`)** — exited 0; no failure.
- **Gate `test` (`commands.test`)** — exited 1:
  - `6a no machine paths` → Finding 1 (first round).
  - `13f GraphScene typecheck` → Finding 2 (first round).
