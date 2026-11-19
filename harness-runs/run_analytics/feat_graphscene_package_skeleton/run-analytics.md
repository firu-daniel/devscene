# Run analytics — feat_graphscene_package_skeleton

## Whole run

| Measure | Value |
|---|---|
| Sessions | 7 (1 incomplete) |
| Engine / planning node sessions | 4 / 3 |
| Span | 2h33m |
| Wall | 2h16m |
| Session wall, summed over sessions | 2h18m |
| Active | 2h16m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $24.76 |
| Input tokens (uncached) | 800 (6 of 7 sessions) |
| Total input tokens (incl. cache) | 47360274 (6 of 7 sessions) |
| Output tokens | 225659 (6 of 7 sessions) |
| Thinking tokens (main thread) | 51797 |
| Cache read tokens | 45718649 (6 of 7 sessions) |
| Cache write tokens | 1640825 (6 of 7 sessions) |
| Cache write tokens, main thread (5m / 1h) | 0 / 966022 |
| Cache hit ratio | 0.9653 |
| Requests | 690 |
| Request latency p50 / p90 / p99 / max | 1.8s / 6.8s / 39.1s / 55.2s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 8 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:skeptic-reviewer — C2.1 skeptic review of branch — 4m 19s (session 7) |
| Rate-limit peak | seven_day 0.32 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 8m 11s | 8m 11s | 0.0s | 8m 12s | $3.28 |
| 3 | 2-architecture_review | 1m 23s | 1m 23s | 0.0s | 1m 25s | $1.26 |
| 4 | 3-plan_review | 4m 20s | 4m 20s | 0.0s | 4m 21s | $2.71 |

## Network refusals

7 of 7 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No possible network attempt in 2 round logs.

## Gate rounds

Wait is the orchestrator's wait on `run-test-suite.sh --wait <label>`, summed over every polling row whose command ends in that label; — when none matches, as for a label waited on fewer than three times in a session (no polling row is written for it) or a command cut at 160 characters.

A phase's test-file total sums each file's own seconds, so it exceeds the gate's wall time when files run in parallel.

### Round task_round_1 — fail

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | 35m 51s |
| Gate rows | 31 (complete) |
| Test files — full | 222 files, 17748.6 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 4 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 2 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2230 s |
| full | 6a | ok | 1 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 17 s |
| full | 13a | FAIL | 1 s |
| full | 13b | ok | 6 s |
| full | 13c | ok | 17 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 0 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1109.8 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 801.9 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 644.1 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 620.7 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 598.2 | 17 | 0 |
| test/remote-run.test.mjs | pass | 597.4 | 130 | 0 |
| test/doctor.test.mjs | pass | 569.5 | 1 | 0 |
| test/remote-control.test.mjs | pass | 543.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 527.2 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 479.4 | 21 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 38m 10s |
| Gate rows | 31 (complete) |
| Test files — full | 222 files, 18230.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 13a | ok | 0 s |
| full | 1 | ok | 1 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 1 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 1 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2321 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 15 s |
| full | 13b | ok | 2 s |
| full | 13c | ok | 14 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 1 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1148.4 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 863.7 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 656.4 | 29 | 0 |
| test/remote-run.test.mjs | pass | 652.0 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 638.9 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 624.3 | 17 | 0 |
| test/remote-control.test.mjs | pass | 586.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 564.3 | 33 | 0 |
| test/doctor.test.mjs | pass | 554.8 | 1 | 0 |
| test/watcher-run-profile.test.mjs | pass | 499.4 | 21 | 0 |

## Session 1 — 2026-11-19T11:09:02.597Z → 2026-11-19T11:09:57.584Z

Session id: `1c24dda2-aae9-47ff-a8c2-c8817c0d1fd0`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 54.9s | 56.7s | 48.1s | 0.0s | 0.0s | 54.9s | 3.7s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 15 | 1.6s | 4.9s | 7.0s | 7.0s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.9s | 1.9s | 1.9s | 1.9s | 0 |
| orchestrator | 14 | 1.6s | 4.9s | 7.0s | 7.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 3.7s | 3.7s |
| Bash | orchestrator | 15 | 9.9s | 6.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 2 | 0.0s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:09:46.518Z | 6.1s | 611 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:05.150Z | 0.5s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:26.834Z | 0.3s | 159 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:38.279Z | 0.3s | 6 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:15.111Z | 0.2s | 6 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:05.500Z | 0.2s | 32 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:13.322Z | 0.2s | 160 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:06.041Z | 0.2s | 27 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:30.031Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T11:09:29.030Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 3.7s | 1 | 287 | 4 | 26978 | 10501 | 16473 | 0.0689 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.83 |
| Cost — claude-opus-5-5 | $0.83 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 829150 |
| Output tokens | 5271 |
| Thinking tokens (main thread) | 324 |
| Cache read tokens | 751800 |
| Cache write tokens | 77316 |
| Cache write tokens, main thread (5m / 1h) | 0 / 60843 |
| Cache hit ratio | 0.9067 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 30 | 802172 | 219 | 741299 | 60843 |
| sub-agents | 4 | 26978 | 287 | 10501 | 16473 |
| remainder | 0 | 0 | 4765 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.3 |

## Session 2 — 2026-11-19T11:10:00.963Z → 2026-11-19T11:18:12.400Z

Session id: `9360c2b9-126e-46ea-bfff-9c4c64da0368`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 8m 11s | 8m 12s | 8m 05s | 0.0s | 0.0s | 8m 11s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 34 | 2.1s | 39.1s | 44.6s | 44.6s | 0 |
| orchestrator | 34 | 2.1s | 39.1s | 44.6s | 44.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 22 | 7.4s | 0.7s |
| Edit | orchestrator | 2 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 0.8s | 0.3s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:12:24.608Z | 0.7s | 2824 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:25.591Z | 0.5s | 11765 | false | false |
| Bash | orchestrator | 2026-11-19T11:14:45.927Z | 0.4s | 610 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:29.599Z | 0.4s | 11920 | false | false |
| Bash | orchestrator | 2026-11-19T11:13:14.075Z | 0.4s | 3763 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:00.969Z | 0.3s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:12:28.240Z | 0.3s | 4108 | false | false |
| Bash | orchestrator | 2026-11-19T11:10:17.957Z | 0.3s | 2259 | false | false |
| Bash | orchestrator | 2026-11-19T11:11:37.820Z | 0.3s | 1312 | false | false |
| Bash | orchestrator | 2026-11-19T11:13:22.384Z | 0.3s | 7342 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.28 |
| Cost — claude-opus-5-5 | $3.28 |
| Input tokens (uncached) | 68 |
| Total input tokens (incl. cache) | 4087226 |
| Output tokens | 50490 |
| Thinking tokens (main thread) | 25831 |
| Cache read tokens | 3901574 |
| Cache write tokens | 185584 |
| Cache write tokens, main thread (5m / 1h) | 0 / 185584 |
| Cache hit ratio | 0.9546 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 68 | 4087226 | 290 | 3901574 | 185584 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 50200 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 47 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.31 |

## Session 3 — 2026-11-19T11:18:16.113Z → 2026-11-19T11:19:40.070Z

Session id: `2b50df55-3a37-43b9-9699-8e535c104c59`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 23s | 1m 25s | 1m 22s | 0.0s | 0.0s | 1m 23s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 2.3s | 9.6s | 15.4s | 15.4s | 0 |
| orchestrator | 13 | 2.3s | 9.6s | 15.4s | 15.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 2.5s | 0.5s |
| Read | orchestrator | 16 | 0.9s | 0.4s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:18:16.577Z | 0.5s | 60 | false | false |
| Read | orchestrator | 2026-11-19T11:18:23.570Z | 0.4s | 31668 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:50.926Z | 0.3s | 7118 | true | false |
| Bash | orchestrator | 2026-11-19T11:19:01.036Z | 0.3s | 4350 | false | false |
| Read | orchestrator | 2026-11-19T11:18:22.569Z | 0.3s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:17.140Z | 0.2s | 5810 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:22.810Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:15.816Z | 0.2s | 1873 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:32.531Z | 0.2s | 166 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:19.804Z | 0.2s | 1555 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.26 |
| Cost — claude-opus-5-5 | $1.26 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1069974 |
| Output tokens | 8706 |
| Thinking tokens (main thread) | 4011 |
| Cache read tokens | 958786 |
| Cache write tokens | 111162 |
| Cache write tokens, main thread (5m / 1h) | 0 / 111162 |
| Cache hit ratio | 0.8961 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1069974 | 142 | 958786 | 111162 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8564 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 26 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.31 |

## Session 4 — 2026-11-19T11:18:16.145Z → 2026-11-19T11:22:36.423Z

Session id: `b8047493-e048-4900-ad0d-0625fd5aee21`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 20s | 4m 21s | 4m 16s | 0.0s | 0.0s | 4m 20s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 27 | 3.6s | 28.7s | 48.6s | 48.6s | 0 |
| orchestrator | 27 | 3.6s | 28.7s | 48.6s | 48.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 25 | 6.8s | 0.5s |
| Read | orchestrator | 18 | 0.9s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:18:16.577Z | 0.5s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:58.024Z | 0.4s | 486 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:23.167Z | 0.3s | 9962 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:26.816Z | 0.3s | 1108 | false | false |
| Bash | orchestrator | 2026-11-19T11:20:24.894Z | 0.3s | 3244 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:35.886Z | 0.3s | 9200 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:33.183Z | 0.3s | 9261 | false | false |
| Bash | orchestrator | 2026-11-19T11:19:47.303Z | 0.3s | 16033 | false | false |
| Read | orchestrator | 2026-11-19T11:18:28.418Z | 0.3s | 46614 | false | false |
| Bash | orchestrator | 2026-11-19T11:18:17.549Z | 0.2s | 7963 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.71 |
| Cost — claude-opus-5-5 | $2.71 |
| Input tokens (uncached) | 54 |
| Total input tokens (incl. cache) | 3663428 |
| Output tokens | 26449 |
| Thinking tokens (main thread) | 17219 |
| Cache read tokens | 3477283 |
| Cache write tokens | 186091 |
| Cache write tokens, main thread (5m / 1h) | 0 / 186091 |
| Cache hit ratio | 0.9492 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 54 | 3663428 | 948 | 3477283 | 186091 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 25501 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 45 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.31 |

## Session 5 — 2026-11-19T11:23:09.506Z → 2026-11-19T11:28:18.800Z

Session id: `020f1708-5577-4edb-993a-c9635f26c7fe`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 09s | 5m 11s | 4m 44s | 0.0s | 0.0s | 5m 09s | 3m 29s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 61 | 1.7s | 6.8s | 55.2s | 55.2s | 0 |
| devscene:layer-implementer | 28 | 2.4s | 12.6s | 55.2s | 55.2s | 0 |
| orchestrator | 33 | 1.5s | 2.5s | 9.5s | 9.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 2 | 3m 29s | 2m 42s |
| Bash | devscene:layer-implementer | 17 | 14.3s | 5.4s |
| Bash | orchestrator | 22 | 11.1s | 6.5s |
| Edit | devscene:layer-implementer | 11 | 0.4s | 0.0s |
| Read | devscene:layer-implementer | 10 | 0.5s | 0.2s |
| Read | orchestrator | 14 | 1.8s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 5 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T11:26:53.199Z | 6.5s | 782 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:16.323Z | 5.4s | 217 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:26.048Z | 4.7s | 507 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:27:36.070Z | 0.4s | 175 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:26:13.090Z | 0.4s | 280 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:27:32.286Z | 0.3s | 182 | true | false |
| Bash | orchestrator | 2026-11-19T11:23:11.638Z | 0.3s | 60 | false | false |
| Bash | orchestrator | 2026-11-19T11:23:28.940Z | 0.3s | 155 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:24:25.563Z | 0.3s | 5117 | false | false |
| Read | orchestrator | 2026-11-19T11:23:48.744Z | 0.3s | 49208 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (general) | 2m 42s | 18 | 17526 | 38 | 1188801 | 1114390 | 74373 | 0.524 |
| devscene:layer-implementer | Implement Task 2 (general) | 47.0s | 10 | 5039 | 22 | 508492 | 468549 | 39921 | 0.1522 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.96 |
| Cost — claude-opus-5-5 | $3.96 |
| Input tokens (uncached) | 128 |
| Total input tokens (incl. cache) | 6229305 |
| Output tokens | 31362 |
| Thinking tokens (main thread) | 1462 |
| Cache read tokens | 5918321 |
| Cache write tokens | 310856 |
| Cache write tokens, main thread (5m / 1h) | 0 / 196562 |
| Cache hit ratio | 0.9501 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 68 | 4532012 | 762 | 4335382 | 196562 |
| sub-agents | 60 | 1697293 | 22565 | 1582939 | 114294 |
| remainder | 0 | 0 | 8035 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 2 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 42 |
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.31 |

## Session 6 — 2026-11-19T11:37:08.591Z → 2026-11-19T12:01:57.483Z (incomplete — no result event)

Session id: `a099b08d-66ee-49b1-95d1-3ccad190291e`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 24m 48s | — | — | — | 0.0s | 24m 48s | 18m 20s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 303 | 1.9s | 5.5s | 17.3s | 19.9s | 0 |
| devscene:architecture-reviewer | 21 | 2.1s | 17.3s | 19.9s | 19.9s | 0 |
| devscene:branch-reviewer | 39 | 3.1s | 13.0s | 18.5s | 18.5s | 0 |
| devscene:layer-implementer | 96 | 2.2s | 3.9s | 11.8s | 11.8s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.6s | 1.6s | 1.6s | 1.6s | 0 |
| devscene:review-plan-reviewer | 8 | 2.1s | 10.8s | 10.8s | 10.8s | 0 |
| devscene:task-plan-reviewer | 29 | 2.9s | 13.5s | 14.5s | 14.5s | 0 |
| devscene:task-plan-writer | 6 | 3.3s | 10.7s | 10.7s | 10.7s | 0 |
| orchestrator | 103 | 1.6s | 2.5s | 4.4s | 4.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 16 | 19m 28s | 4m 10s |
| Bash | devscene:architecture-reviewer | 16 | 3.9s | 0.3s |
| Bash | devscene:branch-reviewer | 37 | 8.9s | 0.7s |
| Bash | devscene:layer-implementer | 77 | 2m 18s | 12.1s |
| Bash | devscene:review-plan-reviewer | 6 | 1.4s | 0.3s |
| Bash | devscene:task-plan-reviewer | 21 | 5.8s | 0.5s |
| Bash | devscene:task-plan-writer | 3 | 0.8s | 0.3s |
| Bash | orchestrator | 75 | 2m 09s | 7.8s |
| Edit | devscene:layer-implementer | 31 | 1.2s | 0.0s |
| Edit | devscene:task-plan-writer | 4 | 0.1s | 0.0s |
| Edit | orchestrator | 7 | 0.2s | 0.0s |
| Grep | orchestrator | 2 | 0.0s | 0.0s |
| Read | devscene:architecture-reviewer | 26 | 1.9s | 0.3s |
| Read | devscene:branch-reviewer | 12 | 0.5s | 0.2s |
| Read | devscene:layer-implementer | 48 | 6.6s | 3.5s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:review-plan-reviewer | 14 | 0.7s | 0.3s |
| Read | devscene:task-plan-reviewer | 27 | 0.9s | 0.2s |
| Read | devscene:task-plan-writer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 13 | 1.1s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 6 | 0.2s | 0.0s |
| Write | devscene:task-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-19T11:58:52.162Z | 12.1s | 4434 | true | false |
| Bash | devscene:layer-implementer | 2026-11-19T12:00:13.168Z | 8.7s | 3341 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T11:46:19.177Z | 8.6s | 3305 | false | false |
| Bash | orchestrator | 2026-11-19T11:42:38.458Z | 7.8s | 982 | false | false |
| Bash | orchestrator | 2026-11-19T11:55:56.419Z | 6.7s | 793 | false | false |
| Bash | orchestrator | 2026-11-19T11:48:20.092Z | 6.7s | 757 | false | false |
| Bash | orchestrator | 2026-11-19T11:45:22.137Z | 6.6s | 762 | false | false |
| Bash | orchestrator | 2026-11-19T12:00:41.416Z | 6.6s | 765 | false | false |
| Bash | orchestrator | 2026-11-19T11:56:16.601Z | 6.4s | 603 | false | false |
| Bash | devscene:layer-implementer | 2026-11-19T12:00:23.985Z | 6.3s | 505 | false | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 9 | 45.9s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.9s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 4 | 20.2s |
| devscene:layer-implementer | npm test --workspace cli -- test/python-service.test.mjs | 3 | 29.5s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/feat_graphscene_package_skeleton_code | 4 | 22.3s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_package_skeleton_story_plan.m | 4 | 25.7s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 8 | 2.1s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen answer_1 for injection | 3.3s | 1 | 285 | 4 | 23292 | 10547 | 12741 | 0.0023 |
| devscene:task-plan-writer | Extend task plan with answer | 40.5s | 6 | 4629 | 14 | 274848 | 232930 | 41904 | 0.0273 |
| devscene:architecture-reviewer | Architecture review round 1 | 1m 10s | 11 | 7324 | 24 | 868115 | 764368 | 103723 | 0.0472 |
| devscene:task-plan-reviewer | Task plan review round 1 | 2m 49s | 29 | 17052 | 60 | 3520720 | 3364225 | 156435 | 0.1141 |
| devscene:layer-implementer | Implement Task 2 (general) | 31.8s | 6 | 2670 | 14 | 309957 | 256915 | 53028 | 0.0214 |
| devscene:layer-implementer | Implement Task 3 (general) | 1m 05s | 15 | 6299 | 32 | 804164 | 757785 | 46347 | 0.044 |
| devscene:layer-implementer | Implement Task 4 (cli) | 1m 13s | 10 | 7060 | 22 | 507969 | 462954 | 44993 | 0.0497 |
| devscene:layer-implementer | Implement Task 5 (general) | 1m 12s | 12 | 6966 | 26 | 838469 | 768735 | 69708 | 0.0488 |
| devscene:architecture-reviewer | Branch architecture review | 1m 16s | 10 | 7602 | 22 | 1020863 | 884112 | 136729 | 0.0511 |
| devscene:branch-reviewer | End-of-branch code review | 4m 10s | 39 | 26210 | 80 | 4515620 | 4360621 | 154919 | 0.168 |
| devscene:review-plan-reviewer | Meta-review code review | 50.7s | 8 | 5231 | 18 | 496811 | 399141 | 97652 | 0.0341 |
| devscene:layer-implementer | Fix code-review Finding 4 | 35.6s | 8 | 3122 | 18 | 477240 | 411865 | 65357 | 0.024 |
| devscene:layer-implementer | Fix code-review Finding 3 | 51.7s | 10 | 4165 | 22 | 633917 | 573481 | 60414 | 0.0348 |
| devscene:layer-implementer | Fix Finding 1 (cli layer) | 1m 04s | 13 | 4650 | 28 | 500862 | 472410 | 28424 | 0.0432 |
| devscene:layer-implementer | Fix Finding 1 (general layer) | 59.9s | 11 | 4501 | 24 | 417655 | 388809 | 28822 | 0.0403 |
| devscene:layer-implementer | Fix code-review Finding 2 | 51.8s | 11 | 4191 | 24 | 715751 | 655608 | 60119 | 0.0348 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | — |
| Input tokens (uncached) | — |
| Total input tokens (incl. cache) | — |
| Output tokens | — |
| Thinking tokens (main thread) | — |
| Cache read tokens | — |
| Cache write tokens | — |
| Cache write tokens, main thread (5m / 1h) | — / — |
| Cache hit ratio | — |
| Token source | not available |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 208 | 17087275 | 2360 | 16877178 | 209889 |
| sub-agents | 432 | 15926253 | 111957 | 14764506 | 1161315 |
| remainder | — | — | — | — | — |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | — |
| Sub-agents spawned / failed / killed | — / — / — |
| terminal_reason | — |
| stop_reason | — |
| Turns | — |
| Time to first token | — |
| Rate-limit peak | seven_day 0.32 |

## Session 7 — 2026-11-19T12:09:19.092Z → 2026-11-19T13:42:36.958Z

Session id: `ed526b93-caeb-4a05-a5a0-098e09f860db`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h33m | 1h33m | 16m 05s | 0.0s | 0.0s | 1h33m | 10m 29s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 237 | 1.7s | 5.4s | 24.7s | 29.1s | 0 |
| devscene:architecture-reviewer | 8 | 1.9s | 5.1s | 5.1s | 5.1s | 0 |
| devscene:layer-implementer | 18 | 1.9s | 3.4s | 8.1s | 8.1s | 0 |
| devscene:review-plan-reviewer | 7 | 3.1s | 9.1s | 9.1s | 9.1s | 0 |
| devscene:skeptic-reviewer | 37 | 2.8s | 24.6s | 26.1s | 26.1s | 0 |
| devscene:statistics-plan-writer | 7 | 1.7s | 17.1s | 17.1s | 17.1s | 0 |
| devscene:test-fix-plan-writer | 18 | 3.7s | 13.2s | 29.1s | 29.1s | 0 |
| orchestrator | 142 | 1.6s | 1.9s | 8.5s | 10.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 7 | 10m 29s | 4m 19s |
| Bash | devscene:architecture-reviewer | 5 | 0.9s | 0.2s |
| Bash | devscene:layer-implementer | 10 | 17.5s | 6.2s |
| Bash | devscene:review-plan-reviewer | 6 | 1.5s | 0.2s |
| Bash | devscene:skeptic-reviewer | 30 | 8.0s | 0.5s |
| Bash | devscene:statistics-plan-writer | 8 | 1.9s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 19 | 4.7s | 0.4s |
| Bash | orchestrator | 203 | 1h17m | 1m 04s |
| Edit | devscene:layer-implementer | 18 | 0.7s | 0.0s |
| Edit | devscene:test-fix-plan-writer | 1 | 0.0s | 0.0s |
| Edit | orchestrator | 6 | 0.2s | 0.0s |
| Read | devscene:architecture-reviewer | 11 | 0.6s | 0.3s |
| Read | devscene:layer-implementer | 18 | 1.1s | 0.3s |
| Read | devscene:review-plan-reviewer | 10 | 0.6s | 0.2s |
| Read | devscene:skeptic-reviewer | 12 | 0.6s | 0.2s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 5 | 0.0s | 0.0s |
| Read | orchestrator | 16 | 7.2s | 5.4s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-19T13:21:42.164Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T13:02:27.943Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T12:20:28.321Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T13:06:47.804Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T12:23:42.392Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T13:07:53.255Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T12:19:23.512Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T13:04:38.609Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T12:25:51.494Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-19T13:05:43.226Z | 1m 02s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 36 | 35m 51s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 38 | 38m 10s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; echo checked | 75 | 59.1s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:skeptic-reviewer | C2.1 skeptic review of branch | 4m 19s | 37 | 25672 | 76 | 3718289 | 3574030 | 144183 | 0.0463 |
| devscene:review-plan-reviewer | C2.2 meta-review skeptic index | 56.5s | 7 | 6032 | 16 | 432753 | 339961 | 92776 | 0.0101 |
| devscene:layer-implementer | C2.4 fix skeptic finding 1 | 37.7s | 6 | 3342 | 14 | 342741 | 276952 | 65775 | 0.0067 |
| devscene:test-fix-plan-writer | G.2 write test fix plan round 1 | 2m 06s | 18 | 13350 | 38 | 708107 | 660170 | 47899 | 0.0227 |
| devscene:architecture-reviewer | G.2 architecture gate on test fix plan | 37.1s | 8 | 3782 | 18 | 464919 | 373086 | 91815 | 0.0066 |
| devscene:layer-implementer | G.4 fix test-fix finding 1 | 1m 14s | 12 | 7553 | 26 | 717658 | 652125 | 65507 | 0.0133 |
| devscene:statistics-plan-writer | D.1 write branch statistics | 37.2s | 7 | 4614 | 16 | 261223 | 225126 | 36081 | 0.0067 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $12.74 |
| Cost — claude-opus-5-5 | $12.74 |
| Input tokens (uncached) | 490 |
| Total input tokens (incl. cache) | 31481191 |
| Output tokens | 103381 |
| Thinking tokens (main thread) | 2950 |
| Cache read tokens | 30710885 |
| Cache write tokens | 769816 |
| Cache write tokens, main thread (5m / 1h) | 0 / 225780 |
| Cache hit ratio | 0.9755 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 286 | 24835501 | 3108 | 24609435 | 225780 |
| sub-agents | 204 | 6645690 | 64345 | 6101450 | 544036 |
| remainder | 0 | 0 | 35928 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 5 |
| Sub-agents spawned / failed / killed | 7 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 236 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.32 |
