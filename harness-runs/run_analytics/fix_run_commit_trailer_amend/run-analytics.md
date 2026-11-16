# Run analytics — fix_run_commit_trailer_amend

## Whole run

| Measure | Value |
|---|---|
| Sessions | 2 (0 incomplete) |
| Engine / planning node sessions | 1 / 1 |
| Span | 16m 55s |
| Wall | 16m 52s |
| Session wall, summed over sessions | 16m 52s |
| Active | 16m 52s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $8.65 |
| Input tokens (uncached) | 194 |
| Total input tokens (incl. cache) | 16956236 |
| Output tokens | 102569 |
| Thinking tokens (main thread) | 56163 |
| Cache read tokens | 16537387 |
| Cache write tokens | 418655 |
| Cache write tokens, main thread (5m / 1h) | 0 / 399163 |
| Cache hit ratio | 0.9753 |
| Requests | 95 |
| Request latency p50 / p90 / p99 / max | 2.6s / 17.9s / 55.3s / 55.3s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:prompt-injection-reviewer — Screen task prompt — 4.5s (session 1) |
| Rate-limit peak | seven_day 0.57 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 16m 00s | 16m 00s | 0.0s | 16m 01s | $7.77 |

## Network refusals

2 of 2 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No Run gates round log was scanned.

## Session 1 — 2026-11-16T11:02:05.326Z → 2026-11-16T11:02:57.530Z

Session id: `5537be86-4a23-4b6d-846b-8e75daf1b58c`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 52.2s | 53.4s | 46.3s | 0.0s | 0.0s | 52.2s | 4.5s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.4s | 1.9s | 4.4s | 4.4s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.4s | 1.4s | 1.4s | 1.4s | 0 |
| orchestrator | 16 | 1.4s | 1.9s | 4.4s | 4.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 4.5s | 4.5s |
| Bash | orchestrator | 15 | 7.6s | 5.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-16T11:02:47.970Z | 5.0s | 418 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:46.162Z | 0.4s | 71 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:07.299Z | 0.2s | 56 | false | false |
| Read | orchestrator | 2026-11-16T11:02:36.159Z | 0.2s | 28893 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:16.160Z | 0.1s | 156 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:27.653Z | 0.1s | 155 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:34.287Z | 0.1s | 1065 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:08.350Z | 0.1s | 27 | false | false |
| Bash | orchestrator | 2026-11-16T11:02:13.017Z | 0.1s | 6932 | true | false |
| Bash | orchestrator | 2026-11-16T11:02:07.750Z | 0.1s | 28 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 4.5s | 1 | 392 | 4 | 29970 | 10474 | 19492 | 0.088 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.88 |
| Cost — claude-opus-5-5 | $0.88 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 971519 |
| Output tokens | 5127 |
| Thinking tokens (main thread) | 214 |
| Cache read tokens | 889155 |
| Cache write tokens | 82328 |
| Cache write tokens, main thread (5m / 1h) | 0 / 62836 |
| Cache hit ratio | 0.9152 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 941549 | 326 | 878681 | 62836 |
| sub-agents | 4 | 29970 | 392 | 10474 | 19492 |
| remainder | 0 | 0 | 4409 | 0 | 0 |

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
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.56 |

## Session 2 — 2026-11-16T11:03:00.517Z → 2026-11-16T11:19:00.716Z

Session id: `12958e1c-7956-4611-ac40-3cf1a3e71403`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 16m 00s | 16m 01s | 15m 46s | 0.0s | 0.0s | 16m 00s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 78 | 3.8s | 21.5s | 55.3s | 55.3s | 0 |
| orchestrator | 78 | 3.8s | 21.5s | 55.3s | 55.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 70 | 16.1s | 1.6s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 21 | 1.3s | 0.2s |
| Write | orchestrator | 8 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-16T11:12:33.789Z | 1.6s | 1454 | false | false |
| Bash | orchestrator | 2026-11-16T11:14:34.268Z | 1.3s | 1653 | false | false |
| Bash | orchestrator | 2026-11-16T11:11:43.887Z | 1.1s | 3058 | false | false |
| Bash | orchestrator | 2026-11-16T11:03:00.533Z | 0.4s | 56 | false | false |
| Bash | orchestrator | 2026-11-16T11:03:59.766Z | 0.3s | 17599 | false | false |
| Bash | orchestrator | 2026-11-16T11:07:32.449Z | 0.2s | 3422 | false | false |
| Read | orchestrator | 2026-11-16T11:03:04.749Z | 0.2s | 41596 | false | false |
| Bash | orchestrator | 2026-11-16T11:10:35.991Z | 0.2s | 659 | false | false |
| Bash | orchestrator | 2026-11-16T11:05:24.931Z | 0.2s | 415 | false | false |
| Read | orchestrator | 2026-11-16T11:10:36.947Z | 0.2s | 27297 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $7.77 |
| Cost — claude-opus-5-5 | $7.77 |
| Input tokens (uncached) | 158 |
| Total input tokens (incl. cache) | 15984717 |
| Output tokens | 97442 |
| Thinking tokens (main thread) | 55949 |
| Cache read tokens | 15648232 |
| Cache write tokens | 336327 |
| Cache write tokens, main thread (5m / 1h) | 0 / 336327 |
| Cache hit ratio | 0.9789 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 158 | 15984717 | 812 | 15648232 | 336327 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 96630 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 103 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.57 |
