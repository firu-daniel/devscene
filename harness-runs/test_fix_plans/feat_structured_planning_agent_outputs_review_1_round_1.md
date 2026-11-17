# Test Fix Plan: feat_structured_planning_agent_outputs — review_1 round 1

## Context

- **Branch:** `feat_structured_planning_agent_outputs`
- **Log:** `harness-runs/test_run_logs/feat_structured_planning_agent_outputs/review_1_round_1.log`
- **Earlier logs:** none named.
- **Summary:** the typecheck gate passed and the test gate failed on run-gates gate 4 (`npm test`, 16 failed and 1 cancelled). Five `watcher-planning-driver` cases fail because their fixture's plugin copy has no `schemas/` directory. The other twelve are `runBash` or file-level timeouts in the planning-driver and watcher suites, and they look like host load, not a defect in the tree.

Gate 13 (13a–13c `BLOCKED`, 13d `SKIPPED`) and gate 14d (`SKIPPED`) are reported by the log as not run, not as failures (`run-gates: 1 failed, 23 passed`), so they yield no entry here.

## Phase 2 Readiness — Ordered Fix List

This list is the **single source of truth** for the fix loop: walk it top to bottom and take the first `[ ]` entry. `[ ]` markers anywhere else, including the `- [ ]` sub-steps inside the per-finding files, are informational only.

1. [x] **Finding 1** — Copy each graph agent's return schema into the watcher planning-driver fixture's plugin. _(layer: cli)_

## Must Fix

### 1. The watcher planning-driver fixture's plugin copy carries no `schemas/` directory

→ [finding_1.md](feat_structured_planning_agent_outputs_review_1_round_1/finding_1.md)

## Not fixable on this branch

Every failure below is a `runBash` or test-file timeout. In each case a bounded shell run hit its fixture's ceiling: 180000 ms for one `pd_drive` (`DRIVE_TIMEOUT_MS` in `cli/test/helpers/planning-driver.mjs`), 120000 ms for one watcher tick, or 1800000 ms for a whole test file (`--test-timeout=1800000`). No assertion failed in any of them. **Reason they are not fixable on this branch:** the cause is host load, which is outside the tree.

- **The whole suite ran slowly.** Gate 4 took `4194 s`, and passing files show the same inflation: `test/doctor.test.mjs (1 tests, 0 failed)` took `1222.1 s` and `test/remote-run.test.mjs (130 tests, 0 failed)` took `1294.2 s`. This branch's earlier `task_round_1` gate log was consulted for timing only, not for classification. In that run gate 4 took `2454 s` and the same files took `675.6 s` and `700.6 s`, so this run was about 1.7–1.9× slower across the board.
- **No changed code path explains a hang.** The only planning-driver code this branch changed since its last green run is `pnl_load_schemas` in `cli/templates/scripts/lib/planning-node-lib.sh`. It now `jq`-reads `schemas/<agent>.return.json` rather than `awk`-scanning the agent file. The schema content is byte-identical: `plugin/schemas/task-plan-reviewer.return.json` matches the block the agent file carried before. The shared `driverFixture` copies the schema files, so these cases do not hit Finding 1's fault.
- **Remedy (operator):** re-run the gates on an unloaded host, without other suites or sessions competing for CPU. Do not raise the timeouts or skip the cases to get past this.

`cli/test/planning-driver-control.test.mjs`:

- `not ok 666 - <ask>: questions park as one Q<k> section per returned item, and an answer resumes the saved walk` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 669 - PAUSE raised mid-set is honoured at the join, and the next drive dispatches the revision` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 671 - a gate stalled once is re-dispatched alone and passes; its siblings run once and planning hands off` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 673 - a plan_review PASS with no findings_file fails its schema and is retried as infrastructure, not parked` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 78 - test/planning-driver-control.test.mjs` — `failureType: 'testTimeoutFailure'`, `error: 'test timed out after 1800000ms'`. This is the file-level cap, reached after the four timeouts above consumed the file's budget (`3420.6 s  test/planning-driver-control.test.mjs  (11 tests, 5 failed)`). The suite's `# cancelled 1` is the case this timeout cut off.

`cli/test/planning-driver-walk.test.mjs`:

- `not ok 677 - a full walk: writer, round 0 with one FAIL, revision, round 1 all PASS, hand-off` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 678 - a round's three gates run concurrently, and the round closes once` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 682 - sessions whose init withholds Glob and Grep beside Bash are not refused, and each is logged` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`
- `not ok 683 - every prompt is the copied core's dispatch block` — `runBash timed out after 180000 ms: bash -c cd "$W" || exit 90`

`cli/test/watcher-keep-awake.test.mjs`:

- `not ok 1819 - (a)(c) macOS: caffeinate waits on the engine's own pid, is gone once the session is, and stays off the stream` — `runBash timed out after 120000 ms: bash -c . "$1" status >/dev/null`

`cli/test/watcher-placeholder-host.test.mjs`:

- `not ok 1861 - a planted .git/commondir in the clone refuses the resume` — `runBash timed out after 120000 ms: bash -c . "$1" status >/dev/null`
- `not ok 1863 - after a launch the manifest lists exactly the absent denyWrite paths, glob expansions included, and --add-dir .mcp.json paths` — `runBash timed out after 120000 ms: bash -c . "$1" status >/dev/null`

## Source failures

No earlier log was named, so every failure below is classed **first round**.

- **Gate `typecheck`** — `exited 0`; no failure.
- **Gate `test`** — `exited 1`, via run-gates `FAIL  4 npm test (exit 1, 4194 s)`; its failing tests are listed below.
  - `cli/test/watcher-planning-driver.test.mjs`
    - `key on: the setup session, then node sessions on its vector, then one engine session` → **Finding 1** (first round)
    - `key on, and the driver parks: no engine session follows, and the record is parked` → **Finding 1** (first round)
    - `key on, and every node dispatch is undelivered: the run pauses and its one paused notification names the overload` → **Finding 1** (first round)
    - `a job with the key on: the setup session, node sessions pinned to the installed runtime root, then the engine session` → **Finding 1** (first round)
    - `the hand-off archives only what the driver consumed` → **Finding 1** (first round)
  - `cli/test/planning-driver-control.test.mjs`
    - `<ask>: questions park as one Q<k> section per returned item, and an answer resumes the saved walk` → `## Not fixable on this branch` (first round)
    - `PAUSE raised mid-set is honoured at the join, and the next drive dispatches the revision` → `## Not fixable on this branch` (first round)
    - `a gate stalled once is re-dispatched alone and passes; its siblings run once and planning hands off` → `## Not fixable on this branch` (first round)
    - `a plan_review PASS with no findings_file fails its schema and is retried as infrastructure, not parked` → `## Not fixable on this branch` (first round)
    - `test/planning-driver-control.test.mjs` (file-level timeout) → `## Not fixable on this branch` (first round)
  - `cli/test/planning-driver-walk.test.mjs`
    - `a full walk: writer, round 0 with one FAIL, revision, round 1 all PASS, hand-off` → `## Not fixable on this branch` (first round)
    - `a round's three gates run concurrently, and the round closes once` → `## Not fixable on this branch` (first round)
    - `sessions whose init withholds Glob and Grep beside Bash are not refused, and each is logged` → `## Not fixable on this branch` (first round)
    - `every prompt is the copied core's dispatch block` → `## Not fixable on this branch` (first round)
  - `cli/test/watcher-keep-awake.test.mjs`
    - `(a)(c) macOS: caffeinate waits on the engine's own pid, is gone once the session is, and stays off the stream` → `## Not fixable on this branch` (first round)
  - `cli/test/watcher-placeholder-host.test.mjs`
    - `a planted .git/commondir in the clone refuses the resume` → `## Not fixable on this branch` (first round)
    - `after a launch the manifest lists exactly the absent denyWrite paths, glob expansions included, and --add-dir .mcp.json paths` → `## Not fixable on this branch` (first round)
