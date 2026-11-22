# Run analytics — feat_graphscene_static_checker

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 1h29m |
| Wall | 1h28m |
| Session wall, summed over sessions | 1h30m |
| Active | 1h26m |
| Host-suspended | 0.0s |
| Idle | 2m 34s |
| Cost | $28.42 |
| Input tokens (uncached) | 858 |
| Total input tokens (incl. cache) | 55976417 |
| Output tokens | 267629 |
| Thinking tokens (main thread) | 50318 |
| Cache read tokens | 54059713 |
| Cache write tokens | 1915846 |
| Cache write tokens, main thread (5m / 1h) | 0 / 891937 |
| Cache hit ratio | 0.9658 |
| Requests | 414 |
| Request latency p50 / p90 / p99 / max | 2.8s / 8.9s / 44.5s / 2m 34s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 13 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 2 graphscene — 5m 12s (session 5) |
| Rate-limit peak | seven_day 0.46 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 9m 38s | 7m 03s | 2m 34s | 9m 41s | $3.94 |
| 3 | 2-architecture_review | 1m 27s | 1m 27s | 0.0s | 1m 30s | $1.26 |
| 4 | 3-plan_review | 3m 43s | 3m 43s | 0.0s | 3m 46s | $2.86 |

## Network refusals

5 of 5 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No possible network attempt in 1 round logs.

## Gate rounds

Wait is the orchestrator's wait on `run-test-suite.sh --wait <label>`, summed over every polling row whose command ends in that label; — when none matches, as for a label waited on fewer than three times in a session (no polling row is written for it) or a command cut at 160 characters.

A phase's test-file total sums each file's own seconds, so it exceeds the gate's wall time when files run in parallel.

### Round task_round_1 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | 38m 06s |
| Gate rows | 34 (complete) |
| Test files — full | 223 files, 18521.5 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 1 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 3g | ok | 1 s |
| full | 3h | ok | 1 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2341 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 18 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 17 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 4 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 223)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1141.6 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 862.3 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 660.9 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 650.4 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 646.7 | 17 | 0 |
| test/remote-run.test.mjs | pass | 603.5 | 130 | 0 |
| test/doctor.test.mjs | pass | 600.6 | 1 | 0 |
| test/remote-control.test.mjs | pass | 553.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 533.2 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 528.2 | 21 | 0 |

## Session 1 — 2026-11-22T07:13:33.069Z → 2026-11-22T07:14:38.513Z

Session id: `65ea9553-219c-411d-b44f-c403f4d6abf5`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 05s | 1m 07s | 58.7s | 0.0s | 0.0s | 1m 05s | 4.9s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 2.3s | 2.8s | 5.1s | 5.1s | 0 |
| devscene:prompt-injection-reviewer | 1 | 2.4s | 2.4s | 2.4s | 2.4s | 0 |
| orchestrator | 16 | 2.3s | 2.8s | 5.1s | 5.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 4.9s | 4.9s |
| Bash | orchestrator | 10 | 8.9s | 6.2s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.7s | 0.4s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T07:14:27.135Z | 6.2s | 603 | false | false |
| Bash | orchestrator | 2026-11-22T07:13:36.347Z | 0.4s | 2210 | true | false |
| Read | orchestrator | 2026-11-22T07:13:36.676Z | 0.4s | 59813 | false | false |
| Bash | orchestrator | 2026-11-22T07:14:02.046Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T07:13:40.674Z | 0.3s | 656 | false | false |
| Bash | orchestrator | 2026-11-22T07:13:58.974Z | 0.3s | 157 | false | false |
| Bash | orchestrator | 2026-11-22T07:13:43.464Z | 0.3s | 158 | false | false |
| Read | orchestrator | 2026-11-22T07:14:13.431Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-22T07:14:05.796Z | 0.2s | 488 | false | false |
| Bash | orchestrator | 2026-11-22T07:14:16.221Z | 0.2s | 166 | true | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 4.9s | 1 | 281 | 4 | 30825 | 11193 | 19628 | 0.0751 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.06 |
| Cost — claude-opus-5-5 | $1.06 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 1220477 |
| Output tokens | 4813 |
| Thinking tokens (main thread) | 400 |
| Cache read tokens | 1120872 |
| Cache write tokens | 99567 |
| Cache write tokens, main thread (5m / 1h) | 0 / 79939 |
| Cache hit ratio | 0.9184 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 1189652 | 190 | 1109679 | 79939 |
| sub-agents | 4 | 30825 | 281 | 11193 | 19628 |
| remainder | 0 | 0 | 4342 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 20 |
| Time to first token | 2.4s |
| Rate-limit peak | seven_day 0.45 |

## Session 2 — 2026-11-22T07:14:42.595Z → 2026-11-22T07:24:21.072Z

Session id: `22ea4372-c4c4-4399-9ef6-b00fe66ed10a`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 9m 38s | 9m 41s | 9m 35s | 0.0s | 2m 34s | 7m 03s | — | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-22T07:17:45.959Z | 2m 34s | orchestrator | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 31 | 3.0s | 24.5s | 2m 34s | 2m 34s | 1 |
| orchestrator | 31 | 3.0s | 24.5s | 2m 34s | 2m 34s | 1 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 15 | 5.9s | 1.1s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 30 | 1.1s | 0.2s |
| Write | orchestrator | 7 | 0.3s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T07:17:27.909Z | 1.1s | 1300 | false | false |
| Bash | orchestrator | 2026-11-22T07:17:07.325Z | 0.9s | 2058 | false | false |
| Bash | orchestrator | 2026-11-22T07:14:42.600Z | 0.3s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T07:17:17.798Z | 0.3s | 2403 | false | false |
| Bash | orchestrator | 2026-11-22T07:14:55.940Z | 0.3s | 2794 | false | false |
| Bash | orchestrator | 2026-11-22T07:17:45.623Z | 0.3s | 117 | false | false |
| Bash | orchestrator | 2026-11-22T07:16:52.760Z | 0.3s | 4167 | false | false |
| Bash | orchestrator | 2026-11-22T07:15:21.215Z | 0.3s | 3145 | false | false |
| Bash | orchestrator | 2026-11-22T07:17:23.933Z | 0.2s | 2663 | false | false |
| Bash | orchestrator | 2026-11-22T07:20:21.482Z | 0.2s | 42 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.94 |
| Cost — claude-opus-5-5 | $3.94 |
| Input tokens (uncached) | 62 |
| Total input tokens (incl. cache) | 4845061 |
| Output tokens | 59780 |
| Thinking tokens (main thread) | 30720 |
| Cache read tokens | 4617694 |
| Cache write tokens | 227305 |
| Cache write tokens, main thread (5m / 1h) | 0 / 227305 |
| Cache hit ratio | 0.9531 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 62 | 4845061 | 283 | 4617694 | 227305 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 59497 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 56 |
| Time to first token | 2.5s |
| Rate-limit peak | seven_day 0.45 |

## Session 3 — 2026-11-22T07:24:26.149Z → 2026-11-22T07:25:53.817Z

Session id: `8d212cfb-5b78-4384-a96a-727c21cc82fe`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 27s | 1m 30s | 1m 26s | 0.0s | 0.0s | 1m 27s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 2.9s | 8.3s | 15.9s | 15.9s | 0 |
| orchestrator | 14 | 2.9s | 8.3s | 15.9s | 15.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 3.2s | 0.4s |
| Read | orchestrator | 14 | 0.5s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T07:24:26.155Z | 0.4s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T07:24:58.005Z | 0.4s | 11459 | false | false |
| Bash | orchestrator | 2026-11-22T07:25:16.751Z | 0.4s | 3942 | false | false |
| Bash | orchestrator | 2026-11-22T07:25:21.783Z | 0.3s | 5548 | false | false |
| Bash | orchestrator | 2026-11-22T07:24:29.041Z | 0.3s | 6672 | true | false |
| Bash | orchestrator | 2026-11-22T07:24:32.098Z | 0.3s | 1527 | false | false |
| Bash | orchestrator | 2026-11-22T07:25:29.375Z | 0.3s | 2262 | false | false |
| Bash | orchestrator | 2026-11-22T07:24:49.524Z | 0.2s | 967 | false | false |
| Read | orchestrator | 2026-11-22T07:24:48.172Z | 0.2s | 59929 | false | false |
| Bash | orchestrator | 2026-11-22T07:25:36.710Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.26 |
| Cost — claude-opus-5-5 | $1.26 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 1059191 |
| Output tokens | 8207 |
| Thinking tokens (main thread) | 3305 |
| Cache read tokens | 945601 |
| Cache write tokens | 113562 |
| Cache write tokens, main thread (5m / 1h) | 0 / 113562 |
| Cache hit ratio | 0.8928 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 1059191 | 127 | 945601 | 113562 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8080 | 0 | 0 |

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
| Time to first token | 2.4s |
| Rate-limit peak | seven_day 0.45 |

## Session 4 — 2026-11-22T07:24:26.048Z → 2026-11-22T07:28:09.971Z

Session id: `012e849f-7716-4639-b944-3a024e62ff3c`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 43s | 3m 46s | 3m 41s | 0.0s | 0.0s | 3m 43s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 27 | 3.1s | 27.0s | 32.4s | 32.4s | 0 |
| orchestrator | 27 | 3.1s | 27.0s | 32.4s | 32.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 16 | 4.5s | 0.4s |
| Read | orchestrator | 33 | 1.1s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T07:24:26.051Z | 0.4s | 58 | false | false |
| Bash | orchestrator | 2026-11-22T07:26:25.515Z | 0.4s | 5145 | false | false |
| Bash | orchestrator | 2026-11-22T07:26:19.158Z | 0.3s | 5923 | false | false |
| Bash | orchestrator | 2026-11-22T07:24:30.139Z | 0.3s | 23094 | false | false |
| Read | orchestrator | 2026-11-22T07:24:40.416Z | 0.2s | 59929 | false | false |
| Bash | orchestrator | 2026-11-22T07:24:55.107Z | 0.2s | 5535 | false | false |
| Bash | orchestrator | 2026-11-22T07:27:12.893Z | 0.2s | 3592 | false | false |
| Bash | orchestrator | 2026-11-22T07:27:16.637Z | 0.2s | 7675 | false | false |
| Bash | orchestrator | 2026-11-22T07:26:15.168Z | 0.2s | 8043 | false | false |
| Bash | orchestrator | 2026-11-22T07:26:39.283Z | 0.2s | 649 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.86 |
| Cost — claude-opus-5-5 | $2.86 |
| Input tokens (uncached) | 54 |
| Total input tokens (incl. cache) | 4005451 |
| Output tokens | 20911 |
| Thinking tokens (main thread) | 12920 |
| Cache read tokens | 3795294 |
| Cache write tokens | 210103 |
| Cache write tokens, main thread (5m / 1h) | 0 / 210103 |
| Cache hit ratio | 0.9475 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 54 | 4005451 | 295 | 3795294 | 210103 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 20616 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 51 |
| Time to first token | 2.3s |
| Rate-limit peak | seven_day 0.45 |

## Session 5 — 2026-11-22T07:28:44.805Z → 2026-11-22T08:43:10.059Z

Session id: `0efcad24-e319-45fb-8fd4-2bf5ecc14bd1`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h14m | 1h14m | 31m 15s | 0.0s | 0.0s | 1h14m | 26m 00s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 325 | 2.8s | 7.8s | 34.5s | 1m 37s | 0 |
| devscene:architecture-reviewer | 9 | 3.2s | 11.9s | 11.9s | 11.9s | 0 |
| devscene:branch-reviewer | 36 | 3.8s | 14.9s | 19.0s | 19.0s | 0 |
| devscene:layer-implementer | 111 | 2.8s | 7.5s | 50.1s | 1m 37s | 0 |
| devscene:review-plan-reviewer | 7 | 2.8s | 6.1s | 6.1s | 6.1s | 0 |
| devscene:skeptic-reviewer | 28 | 3.5s | 16.9s | 26.2s | 26.2s | 0 |
| devscene:statistics-plan-writer | 4 | 3.3s | 17.4s | 17.4s | 17.4s | 0 |
| orchestrator | 130 | 2.7s | 4.4s | 11.8s | 15.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 12 | 26m 00s | 5m 12s |
| Bash | devscene:architecture-reviewer | 8 | 2.3s | 0.3s |
| Bash | devscene:branch-reviewer | 33 | 13.4s | 1.6s |
| Bash | devscene:layer-implementer | 88 | 3m 09s | 16.9s |
| Bash | devscene:review-plan-reviewer | 6 | 2.0s | 0.3s |
| Bash | devscene:skeptic-reviewer | 24 | 7.1s | 0.8s |
| Bash | devscene:statistics-plan-writer | 3 | 0.8s | 0.4s |
| Bash | orchestrator | 105 | 40m 26s | 1m 05s |
| Edit | devscene:layer-implementer | 49 | 2.1s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Read | devscene:architecture-reviewer | 9 | 0.5s | 0.2s |
| Read | devscene:branch-reviewer | 10 | 0.5s | 0.2s |
| Read | devscene:layer-implementer | 39 | 1.4s | 0.2s |
| Read | devscene:review-plan-reviewer | 10 | 0.3s | 0.2s |
| Read | devscene:skeptic-reviewer | 4 | 0.1s | 0.0s |
| Read | devscene:statistics-plan-writer | 4 | 0.0s | 0.0s |
| Read | orchestrator | 22 | 2.4s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 5 | 0.2s | 0.0s |
| Write | devscene:layer-implementer | 12 | 0.5s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T08:32:46.286Z | 1m 05s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:14:25.693Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:02:30.133Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:04:40.564Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:07:55.105Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:11:09.873Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:08:59.844Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:23:07.165Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:03:35.363Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T08:28:29.980Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/engine/test_references.py | 3 | 3.6s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py | 3 | 3.7s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_layers.py | 5 | 24.4s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 9 | 1m 26s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 7 | 1.6s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_static_checker_story_plan.md  | 6 | 38.0s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 38 | 38m 06s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 11 | 3.0s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 2m 59s | 21 | 16946 | 44 | 1454308 | 1375454 | 78810 | 0.0403 |
| devscene:layer-implementer | Implement Task 2 graphscene | 5m 12s | 17 | 34345 | 36 | 1230700 | 1152322 | 78342 | 0.0699 |
| devscene:layer-implementer | Implement Task 3 graphscene | 2m 25s | 19 | 14023 | 40 | 1112576 | 1053195 | 59341 | 0.0327 |
| devscene:layer-implementer | Implement Task 4 graphscene | 1m 22s | 13 | 7293 | 28 | 626159 | 586780 | 39351 | 0.0185 |
| devscene:layer-implementer | Implement Task 5 graphscene | 1m 04s | 13 | 4562 | 28 | 581567 | 547653 | 33886 | 0.0144 |
| devscene:layer-implementer | Implement Task 6 general | 1m 41s | 17 | 7801 | 36 | 1541589 | 1446215 | 95338 | 0.0228 |
| devscene:architecture-reviewer | Architecture review of branch | 1m 01s | 9 | 5231 | 20 | 861252 | 732903 | 128329 | 0.0139 |
| devscene:branch-reviewer | End-of-branch code review | 4m 19s | 36 | 22030 | 74 | 5386442 | 5193734 | 192634 | 0.058 |
| devscene:review-plan-reviewer | Meta-review code review | 41.4s | 7 | 3692 | 16 | 414528 | 330590 | 83922 | 0.0093 |
| devscene:layer-implementer | Fix code-review finding 1 | 57.9s | 11 | 3784 | 24 | 720115 | 653837 | 66254 | 0.013 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 3m 39s | 28 | 20064 | 58 | 2328613 | 2217921 | 110634 | 0.0491 |
| devscene:statistics-plan-writer | Write branch statistics | 34.8s | 4 | 4030 | 10 | 159142 | 121692 | 37440 | 0.0078 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $19.31 |
| Cost — claude-opus-5-5 | $19.31 |
| Input tokens (uncached) | 676 |
| Total input tokens (incl. cache) | 44846237 |
| Output tokens | 173918 |
| Thinking tokens (main thread) | 2973 |
| Cache read tokens | 43580252 |
| Cache write tokens | 1265309 |
| Cache write tokens, main thread (5m / 1h) | 0 / 261028 |
| Cache hit ratio | 0.9718 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 262 | 28429246 | 3091 | 28167956 | 261028 |
| sub-agents | 414 | 16416991 | 143801 | 15412296 | 1004281 |
| remainder | 0 | 0 | 27026 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 11 |
| Sub-agents spawned / failed / killed | 12 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 154 |
| Time to first token | 2.1s |
| Rate-limit peak | seven_day 0.46 |
