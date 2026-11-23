# Run analytics — fix_analyze_provenance_line_growth

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Engine / planning node sessions | 1 / 0 |
| Span | 20.7s |
| Wall | 20.7s |
| Session wall, summed over sessions | 20.7s |
| Active | 20.7s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $0.47 |
| Input tokens (uncached) | 16 |
| Total input tokens (incl. cache) | 397230 |
| Output tokens | 2073 |
| Thinking tokens (main thread) | 162 |
| Cache read tokens | 352993 |
| Cache write tokens | 44221 |
| Cache write tokens, main thread (5m / 1h) | 0 / 44221 |
| Cache hit ratio | 0.8886 |
| Requests | 8 |
| Request latency p50 / p90 / p99 / max | 1.5s / 4.2s / 4.2s / 4.2s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | — |
| Rate-limit peak | seven_day 0.57 |

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
