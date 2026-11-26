# Run analytics — feat_graphscene_run_mode

## Whole run

| Measure | Value |
|---|---|
| Sessions | 8 (0 incomplete) |
| Engine / planning node sessions | 2 / 6 |
| Span | 2h19m |
| Wall | 2h18m |
| Session wall, summed over sessions | 2h20m |
| Active | 2h16m |
| Host-suspended | 0.0s |
| Idle | 2m 05s |
| Cost | $37.67 |
| Input tokens (uncached) | 1194 |
| Total input tokens (incl. cache) | 74470797 |
| Output tokens | 318643 |
| Thinking tokens (main thread) | 52105 |
| Cache read tokens | 71790048 |
| Cache write tokens | 2679555 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1180021 |
| Cache hit ratio | 0.964 |
| Requests | 578 |
| Request latency p50 / p90 / p99 / max | 1.7s / 7.6s / 36.4s / 2m 05s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 18 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:skeptic-reviewer — Adversarial skeptic review — 5m 56s (session 8) |
| Rate-limit peak | seven_day 0.21 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 6m 06s | 6m 06s | 0.0s | 6m 07s | $2.88 |
| 3 | 2-architecture_review | 1m 12s | 1m 12s | 0.0s | 1m 12s | $1.68 |
| 4 | 3-plan_review | 2m 32s | 2m 32s | 0.0s | 2m 33s | $2.24 |
| 5 | 4-plan_writer | 26.2s | 26.2s | 0.0s | 27.2s | $0.29 |
| 6 | 5-architecture_review | 1m 00s | 1m 00s | 0.0s | 1m 00s | $1.28 |
| 7 | 6-plan_review | 3m 39s | 3m 39s | 0.0s | 3m 40s | $2.92 |

## Network refusals

8 of 8 sessions scanned.

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
| Wait (every run of task_round_1) | 39m 10s |
| Gate rows | 32 (complete) |
| Test files — full | 233 files, 19627.5 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 1 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 4 | FAIL | 2411 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 16 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 1 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 7 s |
| full | 13h | ok | 0 s |
| full | 13i | ok | 0 s |
| full | 13j | ok | 15 s |
| full | 14a | ok | 6 s |
| full | 14c | ok | 6 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 233)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/gate12-sandbox-round-full-run.test.mjs | fail | 1856.6 | 9 | 1 |
| test/planning-driver-control.test.mjs | pass | 1144.2 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 822.9 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 647.5 | 29 | 0 |
| test/remote-run.test.mjs | pass | 646.1 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 619.3 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 595.7 | 17 | 0 |
| test/doctor.test.mjs | pass | 590.8 | 1 | 0 |
| test/remote-control.test.mjs | pass | 553.7 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 531.7 | 33 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 45m 01s |
| Gate rows | 33 (complete) |
| Test files — focused | 1 files, 36.6 s summed |
| Test files — full | 233 files, 21510.0 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 4 | ok | 38 s |
| full | 1 | ok | 1 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 1 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 3 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 4 | ok | 2668 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 17 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 17 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 5 s |
| full | 13h | ok | 0 s |
| full | 13i | ok | 1 s |
| full | 13j | ok | 15 s |
| full | 14a | ok | 7 s |
| full | 14c | ok | 7 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — focused (1 of 1)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/gate12-sandbox-round-full-run.test.mjs | pass | 36.6 | 22 | 0 |

#### Slowest test files — full (10 of 233)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1327.1 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 908.0 | 21 | 0 |
| test/remote-run.test.mjs | pass | 758.0 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 725.7 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 703.9 | 27 | 0 |
| test/doctor.test.mjs | pass | 703.0 | 1 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 677.6 | 17 | 0 |
| test/remote-control.test.mjs | pass | 663.7 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 600.9 | 33 | 0 |
| test/planning-driver-walk.test.mjs | pass | 547.5 | 9 | 0 |

## Session 1 — 2026-11-26T08:05:01.831Z → 2026-11-26T08:05:51.851Z

Session id: `dd1bc9df-b8dc-4451-9f61-bdbdb49ea571`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 50.0s | 50.9s | 43.8s | 0.0s | 0.0s | 50.0s | 2.5s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.3s | 3.5s | 4.6s | 4.6s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.2s | 1.2s | 1.2s | 1.2s | 0 |
| orchestrator | 16 | 1.3s | 3.5s | 4.6s | 4.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 2.5s | 2.5s |
| Bash | orchestrator | 11 | 7.0s | 5.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:05:41.997Z | 5.1s | 579 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:04.315Z | 0.3s | 2638 | false | false |
| Read | orchestrator | 2026-11-26T08:05:32.961Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:11.147Z | 0.2s | 152 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:21.569Z | 0.2s | 151 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:31.410Z | 0.2s | 1159 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:07.979Z | 0.1s | 685 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:05.178Z | 0.1s | 2046 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:27.848Z | 0.1s | 488 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:12.512Z | 0.1s | 60 | true | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 2.5s | 1 | 236 | 4 | 29406 | 11229 | 18173 | 0.05 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.86 |
| Cost — claude-opus-5-5 | $0.86 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 945165 |
| Output tokens | 4822 |
| Thinking tokens (main thread) | 261 |
| Cache read tokens | 864696 |
| Cache write tokens | 80433 |
| Cache write tokens, main thread (5m / 1h) | 0 / 62260 |
| Cache hit ratio | 0.9149 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 915759 | 231 | 853467 | 62260 |
| sub-agents | 4 | 29406 | 236 | 11229 | 18173 |
| remainder | 0 | 0 | 4355 | 0 | 0 |

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
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.2 |

## Session 2 — 2026-11-26T08:05:54.266Z → 2026-11-26T08:12:00.395Z

Session id: `6b91a587-657f-47af-aa9e-2df2414cf2fb`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 6m 06s | 6m 07s | 6m 03s | 0.0s | 0.0s | 6m 06s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 27 | 1.6s | 36.4s | 1m 12s | 1m 12s | 0 |
| orchestrator | 27 | 1.6s | 36.4s | 1m 12s | 1m 12s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 13 | 2.8s | 0.2s |
| Read | orchestrator | 26 | 0.9s | 0.2s |
| Write | orchestrator | 5 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:06:23.231Z | 0.2s | 6961 | false | false |
| Bash | orchestrator | 2026-11-26T08:05:54.571Z | 0.2s | 52 | false | false |
| Read | orchestrator | 2026-11-26T08:05:58.371Z | 0.2s | 37356 | false | false |
| Bash | orchestrator | 2026-11-26T08:08:10.318Z | 0.2s | 1735 | false | false |
| Bash | orchestrator | 2026-11-26T08:09:54.018Z | 0.2s | 146 | false | false |
| Read | orchestrator | 2026-11-26T08:05:58.823Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T08:09:40.722Z | 0.2s | 3693 | false | false |
| Bash | orchestrator | 2026-11-26T08:08:13.039Z | 0.2s | 860 | false | false |
| Bash | orchestrator | 2026-11-26T08:07:11.724Z | 0.2s | 2953 | false | false |
| Bash | orchestrator | 2026-11-26T08:06:26.523Z | 0.1s | 1904 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.88 |
| Cost — claude-opus-5-5 | $2.88 |
| Input tokens (uncached) | 54 |
| Total input tokens (incl. cache) | 3253685 |
| Output tokens | 40418 |
| Thinking tokens (main thread) | 20928 |
| Cache read tokens | 3071761 |
| Cache write tokens | 181870 |
| Cache write tokens, main thread (5m / 1h) | 0 / 181870 |
| Cache hit ratio | 0.9441 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 54 | 3253685 | 242 | 3071761 | 181870 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 40176 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 45 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.2 |

## Session 3 — 2026-11-26T08:12:03.706Z → 2026-11-26T08:13:15.749Z

Session id: `0ee4b532-5dd9-4ba8-9110-b98ac9ee2b31`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 12s | 1m 12s | 1m 11s | 0.0s | 0.0s | 1m 12s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 1.7s | 6.2s | 17.4s | 17.4s | 0 |
| orchestrator | 13 | 1.7s | 6.2s | 17.4s | 17.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 6 | 1.1s | 0.2s |
| Read | orchestrator | 19 | 0.9s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-26T08:12:15.761Z | 0.2s | 37356 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:04.076Z | 0.2s | 52 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:54.811Z | 0.2s | 2437 | false | false |
| Read | orchestrator | 2026-11-26T08:12:21.016Z | 0.2s | 63338 | false | false |
| Read | orchestrator | 2026-11-26T08:12:17.804Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:06.873Z | 0.2s | 25155 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:35.701Z | 0.2s | 7723 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:31.348Z | 0.1s | 1282 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:13.985Z | 0.0s | 727 | true | true |
| Read | orchestrator | 2026-11-26T08:12:08.214Z | 0.0s | 9488 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.68 |
| Cost — claude-opus-5-5 | $1.68 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1196252 |
| Output tokens | 8307 |
| Thinking tokens (main thread) | 2952 |
| Cache read tokens | 1033059 |
| Cache write tokens | 163167 |
| Cache write tokens, main thread (5m / 1h) | 0 / 163167 |
| Cache hit ratio | 0.8636 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1196252 | 825 | 1033059 | 163167 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7482 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 27 |
| Time to first token | 0.8s |
| Rate-limit peak | seven_day 0.2 |

## Session 4 — 2026-11-26T08:12:03.666Z → 2026-11-26T08:14:35.980Z

Session id: `598cce67-f247-4366-afc9-21178f4f4430`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 32s | 2m 33s | 2m 28s | 0.0s | 0.0s | 2m 32s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 29 | 2.5s | 9.1s | 16.6s | 16.6s | 0 |
| orchestrator | 29 | 2.5s | 9.1s | 16.6s | 16.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 24 | 5.2s | 0.5s |
| Read | orchestrator | 16 | 0.9s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:13:25.746Z | 0.5s | 2200 | false | false |
| Bash | orchestrator | 2026-11-26T08:13:28.822Z | 0.4s | 9524 | false | false |
| Bash | orchestrator | 2026-11-26T08:13:20.521Z | 0.3s | 3746 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:03.984Z | 0.2s | 52 | false | false |
| Read | orchestrator | 2026-11-26T08:12:19.095Z | 0.2s | 37356 | false | false |
| Bash | orchestrator | 2026-11-26T08:13:32.875Z | 0.2s | 7614 | false | false |
| Bash | orchestrator | 2026-11-26T08:12:31.765Z | 0.2s | 5537 | false | false |
| Bash | orchestrator | 2026-11-26T08:13:55.984Z | 0.2s | 3664 | false | false |
| Read | orchestrator | 2026-11-26T08:12:25.363Z | 0.2s | 35050 | false | false |
| Read | orchestrator | 2026-11-26T08:12:22.181Z | 0.2s | 63403 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.24 |
| Cost — claude-opus-5-5 | $2.24 |
| Input tokens (uncached) | 58 |
| Total input tokens (incl. cache) | 3385715 |
| Output tokens | 16107 |
| Thinking tokens (main thread) | 8191 |
| Cache read tokens | 3226156 |
| Cache write tokens | 159501 |
| Cache write tokens, main thread (5m / 1h) | 0 / 159501 |
| Cache hit ratio | 0.9529 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 58 | 3385715 | 260 | 3226156 | 159501 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 15847 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 42 |
| Time to first token | 0.8s |
| Rate-limit peak | seven_day 0.2 |

## Session 5 — 2026-11-26T08:14:45.786Z → 2026-11-26T08:15:12.063Z

Session id: `8326e5ba-663c-4065-9d66-02a4810f870d`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 26.2s | 27.2s | 26.6s | 0.0s | 0.0s | 26.2s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 7 | 1.3s | 7.6s | 7.6s | 7.6s | 0 |
| orchestrator | 7 | 1.3s | 7.6s | 7.6s | 7.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 2 | 0.4s | 0.3s |
| Edit | orchestrator | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:14:46.194Z | 0.3s | 52 | false | false |
| Bash | orchestrator | 2026-11-26T08:14:52.305Z | 0.1s | 232 | false | false |
| Edit | orchestrator | 2026-11-26T08:15:02.931Z | 0.0s | 224 | false | false |
| Write | orchestrator | 2026-11-26T08:15:04.335Z | 0.0s | 227 | false | false |
| Read | orchestrator | 2026-11-26T08:14:47.718Z | 0.0s | 3640 | false | false |
| Edit | orchestrator | 2026-11-26T08:14:58.908Z | 0.0s | 224 | false | false |
| Read | orchestrator | 2026-11-26T08:14:48.966Z | 0.0s | 9488 | false | false |
| Read | orchestrator | 2026-11-26T08:14:48.366Z | 0.0s | 2127 | false | false |
| Read | orchestrator | 2026-11-26T08:14:50.322Z | 0.0s | 5584 | false | false |
| Read | orchestrator | 2026-11-26T08:14:50.728Z | 0.0s | 9663 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.29 |
| Cost — claude-opus-5-5 | $0.29 |
| Input tokens (uncached) | 14 |
| Total input tokens (incl. cache) | 217761 |
| Output tokens | 3231 |
| Thinking tokens (main thread) | 177 |
| Cache read tokens | 194066 |
| Cache write tokens | 23681 |
| Cache write tokens, main thread (5m / 1h) | 0 / 23681 |
| Cache hit ratio | 0.8912 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 14 | 217761 | 734 | 194066 | 23681 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 2497 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 11 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.2 |

## Session 6 — 2026-11-26T08:15:13.964Z → 2026-11-26T08:16:13.994Z

Session id: `bfcd1505-6e8d-4515-bdd3-3dfa28139c5f`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 00s | 1m 00s | 59.4s | 0.0s | 0.0s | 1m 00s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 1.3s | 7.1s | 13.4s | 13.4s | 0 |
| orchestrator | 13 | 1.3s | 7.1s | 13.4s | 13.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 1.9s | 0.2s |
| Read | orchestrator | 18 | 0.7s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:15:14.420Z | 0.2s | 52 | false | false |
| Read | orchestrator | 2026-11-26T08:15:25.753Z | 0.2s | 37356 | false | false |
| Read | orchestrator | 2026-11-26T08:15:26.252Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:59.410Z | 0.2s | 2193 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:31.734Z | 0.1s | 1127 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:29.431Z | 0.1s | 11790 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:53.680Z | 0.1s | 7501 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:52.326Z | 0.1s | 3299 | false | false |
| Bash | orchestrator | 2026-11-26T08:16:01.378Z | 0.1s | 225 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:15.267Z | 0.1s | 8547 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.28 |
| Cost — claude-opus-5-5 | $1.28 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 1207875 |
| Output tokens | 6846 |
| Thinking tokens (main thread) | 2049 |
| Cache read tokens | 1091943 |
| Cache write tokens | 115906 |
| Cache write tokens, main thread (5m / 1h) | 0 / 115906 |
| Cache hit ratio | 0.904 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 1207875 | 901 | 1091943 | 115906 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 5945 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 31 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.2 |

## Session 7 — 2026-11-26T08:15:14.146Z → 2026-11-26T08:18:53.632Z

Session id: `cef2bee8-aa66-4b9a-9a39-b16921f45143`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 3m 39s | 3m 40s | 3m 36s | 0.0s | 0.0s | 3m 39s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 24 | 4.5s | 24.7s | 43.4s | 43.4s | 0 |
| orchestrator | 24 | 4.5s | 24.7s | 43.4s | 43.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 18 | 3.7s | 0.4s |
| Read | orchestrator | 26 | 1.2s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T08:17:10.140Z | 0.4s | 2376 | false | false |
| Bash | orchestrator | 2026-11-26T08:16:24.088Z | 0.3s | 2882 | false | false |
| Read | orchestrator | 2026-11-26T08:15:27.458Z | 0.2s | 37356 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:14.487Z | 0.2s | 52 | false | false |
| Read | orchestrator | 2026-11-26T08:15:27.959Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T08:15:46.520Z | 0.2s | 2150 | false | false |
| Bash | orchestrator | 2026-11-26T08:17:55.803Z | 0.2s | 14426 | false | false |
| Read | orchestrator | 2026-11-26T08:15:32.191Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-26T08:17:05.600Z | 0.2s | 10528 | false | false |
| Read | orchestrator | 2026-11-26T08:15:35.742Z | 0.2s | 30778 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.92 |
| Cost — claude-opus-5-5 | $2.92 |
| Input tokens (uncached) | 48 |
| Total input tokens (incl. cache) | 3884612 |
| Output tokens | 23755 |
| Thinking tokens (main thread) | 15665 |
| Cache read tokens | 3670804 |
| Cache write tokens | 213760 |
| Cache write tokens, main thread (5m / 1h) | 0 / 213760 |
| Cache hit ratio | 0.945 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 48 | 3884612 | 878 | 3670804 | 213760 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 22877 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 46 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.2 |

## Session 8 — 2026-11-26T08:19:51.400Z → 2026-11-26T10:24:52.484Z

Session id: `b4235ca2-e846-414e-945c-f7815c5e80e6`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2h05m | 2h05m | 34m 11s | 0.0s | 2m 05s | 2h02m | 29m 30s | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-26T08:44:00.362Z | 2m 05s | devscene:skeptic-reviewer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 448 | 1.7s | 7.0s | 26.9s | 2m 05s | 1 |
| devscene:architecture-reviewer | 32 | 2.0s | 5.0s | 10.3s | 10.3s | 0 |
| devscene:branch-reviewer | 39 | 3.1s | 13.4s | 32.0s | 32.0s | 0 |
| devscene:layer-implementer | 112 | 2.1s | 7.8s | 29.4s | 38.2s | 0 |
| devscene:review-plan-reviewer | 23 | 2.5s | 6.8s | 9.7s | 9.7s | 0 |
| devscene:skeptic-reviewer | 32 | 4.0s | 18.6s | 2m 05s | 2m 05s | 1 |
| devscene:statistics-plan-writer | 7 | 1.9s | 16.2s | 16.2s | 16.2s | 0 |
| devscene:test-fix-plan-writer | 25 | 2.0s | 9.7s | 15.2s | 15.2s | 0 |
| orchestrator | 178 | 1.4s | 2.0s | 4.9s | 7.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 18 | 29m 30s | 5m 56s |
| Bash | devscene:architecture-reviewer | 21 | 3.5s | 0.2s |
| Bash | devscene:branch-reviewer | 30 | 6.6s | 0.6s |
| Bash | devscene:layer-implementer | 112 | 2m 37s | 33.9s |
| Bash | devscene:review-plan-reviewer | 18 | 2.8s | 0.2s |
| Bash | devscene:skeptic-reviewer | 20 | 5.3s | 2.4s |
| Bash | devscene:statistics-plan-writer | 7 | 1.2s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 20 | 3.1s | 0.2s |
| Bash | orchestrator | 253 | 1h29m | 1m 05s |
| Edit | devscene:layer-implementer | 42 | 1.7s | 0.0s |
| Edit | devscene:test-fix-plan-writer | 1 | 0.0s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Read | devscene:architecture-reviewer | 42 | 1.5s | 0.6s |
| Read | devscene:branch-reviewer | 16 | 0.3s | 0.2s |
| Read | devscene:layer-implementer | 33 | 0.5s | 0.2s |
| Read | devscene:review-plan-reviewer | 26 | 0.4s | 0.0s |
| Read | devscene:skeptic-reviewer | 21 | 0.3s | 0.0s |
| Read | devscene:statistics-plan-writer | 2 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 10 | 0.4s | 0.2s |
| Read | orchestrator | 10 | 1.9s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 5 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 3 | 0.1s | 0.0s |
| Write | devscene:skeptic-reviewer | 4 | 0.2s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T09:12:17.460Z | 1m 05s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:40:35.999Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:41:42.126Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:39:30.049Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:45:57.770Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:47:03.585Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T08:56:25.129Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:38:24.588Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T08:55:20.356Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T09:52:21.834Z | 1m 02s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:architecture-reviewer | git rev-parse --show-toplevel | 3 | 0.4s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/engine/test_run_loop.py | 5 | 4.3s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_layers.py | 5 | 11.3s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 10 | 56.1s |
| devscene:layer-implementer | git diff --name-only HEAD | 3 | 0.8s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 3 | 0.4s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 8 | 1.1s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 39 | 39m 10s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 45 | 45m 01s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 10 | 1.7s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; echo checked | 84 | 1m 11s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 1m 27s | 14 | 8075 | 30 | 765280 | 709964 | 55286 | 0.0117 |
| devscene:layer-implementer | Implement Task 2 graphscene | 2m 35s | 16 | 17439 | 34 | 1076599 | 1014320 | 62245 | 0.0207 |
| devscene:layer-implementer | Implement Task 3 graphscene | 2m 51s | 21 | 18369 | 44 | 1799396 | 1708548 | 90804 | 0.0229 |
| devscene:layer-implementer | Implement Task 4 graphscene | 1m 48s | 21 | 10883 | 44 | 1454582 | 1388184 | 66354 | 0.0144 |
| devscene:architecture-reviewer | Architecture review of branch | 45.6s | 9 | 4960 | 20 | 960601 | 822668 | 137913 | 0.0061 |
| devscene:branch-reviewer | End-of-branch code review | 4m 14s | 39 | 25983 | 80 | 5247762 | 5067654 | 180028 | 0.034 |
| devscene:review-plan-reviewer | Meta-review the code review | 57.0s | 11 | 6185 | 24 | 793991 | 690713 | 103254 | 0.0076 |
| devscene:layer-implementer | Fix code-review Finding 1 | 51.9s | 11 | 3795 | 24 | 528668 | 482621 | 46023 | 0.0069 |
| devscene:layer-implementer | Fix code-review Finding 2 | 47.5s | 9 | 4718 | 20 | 452117 | 414911 | 37186 | 0.0063 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 5m 56s | 32 | 25823 | 66 | 2616391 | 2497950 | 118375 | 0.0475 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 59.1s | 12 | 5895 | 26 | 1010964 | 896199 | 114739 | 0.0079 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 44.2s | 10 | 4288 | 22 | 513884 | 463858 | 50004 | 0.0059 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 1m 32s | 19 | 10111 | 40 | 1488640 | 1396859 | 91741 | 0.0123 |
| devscene:architecture-reviewer | Architecture gate test fix plan | 1m 01s | 13 | 6986 | 28 | 1386454 | 1254459 | 131967 | 0.0082 |
| devscene:test-fix-plan-writer | Revise test fix plan per arch | 21.4s | 6 | 2358 | 14 | 169403 | 150279 | 19110 | 0.0029 |
| devscene:architecture-reviewer | Re-run arch gate test fix plan | 46.4s | 10 | 5200 | 22 | 826409 | 711336 | 115051 | 0.0062 |
| devscene:layer-implementer | Fix test-fix Finding 1 (cli) | 1m 12s | 10 | 3580 | 22 | 341221 | 309275 | 31924 | 0.0096 |
| devscene:statistics-plan-writer | Write branch statistics | 37.1s | 7 | 4625 | 16 | 223791 | 194418 | 29357 | 0.005 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $25.52 |
| Cost — claude-opus-5-5 | $25.52 |
| Input tokens (uncached) | 932 |
| Total input tokens (incl. cache) | 60379732 |
| Output tokens | 215157 |
| Thinking tokens (main thread) | 1882 |
| Cache read tokens | 58637563 |
| Cache write tokens | 1741237 |
| Cache write tokens, main thread (5m / 1h) | 0 / 259876 |
| Cache hit ratio | 0.9711 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 356 | 38723579 | 4281 | 38463347 | 259876 |
| sub-agents | 576 | 21656153 | 169273 | 20174216 | 1481361 |
| remainder | 0 | 0 | 41603 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 16 |
| Sub-agents spawned / failed / killed | 18 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 296 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.21 |
