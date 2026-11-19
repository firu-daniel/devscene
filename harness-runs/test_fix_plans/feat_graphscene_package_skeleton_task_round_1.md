# Test Fix Plan: feat_graphscene_package_skeleton — task round 1

## Context

- **Branch:** `feat_graphscene_package_skeleton`
- **Log:** `harness-runs/test_run_logs/feat_graphscene_package_skeleton/task_round_1.log`
- **Earlier logs:** none (round 1).

The `typecheck` gate passed (`exited 0`) and the `test` gate failed (`exited 1`) on one sub-gate only, 13a Python lint, where `ruff check` in `docs-retrieval-service/` reports seven unsorted import blocks (`from fakes import …` placed ahead of the `devscene_docs_retrieval` imports in seven test files).

The log's `SKIPPED` lines (13d Python container tests, 14d zizmor) and its `== gates this script cannot run` list are neither failures nor passes and yield no finding.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: it walks these entries in order and flips only these markers. Any `[ ]` marker elsewhere in this plan or its per-finding files is informational only.

1. [ ] **Finding 1** — Sort the `fakes` import after the `devscene_docs_retrieval` imports in seven service test files. _(layer: general)_

## Must Fix

### 1. Sort the `fakes` import after the `devscene_docs_retrieval` imports in seven service test files

→ [finding_1.md](feat_graphscene_package_skeleton_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck` (`commands.typecheck`)** — exited 0; no failures.
- **Gate `test` (`commands.test`)** — exited 1:
  - `FAIL  13a Python lint (exit 1, 1 s)` — `ruff check`, "Found 7 errors." → **Finding 1**. Class: new this round (round 1; no earlier log to compare against).
