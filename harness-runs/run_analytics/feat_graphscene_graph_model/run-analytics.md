# Run analytics — feat_graphscene_graph_model

## Whole run

| Measure | Value |
|---|---|
| Sessions | 6 (0 incomplete) |
| Engine / planning node sessions | 3 / 3 |
| Span | 18h41m |
| Wall | 3h01m |
| Session wall, summed over sessions | 3h03m |
| Active | 3h01m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $41.33 |
| Input tokens (uncached) | 1430 |
| Total input tokens (incl. cache) | 90939657 |
| Output tokens | 354620 |
| Thinking tokens (main thread) | 47254 |
| Cache read tokens | 88268166 |
| Cache write tokens | 2670061 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1075347 |
| Cache hit ratio | 0.9706 |
| Requests | 686 |
| Request latency p50 / p90 / p99 / max | 1.9s / 6.3s / 36.0s / 1m 37s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 26 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:skeptic-reviewer — Adversarial skeptic review — 4m 39s (session 5) |
| Rate-limit peak | seven_day 0.4 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 7m 50s | 7m 50s | 0.0s | 7m 52s | $3.31 |
| 3 | 2-architecture_review | 1m 32s | 1m 32s | 0.0s | 1m 34s | $1.40 |
| 4 | 3-plan_review | 2m 52s | 2m 52s | 0.0s | 2m 54s | $1.89 |

## Network refusals

6 of 6 sessions scanned.

No refused network call.

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No possible network attempt in 3 round logs.

## Gate rounds

Wait is the orchestrator's wait on `run-test-suite.sh --wait <label>`, summed over every polling row whose command ends in that label; — when none matches, as for a label waited on fewer than three times in a session (no polling row is written for it) or a command cut at 160 characters.

A phase's test-file total sums each file's own seconds, so it exceeds the gate's wall time when files run in parallel.

### Round task_round_1 — fail

| Measure | Value |
|---|---|
| Wait (every run of task_round_1) | 41m 33s |
| Gate rows | 34 (complete) |
| Test files — full | 222 files, 19836.3 s summed |

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
| full | 3e | ok | 0 s |
| full | 3f | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2497 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 20 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 7 s |
| full | 13c | ok | 18 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | FAIL | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 1 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1251.3 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 935.6 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 739.8 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 737.4 | 27 | 0 |
| test/remote-run.test.mjs | pass | 721.6 | 130 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 719.7 | 17 | 0 |
| test/remote-control.test.mjs | pass | 635.9 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 607.0 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 577.6 | 21 | 0 |
| test/doctor.test.mjs | pass | 575.5 | 1 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 41m 51s |
| Gate rows | 34 (complete) |
| Test files — full | 222 files, 20116.3 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 13e | ok | 0 s |
| full | 1 | ok | 1 s |
| full | 2a | ok | 4 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 1 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 2 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2527 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 4 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 17 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 0 s |
| full | 13c | ok | 17 s |
| full | 13d | SKIPPED | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 1 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1246.2 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 934.0 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 739.1 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 738.1 | 27 | 0 |
| test/remote-run.test.mjs | pass | 723.6 | 130 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 718.0 | 17 | 0 |
| test/remote-control.test.mjs | pass | 640.4 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 614.0 | 33 | 0 |
| test/doctor.test.mjs | pass | 591.8 | 1 | 0 |
| test/watcher-run-profile.test.mjs | pass | 573.2 | 21 | 0 |

### Round review_1_round_1 — pass

| Measure | Value |
|---|---|
| Wait (every run of review_1_round_1) | 33m 59s |
| Gate rows | 34 (complete) |
| Test files — full | 222 files, 17525.2 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 4 s |
| full | 2b | ok | 0 s |
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
| full | 3h | ok | 1 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2211 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 17 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 0 s |
| full | 13c | ok | 13 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 1 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1090.5 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 804.9 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 632.6 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 614.1 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 596.1 | 17 | 0 |
| test/remote-run.test.mjs | pass | 592.8 | 130 | 0 |
| test/doctor.test.mjs | pass | 559.9 | 1 | 0 |
| test/remote-control.test.mjs | pass | 534.7 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 513.5 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 479.9 | 21 | 0 |

## Session 1 — 2026-11-20T13:45:26.422Z → 2026-11-20T13:46:22.649Z

Session id: `1b850215-ec3a-42ad-ad9f-6e79130e9990`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 56.2s | 58.0s | 47.3s | 0.0s | 0.0s | 56.2s | 3.3s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.5s | 1.9s | 5.4s | 5.4s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.7s | 1.7s | 1.7s | 1.7s | 0 |
| orchestrator | 16 | 1.5s | 1.9s | 5.4s | 5.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 3.3s | 3.3s |
| Bash | orchestrator | 10 | 10.0s | 6.7s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T13:46:10.387Z | 6.7s | 591 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:29.205Z | 0.6s | 4123 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:50.842Z | 0.4s | 31 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:32.930Z | 0.3s | 284 | true | false |
| Bash | orchestrator | 2026-11-20T13:45:57.630Z | 0.3s | 7750 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:53.726Z | 0.3s | 488 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:48.641Z | 0.3s | 154 | false | false |
| Read | orchestrator | 2026-11-20T13:45:59.783Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-20T13:45:38.354Z | 0.2s | 116 | true | false |
| Bash | orchestrator | 2026-11-20T13:45:36.609Z | 0.2s | 155 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 3.3s | 1 | 277 | 4 | 29389 | 11215 | 18170 | 0.0601 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.88 |
| Cost — claude-opus-5-5 | $0.88 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 945354 |
| Output tokens | 4956 |
| Thinking tokens (main thread) | 354 |
| Cache read tokens | 862635 |
| Cache write tokens | 82681 |
| Cache write tokens, main thread (5m / 1h) | 0 / 64511 |
| Cache hit ratio | 0.9125 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 915965 | 235 | 851420 | 64511 |
| sub-agents | 4 | 29389 | 277 | 11215 | 18170 |
| remainder | 0 | 0 | 4444 | 0 | 0 |

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
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.38 |

## Session 2 — 2026-11-20T13:46:26.529Z → 2026-11-20T13:54:17.470Z

Session id: `7584b2d8-6004-42e7-9d62-81adaaf782d5`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 7m 50s | 7m 52s | 7m 45s | 0.0s | 0.0s | 7m 50s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 31 | 2.0s | 9.4s | 1m 37s | 1m 37s | 0 |
| orchestrator | 31 | 2.0s | 9.4s | 1m 37s | 1m 37s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 17 | 7.1s | 0.8s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 21 | 1.1s | 0.2s |
| Write | orchestrator | 6 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T13:46:44.225Z | 0.8s | 1829 | false | false |
| Bash | orchestrator | 2026-11-20T13:47:02.603Z | 0.8s | 4510 | false | false |
| Bash | orchestrator | 2026-11-20T13:46:38.759Z | 0.4s | 12180 | false | false |
| Bash | orchestrator | 2026-11-20T13:46:26.532Z | 0.4s | 55 | false | false |
| Bash | orchestrator | 2026-11-20T13:47:09.256Z | 0.4s | 13488 | false | false |
| Bash | orchestrator | 2026-11-20T13:48:50.428Z | 0.4s | 1602 | false | false |
| Bash | orchestrator | 2026-11-20T13:49:26.243Z | 0.4s | 562 | false | false |
| Bash | orchestrator | 2026-11-20T13:49:00.031Z | 0.4s | 758 | false | false |
| Bash | orchestrator | 2026-11-20T13:47:06.673Z | 0.3s | 11368 | false | false |
| Bash | orchestrator | 2026-11-20T13:47:11.237Z | 0.3s | 2227 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.31 |
| Cost — claude-opus-5-5 | $3.31 |
| Input tokens (uncached) | 62 |
| Total input tokens (incl. cache) | 3971824 |
| Output tokens | 51703 |
| Thinking tokens (main thread) | 25055 |
| Cache read tokens | 3782098 |
| Cache write tokens | 189664 |
| Cache write tokens, main thread (5m / 1h) | 0 / 189664 |
| Cache hit ratio | 0.9522 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 62 | 3971824 | 345 | 3782098 | 189664 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 51358 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 48 |
| Time to first token | 1.6s |
| Rate-limit peak | seven_day 0.38 |

## Session 3 — 2026-11-20T13:54:21.011Z → 2026-11-20T13:55:53.510Z

Session id: `dedddd46-73aa-4d46-a4cf-8ac8619e9afa`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 32s | 1m 34s | 1m 31s | 0.0s | 0.0s | 1m 32s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 11 | 2.4s | 17.0s | 26.9s | 26.9s | 0 |
| orchestrator | 11 | 2.4s | 17.0s | 26.9s | 26.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 7 | 2.5s | 0.5s |
| Read | orchestrator | 15 | 0.7s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T13:54:21.013Z | 0.5s | 55 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:59.599Z | 0.5s | 4977 | false | false |
| Bash | orchestrator | 2026-11-20T13:55:03.917Z | 0.3s | 8296 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:23.403Z | 0.3s | 6002 | false | false |
| Read | orchestrator | 2026-11-20T13:54:34.147Z | 0.3s | 59335 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:26.230Z | 0.2s | 1566 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:39.261Z | 0.2s | 13750 | false | false |
| Bash | orchestrator | 2026-11-20T13:55:32.587Z | 0.2s | 143 | false | false |
| Read | orchestrator | 2026-11-20T13:54:40.364Z | 0.2s | 31668 | false | false |
| Write | orchestrator | 2026-11-20T13:55:45.194Z | 0.0s | 227 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.40 |
| Cost — claude-opus-5-5 | $1.40 |
| Input tokens (uncached) | 22 |
| Total input tokens (incl. cache) | 878748 |
| Output tokens | 9741 |
| Thinking tokens (main thread) | 4602 |
| Cache read tokens | 746499 |
| Cache write tokens | 132227 |
| Cache write tokens, main thread (5m / 1h) | 0 / 132227 |
| Cache hit ratio | 0.8495 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 22 | 878748 | 108 | 746499 | 132227 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 9633 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 24 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.38 |

## Session 4 — 2026-11-20T13:54:21.009Z → 2026-11-20T13:57:13.762Z

Session id: `79c900b2-fb65-486b-8f97-e3f9bc4bba6a`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 52s | 2m 54s | 2m 51s | 0.0s | 0.0s | 2m 52s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 19 | 1.9s | 37.3s | 38.4s | 38.4s | 0 |
| orchestrator | 19 | 1.9s | 37.3s | 38.4s | 38.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 22 | 5.9s | 0.5s |
| Read | orchestrator | 24 | 0.8s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T13:54:21.012Z | 0.5s | 55 | false | false |
| Bash | orchestrator | 2026-11-20T13:56:04.534Z | 0.3s | 156 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:48.580Z | 0.3s | 1715 | false | false |
| Bash | orchestrator | 2026-11-20T13:56:10.350Z | 0.3s | 6526 | false | false |
| Read | orchestrator | 2026-11-20T13:54:34.813Z | 0.3s | 59335 | false | false |
| Bash | orchestrator | 2026-11-20T13:54:23.649Z | 0.3s | 10039 | true | false |
| Bash | orchestrator | 2026-11-20T13:54:45.493Z | 0.3s | 12652 | false | false |
| Bash | orchestrator | 2026-11-20T13:55:18.501Z | 0.2s | 842 | false | false |
| Bash | orchestrator | 2026-11-20T13:55:20.452Z | 0.2s | 490 | false | false |
| Bash | orchestrator | 2026-11-20T13:55:21.453Z | 0.2s | 446 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.89 |
| Cost — claude-opus-5-5 | $1.89 |
| Input tokens (uncached) | 38 |
| Total input tokens (incl. cache) | 1794625 |
| Output tokens | 18356 |
| Thinking tokens (main thread) | 10589 |
| Cache read tokens | 1645959 |
| Cache write tokens | 148628 |
| Cache write tokens, main thread (5m / 1h) | 0 / 148628 |
| Cache hit ratio | 0.9172 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 38 | 1794625 | 887 | 1645959 | 148628 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 17469 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 48 |
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.38 |

## Session 5 — 2026-11-20T13:57:47.394Z → 2026-11-20T15:57:26.777Z

Session id: `ede21bf2-6b18-4cdb-bf8e-70e94fe9b312`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h59m | 1h59m | 30m 48s | 0.0s | 0.0s | 1h59m | 25m 05s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 463 | 1.8s | 5.3s | 23.6s | 45.8s | 0 |
| devscene:architecture-reviewer | 19 | 1.9s | 4.5s | 7.7s | 7.7s | 0 |
| devscene:branch-reviewer | 26 | 2.4s | 13.8s | 17.1s | 17.1s | 0 |
| devscene:layer-implementer | 132 | 1.9s | 6.0s | 23.6s | 40.5s | 0 |
| devscene:review-plan-reviewer | 28 | 3.0s | 8.1s | 12.1s | 12.1s | 0 |
| devscene:skeptic-reviewer | 28 | 2.9s | 30.8s | 45.8s | 45.8s | 0 |
| devscene:statistics-plan-writer | 7 | 1.8s | 16.3s | 16.3s | 16.3s | 0 |
| devscene:test-fix-plan-writer | 9 | 2.8s | 11.0s | 11.0s | 11.0s | 0 |
| orchestrator | 214 | 1.6s | 2.1s | 7.6s | 14.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 19 | 25m 05s | 4m 39s |
| Bash | devscene:architecture-reviewer | 14 | 6.4s | 3.2s |
| Bash | devscene:branch-reviewer | 22 | 8.5s | 1.5s |
| Bash | devscene:layer-implementer | 115 | 2m 22s | 9.3s |
| Bash | devscene:review-plan-reviewer | 27 | 8.3s | 1.1s |
| Bash | devscene:skeptic-reviewer | 22 | 6.1s | 0.6s |
| Bash | devscene:statistics-plan-writer | 9 | 1.9s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 6 | 1.4s | 0.3s |
| Bash | orchestrator | 182 | 1h26m | 1m 03s |
| Edit | devscene:layer-implementer | 30 | 1.2s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Read | devscene:architecture-reviewer | 21 | 1.2s | 0.3s |
| Read | devscene:branch-reviewer | 12 | 0.6s | 0.2s |
| Read | devscene:layer-implementer | 41 | 1.2s | 0.3s |
| Read | devscene:review-plan-reviewer | 26 | 1.1s | 0.3s |
| Read | devscene:skeptic-reviewer | 12 | 0.6s | 0.3s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 9 | 0.3s | 0.2s |
| Read | orchestrator | 17 | 7.7s | 5.6s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 9 | 0.3s | 0.0s |
| Write | devscene:skeptic-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T15:14:52.311Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:39:31.300Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:27:55.470Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:34:15.329Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T15:41:21.981Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:58:33.840Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:29:00.182Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T14:56:26.080Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T15:40:18.080Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T15:17:03.210Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_loader.py | 6 | 6.8s |
| devscene:layer-implementer | bash scripts/python-service.sh --package graphscene test tests/test_model.py | 3 | 3.1s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 8 | 47.1s |
| devscene:layer-implementer | git diff --name-only HEAD | 3 | 5.6s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 3 | 5.1s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 11 | 2.4s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/feat_graphscene_graph_model_code_revi | 3 | 18.0s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_graphscene_graph_model_story_plan.md --i | 5 | 32.8s |
| orchestrator | cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 3 | 0.7s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 41 | 41m 33s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_2 | 41 | 41m 51s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 3 | 0.8s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 12 | 3.1s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 graphscene | 2m 10s | 20 | 14973 | 42 | 1075457 | 1014738 | 60677 | 0.0181 |
| devscene:layer-implementer | Implement Task 2 graphscene | 1m 58s | 14 | 14199 | 30 | 772982 | 722248 | 50704 | 0.0165 |
| devscene:layer-implementer | Implement Task 3 graphscene | 1m 20s | 11 | 8548 | 24 | 502307 | 464637 | 37646 | 0.0112 |
| devscene:layer-implementer | Implement Task 4 graphscene | 1m 12s | 15 | 6547 | 32 | 611557 | 580161 | 31364 | 0.01 |
| devscene:layer-implementer | Implement Task 5 general | 57.8s | 12 | 5004 | 26 | 949809 | 871259 | 78524 | 0.0081 |
| devscene:architecture-reviewer | Architecture review of branch | 57.3s | 10 | 5631 | 22 | 736577 | 650287 | 86268 | 0.008 |
| devscene:branch-reviewer | End-of-branch code review | 2m 46s | 26 | 18034 | 54 | 2508619 | 2369642 | 138923 | 0.0232 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 20s | 15 | 7992 | 32 | 1092644 | 1006896 | 85716 | 0.0112 |
| devscene:layer-implementer | Fix code-review Finding 1 | 27.7s | 8 | 2325 | 18 | 264941 | 233486 | 31437 | 0.0039 |
| devscene:layer-implementer | Fix code-review Finding 2 | 40.7s | 11 | 3535 | 24 | 376435 | 355250 | 21161 | 0.0057 |
| devscene:layer-implementer | Fix code-review Finding 3 | 46.1s | 11 | 4416 | 24 | 402017 | 377890 | 24103 | 0.0064 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 4m 39s | 28 | 30210 | 58 | 2612160 | 2475823 | 136279 | 0.0389 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 1m 15s | 13 | 8041 | 28 | 1174843 | 1053932 | 120883 | 0.0106 |
| devscene:layer-implementer | Fix skeptic Finding 2 | 47.7s | 11 | 4376 | 24 | 413387 | 376288 | 37075 | 0.0066 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 50.0s | 10 | 4883 | 22 | 435792 | 402014 | 33756 | 0.007 |
| devscene:test-fix-plan-writer | Write round 1 test fix plan | 1m 03s | 9 | 6667 | 20 | 494805 | 430563 | 64222 | 0.0088 |
| devscene:architecture-reviewer | Arch gate on test fix plan | 35.8s | 9 | 3636 | 20 | 651763 | 520179 | 131564 | 0.005 |
| devscene:layer-implementer | Fix test-fix Finding 1 | 36.4s | 9 | 2842 | 20 | 305905 | 274342 | 31543 | 0.0051 |
| devscene:statistics-plan-writer | Write branch statistics | 38.4s | 7 | 4701 | 16 | 304980 | 261599 | 43365 | 0.0054 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $24.68 |
| Cost — claude-opus-5-5 | $24.68 |
| Input tokens (uncached) | 966 |
| Total input tokens (incl. cache) | 62239869 |
| Output tokens | 202196 |
| Thinking tokens (main thread) | 3643 |
| Cache read tokens | 60710104 |
| Cache write tokens | 1528799 |
| Cache write tokens, main thread (5m / 1h) | 0 / 283589 |
| Cache hit ratio | 0.9754 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 430 | 46552889 | 4935 | 46268870 | 283589 |
| sub-agents | 536 | 15686980 | 156560 | 14441234 | 1245210 |
| remainder | 0 | 0 | 40701 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 18 |
| Sub-agents spawned / failed / killed | 19 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 233 |
| Time to first token | 2.0s |
| Rate-limit peak | seven_day 0.39 |

## Session 6 — 2026-11-21T07:35:58.596Z → 2026-11-21T08:26:29.085Z

Session id: `6f9da34f-2d02-4a6d-a0f7-c971a8d43077`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 50m 30s | 50m 33s | 12m 51s | 0.0s | 0.0s | 50m 30s | 7m 26s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 145 | 2.6s | 7.1s | 27.4s | 30.4s | 0 |
| devscene:architecture-reviewer | 11 | 2.9s | 7.9s | 9.3s | 9.3s | 0 |
| devscene:layer-implementer | 12 | 2.7s | 16.7s | 17.0s | 17.0s | 0 |
| devscene:layer-reviewer | 10 | 2.0s | 7.1s | 27.4s | 27.4s | 0 |
| devscene:prompt-injection-reviewer | 1 | 2.6s | 2.6s | 2.6s | 2.6s | 0 |
| devscene:statistics-plan-writer | 6 | 2.4s | 22.0s | 22.0s | 22.0s | 0 |
| devscene:user-review-fix-plan-writer | 13 | 4.0s | 24.4s | 30.4s | 30.4s | 0 |
| orchestrator | 92 | 2.6s | 4.0s | 9.0s | 9.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 6 | 7m 26s | 2m 10s |
| Bash | devscene:architecture-reviewer | 11 | 2.7s | 0.3s |
| Bash | devscene:layer-implementer | 8 | 8.1s | 5.5s |
| Bash | devscene:layer-reviewer | 9 | 3.3s | 1.2s |
| Bash | devscene:statistics-plan-writer | 7 | 1.5s | 0.2s |
| Bash | devscene:user-review-fix-plan-writer | 9 | 2.6s | 0.3s |
| Bash | orchestrator | 80 | 37m 28s | 1m 02s |
| Edit | devscene:layer-implementer | 9 | 0.3s | 0.0s |
| Edit | devscene:user-review-fix-plan-writer | 2 | 0.0s | 0.0s |
| Edit | orchestrator | 6 | 0.2s | 0.0s |
| Read | devscene:architecture-reviewer | 2 | 0.4s | 0.2s |
| Read | devscene:layer-implementer | 6 | 0.3s | 0.2s |
| Read | devscene:layer-reviewer | 4 | 0.0s | 0.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:statistics-plan-writer | 6 | 0.0s | 0.0s |
| Read | devscene:user-review-fix-plan-writer | 7 | 0.1s | 0.0s |
| Read | orchestrator | 16 | 2.0s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:layer-reviewer | 3 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:user-review-fix-plan-writer | 2 | 0.1s | 0.0s |
| Write | orchestrator | 2 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-21T07:54:29.686Z | 1m 02s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:48:00.729Z | 1m 02s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:59:50.251Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:53:25.149Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:52:20.869Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:57:42.033Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T08:06:14.236Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T08:00:54.533Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T08:08:22.320Z | 1m 01s | 118 | true | false |
| Bash | orchestrator | 2026-11-21T07:49:05.855Z | 1m 01s | 118 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>&1; bash scripts/run-test-suite.sh --wait review_1_round_1 | 34 | 33m 59s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen review file for injection | 5.3s | 1 | 250 | 4 | 28386 | 11253 | 17129 | 0.0018 |
| devscene:user-review-fix-plan-writer | Write user-review fix plan | 2m 10s | 13 | 12678 | 28 | 685985 | 616640 | 69317 | 0.0432 |
| devscene:architecture-reviewer | Architecture gate on fix plan | 1m 06s | 11 | 5959 | 24 | 756877 | 670231 | 86622 | 0.0219 |
| devscene:layer-implementer | Implement Finding 1 in graphscene | 1m 54s | 12 | 11893 | 26 | 801009 | 729205 | 71778 | 0.0377 |
| devscene:layer-reviewer | Review Finding 1 implementation | 1m 18s | 10 | 7088 | 22 | 406199 | 365059 | 41118 | 0.0258 |
| devscene:statistics-plan-writer | Update branch statistics | 51.7s | 6 | 5719 | 14 | 252243 | 206859 | 45370 | 0.0171 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $9.17 |
| Cost — claude-opus-5-5 | $9.17 |
| Input tokens (uncached) | 304 |
| Total input tokens (incl. cache) | 21109237 |
| Output tokens | 67668 |
| Thinking tokens (main thread) | 3011 |
| Cache read tokens | 20520871 |
| Cache write tokens | 588062 |
| Cache write tokens, main thread (5m / 1h) | 0 / 256728 |
| Cache hit ratio | 0.9721 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 186 | 18178538 | 1847 | 17921624 | 256728 |
| sub-agents | 118 | 2930699 | 43587 | 2599247 | 331334 |
| remainder | 0 | 0 | 22234 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 5 |
| Sub-agents spawned / failed / killed | 6 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 113 |
| Time to first token | 2.5s |
| Rate-limit peak | seven_day 0.4 |
