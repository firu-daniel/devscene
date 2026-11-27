# Run analytics — feat_planning_driver_python_cutover

## Whole run

| Measure | Value |
|---|---|
| Sessions | 14 (0 incomplete) |
| Engine / planning node sessions | 2 / 12 |
| Span | 4h19m |
| Wall | 4h18m |
| Session wall, summed over sessions | 4h25m |
| Active | 3h29m |
| Host-suspended | 0.0s |
| Idle | 48m 56s |
| Cost | $104.21 |
| Input tokens (uncached) | 3398 |
| Total input tokens (incl. cache) | 229584069 |
| Output tokens | 1092711 |
| Thinking tokens (main thread) | 127086 |
| Cache read tokens | 223376838 |
| Cache write tokens | 6203833 |
| Cache write tokens, main thread (5m / 1h) | 0 / 2215515 |
| Cache hit ratio | 0.973 |
| Requests | 1657 |
| Request latency p50 / p90 / p99 / max | 1.9s / 8.3s / 33.4s / 1m 24s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 75 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 19 (flow-host) — 26m 22s (session 14) |
| Rate-limit peak | seven_day 0.33 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 17m 00s | 17m 00s | 0.0s | 17m 00s | $8.75 |
| 3 | 2-architecture_review | 3m 18s | 3m 18s | 0.0s | 3m 18s | $2.66 |
| 4 | 3-plan_review | 4m 06s | 4m 06s | 0.0s | 4m 07s | $3.49 |
| 5 | 4-plan_writer | 5m 54s | 5m 54s | 0.0s | 5m 55s | $2.49 |
| 6 | 5-architecture_review | 2m 56s | 2m 56s | 0.0s | 2m 57s | $2.70 |
| 7 | 6-plan_review | 6m 41s | 6m 41s | 0.0s | 6m 41s | $5.74 |
| 8 | 7-plan_writer | 1m 09s | 1m 09s | 0.0s | 1m 10s | $0.56 |
| 9 | 9-plan_review | 1m 02s | 1m 02s | 0.0s | 1m 03s | $0.80 |
| 10 | 8-architecture_review | 1m 10s | 1m 10s | 0.0s | 1m 11s | $1.02 |
| 11 | 10-plan_writer | 40.2s | 40.2s | 0.0s | 41.1s | $0.35 |
| 12 | 11-architecture_review | 37.7s | 37.7s | 0.0s | 38.5s | $0.81 |
| 13 | 12-plan_review | 56.6s | 56.6s | 0.0s | 57.3s | $0.66 |

## Network refusals

14 of 14 sessions scanned.

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
| Wait (every run of task_round_1) | 48m 49s |
| Gate rows | 32 (complete) |
| Test files — full | 227 files, 16768.9 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 1 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 1 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 1 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 4 | ok | 2146 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 19 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 5 s |
| full | 13h | ok | 1 s |
| full | 13i | ok | 0 s |
| full | 13j | ok | 816 s |
| full | 14a | ok | 6 s |
| full | 14c | ok | 6 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 227)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/watcher-review-drop-payloads.test.mjs | pass | 847.4 | 21 | 0 |
| test/remote-run.test.mjs | pass | 728.0 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 677.1 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 663.9 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 633.4 | 17 | 0 |
| test/remote-control.test.mjs | pass | 628.1 | 83 | 0 |
| test/doctor.test.mjs | pass | 591.1 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 575.4 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 554.9 | 21 | 0 |
| test/watcher-stall-reset-payloads.test.mjs | pass | 508.4 | 18 | 0 |

## Session 1 — 2026-11-27T07:45:59.644Z → 2026-11-27T07:46:51.205Z

Session id: `e5b74d1f-52b9-4c71-b438-90815a399d8b`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 51.5s | 52.5s | 45.1s | 0.0s | 0.0s | 51.5s | 2.9s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 0.9s | 1.8s | 4.6s | 4.6s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.2s | 1.2s | 1.2s | 1.2s | 0 |
| orchestrator | 17 | 0.9s | 1.8s | 4.6s | 4.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 2.9s | 2.9s |
| Bash | orchestrator | 12 | 7.0s | 5.1s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.5s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T07:46:41.413Z | 5.1s | 623 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:01.613Z | 0.3s | 2036 | false | false |
| Read | orchestrator | 2026-11-27T07:46:06.135Z | 0.2s | 59813 | false | false |
| Read | orchestrator | 2026-11-27T07:46:31.752Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:12.509Z | 0.2s | 163 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:30.215Z | 0.2s | 8792 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:28.356Z | 0.1s | 3835 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:23.969Z | 0.1s | 162 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:09.210Z | 0.1s | 171 | true | false |
| Bash | orchestrator | 2026-11-27T07:46:33.373Z | 0.1s | 53 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 2.9s | 1 | 296 | 4 | 31567 | 11222 | 20341 | 0.0571 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.13 |
| Cost — claude-opus-5-5 | $1.13 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 1269426 |
| Output tokens | 5476 |
| Thinking tokens (main thread) | 434 |
| Cache read tokens | 1163601 |
| Cache write tokens | 105787 |
| Cache write tokens, main thread (5m / 1h) | 0 / 85446 |
| Cache hit ratio | 0.9166 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 1237859 | 299 | 1152379 | 85446 |
| sub-agents | 4 | 31567 | 296 | 11222 | 20341 |
| remainder | 0 | 0 | 4881 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.28 |

## Session 2 — 2026-11-27T07:46:53.381Z → 2026-11-27T08:03:53.576Z

Session id: `76d7ebaf-43bb-4498-ab2f-ee6bbd3b3c36`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 17m 00s | 17m 00s | 16m 51s | 0.0s | 0.0s | 17m 00s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 73 | 2.1s | 17.2s | 44.9s | 44.9s | 0 |
| orchestrator | 73 | 2.1s | 17.2s | 44.9s | 44.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 46 | 9.5s | 0.7s |
| Edit | orchestrator | 10 | 0.3s | 0.0s |
| Read | orchestrator | 38 | 1.3s | 0.3s |
| Write | orchestrator | 26 | 1.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T07:54:04.719Z | 0.7s | 4589 | false | false |
| Bash | orchestrator | 2026-11-27T07:48:27.549Z | 0.5s | 2024 | false | false |
| Bash | orchestrator | 2026-11-27T07:53:53.889Z | 0.3s | 964 | false | false |
| Read | orchestrator | 2026-11-27T07:46:56.540Z | 0.3s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T07:49:59.590Z | 0.3s | 505 | false | false |
| Bash | orchestrator | 2026-11-27T07:51:11.592Z | 0.3s | 6786 | false | false |
| Bash | orchestrator | 2026-11-27T07:48:09.646Z | 0.2s | 1673 | false | false |
| Bash | orchestrator | 2026-11-27T07:46:53.827Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T07:48:31.822Z | 0.2s | 10684 | false | false |
| Bash | orchestrator | 2026-11-27T07:49:51.862Z | 0.2s | 2944 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $8.75 |
| Cost — claude-opus-5-5 | $8.75 |
| Input tokens (uncached) | 146 |
| Total input tokens (incl. cache) | 17078792 |
| Output tokens | 119277 |
| Thinking tokens (main thread) | 44657 |
| Cache read tokens | 16700320 |
| Cache write tokens | 378326 |
| Cache write tokens, main thread (5m / 1h) | 0 / 378326 |
| Cache hit ratio | 0.9778 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 146 | 17078792 | 749 | 16700320 | 378326 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 118528 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 3 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 121 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.28 |

## Session 3 — 2026-11-27T08:03:55.659Z → 2026-11-27T08:07:13.872Z

Session id: `683c3b18-ec53-4dc5-a008-771082625107`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 18s | 3m 18s | 3m 17s | 0.0s | 0.0s | 3m 18s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 21 | 3.1s | 25.4s | 43.4s | 43.4s | 0 |
| orchestrator | 21 | 3.1s | 25.4s | 43.4s | 43.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 12 | 2.0s | 0.2s |
| Read | orchestrator | 38 | 1.3s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-27T08:04:05.145Z | 0.3s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:03:56.198Z | 0.2s | 63 | false | false |
| Read | orchestrator | 2026-11-27T08:04:07.537Z | 0.2s | 30738 | false | false |
| Read | orchestrator | 2026-11-27T08:04:08.097Z | 0.2s | 37415 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:47.166Z | 0.1s | 2529 | false | false |
| Bash | orchestrator | 2026-11-27T08:04:44.810Z | 0.1s | 2752 | false | false |
| Bash | orchestrator | 2026-11-27T08:04:40.192Z | 0.1s | 10336 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:16.058Z | 0.1s | 1404 | false | false |
| Bash | orchestrator | 2026-11-27T08:03:57.048Z | 0.1s | 8947 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:09.853Z | 0.1s | 3452 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.66 |
| Cost — claude-opus-5-5 | $2.66 |
| Input tokens (uncached) | 42 |
| Total input tokens (incl. cache) | 2842360 |
| Output tokens | 22336 |
| Thinking tokens (main thread) | 9920 |
| Cache read tokens | 2632074 |
| Cache write tokens | 210244 |
| Cache write tokens, main thread (5m / 1h) | 0 / 210244 |
| Cache hit ratio | 0.926 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 42 | 2842360 | 989 | 2632074 | 210244 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 21347 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 52 |
| Time to first token | 0.6s |
| Rate-limit peak | seven_day 0.28 |

## Session 4 — 2026-11-27T08:03:55.969Z → 2026-11-27T08:08:02.590Z

Session id: `4c2c09e5-17b5-4b48-bc9b-479f5f4b18d1`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 06s | 4m 07s | 4m 00s | 0.0s | 0.0s | 4m 06s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 47 | 2.0s | 7.1s | 28.5s | 28.5s | 0 |
| orchestrator | 47 | 2.0s | 7.1s | 28.5s | 28.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 33 | 6.4s | 0.4s |
| Read | orchestrator | 40 | 0.8s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:05:23.409Z | 0.4s | 1369 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:36.978Z | 0.3s | 960 | false | false |
| Bash | orchestrator | 2026-11-27T08:07:26.933Z | 0.3s | 658 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:51.387Z | 0.3s | 5253 | false | false |
| Bash | orchestrator | 2026-11-27T08:03:56.336Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:05:14.578Z | 0.2s | 1115 | false | false |
| Bash | orchestrator | 2026-11-27T08:04:02.180Z | 0.2s | 4658 | false | false |
| Read | orchestrator | 2026-11-27T08:06:37.815Z | 0.2s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:06:54.910Z | 0.2s | 1850 | false | false |
| Bash | orchestrator | 2026-11-27T08:07:02.956Z | 0.2s | 1723 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.49 |
| Cost — claude-opus-5-5 | $3.49 |
| Input tokens (uncached) | 94 |
| Total input tokens (incl. cache) | 6202732 |
| Output tokens | 26770 |
| Thinking tokens (main thread) | 12914 |
| Cache read tokens | 5983111 |
| Cache write tokens | 219527 |
| Cache write tokens, main thread (5m / 1h) | 0 / 219527 |
| Cache hit ratio | 0.9646 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 94 | 6202732 | 1174 | 5983111 | 219527 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25596 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 3 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 75 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.28 |

## Session 5 — 2026-11-27T08:08:10.622Z → 2026-11-27T08:14:05.111Z

Session id: `620093a8-8fdc-45eb-858f-5300af7b3266`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 54s | 5m 55s | 5m 51s | 0.0s | 0.0s | 5m 54s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 39 | 1.5s | 11.4s | 20.1s | 20.1s | 0 |
| orchestrator | 39 | 1.5s | 11.4s | 20.1s | 20.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 19 | 3.5s | 0.3s |
| Edit | orchestrator | 36 | 1.3s | 0.0s |
| Read | orchestrator | 19 | 0.3s | 0.0s |
| Write | orchestrator | 3 | 0.1s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:10:01.680Z | 0.3s | 248 | false | false |
| Bash | orchestrator | 2026-11-27T08:13:31.946Z | 0.3s | 967 | false | false |
| Bash | orchestrator | 2026-11-27T08:08:11.182Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:09:51.768Z | 0.2s | 2672 | false | false |
| Bash | orchestrator | 2026-11-27T08:10:05.417Z | 0.1s | 1121 | false | false |
| Bash | orchestrator | 2026-11-27T08:08:45.380Z | 0.1s | 1636 | false | false |
| Bash | orchestrator | 2026-11-27T08:08:41.797Z | 0.1s | 1043 | false | false |
| Bash | orchestrator | 2026-11-27T08:08:18.538Z | 0.1s | 2422 | false | false |
| Bash | orchestrator | 2026-11-27T08:08:42.740Z | 0.1s | 1169 | false | false |
| Bash | orchestrator | 2026-11-27T08:09:53.998Z | 0.1s | 152 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.49 |
| Cost — claude-opus-5-5 | $2.49 |
| Input tokens (uncached) | 78 |
| Total input tokens (incl. cache) | 3475414 |
| Output tokens | 45170 |
| Thinking tokens (main thread) | 11390 |
| Cache read tokens | 3360632 |
| Cache write tokens | 114704 |
| Cache write tokens, main thread (5m / 1h) | 0 / 114704 |
| Cache hit ratio | 0.967 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 78 | 3475414 | 438 | 3360632 | 114704 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 44732 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 78 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.29 |

## Session 6 — 2026-11-27T08:14:07.909Z → 2026-11-27T08:17:04.607Z

Session id: `09ce8c4f-28d2-49e1-b856-fa004eb03b67`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 56s | 2m 57s | 2m 55s | 0.0s | 0.0s | 2m 56s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 22 | 1.4s | 10.2s | 1m 00s | 1m 00s | 0 |
| orchestrator | 22 | 1.4s | 10.2s | 1m 00s | 1m 00s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 12 | 2.1s | 0.2s |
| Read | orchestrator | 40 | 1.3s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-27T08:14:14.680Z | 0.3s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:14:08.344Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:15:51.887Z | 0.2s | 10241 | false | false |
| Read | orchestrator | 2026-11-27T08:14:16.327Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-27T08:16:07.858Z | 0.2s | 3196 | false | false |
| Read | orchestrator | 2026-11-27T08:14:16.828Z | 0.2s | 37415 | false | false |
| Bash | orchestrator | 2026-11-27T08:15:55.590Z | 0.2s | 2841 | false | false |
| Bash | orchestrator | 2026-11-27T08:15:59.332Z | 0.1s | 6391 | false | false |
| Bash | orchestrator | 2026-11-27T08:16:24.607Z | 0.1s | 2506 | false | false |
| Bash | orchestrator | 2026-11-27T08:14:10.912Z | 0.1s | 11467 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.70 |
| Cost — claude-opus-5-5 | $2.70 |
| Input tokens (uncached) | 44 |
| Total input tokens (incl. cache) | 3329292 |
| Output tokens | 20353 |
| Thinking tokens (main thread) | 10911 |
| Cache read tokens | 3120408 |
| Cache write tokens | 208840 |
| Cache write tokens, main thread (5m / 1h) | 0 / 208840 |
| Cache hit ratio | 0.9373 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 44 | 3329292 | 1015 | 3120408 | 208840 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 19338 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 54 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.29 |

## Session 7 — 2026-11-27T08:14:07.821Z → 2026-11-27T08:20:49.079Z

Session id: `e86e668a-c03b-4690-945c-8d907b58f9ea`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 6m 41s | 6m 41s | 6m 33s | 0.0s | 0.0s | 6m 41s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 62 | 2.3s | 11.8s | 45.0s | 45.0s | 0 |
| orchestrator | 62 | 2.3s | 11.8s | 45.0s | 45.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 41 | 8.1s | 0.5s |
| Read | orchestrator | 50 | 1.4s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:15:34.078Z | 0.5s | 2150 | false | false |
| Bash | orchestrator | 2026-11-27T08:17:25.371Z | 0.3s | 972 | false | false |
| Bash | orchestrator | 2026-11-27T08:14:08.220Z | 0.3s | 63 | false | false |
| Read | orchestrator | 2026-11-27T08:14:32.731Z | 0.3s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:17:56.568Z | 0.2s | 4967 | false | false |
| Bash | orchestrator | 2026-11-27T08:17:16.581Z | 0.2s | 1545 | false | false |
| Bash | orchestrator | 2026-11-27T08:15:27.325Z | 0.2s | 3816 | false | false |
| Bash | orchestrator | 2026-11-27T08:14:13.813Z | 0.2s | 3921 | false | false |
| Read | orchestrator | 2026-11-27T08:14:36.061Z | 0.2s | 37415 | false | false |
| Bash | orchestrator | 2026-11-27T08:17:33.530Z | 0.2s | 560 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $5.74 |
| Cost — claude-opus-5-5 | $5.74 |
| Input tokens (uncached) | 124 |
| Total input tokens (incl. cache) | 13070235 |
| Output tokens | 43370 |
| Thinking tokens (main thread) | 24725 |
| Cache read tokens | 12780071 |
| Cache write tokens | 290040 |
| Cache write tokens, main thread (5m / 1h) | 0 / 290040 |
| Cache hit ratio | 0.9778 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 124 | 13070235 | 1285 | 12780071 | 290040 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 42085 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 93 |
| Time to first token | 0.6s |
| Rate-limit peak | seven_day 0.29 |

## Session 8 — 2026-11-27T08:20:58.581Z → 2026-11-27T08:22:08.148Z

Session id: `1ca609a3-ba31-4973-9a50-0d443a244121`

Planning node: `7-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 09s | 1m 10s | 1m 09s | 0.0s | 0.0s | 1m 09s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 1.3s | 4.5s | 8.0s | 8.0s | 0 |
| orchestrator | 14 | 1.3s | 4.5s | 8.0s | 8.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 1.1s | 0.3s |
| Edit | orchestrator | 9 | 0.4s | 0.1s |
| Read | orchestrator | 6 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:20:59.128Z | 0.3s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:21:51.494Z | 0.1s | 1126 | false | false |
| Bash | orchestrator | 2026-11-27T08:21:07.029Z | 0.1s | 885 | false | false |
| Bash | orchestrator | 2026-11-27T08:21:54.119Z | 0.1s | 903 | false | false |
| Bash | orchestrator | 2026-11-27T08:21:09.818Z | 0.1s | 492 | false | false |
| Edit | orchestrator | 2026-11-27T08:21:49.230Z | 0.1s | 259 | false | false |
| Bash | orchestrator | 2026-11-27T08:21:11.442Z | 0.1s | 221 | false | false |
| Write | orchestrator | 2026-11-27T08:21:47.355Z | 0.0s | 249 | false | false |
| Edit | orchestrator | 2026-11-27T08:21:19.442Z | 0.0s | 178 | false | false |
| Edit | orchestrator | 2026-11-27T08:21:17.779Z | 0.0s | 246 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.56 |
| Cost — claude-opus-5-5 | $0.56 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 575974 |
| Output tokens | 8630 |
| Thinking tokens (main thread) | 1315 |
| Cache read tokens | 541444 |
| Cache write tokens | 34502 |
| Cache write tokens, main thread (5m / 1h) | 0 / 34502 |
| Cache hit ratio | 0.94 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 575974 | 167 | 541444 | 34502 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8463 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.29 |

## Session 9 — 2026-11-27T08:22:10.606Z → 2026-11-27T08:23:13.474Z

Session id: `c09a97b2-758b-4a39-82f9-dfc472ba9c87`

Planning node: `9-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 02s | 1m 03s | 1m 01s | 0.0s | 0.0s | 1m 02s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.8s | 5.7s | 7.3s | 7.3s | 0 |
| orchestrator | 16 | 1.8s | 5.7s | 7.3s | 7.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 2.2s | 0.4s |
| Read | orchestrator | 12 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:22:10.877Z | 0.4s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:51.031Z | 0.3s | 960 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:18.164Z | 0.2s | 722 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:35.163Z | 0.1s | 2093 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:13.005Z | 0.1s | 5483 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:20.177Z | 0.1s | 10041 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:42.423Z | 0.1s | 7678 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:03.949Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:56.754Z | 0.1s | 785 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:29.466Z | 0.1s | 221 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.80 |
| Cost — claude-opus-5-5 | $0.80 |
| Input tokens (uncached) | 32 |
| Total input tokens (incl. cache) | 790250 |
| Output tokens | 6791 |
| Thinking tokens (main thread) | 1879 |
| Cache read tokens | 725597 |
| Cache write tokens | 64621 |
| Cache write tokens, main thread (5m / 1h) | 0 / 64621 |
| Cache hit ratio | 0.9182 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 790250 | 863 | 725597 | 64621 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 5928 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 25 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.29 |

## Session 10 — 2026-11-27T08:22:10.590Z → 2026-11-27T08:23:21.313Z

Session id: `435064af-29e9-4e50-b775-8312c8cc4711`

Planning node: `8-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 10s | 1m 11s | 1m 10s | 0.0s | 0.0s | 1m 10s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 2.0s | 6.5s | 14.8s | 14.8s | 0 |
| orchestrator | 13 | 2.0s | 6.5s | 14.8s | 14.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 10 | 1.9s | 0.3s |
| Read | orchestrator | 11 | 0.4s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:22:11.009Z | 0.3s | 63 | false | false |
| Read | orchestrator | 2026-11-27T08:22:33.271Z | 0.3s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:31.171Z | 0.2s | 11570 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:12.157Z | 0.2s | 5591 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:18.801Z | 0.1s | 10277 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:38.836Z | 0.1s | 732 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:41.519Z | 0.1s | 213 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:35.425Z | 0.1s | 2589 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:49.267Z | 0.1s | 1510 | false | false |
| Bash | orchestrator | 2026-11-27T08:22:16.776Z | 0.1s | 40 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.02 |
| Cost — claude-opus-5-5 | $1.02 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 867521 |
| Output tokens | 8014 |
| Thinking tokens (main thread) | 2764 |
| Cache read tokens | 780103 |
| Cache write tokens | 87392 |
| Cache write tokens, main thread (5m / 1h) | 0 / 87392 |
| Cache hit ratio | 0.8992 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 867521 | 807 | 780103 | 87392 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7207 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.29 |

## Session 11 — 2026-11-27T08:23:29.374Z → 2026-11-27T08:24:09.589Z

Session id: `73b95157-4c08-4b12-bb95-70a519e830b0`

Planning node: `10-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 40.2s | 41.1s | 40.3s | 0.0s | 0.0s | 40.2s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 11 | 1.2s | 2.8s | 7.1s | 7.1s | 0 |
| orchestrator | 11 | 1.2s | 2.8s | 7.1s | 7.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 1.0s | 0.2s |
| Edit | orchestrator | 2 | 0.1s | 0.0s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:23:29.889Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:34.015Z | 0.1s | 4880 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:56.925Z | 0.1s | 1119 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:53.904Z | 0.1s | 370 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:41.299Z | 0.1s | 1781 | false | false |
| Bash | orchestrator | 2026-11-27T08:23:39.732Z | 0.0s | 727 | true | true |
| Edit | orchestrator | 2026-11-27T08:23:47.951Z | 0.0s | 179 | false | false |
| Edit | orchestrator | 2026-11-27T08:23:50.673Z | 0.0s | 179 | false | false |
| Read | orchestrator | 2026-11-27T08:23:30.534Z | 0.0s | 3083 | false | false |
| Write | orchestrator | 2026-11-27T08:23:52.314Z | 0.0s | 249 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.35 |
| Cost — claude-opus-5-5 | $0.35 |
| Input tokens (uncached) | 22 |
| Total input tokens (incl. cache) | 344277 |
| Output tokens | 5072 |
| Thinking tokens (main thread) | 327 |
| Cache read tokens | 321389 |
| Cache write tokens | 22866 |
| Cache write tokens, main thread (5m / 1h) | 0 / 22866 |
| Cache hit ratio | 0.9335 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 22 | 344277 | 188 | 321389 | 22866 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 4884 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 17 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.29 |

## Session 12 — 2026-11-27T08:24:11.801Z → 2026-11-27T08:24:49.578Z

Session id: `1efe1e64-acac-4ae0-a868-c9b7d2c73e45`

Planning node: `11-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 37.7s | 38.5s | 37.0s | 0.0s | 0.0s | 37.7s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 12 | 1.7s | 2.5s | 6.4s | 6.4s | 0 |
| orchestrator | 12 | 1.7s | 2.5s | 6.4s | 6.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 1.5s | 0.2s |
| Read | orchestrator | 9 | 0.4s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-27T08:24:28.327Z | 0.2s | 63482 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:12.225Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:24.996Z | 0.2s | 9277 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:40.371Z | 0.1s | 1536 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:14.179Z | 0.1s | 5522 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:21.189Z | 0.1s | 3727 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:19.313Z | 0.1s | 198 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:31.080Z | 0.1s | 1683 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:34.870Z | 0.1s | 166 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:30.180Z | 0.0s | 727 | true | true |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.81 |
| Cost — claude-opus-5-5 | $0.81 |
| Input tokens (uncached) | 24 |
| Total input tokens (incl. cache) | 664835 |
| Output tokens | 4087 |
| Thinking tokens (main thread) | 707 |
| Cache read tokens | 588354 |
| Cache write tokens | 76457 |
| Cache write tokens, main thread (5m / 1h) | 0 / 76457 |
| Cache hit ratio | 0.885 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 24 | 664835 | 813 | 588354 | 76457 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 3274 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 20 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.29 |

## Session 13 — 2026-11-27T08:24:11.785Z → 2026-11-27T08:25:08.461Z

Session id: `62e2d011-da8c-4df1-a4b6-c43ea8fafa98`

Planning node: `12-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 56.6s | 57.3s | 54.7s | 0.0s | 0.0s | 56.6s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 19 | 1.8s | 3.4s | 6.2s | 6.2s | 0 |
| orchestrator | 19 | 1.8s | 3.4s | 6.2s | 6.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 13 | 2.6s | 0.3s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-27T08:24:53.792Z | 0.3s | 960 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:12.160Z | 0.2s | 63 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:14.158Z | 0.2s | 6205 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:25.529Z | 0.2s | 6146 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:33.364Z | 0.1s | 1720 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:43.525Z | 0.1s | 1243 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:21.249Z | 0.1s | 3887 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:48.461Z | 0.1s | 82 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:19.096Z | 0.1s | 40 | false | false |
| Bash | orchestrator | 2026-11-27T08:24:29.330Z | 0.1s | 2031 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.66 |
| Cost — claude-opus-5-5 | $0.66 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 839031 |
| Output tokens | 6093 |
| Thinking tokens (main thread) | 1455 |
| Cache read tokens | 791574 |
| Cache write tokens | 47419 |
| Cache write tokens, main thread (5m / 1h) | 0 / 47419 |
| Cache hit ratio | 0.9434 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 38 | 839031 | 164 | 791574 | 47419 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 5929 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 22 |
| Time to first token | 0.6s |
| Rate-limit peak | seven_day 0.29 |

## Session 14 — 2026-11-27T08:25:38.212Z → 2026-11-27T12:05:09.272Z

Session id: `194ef29e-575d-4ae4-aa3a-e7dfc22eff35`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3h39m | 3h39m | 1h47m | 0.0s | 48m 56s | 2h50m | 2h36m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-27T09:21:37.230Z | 8m 10s | devscene:layer-implementer | tool_running |
| 2026-11-27T09:30:48.672Z | 4m 04s | devscene:layer-implementer | tool_running |
| 2026-11-27T09:35:25.978Z | 4m 07s | devscene:layer-implementer | tool_running |
| 2026-11-27T09:39:40.342Z | 4m 03s | devscene:layer-implementer | in_flight_request |
| 2026-11-27T09:49:14.266Z | 5m 05s | devscene:layer-implementer | tool_running |
| 2026-11-27T09:54:33.521Z | 5m 05s | devscene:layer-implementer | tool_running |
| 2026-11-27T10:00:02.937Z | 5m 05s | devscene:layer-implementer | tool_running |
| 2026-11-27T10:45:52.812Z | 8m 09s | devscene:layer-implementer | tool_running |
| 2026-11-27T10:54:02.084Z | 5m 05s | devscene:layer-implementer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 1290 | 1.9s | 8.0s | 31.6s | 1m 24s | 0 |
| devscene:architecture-reviewer | 38 | 3.0s | 15.9s | 19.8s | 19.8s | 0 |
| devscene:branch-reviewer | 87 | 3.7s | 14.5s | 24.8s | 24.8s | 0 |
| devscene:layer-implementer | 775 | 2.2s | 9.0s | 49.4s | 1m 24s | 0 |
| devscene:review-plan-reviewer | 53 | 2.4s | 8.0s | 23.9s | 23.9s | 0 |
| devscene:skeptic-reviewer | 75 | 2.5s | 10.9s | 29.1s | 29.1s | 0 |
| devscene:statistics-plan-writer | 6 | 2.0s | 19.7s | 19.7s | 19.7s | 0 |
| orchestrator | 256 | 1.1s | 1.8s | 7.5s | 9.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 40 | 2h36m | 26m 22s |
| Bash | devscene:architecture-reviewer | 26 | 4.6s | 0.4s |
| Bash | devscene:branch-reviewer | 74 | 14.9s | 1.4s |
| Bash | devscene:layer-implementer | 613 | 1h09m | 13m 14s |
| Bash | devscene:review-plan-reviewer | 45 | 7.6s | 0.3s |
| Bash | devscene:skeptic-reviewer | 56 | 10.0s | 0.5s |
| Bash | devscene:statistics-plan-writer | 8 | 1.2s | 0.1s |
| Bash | orchestrator | 304 | 54m 35s | 1m 03s |
| Edit | devscene:layer-implementer | 267 | 9.3s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Grep | devscene:layer-implementer | 1 | 0.0s | 0.0s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | devscene:architecture-reviewer | 21 | 0.2s | 0.0s |
| Read | devscene:branch-reviewer | 18 | 0.3s | 0.2s |
| Read | devscene:layer-implementer | 246 | 5.3s | 0.2s |
| Read | devscene:review-plan-reviewer | 35 | 0.7s | 0.3s |
| Read | devscene:skeptic-reviewer | 21 | 0.8s | 0.2s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 2.4s | 0.5s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 5 | 0.1s | 0.0s |
| Write | devscene:branch-reviewer | 7 | 0.2s | 0.0s |
| Write | devscene:layer-implementer | 28 | 1.2s | 0.0s |
| Write | devscene:review-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-27T10:45:52.812Z | 13m 14s | 441 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:21:37.230Z | 8m 10s | 10045 | true | false |
| Bash | devscene:layer-implementer | 2026-11-27T10:45:52.061Z | 8m 10s | 441 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:54:33.521Z | 5m 05s | 441 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:49:14.266Z | 5m 05s | 3716 | true | false |
| Bash | devscene:layer-implementer | 2026-11-27T10:00:02.937Z | 5m 05s | 441 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:35:25.978Z | 4m 07s | 1261 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:39:39.019Z | 4m 05s | 469 | false | false |
| Bash | devscene:layer-implementer | 2026-11-27T09:30:48.672Z | 4m 04s | 923 | false | false |
| Bash | orchestrator | 2026-11-27T11:14:13.549Z | 1m 03s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host lint | 10 | 4.1s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py | 10 | 9.8s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py tests/test_layers.py | 6 | 10.1s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_layers.py | 10 | 19.5s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_node_sessions.py | 4 | 3.2s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_driver_control.py | 4 | 28m 30s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_run.py | 3 | 3.9s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_exits.py | 6 | 5.2s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_records.py | 3 | 1.6s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host typecheck | 4 | 1.9s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 40 | 3m 10s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 32 | 4.8s |
| devscene:layer-implementer | grep -n '"typecheck"\\|"test"' devscene.config.json | 3 | 0.4s |
| devscene:layer-implementer | npm test --workspace cli -- test/agent-return-schemas.test.mjs | 5 | 47.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 3 | 9.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 3 | 7.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs | 4 | 8.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 5 | 47.4s |
| devscene:review-plan-reviewer | git rev-parse --show-toplevel | 3 | 0.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/architecture_branch_reviews/feat_planning_driver_p | 4 | 22.8s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_planning_driver_python_cutover_story_pla | 25 | 2m 26s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 49 | 48m 49s |
| orchestrator | cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 40 | 6.6s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE | 89 | 33.8s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (cli) | 2m 29s | 21 | 16622 | 44 | 1384448 | 1292164 | 92240 | 0.0114 |
| devscene:layer-implementer | Implement Task 2 (cli) | 3m 54s | 34 | 25831 | 70 | 2897044 | 2793781 | 103193 | 0.0178 |
| devscene:layer-implementer | Implement Task 3 (cli) | 51.3s | 12 | 5209 | 26 | 538099 | 497182 | 40891 | 0.0039 |
| devscene:layer-implementer | Implement Task 4 (cli) | 2m 53s | 17 | 11001 | 36 | 980207 | 911447 | 68724 | 0.0132 |
| devscene:layer-implementer | Implement Task 5 (cli) | 4m 21s | 28 | 27342 | 58 | 2541860 | 2427358 | 114444 | 0.0199 |
| devscene:layer-implementer | Implement Task 6 (cli) | 1m 02s | 14 | 5791 | 30 | 643846 | 597065 | 46751 | 0.0048 |
| devscene:layer-implementer | Implement Task 7 (plugin) | 45.9s | 11 | 4502 | 24 | 492941 | 448357 | 44560 | 0.0035 |
| devscene:layer-implementer | Implement Task 8 (graphscene) | 37.7s | 13 | 3384 | 28 | 556614 | 525922 | 30664 | 0.0029 |
| devscene:layer-implementer | Implement Task 9 (flow-host) | 2m 21s | 23 | 16939 | 48 | 1406275 | 1345545 | 60682 | 0.0107 |
| devscene:layer-implementer | Implement Task 10 (flow-host) | 2m 09s | 19 | 15924 | 40 | 1063844 | 1007616 | 56188 | 0.0099 |
| devscene:layer-implementer | Implement Task 11 (flow-host) | 2m 35s | 17 | 18525 | 36 | 977652 | 921631 | 55985 | 0.0118 |
| devscene:layer-implementer | Implement Task 12 (flow-host) | 1m 19s | 16 | 9139 | 34 | 779401 | 737847 | 41520 | 0.006 |
| devscene:layer-implementer | Implement Task 13 (flow-host) | 2m 41s | 26 | 18550 | 54 | 1726250 | 1651973 | 74223 | 0.0122 |
| devscene:layer-implementer | Implement Task 14 (flow-host) | 2m 46s | 27 | 17412 | 56 | 1789403 | 1722421 | 66926 | 0.0127 |
| devscene:layer-implementer | Implement Task 15 (flow-host) | 1m 31s | 17 | 10346 | 36 | 966963 | 913904 | 53023 | 0.007 |
| devscene:layer-implementer | Implement Task 16 (flow-host) | 4m 18s | 40 | 30203 | 82 | 4263710 | 4129244 | 134384 | 0.0197 |
| devscene:layer-implementer | Implement Task 17 (flow-host) | 7m 30s | 62 | 54458 | 126 | 8719096 | 8537100 | 181870 | 0.0342 |
| devscene:layer-implementer | Implement Task 18 (flow-host) | 2m 57s | 25 | 21087 | 52 | 2026075 | 1938512 | 87511 | 0.0135 |
| devscene:layer-implementer | Implement Task 19 (flow-host) | 26m 22s | 48 | 39774 | 98 | 5236308 | 4987801 | 248409 | 0.1201 |
| devscene:layer-implementer | Implement Task 20 (flow-host) | 20m 47s | 40 | 36760 | 82 | 4957109 | 4798394 | 158633 | 0.0947 |
| devscene:layer-implementer | Implement Task 21 (flow-host) | 1m 07s | 16 | 6648 | 34 | 898667 | 846602 | 52031 | 0.0052 |
| devscene:layer-implementer | Implement Task 22 (flow-host) | 1m 22s | 14 | 9332 | 30 | 699699 | 653015 | 46654 | 0.0063 |
| devscene:layer-implementer | Implement Task 23 (flow-host) | 3m 10s | 35 | 22452 | 72 | 3224287 | 3123891 | 100324 | 0.0144 |
| devscene:layer-implementer | Implement Task 24 (general) | 4m 40s | 36 | 31976 | 74 | 5098919 | 4924310 | 174535 | 0.0213 |
| devscene:layer-implementer | Implement Task 25 (general) | 5m 11s | 61 | 33968 | 124 | 7698062 | 7537771 | 160167 | 0.0237 |
| devscene:architecture-reviewer | Architecture review of branch | 4m 12s | 38 | 28490 | 78 | 5964139 | 5750661 | 213400 | 0.0192 |
| devscene:layer-implementer | Fix arch Finding 1 (general) | 44.4s | 11 | 4070 | 24 | 641487 | 580545 | 60918 | 0.0034 |
| devscene:layer-implementer | Fix arch Finding 4 (general) | 31.1s | 9 | 2817 | 20 | 460976 | 421611 | 39345 | 0.0024 |
| devscene:layer-implementer | Fix arch Finding 3 (flow-host) | 54.0s | 11 | 5803 | 24 | 558362 | 513223 | 45115 | 0.0041 |
| devscene:layer-implementer | Fix arch Finding 2 (flow-host) | 2m 12s | 29 | 14327 | 60 | 1716463 | 1659834 | 56569 | 0.01 |
| devscene:branch-reviewer | End-of-branch code review | 9m 08s | 87 | 58886 | 176 | 21754689 | 21391155 | 363358 | 0.0416 |
| devscene:review-plan-reviewer | Meta-review the code review | 2m 37s | 23 | 17152 | 48 | 2900833 | 2728864 | 171921 | 0.012 |
| devscene:layer-implementer | Fix code-review Finding 2 | 14m 16s | 13 | 6832 | 28 | 603802 | 505234 | 98540 | 0.065 |
| devscene:layer-implementer | Fix code-review Finding 1 | 42.6s | 12 | 4330 | 26 | 584194 | 545860 | 38308 | 0.0032 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 6m 02s | 71 | 38183 | 146 | 11418742 | 11171235 | 247361 | 0.0275 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 1m 01s | 14 | 6919 | 30 | 1293219 | 1163233 | 129956 | 0.0047 |
| devscene:skeptic-reviewer | Adjust skeptic review per meta | 11.3s | 4 | 1324 | 10 | 140571 | 123633 | 16928 | 0.0009 |
| devscene:review-plan-reviewer | Re-meta-review skeptic review | 1m 14s | 16 | 8107 | 34 | 1050455 | 972084 | 78337 | 0.0057 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 1m 38s | 18 | 11355 | 38 | 1095654 | 1026055 | 69561 | 0.0075 |
| devscene:statistics-plan-writer | Write branch statistics | 39.9s | 6 | 5147 | 14 | 264819 | 220977 | 43828 | 0.003 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $73.05 |
| Cost — claude-opus-5-5 | $73.05 |
| Input tokens (uncached) | 2662 |
| Total input tokens (incl. cache) | 178233930 |
| Output tokens | 771272 |
| Thinking tokens (main thread) | 3688 |
| Cache read tokens | 173888160 |
| Cache write tokens | 4343108 |
| Cache write tokens, main thread (5m / 1h) | 0 / 375131 |
| Cache hit ratio | 0.9756 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 512 | 66218746 | 7634 | 65843103 | 375131 |
| sub-agents | 2150 | 112015184 | 706917 | 108045057 | 3967977 |
| remainder | 0 | 0 | 56721 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 59 |
| Sub-agents spawned / failed / killed | 40 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 376 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.33 |
