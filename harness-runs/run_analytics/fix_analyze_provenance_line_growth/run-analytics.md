# Run analytics — fix_analyze_provenance_line_growth

## Whole run

| Measure | Value |
|---|---|
| Sessions | 9 (0 incomplete) |
| Engine / planning node sessions | 3 / 6 |
| Span | 55m 57s |
| Wall | 43m 40s |
| Session wall, summed over sessions | 47m 13s |
| Active | 43m 40s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $27.11 |
| Input tokens (uncached) | 934 |
| Total input tokens (incl. cache) | 43920151 |
| Output tokens | 240951 |
| Thinking tokens (main thread) | 54048 |
| Cache read tokens | 41831695 |
| Cache write tokens | 2087522 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1160244 |
| Cache hit ratio | 0.9524 |
| Requests | 448 |
| Request latency p50 / p90 / p99 / max | 1.7s / 6.8s / 28.8s / 50.0s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 12 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Fix skeptic Finding 1 — 4m 37s (session 9) |
| Rate-limit peak | seven_day 0.6 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 3 | 1-plan_writer | 4m 40s | 4m 40s | 0.0s | 4m 41s | $2.57 |
| 4 | 2-architecture_review | 2m 15s | 2m 15s | 0.0s | 2m 16s | $1.66 |
| 5 | 3-plan_review | 3m 19s | 3m 19s | 0.0s | 3m 20s | $2.66 |
| 6 | 4-plan_writer | 1m 02s | 1m 02s | 0.0s | 1m 04s | $0.49 |
| 7 | 5-architecture_review | 1m 17s | 1m 17s | 0.0s | 1m 18s | $1.48 |
| 8 | 6-plan_review | 3m 58s | 3m 58s | 0.0s | 3m 59s | $2.57 |

## Network refusals

9 of 9 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No Run gates round log was scanned.

## Session 1 — 2026-11-23T16:14:40.045Z → 2026-11-23T16:15:00.771Z

Session id: `0b998a7e-1ac5-47f1-b9ec-326e1d7b6f5e`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 20.7s | 22.0s | 20.4s | 0.0s | 0.0s | 20.7s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 8 | 1.5s | 4.2s | 4.2s | 4.2s | 0 |
| orchestrator | 8 | 1.5s | 4.2s | 4.2s | 4.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.7s | 0.5s |
| Read | orchestrator | 3 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:14:42.167Z | 0.5s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:54.495Z | 0.4s | 84 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:42.615Z | 0.3s | 34 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:51.065Z | 0.3s | 451 | true | false |
| Bash | orchestrator | 2026-11-23T16:14:43.986Z | 0.2s | 137 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:43.170Z | 0.2s | 27 | false | false |
| Bash | orchestrator | 2026-11-23T16:14:47.736Z | 0.2s | 270 | true | false |
| Bash | orchestrator | 2026-11-23T16:14:44.818Z | 0.2s | 2156 | false | false |
| Skill | orchestrator | 2026-11-23T16:14:40.291Z | 0.0s | 54 | false | false |
| Read | orchestrator | 2026-11-23T16:14:46.632Z | 0.0s | 3548 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.47 |
| Cost — claude-opus-5-5 | $0.47 |
| Input tokens (uncached) | 16 |
| Total input tokens (incl. cache) | 397230 |
| Output tokens | 2073 |
| Thinking tokens (main thread) | 162 |
| Cache read tokens | 352993 |
| Cache write tokens | 44221 |
| Cache write tokens, main thread (5m / 1h) | 0 / 44221 |
| Cache hit ratio | 0.8886 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 16 | 397230 | 547 | 352993 | 44221 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 1526 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 14 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.57 |

## Session 2 — 2026-11-23T16:26:22.939Z → 2026-11-23T16:27:45.880Z

Session id: `a7ac9bb9-12d7-44f2-8a94-df4b47fbb782`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 22s | 1m 24s | 1m 06s | 0.0s | 0.0s | 1m 22s | 9.7s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 23 | 1.2s | 1.9s | 4.7s | 4.7s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.5s | 1.5s | 1.5s | 1.5s | 0 |
| orchestrator | 21 | 1.2s | 1.9s | 4.7s | 4.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 2 | 9.7s | 6.6s |
| Bash | orchestrator | 16 | 17.6s | 6.7s |
| Read | devscene:prompt-injection-reviewer | 4 | 0.0s | 0.0s |
| Read | orchestrator | 3 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 3 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:27:32.224Z | 6.7s | 619 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:07.022Z | 6.4s | 624 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:37.503Z | 0.4s | 60 | true | false |
| Bash | orchestrator | 2026-11-23T16:26:25.734Z | 0.4s | 2034 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:40.764Z | 0.4s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:01.660Z | 0.3s | 160 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:32.012Z | 0.3s | 4639 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:29.171Z | 0.3s | 8065 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:48.142Z | 0.3s | 161 | false | false |
| Bash | orchestrator | 2026-11-23T16:26:36.016Z | 0.2s | 309 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 3.1s | 1 | 249 | 4 | 29799 | 11597 | 18198 | 0.0384 |
| devscene:prompt-injection-reviewer | Screen clarification answer | 6.6s | 1 | 606 | 4 | 25461 | 17087 | 8370 | 0.0797 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.06 |
| Cost — claude-opus-5-5 | $1.06 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 1367856 |
| Output tokens | 7223 |
| Thinking tokens (main thread) | 558 |
| Cache read tokens | 1275610 |
| Cache write tokens | 92194 |
| Cache write tokens, main thread (5m / 1h) | 0 / 65626 |
| Cache hit ratio | 0.9326 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 44 | 1312596 | 739 | 1246926 | 65626 |
| sub-agents | 8 | 55260 | 855 | 28684 | 26568 |
| remainder | 0 | 0 | 5629 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 2 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 27 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.58 |

## Session 3 — 2026-11-23T16:27:49.064Z → 2026-11-23T16:32:29.579Z

Session id: `4752eb10-97ae-4a7f-a4a4-bd1d9e5135e6`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 40s | 4m 41s | 4m 35s | 0.0s | 0.0s | 4m 40s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 36 | 1.7s | 8.4s | 25.7s | 25.7s | 0 |
| orchestrator | 36 | 1.7s | 8.4s | 25.7s | 25.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 18 | 5.8s | 0.6s |
| Edit | orchestrator | 13 | 0.5s | 0.0s |
| Read | orchestrator | 16 | 0.7s | 0.2s |
| Write | orchestrator | 5 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:28:07.040Z | 0.6s | 2288 | false | false |
| Bash | orchestrator | 2026-11-23T16:27:49.273Z | 0.5s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:28:09.449Z | 0.4s | 753 | false | false |
| Bash | orchestrator | 2026-11-23T16:29:18.243Z | 0.3s | 1013 | false | false |
| Bash | orchestrator | 2026-11-23T16:28:14.304Z | 0.3s | 24704 | false | false |
| Bash | orchestrator | 2026-11-23T16:31:28.308Z | 0.3s | 215 | false | false |
| Bash | orchestrator | 2026-11-23T16:28:18.687Z | 0.3s | 1687 | false | false |
| Read | orchestrator | 2026-11-23T16:27:54.158Z | 0.2s | 67351 | false | false |
| Bash | orchestrator | 2026-11-23T16:28:12.472Z | 0.2s | 1914 | false | false |
| Bash | orchestrator | 2026-11-23T16:30:07.062Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.57 |
| Cost — claude-opus-5-5 | $2.57 |
| Input tokens (uncached) | 72 |
| Total input tokens (incl. cache) | 4183725 |
| Output tokens | 31568 |
| Thinking tokens (main thread) | 10055 |
| Cache read tokens | 4043008 |
| Cache write tokens | 140645 |
| Cache write tokens, main thread (5m / 1h) | 0 / 140645 |
| Cache hit ratio | 0.9664 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 72 | 4183725 | 600 | 4043008 | 140645 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 30968 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 53 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.58 |

## Session 4 — 2026-11-23T16:32:34.011Z → 2026-11-23T16:34:49.219Z

Session id: `cfc1b1b1-d5e7-4e52-bb18-b662dd88a9c0`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 15s | 2m 16s | 2m 12s | 0.0s | 0.0s | 2m 15s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 15 | 1.7s | 29.1s | 37.7s | 37.7s | 0 |
| orchestrator | 15 | 1.7s | 29.1s | 37.7s | 37.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 3.5s | 0.7s |
| Read | orchestrator | 17 | 1.0s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:33:30.507Z | 0.7s | 15208 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:34.162Z | 0.6s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:33:47.859Z | 0.4s | 1029 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:36.559Z | 0.3s | 6981 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:55.959Z | 0.3s | 608 | false | false |
| Read | orchestrator | 2026-11-23T16:32:45.884Z | 0.3s | 67351 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:39.242Z | 0.2s | 1313 | false | false |
| Bash | orchestrator | 2026-11-23T16:33:37.880Z | 0.2s | 3124 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:50.667Z | 0.2s | 13456 | false | false |
| Read | orchestrator | 2026-11-23T16:32:46.886Z | 0.2s | 31668 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.66 |
| Cost — claude-opus-5-5 | $1.66 |
| Input tokens (uncached) | 30 |
| Total input tokens (incl. cache) | 1440585 |
| Output tokens | 14453 |
| Thinking tokens (main thread) | 8318 |
| Cache read tokens | 1301465 |
| Cache write tokens | 139090 |
| Cache write tokens, main thread (5m / 1h) | 0 / 139090 |
| Cache hit ratio | 0.9034 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 30 | 1440585 | 854 | 1301465 | 139090 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 13599 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 28 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.58 |

## Session 5 — 2026-11-23T16:32:33.946Z → 2026-11-23T16:35:53.230Z

Session id: `b89d6e23-345c-4a99-afe7-5fd4caeb7572`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 19s | 3m 20s | 3m 12s | 0.0s | 0.0s | 3m 19s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 32 | 1.7s | 10.0s | 24.5s | 24.5s | 0 |
| orchestrator | 32 | 1.7s | 10.0s | 24.5s | 24.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 22 | 7.2s | 0.8s |
| Read | orchestrator | 23 | 1.1s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:33:52.994Z | 0.8s | 10895 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:34.105Z | 0.7s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:39.821Z | 0.3s | 1405 | false | false |
| Bash | orchestrator | 2026-11-23T16:32:36.559Z | 0.3s | 5977 | false | false |
| Bash | orchestrator | 2026-11-23T16:33:48.577Z | 0.3s | 2250 | false | false |
| Bash | orchestrator | 2026-11-23T16:33:08.487Z | 0.3s | 7062 | false | false |
| Bash | orchestrator | 2026-11-23T16:34:37.771Z | 0.3s | 45 | false | false |
| Bash | orchestrator | 2026-11-23T16:34:10.524Z | 0.3s | 528 | false | false |
| Bash | orchestrator | 2026-11-23T16:34:47.391Z | 0.3s | 24924 | false | false |
| Read | orchestrator | 2026-11-23T16:33:12.408Z | 0.3s | 67351 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.66 |
| Cost — claude-opus-5-5 | $2.66 |
| Input tokens (uncached) | 64 |
| Total input tokens (incl. cache) | 4079563 |
| Output tokens | 20863 |
| Thinking tokens (main thread) | 11737 |
| Cache read tokens | 3896661 |
| Cache write tokens | 182838 |
| Cache write tokens, main thread (5m / 1h) | 0 / 182838 |
| Cache hit ratio | 0.9552 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 64 | 4079563 | 1034 | 3896661 | 182838 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 19829 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 47 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.58 |

## Session 6 — 2026-11-23T16:36:03.213Z → 2026-11-23T16:37:05.998Z

Session id: `b05b65f1-e417-4fa2-9a80-f7d9a6e0b9c3`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 02s | 1m 04s | 1m 02s | 0.0s | 0.0s | 1m 02s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 9 | 1.8s | 8.4s | 8.4s | 8.4s | 0 |
| orchestrator | 9 | 1.8s | 8.4s | 8.4s | 8.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 3 | 1.2s | 0.6s |
| Edit | orchestrator | 8 | 0.3s | 0.0s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:36:03.323Z | 0.6s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:36:55.139Z | 0.3s | 6 | false | false |
| Bash | orchestrator | 2026-11-23T16:36:17.697Z | 0.3s | 1260 | false | false |
| Edit | orchestrator | 2026-11-23T16:36:52.052Z | 0.0s | 244 | false | false |
| Write | orchestrator | 2026-11-23T16:36:58.073Z | 0.0s | 247 | false | false |
| Edit | orchestrator | 2026-11-23T16:36:35.397Z | 0.0s | 244 | false | false |
| Edit | orchestrator | 2026-11-23T16:36:37.252Z | 0.0s | 244 | false | false |
| Edit | orchestrator | 2026-11-23T16:36:48.502Z | 0.0s | 244 | false | false |
| Read | orchestrator | 2026-11-23T16:36:05.367Z | 0.0s | 4695 | false | false |
| Edit | orchestrator | 2026-11-23T16:36:33.055Z | 0.0s | 244 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.49 |
| Cost — claude-opus-5-5 | $0.49 |
| Input tokens (uncached) | 18 |
| Total input tokens (incl. cache) | 353220 |
| Output tokens | 7629 |
| Thinking tokens (main thread) | 2117 |
| Cache read tokens | 318478 |
| Cache write tokens | 34724 |
| Cache write tokens, main thread (5m / 1h) | 0 / 34724 |
| Cache hit ratio | 0.9016 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 18 | 353220 | 98 | 318478 | 34724 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7531 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 20 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.58 |

## Session 7 — 2026-11-23T16:37:09.798Z → 2026-11-23T16:38:26.947Z

Session id: `8a60c490-6e6a-4522-97f2-7ce8289c6269`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 17s | 1m 18s | 1m 15s | 0.0s | 0.0s | 1m 17s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 15 | 1.9s | 7.1s | 13.1s | 13.1s | 0 |
| orchestrator | 15 | 1.9s | 7.1s | 13.1s | 13.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.9s | 0.4s |
| Read | orchestrator | 20 | 0.6s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:37:32.479Z | 0.4s | 1059 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:09.901Z | 0.4s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:23.348Z | 0.4s | 852 | false | false |
| Bash | orchestrator | 2026-11-23T16:38:03.011Z | 0.3s | 436 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:54.991Z | 0.3s | 13577 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:15.604Z | 0.3s | 730 | false | false |
| Read | orchestrator | 2026-11-23T16:37:27.849Z | 0.2s | 31668 | false | false |
| Bash | orchestrator | 2026-11-23T16:38:11.404Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:13.459Z | 0.1s | 4345 | false | false |
| Write | orchestrator | 2026-11-23T16:38:18.495Z | 0.0s | 241 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.48 |
| Cost — claude-opus-5-5 | $1.48 |
| Input tokens (uncached) | 30 |
| Total input tokens (incl. cache) | 1349085 |
| Output tokens | 8349 |
| Thinking tokens (main thread) | 2781 |
| Cache read tokens | 1215265 |
| Cache write tokens | 133790 |
| Cache write tokens, main thread (5m / 1h) | 0 / 133790 |
| Cache hit ratio | 0.9008 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 30 | 1349085 | 155 | 1215265 | 133790 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8194 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 30 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.59 |

## Session 8 — 2026-11-23T16:37:09.824Z → 2026-11-23T16:41:08.013Z

Session id: `f4db1ed5-44f0-40b6-a197-f1d8bbfa1ad7`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 58s | 3m 59s | 3m 51s | 0.0s | 0.0s | 3m 58s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 26 | 1.8s | 24.2s | 50.0s | 50.0s | 0 |
| orchestrator | 26 | 1.8s | 24.2s | 50.0s | 50.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 20 | 8.4s | 1.3s |
| Read | orchestrator | 23 | 1.1s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-23T16:38:38.839Z | 1.3s | 5633 | false | false |
| Bash | orchestrator | 2026-11-23T16:38:52.831Z | 1.2s | 496 | true | false |
| Bash | orchestrator | 2026-11-23T16:38:47.802Z | 0.5s | 2647 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:09.905Z | 0.5s | 62 | false | false |
| Bash | orchestrator | 2026-11-23T16:40:35.846Z | 0.4s | 344 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:43.323Z | 0.4s | 13823 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:44.530Z | 0.4s | 14354 | false | false |
| Bash | orchestrator | 2026-11-23T16:39:49.015Z | 0.3s | 5269 | false | false |
| Bash | orchestrator | 2026-11-23T16:38:56.991Z | 0.3s | 4035 | false | false |
| Bash | orchestrator | 2026-11-23T16:37:34.538Z | 0.3s | 10777 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.57 |
| Cost — claude-opus-5-5 | $2.57 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 3270514 |
| Output tokens | 26109 |
| Thinking tokens (main thread) | 16055 |
| Cache read tokens | 3091836 |
| Cache write tokens | 178626 |
| Cache write tokens, main thread (5m / 1h) | 0 / 178626 |
| Cache hit ratio | 0.9454 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 52 | 3270514 | 940 | 3091836 | 178626 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25169 | 0 | 0 |

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
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.59 |

## Session 9 — 2026-11-23T16:41:41.075Z → 2026-11-23T17:10:37.310Z

Session id: `77743674-76f0-420e-87ec-cdaee6b3f5d0`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 28m 56s | 28m 57s | 18m 22s | 0.0s | 0.0s | 28m 56s | 22m 44s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 284 | 1.7s | 4.2s | 19.1s | 28.8s | 0 |
| devscene:architecture-reviewer | 8 | 3.0s | 6.9s | 6.9s | 6.9s | 0 |
| devscene:branch-reviewer | 29 | 2.5s | 18.0s | 28.8s | 28.8s | 0 |
| devscene:layer-implementer | 112 | 1.8s | 3.2s | 16.0s | 21.0s | 0 |
| devscene:review-plan-reviewer | 32 | 2.1s | 6.3s | 10.7s | 10.7s | 0 |
| devscene:skeptic-reviewer | 13 | 2.6s | 14.7s | 16.1s | 16.1s | 0 |
| orchestrator | 90 | 1.3s | 2.1s | 7.6s | 7.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 16 | 22m 44s | 4m 37s |
| Bash | devscene:architecture-reviewer | 7 | 1.9s | 0.3s |
| Bash | devscene:branch-reviewer | 26 | 8.2s | 1.5s |
| Bash | devscene:layer-implementer | 111 | 16m 38s | 2m 53s |
| Bash | devscene:review-plan-reviewer | 22 | 17.9s | 2.8s |
| Bash | devscene:skeptic-reviewer | 11 | 15.8s | 2.5s |
| Bash | orchestrator | 75 | 2m 41s | 10.0s |
| Edit | devscene:layer-implementer | 19 | 0.9s | 0.1s |
| Edit | orchestrator | 9 | 0.6s | 0.1s |
| Read | devscene:architecture-reviewer | 4 | 0.8s | 0.3s |
| Read | devscene:branch-reviewer | 15 | 1.1s | 0.3s |
| Read | devscene:layer-implementer | 28 | 2.3s | 0.4s |
| Read | devscene:review-plan-reviewer | 32 | 1.4s | 0.2s |
| Read | devscene:skeptic-reviewer | 2 | 0.3s | 0.2s |
| Read | orchestrator | 13 | 2.2s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 1 | 0.0s | 0.0s |
| Write | devscene:review-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.1s | 0.0s |
| Write | orchestrator | 2 | 0.2s | 0.1s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-23T17:06:38.522Z | 2m 53s | 496 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:06:37.981Z | 2m 39s | 14378 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:06:37.424Z | 2m 18s | 1420 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:06:36.837Z | 1m 36s | 3520 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:06:36.223Z | 51.3s | 508 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:06:02.318Z | 32.5s | 1648 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:05:18.176Z | 32.4s | 1895 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T17:00:23.134Z | 22.5s | 804 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T16:43:02.304Z | 21.6s | 35 | false | false |
| Bash | devscene:layer-implementer | 2026-11-23T16:43:01.804Z | 21.5s | 804 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 8 | 1m 32s |
| devscene:layer-implementer | git diff --name-only HEAD | 4 | 32.9s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 4 | 32.0s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 2.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/conventions-provenance-line.test.mjs | 5 | 33.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-repo-resolution-corpus.test.mjs test/no-container-home-paths.test.mjs test/untrusted-input-corpus.test.mjs test/commit-ste | 3 | 17.1s |
| devscene:review-plan-reviewer | git rev-parse --show-toplevel | 3 | 2.1s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/fix_analyze_provenance_line_growth_co | 3 | 22.7s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/fix_analyze_provenance_line_growth_story_plan | 4 | 25.5s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE | 14 | 4.4s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (plugin) | 1m 06s | 11 | 4450 | 24 | 517910 | 467877 | 50009 | 0.0381 |
| devscene:layer-implementer | Implement Task 2 (plugin) | 55.4s | 13 | 4221 | 28 | 591774 | 546669 | 45077 | 0.0319 |
| devscene:layer-implementer | Implement Task 3 (plugin) | 1m 20s | 18 | 7640 | 38 | 908444 | 855355 | 53051 | 0.0466 |
| devscene:layer-implementer | Implement Task 4 (cli) | 1m 07s | 10 | 5590 | 22 | 448166 | 412236 | 35908 | 0.0387 |
| devscene:architecture-reviewer | Architecture review of branch | 44.3s | 8 | 4592 | 18 | 580446 | 493170 | 87258 | 0.0255 |
| devscene:branch-reviewer | End-of-branch code review | 3m 28s | 26 | 22566 | 54 | 3195543 | 3032055 | 163434 | 0.1198 |
| devscene:review-plan-reviewer | Meta-review code review | 59.0s | 11 | 6576 | 24 | 555603 | 505441 | 50138 | 0.034 |
| devscene:branch-reviewer | Adjust code review per meta-review | 14.3s | 3 | 1608 | 8 | 119974 | 103421 | 16545 | 0.0083 |
| devscene:review-plan-reviewer | Meta-review code review round 2 | 1m 05s | 14 | 6853 | 30 | 1054806 | 942021 | 112755 | 0.0378 |
| devscene:layer-implementer | Fix code-review Finding 3 | 40.7s | 11 | 2577 | 24 | 444482 | 408076 | 36382 | 0.0235 |
| devscene:layer-implementer | Fix code-review Finding 1 | 1m 16s | 12 | 4548 | 26 | 530155 | 488210 | 41919 | 0.044 |
| devscene:layer-implementer | Fix code-review Finding 2 (cli) | 1m 00s | 15 | 4704 | 32 | 597774 | 567339 | 30403 | 0.035 |
| devscene:layer-implementer | Fix code-review Finding 2 (plugin) | 1m 24s | 10 | 5682 | 22 | 419012 | 389407 | 29583 | 0.049 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 1m 57s | 13 | 11193 | 28 | 753761 | 694208 | 59525 | 0.0679 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 45.8s | 7 | 3564 | 16 | 308056 | 259371 | 48669 | 0.0264 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 4m 37s | 12 | 3471 | 26 | 513472 | 473392 | 40054 | 0.1595 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $14.15 |
| Cost — claude-opus-5-5 | $14.15 |
| Input tokens (uncached) | 600 |
| Total input tokens (incl. cache) | 27478373 |
| Output tokens | 122684 |
| Thinking tokens (main thread) | 2265 |
| Cache read tokens | 26336379 |
| Cache write tokens | 1141394 |
| Cache write tokens, main thread (5m / 1h) | 0 / 240684 |
| Cache hit ratio | 0.9584 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 180 | 15938995 | 2316 | 15698131 | 240684 |
| sub-agents | 420 | 11539378 | 99835 | 10638248 | 900710 |
| remainder | 0 | 0 | 20533 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 8 |
| Sub-agents spawned / failed / killed | 16 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 118 |
| Time to first token | 1.6s |
| Rate-limit peak | seven_day 0.6 |
