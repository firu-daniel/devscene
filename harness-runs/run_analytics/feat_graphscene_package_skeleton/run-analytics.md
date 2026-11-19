# Run analytics — feat_graphscene_package_skeleton

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 19m 16s |
| Wall | 18m 36s |
| Session wall, summed over sessions | 19m 59s |
| Active | 18m 36s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $12.02 |
| Input tokens (uncached) | 310 |
| Total input tokens (incl. cache) | 15879083 |
| Output tokens | 122278 |
| Thinking tokens (main thread) | 48847 |
| Cache read tokens | 15007764 |
| Cache write tokens | 871009 |
| Cache write tokens, main thread (5m / 1h) | 0 / 740242 |
| Cache hit ratio | 0.9451 |
| Requests | 150 |
| Request latency p50 / p90 / p99 / max | 2.0s / 12.0s / 48.6s / 55.2s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 3 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 1 (general) — 2m 42s (session 5) |
| Rate-limit peak | seven_day 0.31 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 8m 11s | 8m 11s | 0.0s | 8m 12s | $3.28 |
| 3 | 2-architecture_review | 1m 23s | 1m 23s | 0.0s | 1m 25s | $1.26 |
| 4 | 3-plan_review | 4m 20s | 4m 20s | 0.0s | 4m 21s | $2.71 |

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

## Session 1 — 2026-11-19T11:09:02.597Z → 2026-11-19T11:09:57.584Z

Session id: `1c24dda2-aae9-47ff-a8c2-c8817c0d1fd0`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 54.9s | 56.7s | 48.1s | 0.0s | 0.0s | 54.9s | 3.7s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 15 | 1.6s | 4.9s | 7.0s | 7.0s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.9s | 1.9s | 1.9s | 1.9s | 0 |
| orchestrator | 14 | 1.6s | 4.9s | 7.0s | 7.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 3.7s | 3.7s |
| Bash | orchestrator | 15 | 9.9s | 6.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 2 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:09:46.518Z | 6.1s | 611 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:05.150Z | 0.5s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:26.834Z | 0.3s | 159 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:38.279Z | 0.3s | 6 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:15.111Z | 0.2s | 6 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:05.500Z | 0.2s | 32 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:13.322Z | 0.2s | 160 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:06.041Z | 0.2s | 27 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:30.031Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:29.030Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 3.7s | 1 | 287 | 4 | 26978 | 10501 | 16473 | 0.0689 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.83 |
| Cost — claude-opus-5-5 | $0.83 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 829150 |
| Output tokens | 5271 |
| Thinking tokens (main thread) | 324 |
| Cache read tokens | 751800 |
| Cache write tokens | 77316 |
| Cache write tokens, main thread (5m / 1h) | 0 / 60843 |
| Cache hit ratio | 0.9067 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 30 | 802172 | 219 | 741299 | 60843 |
| sub-agents | 4 | 26978 | 287 | 10501 | 16473 |
| remainder | 0 | 0 | 4765 | 0 | 0 |

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
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.3 |

## Session 2 — 2026-11-19T11:10:00.963Z → 2026-11-19T11:18:12.400Z

Session id: `9360c2b9-126e-46ea-bfff-9c4c64da0368`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 8m 11s | 8m 12s | 8m 05s | 0.0s | 0.0s | 8m 11s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 34 | 2.1s | 39.1s | 44.6s | 44.6s | 0 |
| orchestrator | 34 | 2.1s | 39.1s | 44.6s | 44.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 22 | 7.4s | 0.7s |
| Edit | orchestrator | 2 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 0.8s | 0.3s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:12:24.608Z | 0.7s | 2824 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:25.591Z | 0.5s | 11765 | false | false |
| Bash | orchestrator | 2026-11-19T11:14:45.927Z | 0.4s | 610 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:29.599Z | 0.4s | 11920 | false | false |
| Bash | orchestrator | 2026-11-19T11:13:14.075Z | 0.4s | 3763 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:00.969Z | 0.3s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:12:28.240Z | 0.3s | 4108 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:17.957Z | 0.3s | 2259 | false | false |
| Bash | orchestrator | 2026-11-19T11:11:37.820Z | 0.3s | 1312 | false | false |
| Bash | orchestrator | 2026-11-19T11:13:22.384Z | 0.3s | 7342 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.28 |
| Cost — claude-opus-5-5 | $3.28 |
| Input tokens (uncached) | 68 |
| Total input tokens (incl. cache) | 4087226 |
| Output tokens | 50490 |
| Thinking tokens (main thread) | 25831 |
| Cache read tokens | 3901574 |
| Cache write tokens | 185584 |
| Cache write tokens, main thread (5m / 1h) | 0 / 185584 |
| Cache hit ratio | 0.9546 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 68 | 4087226 | 290 | 3901574 | 185584 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 50200 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 47 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.31 |

## Session 3 — 2026-11-19T11:18:16.113Z → 2026-11-19T11:19:40.070Z

Session id: `2b50df55-3a37-43b9-9699-8e535c104c59`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 23s | 1m 25s | 1m 22s | 0.0s | 0.0s | 1m 23s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 2.3s | 9.6s | 15.4s | 15.4s | 0 |
| orchestrator | 13 | 2.3s | 9.6s | 15.4s | 15.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.5s | 0.5s |
| Read | orchestrator | 16 | 0.9s | 0.4s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:18:16.577Z | 0.5s | 60 | false | false |
| Read | orchestrator | 2026-11-19T11:18:23.570Z | 0.4s | 31668 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:50.926Z | 0.3s | 7118 | true | false |
| Bash | orchestrator | 2026-11-19T11:19:01.036Z | 0.3s | 4350 | false | false |
| Read | orchestrator | 2026-11-19T11:18:22.569Z | 0.3s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:17.140Z | 0.2s | 5810 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:22.810Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:15.816Z | 0.2s | 1873 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:32.531Z | 0.2s | 166 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:19.804Z | 0.2s | 1555 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.26 |
| Cost — claude-opus-5-5 | $1.26 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1069974 |
| Output tokens | 8706 |
| Thinking tokens (main thread) | 4011 |
| Cache read tokens | 958786 |
| Cache write tokens | 111162 |
| Cache write tokens, main thread (5m / 1h) | 0 / 111162 |
| Cache hit ratio | 0.8961 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1069974 | 142 | 958786 | 111162 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8564 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 26 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.31 |

## Session 4 — 2026-11-19T11:18:16.145Z → 2026-11-19T11:22:36.423Z

Session id: `b8047493-e048-4900-ad0d-0625fd5aee21`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 20s | 4m 21s | 4m 16s | 0.0s | 0.0s | 4m 20s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 27 | 3.6s | 28.7s | 48.6s | 48.6s | 0 |
| orchestrator | 27 | 3.6s | 28.7s | 48.6s | 48.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 25 | 6.8s | 0.5s |
| Read | orchestrator | 18 | 0.9s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:18:16.577Z | 0.5s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:58.024Z | 0.4s | 486 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:23.167Z | 0.3s | 9962 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:26.816Z | 0.3s | 1108 | false | false |
| Bash | orchestrator | 2026-11-19T11:20:24.894Z | 0.3s | 3244 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:35.886Z | 0.3s | 9200 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:33.183Z | 0.3s | 9261 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:47.303Z | 0.3s | 16033 | false | false |
| Read | orchestrator | 2026-11-19T11:18:28.418Z | 0.3s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:17.549Z | 0.2s | 7963 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.71 |
| Cost — claude-opus-5-5 | $2.71 |
| Input tokens (uncached) | 54 |
| Total input tokens (incl. cache) | 3663428 |
| Output tokens | 26449 |
| Thinking tokens (main thread) | 17219 |
| Cache read tokens | 3477283 |
| Cache write tokens | 186091 |
| Cache write tokens, main thread (5m / 1h) | 0 / 186091 |
| Cache hit ratio | 0.9492 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 54 | 3663428 | 948 | 3477283 | 186091 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25501 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 45 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.31 |

## Session 5 — 2026-11-19T11:23:09.506Z → 2026-11-19T11:28:18.800Z

Session id: `020f1708-5577-4edb-993a-c9635f26c7fe`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 09s | 5m 11s | 4m 44s | 0.0s | 0.0s | 5m 09s | 3m 29s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 61 | 1.7s | 6.8s | 55.2s | 55.2s | 0 |
| devscene:layer-implementer | 28 | 2.4s | 12.6s | 55.2s | 55.2s | 0 |
| orchestrator | 33 | 1.5s | 2.5s | 9.5s | 9.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 2 | 3m 29s | 2m 42s |
| Bash | devscene:layer-implementer | 17 | 14.3s | 5.4s |
| Bash | orchestrator | 22 | 11.1s | 6.5s |
| Edit | devscene:layer-implementer | 11 | 0.4s | 0.0s |
| Read | devscene:layer-implementer | 10 | 0.5s | 0.2s |
| Read | orchestrator | 14 | 1.8s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 5 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:26:53.199Z | 6.5s | 782 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:16.323Z | 5.4s | 217 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:26.048Z | 4.7s | 507 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:27:36.070Z | 0.4s | 175 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:13.090Z | 0.4s | 280 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:27:32.286Z | 0.3s | 182 | true | false |
| Bash | orchestrator | 2026-11-19T11:23:11.638Z | 0.3s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:23:28.940Z | 0.3s | 155 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:24:25.563Z | 0.3s | 5117 | false | false |
| Read | orchestrator | 2026-11-19T11:23:48.744Z | 0.3s | 49208 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (general) | 2m 42s | 18 | 17526 | 38 | 1188801 | 1114390 | 74373 | 0.524 |
| devscene:layer-implementer | Implement Task 2 (general) | 47.0s | 10 | 5039 | 22 | 508492 | 468549 | 39921 | 0.1522 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.96 |
| Cost — claude-opus-5-5 | $3.96 |
| Input tokens (uncached) | 128 |
| Total input tokens (incl. cache) | 6229305 |
| Output tokens | 31362 |
| Thinking tokens (main thread) | 1462 |
| Cache read tokens | 5918321 |
| Cache write tokens | 310856 |
| Cache write tokens, main thread (5m / 1h) | 0 / 196562 |
| Cache hit ratio | 0.9501 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 68 | 4532012 | 762 | 4335382 | 196562 |
| sub-agents | 60 | 1697293 | 22565 | 1582939 | 114294 |
| remainder | 0 | 0 | 8035 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 2 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 42 |
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.31 |
