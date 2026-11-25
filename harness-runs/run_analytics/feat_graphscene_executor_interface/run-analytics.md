# Run analytics — feat_graphscene_executor_interface

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 1h26m |
| Wall | 1h25m |
| Session wall, summed over sessions | 1h27m |
| Active | 1h18m |
| Host-suspended | 0.0s |
| Idle | 6m 51s |
| Cost | $27.83 |
| Input tokens (uncached) | 852 |
| Total input tokens (incl. cache) | 55125290 |
| Output tokens | 224431 |
| Thinking tokens (main thread) | 30401 |
| Cache read tokens | 53131799 |
| Cache write tokens | 1992639 |
| Cache write tokens, main thread (5m / 1h) | 0 / 914707 |
| Cache hit ratio | 0.9638 |
| Requests | 410 |
| Request latency p50 / p90 / p99 / max | 1.6s / 7.2s / 33.1s / 6m 51s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 14 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — End-of-branch code review — 4m 13s (session 5) |
| Rate-limit peak | seven_day 0.17 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 5m 11s | 5m 11s | 0.0s | 5m 12s | $2.87 |
| 3 | 2-architecture_review | 1m 16s | 1m 16s | 0.0s | 1m 17s | $1.77 |
| 4 | 3-plan_review | 2m 36s | 2m 36s | 0.0s | 2m 37s | $2.45 |

## Network refusals

5 of 5 sessions scanned.

| Session | Context | Tool | Command | Host | Port | Refusal line |
|---|---|---|---|---|---|---|
| 5 | devscene:branch-reviewer | Bash | bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_probe.py | example.invalid | 443 | <sandbox_violations> |

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
| Wait (every run of task_round_1) | 41m 24s |
| Gate rows | 32 (complete) |
| Test files — full | 233 files, 20050.4 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 1 s |
| full | 2b | ok | 1 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 1 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 4 | ok | 2491 s |
| full | 6a | ok | 3 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 19 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 18 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 7 s |
| full | 13h | ok | 1 s |
| full | 13i | ok | 0 s |
| full | 13j | ok | 14 s |
| full | 14a | ok | 7 s |
| full | 14c | ok | 7 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 233)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1333.7 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 886.7 | 21 | 0 |
| test/remote-run.test.mjs | pass | 753.2 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 718.0 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 709.4 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 671.1 | 17 | 0 |
| test/remote-control.test.mjs | pass | 659.1 | 83 | 0 |
| test/doctor.test.mjs | pass | 639.0 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 588.9 | 33 | 0 |
| test/planning-driver-walk.test.mjs | pass | 545.4 | 9 | 0 |

## Session 1 — 2026-11-25T14:18:35.251Z → 2026-11-25T14:19:28.335Z

Session id: `d4e71aa6-02f1-4a76-bf65-e9708c85e7b3`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 53.0s | 54.1s | 46.7s | 0.0s | 0.0s | 53.0s | 2.7s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 1.3s | 3.1s | 4.7s | 4.7s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.3s | 1.3s | 1.3s | 1.3s | 0 |
| orchestrator | 17 | 1.2s | 3.1s | 4.7s | 4.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 2.7s | 2.7s |
| Bash | orchestrator | 14 | 7.6s | 5.2s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.4s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-25T14:19:18.329Z | 5.2s | 619 | false | false |
| Read | orchestrator | 2026-11-25T14:19:07.164Z | 0.3s | 26508 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:37.121Z | 0.2s | 62 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:45.596Z | 0.2s | 162 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:42.263Z | 0.2s | 8751 | true | false |
| Bash | orchestrator | 2026-11-25T14:19:05.533Z | 0.1s | 1267 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:56.773Z | 0.1s | 161 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:59.077Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-25T14:18:59.963Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-25T14:19:01.785Z | 0.1s | 644 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 2.7s | 1 | 228 | 4 | 29387 | 11246 | 18137 | 0.0523 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.93 |
| Cost — claude-opus-5-5 | $0.93 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 1074772 |
| Output tokens | 5191 |
| Thinking tokens (main thread) | 280 |
| Cache read tokens | 989956 |
| Cache write tokens | 84778 |
| Cache write tokens, main thread (5m / 1h) | 0 / 66641 |
| Cache hit ratio | 0.9211 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 1045385 | 287 | 978710 | 66641 |
| sub-agents | 4 | 29387 | 228 | 11246 | 18137 |
| remainder | 0 | 0 | 4676 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 24 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.16 |

## Session 2 — 2026-11-25T14:19:30.614Z → 2026-11-25T14:24:41.923Z

Session id: `50f3aed3-5e98-459a-ab99-ce4690c9d22d`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 11s | 5m 12s | 5m 10s | 0.0s | 0.0s | 5m 11s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 27 | 1.7s | 15.3s | 50.5s | 50.5s | 0 |
| orchestrator | 27 | 1.7s | 15.3s | 50.5s | 50.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 2.2s | 0.2s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 29 | 1.1s | 0.3s |
| Write | orchestrator | 5 | 0.1s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-25T14:19:37.109Z | 0.3s | 37113 | false | false |
| Bash | orchestrator | 2026-11-25T14:19:31.088Z | 0.2s | 62 | false | false |
| Read | orchestrator | 2026-11-25T14:19:37.557Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-25T14:19:57.599Z | 0.2s | 9063 | false | false |
| Read | orchestrator | 2026-11-25T14:19:40.758Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-25T14:21:25.525Z | 0.2s | 2092 | false | false |
| Bash | orchestrator | 2026-11-25T14:21:34.586Z | 0.2s | 725 | false | false |
| Bash | orchestrator | 2026-11-25T14:21:15.087Z | 0.2s | 728 | false | false |
| Bash | orchestrator | 2026-11-25T14:21:19.939Z | 0.1s | 3635 | false | false |
| Bash | orchestrator | 2026-11-25T14:21:42.535Z | 0.1s | 283 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.87 |
| Cost — claude-opus-5-5 | $2.87 |
| Input tokens (uncached) | 54 |
| Total input tokens (incl. cache) | 3564134 |
| Output tokens | 35121 |
| Thinking tokens (main thread) | 13099 |
| Cache read tokens | 3377921 |
| Cache write tokens | 186159 |
| Cache write tokens, main thread (5m / 1h) | 0 / 186159 |
| Cache hit ratio | 0.9478 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 54 | 3564134 | 228 | 3377921 | 186159 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 34893 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 49 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.16 |

## Session 3 — 2026-11-25T14:24:44.233Z → 2026-11-25T14:26:00.769Z

Session id: `13932a62-a841-4965-8a46-f53dad220bff`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 16s | 1m 17s | 1m 15s | 0.0s | 0.0s | 1m 16s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 1.9s | 7.5s | 20.5s | 20.5s | 0 |
| orchestrator | 13 | 1.9s | 7.5s | 20.5s | 20.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 1.1s | 0.2s |
| Read | orchestrator | 21 | 1.3s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-25T14:24:55.048Z | 0.3s | 37113 | false | false |
| Bash | orchestrator | 2026-11-25T14:24:44.601Z | 0.2s | 62 | false | false |
| Read | orchestrator | 2026-11-25T14:25:18.575Z | 0.2s | 63403 | false | false |
| Read | orchestrator | 2026-11-25T14:25:23.131Z | 0.2s | 30738 | false | false |
| Read | orchestrator | 2026-11-25T14:24:59.529Z | 0.2s | 63338 | false | false |
| Bash | orchestrator | 2026-11-25T14:25:45.251Z | 0.2s | 7552 | false | false |
| Bash | orchestrator | 2026-11-25T14:25:08.699Z | 0.1s | 1570 | false | false |
| Bash | orchestrator | 2026-11-25T14:24:46.894Z | 0.1s | 8486 | true | false |
| Bash | orchestrator | 2026-11-25T14:25:49.903Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-25T14:24:56.397Z | 0.0s | 727 | true | true |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.77 |
| Cost — claude-opus-5-5 | $1.77 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1296994 |
| Output tokens | 8046 |
| Thinking tokens (main thread) | 3937 |
| Cache read tokens | 1124215 |
| Cache write tokens | 172753 |
| Cache write tokens, main thread (5m / 1h) | 0 / 172753 |
| Cache hit ratio | 0.8668 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1296994 | 148 | 1124215 | 172753 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7898 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 29 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.16 |

## Session 4 — 2026-11-25T14:24:44.370Z → 2026-11-25T14:27:20.525Z

Session id: `b460eb76-b618-4836-a1ec-e226b388db85`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 36s | 2m 37s | 2m 34s | 0.0s | 0.0s | 2m 36s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 19 | 1.5s | 23.1s | 37.9s | 37.9s | 0 |
| orchestrator | 19 | 1.5s | 23.1s | 37.9s | 37.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 15 | 2.6s | 0.2s |
| Read | orchestrator | 29 | 1.4s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-25T14:24:52.520Z | 0.2s | 37113 | false | false |
| Read | orchestrator | 2026-11-25T14:25:05.741Z | 0.2s | 30738 | false | false |
| Read | orchestrator | 2026-11-25T14:24:53.069Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-25T14:26:22.534Z | 0.2s | 175 | false | false |
| Bash | orchestrator | 2026-11-25T14:24:44.804Z | 0.2s | 62 | false | false |
| Read | orchestrator | 2026-11-25T14:25:00.779Z | 0.2s | 30778 | false | false |
| Bash | orchestrator | 2026-11-25T14:26:09.067Z | 0.2s | 9154 | false | false |
| Bash | orchestrator | 2026-11-25T14:26:03.556Z | 0.2s | 1077 | false | false |
| Bash | orchestrator | 2026-11-25T14:26:17.412Z | 0.2s | 5303 | false | false |
| Bash | orchestrator | 2026-11-25T14:24:45.852Z | 0.1s | 9451 | true | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.45 |
| Cost — claude-opus-5-5 | $2.45 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 2728842 |
| Output tokens | 17108 |
| Thinking tokens (main thread) | 10406 |
| Cache read tokens | 2528373 |
| Cache write tokens | 200431 |
| Cache write tokens, main thread (5m / 1h) | 0 / 200431 |
| Cache hit ratio | 0.9265 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 38 | 2728842 | 889 | 2528373 | 200431 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 16219 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 46 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.16 |

## Session 5 — 2026-11-25T14:27:51.116Z → 2026-11-25T15:44:59.604Z

Session id: `4a5655a8-c87c-498b-b7f7-f073a871b6b5`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h17m | 1h17m | 30m 31s | 0.0s | 6m 51s | 1h10m | 19m 50s | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-25T14:34:51.944Z | 6m 51s | orchestrator | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 333 | 1.7s | 6.4s | 29.5s | 6m 51s | 1 |
| devscene:architecture-reviewer | 11 | 2.1s | 8.7s | 9.8s | 9.8s | 0 |
| devscene:branch-reviewer | 29 | 3.1s | 29.5s | 36.4s | 36.4s | 0 |
| devscene:layer-implementer | 109 | 1.7s | 5.5s | 14.9s | 17.3s | 0 |
| devscene:review-plan-reviewer | 17 | 2.5s | 9.7s | 14.7s | 14.7s | 0 |
| devscene:skeptic-reviewer | 24 | 3.2s | 22.7s | 27.8s | 27.8s | 0 |
| devscene:statistics-plan-writer | 4 | 1.3s | 17.3s | 17.3s | 17.3s | 0 |
| orchestrator | 139 | 1.5s | 1.9s | 7.9s | 6m 51s | 1 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 15 | 19m 50s | 4m 13s |
| Bash | devscene:architecture-reviewer | 10 | 1.5s | 0.1s |
| Bash | devscene:branch-reviewer | 25 | 5.3s | 0.6s |
| Bash | devscene:layer-implementer | 92 | 1m 46s | 12.4s |
| Bash | devscene:review-plan-reviewer | 15 | 2.8s | 0.4s |
| Bash | devscene:skeptic-reviewer | 18 | 3.3s | 0.4s |
| Bash | devscene:statistics-plan-writer | 4 | 0.6s | 0.1s |
| Bash | orchestrator | 174 | 45m 23s | 1m 03s |
| Edit | devscene:layer-implementer | 42 | 1.4s | 0.0s |
| Edit | orchestrator | 11 | 0.3s | 0.0s |
| Read | devscene:architecture-reviewer | 8 | 0.5s | 0.2s |
| Read | devscene:branch-reviewer | 14 | 0.2s | 0.0s |
| Read | devscene:layer-implementer | 42 | 0.9s | 0.2s |
| Read | devscene:review-plan-reviewer | 13 | 0.1s | 0.0s |
| Read | devscene:skeptic-reviewer | 11 | 0.4s | 0.2s |
| Read | devscene:statistics-plan-writer | 4 | 0.1s | 0.0s |
| Read | orchestrator | 12 | 2.4s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 6 | 0.2s | 0.0s |
| Write | devscene:layer-implementer | 6 | 0.2s | 0.0s |
| Write | devscene:review-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:skeptic-reviewer | 6 | 0.2s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-25T15:22:41.283Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:05:39.330Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:29:04.735Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:20:32.713Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:01:22.456Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:04:34.648Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:13:06.217Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:33:19.619Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:06:44.441Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-25T15:43:44.654Z | 1m 01s | 745 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/adapters/test_return_schema.py | 5 | 6.9s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/adapters/test_stub_executor.py | 4 | 2.8s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_layers.py | 7 | 15.3s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 11 | 59.6s |
| devscene:layer-implementer | git diff --name-only HEAD | 5 | 0.9s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 5 | 0.9s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.3s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/feat_graphscene_executor_interface_co | 3 | 16.9s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_executor_interface_story_plan | 4 | 25.1s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 41 | 41m 24s |
| orchestrator | cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 14 | 2.2s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null | 55 | 31.6s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 1m 04s | 13 | 5764 | 28 | 714693 | 656935 | 57730 | 0.014 |
| devscene:layer-implementer | Implement Task 2 graphscene | 1m 24s | 14 | 8493 | 30 | 784593 | 734700 | 49863 | 0.0183 |
| devscene:layer-implementer | Implement Task 3 graphscene | 1m 26s | 16 | 8941 | 34 | 923074 | 871880 | 51160 | 0.0187 |
| devscene:layer-implementer | Implement Task 4 graphscene | 1m 39s | 21 | 10134 | 44 | 1382398 | 1319783 | 62571 | 0.0215 |
| devscene:architecture-reviewer | Architecture review implemented branch | 58.0s | 11 | 6161 | 24 | 1144927 | 1004635 | 140268 | 0.0126 |
| devscene:branch-reviewer | End-of-branch code review | 4m 13s | 29 | 28034 | 60 | 3519055 | 3361410 | 157585 | 0.0548 |
| devscene:review-plan-reviewer | Meta-review code review | 54.2s | 9 | 5689 | 20 | 484896 | 413906 | 70970 | 0.0117 |
| devscene:layer-implementer | Fix Finding 3 NaN delay | 36.6s | 11 | 2885 | 24 | 710978 | 645888 | 65066 | 0.0079 |
| devscene:layer-implementer | Fix Finding 2 delay cancel test | 33.5s | 10 | 2883 | 22 | 662842 | 606370 | 56450 | 0.0072 |
| devscene:layer-implementer | Fix Finding 1 ecma patterns | 1m 02s | 12 | 6385 | 26 | 689744 | 638486 | 51232 | 0.0135 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 3m 40s | 24 | 23920 | 50 | 1985774 | 1871993 | 113731 | 0.0477 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 44.5s | 8 | 4931 | 18 | 370661 | 308014 | 62629 | 0.0096 |
| devscene:layer-implementer | Fix skeptic Finding 2 comment | 16.3s | 4 | 1190 | 10 | 166082 | 129123 | 36949 | 0.0035 |
| devscene:layer-implementer | Fix skeptic Finding 1 $schema | 43.7s | 8 | 4429 | 18 | 416651 | 374138 | 42495 | 0.0095 |
| devscene:statistics-plan-writer | Write branch statistics | 31.1s | 4 | 4190 | 10 | 175217 | 134111 | 41096 | 0.0067 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $19.81 |
| Cost — claude-opus-5-5 | $19.81 |
| Input tokens (uncached) | 696 |
| Total input tokens (incl. cache) | 46460548 |
| Output tokens | 158965 |
| Thinking tokens (main thread) | 2679 |
| Cache read tokens | 45111334 |
| Cache write tokens | 1348518 |
| Cache write tokens, main thread (5m / 1h) | 0 / 288723 |
| Cache hit ratio | 0.971 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 278 | 32328963 | 3215 | 32039962 | 288723 |
| sub-agents | 418 | 14131585 | 124029 | 13071372 | 1059795 |
| remainder | 0 | 0 | 31721 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 12 |
| Sub-agents spawned / failed / killed | 15 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 215 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.17 |
