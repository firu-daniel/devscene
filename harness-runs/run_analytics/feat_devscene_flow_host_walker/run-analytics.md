# Run analytics — feat_devscene_flow_host_walker

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 1h26m |
| Wall | 1h26m |
| Session wall, summed over sessions | 1h29m |
| Active | 1h26m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $32.96 |
| Input tokens (uncached) | 1058 |
| Total input tokens (incl. cache) | 68849935 |
| Output tokens | 296627 |
| Thinking tokens (main thread) | 66437 |
| Cache read tokens | 66736259 |
| Cache write tokens | 2112618 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1036630 |
| Cache hit ratio | 0.9693 |
| Requests | 512 |
| Request latency p50 / p90 / p99 / max | 1.7s / 7.8s / 40.1s / 1m 04s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 19 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — End-of-branch code review — 4m 58s (session 5) |
| Rate-limit peak | seven_day 0.6 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 9m 58s | 9m 58s | 0.0s | 9m 59s | $4.82 |
| 3 | 2-architecture_review | 2m 45s | 2m 45s | 0.0s | 2m 46s | $2.08 |
| 4 | 3-plan_review | 5m 06s | 5m 06s | 0.0s | 5m 07s | $3.62 |

## Network refusals

5 of 5 sessions scanned.

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
| Wait (every run of task_round_1) | 37m 07s |
| Gate rows | 37 (complete) |
| Test files — full | 223 files, 18146.6 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 1 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 2 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 3g | ok | 1 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2280 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 18 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 6 s |
| full | 13h | ok | 0 s |
| full | 13i | ok | 1 s |
| full | 13j | ok | 3 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 223)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1147.3 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 823.3 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 649.7 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 638.8 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 616.9 | 17 | 0 |
| test/remote-run.test.mjs | pass | 612.2 | 130 | 0 |
| test/doctor.test.mjs | pass | 575.0 | 1 | 0 |
| test/remote-control.test.mjs | pass | 549.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 527.6 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 491.3 | 21 | 0 |

## Session 1 — 2026-11-23T16:14:04.979Z → 2026-11-23T16:15:01.832Z

Session id: `a9201937-b724-4145-b554-171e82e1306c`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 56.8s | 58.1s | 48.4s | 0.0s | 0.0s | 56.8s | 3.8s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 1.2s | 1.7s | 4.3s | 4.3s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.5s | 1.5s | 1.5s | 1.5s | 0 |
| orchestrator | 17 | 1.2s | 1.7s | 4.3s | 4.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 3.8s | 3.8s |
| Bash | orchestrator | 13 | 10.0s | 6.5s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 6 | 0.5s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:14:50.993Z | 6.5s | 603 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:15.156Z | 0.4s | 158 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:16.926Z | 0.4s | 6 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:07.142Z | 0.3s | 58 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:11.413Z | 0.3s | 10039 | true | false |
| Bash | orchestrator | 2026-11-23T16:14:27.752Z | 0.2s | 157 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:36.357Z | 0.2s | 1064 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:31.000Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:40.053Z | 0.2s | 171 | true | false |
| Bash | orchestrator | 2026-11-23T16:14:33.013Z | 0.2s | 488 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 3.8s | 1 | 324 | 4 | 31744 | 11534 | 20206 | 0.0678 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.18 |
| Cost — claude-opus-5-5 | $1.18 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 1376157 |
| Output tokens | 5516 |
| Thinking tokens (main thread) | 380 |
| Cache read tokens | 1267128 |
| Cache write tokens | 108989 |
| Cache write tokens, main thread (5m / 1h) | 0 / 88783 |
| Cache hit ratio | 0.9208 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 36 | 1344413 | 765 | 1255594 | 88783 |
| sub-agents | 4 | 31744 | 324 | 11534 | 20206 |
| remainder | 0 | 0 | 4427 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 25 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.57 |

## Session 2 — 2026-11-23T16:15:05.528Z → 2026-11-23T16:25:03.644Z

Session id: `11558ee1-629f-4d81-8ad5-f42261f85fe1`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 9m 58s | 9m 59s | 9m 48s | 0.0s | 0.0s | 9m 58s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 43 | 1.8s | 23.5s | 1m 04s | 1m 04s | 0 |
| orchestrator | 43 | 1.8s | 23.5s | 1m 04s | 1m 04s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 30 | 9.8s | 0.7s |
| Edit | orchestrator | 1 | 0.0s | 0.0s |
| Read | orchestrator | 26 | 1.2s | 0.2s |
| Write | orchestrator | 9 | 0.4s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:19:35.541Z | 0.7s | 2840 | false | false |
| Bash | orchestrator | 2026-11-23T16:15:05.805Z | 0.6s | 58 | false | false |
| Bash | orchestrator | 2026-11-23T16:17:58.670Z | 0.4s | 24957 | false | false |
| Bash | orchestrator | 2026-11-23T16:24:47.895Z | 0.4s | 370 | false | false |
| Bash | orchestrator | 2026-11-23T16:16:13.402Z | 0.4s | 5507 | false | false |
| Bash | orchestrator | 2026-11-23T16:19:45.794Z | 0.3s | 281 | false | false |
| Bash | orchestrator | 2026-11-23T16:15:53.335Z | 0.3s | 7801 | false | false |
| Bash | orchestrator | 2026-11-23T16:19:47.792Z | 0.3s | 1104 | false | false |
| Bash | orchestrator | 2026-11-23T16:15:24.370Z | 0.3s | 1989 | false | false |
| Bash | orchestrator | 2026-11-23T16:15:46.850Z | 0.3s | 7979 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $4.82 |
| Cost — claude-opus-5-5 | $4.82 |
| Input tokens (uncached) | 86 |
| Total input tokens (incl. cache) | 7102734 |
| Output tokens | 66929 |
| Thinking tokens (main thread) | 31516 |
| Cache read tokens | 6838300 |
| Cache write tokens | 264348 |
| Cache write tokens, main thread (5m / 1h) | 0 / 264348 |
| Cache hit ratio | 0.9628 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 86 | 7102734 | 462 | 6838300 | 264348 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 66467 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 67 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.58 |

## Session 3 — 2026-11-23T16:25:07.920Z → 2026-11-23T16:27:53.294Z

Session id: `894bfcba-db7c-4030-bcc0-c749c19f6fd1`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 45s | 2m 46s | 2m 43s | 0.0s | 0.0s | 2m 45s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 1.3s | 24.0s | 32.9s | 32.9s | 0 |
| orchestrator | 18 | 1.3s | 24.0s | 32.9s | 32.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 10 | 3.2s | 0.5s |
| Read | orchestrator | 25 | 1.1s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:25:08.071Z | 0.5s | 58 | false | false |
| Bash | orchestrator | 2026-11-23T16:25:10.521Z | 0.4s | 6989 | false | false |
| Bash | orchestrator | 2026-11-23T16:25:28.435Z | 0.3s | 1112 | false | false |
| Bash | orchestrator | 2026-11-23T16:25:13.731Z | 0.3s | 1943 | false | false |
| Read | orchestrator | 2026-11-23T16:25:16.313Z | 0.2s | 39020 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:18.488Z | 0.2s | 1231 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:17.234Z | 0.2s | 385 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:09.936Z | 0.2s | 727 | true | true |
| Bash | orchestrator | 2026-11-23T16:26:16.401Z | 0.2s | 34 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:28.367Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.08 |
| Cost — claude-opus-5-5 | $2.08 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 1975707 |
| Output tokens | 17602 |
| Thinking tokens (main thread) | 10483 |
| Cache read tokens | 1805169 |
| Cache write tokens | 170502 |
| Cache write tokens, main thread (5m / 1h) | 0 / 170502 |
| Cache hit ratio | 0.9137 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 36 | 1975707 | 937 | 1805169 | 170502 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 16665 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 37 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.58 |

## Session 4 — 2026-11-23T16:25:07.847Z → 2026-11-23T16:30:14.253Z

Session id: `26fda19f-d73e-4f6c-9eb1-12d838af1295`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 06s | 5m 07s | 4m 57s | 0.0s | 0.0s | 5m 06s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 37 | 2.1s | 16.4s | 43.0s | 43.0s | 0 |
| orchestrator | 37 | 2.1s | 16.4s | 43.0s | 43.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 29 | 9.2s | 0.6s |
| Read | orchestrator | 25 | 1.3s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:25:07.997Z | 0.6s | 58 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:04.967Z | 0.4s | 1308 | false | false |
| Bash | orchestrator | 2026-11-23T16:25:10.552Z | 0.4s | 6973 | false | false |
| Bash | orchestrator | 2026-11-23T16:25:27.776Z | 0.3s | 1318 | false | false |
| Bash | orchestrator | 2026-11-23T16:29:19.643Z | 0.3s | 710 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:01.677Z | 0.3s | 7991 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:12.624Z | 0.3s | 3432 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:37.767Z | 0.3s | 6757 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:01.394Z | 0.3s | 2091 | false | false |
| Bash | orchestrator | 2026-11-23T16:28:14.505Z | 0.3s | 7817 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.62 |
| Cost — claude-opus-5-5 | $3.62 |
| Input tokens (uncached) | 74 |
| Total input tokens (incl. cache) | 5924018 |
| Output tokens | 32332 |
| Thinking tokens (main thread) | 21070 |
| Cache read tokens | 5694404 |
| Cache write tokens | 229540 |
| Cache write tokens, main thread (5m / 1h) | 0 / 229540 |
| Cache hit ratio | 0.9612 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 74 | 5924018 | 1051 | 5694404 | 229540 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 31281 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 56 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.58 |

## Session 5 — 2026-11-23T16:30:46.689Z → 2026-11-23T17:41:01.921Z

Session id: `6de420fa-3442-4f1a-8898-f9eb678b63cb`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h10m | 1h10m | 25m 49s | 0.0s | 0.0s | 1h10m | 23m 52s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 396 | 1.7s | 5.0s | 19.6s | 42.7s | 0 |
| devscene:architecture-reviewer | 10 | 1.8s | 2.4s | 8.4s | 8.4s | 0 |
| devscene:branch-reviewer | 40 | 2.5s | 11.6s | 42.7s | 42.7s | 0 |
| devscene:layer-implementer | 139 | 2.0s | 5.0s | 16.3s | 17.3s | 0 |
| devscene:review-plan-reviewer | 16 | 2.1s | 5.4s | 12.8s | 12.8s | 0 |
| devscene:skeptic-reviewer | 31 | 3.0s | 12.0s | 19.6s | 19.6s | 0 |
| devscene:statistics-plan-writer | 8 | 1.4s | 16.4s | 16.4s | 16.4s | 0 |
| orchestrator | 152 | 1.5s | 2.0s | 6.9s | 7.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 15 | 23m 52s | 4m 58s |
| Bash | devscene:architecture-reviewer | 8 | 2.4s | 0.6s |
| Bash | devscene:branch-reviewer | 30 | 11.5s | 1.8s |
| Bash | devscene:layer-implementer | 116 | 3m 29s | 22.8s |
| Bash | devscene:review-plan-reviewer | 12 | 3.8s | 1.0s |
| Bash | devscene:skeptic-reviewer | 27 | 7.4s | 0.4s |
| Bash | devscene:statistics-plan-writer | 11 | 2.4s | 0.2s |
| Bash | orchestrator | 124 | 41m 15s | 1m 03s |
| Edit | devscene:layer-implementer | 26 | 1.1s | 0.0s |
| Edit | orchestrator | 12 | 0.5s | 0.0s |
| Read | devscene:architecture-reviewer | 8 | 0.6s | 0.3s |
| Read | devscene:branch-reviewer | 20 | 0.9s | 0.2s |
| Read | devscene:layer-implementer | 51 | 2.7s | 0.9s |
| Read | devscene:review-plan-reviewer | 13 | 0.5s | 0.3s |
| Read | devscene:skeptic-reviewer | 10 | 0.1s | 0.0s |
| Read | devscene:statistics-plan-writer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 17 | 2.9s | 0.5s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 6 | 0.2s | 0.0s |
| Write | devscene:layer-implementer | 16 | 0.6s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T17:03:57.257Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:01:48.488Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:02:52.828Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:30:15.110Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:08:11.714Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:20:48.275Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:17:39.428Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:33:23.376Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:06:04.887Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-23T17:11:21.507Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py | 7 | 7.5s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_config.py | 3 | 2.8s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_layers.py | 3 | 11.0s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_walking.py | 3 | 3.3s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 14 | 2m 12s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 10 | 2.2s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_devscene_flow_host_walker_story_plan.md  | 8 | 50.7s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 37 | 37m 07s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 13 | 14.3s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 | 1m 53s | 18 | 9153 | 38 | 886998 | 831306 | 55654 | 0.0269 |
| devscene:layer-implementer | Implement Task 2 | 1m 03s | 9 | 6689 | 20 | 667154 | 598035 | 69099 | 0.0151 |
| devscene:layer-implementer | Implement Task 3 | 1m 07s | 10 | 6491 | 22 | 445276 | 411492 | 33762 | 0.0161 |
| devscene:layer-implementer | Implement Task 4 | 1m 16s | 13 | 6875 | 28 | 552767 | 519020 | 33719 | 0.0182 |
| devscene:layer-implementer | Implement Task 5 | 57.5s | 10 | 5484 | 22 | 465381 | 427810 | 37549 | 0.0136 |
| devscene:layer-implementer | Implement Task 6 | 1m 49s | 23 | 10052 | 48 | 1292444 | 1239251 | 53145 | 0.026 |
| devscene:layer-implementer | Implement Task 7 | 1m 05s | 11 | 6263 | 24 | 488614 | 447950 | 40640 | 0.0156 |
| devscene:layer-implementer | Implement Task 8 | 1m 22s | 21 | 7267 | 44 | 1670622 | 1590992 | 79586 | 0.0195 |
| devscene:architecture-reviewer | Architecture review of branch | 49.9s | 10 | 4992 | 22 | 810389 | 700409 | 109958 | 0.0118 |
| devscene:branch-reviewer | End-of-branch code review | 4m 58s | 40 | 33038 | 82 | 6642299 | 6423638 | 218579 | 0.0709 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 20s | 16 | 8148 | 34 | 1162373 | 1059786 | 102553 | 0.0191 |
| devscene:layer-implementer | Fix code-review Finding 1 | 45.0s | 8 | 3846 | 18 | 307768 | 270750 | 37000 | 0.0107 |
| devscene:layer-implementer | Fix code-review Finding 2 | 1m 29s | 16 | 8841 | 34 | 779960 | 738291 | 41635 | 0.0212 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 3m 14s | 31 | 19333 | 64 | 2321645 | 2210718 | 110863 | 0.0462 |
| devscene:statistics-plan-writer | Write branch statistics | 37.3s | 8 | 4551 | 18 | 270830 | 238772 | 32040 | 0.0089 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $21.26 |
| Cost — claude-opus-5-5 | $21.26 |
| Input tokens (uncached) | 822 |
| Total input tokens (incl. cache) | 52471319 |
| Output tokens | 174248 |
| Thinking tokens (main thread) | 2988 |
| Cache read tokens | 51131258 |
| Cache write tokens | 1339239 |
| Cache write tokens, main thread (5m / 1h) | 0 / 283457 |
| Cache hit ratio | 0.9745 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 304 | 33706799 | 3815 | 33423038 | 283457 |
| sub-agents | 518 | 18764520 | 141023 | 17708220 | 1055782 |
| remainder | 0 | 0 | 29410 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 18 |
| Sub-agents spawned / failed / killed | 15 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 171 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.6 |
