# Run analytics — fix_python_gate_run_copies

## Whole run

| Measure | Value |
|---|---|
| Sessions | 8 (0 incomplete) |
| Engine / planning node sessions | 2 / 6 |
| Span | 1h33m |
| Wall | 1h32m |
| Session wall, summed over sessions | 1h34m |
| Active | 1h32m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $35.45 |
| Input tokens (uncached) | 1140 |
| Total input tokens (incl. cache) | 69112815 |
| Output tokens | 340264 |
| Thinking tokens (main thread) | 96019 |
| Cache read tokens | 66795553 |
| Cache write tokens | 2316122 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1233521 |
| Cache hit ratio | 0.9665 |
| Requests | 554 |
| Request latency p50 / p90 / p99 / max | 1.9s / 9.2s / 34.7s / 1m 12s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 22 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — End-of-branch code review — 3m 56s (session 8) |
| Rate-limit peak | seven_day 0.3 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 12m 19s | 12m 19s | 0.0s | 12m 20s | $5.35 |
| 3 | 2-architecture_review | 1m 05s | 1m 05s | 0.0s | 1m 07s | $1.27 |
| 4 | 3-plan_review | 5m 32s | 5m 32s | 0.0s | 5m 34s | $3.71 |
| 5 | 4-plan_writer | 3m 01s | 3m 01s | 0.0s | 3m 03s | $1.04 |
| 6 | 5-architecture_review | 1m 23s | 1m 23s | 0.0s | 1m 24s | $1.47 |
| 7 | 6-plan_review | 4m 33s | 4m 33s | 0.0s | 4m 35s | $2.83 |

## Network refusals

8 of 8 sessions scanned.

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
| Wait (every run of task_round_1) | 35m 14s |
| Gate rows | 28 (complete) |
| Test files — full | 222 files, 17581.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 3 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 1 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2219 s |
| full | 6a | ok | 1 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 19 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1113.5 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 803.4 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 631.0 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 607.4 | 27 | 0 |
| test/remote-run.test.mjs | pass | 607.3 | 130 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 591.2 | 17 | 0 |
| test/remote-control.test.mjs | pass | 558.1 | 83 | 0 |
| test/doctor.test.mjs | pass | 548.0 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 541.7 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 474.3 | 21 | 0 |

## Session 1 — 2026-11-19T08:10:56.998Z → 2026-11-19T08:11:52.102Z

Session id: `c88f7d57-1b07-4117-92fd-c9ccc951f736`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 55.1s | 56.3s | 48.1s | 0.0s | 0.0s | 55.1s | 5.3s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.3s | 2.4s | 4.5s | 4.5s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.9s | 1.9s | 1.9s | 1.9s | 0 |
| orchestrator | 15 | 1.3s | 2.4s | 4.5s | 4.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 5.3s | 5.3s |
| Bash | orchestrator | 14 | 9.0s | 5.5s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:11:40.083Z | 5.5s | 587 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:21.902Z | 0.3s | 153 | false | false |
| Bash | orchestrator | 2026-11-19T08:10:59.707Z | 0.3s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:47.186Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:10.197Z | 0.2s | 115 | true | false |
| Bash | orchestrator | 2026-11-19T08:11:28.958Z | 0.2s | 1064 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:23.626Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:08.224Z | 0.2s | 154 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:03.627Z | 0.2s | 1120 | true | false |
| Read | orchestrator | 2026-11-19T08:11:30.997Z | 0.2s | 26508 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 5.3s | 1 | 458 | 4 | 26952 | 10486 | 16462 | 0.0974 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.83 |
| Cost — claude-opus-5-5 | $0.83 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 885718 |
| Output tokens | 5384 |
| Thinking tokens (main thread) | 335 |
| Cache read tokens | 809490 |
| Cache write tokens | 76194 |
| Cache write tokens, main thread (5m / 1h) | 0 / 59732 |
| Cache hit ratio | 0.9139 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 30 | 858766 | 694 | 799004 | 59732 |
| sub-agents | 4 | 26952 | 458 | 10486 | 16462 |
| remainder | 0 | 0 | 4232 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 24 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.29 |

## Session 2 — 2026-11-19T08:11:55.323Z → 2026-11-19T08:24:14.594Z

Session id: `64728ed5-b8c6-4ea6-a03c-a1c060ccc7bf`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 12m 19s | 12m 20s | 12m 07s | 0.0s | 0.0s | 12m 19s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 64 | 2.3s | 23.2s | 1m 12s | 1m 12s | 0 |
| orchestrator | 64 | 2.3s | 23.2s | 1m 12s | 1m 12s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 44 | 12.5s | 1.0s |
| Edit | orchestrator | 2 | 0.0s | 0.0s |
| Read | orchestrator | 21 | 1.1s | 0.3s |
| Write | orchestrator | 7 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:12:12.939Z | 1.0s | 14029 | false | false |
| Bash | orchestrator | 2026-11-19T08:12:22.733Z | 0.5s | 208 | false | false |
| Bash | orchestrator | 2026-11-19T08:11:55.406Z | 0.4s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:16:37.743Z | 0.4s | 3171 | false | false |
| Bash | orchestrator | 2026-11-19T08:17:04.282Z | 0.3s | 3810 | false | false |
| Bash | orchestrator | 2026-11-19T08:18:13.018Z | 0.3s | 1004 | false | false |
| Bash | orchestrator | 2026-11-19T08:16:48.682Z | 0.3s | 1151 | false | false |
| Bash | orchestrator | 2026-11-19T08:18:25.530Z | 0.3s | 233 | false | false |
| Bash | orchestrator | 2026-11-19T08:21:09.536Z | 0.3s | 465 | false | false |
| Read | orchestrator | 2026-11-19T08:12:00.363Z | 0.3s | 46614 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $5.35 |
| Cost — claude-opus-5-5 | $5.35 |
| Input tokens (uncached) | 128 |
| Total input tokens (incl. cache) | 10052911 |
| Output tokens | 76282 |
| Thinking tokens (main thread) | 46327 |
| Cache read tokens | 9819675 |
| Cache write tokens | 233108 |
| Cache write tokens, main thread (5m / 1h) | 0 / 233108 |
| Cache hit ratio | 0.9768 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 128 | 10052911 | 652 | 9819675 | 233108 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 75630 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 75 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.29 |

## Session 3 — 2026-11-19T08:24:18.028Z → 2026-11-19T08:25:23.778Z

Session id: `6d2a6f03-af8f-4426-87f7-eddba68b7729`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 05s | 1m 07s | 1m 04s | 0.0s | 0.0s | 1m 05s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.8s | 8.2s | 10.1s | 10.1s | 0 |
| orchestrator | 16 | 1.8s | 8.2s | 10.1s | 10.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 10 | 2.6s | 0.4s |
| Read | orchestrator | 16 | 0.7s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:24:18.032Z | 0.4s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:58.176Z | 0.3s | 1778 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:49.108Z | 0.3s | 3290 | false | false |
| Read | orchestrator | 2026-11-19T08:24:28.654Z | 0.2s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:33.509Z | 0.2s | 7167 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:55.235Z | 0.2s | 3526 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:20.685Z | 0.2s | 6294 | false | false |
| Read | orchestrator | 2026-11-19T08:24:29.694Z | 0.2s | 31668 | false | false |
| Bash | orchestrator | 2026-11-19T08:25:09.408Z | 0.1s | 1181 | false | false |
| Bash | orchestrator | 2026-11-19T08:25:13.511Z | 0.1s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.27 |
| Cost — claude-opus-5-5 | $1.27 |
| Input tokens (uncached) | 32 |
| Total input tokens (incl. cache) | 1293643 |
| Output tokens | 6757 |
| Thinking tokens (main thread) | 2521 |
| Cache read tokens | 1181142 |
| Cache write tokens | 112469 |
| Cache write tokens, main thread (5m / 1h) | 0 / 112469 |
| Cache hit ratio | 0.913 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 1293643 | 210 | 1181142 | 112469 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 6547 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 28 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.29 |

## Session 4 — 2026-11-19T08:24:18.033Z → 2026-11-19T08:29:50.467Z

Session id: `22a7bf37-c90d-4a6a-b102-16e659dd8772`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 32s | 5m 34s | 5m 23s | 0.0s | 0.0s | 5m 32s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 50 | 2.6s | 11.9s | 22.6s | 22.6s | 0 |
| orchestrator | 50 | 2.6s | 11.9s | 22.6s | 22.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 40 | 11.2s | 0.6s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | orchestrator | 27 | 1.1s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:27:08.680Z | 0.6s | 1751 | false | false |
| Bash | orchestrator | 2026-11-19T08:28:21.755Z | 0.4s | 1641 | false | false |
| Bash | orchestrator | 2026-11-19T08:24:18.036Z | 0.4s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:28:08.565Z | 0.4s | 419 | false | false |
| Bash | orchestrator | 2026-11-19T08:26:44.844Z | 0.4s | 465 | false | false |
| Bash | orchestrator | 2026-11-19T08:28:40.190Z | 0.3s | 4093 | false | false |
| Bash | orchestrator | 2026-11-19T08:26:45.900Z | 0.3s | 64 | false | false |
| Bash | orchestrator | 2026-11-19T08:27:30.158Z | 0.3s | 1180 | false | false |
| Bash | orchestrator | 2026-11-19T08:28:37.626Z | 0.3s | 83 | false | false |
| Read | orchestrator | 2026-11-19T08:24:34.951Z | 0.3s | 46614 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.71 |
| Cost — claude-opus-5-5 | $3.71 |
| Input tokens (uncached) | 100 |
| Total input tokens (incl. cache) | 7329955 |
| Output tokens | 32839 |
| Thinking tokens (main thread) | 18664 |
| Cache read tokens | 7126217 |
| Cache write tokens | 203638 |
| Cache write tokens, main thread (5m / 1h) | 0 / 203638 |
| Cache hit ratio | 0.9722 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 100 | 7329955 | 1186 | 7126217 | 203638 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 31653 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 70 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.29 |

## Session 5 — 2026-11-19T08:30:00.558Z → 2026-11-19T08:33:02.234Z

Session id: `215af7c8-3464-49f9-b89d-57755bd4d497`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 01s | 3m 03s | 3m 01s | 0.0s | 0.0s | 3m 01s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 2.1s | 23.7s | 25.7s | 25.7s | 0 |
| orchestrator | 17 | 2.1s | 23.7s | 25.7s | 25.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.0s | 0.4s |
| Edit | orchestrator | 29 | 1.1s | 0.0s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:30:00.969Z | 0.4s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:30:12.335Z | 0.3s | 4596 | false | false |
| Bash | orchestrator | 2026-11-19T08:32:43.260Z | 0.2s | 372 | false | false |
| Bash | orchestrator | 2026-11-19T08:30:03.641Z | 0.2s | 15811 | false | false |
| Bash | orchestrator | 2026-11-19T08:30:39.114Z | 0.2s | 4599 | false | false |
| Bash | orchestrator | 2026-11-19T08:32:16.788Z | 0.2s | 4814 | false | false |
| Bash | orchestrator | 2026-11-19T08:31:28.801Z | 0.1s | 727 | true | true |
| Bash | orchestrator | 2026-11-19T08:30:05.453Z | 0.1s | 727 | true | true |
| Edit | orchestrator | 2026-11-19T08:31:37.398Z | 0.0s | 228 | false | false |
| Edit | orchestrator | 2026-11-19T08:31:40.148Z | 0.0s | 228 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.04 |
| Cost — claude-opus-5-5 | $1.04 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 883216 |
| Output tokens | 20981 |
| Thinking tokens (main thread) | 5722 |
| Cache read tokens | 826174 |
| Cache write tokens | 57008 |
| Cache write tokens, main thread (5m / 1h) | 0 / 57008 |
| Cache hit ratio | 0.9354 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 883216 | 192 | 826174 | 57008 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 20789 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 46 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.29 |

## Session 6 — 2026-11-19T08:33:05.744Z → 2026-11-19T08:34:28.995Z

Session id: `1185d480-278d-4cdc-85fb-f6714c89bf7e`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 23s | 1m 24s | 1m 21s | 0.0s | 0.0s | 1m 23s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 2.2s | 11.8s | 13.2s | 13.2s | 0 |
| orchestrator | 16 | 2.2s | 11.8s | 13.2s | 13.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 12 | 3.6s | 0.6s |
| Read | orchestrator | 17 | 1.0s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:33:05.961Z | 0.6s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:38.910Z | 0.4s | 1261 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:06.711Z | 0.3s | 5561 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:49.965Z | 0.3s | 1099 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:34.031Z | 0.3s | 1938 | false | false |
| Read | orchestrator | 2026-11-19T08:33:18.005Z | 0.2s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:43.520Z | 0.2s | 4106 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:54.904Z | 0.2s | 8257 | false | false |
| Read | orchestrator | 2026-11-19T08:33:20.503Z | 0.2s | 63280 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:48.245Z | 0.2s | 42 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.47 |
| Cost — claude-opus-5-5 | $1.47 |
| Input tokens (uncached) | 32 |
| Total input tokens (incl. cache) | 1615241 |
| Output tokens | 8587 |
| Thinking tokens (main thread) | 4026 |
| Cache read tokens | 1490621 |
| Cache write tokens | 124588 |
| Cache write tokens, main thread (5m / 1h) | 0 / 124588 |
| Cache hit ratio | 0.9228 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 1615241 | 925 | 1490621 | 124588 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7662 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 31 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.29 |

## Session 7 — 2026-11-19T08:33:05.833Z → 2026-11-19T08:37:39.350Z

Session id: `e2985ce3-da5a-432b-9377-4c74d9ca1088`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 33s | 4m 35s | 4m 25s | 0.0s | 0.0s | 4m 33s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 42 | 2.2s | 10.1s | 33.0s | 33.0s | 0 |
| orchestrator | 42 | 2.2s | 10.1s | 33.0s | 33.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 30 | 8.7s | 0.8s |
| Read | orchestrator | 23 | 0.8s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T08:34:35.031Z | 0.8s | 1065 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:05.843Z | 0.6s | 54 | false | false |
| Bash | orchestrator | 2026-11-19T08:34:45.034Z | 0.3s | 540 | false | false |
| Bash | orchestrator | 2026-11-19T08:34:39.530Z | 0.3s | 896 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:11.550Z | 0.3s | 1720 | false | false |
| Bash | orchestrator | 2026-11-19T08:34:30.457Z | 0.3s | 2735 | false | false |
| Bash | orchestrator | 2026-11-19T08:35:20.827Z | 0.3s | 401 | false | false |
| Bash | orchestrator | 2026-11-19T08:34:17.983Z | 0.3s | 10323 | false | false |
| Bash | orchestrator | 2026-11-19T08:33:49.202Z | 0.3s | 934 | false | false |
| Bash | orchestrator | 2026-11-19T08:34:27.880Z | 0.2s | 3850 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.83 |
| Cost — claude-opus-5-5 | $2.83 |
| Input tokens (uncached) | 84 |
| Total input tokens (incl. cache) | 5027144 |
| Output tokens | 27439 |
| Thinking tokens (main thread) | 16163 |
| Cache read tokens | 4863112 |
| Cache write tokens | 163948 |
| Cache write tokens, main thread (5m / 1h) | 0 / 163948 |
| Cache hit ratio | 0.9674 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 84 | 5027144 | 1121 | 4863112 | 163948 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 26318 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 55 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.29 |

## Session 8 — 2026-11-19T08:38:13.178Z → 2026-11-19T09:44:17.327Z

Session id: `1cef8287-d044-4991-8ff3-697e8549cb01`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h06m | 1h06m | 24m 53s | 0.0s | 0.0s | 1h06m | 22m 01s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 333 | 1.8s | 6.0s | 29.5s | 52.8s | 0 |
| devscene:architecture-reviewer | 9 | 2.2s | 5.4s | 5.4s | 5.4s | 0 |
| devscene:branch-reviewer | 32 | 3.4s | 13.9s | 31.6s | 31.6s | 0 |
| devscene:layer-implementer | 124 | 2.1s | 6.6s | 43.4s | 52.8s | 0 |
| devscene:review-plan-reviewer | 7 | 2.0s | 6.1s | 6.1s | 6.1s | 0 |
| devscene:skeptic-reviewer | 33 | 3.2s | 10.6s | 19.7s | 19.7s | 0 |
| devscene:statistics-plan-writer | 7 | 1.6s | 16.8s | 16.8s | 16.8s | 0 |
| orchestrator | 121 | 1.6s | 2.0s | 4.7s | 7.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 14 | 22m 01s | 3m 56s |
| Bash | devscene:architecture-reviewer | 8 | 2.2s | 0.3s |
| Bash | devscene:branch-reviewer | 28 | 10.1s | 0.9s |
| Bash | devscene:layer-implementer | 102 | 2m 22s | 18.9s |
| Bash | devscene:review-plan-reviewer | 6 | 1.7s | 0.4s |
| Bash | devscene:skeptic-reviewer | 30 | 7.2s | 0.4s |
| Bash | devscene:statistics-plan-writer | 7 | 1.9s | 0.3s |
| Bash | orchestrator | 149 | 39m 17s | 1m 03s |
| Edit | devscene:layer-implementer | 31 | 1.3s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Read | devscene:architecture-reviewer | 9 | 0.7s | 0.2s |
| Read | devscene:branch-reviewer | 10 | 0.6s | 0.2s |
| Read | devscene:layer-implementer | 46 | 3.4s | 0.2s |
| Read | devscene:review-plan-reviewer | 12 | 0.7s | 0.3s |
| Read | devscene:skeptic-reviewer | 7 | 0.1s | 0.0s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | orchestrator | 9 | 1.7s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 6 | 0.2s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T09:10:47.983Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:11:53.255Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:06:32.753Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:34:08.889Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:05:28.178Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:21:26.229Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:27:47.350Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:17:12.290Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:35:16.437Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T09:28:51.351Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 8 | 42.4s |
| devscene:layer-implementer | git diff --name-only HEAD | 4 | 6.9s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 3 | 6.3s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 4 | 22.5s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/fix_python_gate_run_copies_code_revie | 3 | 17.9s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/fix_python_gate_run_copies_story_plan.md --id | 6 | 35.8s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 35 | 35m 14s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; echo checked | 34 | 25.0s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 12 | 3.0s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 general layer | 1m 49s | 15 | 12089 | 32 | 839380 | 777463 | 61885 | 0.0275 |
| devscene:layer-implementer | Implement Task 2 general layer | 34.6s | 8 | 3097 | 18 | 476993 | 421638 | 55337 | 0.0087 |
| devscene:layer-implementer | Implement Task 3 general layer | 2m 01s | 25 | 12450 | 52 | 1919447 | 1843505 | 75890 | 0.0305 |
| devscene:layer-implementer | Implement Task 4 cli layer | 3m 24s | 16 | 18449 | 34 | 1210389 | 1132281 | 78074 | 0.0515 |
| devscene:layer-implementer | Implement Task 5 cli layer | 55.1s | 10 | 4404 | 22 | 610473 | 558050 | 52401 | 0.0139 |
| devscene:layer-implementer | Implement Task 6 general layer | 1m 54s | 22 | 11055 | 46 | 1847993 | 1762815 | 85132 | 0.0288 |
| devscene:architecture-reviewer | Architecture review implemented branch | 46.7s | 9 | 4596 | 20 | 939046 | 805372 | 133654 | 0.0118 |
| devscene:branch-reviewer | End-of-branch code review | 3m 56s | 32 | 24166 | 66 | 3650494 | 3486263 | 164165 | 0.0597 |
| devscene:review-plan-reviewer | Meta-review code review | 42.0s | 7 | 4417 | 16 | 429288 | 342683 | 86589 | 0.0106 |
| devscene:layer-implementer | Fix code-review Finding 3 | 33.7s | 9 | 2343 | 20 | 392032 | 350207 | 41805 | 0.0085 |
| devscene:layer-implementer | Fix code-review Finding 2 | 30.5s | 7 | 2484 | 16 | 320469 | 278325 | 42128 | 0.0077 |
| devscene:layer-implementer | Fix code-review Finding 1 | 1m 03s | 12 | 5894 | 26 | 670724 | 621972 | 48726 | 0.016 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 3m 14s | 33 | 18431 | 68 | 2317927 | 2212111 | 105748 | 0.049 |
| devscene:statistics-plan-writer | Write branch statistics | 36.4s | 7 | 4459 | 16 | 253450 | 218829 | 34605 | 0.0092 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $18.94 |
| Cost — claude-opus-5-5 | $18.94 |
| Input tokens (uncached) | 696 |
| Total input tokens (incl. cache) | 42024987 |
| Output tokens | 161995 |
| Thinking tokens (main thread) | 2261 |
| Cache read tokens | 40679122 |
| Cache write tokens | 1345169 |
| Cache write tokens, main thread (5m / 1h) | 0 / 279030 |
| Cache hit ratio | 0.968 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 244 | 26146882 | 3040 | 25867608 | 279030 |
| sub-agents | 452 | 15878105 | 128334 | 14811514 | 1066139 |
| remainder | 0 | 0 | 30621 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 14 |
| Sub-agents spawned / failed / killed | 14 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 187 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.3 |
