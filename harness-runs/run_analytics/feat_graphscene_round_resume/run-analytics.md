# Run analytics — feat_graphscene_round_resume

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 2h08m |
| Wall | 2h07m |
| Session wall, summed over sessions | 2h08m |
| Active | 2h07m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $25.51 |
| Input tokens (uncached) | 862 |
| Total input tokens (incl. cache) | 53728578 |
| Output tokens | 200879 |
| Thinking tokens (main thread) | 26194 |
| Cache read tokens | 51953934 |
| Cache write tokens | 1773782 |
| Cache write tokens, main thread (5m / 1h) | 0 / 743137 |
| Cache hit ratio | 0.967 |
| Requests | 416 |
| Request latency p50 / p90 / p99 / max | 3.8s / 7.5s / 23.1s / 47.5s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 14 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — End-of-branch code review — 2m 57s (session 5) |
| Rate-limit peak | seven_day 0.51 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 5m 50s | 5m 50s | 0.0s | 5m 53s | $2.35 |
| 3 | 2-architecture_review | 53.3s | 53.3s | 0.0s | 57.9s | $1.29 |
| 4 | 3-plan_review | 3m 01s | 3m 01s | 0.0s | 3m 06s | $1.78 |

## Network refusals

5 of 5 sessions scanned.

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
| Wait (every run of task_round_1) | 39m 31s |
| Gate rows | 34 (complete) |
| Test files — full | 223 files, 20161.2 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 1 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 1 s |
| full | 3f | ok | 1 s |
| full | 3g | ok | 1 s |
| full | 3h | ok | 1 s |
| full | 3i | ok | 1 s |
| full | 4 | ok | 2540 s |
| full | 6a | FAIL | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 20 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 20 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 6 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 223)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1260.7 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 929.7 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 714.6 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 713.9 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 699.5 | 17 | 0 |
| test/remote-run.test.mjs | pass | 695.0 | 130 | 0 |
| test/remote-control.test.mjs | pass | 634.3 | 83 | 0 |
| test/doctor.test.mjs | pass | 624.6 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 611.0 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 566.6 | 21 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 41m 02s |
| Gate rows | 34 (complete) |
| Test files — full | 223 files, 20243.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 6a | ok | 1 s |
| full | 1 | ok | 0 s |
| full | 2a | ok | 4 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 1 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 3 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2546 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 18 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 0 s |
| full | 13c | ok | 15 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 7 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 223)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1277.0 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 929.1 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 726.0 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 722.2 | 27 | 0 |
| test/remote-run.test.mjs | pass | 710.9 | 130 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 709.6 | 17 | 0 |
| test/remote-control.test.mjs | pass | 642.9 | 83 | 0 |
| test/doctor.test.mjs | pass | 625.1 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 615.4 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 563.4 | 21 | 0 |

## Session 1 — 2026-11-22T15:28:34.227Z → 2026-11-22T15:30:24.353Z

Session id: `d039a21f-a56e-401a-81ac-c32e3c5b8b90`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 50s | 1m 55s | 1m 46s | 0.0s | 0.0s | 1m 50s | 6.5s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 20 | 4.7s | 5.7s | 6.7s | 6.7s | 0 |
| devscene:prompt-injection-reviewer | 1 | 4.4s | 4.4s | 4.4s | 4.4s | 0 |
| orchestrator | 19 | 4.7s | 5.7s | 6.7s | 6.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 6.5s | 6.5s |
| Bash | orchestrator | 13 | 9.3s | 5.8s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T15:30:11.785Z | 5.8s | 595 | false | false |
| Bash | orchestrator | 2026-11-22T15:28:40.353Z | 0.4s | 2106 | false | false |
| Bash | orchestrator | 2026-11-22T15:29:20.504Z | 0.4s | 155 | false | false |
| Bash | orchestrator | 2026-11-22T15:28:54.894Z | 0.4s | 156 | false | false |
| Bash | orchestrator | 2026-11-22T15:29:39.938Z | 0.3s | 1511 | false | false |
| Bash | orchestrator | 2026-11-22T15:28:47.442Z | 0.3s | 246 | false | false |
| Bash | orchestrator | 2026-11-22T15:28:57.527Z | 0.2s | 60 | true | false |
| Bash | orchestrator | 2026-11-22T15:29:30.218Z | 0.2s | 488 | false | false |
| Bash | orchestrator | 2026-11-22T15:29:55.270Z | 0.2s | 214 | false | false |
| Bash | orchestrator | 2026-11-22T15:29:24.111Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 6.5s | 1 | 245 | 4 | 29147 | 11205 | 17938 | 0.0592 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.90 |
| Cost — claude-opus-5-5 | $0.90 |
| Input tokens (uncached) | 44 |
| Total input tokens (incl. cache) | 1136910 |
| Output tokens | 5239 |
| Thinking tokens (main thread) | 383 |
| Cache read tokens | 1056764 |
| Cache write tokens | 80102 |
| Cache write tokens, main thread (5m / 1h) | 0 / 62164 |
| Cache hit ratio | 0.9295 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 40 | 1107763 | 294 | 1045559 | 62164 |
| sub-agents | 4 | 29147 | 245 | 11205 | 17938 |
| remainder | 0 | 0 | 4700 | 0 | 0 |

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
| Time to first token | 5.3s |
| Rate-limit peak | seven_day 0.5 |

## Session 2 — 2026-11-22T15:30:29.134Z → 2026-11-22T15:36:19.669Z

Session id: `483bf499-a181-44ff-adbf-24b3fb11d26e`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 50s | 5m 53s | 5m 49s | 0.0s | 0.0s | 5m 50s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 23 | 5.5s | 18.0s | 47.5s | 47.5s | 0 |
| orchestrator | 23 | 5.5s | 18.0s | 47.5s | 47.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 14 | 4.8s | 0.5s |
| Read | orchestrator | 19 | 0.8s | 0.2s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T15:33:33.531Z | 0.5s | 566 | false | false |
| Bash | orchestrator | 2026-11-22T15:32:28.115Z | 0.5s | 8606 | false | false |
| Bash | orchestrator | 2026-11-22T15:30:29.138Z | 0.4s | 56 | false | false |
| Bash | orchestrator | 2026-11-22T15:32:18.881Z | 0.3s | 10935 | false | false |
| Bash | orchestrator | 2026-11-22T15:32:41.259Z | 0.3s | 14998 | false | false |
| Bash | orchestrator | 2026-11-22T15:33:22.119Z | 0.3s | 725 | false | false |
| Bash | orchestrator | 2026-11-22T15:33:11.208Z | 0.3s | 826 | false | false |
| Bash | orchestrator | 2026-11-22T15:30:51.222Z | 0.3s | 2954 | false | false |
| Bash | orchestrator | 2026-11-22T15:32:35.355Z | 0.3s | 1917 | false | false |
| Bash | orchestrator | 2026-11-22T15:30:50.307Z | 0.3s | 15067 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.35 |
| Cost — claude-opus-5-5 | $2.35 |
| Input tokens (uncached) | 46 |
| Total input tokens (incl. cache) | 2485316 |
| Output tokens | 30969 |
| Thinking tokens (main thread) | 11485 |
| Cache read tokens | 2326927 |
| Cache write tokens | 158343 |
| Cache write tokens, main thread (5m / 1h) | 0 / 158343 |
| Cache hit ratio | 0.9363 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 46 | 2485316 | 217 | 2326927 | 158343 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 30752 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 40 |
| Time to first token | 2.9s |
| Rate-limit peak | seven_day 0.5 |

## Session 3 — 2026-11-22T15:36:26.342Z → 2026-11-22T15:37:19.738Z

Session id: `72e069f5-c813-49e5-b675-abacc4ed4a60`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 53.3s | 57.9s | 56.1s | 0.0s | 0.0s | 53.3s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 10 | 4.4s | 6.8s | 6.8s | 6.8s | 0 |
| orchestrator | 10 | 4.4s | 6.8s | 6.8s | 6.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 1.7s | 0.3s |
| Read | orchestrator | 17 | 0.9s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T15:36:26.346Z | 0.3s | 56 | false | false |
| Bash | orchestrator | 2026-11-22T15:37:03.340Z | 0.3s | 3778 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:31.135Z | 0.3s | 7268 | true | false |
| Read | orchestrator | 2026-11-22T15:36:35.407Z | 0.2s | 31957 | false | false |
| Bash | orchestrator | 2026-11-22T15:37:10.948Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:52.263Z | 0.2s | 5070 | false | false |
| Read | orchestrator | 2026-11-22T15:36:35.903Z | 0.2s | 60702 | false | false |
| Read | orchestrator | 2026-11-22T15:36:47.703Z | 0.2s | 63338 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:42.706Z | 0.1s | 727 | true | true |
| Read | orchestrator | 2026-11-22T15:36:36.803Z | 0.0s | 9663 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.29 |
| Cost — claude-opus-5-5 | $1.29 |
| Input tokens (uncached) | 20 |
| Total input tokens (incl. cache) | 862638 |
| Output tokens | 5085 |
| Thinking tokens (main thread) | 1403 |
| Cache read tokens | 732050 |
| Cache write tokens | 130568 |
| Cache write tokens, main thread (5m / 1h) | 0 / 130568 |
| Cache hit ratio | 0.8486 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 20 | 862638 | 825 | 732050 | 130568 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 4260 | 0 | 0 |

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
| Time to first token | 4.5s |
| Rate-limit peak | seven_day 0.5 |

## Session 4 — 2026-11-22T15:36:26.219Z → 2026-11-22T15:39:27.991Z

Session id: `674f51c1-10df-4992-9a8b-67f4ca40bfc2`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 01s | 3m 06s | 2m 59s | 0.0s | 0.0s | 3m 01s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 31 | 2.2s | 12.7s | 20.5s | 20.5s | 0 |
| orchestrator | 31 | 2.2s | 12.7s | 20.5s | 20.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 21 | 6.5s | 0.5s |
| Read | orchestrator | 21 | 0.5s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T15:38:04.657Z | 0.5s | 284 | false | false |
| Bash | orchestrator | 2026-11-22T15:38:11.200Z | 0.4s | 2249 | false | false |
| Bash | orchestrator | 2026-11-22T15:37:59.900Z | 0.4s | 1546 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:26.719Z | 0.4s | 56 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:36.782Z | 0.3s | 16140 | false | false |
| Bash | orchestrator | 2026-11-22T15:38:46.738Z | 0.3s | 485 | false | false |
| Bash | orchestrator | 2026-11-22T15:36:32.019Z | 0.3s | 10039 | true | false |
| Bash | orchestrator | 2026-11-22T15:38:07.270Z | 0.3s | 6592 | false | false |
| Bash | orchestrator | 2026-11-22T15:38:33.828Z | 0.3s | 1049 | false | false |
| Bash | orchestrator | 2026-11-22T15:37:21.904Z | 0.3s | 2242 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.78 |
| Cost — claude-opus-5-5 | $1.78 |
| Input tokens (uncached) | 62 |
| Total input tokens (incl. cache) | 2509801 |
| Output tokens | 17697 |
| Thinking tokens (main thread) | 9609 |
| Cache read tokens | 2391490 |
| Cache write tokens | 118249 |
| Cache write tokens, main thread (5m / 1h) | 0 / 118249 |
| Cache hit ratio | 0.9529 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 62 | 2509801 | 960 | 2391490 | 118249 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 16737 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 44 |
| Time to first token | 4.4s |
| Rate-limit peak | seven_day 0.5 |

## Session 5 — 2026-11-22T15:40:01.208Z → 2026-11-22T17:37:18.077Z

Session id: `68636ae9-16c0-4f90-87b8-486371718c4f`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h57m | 1h57m | 30m 58s | 0.0s | 0.0s | 1h57m | 20m 55s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 332 | 3.6s | 6.7s | 21.6s | 25.6s | 0 |
| devscene:architecture-reviewer | 15 | 4.7s | 6.8s | 8.7s | 8.7s | 0 |
| devscene:branch-reviewer | 21 | 5.1s | 16.1s | 23.1s | 23.1s | 0 |
| devscene:layer-implementer | 79 | 3.0s | 7.5s | 19.6s | 19.6s | 0 |
| devscene:review-plan-reviewer | 17 | 4.4s | 5.4s | 18.8s | 18.8s | 0 |
| devscene:skeptic-reviewer | 18 | 4.0s | 24.7s | 25.6s | 25.6s | 0 |
| devscene:statistics-plan-writer | 5 | 4.6s | 18.0s | 18.0s | 18.0s | 0 |
| devscene:test-fix-plan-writer | 9 | 4.1s | 12.9s | 12.9s | 12.9s | 0 |
| orchestrator | 168 | 3.2s | 5.3s | 12.1s | 13.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 13 | 20m 55s | 2m 57s |
| Bash | devscene:architecture-reviewer | 12 | 3.3s | 0.3s |
| Bash | devscene:branch-reviewer | 19 | 7.5s | 1.5s |
| Bash | devscene:layer-implementer | 59 | 2m 21s | 22.4s |
| Bash | devscene:review-plan-reviewer | 14 | 3.7s | 0.3s |
| Bash | devscene:skeptic-reviewer | 14 | 4.0s | 0.4s |
| Bash | devscene:statistics-plan-writer | 7 | 1.6s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 7 | 1.8s | 0.3s |
| Bash | orchestrator | 237 | 1h25m | 1m 06s |
| Edit | devscene:layer-implementer | 36 | 1.4s | 0.0s |
| Edit | devscene:test-fix-plan-writer | 1 | 0.0s | 0.0s |
| Edit | orchestrator | 13 | 0.5s | 0.0s |
| Read | devscene:architecture-reviewer | 21 | 1.9s | 0.2s |
| Read | devscene:branch-reviewer | 9 | 0.5s | 0.2s |
| Read | devscene:layer-implementer | 39 | 4.2s | 1.8s |
| Read | devscene:review-plan-reviewer | 12 | 0.9s | 0.3s |
| Read | devscene:skeptic-reviewer | 5 | 0.3s | 0.2s |
| Read | devscene:statistics-plan-writer | 4 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 5 | 0.0s | 0.0s |
| Read | orchestrator | 9 | 2.0s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-22T16:54:46.334Z | 1m 06s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:07:16.089Z | 1m 06s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:04:55.069Z | 1m 05s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:52:27.997Z | 1m 05s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:59:16.307Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:58:08.771Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:10:39.564Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:06:06.733Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:53:38.488Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-22T16:26:15.990Z | 1m 03s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_layers.py | 4 | 18.1s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 6 | 1m 08s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 6 | 1.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_round_resume_story_plan.md -- | 5 | 32.9s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 39 | 39m 31s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 40 | 41m 02s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; echo checked | 78 | 1m 15s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 8 | 2.0s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 1m 17s | 11 | 5517 | 24 | 525050 | 472709 | 52317 | 0.011 |
| devscene:layer-implementer | Implement Task 2 graphscene | 2m 05s | 16 | 12672 | 34 | 892047 | 837912 | 54101 | 0.0178 |
| devscene:layer-implementer | Implement Task 3 graphscene | 1m 55s | 13 | 11369 | 28 | 766209 | 710881 | 55300 | 0.0165 |
| devscene:layer-implementer | Implement Task 4 graphscene | 2m 00s | 18 | 8905 | 38 | 1054265 | 998975 | 55252 | 0.0171 |
| devscene:layer-implementer | Implement Task 5 general | 1m 24s | 12 | 4969 | 26 | 939890 | 853526 | 86338 | 0.012 |
| devscene:architecture-reviewer | Architecture review of branch | 55.2s | 8 | 3902 | 18 | 708364 | 594005 | 114341 | 0.0079 |
| devscene:branch-reviewer | End-of-branch code review | 2m 57s | 21 | 12806 | 44 | 2087771 | 1960110 | 127617 | 0.0252 |
| devscene:review-plan-reviewer | Meta-review the code review | 1m 46s | 17 | 7219 | 36 | 1074638 | 936779 | 137823 | 0.0151 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 2m 55s | 18 | 11745 | 38 | 1069510 | 984127 | 85345 | 0.0249 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 1m 12s | 9 | 6116 | 20 | 332925 | 293244 | 39661 | 0.0103 |
| devscene:architecture-reviewer | Architecture gate on test fix plan | 49.9s | 7 | 3756 | 16 | 401095 | 286921 | 114158 | 0.0071 |
| devscene:layer-implementer | Fix test-fix Finding 1 | 50.0s | 9 | 3323 | 20 | 457503 | 407053 | 50430 | 0.0071 |
| devscene:statistics-plan-writer | Write branch statistics | 45.3s | 5 | 4546 | 12 | 211434 | 171398 | 40024 | 0.0064 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $19.18 |
| Cost — claude-opus-5-5 | $19.18 |
| Input tokens (uncached) | 690 |
| Total input tokens (incl. cache) | 46733913 |
| Output tokens | 141889 |
| Thinking tokens (main thread) | 3314 |
| Cache read tokens | 45446703 |
| Cache write tokens | 1286520 |
| Cache write tokens, main thread (5m / 1h) | 0 / 273813 |
| Cache hit ratio | 0.9725 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 336 | 36213212 | 3885 | 35939063 | 273813 |
| sub-agents | 354 | 10520701 | 96845 | 9507640 | 1012707 |
| remainder | 0 | 0 | 41159 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 9 |
| Sub-agents spawned / failed / killed | 13 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 275 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.51 |
