# Test Fix Plan: feat_flow_host_claude_executor — task round 1

## Context

- **Branch:** `feat_flow_host_claude_executor`
- **Log:** `harness-runs/test_run_logs/feat_flow_host_claude_executor/task_round_1.log`
- **Summary:** the typecheck gate passed, and in the test gate leg 13j (the `devscene-flow-host` pytest suite) failed one test with an unhandled `PermissionError` from `os.killpg` in `session_process._signal_group`; all other 30 legs passed or were skipped by design.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: the loop walks these entries in order, and `[ ]` markers anywhere else in this plan are informational only.

1. [ ] **Finding 1** — `_signal_group` lets a `PermissionError` from `os.killpg` escape after the leader has exited. _(layer: devscene-flow-host)_

## Must Fix

### 1. `_signal_group` lets a `PermissionError` from `os.killpg` escape after the leader has exited

→ [finding_1.md](feat_flow_host_claude_executor_task_round_1/finding_1.md)

## Not fixable on this branch

None.

## Source failures

- **Gate `typecheck`** — exited 0; no failure.
- **Gate `test`** — exited 1 (`run-gates: 1 failed, 30 passed`):
  - `13j devscene-flow-host tests` — `devscene-flow-host/tests/test_session_process.py` (`test_a_member_holding_stderr_does_not_hold_the_run`, identified from the traceback), `PermissionError: [Errno 1] Operation not permitted` → **Finding 1**. Class: new this round (round 1, no earlier log).
- Not failures, no finding: `13d` and `14d` reported SKIPPED, and the gates the script cannot run (4's jq 1.6 leg, 5, 7, 8, 9, 10, 12, 15).
