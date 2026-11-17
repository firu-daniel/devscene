# Run analytics — feat_structured_outputs_mechanism

## Whole run

| Measure | Value |
|---|---|
| Sessions | 2 (0 incomplete) |
| Engine / planning node sessions | 1 / 1 |
| Span | 14m 22s |
| Wall | 14m 19s |
| Session wall, summed over sessions | 14m 19s |
| Active | 14m 19s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $6.75 |
| Input tokens (uncached) | 154 |
| Total input tokens (incl. cache) | 11346730 |
| Output tokens | 91238 |
| Thinking tokens (main thread) | 44560 |
| Cache read tokens | 10998542 |
| Cache write tokens | 348034 |
| Cache write tokens, main thread (5m / 1h) | 0 / 327286 |
| Cache hit ratio | 0.9693 |
| Requests | 76 |
| Request latency p50 / p90 / p99 / max | 1.7s / 17.7s / 1m 16s / 1m 16s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:prompt-injection-reviewer — Screen task prompt — 5.0s (session 1) |
| Rate-limit peak | seven_day 0.01 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 13m 22s | 13m 22s | 0.0s | 13m 24s | $5.84 |

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

## Session 1 — 2026-11-17T09:23:06.948Z → 2026-11-17T09:24:04.457Z

Session id: `68cb81a0-3ebb-4c7d-82b7-d89705d235c5`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 57.5s | 58.6s | 52.0s | 0.0s | 0.0s | 57.5s | 5.0s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 19 | 1.4s | 2.3s | 4.4s | 4.4s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.7s | 1.7s | 1.7s | 1.7s | 0 |
| orchestrator | 18 | 1.4s | 2.3s | 4.4s | 4.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 5.0s | 5.0s |
| Bash | orchestrator | 16 | 7.5s | 4.9s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-17T09:23:53.299Z | 4.9s | 615 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:09.156Z | 0.2s | 61 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:18.720Z | 0.2s | 161 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:43.481Z | 0.1s | 235 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:31.043Z | 0.1s | 160 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:59.857Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:16.927Z | 0.1s | 750 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:13.462Z | 0.1s | 82 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:33.164Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-17T09:23:20.176Z | 0.1s | 11 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 5.0s | 1 | 438 | 4 | 31194 | 10442 | 20748 | 0.0885 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.91 |
| Cost — claude-opus-5-5 | $0.91 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 1063716 |
| Output tokens | 5564 |
| Thinking tokens (main thread) | 324 |
| Cache read tokens | 981214 |
| Cache write tokens | 82462 |
| Cache write tokens, main thread (5m / 1h) | 0 / 61714 |
| Cache hit ratio | 0.9224 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 36 | 1032522 | 700 | 970772 | 61714 |
| sub-agents | 4 | 31194 | 438 | 10442 | 20748 |
| remainder | 0 | 0 | 4426 | 0 | 0 |

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
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0 |

## Session 2 — 2026-11-17T09:24:07.144Z → 2026-11-17T09:37:29.525Z

Session id: `9a4d0b26-bd2b-4275-8c28-a8f2c6eac103`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 13m 22s | 13m 24s | 13m 15s | 0.0s | 0.0s | 13m 22s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 57 | 2.0s | 27.7s | 1m 16s | 1m 16s | 0 |
| orchestrator | 57 | 2.0s | 27.7s | 1m 16s | 1m 16s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 40 | 7.9s | 0.4s |
| Edit | orchestrator | 5 | 0.2s | 0.0s |
| Read | orchestrator | 23 | 1.3s | 0.2s |
| Write | orchestrator | 8 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-17T09:32:49.258Z | 0.4s | 474 | false | false |
| Bash | orchestrator | 2026-11-17T09:32:45.576Z | 0.3s | 467 | false | false |
| Bash | orchestrator | 2026-11-17T09:26:26.891Z | 0.3s | 1500 | false | false |
| Bash | orchestrator | 2026-11-17T09:26:34.665Z | 0.3s | 437 | false | false |
| Read | orchestrator | 2026-11-17T09:24:11.082Z | 0.2s | 44346 | false | false |
| Bash | orchestrator | 2026-11-17T09:26:37.482Z | 0.2s | 1033 | false | false |
| Bash | orchestrator | 2026-11-17T09:24:56.994Z | 0.2s | 547 | false | false |
| Read | orchestrator | 2026-11-17T09:24:12.189Z | 0.2s | 31149 | false | false |
| Bash | orchestrator | 2026-11-17T09:31:28.372Z | 0.2s | 542 | false | false |
| Bash | orchestrator | 2026-11-17T09:29:47.486Z | 0.2s | 8404 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| orchestrator | jq -R -r -s '[split("\n")[] \| fromjson? \| objects] as $ev \| [$ev[] \| select(.type == "user") \| .message.content[]? \| select(.type == "tool_result") \| .content \| | 3 | 0.9s |

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $5.84 |
| Cost — claude-opus-5-5 | $5.84 |
| Input tokens (uncached) | 114 |
| Total input tokens (incl. cache) | 10283014 |
| Output tokens | 85674 |
| Thinking tokens (main thread) | 44236 |
| Cache read tokens | 10017328 |
| Cache write tokens | 265572 |
| Cache write tokens, main thread (5m / 1h) | 0 / 265572 |
| Cache hit ratio | 0.9742 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 114 | 10283014 | 562 | 10017328 | 265572 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 85112 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 77 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.01 |
