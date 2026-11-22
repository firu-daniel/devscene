# Run analytics — feat_devscene_runtime_skeleton

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 22m 55s |
| Wall | 22m 09s |
| Session wall, summed over sessions | 24m 16s |
| Active | 22m 09s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $12.92 |
| Input tokens (uncached) | 350 |
| Total input tokens (incl. cache) | 19196819 |
| Output tokens | 115444 |
| Thinking tokens (main thread) | 39924 |
| Cache read tokens | 18268995 |
| Cache write tokens | 927474 |
| Cache write tokens, main thread (5m / 1h) | 0 / 773343 |
| Cache hit ratio | 0.9517 |
| Requests | 170 |
| Request latency p50 / p90 / p99 / max | 4.4s / 10.6s / 54.4s / 1m 00s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 7 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 1 general layer — 3m 11s (session 5) |
| Rate-limit peak | seven_day 0.51 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 7m 36s | 7m 36s | 0.0s | 7m 39s | $3.32 |
| 3 | 2-architecture_review | 2m 08s | 2m 08s | 0.0s | 2m 10s | $1.70 |
| 4 | 3-plan_review | 6m 13s | 6m 13s | 0.0s | 6m 17s | $3.24 |

## Network refusals

5 of 5 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No Run gates round log was scanned.

## Session 1 — 2026-11-22T18:02:26.689Z → 2026-11-22T18:03:58.940Z

Session id: `26c6fb1e-f180-4beb-8a3c-970b97a65fb7`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 32s | 1m 38s | 1m 28s | 0.0s | 0.0s | 1m 32s | 8.6s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 3.4s | 5.3s | 5.6s | 5.6s | 0 |
| devscene:prompt-injection-reviewer | 1 | 4.5s | 4.5s | 4.5s | 4.5s | 0 |
| orchestrator | 17 | 3.1s | 5.3s | 5.6s | 5.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 8.6s | 8.6s |
| Bash | orchestrator | 17 | 11.6s | 6.5s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 3 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T18:03:43.696Z | 6.5s | 603 | false | false |
| Bash | orchestrator | 2026-11-22T18:02:37.540Z | 0.6s | 675 | false | false |
| Bash | orchestrator | 2026-11-22T18:02:30.866Z | 0.4s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T18:02:45.880Z | 0.4s | 158 | false | false |
| Bash | orchestrator | 2026-11-22T18:02:35.578Z | 0.3s | 99 | true | false |
| Bash | orchestrator | 2026-11-22T18:02:36.723Z | 0.3s | 7397 | true | false |
| Bash | orchestrator | 2026-11-22T18:02:31.155Z | 0.3s | 27 | false | false |
| Bash | orchestrator | 2026-11-22T18:03:53.006Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T18:03:16.189Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T18:02:31.643Z | 0.2s | 30 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 8.6s | 1 | 274 | 4 | 29382 | 11222 | 18156 | 0.0942 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.96 |
| Cost — claude-opus-5-5 | $0.96 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 1103301 |
| Output tokens | 5415 |
| Thinking tokens (main thread) | 320 |
| Cache read tokens | 1015559 |
| Cache write tokens | 87702 |
| Cache write tokens, main thread (5m / 1h) | 0 / 69546 |
| Cache hit ratio | 0.9205 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 36 | 1073919 | 682 | 1004337 | 69546 |
| sub-agents | 4 | 29382 | 274 | 11222 | 18156 |
| remainder | 0 | 0 | 4459 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 26 |
| Time to first token | 5.9s |
| Rate-limit peak | seven_day 0.51 |

## Session 2 — 2026-11-22T18:04:03.538Z → 2026-11-22T18:11:40.416Z

Session id: `5bfbbe54-e34b-4172-9f7c-ef655109cbab`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 7m 36s | 7m 39s | 7m 31s | 0.0s | 0.0s | 7m 36s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 31 | 4.6s | 13.7s | 1m 00s | 1m 00s | 0 |
| orchestrator | 31 | 4.6s | 13.7s | 1m 00s | 1m 00s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 18 | 7.4s | 0.7s |
| Edit | orchestrator | 2 | 0.0s | 0.0s |
| Read | orchestrator | 18 | 1.0s | 0.3s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T18:05:30.144Z | 0.7s | 6670 | false | false |
| Bash | orchestrator | 2026-11-22T18:06:44.114Z | 0.6s | 9914 | false | false |
| Bash | orchestrator | 2026-11-22T18:05:14.160Z | 0.6s | 7699 | false | false |
| Bash | orchestrator | 2026-11-22T18:04:44.084Z | 0.5s | 11039 | false | false |
| Bash | orchestrator | 2026-11-22T18:06:56.060Z | 0.4s | 772 | false | false |
| Bash | orchestrator | 2026-11-22T18:07:02.654Z | 0.4s | 2462 | false | false |
| Bash | orchestrator | 2026-11-22T18:08:15.013Z | 0.4s | 185 | false | false |
| Bash | orchestrator | 2026-11-22T18:04:40.518Z | 0.4s | 23003 | false | false |
| Read | orchestrator | 2026-11-22T18:04:11.734Z | 0.3s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T18:04:03.543Z | 0.3s | 58 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.32 |
| Cost — claude-opus-5-5 | $3.32 |
| Input tokens (uncached) | 62 |
| Total input tokens (incl. cache) | 4246157 |
| Output tokens | 44144 |
| Thinking tokens (main thread) | 16036 |
| Cache read tokens | 4043164 |
| Cache write tokens | 202931 |
| Cache write tokens, main thread (5m / 1h) | 0 / 202931 |
| Cache hit ratio | 0.9522 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 62 | 4246157 | 331 | 4043164 | 202931 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 43813 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 45 |
| Time to first token | 3.0s |
| Rate-limit peak | seven_day 0.51 |

## Session 3 — 2026-11-22T18:11:45.572Z → 2026-11-22T18:13:54.422Z

Session id: `4e08efa6-fe28-473d-8237-9118bc2cc831`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 08s | 2m 10s | 2m 08s | 0.0s | 0.0s | 2m 08s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 4.3s | 19.7s | 22.5s | 22.5s | 0 |
| orchestrator | 17 | 4.3s | 19.7s | 22.5s | 22.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 10 | 2.8s | 0.5s |
| Read | orchestrator | 18 | 1.0s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T18:11:45.694Z | 0.5s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T18:11:46.698Z | 0.3s | 4202 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:08.209Z | 0.3s | 427 | false | false |
| Read | orchestrator | 2026-11-22T18:11:53.827Z | 0.2s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:24.413Z | 0.2s | 352 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:14.362Z | 0.2s | 8005 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:36.794Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T18:12:44.485Z | 0.2s | 1850 | false | false |
| Bash | orchestrator | 2026-11-22T18:12:08.276Z | 0.2s | 1095 | false | false |
| Read | orchestrator | 2026-11-22T18:11:58.207Z | 0.2s | 31668 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.70 |
| Cost — claude-opus-5-5 | $1.70 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 1829164 |
| Output tokens | 10521 |
| Thinking tokens (main thread) | 5563 |
| Cache read tokens | 1685597 |
| Cache write tokens | 143533 |
| Cache write tokens, main thread (5m / 1h) | 0 / 143533 |
| Cache hit ratio | 0.9215 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 1829164 | 932 | 1685597 | 143533 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 9589 | 0 | 0 |

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
| Time to first token | 2.1s |
| Rate-limit peak | seven_day 0.51 |

## Session 4 — 2026-11-22T18:11:47.006Z → 2026-11-22T18:18:01.003Z

Session id: `f0956e06-1c7a-4768-8a9b-8a0cb3b5b87b`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 6m 13s | 6m 17s | 6m 07s | 0.0s | 0.0s | 6m 13s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 45 | 5.0s | 11.3s | 46.1s | 46.1s | 0 |
| orchestrator | 45 | 5.0s | 11.3s | 46.1s | 46.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 35 | 11.1s | 0.8s |
| Read | orchestrator | 24 | 1.0s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T18:15:15.258Z | 0.8s | 1233 | false | false |
| Bash | orchestrator | 2026-11-22T18:11:47.565Z | 0.5s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T18:14:34.654Z | 0.5s | 3904 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:47.251Z | 0.5s | 690 | false | false |
| Bash | orchestrator | 2026-11-22T18:14:19.791Z | 0.4s | 1188 | false | false |
| Read | orchestrator | 2026-11-22T18:12:10.330Z | 0.3s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T18:17:07.961Z | 0.3s | 707 | false | false |
| Bash | orchestrator | 2026-11-22T18:16:03.652Z | 0.3s | 538 | false | false |
| Bash | orchestrator | 2026-11-22T18:13:39.024Z | 0.3s | 1941 | false | false |
| Bash | orchestrator | 2026-11-22T18:11:51.407Z | 0.3s | 10040 | true | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.24 |
| Cost — claude-opus-5-5 | $3.24 |
| Input tokens (uncached) | 90 |
| Total input tokens (incl. cache) | 6348236 |
| Output tokens | 26543 |
| Thinking tokens (main thread) | 16100 |
| Cache read tokens | 6163916 |
| Cache write tokens | 184230 |
| Cache write tokens, main thread (5m / 1h) | 0 / 184230 |
| Cache hit ratio | 0.971 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 90 | 6348236 | 1279 | 6163916 | 184230 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25264 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 61 |
| Time to first token | 3.5s |
| Rate-limit peak | seven_day 0.51 |

## Session 5 — 2026-11-22T18:18:37.429Z → 2026-11-22T18:25:22.086Z

Session id: `0c74a403-6863-47f1-a8f4-07087e07b891`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 6m 44s | 6m 47s | 6m 01s | 0.0s | 0.0s | 6m 44s | 3m 59s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 59 | 4.2s | 7.9s | 26.8s | 26.8s | 0 |
| devscene:layer-implementer | 29 | 4.8s | 10.8s | 26.8s | 26.8s | 0 |
| orchestrator | 30 | 4.2s | 6.2s | 10.7s | 10.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 2 | 3m 59s | 3m 11s |
| Bash | devscene:layer-implementer | 23 | 33.4s | 17.9s |
| Bash | orchestrator | 21 | 12.3s | 6.8s |
| Edit | devscene:layer-implementer | 6 | 0.2s | 0.0s |
| Read | devscene:layer-implementer | 9 | 0.6s | 0.3s |
| Read | orchestrator | 10 | 1.5s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 7 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-22T18:22:49.851Z | 17.9s | 607 | false | false |
| Bash | orchestrator | 2026-11-22T18:23:44.430Z | 6.8s | 816 | false | false |
| Bash | devscene:layer-implementer | 2026-11-22T18:23:10.697Z | 5.6s | 510 | false | false |
| Bash | devscene:layer-implementer | 2026-11-22T18:22:19.765Z | 3.5s | 136 | false | false |
| Bash | devscene:layer-implementer | 2026-11-22T18:22:08.837Z | 1.0s | 435 | false | false |
| Bash | orchestrator | 2026-11-22T18:18:43.010Z | 0.5s | 2690 | false | false |
| Bash | orchestrator | 2026-11-22T18:18:51.754Z | 0.4s | 4140 | false | false |
| Bash | orchestrator | 2026-11-22T18:18:47.219Z | 0.4s | 7625 | false | false |
| Bash | devscene:layer-implementer | 2026-11-22T18:24:34.756Z | 0.3s | 63 | false | false |
| Bash | devscene:layer-implementer | 2026-11-22T18:24:30.292Z | 0.3s | 182 | true | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 general layer | 3m 11s | 20 | 15688 | 42 | 1552558 | 1466831 | 85685 | 0.4741 |
| devscene:layer-implementer | Implement Task 2 general layer | 47.3s | 9 | 3961 | 20 | 543960 | 493650 | 50290 | 0.1171 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.71 |
| Cost — claude-opus-5-5 | $3.71 |
| Input tokens (uncached) | 124 |
| Total input tokens (incl. cache) | 5669961 |
| Output tokens | 28821 |
| Thinking tokens (main thread) | 1905 |
| Cache read tokens | 5360759 |
| Cache write tokens | 309078 |
| Cache write tokens, main thread (5m / 1h) | 0 / 173103 |
| Cache hit ratio | 0.9455 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 62 | 3573443 | 451 | 3400278 | 173103 |
| sub-agents | 62 | 2096518 | 19649 | 1960481 | 135975 |
| remainder | 0 | 0 | 8721 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 4 |
| Sub-agents spawned / failed / killed | 2 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 37 |
| Time to first token | 3.2s |
| Rate-limit peak | seven_day 0.51 |
