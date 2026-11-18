# Run analytics — fix_injection_verdict_tools_used_prefix

## Whole run

| Measure | Value |
|---|---|
| Sessions | 3 (0 incomplete) |
| Engine / planning node sessions | 3 / 0 |
| Span | 9m 31s |
| Wall | 2m 22s |
| Session wall, summed over sessions | 2m 22s |
| Active | 2m 22s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $2.14 |
| Input tokens (uncached) | 70 |
| Total input tokens (incl. cache) | 1644009 |
| Output tokens | 15528 |
| Thinking tokens (main thread) | 3129 |
| Cache read tokens | 1433501 |
| Cache write tokens | 210438 |
| Cache write tokens, main thread (5m / 1h) | 0 / 163958 |
| Cache hit ratio | 0.872 |
| Requests | 32 |
| Request latency p50 / p90 / p99 / max | 1.8s / 9.6s / 10.5s / 10.5s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:prompt-injection-reviewer — Screen task prompt for injection — 9.5s (session 2) |
| Rate-limit peak | seven_day 0.25 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Network refusals

3 of 3 sessions scanned.

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

## Session 2 — 2026-11-18T19:27:36.660Z → 2026-11-18T19:28:22.210Z

Session id: `359fd099-b68d-4f98-b4f0-1e083c729b62`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 45.5s | 46.6s | 45.7s | 0.0s | 0.0s | 45.5s | 9.5s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 10 | 1.5s | 9.6s | 9.6s | 9.6s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.3s | 7.0s | 7.0s | 7.0s | 0 |
| orchestrator | 8 | 1.5s | 9.6s | 9.6s | 9.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 9.5s | 9.5s |
| Bash | orchestrator | 9 | 1.6s | 0.2s |
| Grep | devscene:prompt-injection-reviewer | 1 | 0.0s | 0.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-18T19:27:39.340Z | 0.2s | 67 | false | false |
| Bash | orchestrator | 2026-11-18T19:28:06.589Z | 0.2s | 117 | true | false |
| Bash | orchestrator | 2026-11-18T19:27:47.505Z | 0.2s | 319 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:40.392Z | 0.1s | 39 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:41.250Z | 0.1s | 2046 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:45.567Z | 0.1s | 6 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:44.517Z | 0.1s | 6 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:39.890Z | 0.1s | 27 | false | false |
| Bash | orchestrator | 2026-11-18T19:27:46.367Z | 0.1s | 6 | false | false |
| Grep | devscene:prompt-injection-reviewer | 2026-11-18T19:27:59.422Z | 0.0s | 2429 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 9.5s | 2 | 962 | 6 | 47341 | 33542 | 13793 | 0.2102 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.64 |
| Cost — claude-opus-5-5 | $0.64 |
| Input tokens (uncached) | 22 |
| Total input tokens (incl. cache) | 475180 |
| Output tokens | 5080 |
| Thinking tokens (main thread) | 943 |
| Cache read tokens | 412613 |
| Cache write tokens | 62545 |
| Cache write tokens, main thread (5m / 1h) | 0 / 48752 |
| Cache hit ratio | 0.8683 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 16 | 427839 | 58 | 379071 | 48752 |
| sub-agents | 6 | 47341 | 962 | 33542 | 13793 |
| remainder | 0 | 0 | 4060 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 18 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.25 |

## Session 3 — 2026-11-18T19:32:00.117Z → 2026-11-18T19:32:44.637Z

Session id: `e141e332-3573-4e2a-bf67-586ca0c060b7`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 44.5s | 46.0s | 44.9s | 0.0s | 0.0s | 44.5s | 8.0s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 10 | 1.8s | 10.5s | 10.5s | 10.5s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.3s | 5.6s | 5.6s | 5.6s | 0 |
| orchestrator | 8 | 1.8s | 10.5s | 10.5s | 10.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 8.0s | 8.0s |
| Bash | orchestrator | 9 | 1.6s | 0.2s |
| Grep | devscene:prompt-injection-reviewer | 1 | 0.0s | 0.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.4s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-18T19:32:05.121Z | 0.3s | 59446 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:03.066Z | 0.2s | 67 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:09.455Z | 0.2s | 480 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:27.398Z | 0.2s | 117 | true | false |
| Bash | orchestrator | 2026-11-18T19:32:33.922Z | 0.1s | 83 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:07.305Z | 0.1s | 482 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:03.670Z | 0.1s | 27 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:04.223Z | 0.1s | 39 | false | false |
| Bash | orchestrator | 2026-11-18T19:32:11.746Z | 0.1s | 60 | true | false |
| Bash | orchestrator | 2026-11-18T19:32:06.422Z | 0.1s | 99 | true | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 8.0s | 2 | 820 | 6 | 47241 | 33569 | 13666 | 0.1816 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.77 |
| Cost — claude-opus-5-5 | $0.77 |
| Input tokens (uncached) | 22 |
| Total input tokens (incl. cache) | 580684 |
| Output tokens | 4794 |
| Thinking tokens (main thread) | 954 |
| Cache read tokens | 503456 |
| Cache write tokens | 77206 |
| Cache write tokens, main thread (5m / 1h) | 0 / 63540 |
| Cache hit ratio | 0.867 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 16 | 533443 | 98 | 469887 | 63540 |
| sub-agents | 6 | 47241 | 820 | 33569 | 13666 |
| remainder | 0 | 0 | 3876 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 18 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.25 |
