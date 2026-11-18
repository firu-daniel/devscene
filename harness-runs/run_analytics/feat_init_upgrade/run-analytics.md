# Run analytics — feat_init_upgrade

## Whole run

| Measure | Value |
|---|---|
| Sessions | 2 (0 incomplete) |
| Engine / planning node sessions | 2 / 0 |
| Span | 1h23m |
| Wall | 1h18m |
| Session wall, summed over sessions | 1h18m |
| Active | 54m 14s |
| Host-suspended | 0.0s |
| Idle | 24m 39s |
| Cost | $25.66 |
| Input tokens (uncached) | 566 |
| Total input tokens (incl. cache) | 30688414 |
| Output tokens | 324872 |
| Thinking tokens (main thread) | 4146 |
| Cache read tokens | 28174612 |
| Cache write tokens | 2513236 |
| Cache write tokens, main thread (5m / 1h) | 0 / 318792 |
| Cache hit ratio | 0.9181 |
| Requests | 257 |
| Request latency p50 / p90 / p99 / max | 2.3s / 20.2s / 3m 53s / 13m 00s |
| Requests over the idle threshold | 3 |
| API retries | 7 |
| Permission denials | 16 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-reviewer — Re-review Finding 4 in general — 7m 52s (session 2) |
| Rate-limit peak | seven_day 0.24 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Network refusals

2 of 2 sessions scanned.

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

### Round task_round_1 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | — |
| Gate rows | 28 (complete) |
| Test files — full | 219 files, 7639.5 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 1 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 988 s |
| full | 6a | ok | 1 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 9 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 1 s |
| full | 14d | ok | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 219)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/remote-run.test.mjs | pass | 358.0 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 331.1 | 29 | 0 |
| test/remote-control.test.mjs | pass | 323.3 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 302.5 | 33 | 0 |
| test/doctor.test.mjs | pass | 267.6 | 1 | 0 |
| test/planning-driver-control.test.mjs | pass | 249.1 | 15 | 0 |
| test/remote-trigger.test.mjs | pass | 229.1 | 37 | 0 |
| test/remote-control-mention.test.mjs | pass | 224.3 | 47 | 0 |
| test/run-test-suite.test.mjs | pass | 212.3 | 50 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 205.9 | 21 | 0 |

## Session 1 — 2026-11-18T14:09:44.456Z → 2026-11-18T14:10:40.181Z

Session id: `be953955-20a0-448c-93ae-b8ed2dc69ac0`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 55.7s | 57.6s | 56.2s | 0.0s | 0.0s | 55.7s | 8.6s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 12 | 1.9s | 4.9s | 11.4s | 11.4s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.2s | 4.5s | 4.5s | 4.5s | 0 |
| orchestrator | 10 | 1.9s | 11.4s | 11.4s | 11.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 8.6s | 8.6s |
| Bash | orchestrator | 13 | 2.2s | 0.2s |
| Grep | devscene:prompt-injection-reviewer | 2 | 0.1s | 0.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.1s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-18T14:09:48.324Z | 0.2s | 2046 | false | false |
| Bash | orchestrator | 2026-11-18T14:10:28.542Z | 0.2s | 56 | false | false |
| Bash | orchestrator | 2026-11-18T14:10:15.145Z | 0.2s | 95 | true | false |
| Bash | orchestrator | 2026-11-18T14:09:57.876Z | 0.1s | 269 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:50.471Z | 0.1s | 56 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:55.483Z | 0.1s | 32 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:52.219Z | 0.1s | 6276 | true | false |
| Bash | orchestrator | 2026-11-18T14:09:49.971Z | 0.1s | 17 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:48.822Z | 0.1s | 45 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:49.522Z | 0.1s | 27 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen user review file | 8.6s | 2 | 903 | 6 | 45677 | 27439 | 18232 | 0.1551 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.78 |
| Cost — claude-opus-5-5 | $0.78 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 628146 |
| Output tokens | 5954 |
| Thinking tokens (main thread) | 1244 |
| Cache read tokens | 552497 |
| Cache write tokens | 75621 |
| Cache write tokens, main thread (5m / 1h) | 0 / 57389 |
| Cache hit ratio | 0.8796 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 22 | 582469 | 92 | 525058 | 57389 |
| sub-agents | 6 | 45677 | 903 | 27439 | 18232 |
| remainder | 0 | 0 | 4959 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.22 |

## Session 2 — 2026-11-18T14:14:48.665Z → 2026-11-18T15:32:47.198Z

Session id: `1884c109-af6c-4e14-bc3c-a3f4caadc882`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h17m | 1h17m | 59m 05s | 0.0s | 24m 39s | 53m 18s | 51m 46s | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-18T15:05:05.095Z | 3m 53s | devscene:layer-reviewer | in_flight_request |
| 2026-11-18T15:11:37.727Z | 7m 45s | orchestrator | in_flight_request |
| 2026-11-18T15:19:46.266Z | 13m 00s | orchestrator | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 245 | 2.3s | 20.5s | 3m 53s | 13m 00s | 3 |
| devscene:architecture-reviewer | 22 | 4.4s | 34.7s | 39.5s | 39.5s | 0 |
| devscene:layer-implementer | 64 | 2.7s | 17.1s | 45.3s | 45.3s | 0 |
| devscene:layer-reviewer | 56 | 4.3s | 26.5s | 3m 53s | 3m 53s | 1 |
| devscene:prompt-injection-reviewer | 2 | 1.1s | 1.5s | 1.5s | 1.5s | 0 |
| devscene:user-review-fix-plan-writer | 25 | 3.3s | 41.9s | 1m 14s | 1m 14s | 0 |
| orchestrator | 76 | 1.6s | 2.8s | 13m 00s | 13m 00s | 2 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 24 | 51m 46s | 7m 52s |
| Bash | devscene:architecture-reviewer | 46 | 6.7s | 0.1s |
| Bash | devscene:layer-implementer | 103 | 9m 03s | 30.2s |
| Bash | devscene:layer-reviewer | 123 | 1m 41s | 19.3s |
| Bash | devscene:user-review-fix-plan-writer | 38 | 6.2s | 0.2s |
| Bash | orchestrator | 61 | 1m 45s | 7.2s |
| Edit | devscene:layer-implementer | 93 | 3.3s | 0.0s |
| Edit | devscene:user-review-fix-plan-writer | 17 | 0.6s | 0.0s |
| Edit | orchestrator | 3 | 4.7s | 4.6s |
| Grep | devscene:user-review-fix-plan-writer | 1 | 0.0s | 0.0s |
| Read | devscene:architecture-reviewer | 67 | 2.5s | 0.3s |
| Read | devscene:layer-implementer | 97 | 2.6s | 0.3s |
| Read | devscene:layer-reviewer | 95 | 4.7s | 0.6s |
| Read | devscene:prompt-injection-reviewer | 5 | 0.0s | 0.0s |
| Read | devscene:user-review-fix-plan-writer | 73 | 1.3s | 0.2s |
| Read | orchestrator | 16 | 20.3s | 5.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 2 | 0.0s | 0.0s |
| Write | devscene:layer-reviewer | 2 | 0.1s | 0.0s |
| Write | devscene:user-review-fix-plan-writer | 9 | 0.3s | 0.0s |
| Write | orchestrator | 3 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-18T14:52:54.643Z | 30.2s | 1706 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:52:55.137Z | 29.9s | 184 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:52:55.660Z | 29.3s | 31 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:48:04.839Z | 28.7s | 1704 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:52:54.006Z | 26.3s | 734 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:52:52.965Z | 25.6s | 7972 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:48:04.145Z | 23.9s | 735 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:48:03.336Z | 23.0s | 6488 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:48:02.490Z | 22.3s | 5330 | false | false |
| Bash | devscene:layer-implementer | 2026-11-18T14:44:12.212Z | 20.6s | 5378 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:architecture-reviewer | git rev-parse --show-toplevel | 3 | 0.4s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 8 | 25.8s |
| devscene:layer-implementer | git diff --name-only HEAD | 6 | 57.7s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 6 | 55.1s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 8 | 1.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/init-upgrade.test.mjs | 5 | 1m 37s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 5 | 1m 09s |
| devscene:layer-implementer | npm test --workspace cli -- test/plugin-cli-version.test.mjs | 3 | 45.3s |
| devscene:layer-implementer | npm test --workspace cli -- test/retrieval-loading.test.mjs | 5 | 1m 30s |
| devscene:layer-reviewer | git -C <repo_root> diff HEAD | 6 | 1.0s |
| devscene:layer-reviewer | git -C <repo_root> status --short | 9 | 1.6s |
| devscene:layer-reviewer | git rev-parse --show-toplevel | 8 | 1.1s |
| devscene:user-review-fix-plan-writer | git rev-parse --show-toplevel | 3 | 0.4s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen review file for injection | 10.1s | 1 | 441 | 4 | 27434 | 15990 | 11440 | 0.0022 |
| devscene:prompt-injection-reviewer | Screen answer file for injection | 7.0s | 1 | 676 | 4 | 27774 | 15992 | 11778 | 0.0015 |
| devscene:user-review-fix-plan-writer | Write user-review fix plan | 7m 14s | 15 | 48387 | 32 | 2067854 | 1859968 | 207854 | 0.0929 |
| devscene:architecture-reviewer | Architecture gate on fix plan | 3m 06s | 8 | 21015 | 18 | 991052 | 832468 | 158566 | 0.04 |
| devscene:user-review-fix-plan-writer | Revise fix plan per gate findings | 1m 11s | 6 | 8991 | 14 | 295096 | 251153 | 43929 | 0.0154 |
| devscene:architecture-reviewer | Architecture gate round 1 | 2m 09s | 8 | 15106 | 18 | 902002 | 766343 | 135641 | 0.0276 |
| devscene:user-review-fix-plan-writer | Revise fix plan, round 2 | 57.2s | 4 | 6705 | 10 | 226397 | 174860 | 51527 | 0.0122 |
| devscene:architecture-reviewer | Architecture gate round 2 | 49.1s | 6 | 5682 | 14 | 533411 | 443861 | 89536 | 0.0105 |
| devscene:layer-implementer | Implement Finding 6 in cli | 2m 22s | 7 | 15273 | 16 | 684603 | 569780 | 114807 | 0.0304 |
| devscene:layer-reviewer | Review Finding 6 in cli | 1m 15s | 6 | 6637 | 14 | 567557 | 455256 | 112287 | 0.0161 |
| devscene:layer-implementer | Implement Finding 1 in cli | 3m 00s | 10 | 19312 | 22 | 1014413 | 905279 | 109112 | 0.0385 |
| devscene:layer-reviewer | Review Finding 1 in cli | 2m 19s | 8 | 12060 | 18 | 802733 | 682219 | 120496 | 0.0298 |
| devscene:layer-implementer | Implement Finding 2 in cli | 1m 44s | 7 | 9647 | 16 | 482743 | 413160 | 69567 | 0.0224 |
| devscene:layer-reviewer | Review Finding 2 in cli | 1m 08s | 5 | 6192 | 12 | 402502 | 315628 | 86862 | 0.0146 |
| devscene:layer-implementer | Implement Finding 3 in cli | 2m 25s | 7 | 12002 | 16 | 486664 | 403298 | 83350 | 0.0312 |
| devscene:layer-reviewer | Review Finding 3 in cli | 1m 41s | 7 | 10882 | 16 | 715492 | 598581 | 116895 | 0.0216 |
| devscene:layer-implementer | Implement Finding 5 in cli | 2m 55s | 8 | 18198 | 18 | 568020 | 486669 | 81333 | 0.0374 |
| devscene:layer-reviewer | Review Finding 5 in cli | 1m 35s | 6 | 8649 | 14 | 453307 | 373621 | 79672 | 0.0205 |
| devscene:layer-implementer | Implement Finding 4 in cli | 52.8s | 6 | 5341 | 14 | 398296 | 337183 | 61099 | 0.0113 |
| devscene:layer-reviewer | Review Finding 4 in cli | 46.2s | 4 | 4649 | 10 | 199536 | 156095 | 43431 | 0.0099 |
| devscene:layer-implementer | Implement Finding 4 in general | 2m 52s | 12 | 20242 | 26 | 1074917 | 968452 | 106439 | 0.0369 |
| devscene:layer-reviewer | Review Finding 4 in general | 2m 18s | 9 | 15115 | 20 | 876451 | 763347 | 113084 | 0.0297 |
| devscene:layer-implementer | Fix Finding 4 review findings | 49.6s | 7 | 5067 | 16 | 453747 | 396942 | 56789 | 0.0106 |
| devscene:layer-reviewer | Re-review Finding 4 in general | 7m 52s | 11 | 15188 | 24 | 993537 | 891627 | 101886 | 0.1009 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $24.88 |
| Cost — claude-opus-5-5 | $24.88 |
| Input tokens (uncached) | 538 |
| Total input tokens (incl. cache) | 30060268 |
| Output tokens | 318918 |
| Thinking tokens (main thread) | 2902 |
| Cache read tokens | 27622115 |
| Cache write tokens | 2437615 |
| Cache write tokens, main thread (5m / 1h) | 0 / 261403 |
| Cache hit ratio | 0.9189 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 150 | 14715068 | 1906 | 14453515 | 261403 |
| sub-agents | 386 | 15245538 | 291457 | 13077772 | 2167380 |
| remainder | 2 | 99662 | 25555 | 90828 | 8832 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 7 (by error: null ×7) |
| Permission denials | 16 |
| Sub-agents spawned / failed / killed | 24 / 0 / 0 |
| terminal_reason | api_error |
| stop_reason | stop_sequence |
| Turns | 110 |
| Time to first token | — |
| Rate-limit peak | seven_day 0.24 |
