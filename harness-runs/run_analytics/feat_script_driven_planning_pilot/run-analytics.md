# Run analytics — feat_script_driven_planning_pilot

## Whole run

| Measure | Value |
|---|---|
| Sessions | 2 (0 incomplete) |
| Span | 11h54m |
| Wall | 7h16m |
| Active | 6h37m |
| Host-suspended | 0.0s |
| Idle | 39m 34s |
| Cost | $134.85 |
| Input tokens (uncached) | 4838 |
| Total input tokens (incl. cache) | 316768115 |
| Output tokens | 1471458 |
| Thinking tokens (main thread) | 9742 |
| Cache read tokens | 308429233 |
| Cache write tokens | 8334044 |
| Cache write tokens, main thread (5m / 1h) | 0 / 680829 |
| Cache hit ratio | 0.9737 |
| Requests | 2323 |
| Request latency p50 / p90 / p99 / max | 3.1s / 11.1s / 46.7s / 4m 04s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 54 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:task-plan-writer — Write task plan — 19m 55s (session 1) |
| Rate-limit peak | seven_day 0.56 |

## Network refusals

2 of 2 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No possible network attempt in 3 round logs.

## Gate rounds

Wait is the orchestrator's wait on `run-test-suite.sh --wait <label>`, summed over every polling row whose command ends in that label; — when none matches, as for a label waited on fewer than three times in a session (no polling row is written for it) or a command cut at 160 characters.

A phase's test-file total sums each file's own seconds, so it exceeds the gate's wall time when files run in parallel.

### Round task_round_1 — fail

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | 32m 52s |
| Gate rows | 28 (complete) |
| Test files — full | 199 files, 16710.4 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 0 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2124 s |
| full | 6a | FAIL | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 0 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | FAIL | 0 s |
| full | 11 | ok | 19 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 199)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/watcher-review-drop-payloads.test.mjs | pass | 838.3 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 669.6 | 29 | 0 |
| test/remote-run.test.mjs | pass | 657.6 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 628.5 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 612.5 | 17 | 0 |
| test/doctor.test.mjs | pass | 602.0 | 1 | 0 |
| test/remote-control.test.mjs | pass | 578.2 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 553.1 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 495.9 | 21 | 0 |
| test/planning-driver-control.test.mjs | pass | 490.4 | 7 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 35m 01s |
| Gate rows | 28 (complete) |
| Test files — full | 199 files, 17454.1 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 6a | ok | 0 s |
| focused | 6f | ok | 1 s |
| full | 1 | ok | 0 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 1 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2204 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 11 | ok | 17 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 199)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/watcher-review-drop-payloads.test.mjs | pass | 830.4 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 664.5 | 29 | 0 |
| test/remote-run.test.mjs | pass | 651.3 | 130 | 0 |
| test/doctor.test.mjs | pass | 634.9 | 1 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 627.2 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 617.3 | 17 | 0 |
| test/remote-control.test.mjs | pass | 576.8 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 548.0 | 33 | 0 |
| test/planning-driver-control.test.mjs | pass | 493.5 | 7 | 0 |
| test/watcher-run-profile.test.mjs | pass | 493.5 | 21 | 0 |

### Round review_1_round_1 — pass

| Measure | Value |
|---|---|
| Wait (every run of review_1_round_1) | 34m 30s |
| Gate rows | 28 (complete) |
| Test files — full | 201 files, 16649.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 1 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 1 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 0 s |
| full | 4 | ok | 2120 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 20 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 201)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 996.5 | 14 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 844.8 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 672.8 | 29 | 0 |
| test/remote-run.test.mjs | pass | 657.2 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 649.2 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 620.1 | 17 | 0 |
| test/remote-control.test.mjs | pass | 589.6 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 567.0 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 524.5 | 21 | 0 |
| test/doctor.test.mjs | pass | 515.1 | 1 | 0 |

## Session 1 — 2026-11-14T22:31:28.108Z → 2026-11-15T03:01:59.718Z

Session id: `683b0f8e-35fa-4cab-8582-ffb9067a56c3`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4h30m | 4h30m | 2h55m | 0.0s | 4m 04s | 4h26m | 2h59m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-14T23:38:10.822Z | 4m 04s | devscene:layer-implementer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 1544 | 3.0s | 11.3s | 52.5s | 4m 04s | 1 |
| devscene:architecture-reviewer | 91 | 3.3s | 12.4s | 55.8s | 55.8s | 0 |
| devscene:branch-reviewer | 114 | 4.0s | 16.1s | 31.2s | 31.9s | 0 |
| devscene:committer | 166 | 2.2s | 4.7s | 8.0s | 10.9s | 0 |
| devscene:layer-implementer | 449 | 3.2s | 11.2s | 1m 25s | 4m 04s | 1 |
| devscene:prompt-injection-reviewer | 1 | 1.8s | 1.8s | 1.8s | 1.8s | 0 |
| devscene:review-plan-reviewer | 77 | 3.9s | 11.1s | 20.0s | 20.0s | 0 |
| devscene:skeptic-reviewer | 54 | 4.8s | 24.8s | 32.8s | 32.8s | 0 |
| devscene:statistics-plan-writer | 7 | 3.2s | 18.2s | 18.2s | 18.2s | 0 |
| devscene:task-plan-reviewer | 92 | 3.4s | 15.7s | 49.6s | 49.6s | 0 |
| devscene:task-plan-writer | 120 | 5.0s | 31.3s | 1m 02s | 1m 14s | 0 |
| devscene:test-fix-plan-writer | 15 | 3.8s | 6.5s | 16.6s | 16.6s | 0 |
| orchestrator | 358 | 2.5s | 3.5s | 7.8s | 16.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 63 | 3h06m | 19m 55s |
| Bash | devscene:architecture-reviewer | 67 | 10.7s | 0.5s |
| Bash | devscene:branch-reviewer | 76 | 11.9s | 0.7s |
| Bash | devscene:committer | 229 | 2m 31s | 11.2s |
| Bash | devscene:layer-implementer | 339 | 31m 48s | 1m 43s |
| Bash | devscene:review-plan-reviewer | 61 | 9.8s | 0.2s |
| Bash | devscene:skeptic-reviewer | 35 | 5.4s | 0.4s |
| Bash | devscene:statistics-plan-writer | 8 | 1.2s | 0.1s |
| Bash | devscene:task-plan-reviewer | 64 | 10.3s | 0.2s |
| Bash | devscene:task-plan-writer | 84 | 13.1s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 12 | 1.8s | 0.2s |
| Bash | orchestrator | 351 | 1h12m | 1m 03s |
| Edit | devscene:committer | 18 | 0.6s | 0.0s |
| Edit | devscene:layer-implementer | 116 | 4.5s | 0.0s |
| Edit | devscene:task-plan-writer | 41 | 1.5s | 0.0s |
| Edit | orchestrator | 13 | 0.5s | 0.0s |
| Read | devscene:architecture-reviewer | 60 | 3.3s | 0.3s |
| Read | devscene:branch-reviewer | 55 | 1.5s | 0.2s |
| Read | devscene:committer | 31 | 0.5s | 0.0s |
| Read | devscene:layer-implementer | 146 | 6.6s | 0.3s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:review-plan-reviewer | 51 | 2.3s | 0.4s |
| Read | devscene:skeptic-reviewer | 27 | 1.1s | 0.3s |
| Read | devscene:statistics-plan-writer | 2 | 0.0s | 0.0s |
| Read | devscene:task-plan-reviewer | 65 | 2.2s | 0.2s |
| Read | devscene:task-plan-writer | 37 | 1.9s | 0.5s |
| Read | devscene:test-fix-plan-writer | 7 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 3.1s | 0.5s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:branch-reviewer | 12 | 0.5s | 0.0s |
| Write | devscene:layer-implementer | 13 | 0.5s | 0.0s |
| Write | devscene:review-plan-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:task-plan-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:task-plan-writer | 13 | 0.5s | 0.0s |
| Write | devscene:test-fix-plan-writer | 3 | 0.1s | 0.0s |
| Write | orchestrator | 3 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-15T00:03:58.236Z | 1m 43s | 1903 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T00:02:01.097Z | 1m 42s | 3738 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:33:31.543Z | 1m 31s | 913 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:33:30.840Z | 1m 25s | 527 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:33:29.986Z | 1m 25s | 735 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:15:34.919Z | 1m 24s | 1445 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:33:29.141Z | 1m 24s | 1763 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:30:27.924Z | 1m 23s | 1764 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T01:31:58.140Z | 1m 20s | 9386 | true | false |
| Bash | devscene:layer-implementer | 2026-11-15T00:05:43.737Z | 1m 19s | 1483 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:architecture-reviewer | git rev-parse --show-toplevel | 5 | 0.6s |
| devscene:committer | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> harness-runs/story_plans/feat_script_driven_planning_pilot_story_plan.md harness-runs/task_plans | 6 | 3.2s |
| devscene:committer | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> harness-runs/test_fix_plans/feat_script_driven_planning_pilot_task_round_1.md harness-runs/test_ | 3 | 1.6s |
| devscene:committer | bash <main_repo>/scripts/push-branch.sh <repo_root> | 21 | 1m 54s |
| devscene:committer | git branch --show-current | 21 | 2.8s |
| devscene:committer | git log -1 --oneline | 21 | 2.7s |
| devscene:committer | git rev-parse --show-toplevel | 21 | 2.8s |
| devscene:committer | git show --stat --format= HEAD | 3 | 0.3s |
| devscene:committer | git status --short | 50 | 7.8s |
| devscene:committer | grep -n -i "^## .*commit" <repo_root>/.claude/context/conventions.md | 3 | 0.3s |
| devscene:committer | grep -n -i -A40 "^## .*commit" <repo_root>/.claude/context/conventions.md | 5 | 0.6s |
| devscene:committer | grep -n -i -A40 "^## .*commit" <repo_root>/context/conventions.md | 3 | 0.4s |
| devscene:committer | printenv DEVSCENE_MAIN_REPO | 21 | 2.7s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 14 | 39.5s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 18 | 2.4s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 5 | 1m 32s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 3 | 10.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/planning-driver-walk.test.mjs | 4 | 5m 27s |
| devscene:layer-implementer | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs | 5 | 1m 37s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 5 | 2m 08s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-planning-driver.test.mjs | 5 | 3m 39s |
| devscene:review-plan-reviewer | git rev-parse --show-toplevel | 5 | 0.6s |
| devscene:task-plan-reviewer | git rev-parse --show-toplevel | 3 | 0.4s |
| devscene:task-plan-writer | git rev-parse --show-toplevel | 3 | 0.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/flow_progress/feat_script_driven_planning_pilot_progress.md" -- "chore: Flow progr | 13 | 6.2s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/story_plans/feat_script_driven_planning_pilot_story_plan.md" "harness-runs/task_pl | 4 | 2.9s |
| orchestrator | bash <main_repo>/scripts/push-branch.sh <repo_root> | 20 | 1m 37s |
| orchestrator | bash scripts/flow-walker.sh next --flow task_plan_writing --branch feat_script_driven_planning_pilot --node plan_writer --outcome returned | 3 | 1.1s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 33 | 32m 52s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 35 | 35m 01s |
| orchestrator | ls harness-runs/STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 3 | 0.4s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 51 | 12.3s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; echo checked | 68 | 48.5s |
| orchestrator | ls harness-runs/review_plan_reviews/feat_script_driven_planning_pilot/; ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter  | 3 | 0.4s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 4.3s | 1 | 351 | 4 | 30212 | 10469 | 19739 | 0.0003 |
| devscene:task-plan-writer | Write task plan | 19m 55s | 82 | 122174 | 166 | 21022405 | 20622641 | 399598 | 0.0737 |
| devscene:architecture-reviewer | Architecture review plan round 0 | 3m 19s | 21 | 20434 | 44 | 2405018 | 2247453 | 157521 | 0.0123 |
| devscene:task-plan-reviewer | Task plan review round 0 | 6m 56s | 49 | 41449 | 100 | 8885093 | 8615215 | 269778 | 0.0256 |
| devscene:task-plan-writer | Revise task plan round 1 | 5m 47s | 31 | 38374 | 64 | 2681321 | 2560968 | 120289 | 0.0214 |
| devscene:architecture-reviewer | Architecture review plan round 1 | 2m 40s | 22 | 16446 | 46 | 2390337 | 2236069 | 154222 | 0.0099 |
| devscene:task-plan-reviewer | Task plan review round 1 | 3m 27s | 33 | 20757 | 68 | 4536925 | 4338456 | 198401 | 0.0128 |
| devscene:task-plan-writer | Revise task plan round 2 | 41.4s | 7 | 4781 | 16 | 312946 | 278886 | 34044 | 0.0026 |
| devscene:architecture-reviewer | Architecture review plan round 2 | 35.1s | 6 | 3679 | 14 | 241654 | 210245 | 31395 | 0.0022 |
| devscene:task-plan-reviewer | Task plan review round 2 | 34.4s | 10 | 3383 | 22 | 450403 | 410574 | 39807 | 0.0021 |
| devscene:layer-implementer | Implement Task 10 (cli) | 1m 59s | 24 | 11870 | 50 | 1450491 | 1373295 | 77146 | 0.0074 |
| devscene:committer | Commit Task 10 | 30.1s | 8 | 2437 | 18 | 220085 | 193841 | 26226 | 0.0019 |
| devscene:layer-implementer | Implement Task 1 (cli) | 8m 34s | 41 | 57168 | 84 | 5044874 | 4871010 | 173780 | 0.0317 |
| devscene:committer | Commit Task 1 | 30.5s | 9 | 2428 | 20 | 254458 | 226675 | 27763 | 0.0019 |
| devscene:layer-implementer | Implement Task 2 (cli) | 8m 47s | 42 | 47630 | 86 | 5627881 | 5454966 | 172829 | 0.0325 |
| devscene:committer | Commit Task 2 | 27.1s | 7 | 2121 | 16 | 217179 | 187356 | 29807 | 0.0017 |
| devscene:layer-implementer | Implement Task 3 (cli) | 16m 43s | 63 | 90815 | 128 | 12836410 | 12565162 | 271120 | 0.0618 |
| devscene:committer | Commit Task 3 | 31.2s | 7 | 2331 | 16 | 202085 | 174297 | 27772 | 0.0019 |
| devscene:layer-implementer | Implement Task 4 (cli) | 2m 30s | 18 | 8946 | 38 | 1118820 | 1049929 | 68853 | 0.0093 |
| devscene:committer | Commit Task 4 | 36.4s | 9 | 2486 | 20 | 247330 | 232612 | 14698 | 0.0022 |
| devscene:layer-implementer | Implement Task 5 (cli) | 12m 28s | 31 | 37337 | 64 | 4448836 | 4267285 | 181487 | 0.0461 |
| devscene:committer | Commit Task 5 | 39.7s | 11 | 2380 | 24 | 288456 | 261985 | 26447 | 0.0024 |
| devscene:layer-implementer | Implement Task 6 (cli) | 12m 03s | 51 | 57107 | 104 | 9643077 | 9392994 | 249979 | 0.0446 |
| devscene:committer | Commit Task 6 | 36.5s | 7 | 2078 | 16 | 196950 | 169850 | 27084 | 0.0023 |
| devscene:layer-implementer | Implement Task 7 (plugin) | 1m 17s | 14 | 7147 | 30 | 761025 | 711936 | 49059 | 0.0048 |
| devscene:committer | Commit Task 7 | 54.5s | 8 | 2317 | 18 | 217637 | 204382 | 13237 | 0.0034 |
| devscene:layer-implementer | Implement Task 8 (general) | 5m 16s | 36 | 29079 | 74 | 5086414 | 4919535 | 166805 | 0.0195 |
| devscene:committer | Commit Task 8 | 34.7s | 8 | 2267 | 18 | 252132 | 219957 | 32157 | 0.0021 |
| devscene:layer-implementer | Implement Task 9 (general) | 2m 02s | 21 | 9992 | 44 | 1461422 | 1393049 | 68329 | 0.0076 |
| devscene:committer | Commit Task 9 | 42.3s | 9 | 2371 | 20 | 255954 | 240556 | 15378 | 0.0026 |
| devscene:architecture-reviewer | Branch architecture review | 2m 59s | 29 | 15153 | 60 | 3223467 | 3074430 | 148977 | 0.011 |
| devscene:branch-reviewer | End-of-branch code review | 6m 31s | 46 | 35049 | 94 | 8467860 | 8205147 | 262619 | 0.0241 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 23s | 12 | 7106 | 26 | 800132 | 720088 | 80018 | 0.0052 |
| devscene:branch-reviewer | Adjust code review per meta-review | 2m 52s | 25 | 16327 | 52 | 1579908 | 1507253 | 72603 | 0.0106 |
| devscene:review-plan-reviewer | Meta-review code review iter 1 | 2m 20s | 19 | 12541 | 40 | 1630233 | 1522890 | 107303 | 0.0086 |
| devscene:branch-reviewer | Adjust code review per meta-review 1 | 5m 10s | 35 | 31371 | 72 | 2455589 | 2369160 | 86357 | 0.0192 |
| devscene:review-plan-reviewer | Meta-review code review iter 2 | 2m 02s | 21 | 11201 | 44 | 1686507 | 1576624 | 109839 | 0.0076 |
| devscene:branch-reviewer | Adjust code review per meta-review 2 | 1m 11s | 8 | 8429 | 18 | 318702 | 288425 | 30259 | 0.0044 |
| devscene:review-plan-reviewer | Meta-review code review iter 3 | 1m 21s | 17 | 7455 | 36 | 1048457 | 978049 | 70372 | 0.005 |
| devscene:committer | Commit code review file | 19.1s | 4 | 1134 | 10 | 118755 | 93695 | 25050 | 0.0012 |
| devscene:layer-implementer | Fix code-review Finding 2 | 51.2s | 11 | 3150 | 24 | 480693 | 431702 | 48967 | 0.0032 |
| devscene:committer | Commit Finding 2 fix | 37.6s | 9 | 2619 | 20 | 241015 | 226941 | 14054 | 0.0023 |
| devscene:layer-implementer | Fix code-review Finding 5 | 23.8s | 6 | 1670 | 14 | 228731 | 205290 | 23427 | 0.0015 |
| devscene:committer | Commit Finding 5 fix | 36.8s | 8 | 2559 | 18 | 213860 | 200640 | 13202 | 0.0023 |
| devscene:layer-implementer | Fix code-review Finding 4 | 35.9s | 7 | 2783 | 16 | 287489 | 257553 | 29920 | 0.0022 |
| devscene:committer | Commit Finding 4 fix | 39.9s | 10 | 2880 | 22 | 267735 | 253015 | 14698 | 0.0025 |
| devscene:layer-implementer | Fix code-review Finding 1 | 6m 27s | 27 | 11579 | 56 | 1484415 | 1430668 | 53691 | 0.0239 |
| devscene:committer | Commit Finding 1 fix | 29.7s | 7 | 1831 | 16 | 194032 | 168117 | 25899 | 0.0018 |
| devscene:layer-implementer | Fix code-review Finding 3 | 2m 38s | 15 | 6252 | 32 | 697640 | 656033 | 41575 | 0.0097 |
| devscene:committer | Commit Finding 3 fix | 33.4s | 9 | 2288 | 20 | 238219 | 224976 | 13223 | 0.0021 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 8m 49s | 54 | 47352 | 110 | 8548748 | 8282735 | 265903 | 0.0326 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 48.9s | 8 | 4068 | 18 | 291935 | 250637 | 41280 | 0.003 |
| devscene:committer | Commit skeptic review file | 25.4s | 6 | 1582 | 14 | 176818 | 149284 | 27520 | 0.0016 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 5m 32s | 13 | 7186 | 28 | 612855 | 551867 | 60960 | 0.0205 |
| devscene:committer | Commit skeptic Finding 1 fix | 37.3s | 9 | 2637 | 20 | 241231 | 214776 | 26435 | 0.0023 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 1m 58s | 15 | 12176 | 32 | 671788 | 613683 | 58073 | 0.0073 |
| devscene:architecture-reviewer | Architecture gate on test fix plan | 1m 05s | 13 | 4780 | 28 | 767939 | 682713 | 85198 | 0.004 |
| devscene:committer | Commit test fix plan round 1 | 24.4s | 5 | 1461 | 12 | 147632 | 121361 | 26259 | 0.0015 |
| devscene:layer-implementer | Fix test-fix Finding 1 | 1m 12s | 15 | 5598 | 32 | 724144 | 673150 | 50962 | 0.0045 |
| devscene:committer | Commit test-fix Finding 1 | 31.9s | 7 | 2080 | 16 | 191753 | 178526 | 13211 | 0.002 |
| devscene:layer-implementer | Fix test-fix Finding 2 | 1m 12s | 14 | 5091 | 30 | 523684 | 496523 | 27131 | 0.0045 |
| devscene:committer | Commit test-fix Finding 2 | 43.2s | 9 | 2881 | 20 | 239403 | 225826 | 13557 | 0.0027 |
| devscene:statistics-plan-writer | Write branch statistics | 40.9s | 7 | 4225 | 16 | 229397 | 195022 | 34359 | 0.0025 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $93.05 |
| Cost — claude-opus-5-5 | $93.05 |
| Input tokens (uncached) | 3214 |
| Total input tokens (incl. cache) | 224339945 |
| Output tokens | 1020533 |
| Thinking tokens (main thread) | 5740 |
| Cache read tokens | 218797387 |
| Cache write tokens | 5539344 |
| Cache write tokens, main thread (5m / 1h) | 0 / 391693 |
| Cache hit ratio | 0.9753 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 716 | 92521349 | 10018 | 92128940 | 391693 |
| sub-agents | 2498 | 131818596 | 936629 | 126668447 | 5147651 |
| remainder | 0 | 0 | 73886 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 37 |
| Sub-agents spawned / failed / killed | 63 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 449 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.54 |

## Session 2 — 2026-11-15T07:39:48.534Z → 2026-11-15T10:25:57.356Z

Session id: `58e5b85b-e4f0-4326-9c40-a1ec84d0774f`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2h46m | 2h46m | 1h23m | 0.0s | 35m 30s | 2h10m | 2h00m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-15T08:00:20.329Z | 2m 14s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:12:23.078Z | 3m 37s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:16:17.510Z | 2m 45s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:20:37.258Z | 3m 31s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:27:49.909Z | 3m 20s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:32:06.815Z | 3m 20s | devscene:layer-reviewer | tool_running |
| 2026-11-15T08:35:36.323Z | 2m 01s | devscene:layer-reviewer | tool_running |
| 2026-11-15T08:42:53.746Z | 3m 45s | devscene:layer-implementer | tool_running |
| 2026-11-15T08:47:30.286Z | 4m 17s | devscene:layer-reviewer | tool_running |
| 2026-11-15T09:01:44.760Z | 4m 26s | devscene:layer-implementer | tool_running |
| 2026-11-15T09:29:25.248Z | 2m 10s | devscene:layer-implementer | tool_running |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 779 | 3.6s | 10.7s | 31.4s | 53.3s | 0 |
| devscene:architecture-reviewer | 34 | 2.4s | 19.5s | 29.0s | 29.0s | 0 |
| devscene:committer | 33 | 2.7s | 6.7s | 10.0s | 10.0s | 0 |
| devscene:layer-implementer | 325 | 4.3s | 11.5s | 37.8s | 53.3s | 0 |
| devscene:layer-reviewer | 158 | 4.6s | 11.7s | 21.9s | 23.9s | 0 |
| devscene:prompt-injection-reviewer | 1 | 2.1s | 2.1s | 2.1s | 2.1s | 0 |
| devscene:statistics-plan-writer | 9 | 1.8s | 20.9s | 20.9s | 20.9s | 0 |
| devscene:user-review-fix-plan-writer | 52 | 3.0s | 11.5s | 47.4s | 47.4s | 0 |
| orchestrator | 167 | 2.1s | 4.7s | 9.1s | 11.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 32 | 2h00m | 16m 54s |
| Bash | devscene:architecture-reviewer | 23 | 3.9s | 0.5s |
| Bash | devscene:committer | 44 | 33.6s | 9.4s |
| Bash | devscene:layer-implementer | 230 | 35m 48s | 4m 26s |
| Bash | devscene:layer-reviewer | 129 | 10m 42s | 4m 17s |
| Bash | devscene:statistics-plan-writer | 10 | 1.4s | 0.1s |
| Bash | devscene:user-review-fix-plan-writer | 37 | 5.9s | 0.2s |
| Bash | orchestrator | 122 | 35m 49s | 1m 01s |
| Edit | devscene:committer | 4 | 0.1s | 0.0s |
| Edit | devscene:layer-implementer | 170 | 6.5s | 0.0s |
| Edit | devscene:user-review-fix-plan-writer | 8 | 0.2s | 0.0s |
| Edit | orchestrator | 6 | 0.2s | 0.0s |
| Read | devscene:architecture-reviewer | 33 | 1.6s | 0.2s |
| Read | devscene:committer | 3 | 0.0s | 0.0s |
| Read | devscene:layer-implementer | 90 | 3.8s | 0.2s |
| Read | devscene:layer-reviewer | 66 | 3.5s | 0.4s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | devscene:user-review-fix-plan-writer | 20 | 0.5s | 0.2s |
| Read | orchestrator | 16 | 2.1s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 3 | 0.0s | 0.0s |
| Write | devscene:layer-reviewer | 9 | 0.3s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:user-review-fix-plan-writer | 6 | 0.2s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-15T09:01:44.760Z | 4m 26s | 41 | false | false |
| Bash | devscene:layer-reviewer | 2026-11-15T08:47:30.286Z | 4m 17s | 3694 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:42:53.746Z | 3m 45s | 3701 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:12:23.078Z | 3m 37s | 10039 | true | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:20:37.258Z | 3m 31s | 3424 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:27:49.909Z | 3m 20s | 3427 | false | false |
| Bash | devscene:layer-reviewer | 2026-11-15T08:32:06.815Z | 3m 20s | 1406 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:16:17.510Z | 2m 45s | 5086 | true | false |
| Bash | devscene:layer-implementer | 2026-11-15T08:00:20.329Z | 2m 14s | 2596 | false | false |
| Bash | devscene:layer-implementer | 2026-11-15T09:29:25.248Z | 2m 10s | 10679 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:committer | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> harness-runs/user_reviews/feat_script_driven_planning_pilot_fix_plan.md harness-runs/user_review | 4 | 2.8s |
| devscene:committer | bash <main_repo>/scripts/push-branch.sh <repo_root> | 4 | 25.7s |
| devscene:committer | git branch --show-current | 4 | 0.5s |
| devscene:committer | git log -1 --oneline | 4 | 0.5s |
| devscene:committer | git rev-parse --show-toplevel | 4 | 0.5s |
| devscene:committer | git status --short | 8 | 1.3s |
| devscene:committer | printenv DEVSCENE_MAIN_REPO | 4 | 0.5s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 9 | 26.6s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 11 | 1.4s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 3 | 9.2s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 4 | 9.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/planning-driver-control.test.mjs | 6 | 19m 14s |
| devscene:layer-implementer | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs | 3 | 12.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 3 | 29.8s |
| devscene:layer-reviewer | git rev-parse --show-toplevel | 11 | 1.4s |
| devscene:layer-reviewer | git status --short && git diff HEAD --stat | 4 | 0.8s |
| devscene:layer-reviewer | mkdir -p <repo_root>/harness-runs/user_review_fix_plan_point_reviews/feat_script_driven_planning_pilot_fix_plan/item_4/ | 3 | 0.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/flow_progress/feat_script_driven_planning_pilot_progress.md" -- "chore: Flow progr | 5 | 2.3s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/user_reviews/feat_script_driven_planning_pilot_fix_plan.md" "harness-runs/user_rev | 3 | 1.8s |
| orchestrator | bash <main_repo>/scripts/push-branch.sh <repo_root> | 12 | 1m 00s |
| orchestrator | cd <repo_root>; ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>&1; echo $(( $(cat harness-runs/.dispatch_counter) + 1 )) > h | 3 | 0.5s |
| orchestrator | cd <repo_root>; ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; echo $(( $(cat harness-runs/.dispatch_counter) + 1 | 14 | 2.4s |
| orchestrator | cd <repo_root>; ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; ls harness-runs/user_review_fix_plan_point_reviews | 11 | 1.7s |
| orchestrator | ls <repo_root>/harness-runs/STOP <repo_root>/harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait review_1_round_1 | 35 | 34m 30s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen user review file | 3.5s | 1 | 270 | 4 | 28375 | 10518 | 17853 | 0.0004 |
| devscene:user-review-fix-plan-writer | Write user-review fix plan | 6m 16s | 43 | 38695 | 88 | 4763555 | 4562363 | 201104 | 0.0378 |
| devscene:architecture-reviewer | Architecture gate on fix plan | 2m 21s | 21 | 14649 | 44 | 1970629 | 1843571 | 127014 | 0.0142 |
| devscene:user-review-fix-plan-writer | Revise fix plan per findings | 42.1s | 9 | 4818 | 20 | 400085 | 362523 | 37542 | 0.0042 |
| devscene:architecture-reviewer | Architecture gate round 1 | 1m 46s | 13 | 11153 | 28 | 1193795 | 1086181 | 107586 | 0.0107 |
| devscene:layer-implementer | Implement Finding 3 cli layer | 10m 58s | 32 | 37441 | 66 | 3343138 | 3201283 | 141789 | 0.066 |
| devscene:layer-reviewer | Review Finding 3 cli layer | 1m 38s | 13 | 8389 | 28 | 791213 | 711915 | 79270 | 0.0098 |
| devscene:layer-implementer | Implement Finding 3 general layer | 2m 01s | 18 | 10238 | 38 | 1380587 | 1300656 | 79893 | 0.0122 |
| devscene:layer-reviewer | Review Finding 3 general layer | 1m 04s | 9 | 5858 | 20 | 479094 | 423668 | 55406 | 0.0065 |
| devscene:committer | Commit Finding 3 | 41.3s | 9 | 2391 | 20 | 248503 | 221077 | 27406 | 0.0041 |
| devscene:layer-implementer | Implement Finding 4 cli layer | 14m 03s | 30 | 20919 | 62 | 2490664 | 2388766 | 101836 | 0.0846 |
| devscene:layer-reviewer | Review Finding 4 cli layer | 1m 58s | 22 | 9900 | 46 | 1356355 | 1274818 | 81491 | 0.0118 |
| devscene:layer-implementer | Fix Finding 4 cli per review | 4m 05s | 9 | 3885 | 20 | 318295 | 295917 | 22358 | 0.0246 |
| devscene:layer-reviewer | Re-review Finding 4 cli | 6m 29s | 13 | 5625 | 28 | 641561 | 595180 | 46353 | 0.0391 |
| devscene:layer-implementer | Implement Finding 4 general layer | 1m 49s | 18 | 8985 | 38 | 1267329 | 1182292 | 84999 | 0.011 |
| devscene:layer-reviewer | Review Finding 4 general layer | 2m 11s | 15 | 9899 | 32 | 893633 | 827583 | 66018 | 0.0132 |
| devscene:layer-implementer | Fix Finding 4 general per review | 4m 36s | 7 | 4413 | 16 | 271800 | 244492 | 27292 | 0.0277 |
| devscene:layer-reviewer | Re-review Finding 4 general | 4m 45s | 5 | 2300 | 12 | 252531 | 196973 | 55546 | 0.0287 |
| devscene:committer | Commit Finding 4 | 40.0s | 7 | 2465 | 16 | 205207 | 177381 | 27810 | 0.004 |
| devscene:layer-implementer | Implement Finding 2 cli layer | 16m 54s | 61 | 61483 | 124 | 9960462 | 9735796 | 224542 | 0.1017 |
| devscene:layer-reviewer | Review Finding 2 cli layer | 2m 40s | 17 | 10002 | 36 | 1079833 | 999749 | 80048 | 0.0161 |
| devscene:layer-implementer | Implement Finding 2 plugin layer | 1m 09s | 10 | 4492 | 22 | 546445 | 500397 | 46026 | 0.007 |
| devscene:layer-reviewer | Review Finding 2 plugin layer | 25.2s | 4 | 1879 | 10 | 165866 | 132221 | 33635 | 0.0025 |
| devscene:layer-implementer | Implement Finding 2 general layer | 1m 52s | 15 | 7188 | 32 | 978860 | 913840 | 64988 | 0.0113 |
| devscene:layer-reviewer | Review Finding 2 general layer | 2m 01s | 17 | 6995 | 36 | 1117059 | 1049827 | 67196 | 0.0121 |
| devscene:committer | Commit Finding 2 | 50.5s | 8 | 2315 | 18 | 239290 | 208989 | 30283 | 0.0051 |
| devscene:layer-implementer | Implement Finding 1 cli layer | 15m 14s | 90 | 60149 | 182 | 13584354 | 13369103 | 215069 | 0.0917 |
| devscene:layer-reviewer | Review Finding 1 cli layer | 2m 37s | 25 | 9389 | 52 | 1718884 | 1631323 | 87509 | 0.0158 |
| devscene:layer-implementer | Implement Finding 1 general layer | 4m 24s | 35 | 18237 | 72 | 3103827 | 2999967 | 103788 | 0.0265 |
| devscene:layer-reviewer | Review Finding 1 general layer | 2m 13s | 18 | 9624 | 38 | 1458220 | 1364074 | 94108 | 0.0134 |
| devscene:committer | Commit Finding 1 | 57.2s | 9 | 2611 | 20 | 274622 | 242644 | 31958 | 0.0057 |
| devscene:statistics-plan-writer | Update branch statistics | 51.2s | 9 | 6138 | 20 | 304933 | 267065 | 37848 | 0.0051 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $41.79 |
| Cost — claude-opus-5-5 | $41.79 |
| Input tokens (uncached) | 1624 |
| Total input tokens (incl. cache) | 92428170 |
| Output tokens | 450925 |
| Thinking tokens (main thread) | 4002 |
| Cache read tokens | 89631846 |
| Cache write tokens | 2794700 |
| Cache write tokens, main thread (5m / 1h) | 0 / 289136 |
| Cache hit ratio | 0.9697 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 336 | 35599166 | 4273 | 35309694 | 289136 |
| sub-agents | 1288 | 56829004 | 402795 | 54322152 | 2505564 |
| remainder | 0 | 0 | 43857 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 17 |
| Sub-agents spawned / failed / killed | 32 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 181 |
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.56 |
