# Test Fix Plan: fix_injection_verdict_tools_used_prefix — review_1 round 1

## Context

- **Branch:** `fix_injection_verdict_tools_used_prefix`
- **Log:** `harness-runs/test_run_logs/fix_injection_verdict_tools_used_prefix/review_1_round_1.log`
- **Summary:** the typecheck gate passed and the test gate failed on two of its sub-gates — one `cli/test/doctor.test.mjs` case whose substring assertion collided with this run's random fixture-directory name (gate 4), and four absolute home-directory paths in three tracked review-round artifacts under `harness-runs/` (gate 6a).

Gate 13's three sub-gates (13a, 13b, 13c) report `BLOCKED` and 13d `SKIPPED`; the log counts neither as a failure (`run-gates: 2 failed, 23 passed`), so neither yields a finding or a `## Not fixable on this branch` entry.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop. `[ ]` markers anywhere else in this plan or its per-finding files are informational only.

1. [x] **Finding 2** — Replace the home-directory paths in three tracked review artifacts. _(layer: general)_
2. [ ] **Finding 1** — Give the daemon-path test's gh stub a name no fixture path can contain. _(layer: cli)_

## Must Fix

### 1. The daemon-path test's gh-name assertion collides with the random fixture directory name
→ [finding_1.md](fix_injection_verdict_tools_used_prefix_review_1_round_1/finding_1.md)

### 2. Tracked review-round artifacts carry the running user's home directory
→ [finding_2.md](fix_injection_verdict_tools_used_prefix_review_1_round_1/finding_2.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck`** (`commands.typecheck`) — exited 0; no failure.
- **Gate `test`** (`commands.test`) — exited 1, from these sub-gates:
  - `4 npm test` → `not ok 91 - daemon-path names gh when remote execution is on, and not when it is off` (`cli/test/doctor.test.mjs`), and its parent `not ok 374 - doctor` suite (`1 subtest failed`, the same failure) → **Finding 1**. Class: first round, no earlier log — not classed as new or persisting.
  - `6a no machine paths` → **Finding 2**. Class: first round, no earlier log — not classed as new or persisting.
