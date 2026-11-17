# Test Fix Plan: fix_run_commit_trailer_amend — task round 1

## Context

- **Branch:** `fix_run_commit_trailer_amend`
- **Log:** `harness-runs/test_run_logs/fix_run_commit_trailer_amend/task_round_1.log` (no earlier rounds)
- **Summary:** The typecheck gate passed (exit 0); the test gate failed (exit 1) on gate 4 `npm test` alone, with 2 of 4103 tests failing — both because this branch changed one side of a table that a test holds equal to a second copy (`COPY_GIT_PATHS` gained three kept rows; Gate 15's restated `git` leg row was reworded) without updating the other.

Gate 13 (13a–13c, Python docs-retrieval service) was reported `BLOCKED` and 13d / 14d `SKIPPED`; the gate script counts those among neither its passes nor its failures (`run-gates: 1 failed, 23 passed`), so they are not failures of this round and yield no finding.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: its `[ ]` / `[x]` markers are the ones the loop reads and flips. Any `[ ]` marker elsewhere in this plan or its per-finding files is informational only.

1. [x] **Finding 1** — Placeholder-host profile test still counts three kept `COPY_GIT_PATHS` rows. _(layer: cli)_
2. [x] **Finding 2** — Probe's `git` leg declaration disagrees with Gate 15's restated leg table. _(layer: general)_

## Must Fix

### 1. Placeholder-host profile test still counts three kept `COPY_GIT_PATHS` rows

→ [finding_1.md](fix_run_commit_trailer_amend_task_round_1/finding_1.md)

### 2. Probe's `git` leg declaration disagrees with Gate 15's restated leg table

→ [finding_2.md](fix_run_commit_trailer_amend_task_round_1/finding_2.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck`** (`commands.typecheck`) — exited 0; no failures.
- **Gate `test`** (`commands.test`) — exited 1; `run-gates: 1 failed` — `4 npm test`, which reported two failing tests:
  - `cli/test/watcher-run-profile.test.mjs` — `on a placeholder host a clone's per-run copy re-roots the base's trio globs at every other sibling` (TAP 1988) → **Finding 1**. Class: new this round.
  - `cli/test/sandbox-probe-git-and-legs.test.mjs` — `Gate 15's restated leg table matches --list, row for row` (TAP 1675) → **Finding 2**. Class: new this round.
