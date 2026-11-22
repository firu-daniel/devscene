# Run analytics — feat_graphscene_walker_engine

## Whole run

| Measure | Value |
|---|---|
| Sessions | 8 (0 incomplete) |
| Engine / planning node sessions | 2 / 6 |
| Span | 1h57m |
| Wall | 1h56m |
| Session wall, summed over sessions | 1h59m |
| Active | 1h56m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $38.38 |
| Input tokens (uncached) | 1228 |
| Total input tokens (incl. cache) | 68972811 |
| Output tokens | 404357 |
| Thinking tokens (main thread) | 70652 |
| Cache read tokens | 66292475 |
| Cache write tokens | 2679108 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1212732 |
| Cache hit ratio | 0.9611 |
| Requests | 593 |
| Request latency p50 / p90 / p99 / max | 2.8s / 11.6s / 46.1s / 1m 44s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 24 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:skeptic-reviewer — Adversarial skeptic review — 5m 54s (session 8) |
| Rate-limit peak | seven_day 0.48 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 8m 37s | 8m 37s | 0.0s | 8m 39s | $3.48 |
| 3 | 2-architecture_review | 1m 21s | 1m 21s | 0.0s | 1m 22s | $1.33 |
| 4 | 3-plan_review | 3m 55s | 3m 55s | 0.0s | 3m 56s | $2.80 |
| 5 | 4-plan_writer | 28.0s | 28.0s | 0.0s | 29.2s | $0.28 |
| 6 | 5-architecture_review | 1m 30s | 1m 30s | 0.0s | 1m 31s | $1.48 |
| 7 | 6-plan_review | 3m 42s | 3m 42s | 0.0s | 3m 44s | $2.40 |

## Network refusals

8 of 8 sessions scanned.

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
| Wait (every run of task_round_1) | 40m 59s |
| Gate rows | 34 (complete) |
| Test files — full | 223 files, 20292.1 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 1 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 1 s |
| full | 3f | ok | 1 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2554 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 21 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 17 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 6 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 223)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1264.9 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 944.0 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 747.2 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 742.8 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 725.8 | 17 | 0 |
| test/remote-run.test.mjs | pass | 715.6 | 130 | 0 |
| test/remote-control.test.mjs | pass | 627.5 | 83 | 0 |
| test/doctor.test.mjs | pass | 621.0 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 598.5 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 575.8 | 21 | 0 |

## Session 1 — 2026-11-22T09:05:25.614Z → 2026-11-22T09:06:17.965Z

Session id: `f3c2ec80-13f0-4a4d-9f5b-97bd24fdd812`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 52.3s | 53.7s | 44.5s | 0.0s | 0.0s | 52.3s | 2.8s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.4s | 3.1s | 5.2s | 5.2s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.3s | 1.3s | 1.3s | 1.3s | 0 |
| orchestrator | 15 | 1.4s | 3.1s | 5.2s | 5.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 2.8s | 2.8s |
| Bash | orchestrator | 10 | 8.9s | 6.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 3 | 0.2s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:06:06.664Z | 6.0s | 599 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:27.783Z | 0.4s | 2196 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:55.686Z | 0.4s | 1410 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:47.377Z | 0.4s | 156 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:49.481Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:35.499Z | 0.3s | 157 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:31.383Z | 0.2s | 8887 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:52.119Z | 0.2s | 3717 | false | false |
| Bash | orchestrator | 2026-11-22T09:05:28.530Z | 0.2s | 2046 | false | false |
| Read | orchestrator | 2026-11-22T09:05:57.598Z | 0.2s | 26508 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 2.8s | 1 | 244 | 4 | 29005 | 11208 | 17793 | 0.0546 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.85 |
| Cost — claude-opus-5-5 | $0.85 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 914250 |
| Output tokens | 4737 |
| Thinking tokens (main thread) | 264 |
| Cache read tokens | 833672 |
| Cache write tokens | 80542 |
| Cache write tokens, main thread (5m / 1h) | 0 / 62749 |
| Cache hit ratio | 0.9119 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 885245 | 279 | 822464 | 62749 |
| sub-agents | 4 | 29005 | 244 | 11208 | 17793 |
| remainder | 0 | 0 | 4214 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 19 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.46 |

## Session 2 — 2026-11-22T09:06:21.280Z → 2026-11-22T09:14:59.082Z

Session id: `9a060cc8-0cb4-426b-8802-bfdb1ef1c068`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 8m 37s | 8m 39s | 8m 34s | 0.0s | 0.0s | 8m 37s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 26 | 1.8s | 46.1s | 1m 44s | 1m 44s | 0 |
| orchestrator | 26 | 1.8s | 46.1s | 1m 44s | 1m 44s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 14 | 4.0s | 0.4s |
| Read | orchestrator | 28 | 1.1s | 0.2s |
| Write | orchestrator | 11 | 0.5s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:10:01.624Z | 0.4s | 3141 | false | false |
| Bash | orchestrator | 2026-11-22T09:06:21.283Z | 0.4s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:07:54.155Z | 0.3s | 818 | false | false |
| Bash | orchestrator | 2026-11-22T09:09:50.339Z | 0.3s | 7511 | false | false |
| Bash | orchestrator | 2026-11-22T09:06:29.982Z | 0.2s | 2993 | false | false |
| Read | orchestrator | 2026-11-22T09:06:25.641Z | 0.2s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T09:10:08.809Z | 0.2s | 1839 | false | false |
| Bash | orchestrator | 2026-11-22T09:06:44.344Z | 0.2s | 968 | false | false |
| Bash | orchestrator | 2026-11-22T09:09:42.424Z | 0.2s | 12161 | false | false |
| Bash | orchestrator | 2026-11-22T09:06:41.555Z | 0.2s | 860 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.48 |
| Cost — claude-opus-5-5 | $3.48 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 3307556 |
| Output tokens | 57761 |
| Thinking tokens (main thread) | 26374 |
| Cache read tokens | 3093996 |
| Cache write tokens | 213508 |
| Cache write tokens, main thread (5m / 1h) | 0 / 213508 |
| Cache hit ratio | 0.9354 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 52 | 3307556 | 231 | 3093996 | 213508 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 57530 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 54 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.46 |

## Session 3 — 2026-11-22T09:15:02.714Z → 2026-11-22T09:16:24.424Z

Session id: `b375fa10-e4a9-4c0c-9295-6a59961595c5`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 21s | 1m 22s | 1m 20s | 0.0s | 0.0s | 1m 21s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 1.3s | 14.7s | 18.0s | 18.0s | 0 |
| orchestrator | 13 | 1.3s | 14.7s | 18.0s | 18.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 2.1s | 0.5s |
| Read | orchestrator | 22 | 0.6s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:15:03.102Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:48.141Z | 0.3s | 2335 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:13.847Z | 0.3s | 4160 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:04.306Z | 0.3s | 4393 | false | false |
| Read | orchestrator | 2026-11-22T09:15:06.537Z | 0.2s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T09:16:06.540Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:50.862Z | 0.2s | 2104 | false | false |
| Write | orchestrator | 2026-11-22T09:16:15.228Z | 0.0s | 231 | false | false |
| Read | orchestrator | 2026-11-22T09:15:06.043Z | 0.0s | 23014 | false | false |
| Read | orchestrator | 2026-11-22T09:15:27.168Z | 0.0s | 6025 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.33 |
| Cost — claude-opus-5-5 | $1.33 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1142484 |
| Output tokens | 9123 |
| Thinking tokens (main thread) | 3801 |
| Cache read tokens | 1024118 |
| Cache write tokens | 118340 |
| Cache write tokens, main thread (5m / 1h) | 0 / 118340 |
| Cache hit ratio | 0.8964 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1142484 | 181 | 1024118 | 118340 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8942 | 0 | 0 |

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
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.46 |

## Session 4 — 2026-11-22T09:15:03.103Z → 2026-11-22T09:18:58.338Z

Session id: `bf90803a-159d-4856-aef6-99419530f4ff`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 55s | 3m 56s | 3m 52s | 0.0s | 0.0s | 3m 55s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 26 | 2.3s | 17.7s | 51.2s | 51.2s | 0 |
| orchestrator | 26 | 2.3s | 17.7s | 51.2s | 51.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 12 | 3.6s | 0.5s |
| Read | orchestrator | 32 | 1.2s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:15:03.132Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:16:41.407Z | 0.4s | 3141 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:44.973Z | 0.4s | 1434 | false | false |
| Bash | orchestrator | 2026-11-22T09:17:07.725Z | 0.3s | 5101 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:05.983Z | 0.3s | 23352 | false | false |
| Bash | orchestrator | 2026-11-22T09:16:48.113Z | 0.3s | 10310 | false | false |
| Read | orchestrator | 2026-11-22T09:15:32.570Z | 0.2s | 31668 | false | false |
| Bash | orchestrator | 2026-11-22T09:15:37.590Z | 0.2s | 17154 | false | false |
| Bash | orchestrator | 2026-11-22T09:17:02.101Z | 0.2s | 3161 | false | false |
| Bash | orchestrator | 2026-11-22T09:17:32.663Z | 0.2s | 3505 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.80 |
| Cost — claude-opus-5-5 | $2.80 |
| Input tokens (uncached) | 52 |
| Total input tokens (incl. cache) | 3512949 |
| Output tokens | 24832 |
| Thinking tokens (main thread) | 16382 |
| Cache read tokens | 3308263 |
| Cache write tokens | 204634 |
| Cache write tokens, main thread (5m / 1h) | 0 / 204634 |
| Cache hit ratio | 0.9417 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 52 | 3512949 | 930 | 3308263 | 204634 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 23902 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 46 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.46 |

## Session 5 — 2026-11-22T09:19:07.508Z → 2026-11-22T09:19:35.535Z

Session id: `ee4b521d-0d95-430a-b467-5b0b6638c6aa`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 28.0s | 29.2s | 28.3s | 0.0s | 0.0s | 28.0s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 7 | 1.1s | 7.5s | 7.5s | 7.5s | 0 |
| orchestrator | 7 | 1.1s | 7.5s | 7.5s | 7.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 3 | 1.1s | 0.5s |
| Edit | orchestrator | 1 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:19:07.915Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:13.291Z | 0.3s | 1503 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:27.050Z | 0.2s | 1830 | false | false |
| Write | orchestrator | 2026-11-22T09:19:24.609Z | 0.0s | 237 | false | false |
| Edit | orchestrator | 2026-11-22T09:19:21.925Z | 0.0s | 234 | false | false |
| Read | orchestrator | 2026-11-22T09:19:09.652Z | 0.0s | 9663 | false | false |
| Read | orchestrator | 2026-11-22T09:19:08.561Z | 0.0s | 2265 | false | false |
| Read | orchestrator | 2026-11-22T09:19:11.378Z | 0.0s | 6025 | false | false |
| Read | orchestrator | 2026-11-22T09:19:09.211Z | 0.0s | 5109 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.28 |
| Cost — claude-opus-5-5 | $0.28 |
| Input tokens (uncached) | 14 |
| Total input tokens (incl. cache) | 221058 |
| Output tokens | 3294 |
| Thinking tokens (main thread) | 205 |
| Cache read tokens | 199073 |
| Cache write tokens | 21971 |
| Cache write tokens, main thread (5m / 1h) | 0 / 21971 |
| Cache hit ratio | 0.9005 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 14 | 221058 | 126 | 199073 | 21971 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 3168 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 10 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.46 |

## Session 6 — 2026-11-22T09:19:39.087Z → 2026-11-22T09:21:09.236Z

Session id: `77893013-cf27-4ee9-85d3-b9df8a94e489`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 30s | 1m 31s | 1m 28s | 0.0s | 0.0s | 1m 30s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 1.3s | 17.7s | 21.3s | 21.3s | 0 |
| orchestrator | 14 | 1.3s | 17.7s | 21.3s | 21.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 2.7s | 0.5s |
| Read | orchestrator | 23 | 0.8s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:19:39.104Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:35.990Z | 0.3s | 3390 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:41.676Z | 0.3s | 6634 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:33.188Z | 0.3s | 2939 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:29.654Z | 0.2s | 1432 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:34.488Z | 0.2s | 4082 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:44.866Z | 0.2s | 2457 | false | false |
| Read | orchestrator | 2026-11-22T09:19:55.279Z | 0.2s | 31668 | false | false |
| Read | orchestrator | 2026-11-22T09:19:52.775Z | 0.2s | 60702 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:50.126Z | 0.1s | 166 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.48 |
| Cost — claude-opus-5-5 | $1.48 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 1179485 |
| Output tokens | 10155 |
| Thinking tokens (main thread) | 4409 |
| Cache read tokens | 1046506 |
| Cache write tokens | 132951 |
| Cache write tokens, main thread (5m / 1h) | 0 / 132951 |
| Cache hit ratio | 0.8873 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 1179485 | 187 | 1046506 | 132951 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 9968 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 34 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.46 |

## Session 7 — 2026-11-22T09:19:39.002Z → 2026-11-22T09:23:21.964Z

Session id: `c2dd96a0-b69d-4038-8548-2c970e80141e`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 42s | 3m 44s | 3m 39s | 0.0s | 0.0s | 3m 42s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 23 | 2.5s | 18.7s | 54.9s | 54.9s | 0 |
| orchestrator | 23 | 2.5s | 18.7s | 54.9s | 54.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 14 | 4.3s | 0.5s |
| Read | orchestrator | 31 | 1.0s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T09:19:39.021Z | 0.5s | 57 | false | false |
| Bash | orchestrator | 2026-11-22T09:21:21.904Z | 0.3s | 3141 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:13.982Z | 0.3s | 7805 | false | false |
| Bash | orchestrator | 2026-11-22T09:22:30.876Z | 0.3s | 751 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:41.642Z | 0.3s | 6285 | false | false |
| Bash | orchestrator | 2026-11-22T09:21:34.806Z | 0.3s | 4410 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:25.150Z | 0.3s | 3277 | false | false |
| Bash | orchestrator | 2026-11-22T09:19:45.402Z | 0.3s | 1981 | false | false |
| Bash | orchestrator | 2026-11-22T09:20:53.310Z | 0.2s | 3620 | false | false |
| Bash | orchestrator | 2026-11-22T09:21:03.159Z | 0.2s | 6362 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.40 |
| Cost — claude-opus-5-5 | $2.40 |
| Input tokens (uncached) | 46 |
| Total input tokens (incl. cache) | 2799998 |
| Output tokens | 24377 |
| Thinking tokens (main thread) | 15928 |
| Cache read tokens | 2626220 |
| Cache write tokens | 173732 |
| Cache write tokens, main thread (5m / 1h) | 0 / 173732 |
| Cache hit ratio | 0.9379 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 46 | 2799998 | 906 | 2626220 | 173732 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 23471 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 47 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.47 |

## Session 8 — 2026-11-22T09:23:54.114Z → 2026-11-22T11:02:26.078Z

Session id: `5229f473-3e27-48fa-8df0-c3364b1e889d`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h38m | 1h38m | 48m 14s | 0.0s | 0.0s | 1h38m | 43m 07s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 468 | 2.9s | 9.8s | 40.6s | 1m 03s | 0 |
| devscene:architecture-reviewer | 11 | 3.8s | 5.9s | 9.8s | 9.8s | 0 |
| devscene:branch-reviewer | 35 | 4.4s | 23.8s | 30.1s | 30.1s | 0 |
| devscene:layer-implementer | 202 | 2.7s | 11.3s | 44.1s | 1m 03s | 0 |
| devscene:review-plan-reviewer | 29 | 3.2s | 7.2s | 13.5s | 13.5s | 0 |
| devscene:skeptic-reviewer | 39 | 4.4s | 18.3s | 31.0s | 31.0s | 0 |
| devscene:statistics-plan-writer | 7 | 2.8s | 19.3s | 19.3s | 19.3s | 0 |
| orchestrator | 145 | 2.8s | 5.0s | 9.5s | 13.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 19 | 43m 07s | 5m 54s |
| Bash | devscene:architecture-reviewer | 10 | 2.5s | 0.3s |
| Bash | devscene:branch-reviewer | 26 | 7.9s | 1.5s |
| Bash | devscene:layer-implementer | 154 | 4m 25s | 16.8s |
| Bash | devscene:review-plan-reviewer | 20 | 5.3s | 0.3s |
| Bash | devscene:skeptic-reviewer | 26 | 6.8s | 0.5s |
| Bash | devscene:statistics-plan-writer | 10 | 2.4s | 0.3s |
| Bash | orchestrator | 174 | 47m 30s | 1m 15s |
| Edit | devscene:layer-implementer | 78 | 3.0s | 0.0s |
| Edit | orchestrator | 12 | 6.3s | 5.8s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | devscene:architecture-reviewer | 10 | 0.7s | 0.2s |
| Read | devscene:branch-reviewer | 15 | 0.6s | 0.2s |
| Read | devscene:layer-implementer | 79 | 2.6s | 0.2s |
| Read | devscene:review-plan-reviewer | 27 | 0.7s | 0.2s |
| Read | devscene:skeptic-reviewer | 23 | 0.3s | 0.0s |
| Read | devscene:statistics-plan-writer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 13 | 7.6s | 5.7s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 5 | 0.2s | 0.0s |
| Write | devscene:layer-implementer | 16 | 0.7s | 0.0s |
| Write | devscene:skeptic-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T10:01:39.659Z | 1m 15s | 722 | false | false |
| Bash | orchestrator | 2026-11-22T10:24:26.306Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:18:51.600Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:20:01.686Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:29:54.907Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:46:26.664Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:23:19.001Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:37:37.016Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:28:48.748Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T10:39:50.046Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/engine/test_transitions.py | 3 | 3.1s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_layers.py | 11 | 49.1s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 13 | 1m 47s |
| devscene:layer-implementer | git diff --name-only HEAD | 4 | 4.9s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 3 | 0.8s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 13 | 3.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 3 | 20.0s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_walker_engine_story_plan.md - | 10 | 1m 08s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 41 | 40m 59s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null | 57 | 48.0s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 1m 23s | 11 | 7043 | 24 | 766646 | 692974 | 73648 | 0.0141 |
| devscene:layer-implementer | Implement Task 2 graphscene | 57.3s | 9 | 4928 | 20 | 565633 | 512305 | 53308 | 0.0097 |
| devscene:layer-implementer | Implement Task 3 graphscene | 5m 14s | 31 | 35007 | 64 | 2524946 | 2435592 | 89290 | 0.0531 |
| devscene:layer-implementer | Implement Task 4 graphscene | 1m 56s | 16 | 10745 | 34 | 937958 | 882428 | 55496 | 0.0197 |
| devscene:layer-implementer | Implement Task 5 graphscene | 2m 42s | 19 | 15401 | 40 | 1116682 | 1060882 | 55760 | 0.0274 |
| devscene:layer-implementer | Implement Task 6 graphscene | 3m 26s | 18 | 21936 | 38 | 1519334 | 1434396 | 84900 | 0.0349 |
| devscene:layer-implementer | Implement Task 7 graphscene | 1m 47s | 11 | 9325 | 24 | 623124 | 571193 | 51907 | 0.0181 |
| devscene:layer-implementer | Implement Task 8 graphscene | 2m 31s | 20 | 13701 | 42 | 1241368 | 1182837 | 58489 | 0.0256 |
| devscene:layer-implementer | Implement Task 9 graphscene | 1m 50s | 19 | 8513 | 40 | 1000013 | 953213 | 46760 | 0.0187 |
| devscene:layer-implementer | Implement Task 10 general | 1m 05s | 9 | 4145 | 20 | 697494 | 617508 | 79966 | 0.0111 |
| devscene:architecture-reviewer | Architecture review of branch | 1m 07s | 11 | 5181 | 24 | 1099777 | 969447 | 130306 | 0.0114 |
| devscene:branch-reviewer | End-of-branch code review | 5m 05s | 35 | 25788 | 72 | 5277521 | 5083080 | 194369 | 0.0516 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 14s | 12 | 6600 | 26 | 832950 | 743567 | 89357 | 0.0126 |
| devscene:layer-implementer | Fix code-review Finding 2 | 1m 16s | 10 | 2289 | 22 | 371374 | 336678 | 34674 | 0.013 |
| devscene:layer-implementer | Fix code-review Finding 1 | 1m 18s | 12 | 4964 | 26 | 506267 | 474764 | 31477 | 0.0134 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 5m 54s | 39 | 31219 | 80 | 4103939 | 3951957 | 151902 | 0.06 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 1m 32s | 17 | 7315 | 36 | 921952 | 843207 | 78709 | 0.0157 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 1m 52s | 17 | 9858 | 36 | 836473 | 780748 | 55689 | 0.019 |
| devscene:statistics-plan-writer | Write branch statistics | 50.5s | 7 | 5062 | 16 | 240017 | 207425 | 32576 | 0.0086 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $25.76 |
| Cost — claude-opus-5-5 | $25.76 |
| Input tokens (uncached) | 974 |
| Total input tokens (incl. cache) | 55895031 |
| Output tokens | 270078 |
| Thinking tokens (main thread) | 3289 |
| Cache read tokens | 54160627 |
| Cache write tokens | 1733430 |
| Cache write tokens, main thread (5m / 1h) | 0 / 284847 |
| Cache hit ratio | 0.969 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 290 | 30711563 | 3991 | 30426426 | 284847 |
| sub-agents | 684 | 25183468 | 229020 | 23734201 | 1448583 |
| remainder | 0 | 0 | 37067 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 21 |
| Sub-agents spawned / failed / killed | 19 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 222 |
| Time to first token | 1.6s |
| Rate-limit peak | seven_day 0.48 |
