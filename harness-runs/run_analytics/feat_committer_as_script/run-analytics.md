# Run analytics — feat_committer_as_script

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Engine / planning node sessions | 1 / 0 |
| Span | 4h28m |
| Wall | 4h28m |
| Session wall, summed over sessions | 4h28m |
| Active | 4h14m |
| Host-suspended | 0.0s |
| Idle | 13m 21s |
| Cost | $103.04 |
| Input tokens (uncached) | 3878 |
| Total input tokens (incl. cache) | 248643046 |
| Output tokens | 1147636 |
| Thinking tokens (main thread) | 4002 |
| Cache read tokens | 242552775 |
| Cache write tokens | 6086393 |
| Cache write tokens, main thread (5m / 1h) | 0 / 377279 |
| Cache hit ratio | 0.9755 |
| Requests | 1853 |
| Request latency p50 / p90 / p99 / max | 2.1s / 8.0s / 47.1s / 2m 47s |
| Requests over the idle threshold | 3 |
| API retries | 0 |
| Permission denials | 51 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:task-plan-writer — Write task plan — 28m 30s (session 1) |
| Rate-limit peak | seven_day 0.68 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Network refusals

1 of 1 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No possible network attempt in 1 round logs.

## Gate rounds

Wait is the orchestrator's wait on `run-test-suite.sh --wait <label>`, summed over every polling row whose command ends in that label; — when none matches, as for a label waited on fewer than three times in a session (no polling row is written for it) or a command cut at 160 characters.

A phase's test-file total sums each file's own seconds, so it exceeds the gate's wall time when files run in parallel.

### Round task_round_1 — fail

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | 1h07m |
| Gate rows | 28 (complete) |
| Test files — full | 204 files, 35253.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 10 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 1 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 7 s |
| full | 3c | ok | 4 s |
| full | 3d | ok | 5 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 3 s |
| full | 4 | FAIL | 4167 s |
| full | 6a | ok | 1 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 15 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 204)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | fail | 3422.0 | 11 | 5 |
| test/watcher-review-drop-payloads.test.mjs | pass | 1433.1 | 21 | 0 |
| test/remote-run.test.mjs | pass | 1287.7 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | fail | 1275.4 | 27 | 1 |
| test/watcher-remote-dispatch.test.mjs | pass | 1227.5 | 17 | 0 |
| test/remote-control.test.mjs | pass | 1178.7 | 83 | 0 |
| test/planning-driver-walk.test.mjs | fail | 1160.8 | 8 | 3 |
| test/doctor.test.mjs | pass | 1087.1 | 1 | 0 |
| test/watcher-keep-awake.test.mjs | pass | 1000.8 | 9 | 0 |
| test/watcher-remote-job.test.mjs | pass | 949.2 | 29 | 0 |

## Session 1 — 2026-11-16T14:50:34.670Z → 2026-11-16T19:18:45.711Z

Session id: `4bf93b6a-f0ee-4983-baa6-f59ce4aec65f`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4h28m | 4h28m | 2h50m | 0.0s | 13m 21s | 4h14m | 3h04m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-16T15:08:26.317Z | 2m 44s | devscene:task-plan-writer | in_flight_request |
| 2026-11-16T15:54:39.149Z | 2m 18s | devscene:layer-implementer | in_flight_request |
| 2026-11-16T17:13:39.619Z | 2m 47s | devscene:layer-implementer | in_flight_request |
| 2026-11-16T17:25:17.618Z | 5m 30s | devscene:layer-implementer | tool_running |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 1853 | 2.1s | 8.0s | 47.1s | 2m 47s | 3 |
| devscene:architecture-reviewer | 95 | 2.9s | 9.6s | 48.6s | 48.6s | 0 |
| devscene:branch-reviewer | 70 | 2.9s | 15.1s | 47.1s | 47.1s | 0 |
| devscene:committer | 246 | 1.5s | 4.2s | 6.7s | 7.4s | 0 |
| devscene:layer-implementer | 710 | 2.4s | 7.3s | 57.7s | 2m 47s | 2 |
| devscene:prompt-injection-reviewer | 1 | 1.5s | 1.5s | 1.5s | 1.5s | 0 |
| devscene:review-plan-reviewer | 43 | 2.9s | 8.9s | 12.3s | 12.3s | 0 |
| devscene:skeptic-reviewer | 66 | 3.9s | 12.5s | 20.7s | 20.7s | 0 |
| devscene:task-plan-reviewer | 101 | 3.7s | 14.2s | 26.1s | 34.7s | 0 |
| devscene:task-plan-writer | 117 | 4.5s | 32.5s | 1m 49s | 2m 44s | 1 |
| devscene:test-fix-plan-writer | 29 | 3.6s | 10.0s | 29.2s | 29.2s | 0 |
| orchestrator | 375 | 1.3s | 2.5s | 4.4s | 7.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 82 | 3h11m | 28m 30s |
| Bash | devscene:architecture-reviewer | 70 | 10.6s | 0.2s |
| Bash | devscene:branch-reviewer | 55 | 7.9s | 0.2s |
| Bash | devscene:committer | 340 | 5m 33s | 7.9s |
| Bash | devscene:layer-implementer | 578 | 34m 52s | 5m 30s |
| Bash | devscene:review-plan-reviewer | 34 | 5.4s | 0.2s |
| Bash | devscene:skeptic-reviewer | 59 | 9.6s | 0.6s |
| Bash | devscene:task-plan-reviewer | 70 | 11.6s | 0.4s |
| Bash | devscene:task-plan-writer | 76 | 16.5s | 1.5s |
| Bash | devscene:test-fix-plan-writer | 24 | 3.5s | 0.1s |
| Bash | orchestrator | 292 | 1h10m | 1m 04s |
| Edit | devscene:committer | 26 | 1.7s | 0.3s |
| Edit | devscene:layer-implementer | 402 | 26.6s | 0.3s |
| Edit | devscene:task-plan-writer | 42 | 1.4s | 0.0s |
| Edit | orchestrator | 9 | 7.6s | 4.1s |
| Read | devscene:architecture-reviewer | 82 | 3.7s | 0.3s |
| Read | devscene:branch-reviewer | 27 | 1.2s | 0.2s |
| Read | devscene:committer | 40 | 0.9s | 0.0s |
| Read | devscene:layer-implementer | 197 | 14.0s | 0.6s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:review-plan-reviewer | 20 | 0.7s | 0.3s |
| Read | devscene:skeptic-reviewer | 10 | 0.8s | 0.3s |
| Read | devscene:task-plan-reviewer | 94 | 2.8s | 0.2s |
| Read | devscene:task-plan-writer | 32 | 1.8s | 0.2s |
| Read | devscene:test-fix-plan-writer | 5 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 12.2s | 6.1s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 5 | 0.2s | 0.0s |
| Write | devscene:branch-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 7 | 0.2s | 0.0s |
| Write | devscene:review-plan-reviewer | 2 | 0.1s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.1s | 0.0s |
| Write | devscene:task-plan-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:task-plan-writer | 27 | 0.8s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |
| Write | orchestrator | 4 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-16T17:25:17.618Z | 5m 30s | 8450 | false | false |
| Bash | devscene:layer-implementer | 2026-11-16T16:02:03.985Z | 1m 38s | 217 | false | false |
| Bash | devscene:layer-implementer | 2026-11-16T16:02:03.384Z | 1m 33s | 2180 | false | false |
| Bash | orchestrator | 2026-11-16T18:09:33.070Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:08:26.444Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:40:58.273Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:06:13.171Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:18:19.384Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:19:25.876Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-16T18:17:13.012Z | 1m 03s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:architecture-reviewer | git rev-parse --show-toplevel | 5 | 0.6s |
| devscene:branch-reviewer | git rev-parse --show-toplevel | 3 | 0.3s |
| devscene:committer | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> harness-runs/story_plans/feat_committer_as_script_story_plan.md harness-runs/task_plans/feat_com | 13 | 18.8s |
| devscene:committer | bash <main_repo>/scripts/push-branch.sh <repo_root> | 31 | 2m 57s |
| devscene:committer | git -C <repo_root> status --short | 3 | 0.5s |
| devscene:committer | git branch --show-current | 30 | 12.1s |
| devscene:committer | git log -1 --oneline | 30 | 13.4s |
| devscene:committer | git rev-parse --show-toplevel | 31 | 11.9s |
| devscene:committer | git show --stat --format= HEAD | 5 | 0.7s |
| devscene:committer | git status --short | 69 | 35.6s |
| devscene:committer | grep -n -i "^## .*commit" <repo_root>/.claude/context/conventions.md | 3 | 1.4s |
| devscene:committer | grep -n -i "commit" <repo_root>/.claude/context/conventions.md | 4 | 1.4s |
| devscene:committer | grep -n -i "commit" <repo_root>/.claude/context/conventions.md \| head -40 | 4 | 0.4s |
| devscene:committer | grep -n -i -A30 "^## .*commit" <repo_root>/.claude/context/conventions.md | 3 | 0.6s |
| devscene:committer | grep -n -i -A40 "^## .*commit" <repo_root>/.claude/context/conventions.md | 3 | 1.2s |
| devscene:committer | printenv DEVSCENE_MAIN_REPO | 31 | 13.7s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 18 | 3m 58s |
| devscene:layer-implementer | bash scripts/typecheck.sh 2>&1 \| tail -15 | 6 | 34.7s |
| devscene:layer-implementer | bash scripts/typecheck.sh 2>&1 \| tail -5 | 3 | 46.9s |
| devscene:layer-implementer | bash scripts/typecheck.sh 2>&1 \| tail -5; echo "exit=$?" | 3 | 23.0s |
| devscene:layer-implementer | git -C <repo_root> status --short | 3 | 1.5s |
| devscene:layer-implementer | git diff --name-only HEAD | 3 | 4.2s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 4 | 6.3s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 30 | 9.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/commit-on-branch-unit.test.mjs | 3 | 1m 20s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 4 | 10.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-repo-resolution-corpus.test.mjs | 9 | 1m 06s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 14 | 2m 18s |
| devscene:layer-implementer | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs | 5 | 13.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/untrusted-input-corpus.test.mjs | 8 | 1m 43s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 4 | 42.1s |
| devscene:review-plan-reviewer | git rev-parse --show-toplevel | 4 | 0.5s |
| devscene:task-plan-reviewer | git rev-parse --show-toplevel | 3 | 0.3s |
| devscene:task-plan-reviewer | mkdir -p <repo_root>/harness-runs/task_plan_reviews/feat_committer_as_script | 3 | 0.3s |
| devscene:task-plan-writer | git rev-parse --show-toplevel | 3 | 0.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/story_plans/feat_committer_as_script_story_plan.md" "harness-runs/task_plans/feat_ | 4 | 3.5s |
| orchestrator | bash <main_repo>/scripts/push-branch.sh <repo_root> | 14 | 1m 10s |
| orchestrator | bash scripts/flow-walker.sh next --flow task_plan_writing --branch feat_committer_as_script --node plan_writer --outcome returned | 3 | 1.2s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 66 | 1h07m |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 74 | 39.7s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 4.1s | 1 | 332 | 4 | 30205 | 10438 | 19763 | 0.0003 |
| devscene:task-plan-writer | Write task plan | 28m 30s | 79 | 188053 | 160 | 22678095 | 22233009 | 444926 | 0.1063 |
| devscene:architecture-reviewer | Architecture review of plan | 3m 24s | 32 | 20539 | 66 | 4725288 | 4533719 | 191503 | 0.0127 |
| devscene:task-plan-reviewer | Task plan review | 5m 58s | 52 | 36441 | 106 | 8745819 | 8512450 | 233263 | 0.0223 |
| devscene:task-plan-writer | Revise task plan round 1 | 4m 02s | 30 | 27108 | 62 | 2631885 | 2519186 | 112637 | 0.0151 |
| devscene:architecture-reviewer | Architecture review round 1 | 3m 02s | 22 | 19083 | 46 | 3059599 | 2860338 | 199215 | 0.0113 |
| devscene:task-plan-reviewer | Task plan review round 1 | 4m 09s | 37 | 26064 | 78 | 6590034 | 6348698 | 241258 | 0.0155 |
| devscene:task-plan-writer | Revise task plan round 2 | 32.8s | 8 | 3526 | 18 | 294949 | 270609 | 24322 | 0.002 |
| devscene:architecture-reviewer | Architecture review round 2 | 17.7s | 5 | 1930 | 12 | 190118 | 168275 | 21831 | 0.0011 |
| devscene:task-plan-reviewer | Task plan review round 2 | 50.9s | 12 | 5184 | 26 | 618890 | 565551 | 53313 | 0.0032 |
| devscene:layer-implementer | Implement Task 1 (cli) | 6m 34s | 29 | 45626 | 60 | 2586204 | 2455361 | 130783 | 0.0245 |
| devscene:committer | Commit Task 1 | 28.7s | 10 | 2406 | 22 | 278395 | 262547 | 15826 | 0.0018 |
| devscene:layer-implementer | Implement Task 2 (cli) | 2m 34s | 20 | 11794 | 42 | 1446997 | 1373716 | 73239 | 0.0096 |
| devscene:committer | Commit Task 2 | 28.7s | 9 | 2435 | 20 | 255449 | 238670 | 16759 | 0.0018 |
| devscene:layer-implementer | Implement Task 3 (cli) | 11m 55s | 37 | 72502 | 76 | 4831889 | 4656547 | 175266 | 0.0444 |
| devscene:committer | Commit Task 3 | 28.1s | 8 | 2396 | 18 | 224029 | 196863 | 27148 | 0.0017 |
| devscene:layer-implementer | Implement Task 4 (cli) | 2m 55s | 15 | 8556 | 34 | 668013 | 628574 | 39405 | 0.0109 |
| devscene:committer | Commit Task 4 | 27.4s | 8 | 2192 | 18 | 248428 | 228759 | 19651 | 0.0017 |
| devscene:layer-implementer | Implement Task 5 (cli) | 1m 50s | 12 | 11673 | 26 | 670818 | 611945 | 58847 | 0.0069 |
| devscene:committer | Commit Task 5 | 40.5s | 6 | 2647 | 14 | 181496 | 165593 | 15889 | 0.0025 |
| devscene:layer-implementer | Implement Task 6 (cli) | 6m 49s | 19 | 9465 | 40 | 871582 | 833493 | 38049 | 0.0255 |
| devscene:committer | Commit Task 6 | 43.2s | 10 | 2393 | 22 | 280605 | 250917 | 29666 | 0.0027 |
| devscene:layer-implementer | Implement Task 7 (plugin) | 1m 23s | 13 | 6741 | 28 | 611525 | 572329 | 39168 | 0.0052 |
| devscene:committer | Commit Task 7 | 33.6s | 8 | 2053 | 18 | 220120 | 205988 | 14114 | 0.0021 |
| devscene:layer-implementer | Implement Task 8 (plugin) | 1m 32s | 12 | 7880 | 26 | 756449 | 693660 | 62763 | 0.0057 |
| devscene:committer | Commit Task 8 | 38.6s | 8 | 2208 | 18 | 225256 | 209413 | 15825 | 0.0024 |
| devscene:layer-implementer | Implement Task 9 (plugin) | 3m 46s | 26 | 20421 | 54 | 2136899 | 2049088 | 87757 | 0.0141 |
| devscene:committer | Commit Task 9 | 37.0s | 9 | 2271 | 20 | 235696 | 222656 | 13020 | 0.0023 |
| devscene:layer-implementer | Implement Task 10 (plugin) | 3m 39s | 27 | 16912 | 56 | 2258599 | 2164736 | 93807 | 0.0136 |
| devscene:committer | Commit Task 10 | 42.2s | 8 | 2270 | 18 | 216354 | 203176 | 13160 | 0.0026 |
| devscene:layer-implementer | Implement Task 11 (plugin) | 5m 34s | 45 | 26623 | 92 | 5209038 | 5073960 | 134986 | 0.0208 |
| devscene:committer | Commit Task 11 | 35.3s | 9 | 2247 | 20 | 250042 | 221407 | 28615 | 0.0022 |
| devscene:layer-implementer | Implement Task 12 (plugin) | 4m 01s | 32 | 18409 | 66 | 3010061 | 2906254 | 103741 | 0.015 |
| devscene:committer | Commit Task 12 | 30.5s | 6 | 1917 | 14 | 164890 | 152503 | 12373 | 0.0019 |
| devscene:layer-implementer | Implement Task 13 (plugin) | 4m 21s | 46 | 24680 | 94 | 4710419 | 4570448 | 139877 | 0.0163 |
| devscene:committer | Commit Task 13 | 29.1s | 8 | 2230 | 18 | 215966 | 202592 | 13356 | 0.0018 |
| devscene:layer-implementer | Implement Task 14 (plugin) | 4m 03s | 42 | 24857 | 86 | 4348431 | 4232333 | 116012 | 0.0151 |
| devscene:committer | Commit Task 14 | 24.5s | 7 | 1867 | 16 | 217066 | 199827 | 17223 | 0.0015 |
| devscene:layer-implementer | Implement Task 15 (plugin) | 5m 51s | 49 | 41338 | 100 | 6622196 | 6451881 | 170215 | 0.0219 |
| devscene:committer | Commit Task 15 | 28.7s | 9 | 2332 | 20 | 244359 | 217737 | 26602 | 0.0018 |
| devscene:layer-implementer | Implement Task 16 (plugin) | 57.1s | 10 | 6500 | 22 | 487702 | 438807 | 48873 | 0.0036 |
| devscene:committer | Commit Task 16 | 28.4s | 9 | 2341 | 20 | 251633 | 235424 | 16189 | 0.0018 |
| devscene:layer-implementer | Implement Task 17 (plugin) | 1m 09s | 12 | 7974 | 26 | 578211 | 533629 | 44556 | 0.0043 |
| devscene:committer | Commit Task 17 | 26.8s | 8 | 2315 | 18 | 223770 | 209136 | 14616 | 0.0017 |
| devscene:layer-implementer | Implement Task 18 (plugin) | 1m 08s | 17 | 7118 | 36 | 795965 | 755169 | 40760 | 0.0043 |
| devscene:committer | Commit Task 18 | 24.7s | 7 | 2066 | 16 | 192746 | 179461 | 13269 | 0.0015 |
| devscene:layer-implementer | Implement Task 19 (plugin) | 1m 18s | 18 | 8373 | 38 | 893306 | 847415 | 45853 | 0.0049 |
| devscene:committer | Commit Task 19 | 28.8s | 9 | 2353 | 20 | 238480 | 225109 | 13351 | 0.0018 |
| devscene:layer-implementer | Implement Task 20 (plugin) | 1m 42s | 22 | 10748 | 46 | 1324851 | 1264020 | 60785 | 0.0064 |
| devscene:committer | Commit Task 20 | 34.4s | 11 | 2842 | 24 | 304295 | 288468 | 15803 | 0.0021 |
| devscene:layer-implementer | Implement Task 21 (cli) | 1m 33s | 18 | 9931 | 38 | 963076 | 912429 | 50609 | 0.0058 |
| devscene:committer | Commit Task 21 | 31.0s | 7 | 2337 | 16 | 208517 | 192490 | 16011 | 0.0019 |
| devscene:layer-implementer | Implement Task 22 (general) | 1m 03s | 16 | 6321 | 34 | 1307498 | 1226668 | 80796 | 0.004 |
| devscene:committer | Commit Task 22 | 23.3s | 7 | 1763 | 16 | 206393 | 190964 | 15413 | 0.0014 |
| devscene:layer-implementer | Implement Task 23 (general) | 33.8s | 7 | 3299 | 16 | 403517 | 352695 | 50806 | 0.0021 |
| devscene:committer | Commit Task 23 | 28.3s | 8 | 2416 | 18 | 220332 | 206157 | 14157 | 0.0018 |
| devscene:layer-implementer | Implement Task 24 (general) | 6m 47s | 34 | 57788 | 70 | 3741866 | 3581863 | 159933 | 0.0254 |
| devscene:committer | Commit Task 24 | 27.3s | 8 | 2271 | 18 | 228728 | 200611 | 28099 | 0.0017 |
| devscene:architecture-reviewer | Branch architecture review | 2m 22s | 28 | 14392 | 58 | 2569779 | 2441349 | 128372 | 0.0088 |
| devscene:committer | Commit arch review file | 19.0s | 5 | 1375 | 12 | 144003 | 131430 | 12561 | 0.0012 |
| devscene:layer-implementer | Fix arch finding 1 (cli) | 9m 09s | 33 | 20078 | 68 | 2781155 | 2581481 | 199606 | 0.0342 |
| devscene:layer-implementer | Fix arch finding 1 (general) | 2m 00s | 20 | 12590 | 42 | 1278409 | 1210626 | 67741 | 0.0075 |
| devscene:committer | Commit arch finding 1 fix | 27.4s | 8 | 2274 | 18 | 216917 | 190650 | 26249 | 0.0017 |
| devscene:branch-reviewer | End-of-branch code review | 6m 07s | 51 | 36386 | 106 | 8960751 | 8695050 | 265595 | 0.0228 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 23s | 14 | 8073 | 30 | 550045 | 501969 | 48046 | 0.0052 |
| devscene:branch-reviewer | Adjust code review per meta | 1m 40s | 15 | 11069 | 32 | 686709 | 641849 | 44828 | 0.0062 |
| devscene:review-plan-reviewer | Meta-review code review round 2 | 1m 06s | 15 | 6486 | 32 | 1323628 | 1229859 | 93737 | 0.0041 |
| devscene:branch-reviewer | Adjust code review per meta 2 | 17.2s | 4 | 1736 | 10 | 136522 | 120803 | 15709 | 0.0011 |
| devscene:review-plan-reviewer | Meta-review code review round 3 | 39.5s | 9 | 3850 | 20 | 386321 | 347139 | 39162 | 0.0025 |
| devscene:committer | Commit code review file | 15.1s | 4 | 1037 | 10 | 112308 | 88917 | 23381 | 0.0009 |
| devscene:layer-implementer | Fix code-review finding 2 (cli) | 35.6s | 11 | 2640 | 24 | 373653 | 352174 | 21455 | 0.0022 |
| devscene:committer | Commit code-review finding 2 | 29.1s | 9 | 2396 | 20 | 249282 | 233680 | 15582 | 0.0018 |
| devscene:layer-implementer | Fix code-review finding 1 (cli) | 4m 00s | 40 | 16595 | 82 | 2624186 | 2552789 | 71315 | 0.0149 |
| devscene:layer-implementer | Fix code-review finding 1 (general) | 1m 32s | 17 | 8757 | 36 | 1242420 | 1165900 | 76484 | 0.0058 |
| devscene:committer | Commit code-review finding 1 | 27.2s | 9 | 2154 | 20 | 249496 | 234095 | 15381 | 0.0017 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 6m 53s | 66 | 40290 | 134 | 10685183 | 10421342 | 263707 | 0.0257 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 18.2s | 5 | 1779 | 12 | 157916 | 125696 | 32208 | 0.0011 |
| devscene:committer | Commit skeptic review file | 20.3s | 6 | 1481 | 14 | 185739 | 156504 | 29221 | 0.0013 |
| devscene:layer-implementer | Fix skeptic finding 1 (plugin) | 39.5s | 11 | 3424 | 24 | 453591 | 423915 | 29652 | 0.0025 |
| devscene:committer | Commit skeptic finding 1 | 31.1s | 8 | 2688 | 18 | 219234 | 205607 | 13609 | 0.0019 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 2m 48s | 29 | 17256 | 60 | 1908489 | 1817467 | 90962 | 0.0105 |
| devscene:architecture-reviewer | Arch gate on test fix plan | 34.0s | 8 | 3324 | 18 | 472405 | 402888 | 69499 | 0.0021 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $103.04 |
| Cost — claude-opus-5-5 | $103.04 |
| Input tokens (uncached) | 3878 |
| Total input tokens (incl. cache) | 248643046 |
| Output tokens | 1147636 |
| Thinking tokens (main thread) | 4002 |
| Cache read tokens | 242552775 |
| Cache write tokens | 6086393 |
| Cache write tokens, main thread (5m / 1h) | 0 / 377279 |
| Cache hit ratio | 0.9755 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 752 | 104341866 | 11115 | 103963835 | 377279 |
| sub-agents | 3126 | 144301180 | 1070487 | 138588940 | 5709114 |
| remainder | 0 | 0 | 66034 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 51 |
| Sub-agents spawned / failed / killed | 82 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 406 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.68 |
