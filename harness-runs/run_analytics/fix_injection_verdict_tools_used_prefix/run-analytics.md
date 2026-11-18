# Run analytics — fix_injection_verdict_tools_used_prefix

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Engine / planning node sessions | 1 / 0 |
| Span | 52.0s |
| Wall | 52.0s |
| Session wall, summed over sessions | 52.0s |
| Active | 52.0s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $0.73 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 588145 |
| Output tokens | 5654 |
| Thinking tokens (main thread) | 1232 |
| Cache read tokens | 517432 |
| Cache write tokens | 70687 |
| Cache write tokens, main thread (5m / 1h) | 0 / 51666 |
| Cache hit ratio | 0.8798 |
| Requests | 12 |
| Request latency p50 / p90 / p99 / max | 2.2s / 5.3s / 9.6s / 9.6s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:prompt-injection-reviewer — Screen task prompt for injection — 7.8s (session 1) |
| Rate-limit peak | seven_day 0.25 |

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

## Session 1 — 2026-11-18T19:23:13.255Z → 2026-11-18T19:24:05.333Z

Session id: `a991c050-df1f-4f9b-a8dc-ac8f5d3712a6`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 52.0s | 53.4s | 52.2s | 0.0s | 0.0s | 52.0s | 7.8s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 12 | 2.2s | 5.3s | 9.6s | 9.6s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.3s | 5.3s | 5.3s | 5.3s | 0 |
| orchestrator | 10 | 2.2s | 9.6s | 9.6s | 9.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 7.8s | 7.8s |
| Bash | orchestrator | 11 | 2.0s | 0.2s |
| Grep | devscene:prompt-injection-reviewer | 1 | 0.1s | 0.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.1s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-18T19:23:17.105Z | 0.2s | 67 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:43.535Z | 0.2s | 117 | true | false |
| Bash | orchestrator | 2026-11-18T19:23:26.394Z | 0.2s | 167 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:23.740Z | 0.2s | 2054 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:50.140Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:21.874Z | 0.1s | 6 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:17.560Z | 0.1s | 39 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:19.601Z | 0.1s | 2156 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:49.659Z | 0.1s | 1419 | false | false |
| Bash | orchestrator | 2026-11-18T19:23:27.979Z | 0.1s | 6 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 7.8s | 2 | 766 | 6 | 46944 | 27917 | 19021 | 0.1499 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.73 |
| Cost — claude-opus-5-5 | $0.73 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 588145 |
| Output tokens | 5654 |
| Thinking tokens (main thread) | 1232 |
| Cache read tokens | 517432 |
| Cache write tokens | 70687 |
| Cache write tokens, main thread (5m / 1h) | 0 / 51666 |
| Cache hit ratio | 0.8798 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 20 | 541201 | 139 | 489515 | 51666 |
| sub-agents | 6 | 46944 | 766 | 27917 | 19021 |
| remainder | 0 | 0 | 4749 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 21 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.25 |
