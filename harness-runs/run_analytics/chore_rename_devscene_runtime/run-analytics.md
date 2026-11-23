# Run analytics — chore_rename_devscene_runtime

## Whole run

| Measure | Value |
|---|---|
| Sessions | 11 (0 incomplete) |
| Engine / planning node sessions | 2 / 9 |
| Span | 46m 54s |
| Wall | 45m 46s |
| Session wall, summed over sessions | 50m 13s |
| Active | 34m 59s |
| Host-suspended | 0.0s |
| Idle | 10m 47s |
| Cost | $26.93 |
| Input tokens (uncached) | 700 |
| Total input tokens (incl. cache) | 34376939 |
| Output tokens | 323909 |
| Thinking tokens (main thread) | 95937 |
| Cache read tokens | 32409534 |
| Cache write tokens | 1966705 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1376922 |
| Cache hit ratio | 0.9428 |
| Requests | 342 |
| Request latency p50 / p90 / p99 / max | 1.9s / 11.7s / 31.5s / 10m 47s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 15 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 1 (general) — 14m 08s (session 11) |
| Rate-limit peak | seven_day 0.54 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 7m 19s | 7m 19s | 0.0s | 7m 20s | $2.99 |
| 3 | 2-architecture_review | 2m 06s | 2m 06s | 0.0s | 2m 07s | $1.56 |
| 4 | 3-plan_review | 4m 08s | 4m 08s | 0.0s | 4m 09s | $3.05 |
| 5 | 4-plan_writer | 2m 37s | 2m 37s | 0.0s | 2m 38s | $1.03 |
| 6 | 5-architecture_review | 1m 37s | 1m 37s | 0.0s | 1m 38s | $1.62 |
| 7 | 6-plan_review | 3m 30s | 3m 30s | 0.0s | 3m 32s | $2.31 |
| 8 | 7-plan_writer | 5m 08s | 5m 08s | 0.0s | 5m 09s | $2.01 |
| 9 | 8-architecture_review | 42.3s | 42.3s | 0.0s | 43.2s | $1.18 |
| 10 | 9-plan_review | 2m 16s | 2m 16s | 0.0s | 2m 17s | $1.34 |

## Network refusals

11 of 11 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No Run gates round log was scanned.

## Session 1 — 2026-11-23T07:24:30.444Z → 2026-11-23T07:25:20.873Z

Session id: `9f6c710b-34c0-4584-a517-d9a16d1d062a`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 50.4s | 51.4s | 42.6s | 0.0s | 0.0s | 50.4s | 4.9s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.0s | 1.9s | 5.0s | 5.0s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.3s | 1.3s | 1.3s | 1.3s | 0 |
| orchestrator | 15 | 0.9s | 1.9s | 5.0s | 5.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 4.9s | 4.9s |
| Bash | orchestrator | 11 | 8.7s | 5.7s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:25:10.107Z | 5.7s | 599 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:33.128Z | 0.4s | 286 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:55.089Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:52.609Z | 0.3s | 156 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:38.831Z | 0.3s | 157 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:34.479Z | 0.2s | 8683 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:40.223Z | 0.2s | 6 | false | false |
| Bash | orchestrator | 2026-11-23T07:25:01.301Z | 0.2s | 219 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:37.076Z | 0.2s | 15468 | false | false |
| Bash | orchestrator | 2026-11-23T07:24:57.145Z | 0.2s | 10370 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 4.9s | 1 | 440 | 4 | 30624 | 11476 | 19144 | 0.099 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.84 |
| Cost — claude-opus-5-5 | $0.84 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 894207 |
| Output tokens | 4945 |
| Thinking tokens (main thread) | 327 |
| Cache read tokens | 815299 |
| Cache write tokens | 78872 |
| Cache write tokens, main thread (5m / 1h) | 0 / 59728 |
| Cache hit ratio | 0.9118 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 863583 | 230 | 803823 | 59728 |
| sub-agents | 4 | 30624 | 440 | 11476 | 19144 |
| remainder | 0 | 0 | 4275 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 17 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.53 |

## Session 2 — 2026-11-23T07:25:23.764Z → 2026-11-23T07:32:43.529Z

Session id: `8fb5789e-fd7d-429d-b9e2-3f1f90a12a01`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 7m 19s | 7m 20s | 7m 11s | 0.0s | 0.0s | 7m 19s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 34 | 2.3s | 19.6s | 1m 03s | 1m 03s | 0 |
| orchestrator | 34 | 2.3s | 19.6s | 1m 03s | 1m 03s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 24 | 8.7s | 1.4s |
| Edit | orchestrator | 4 | 0.1s | 0.0s |
| Read | orchestrator | 11 | 0.7s | 0.3s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:26:17.065Z | 1.4s | 5555 | false | false |
| Bash | orchestrator | 2026-11-23T07:31:50.210Z | 0.5s | 983 | false | false |
| Bash | orchestrator | 2026-11-23T07:28:55.876Z | 0.5s | 738 | false | false |
| Bash | orchestrator | 2026-11-23T07:28:42.143Z | 0.5s | 714 | false | false |
| Bash | orchestrator | 2026-11-23T07:25:24.070Z | 0.4s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:28:45.890Z | 0.3s | 107 | false | false |
| Bash | orchestrator | 2026-11-23T07:25:38.068Z | 0.3s | 16554 | false | false |
| Bash | orchestrator | 2026-11-23T07:26:12.544Z | 0.3s | 8583 | false | false |
| Bash | orchestrator | 2026-11-23T07:28:27.919Z | 0.3s | 1834 | false | false |
| Bash | orchestrator | 2026-11-23T07:25:28.792Z | 0.3s | 1001 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.99 |
| Cost — claude-opus-5-5 | $2.99 |
| Input tokens (uncached) | 68 |
| Total input tokens (incl. cache) | 3670242 |
| Output tokens | 49181 |
| Thinking tokens (main thread) | 24014 |
| Cache read tokens | 3506529 |
| Cache write tokens | 163645 |
| Cache write tokens, main thread (5m / 1h) | 0 / 163645 |
| Cache hit ratio | 0.9554 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 68 | 3670242 | 378 | 3506529 | 163645 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 48803 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 46 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.53 |

## Session 3 — 2026-11-23T07:32:47.464Z → 2026-11-23T07:34:53.856Z

Session id: `866195b0-a868-4e8d-a3d3-bfffa8675199`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 06s | 2m 07s | 2m 01s | 0.0s | 0.0s | 2m 06s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 20 | 2.3s | 14.0s | 23.9s | 23.9s | 0 |
| orchestrator | 20 | 2.3s | 14.0s | 23.9s | 23.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 16 | 5.8s | 1.0s |
| Read | orchestrator | 7 | 0.4s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:33:36.326Z | 1.0s | 1275 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:08.099Z | 0.5s | 14828 | false | false |
| Bash | orchestrator | 2026-11-23T07:32:47.692Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:43.718Z | 0.3s | 7846 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:02.298Z | 0.3s | 2247 | false | false |
| Bash | orchestrator | 2026-11-23T07:32:56.142Z | 0.3s | 586 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:04.696Z | 0.3s | 2132 | false | false |
| Bash | orchestrator | 2026-11-23T07:32:49.794Z | 0.3s | 19963 | false | false |
| Read | orchestrator | 2026-11-23T07:32:57.948Z | 0.2s | 64202 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:59.653Z | 0.2s | 3284 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.56 |
| Cost — claude-opus-5-5 | $1.56 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 1758463 |
| Output tokens | 13275 |
| Thinking tokens (main thread) | 6716 |
| Cache read tokens | 1637030 |
| Cache write tokens | 121393 |
| Cache write tokens, main thread (5m / 1h) | 0 / 121393 |
| Cache hit ratio | 0.9309 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 40 | 1758463 | 251 | 1637030 | 121393 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 13024 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 25 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.53 |

## Session 4 — 2026-11-23T07:32:47.337Z → 2026-11-23T07:36:55.835Z

Session id: `bf706cf3-6730-466b-9c87-775747cc37f8`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 08s | 4m 09s | 4m 00s | 0.0s | 0.0s | 4m 08s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 37 | 2.4s | 13.5s | 25.6s | 25.6s | 0 |
| orchestrator | 37 | 2.4s | 13.5s | 25.6s | 25.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 37 | 11.2s | 0.7s |
| Read | orchestrator | 20 | 1.2s | 0.4s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:33:29.420Z | 0.7s | 7488 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:19.599Z | 0.5s | 650 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:23.209Z | 0.4s | 12118 | false | false |
| Read | orchestrator | 2026-11-23T07:33:00.715Z | 0.4s | 30778 | false | false |
| Bash | orchestrator | 2026-11-23T07:32:47.834Z | 0.4s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:18.247Z | 0.4s | 107 | false | false |
| Bash | orchestrator | 2026-11-23T07:33:17.494Z | 0.4s | 502 | false | false |
| Bash | orchestrator | 2026-11-23T07:36:08.600Z | 0.3s | 5350 | false | false |
| Bash | orchestrator | 2026-11-23T07:34:53.593Z | 0.3s | 2998 | false | false |
| Bash | orchestrator | 2026-11-23T07:34:49.360Z | 0.3s | 1138 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.05 |
| Cost — claude-opus-5-5 | $3.05 |
| Input tokens (uncached) | 74 |
| Total input tokens (incl. cache) | 5131518 |
| Output tokens | 26250 |
| Thinking tokens (main thread) | 15000 |
| Cache read tokens | 4938762 |
| Cache write tokens | 192682 |
| Cache write tokens, main thread (5m / 1h) | 0 / 192682 |
| Cache hit ratio | 0.9624 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 74 | 5131518 | 1021 | 4938762 | 192682 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25229 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 59 |
| Time to first token | 0.8s |
| Rate-limit peak | seven_day 0.53 |

## Session 5 — 2026-11-23T07:37:05.525Z → 2026-11-23T07:39:42.636Z

Session id: `b4a0291a-e167-422d-a471-ebd4bb01e1fb`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 37s | 2m 38s | 2m 32s | 0.0s | 0.0s | 2m 37s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.5s | 10.9s | 23.6s | 23.6s | 0 |
| orchestrator | 17 | 1.5s | 10.9s | 23.6s | 23.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 4.9s | 1.8s |
| Edit | orchestrator | 11 | 0.4s | 0.0s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:38:17.629Z | 1.8s | 3597 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:05.525Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:51.738Z | 0.4s | 1695 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:30.896Z | 0.3s | 8935 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:13.388Z | 0.3s | 774 | false | false |
| Bash | orchestrator | 2026-11-23T07:39:24.107Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:48.278Z | 0.2s | 55 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:16.197Z | 0.2s | 15413 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:09.786Z | 0.2s | 2422 | false | false |
| Bash | orchestrator | 2026-11-23T07:37:45.486Z | 0.2s | 2058 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.03 |
| Cost — claude-opus-5-5 | $1.03 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 951760 |
| Output tokens | 17916 |
| Thinking tokens (main thread) | 6035 |
| Cache read tokens | 889551 |
| Cache write tokens | 62175 |
| Cache write tokens, main thread (5m / 1h) | 0 / 62175 |
| Cache hit ratio | 0.9346 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 951760 | 140 | 889551 | 62175 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 17776 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 32 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.53 |

## Session 6 — 2026-11-23T07:39:46.154Z → 2026-11-23T07:41:24.087Z

Session id: `49f3ac33-9de6-4aa4-ac36-f80f8fbc03fb`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 37s | 1m 38s | 1m 36s | 0.0s | 0.0s | 1m 37s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 1.4s | 19.3s | 28.5s | 28.5s | 0 |
| orchestrator | 14 | 1.4s | 19.3s | 28.5s | 28.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 2.3s | 0.6s |
| Read | orchestrator | 22 | 1.4s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:39:46.636Z | 0.6s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:41:06.417Z | 0.5s | 565 | false | false |
| Bash | orchestrator | 2026-11-23T07:39:47.633Z | 0.4s | 4567 | false | false |
| Read | orchestrator | 2026-11-23T07:40:00.236Z | 0.3s | 31957 | false | false |
| Read | orchestrator | 2026-11-23T07:39:51.706Z | 0.3s | 64202 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:14.402Z | 0.2s | 4151 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:01.395Z | 0.2s | 1221 | false | false |
| Read | orchestrator | 2026-11-23T07:40:04.783Z | 0.2s | 30196 | false | false |
| Read | orchestrator | 2026-11-23T07:40:02.933Z | 0.2s | 31668 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:11.815Z | 0.1s | 727 | true | true |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.62 |
| Cost — claude-opus-5-5 | $1.62 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 1480689 |
| Output tokens | 10891 |
| Thinking tokens (main thread) | 5936 |
| Cache read tokens | 1338959 |
| Cache write tokens | 141702 |
| Cache write tokens, main thread (5m / 1h) | 0 / 141702 |
| Cache hit ratio | 0.9043 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 1480689 | 869 | 1338959 | 141702 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 10022 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 30 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.54 |

## Session 7 — 2026-11-23T07:39:46.199Z → 2026-11-23T07:43:17.160Z

Session id: `aacb693d-b6c9-4e3f-a1f3-a34cb74576e0`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 30s | 3m 32s | 3m 26s | 0.0s | 0.0s | 3m 30s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 32 | 2.9s | 12.4s | 26.9s | 26.9s | 0 |
| orchestrator | 32 | 2.9s | 12.4s | 26.9s | 26.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 23 | 6.4s | 0.7s |
| Read | orchestrator | 30 | 0.8s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:39:46.462Z | 0.7s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:41.399Z | 0.4s | 107 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:40.645Z | 0.4s | 502 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:49.941Z | 0.4s | 1273 | false | false |
| Bash | orchestrator | 2026-11-23T07:39:48.998Z | 0.3s | 8581 | false | false |
| Bash | orchestrator | 2026-11-23T07:39:53.497Z | 0.3s | 3234 | false | false |
| Read | orchestrator | 2026-11-23T07:40:12.329Z | 0.3s | 64202 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:42.203Z | 0.2s | 5376 | false | false |
| Bash | orchestrator | 2026-11-23T07:41:16.136Z | 0.2s | 4911 | false | false |
| Bash | orchestrator | 2026-11-23T07:40:51.447Z | 0.2s | 11706 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.31 |
| Cost — claude-opus-5-5 | $2.31 |
| Input tokens (uncached) | 64 |
| Total input tokens (incl. cache) | 3602150 |
| Output tokens | 22543 |
| Thinking tokens (main thread) | 11546 |
| Cache read tokens | 3455562 |
| Cache write tokens | 146524 |
| Cache write tokens, main thread (5m / 1h) | 0 / 146524 |
| Cache hit ratio | 0.9593 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 64 | 3602150 | 304 | 3455562 | 146524 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 22239 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 55 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.54 |

## Session 8 — 2026-11-23T07:43:27.877Z → 2026-11-23T07:48:35.930Z

Session id: `65fabef0-5c5e-4ab6-ab2f-81031da8cce6`

Planning node: `7-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 08s | 5m 09s | 5m 03s | 0.0s | 0.0s | 5m 08s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 28 | 2.9s | 24.9s | 31.5s | 31.5s | 0 |
| orchestrator | 28 | 2.9s | 24.9s | 31.5s | 31.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 15 | 5.0s | 0.9s |
| Edit | orchestrator | 10 | 0.4s | 0.0s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 0.3s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:46:22.003Z | 0.9s | 3597 | false | false |
| Bash | orchestrator | 2026-11-23T07:43:49.974Z | 0.7s | 1765 | false | false |
| Bash | orchestrator | 2026-11-23T07:43:27.877Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:44:01.198Z | 0.3s | 12092 | false | false |
| Bash | orchestrator | 2026-11-23T07:44:25.350Z | 0.3s | 17578 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:11.286Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T07:47:19.359Z | 0.2s | 654 | false | false |
| Bash | orchestrator | 2026-11-23T07:43:33.894Z | 0.2s | 8256 | false | false |
| Bash | orchestrator | 2026-11-23T07:43:42.165Z | 0.2s | 6702 | false | false |
| Bash | orchestrator | 2026-11-23T07:45:39.046Z | 0.2s | 478 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.01 |
| Cost — claude-opus-5-5 | $2.01 |
| Input tokens (uncached) | 56 |
| Total input tokens (incl. cache) | 2336859 |
| Output tokens | 35318 |
| Thinking tokens (main thread) | 16371 |
| Cache read tokens | 2229248 |
| Cache write tokens | 107555 |
| Cache write tokens, main thread (5m / 1h) | 0 / 107555 |
| Cache hit ratio | 0.954 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 56 | 2336859 | 469 | 2229248 | 107555 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 34849 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 45 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.54 |

## Session 9 — 2026-11-23T07:48:38.522Z → 2026-11-23T07:49:20.908Z

Session id: `fa710f48-059c-4a68-ac40-56a94d2f8084`

Planning node: `8-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 42.3s | 43.2s | 41.1s | 0.0s | 0.0s | 42.3s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 10 | 1.9s | 10.3s | 10.3s | 10.3s | 0 |
| orchestrator | 10 | 1.9s | 10.3s | 10.3s | 10.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 2.2s | 0.5s |
| Read | orchestrator | 14 | 1.1s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:48:39.025Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:46.960Z | 0.5s | 1296 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:10.575Z | 0.3s | 1629 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:52.300Z | 0.3s | 1377 | false | false |
| Read | orchestrator | 2026-11-23T07:48:53.756Z | 0.2s | 64202 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:40.074Z | 0.2s | 4637 | false | false |
| Read | orchestrator | 2026-11-23T07:48:48.984Z | 0.2s | 44999 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:44.833Z | 0.2s | 40 | false | false |
| Read | orchestrator | 2026-11-23T07:48:55.953Z | 0.2s | 31957 | false | false |
| Read | orchestrator | 2026-11-23T07:48:55.354Z | 0.2s | 31668 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.18 |
| Cost — claude-opus-5-5 | $1.18 |
| Input tokens (uncached) | 20 |
| Total input tokens (incl. cache) | 671017 |
| Output tokens | 4579 |
| Thinking tokens (main thread) | 1270 |
| Cache read tokens | 548734 |
| Cache write tokens | 122263 |
| Cache write tokens, main thread (5m / 1h) | 0 / 122263 |
| Cache hit ratio | 0.8178 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 20 | 671017 | 779 | 548734 | 122263 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 3800 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 22 |
| Time to first token | 0.8s |
| Rate-limit peak | seven_day 0.54 |

## Session 10 — 2026-11-23T07:48:38.664Z → 2026-11-23T07:50:54.860Z

Session id: `9805bbbe-1c62-4fd3-af25-caac499050f6`

Planning node: `9-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 16s | 2m 17s | 2m 11s | 0.0s | 0.0s | 2m 16s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 26 | 1.6s | 10.9s | 12.2s | 12.2s | 0 |
| orchestrator | 26 | 1.6s | 10.9s | 12.2s | 12.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 18 | 6.0s | 1.1s |
| Read | orchestrator | 12 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T07:50:16.389Z | 1.1s | 3597 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:46.902Z | 0.5s | 891 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:38.901Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:33.976Z | 0.3s | 1736 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:54.514Z | 0.3s | 2421 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:02.008Z | 0.3s | 547 | false | false |
| Bash | orchestrator | 2026-11-23T07:48:49.446Z | 0.3s | 25373 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:21.055Z | 0.2s | 12428 | false | false |
| Bash | orchestrator | 2026-11-23T07:49:49.161Z | 0.2s | 2298 | false | false |
| Bash | orchestrator | 2026-11-23T07:50:25.519Z | 0.2s | 10700 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.34 |
| Cost — claude-opus-5-5 | $1.34 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 1738799 |
| Output tokens | 14622 |
| Thinking tokens (main thread) | 7289 |
| Cache read tokens | 1649198 |
| Cache write tokens | 89549 |
| Cache write tokens, main thread (5m / 1h) | 0 / 89549 |
| Cache hit ratio | 0.9485 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 52 | 1738799 | 990 | 1649198 | 89549 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 13632 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 32 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.54 |

## Session 11 — 2026-11-23T07:51:30.045Z → 2026-11-23T08:11:25.384Z

Session id: `cd673aaa-2460-40d4-85b9-8c263f49042a`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 19m 55s | 19m 56s | 17m 59s | 0.0s | 10m 47s | 9m 07s | 17m 23s | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-23T07:53:08.237Z | 10m 47s | devscene:layer-implementer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 108 | 1.8s | 5.2s | 26.8s | 10m 47s | 1 |
| devscene:layer-implementer | 69 | 2.2s | 6.2s | 10m 47s | 10m 47s | 1 |
| orchestrator | 39 | 1.4s | 3.1s | 7.7s | 7.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 5 | 17m 23s | 14m 08s |
| Bash | devscene:layer-implementer | 75 | 1m 52s | 23.5s |
| Bash | orchestrator | 36 | 34.8s | 7.2s |
| Edit | devscene:layer-implementer | 10 | 0.4s | 0.0s |
| Read | devscene:layer-implementer | 22 | 1.4s | 0.3s |
| Read | orchestrator | 10 | 1.0s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 8 | 0.3s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-23T08:07:03.346Z | 23.5s | 1399 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T08:05:27.991Z | 16.8s | 1399 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T08:07:02.694Z | 16.7s | 6379 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T08:07:46.762Z | 7.4s | 508 | false | false |
| Bash | orchestrator | 2026-11-23T08:08:02.660Z | 7.2s | 724 | false | false |
| Bash | orchestrator | 2026-11-23T08:06:32.166Z | 7.1s | 756 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T08:09:44.617Z | 6.6s | 1399 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T08:08:41.374Z | 6.4s | 1399 | false | false |
| Bash | orchestrator | 2026-11-23T08:09:03.326Z | 6.3s | 733 | false | false |
| Bash | orchestrator | 2026-11-23T08:10:16.409Z | 6.3s | 727 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 4 | 53.4s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 5 | 1.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 3 | 17.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/chore_rename_devscene_runtime_story_plan.md - | 4 | 27.0s |
| orchestrator | cat <repo_root>/harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 5 | 1.3s |
| orchestrator | ls <repo_root>/harness-runs/STOP <repo_root>/harness-runs/PAUSE 2>/dev/null | 5 | 0.9s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (general) | 14m 08s | 30 | 95710 | 62 | 5132313 | 4724514 | 407737 | 0.7097 |
| devscene:layer-implementer | Implement Task 2 (cli) | 1m 12s | 14 | 4153 | 30 | 544550 | 514807 | 29713 | 0.0602 |
| devscene:layer-implementer | Implement Task 3 (general) | 42.1s | 10 | 3514 | 22 | 518307 | 477954 | 40331 | 0.0353 |
| devscene:layer-implementer | Implement Task 4 (general) | 56.8s | 11 | 4907 | 24 | 682558 | 628876 | 53658 | 0.0475 |
| devscene:layer-implementer | Implement Task 5 (general) | 24.2s | 4 | 2832 | 10 | 207070 | 167860 | 39200 | 0.0203 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $8.98 |
| Cost — claude-opus-5-5 | $8.98 |
| Input tokens (uncached) | 228 |
| Total input tokens (incl. cache) | 12141235 |
| Output tokens | 124389 |
| Thinking tokens (main thread) | 1433 |
| Cache read tokens | 11400662 |
| Cache write tokens | 740345 |
| Cache write tokens, main thread (5m / 1h) | 0 / 169706 |
| Cache hit ratio | 0.939 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 80 | 5056437 | 779 | 4886651 | 169706 |
| sub-agents | 148 | 7084798 | 111116 | 6514011 | 570639 |
| remainder | 0 | 0 | 12494 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 6 |
| Sub-agents spawned / failed / killed | 5 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 55 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.54 |
