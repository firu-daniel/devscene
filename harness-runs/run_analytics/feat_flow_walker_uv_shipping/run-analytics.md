# Run analytics — feat_flow_walker_uv_shipping

## Whole run

| Measure | Value |
|---|---|
| Sessions | 11 (0 incomplete) |
| Engine / planning node sessions | 2 / 9 |
| Span | 1h23m |
| Wall | 1h22m |
| Session wall, summed over sessions | 1h30m |
| Active | 1h22m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $50.11 |
| Input tokens (uncached) | 1578 |
| Total input tokens (incl. cache) | 99501213 |
| Output tokens | 516966 |
| Thinking tokens (main thread) | 162162 |
| Cache read tokens | 96534506 |
| Cache write tokens | 2965129 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1876402 |
| Cache hit ratio | 0.9702 |
| Requests | 775 |
| Request latency p50 / p90 / p99 / max | 2.2s / 9.3s / 46.2s / 1m 30s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 30 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 3 (cli) — 6m 58s (session 11) |
| Rate-limit peak | seven_day 0.05 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 14m 48s | 14m 48s | 0.0s | 14m 49s | $7.06 |
| 3 | 2-architecture_review | 3m 15s | 3m 15s | 0.0s | 3m 16s | $2.29 |
| 4 | 3-plan_review | 9m 15s | 9m 15s | 0.0s | 9m 16s | $6.57 |
| 5 | 4-plan_writer | 2m 48s | 2m 48s | 0.0s | 2m 49s | $1.43 |
| 6 | 5-architecture_review | 3m 04s | 3m 04s | 0.0s | 3m 05s | $2.26 |
| 7 | 6-plan_review | 9m 18s | 9m 18s | 0.0s | 9m 19s | $7.34 |
| 8 | 7-plan_writer | 2m 35s | 2m 35s | 0.0s | 2m 37s | $1.28 |
| 9 | 8-architecture_review | 1m 04s | 1m 04s | 0.0s | 1m 05s | $0.92 |
| 10 | 9-plan_review | 2m 04s | 2m 04s | 0.0s | 2m 05s | $1.21 |

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

## Session 1 — 2026-11-24T15:22:40.768Z → 2026-11-24T15:23:55.744Z

Session id: `6bae8bae-10ce-4757-a9a5-d0d83cf2c224`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 14s | 1m 16s | 1m 05s | 0.0s | 0.0s | 1m 14s | 11.8s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 23 | 1.4s | 5.2s | 8.3s | 8.3s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.3s | 8.3s | 8.3s | 8.3s | 0 |
| orchestrator | 21 | 1.4s | 2.2s | 7.0s | 7.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 11.8s | 11.8s |
| Bash | orchestrator | 17 | 11.4s | 7.1s |
| Grep | devscene:prompt-injection-reviewer | 1 | 0.1s | 0.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:23:43.291Z | 7.1s | 595 | false | false |
| Bash | orchestrator | 2026-11-24T15:22:42.241Z | 0.4s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:22:51.477Z | 0.3s | 156 | false | false |
| Bash | orchestrator | 2026-11-24T15:23:23.166Z | 0.3s | 1267 | false | false |
| Bash | orchestrator | 2026-11-24T15:23:13.195Z | 0.3s | 155 | false | false |
| Bash | orchestrator | 2026-11-24T15:22:49.233Z | 0.3s | 331 | true | false |
| Read | orchestrator | 2026-11-24T15:23:24.884Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-24T15:23:15.519Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-24T15:23:27.114Z | 0.2s | 119 | false | false |
| Bash | orchestrator | 2026-11-24T15:22:46.543Z | 0.2s | 210 | true | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 11.8s | 2 | 1112 | 6 | 48371 | 29190 | 19175 | 0.1579 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.99 |
| Cost — claude-opus-5-5 | $0.99 |
| Input tokens (uncached) | 48 |
| Total input tokens (incl. cache) | 1312609 |
| Output tokens | 6893 |
| Thinking tokens (main thread) | 437 |
| Cache read tokens | 1229802 |
| Cache write tokens | 82759 |
| Cache write tokens, main thread (5m / 1h) | 0 / 63584 |
| Cache hit ratio | 0.9369 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 42 | 1264238 | 374 | 1200612 | 63584 |
| sub-agents | 6 | 48371 | 1112 | 29190 | 19175 |
| remainder | 0 | 0 | 5407 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 27 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.03 |

## Session 2 — 2026-11-24T15:23:59.071Z → 2026-11-24T15:38:47.092Z

Session id: `ebd007e7-1042-4e18-8ee6-6eca4d8ebe6c`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 14m 48s | 14m 49s | 14m 31s | 0.0s | 0.0s | 14m 48s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 63 | 2.6s | 18.5s | 1m 30s | 1m 30s | 0 |
| orchestrator | 63 | 2.6s | 18.5s | 1m 30s | 1m 30s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 53 | 17.9s | 0.8s |
| Edit | orchestrator | 4 | 0.1s | 0.0s |
| Read | orchestrator | 16 | 1.2s | 0.3s |
| Write | orchestrator | 14 | 0.5s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:31:09.066Z | 0.8s | 874 | false | false |
| Bash | orchestrator | 2026-11-24T15:23:59.563Z | 0.7s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:24:15.743Z | 0.6s | 3558 | false | false |
| Bash | orchestrator | 2026-11-24T15:25:21.552Z | 0.4s | 2872 | false | false |
| Bash | orchestrator | 2026-11-24T15:31:12.531Z | 0.4s | 655 | false | false |
| Bash | orchestrator | 2026-11-24T15:30:10.243Z | 0.4s | 3547 | false | false |
| Bash | orchestrator | 2026-11-24T15:38:06.118Z | 0.4s | 82 | false | false |
| Bash | orchestrator | 2026-11-24T15:32:40.658Z | 0.4s | 704 | false | false |
| Bash | orchestrator | 2026-11-24T15:25:09.158Z | 0.4s | 9558 | false | false |
| Bash | orchestrator | 2026-11-24T15:24:17.899Z | 0.4s | 11997 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $7.06 |
| Cost — claude-opus-5-5 | $7.06 |
| Input tokens (uncached) | 126 |
| Total input tokens (incl. cache) | 13139242 |
| Output tokens | 95690 |
| Thinking tokens (main thread) | 52108 |
| Cache read tokens | 12816692 |
| Cache write tokens | 322424 |
| Cache write tokens, main thread (5m / 1h) | 0 / 322424 |
| Cache hit ratio | 0.9755 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 126 | 13139242 | 610 | 12816692 | 322424 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 95080 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 88 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.03 |

## Session 3 — 2026-11-24T15:38:50.874Z → 2026-11-24T15:42:06.308Z

Session id: `f7b96438-4551-456e-8d04-390c51bb4c7a`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 15s | 3m 16s | 3m 12s | 0.0s | 0.0s | 3m 15s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 21 | 1.5s | 30.3s | 48.4s | 48.4s | 0 |
| orchestrator | 21 | 1.5s | 30.3s | 48.4s | 48.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 3.4s | 0.4s |
| Read | orchestrator | 28 | 1.1s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:38:51.182Z | 0.4s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:40:14.651Z | 0.3s | 4700 | false | false |
| Bash | orchestrator | 2026-11-24T15:38:57.659Z | 0.3s | 1656 | false | false |
| Bash | orchestrator | 2026-11-24T15:40:18.390Z | 0.3s | 1474 | false | false |
| Bash | orchestrator | 2026-11-24T15:40:33.197Z | 0.3s | 302 | false | false |
| Bash | orchestrator | 2026-11-24T15:40:40.114Z | 0.3s | 197 | false | false |
| Bash | orchestrator | 2026-11-24T15:38:53.311Z | 0.3s | 6982 | false | false |
| Bash | orchestrator | 2026-11-24T15:40:21.309Z | 0.2s | 4024 | false | false |
| Read | orchestrator | 2026-11-24T15:39:17.498Z | 0.2s | 37125 | false | false |
| Bash | orchestrator | 2026-11-24T15:41:27.424Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.29 |
| Cost — claude-opus-5-5 | $2.29 |
| Input tokens (uncached) | 42 |
| Total input tokens (incl. cache) | 2327208 |
| Output tokens | 21015 |
| Thinking tokens (main thread) | 11617 |
| Cache read tokens | 2147365 |
| Cache write tokens | 179801 |
| Cache write tokens, main thread (5m / 1h) | 0 / 179801 |
| Cache hit ratio | 0.9227 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 42 | 2327208 | 976 | 2147365 | 179801 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 20039 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 41 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.03 |

## Session 4 — 2026-11-24T15:38:50.722Z → 2026-11-24T15:48:05.748Z

Session id: `43d28685-9125-4558-93eb-bf25065a5a1b`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 9m 15s | 9m 16s | 9m 01s | 0.0s | 0.0s | 9m 15s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 63 | 2.4s | 12.8s | 1m 08s | 1m 08s | 0 |
| orchestrator | 63 | 2.4s | 12.8s | 1m 08s | 1m 08s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 48 | 15.5s | 0.6s |
| Read | orchestrator | 47 | 2.0s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:44:37.479Z | 0.6s | 832 | false | false |
| Bash | orchestrator | 2026-11-24T15:44:26.128Z | 0.6s | 20568 | false | false |
| Bash | orchestrator | 2026-11-24T15:38:51.088Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:42:10.650Z | 0.4s | 9205 | false | false |
| Bash | orchestrator | 2026-11-24T15:44:06.346Z | 0.3s | 3547 | false | false |
| Bash | orchestrator | 2026-11-24T15:43:59.282Z | 0.3s | 2176 | false | false |
| Bash | orchestrator | 2026-11-24T15:42:00.965Z | 0.3s | 5932 | false | false |
| Bash | orchestrator | 2026-11-24T15:43:08.058Z | 0.3s | 2772 | false | false |
| Bash | orchestrator | 2026-11-24T15:43:18.417Z | 0.3s | 386 | false | false |
| Bash | orchestrator | 2026-11-24T15:42:04.463Z | 0.3s | 634 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $6.57 |
| Cost — claude-opus-5-5 | $6.57 |
| Input tokens (uncached) | 126 |
| Total input tokens (incl. cache) | 13948762 |
| Output tokens | 58619 |
| Thinking tokens (main thread) | 35615 |
| Cache read tokens | 13613972 |
| Cache write tokens | 334664 |
| Cache write tokens, main thread (5m / 1h) | 0 / 334664 |
| Cache hit ratio | 0.976 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 126 | 13948762 | 1291 | 13613972 | 334664 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 57328 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 97 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.03 |

## Session 5 — 2026-11-24T15:48:16.899Z → 2026-11-24T15:51:05.503Z

Session id: `18a8ab1e-bcd0-45dd-a561-f6842a369405`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 48s | 2m 49s | 2m 45s | 0.0s | 0.0s | 2m 48s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 28 | 1.8s | 4.6s | 17.3s | 17.3s | 0 |
| orchestrator | 28 | 1.8s | 4.6s | 17.3s | 17.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 16 | 5.0s | 0.6s |
| Edit | orchestrator | 19 | 0.7s | 0.0s |
| Read | orchestrator | 11 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:48:17.267Z | 0.6s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:50:33.056Z | 0.5s | 5887 | false | false |
| Bash | orchestrator | 2026-11-24T15:48:39.662Z | 0.3s | 2963 | false | false |
| Bash | orchestrator | 2026-11-24T15:48:29.610Z | 0.3s | 14887 | false | false |
| Bash | orchestrator | 2026-11-24T15:49:57.306Z | 0.3s | 124 | false | false |
| Bash | orchestrator | 2026-11-24T15:48:37.711Z | 0.3s | 3974 | false | false |
| Bash | orchestrator | 2026-11-24T15:49:02.344Z | 0.2s | 1720 | false | false |
| Bash | orchestrator | 2026-11-24T15:48:53.148Z | 0.2s | 4883 | false | false |
| Bash | orchestrator | 2026-11-24T15:48:56.514Z | 0.2s | 43 | false | false |
| Bash | orchestrator | 2026-11-24T15:49:16.627Z | 0.2s | 3425 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.43 |
| Cost — claude-opus-5-5 | $1.43 |
| Input tokens (uncached) | 56 |
| Total input tokens (incl. cache) | 2009228 |
| Output tokens | 20130 |
| Thinking tokens (main thread) | 3764 |
| Cache read tokens | 1928524 |
| Cache write tokens | 80648 |
| Cache write tokens, main thread (5m / 1h) | 0 / 80648 |
| Cache hit ratio | 0.9598 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 56 | 2009228 | 1017 | 1928524 | 80648 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 19113 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 48 |
| Time to first token | 0.8s |
| Rate-limit peak | seven_day 0.04 |

## Session 6 — 2026-11-24T15:51:09.205Z → 2026-11-24T15:54:14.066Z

Session id: `d54a14b5-9a67-46d2-8fea-c50c9b83c7db`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 04s | 3m 05s | 3m 01s | 0.0s | 0.0s | 3m 04s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 21 | 1.7s | 11.8s | 1m 17s | 1m 17s | 0 |
| orchestrator | 21 | 1.7s | 11.8s | 1m 17s | 1m 17s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 12 | 3.8s | 0.5s |
| Read | orchestrator | 27 | 1.2s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:51:09.530Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:03.399Z | 0.4s | 3094 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:06.300Z | 0.3s | 4917 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:38.586Z | 0.3s | 2060 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:27.538Z | 0.3s | 2281 | false | false |
| Read | orchestrator | 2026-11-24T15:51:22.388Z | 0.3s | 63315 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:09.422Z | 0.3s | 5590 | false | false |
| Read | orchestrator | 2026-11-24T15:51:24.921Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:53.848Z | 0.2s | 283 | false | false |
| Bash | orchestrator | 2026-11-24T15:51:20.110Z | 0.2s | 7678 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.26 |
| Cost — claude-opus-5-5 | $2.26 |
| Input tokens (uncached) | 42 |
| Total input tokens (incl. cache) | 2554181 |
| Output tokens | 20175 |
| Thinking tokens (main thread) | 12756 |
| Cache read tokens | 2381188 |
| Cache write tokens | 172951 |
| Cache write tokens, main thread (5m / 1h) | 0 / 172951 |
| Cache hit ratio | 0.9323 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 42 | 2554181 | 944 | 2381188 | 172951 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 19231 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 41 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.04 |

## Session 7 — 2026-11-24T15:51:09.208Z → 2026-11-24T16:00:27.901Z

Session id: `1b807123-d70e-408a-a988-fcef046dd04f`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 9m 18s | 9m 19s | 8m 58s | 0.0s | 0.0s | 9m 18s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 91 | 2.2s | 14.5s | 28.8s | 28.8s | 0 |
| orchestrator | 91 | 2.2s | 14.5s | 28.8s | 28.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 69 | 21.3s | 0.5s |
| Read | orchestrator | 54 | 1.6s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T15:51:09.537Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T15:52:27.565Z | 0.5s | 2467 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:58.045Z | 0.4s | 963 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:32.109Z | 0.4s | 14657 | false | false |
| Bash | orchestrator | 2026-11-24T15:52:30.567Z | 0.4s | 1246 | false | false |
| Bash | orchestrator | 2026-11-24T15:57:07.874Z | 0.4s | 160 | false | false |
| Bash | orchestrator | 2026-11-24T15:59:31.066Z | 0.4s | 999 | false | false |
| Bash | orchestrator | 2026-11-24T15:53:07.211Z | 0.4s | 1359 | false | false |
| Bash | orchestrator | 2026-11-24T15:57:47.220Z | 0.3s | 1551 | false | false |
| Bash | orchestrator | 2026-11-24T15:57:43.432Z | 0.3s | 127 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $7.34 |
| Cost — claude-opus-5-5 | $7.34 |
| Input tokens (uncached) | 182 |
| Total input tokens (incl. cache) | 19759996 |
| Output tokens | 57266 |
| Thinking tokens (main thread) | 31634 |
| Cache read tokens | 19472012 |
| Cache write tokens | 287802 |
| Cache write tokens, main thread (5m / 1h) | 0 / 287802 |
| Cache hit ratio | 0.9854 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 182 | 19759996 | 1718 | 19472012 | 287802 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 55548 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 3 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 125 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.04 |

## Session 8 — 2026-11-24T16:00:39.924Z → 2026-11-24T16:03:15.738Z

Session id: `500209f1-65f8-45e1-a4c7-8270474b26c9`

Planning node: `7-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 35s | 2m 37s | 2m 31s | 0.0s | 0.0s | 2m 35s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 26 | 2.7s | 8.4s | 9.5s | 9.5s | 0 |
| orchestrator | 26 | 2.7s | 8.4s | 9.5s | 9.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 20 | 6.0s | 0.5s |
| Edit | orchestrator | 5 | 0.2s | 0.0s |
| Read | orchestrator | 6 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T16:00:40.412Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T16:02:51.157Z | 0.4s | 5728 | false | false |
| Bash | orchestrator | 2026-11-24T16:01:09.149Z | 0.4s | 2948 | false | false |
| Bash | orchestrator | 2026-11-24T16:01:05.529Z | 0.4s | 4324 | false | false |
| Bash | orchestrator | 2026-11-24T16:01:56.856Z | 0.3s | 461 | false | false |
| Bash | orchestrator | 2026-11-24T16:00:52.307Z | 0.3s | 2653 | false | false |
| Bash | orchestrator | 2026-11-24T16:01:31.844Z | 0.3s | 45 | false | false |
| Bash | orchestrator | 2026-11-24T16:02:27.897Z | 0.3s | 2977 | false | false |
| Bash | orchestrator | 2026-11-24T16:01:23.122Z | 0.3s | 937 | false | false |
| Bash | orchestrator | 2026-11-24T16:00:48.357Z | 0.2s | 2054 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.28 |
| Cost — claude-opus-5-5 | $1.28 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 1724002 |
| Output tokens | 16828 |
| Thinking tokens (main thread) | 5879 |
| Cache read tokens | 1647068 |
| Cache write tokens | 76882 |
| Cache write tokens, main thread (5m / 1h) | 0 / 76882 |
| Cache hit ratio | 0.9554 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 52 | 1724002 | 259 | 1647068 | 76882 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 16569 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 33 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.04 |

## Session 9 — 2026-11-24T16:03:19.302Z → 2026-11-24T16:04:23.891Z

Session id: `18bd4524-4438-4c2c-8cd4-198967acc7b8`

Planning node: `8-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 04s | 1m 05s | 1m 02s | 0.0s | 0.0s | 1m 04s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 1.9s | 5.9s | 6.9s | 6.9s | 0 |
| orchestrator | 14 | 1.9s | 5.9s | 6.9s | 6.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.7s | 0.5s |
| Read | orchestrator | 12 | 0.4s | 0.2s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T16:03:19.681Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:29.667Z | 0.4s | 5335 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:33.819Z | 0.3s | 6435 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:27.333Z | 0.3s | 40 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:49.100Z | 0.3s | 8279 | false | false |
| Read | orchestrator | 2026-11-24T16:03:38.927Z | 0.2s | 63315 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:22.167Z | 0.2s | 5066 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:35.839Z | 0.2s | 7701 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:56.313Z | 0.1s | 727 | true | true |
| Write | orchestrator | 2026-11-24T16:04:12.084Z | 0.0s | 229 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.92 |
| Cost — claude-opus-5-5 | $0.92 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 798298 |
| Output tokens | 6906 |
| Thinking tokens (main thread) | 1772 |
| Cache read tokens | 718673 |
| Cache write tokens | 79597 |
| Cache write tokens, main thread (5m / 1h) | 0 / 79597 |
| Cache hit ratio | 0.9003 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 798298 | 884 | 718673 | 79597 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 6022 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.04 |

## Session 10 — 2026-11-24T16:03:19.304Z → 2026-11-24T16:05:24.070Z

Session id: `e56c287b-51fe-474d-a4fd-de300c659d21`

Planning node: `9-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 04s | 2m 05s | 1m 58s | 0.0s | 0.0s | 2m 04s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 29 | 2.2s | 5.1s | 8.9s | 8.9s | 0 |
| orchestrator | 29 | 2.2s | 5.1s | 8.9s | 8.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 25 | 8.4s | 0.6s |
| Read | orchestrator | 9 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T16:04:54.159Z | 0.6s | 6527 | false | false |
| Bash | orchestrator | 2026-11-24T16:04:03.794Z | 0.5s | 2102 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:19.730Z | 0.5s | 56 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:53.294Z | 0.4s | 4177 | false | false |
| Bash | orchestrator | 2026-11-24T16:04:19.215Z | 0.4s | 991 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:29.201Z | 0.4s | 5335 | false | false |
| Bash | orchestrator | 2026-11-24T16:04:38.380Z | 0.3s | 5306 | false | false |
| Bash | orchestrator | 2026-11-24T16:04:09.406Z | 0.3s | 2480 | false | false |
| Bash | orchestrator | 2026-11-24T16:04:20.018Z | 0.3s | 1421 | false | false |
| Bash | orchestrator | 2026-11-24T16:03:56.623Z | 0.3s | 4825 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.21 |
| Cost — claude-opus-5-5 | $1.21 |
| Input tokens (uncached) | 58 |
| Total input tokens (incl. cache) | 1812864 |
| Output tokens | 12989 |
| Thinking tokens (main thread) | 4142 |
| Cache read tokens | 1737932 |
| Cache write tokens | 74874 |
| Cache write tokens, main thread (5m / 1h) | 0 / 74874 |
| Cache hit ratio | 0.9587 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 58 | 1812864 | 1044 | 1737932 | 74874 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 11945 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 36 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.04 |

## Session 11 — 2026-11-24T16:06:00.491Z → 2026-11-24T16:46:32.859Z

Session id: `117a404b-4865-4a63-9d08-1ccfc3609b38`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 40m 32s | 40m 34s | 28m 59s | 0.0s | 0.0s | 40m 32s | 36m 10s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 396 | 2.2s | 6.2s | 25.7s | 30.1s | 0 |
| devscene:layer-implementer | 330 | 2.4s | 7.0s | 25.7s | 30.1s | 0 |
| orchestrator | 66 | 1.2s | 3.5s | 9.3s | 9.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 12 | 36m 10s | 6m 58s |
| Bash | devscene:layer-implementer | 279 | 12m 54s | 1m 44s |
| Bash | orchestrator | 50 | 1m 28s | 8.6s |
| Edit | devscene:layer-implementer | 78 | 3.5s | 0.3s |
| Read | devscene:layer-implementer | 70 | 10.2s | 7.1s |
| Read | orchestrator | 11 | 1.6s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 15 | 0.7s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-24T16:17:37.076Z | 1m 44s | 2264 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:08:38.739Z | 24.6s | 837 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:29:35.195Z | 23.3s | 1739 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:20:13.586Z | 21.1s | 1739 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:24:33.438Z | 20.6s | 14428 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:20:38.232Z | 19.7s | 540 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:34:20.203Z | 19.7s | 70 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:42:53.783Z | 17.8s | 14422 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:24:32.682Z | 17.7s | 945 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T16:35:28.226Z | 17.4s | 43 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 8 | 1m 24s |
| devscene:layer-implementer | git diff --name-only HEAD | 4 | 1.6s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 4 | 1.0s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 12 | 2.8s |
| devscene:layer-implementer | npm test --workspace cli -- test/agent-return-schemas.test.mjs | 3 | 53.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 6 | 48.5s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 3 | 28.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/retrieval-loading.test.mjs | 5 | 1m 25s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 3 | 43.7s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_flow_walker_uv_shipping_story_plan.md -- | 11 | 1m 18s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 11 | 3.2s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (cli) | 3m 20s | 25 | 15790 | 52 | 1704914 | 1625200 | 79662 | 0.0824 |
| devscene:layer-implementer | Implement Task 2 (cli) | 3m 36s | 32 | 20782 | 66 | 3070708 | 2956794 | 113848 | 0.0891 |
| devscene:layer-implementer | Implement Task 3 (cli) | 6m 58s | 42 | 29372 | 86 | 5658007 | 5493589 | 164332 | 0.172 |
| devscene:layer-implementer | Implement Task 4 (cli) | 3m 34s | 34 | 19585 | 70 | 2816769 | 2708888 | 107811 | 0.0881 |
| devscene:layer-implementer | Implement Task 5 (cli) | 2m 05s | 21 | 10988 | 44 | 1409942 | 1340433 | 69465 | 0.0517 |
| devscene:layer-implementer | Implement Task 6 (cli) | 2m 24s | 23 | 11790 | 48 | 1622729 | 1546779 | 75902 | 0.0596 |
| devscene:layer-implementer | Implement Task 7 (cli) | 5m 28s | 51 | 27045 | 104 | 5729376 | 5588338 | 140934 | 0.135 |
| devscene:layer-implementer | Implement Task 8 (cli) | 3m 27s | 41 | 19318 | 84 | 3344097 | 3251790 | 92223 | 0.0855 |
| devscene:layer-implementer | Implement Task 9 (cli) | 1m 32s | 15 | 7899 | 32 | 1010519 | 945444 | 65043 | 0.0379 |
| devscene:layer-implementer | Implement Task 10 (cli) | 1m 33s | 13 | 7550 | 28 | 721341 | 662721 | 58592 | 0.0385 |
| devscene:layer-implementer | Implement Task 11 (flow-host) | 35.0s | 8 | 2850 | 18 | 402460 | 363075 | 39367 | 0.0144 |
| devscene:layer-implementer | Implement Task 12 (general) | 1m 32s | 25 | 8599 | 54 | 1697745 | 1635318 | 62373 | 0.0379 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $18.75 |
| Cost — claude-opus-5-5 | $18.75 |
| Input tokens (uncached) | 818 |
| Total input tokens (incl. cache) | 40114823 |
| Output tokens | 200455 |
| Thinking tokens (main thread) | 2438 |
| Cache read tokens | 38841278 |
| Cache write tokens | 1272727 |
| Cache write tokens, main thread (5m / 1h) | 0 / 203175 |
| Cache hit ratio | 0.9683 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 132 | 10926216 | 2325 | 10722909 | 203175 |
| sub-agents | 686 | 29188607 | 181568 | 28118369 | 1069552 |
| remainder | 0 | 0 | 16562 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 15 |
| Sub-agents spawned / failed / killed | 12 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 77 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.05 |
