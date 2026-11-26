# Run analytics — feat_flow_host_claude_executor

## Whole run

| Measure | Value |
|---|---|
| Sessions | 5 (0 incomplete) |
| Engine / planning node sessions | 2 / 3 |
| Span | 2h20m |
| Wall | 2h20m |
| Session wall, summed over sessions | 2h21m |
| Active | 2h20m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $37.31 |
| Input tokens (uncached) | 1192 |
| Total input tokens (incl. cache) | 83148973 |
| Output tokens | 342945 |
| Thinking tokens (main thread) | 53326 |
| Cache read tokens | 80842804 |
| Cache write tokens | 2304977 |
| Cache write tokens, main thread (5m / 1h) | 0 / 918971 |
| Cache hit ratio | 0.9723 |
| Requests | 578 |
| Request latency p50 / p90 / p99 / max | 1.7s / 9.1s / 40.3s / 1m 00s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 19 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — Phase B end-of-branch review — 4m 49s (session 5) |
| Rate-limit peak | seven_day 0.23 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 8m 13s | 8m 13s | 0.0s | 8m 14s | $4.08 |
| 3 | 2-architecture_review | 1m 07s | 1m 07s | 0.0s | 1m 09s | $1.16 |
| 4 | 3-plan_review | 4m 55s | 4m 55s | 0.0s | 4m 57s | $3.61 |

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
| Wait (every run of task_round_1) | 41m 35s |
| Gate rows | 32 (complete) |
| Test files — full | 233 files, 19985.0 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 4 | ok | 2479 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 17 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 0 s |
| full | 13g | ok | 7 s |
| full | 13h | ok | 0 s |
| full | 13i | ok | 1 s |
| full | 13j | FAIL | 15 s |
| full | 14a | ok | 7 s |
| full | 14c | ok | 9 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 233)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1304.0 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 877.5 | 21 | 0 |
| test/remote-run.test.mjs | pass | 744.0 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 710.5 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 693.9 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 671.7 | 17 | 0 |
| test/remote-control.test.mjs | pass | 652.7 | 83 | 0 |
| test/doctor.test.mjs | pass | 638.7 | 1 | 0 |
| test/remote-control-review.test.mjs | pass | 588.7 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 531.4 | 21 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 44m 24s |
| Gate rows | 32 (complete) |
| Test files — full | 233 files, 21452.8 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 13j | ok | 21 s |
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 4 | ok | 2652 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 15 s |
| full | 13a | ok | 0 s |
| full | 13b | ok | 1 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13f | ok | 1 s |
| full | 13g | ok | 7 s |
| full | 13h | ok | 0 s |
| full | 13i | ok | 0 s |
| full | 14a | ok | 7 s |
| full | 14c | ok | 5 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 233)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1298.7 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 886.3 | 21 | 0 |
| test/remote-run.test.mjs | pass | 733.6 | 130 | 0 |
| test/doctor.test.mjs | pass | 717.5 | 1 | 0 |
| test/watcher-remote-job.test.mjs | pass | 706.6 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 687.8 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 670.4 | 17 | 0 |
| test/remote-control.test.mjs | pass | 654.0 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 588.9 | 33 | 0 |
| test/planning-driver-walk.test.mjs | pass | 544.9 | 9 | 0 |

## Session 1 — 2026-11-26T12:30:35.242Z → 2026-11-26T12:31:28.285Z

Session id: `7805bc29-1d63-40df-9715-9e253436ba9f`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 53.0s | 54.4s | 47.0s | 0.0s | 0.0s | 53.0s | 4.1s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.4s | 3.0s | 5.1s | 5.1s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.6s | 1.6s | 1.6s | 1.6s | 0 |
| orchestrator | 16 | 1.4s | 3.0s | 5.1s | 5.1s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 4.1s | 4.1s |
| Bash | orchestrator | 14 | 7.5s | 5.0s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 4 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T12:31:18.050Z | 5.0s | 603 | false | false |
| Bash | orchestrator | 2026-11-26T12:30:37.381Z | 0.2s | 58 | false | false |
| Read | orchestrator | 2026-11-26T12:31:07.728Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-26T12:30:57.547Z | 0.2s | 157 | false | false |
| Bash | orchestrator | 2026-11-26T12:30:45.412Z | 0.2s | 158 | false | false |
| Bash | orchestrator | 2026-11-26T12:31:06.003Z | 0.1s | 1064 | false | false |
| Bash | orchestrator | 2026-11-26T12:30:42.102Z | 0.1s | 8742 | false | false |
| Bash | orchestrator | 2026-11-26T12:30:59.302Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-26T12:31:02.459Z | 0.1s | 606 | false | false |
| Bash | orchestrator | 2026-11-26T12:31:00.149Z | 0.1s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 4.1s | 1 | 354 | 4 | 30818 | 11215 | 19599 | 0.0773 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.91 |
| Cost — claude-opus-5-5 | $0.91 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 985416 |
| Output tokens | 5247 |
| Thinking tokens (main thread) | 283 |
| Cache read tokens | 900152 |
| Cache write tokens | 85228 |
| Cache write tokens, main thread (5m / 1h) | 0 / 65629 |
| Cache hit ratio | 0.9135 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 954598 | 696 | 888937 | 65629 |
| sub-agents | 4 | 30818 | 354 | 11215 | 19599 |
| remainder | 0 | 0 | 4197 | 0 | 0 |

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
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.22 |

## Session 2 — 2026-11-26T12:31:30.934Z → 2026-11-26T12:39:44.388Z

Session id: `5acb0dc8-3639-4e14-8752-642cc03f4623`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 8m 13s | 8m 14s | 8m 10s | 0.0s | 0.0s | 8m 13s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 38 | 1.6s | 28.7s | 56.7s | 56.7s | 0 |
| orchestrator | 38 | 1.6s | 28.7s | 56.7s | 56.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 26 | 4.6s | 0.2s |
| Edit | orchestrator | 1 | 0.0s | 0.0s |
| Read | orchestrator | 21 | 1.7s | 0.4s |
| Write | orchestrator | 6 | 0.1s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-26T12:31:38.583Z | 0.4s | 37356 | false | false |
| Read | orchestrator | 2026-11-26T12:32:02.141Z | 0.3s | 33214 | false | false |
| Bash | orchestrator | 2026-11-26T12:31:31.230Z | 0.2s | 58 | false | false |
| Read | orchestrator | 2026-11-26T12:31:36.364Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T12:33:59.434Z | 0.2s | 850 | false | false |
| Read | orchestrator | 2026-11-26T12:32:18.009Z | 0.2s | 29247 | false | false |
| Bash | orchestrator | 2026-11-26T12:34:08.902Z | 0.2s | 1705 | false | false |
| Bash | orchestrator | 2026-11-26T12:33:46.120Z | 0.2s | 883 | false | false |
| Read | orchestrator | 2026-11-26T12:31:41.377Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-26T12:32:13.720Z | 0.1s | 1179 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $4.08 |
| Cost — claude-opus-5-5 | $4.08 |
| Input tokens (uncached) | 76 |
| Total input tokens (incl. cache) | 5821176 |
| Output tokens | 55047 |
| Thinking tokens (main thread) | 26935 |
| Cache read tokens | 5588625 |
| Cache write tokens | 232475 |
| Cache write tokens, main thread (5m / 1h) | 0 / 232475 |
| Cache hit ratio | 0.9601 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 76 | 5821176 | 457 | 5588625 | 232475 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 54590 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 55 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.22 |

## Session 3 — 2026-11-26T12:39:47.376Z → 2026-11-26T12:40:55.330Z

Session id: `7ac76ff5-a23a-4331-a6b6-6e5890dee9eb`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 07s | 1m 09s | 1m 08s | 0.0s | 0.0s | 1m 07s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 9 | 1.5s | 28.9s | 28.9s | 28.9s | 0 |
| orchestrator | 9 | 1.5s | 28.9s | 28.9s | 28.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 1.3s | 0.2s |
| Read | orchestrator | 13 | 0.3s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-26T12:39:59.503Z | 0.2s | 63403 | false | false |
| Bash | orchestrator | 2026-11-26T12:39:47.876Z | 0.2s | 58 | false | false |
| Bash | orchestrator | 2026-11-26T12:39:48.618Z | 0.2s | 7188 | false | false |
| Bash | orchestrator | 2026-11-26T12:39:51.441Z | 0.1s | 1143 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:36.681Z | 0.1s | 71 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:37.433Z | 0.1s | 881 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:02.931Z | 0.1s | 14070 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:36.025Z | 0.1s | 1807 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:34.413Z | 0.1s | 727 | true | true |
| Read | orchestrator | 2026-11-26T12:39:53.648Z | 0.0s | 14289 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.16 |
| Cost — claude-opus-5-5 | $1.16 |
| Input tokens (uncached) | 18 |
| Total input tokens (incl. cache) | 664947 |
| Output tokens | 7392 |
| Thinking tokens (main thread) | 3654 |
| Cache read tokens | 551972 |
| Cache write tokens | 112957 |
| Cache write tokens, main thread (5m / 1h) | 0 / 112957 |
| Cache hit ratio | 0.8301 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 18 | 664947 | 87 | 551972 | 112957 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7305 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 23 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.22 |

## Session 4 — 2026-11-26T12:39:47.387Z → 2026-11-26T12:44:43.271Z

Session id: `a185d9cf-76bd-4099-81d8-16062ee418bb`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 55s | 4m 57s | 4m 51s | 0.0s | 0.0s | 4m 55s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 38 | 2.2s | 24.3s | 50.2s | 50.2s | 0 |
| orchestrator | 38 | 2.2s | 24.3s | 50.2s | 50.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 31 | 5.6s | 0.3s |
| Read | orchestrator | 17 | 1.3s | 0.4s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-26T12:40:10.618Z | 0.4s | 37356 | false | false |
| Bash | orchestrator | 2026-11-26T12:39:47.673Z | 0.3s | 58 | false | false |
| Read | orchestrator | 2026-11-26T12:40:06.605Z | 0.2s | 63403 | false | false |
| Read | orchestrator | 2026-11-26T12:40:15.885Z | 0.2s | 32601 | false | false |
| Bash | orchestrator | 2026-11-26T12:41:54.929Z | 0.2s | 300 | false | false |
| Bash | orchestrator | 2026-11-26T12:41:38.665Z | 0.2s | 5233 | false | false |
| Read | orchestrator | 2026-11-26T12:40:07.007Z | 0.2s | 30778 | false | false |
| Bash | orchestrator | 2026-11-26T12:41:44.330Z | 0.2s | 2132 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:31.277Z | 0.2s | 3922 | false | false |
| Bash | orchestrator | 2026-11-26T12:40:35.851Z | 0.2s | 2481 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.61 |
| Cost — claude-opus-5-5 | $3.61 |
| Input tokens (uncached) | 76 |
| Total input tokens (incl. cache) | 6181817 |
| Output tokens | 30611 |
| Thinking tokens (main thread) | 19528 |
| Cache read tokens | 5955932 |
| Cache write tokens | 225809 |
| Cache write tokens, main thread (5m / 1h) | 0 / 225809 |
| Cache hit ratio | 0.9635 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 76 | 6181817 | 1044 | 5955932 | 225809 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 29567 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 50 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.22 |

## Session 5 — 2026-11-26T12:45:10.650Z → 2026-11-26T14:51:11.373Z

Session id: `a645cb9f-9d51-4e74-b4b2-70f60b3fc8e4`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2h06m | 2h06m | 35m 11s | 0.0s | 0.0s | 2h06m | 30m 40s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 476 | 1.7s | 7.7s | 32.6s | 1m 00s | 0 |
| devscene:architecture-reviewer | 23 | 2.0s | 6.2s | 19.3s | 19.3s | 0 |
| devscene:branch-reviewer | 40 | 2.9s | 7.9s | 1m 00s | 1m 00s | 0 |
| devscene:layer-implementer | 132 | 1.9s | 11.7s | 34.6s | 42.8s | 0 |
| devscene:review-plan-reviewer | 26 | 2.6s | 11.5s | 18.5s | 18.5s | 0 |
| devscene:skeptic-reviewer | 42 | 3.2s | 11.9s | 30.1s | 30.1s | 0 |
| devscene:statistics-plan-writer | 4 | 2.1s | 16.2s | 16.2s | 16.2s | 0 |
| devscene:test-fix-plan-writer | 10 | 2.0s | 23.5s | 24.1s | 24.1s | 0 |
| orchestrator | 199 | 1.6s | 2.0s | 7.3s | 7.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 17 | 30m 40s | 4m 49s |
| Bash | devscene:architecture-reviewer | 18 | 3.5s | 0.3s |
| Bash | devscene:branch-reviewer | 27 | 17.9s | 12.9s |
| Bash | devscene:layer-implementer | 104 | 2m 15s | 12.8s |
| Bash | devscene:review-plan-reviewer | 24 | 4.5s | 0.5s |
| Bash | devscene:skeptic-reviewer | 31 | 4.8s | 0.2s |
| Bash | devscene:statistics-plan-writer | 5 | 0.9s | 0.2s |
| Bash | devscene:test-fix-plan-writer | 7 | 1.3s | 0.3s |
| Bash | orchestrator | 168 | 1h28m | 1m 02s |
| Edit | devscene:layer-implementer | 53 | 1.8s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Grep | orchestrator | 1 | 0.0s | 0.0s |
| Read | devscene:architecture-reviewer | 21 | 1.0s | 0.2s |
| Read | devscene:branch-reviewer | 22 | 0.5s | 0.2s |
| Read | devscene:layer-implementer | 43 | 1.1s | 0.2s |
| Read | devscene:review-plan-reviewer | 13 | 0.4s | 0.2s |
| Read | devscene:skeptic-reviewer | 19 | 0.2s | 0.0s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 5 | 0.0s | 0.0s |
| Read | orchestrator | 15 | 1.9s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 5 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 10 | 0.4s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.0s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-26T14:13:07.065Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T14:20:33.137Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T14:15:16.199Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T13:18:12.017Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T14:07:50.652Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T13:40:15.350Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T13:24:32.966Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T14:12:03.221Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T13:36:04.087Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-26T14:37:22.095Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host lint | 5 | 2.5s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py | 5 | 11.7s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_layers.py | 5 | 17.4s |
| devscene:layer-implementer | bash scripts/python-service.sh --package devscene-flow-host test tests/test_session_process.py | 4 | 15.2s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 10 | 56.2s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.3s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_flow_host_claude_executor_story_plan.md  | 5 | 27.0s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 41 | 41m 35s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_2 | 44 | 44m 24s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 11 | 2.1s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 records reader | 1m 40s | 14 | 10942 | 30 | 1007682 | 927642 | 80010 | 0.0133 |
| devscene:layer-implementer | Implement Task 2 session stream | 2m 19s | 17 | 17018 | 36 | 1007594 | 950816 | 56742 | 0.0185 |
| devscene:layer-implementer | Implement Task 3 session process | 2m 01s | 13 | 12631 | 28 | 671194 | 626809 | 44357 | 0.016 |
| devscene:layer-implementer | Implement Task 4 ClaudeExecutor | 2m 40s | 23 | 19781 | 48 | 1618396 | 1543831 | 74517 | 0.0212 |
| devscene:layer-implementer | Implement Task 5 README docs | 1m 28s | 14 | 9974 | 30 | 1023077 | 949643 | 73404 | 0.0117 |
| devscene:architecture-reviewer | A2 architecture review of branch | 1m 23s | 15 | 9095 | 32 | 1430792 | 1308479 | 122281 | 0.011 |
| devscene:branch-reviewer | Phase B end-of-branch review | 4m 49s | 40 | 31185 | 82 | 6424217 | 6199827 | 224308 | 0.0383 |
| devscene:review-plan-reviewer | B.2 meta-review of code review | 1m 24s | 15 | 8933 | 32 | 878406 | 804671 | 73703 | 0.0111 |
| devscene:layer-implementer | Fix code-review Finding 2 | 35.7s | 11 | 2846 | 24 | 471186 | 423421 | 47741 | 0.0047 |
| devscene:layer-implementer | Fix code-review Finding 1 | 1m 07s | 11 | 7235 | 24 | 530584 | 491543 | 39017 | 0.0089 |
| devscene:skeptic-reviewer | C2 adversarial skeptic review | 4m 47s | 42 | 30919 | 86 | 3821073 | 3690593 | 130394 | 0.038 |
| devscene:review-plan-reviewer | C2.2 meta-review of skeptic review | 1m 12s | 11 | 7861 | 24 | 621771 | 547778 | 73969 | 0.0096 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 1m 38s | 19 | 11278 | 40 | 1092539 | 1027048 | 65451 | 0.0131 |
| devscene:test-fix-plan-writer | G.2 write test fix plan round 1 | 1m 24s | 10 | 9358 | 22 | 441344 | 384990 | 56332 | 0.0112 |
| devscene:architecture-reviewer | G.2 architecture gate on fix plan | 35.2s | 8 | 3917 | 18 | 640560 | 516282 | 124260 | 0.0047 |
| devscene:layer-implementer | Fix test-fix Finding 1 | 59.4s | 10 | 5121 | 22 | 436916 | 393372 | 43522 | 0.0079 |
| devscene:statistics-plan-writer | D.1 write branch statistics | 31.4s | 4 | 4305 | 10 | 161255 | 124846 | 36399 | 0.0042 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $27.55 |
| Cost — claude-opus-5-5 | $27.55 |
| Input tokens (uncached) | 986 |
| Total input tokens (incl. cache) | 69495617 |
| Output tokens | 244648 |
| Thinking tokens (main thread) | 2926 |
| Cache read tokens | 67846123 |
| Cache write tokens | 1648508 |
| Cache write tokens, main thread (5m / 1h) | 0 / 282101 |
| Cache hit ratio | 0.9763 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 398 | 47217031 | 4551 | 46934532 | 282101 |
| sub-agents | 588 | 22278586 | 202399 | 20911591 | 1366407 |
| remainder | 0 | 0 | 37698 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 17 |
| Sub-agents spawned / failed / killed | 17 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 216 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.23 |
