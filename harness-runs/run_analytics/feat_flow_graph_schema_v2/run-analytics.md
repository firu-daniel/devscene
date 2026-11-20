# Run analytics — feat_flow_graph_schema_v2

## Whole run

| Measure | Value |
|---|---|
| Sessions | 11 (0 incomplete) |
| Engine / planning node sessions | 2 / 9 |
| Span | 2h38m |
| Wall | 2h37m |
| Session wall, summed over sessions | 2h42m |
| Active | 2h37m |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $53.47 |
| Input tokens (uncached) | 1698 |
| Total input tokens (incl. cache) | 116063754 |
| Output tokens | 489288 |
| Thinking tokens (main thread) | 93412 |
| Cache read tokens | 112761176 |
| Cache write tokens | 3300880 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1541719 |
| Cache hit ratio | 0.9715 |
| Requests | 824 |
| Request latency p50 / p90 / p99 / max | 2.1s / 8.5s / 42.2s / 1m 24s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 27 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:branch-reviewer — End-of-branch code review — 4m 39s (session 11) |
| Rate-limit peak | seven_day 0.36 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 12m 00s | 12m 00s | 0.0s | 12m 02s | $5.39 |
| 3 | 2-architecture_review | 1m 58s | 1m 58s | 0.0s | 1m 59s | $1.65 |
| 4 | 3-plan_review | 4m 37s | 4m 37s | 0.0s | 4m 38s | $3.29 |
| 5 | 4-plan_writer | 41.8s | 41.8s | 0.0s | 43.1s | $0.40 |
| 6 | 5-architecture_review | 2m 03s | 2m 03s | 0.0s | 2m 04s | $1.58 |
| 7 | 6-plan_review | 5m 15s | 5m 15s | 0.0s | 5m 17s | $3.34 |
| 8 | 7-plan_writer | 1m 00s | 1m 00s | 0.0s | 1m 01s | $0.56 |
| 9 | 8-architecture_review | 56.2s | 56.2s | 0.0s | 58.0s | $0.56 |
| 10 | 9-plan_review | 1m 33s | 1m 33s | 0.0s | 1m 34s | $1.47 |

## Network refusals

11 of 11 sessions scanned.

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
| Wait (every run of task_round_1) | 38m 11s |
| Gate rows | 34 (complete) |
| Test files — full | 222 files, 18216.8 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 1 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 3 s |
| full | 3c | ok | 3 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 1 s |
| full | 3i | ok | 1 s |
| full | 4 | ok | 2315 s |
| full | 6a | FAIL | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 1 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 21 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 7 s |
| full | 13c | ok | 19 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 1 s |
| full | 13f | FAIL | 3 s |
| full | 13g | ok | 1 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1133.3 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 853.7 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 641.2 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 631.9 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 622.1 | 17 | 0 |
| test/remote-run.test.mjs | pass | 611.4 | 130 | 0 |
| test/doctor.test.mjs | pass | 568.7 | 1 | 0 |
| test/remote-control.test.mjs | pass | 557.0 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 537.1 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 503.2 | 21 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 37m 37s |
| Gate rows | 34 (complete) |
| Test files — full | 222 files, 18730.4 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 6a | ok | 1 s |
| focused | 13f | ok | 0 s |
| full | 1 | ok | 1 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 1 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 3 s |
| full | 3c | ok | 2 s |
| full | 3d | ok | 2 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 2 s |
| full | 3g | ok | 0 s |
| full | 3h | ok | 2 s |
| full | 3i | ok | 0 s |
| full | 4 | ok | 2341 s |
| full | 6b | ok | 1 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 1 s |
| full | 11 | ok | 15 s |
| full | 13a | ok | 1 s |
| full | 13b | ok | 0 s |
| full | 13c | ok | 16 s |
| full | 13d | SKIPPED | 0 s |
| full | 13e | ok | 0 s |
| full | 13g | ok | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 222)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/planning-driver-control.test.mjs | pass | 1153.1 | 17 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 818.2 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 641.9 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 640.4 | 27 | 0 |
| test/remote-run.test.mjs | pass | 635.4 | 130 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 629.3 | 17 | 0 |
| test/doctor.test.mjs | pass | 600.8 | 1 | 0 |
| test/remote-control.test.mjs | pass | 573.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 549.5 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 506.2 | 21 | 0 |

## Session 1 — 2026-11-20T06:35:39.183Z → 2026-11-20T06:36:38.392Z

Session id: `677c2241-32fa-4aec-a9cb-46d6e7b97cfa`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 59.2s | 1m 00s | 51.7s | 0.0s | 0.0s | 59.2s | 4.1s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 18 | 1.7s | 2.5s | 5.3s | 5.3s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.7s | 1.7s | 1.7s | 1.7s | 0 |
| orchestrator | 17 | 1.7s | 2.5s | 5.3s | 5.3s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 4.1s | 4.1s |
| Bash | orchestrator | 9 | 8.6s | 6.5s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.3s | 0.2s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:36:26.478Z | 6.5s | 583 | false | false |
| Bash | orchestrator | 2026-11-20T06:35:42.466Z | 0.4s | 783 | false | false |
| Bash | orchestrator | 2026-11-20T06:35:50.013Z | 0.3s | 153 | false | false |
| Bash | orchestrator | 2026-11-20T06:36:04.570Z | 0.2s | 152 | false | false |
| Bash | orchestrator | 2026-11-20T06:36:14.135Z | 0.2s | 1323 | false | false |
| Bash | orchestrator | 2026-11-20T06:35:46.533Z | 0.2s | 1034 | false | false |
| Bash | orchestrator | 2026-11-20T06:36:06.935Z | 0.2s | 31 | false | false |
| Read | orchestrator | 2026-11-20T06:36:16.534Z | 0.2s | 26508 | false | false |
| Bash | orchestrator | 2026-11-20T06:35:52.048Z | 0.2s | 114 | true | false |
| Bash | orchestrator | 2026-11-20T06:36:09.463Z | 0.2s | 644 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 4.1s | 1 | 254 | 4 | 30149 | 11217 | 18928 | 0.0697 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.90 |
| Cost — claude-opus-5-5 | $0.90 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 1027323 |
| Output tokens | 5044 |
| Thinking tokens (main thread) | 290 |
| Cache read tokens | 944361 |
| Cache write tokens | 82922 |
| Cache write tokens, main thread (5m / 1h) | 0 / 63994 |
| Cache hit ratio | 0.9192 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 36 | 997174 | 728 | 933144 | 63994 |
| sub-agents | 4 | 30149 | 254 | 11217 | 18928 |
| remainder | 0 | 0 | 4062 | 0 | 0 |

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
| Time to first token | 1.5s |
| Rate-limit peak | seven_day 0.33 |

## Session 2 — 2026-11-20T06:36:41.682Z → 2026-11-20T06:48:42.483Z

Session id: `301a048a-d56f-4d36-835e-47507e4346b8`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 12m 00s | 12m 02s | 11m 51s | 0.0s | 0.0s | 12m 00s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 56 | 2.1s | 18.1s | 1m 24s | 1m 24s | 0 |
| orchestrator | 56 | 2.1s | 18.1s | 1m 24s | 1m 24s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 38 | 10.2s | 0.7s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 28 | 1.5s | 0.2s |
| Write | orchestrator | 7 | 0.3s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:37:12.061Z | 0.7s | 2216 | false | false |
| Bash | orchestrator | 2026-11-20T06:36:41.688Z | 0.4s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T06:38:00.518Z | 0.4s | 6272 | false | false |
| Bash | orchestrator | 2026-11-20T06:44:21.492Z | 0.3s | 263 | false | false |
| Bash | orchestrator | 2026-11-20T06:38:14.616Z | 0.3s | 2652 | false | false |
| Bash | orchestrator | 2026-11-20T06:41:01.109Z | 0.3s | 891 | false | false |
| Bash | orchestrator | 2026-11-20T06:36:56.089Z | 0.3s | 519 | false | false |
| Bash | orchestrator | 2026-11-20T06:37:42.694Z | 0.3s | 31 | false | false |
| Bash | orchestrator | 2026-11-20T06:38:35.606Z | 0.3s | 5413 | false | false |
| Read | orchestrator | 2026-11-20T06:36:48.146Z | 0.2s | 57794 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $5.39 |
| Cost — claude-opus-5-5 | $5.39 |
| Input tokens (uncached) | 112 |
| Total input tokens (incl. cache) | 9315680 |
| Output tokens | 74587 |
| Thinking tokens (main thread) | 38154 |
| Cache read tokens | 9054477 |
| Cache write tokens | 261091 |
| Cache write tokens, main thread (5m / 1h) | 0 / 261091 |
| Cache hit ratio | 0.972 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 112 | 9315680 | 604 | 9054477 | 261091 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 73983 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 77 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.33 |

## Session 3 — 2026-11-20T06:48:46.100Z → 2026-11-20T06:50:44.394Z

Session id: `a2609cd1-84ec-45f5-9a84-1d3251273a78`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 58s | 1m 59s | 1m 56s | 0.0s | 0.0s | 1m 58s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 14 | 1.9s | 26.2s | 32.2s | 32.2s | 0 |
| orchestrator | 14 | 1.9s | 26.2s | 32.2s | 32.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 2.9s | 0.5s |
| Read | orchestrator | 19 | 0.8s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:48:46.672Z | 0.5s | 53 | false | false |
| Read | orchestrator | 2026-11-20T06:48:57.019Z | 0.3s | 57794 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:06.977Z | 0.3s | 519 | false | false |
| Bash | orchestrator | 2026-11-20T06:48:49.330Z | 0.3s | 2688 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:37.358Z | 0.3s | 2965 | false | false |
| Bash | orchestrator | 2026-11-20T06:50:18.968Z | 0.3s | 3060 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:45.089Z | 0.2s | 3085 | false | false |
| Bash | orchestrator | 2026-11-20T06:48:53.505Z | 0.2s | 1105 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:41.465Z | 0.2s | 5788 | false | false |
| Bash | orchestrator | 2026-11-20T06:50:23.674Z | 0.2s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.65 |
| Cost — claude-opus-5-5 | $1.65 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 1391834 |
| Output tokens | 12366 |
| Thinking tokens (main thread) | 6522 |
| Cache read tokens | 1248012 |
| Cache write tokens | 143794 |
| Cache write tokens, main thread (5m / 1h) | 0 / 143794 |
| Cache hit ratio | 0.8967 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 28 | 1391834 | 802 | 1248012 | 143794 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 11564 | 0 | 0 |

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
| Rate-limit peak | seven_day 0.34 |

## Session 4 — 2026-11-20T06:48:46.473Z → 2026-11-20T06:53:23.763Z

Session id: `caca5cf9-0a5f-41cd-aeba-d826f9e36893`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 4m 37s | 4m 38s | 4m 30s | 0.0s | 0.0s | 4m 37s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 42 | 1.8s | 16.4s | 43.0s | 43.0s | 0 |
| orchestrator | 42 | 1.8s | 16.4s | 43.0s | 43.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 32 | 8.4s | 0.5s |
| Read | orchestrator | 24 | 1.0s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:48:46.478Z | 0.5s | 53 | false | false |
| Read | orchestrator | 2026-11-20T06:49:03.330Z | 0.3s | 57794 | false | false |
| Bash | orchestrator | 2026-11-20T06:51:22.388Z | 0.3s | 1084 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:06.983Z | 0.3s | 2076 | false | false |
| Bash | orchestrator | 2026-11-20T06:51:17.734Z | 0.3s | 13720 | false | false |
| Bash | orchestrator | 2026-11-20T06:50:13.831Z | 0.3s | 2806 | false | false |
| Bash | orchestrator | 2026-11-20T06:52:10.505Z | 0.3s | 987 | false | false |
| Bash | orchestrator | 2026-11-20T06:48:49.475Z | 0.3s | 11998 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:59.938Z | 0.2s | 1665 | false | false |
| Bash | orchestrator | 2026-11-20T06:49:00.538Z | 0.2s | 10896 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.29 |
| Cost — claude-opus-5-5 | $3.29 |
| Input tokens (uncached) | 84 |
| Total input tokens (incl. cache) | 6149935 |
| Output tokens | 27379 |
| Thinking tokens (main thread) | 14399 |
| Cache read tokens | 5955849 |
| Cache write tokens | 194002 |
| Cache write tokens, main thread (5m / 1h) | 0 / 194002 |
| Cache hit ratio | 0.9684 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 84 | 6149935 | 392 | 5955849 | 194002 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 26987 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 58 |
| Time to first token | 1.4s |
| Rate-limit peak | seven_day 0.34 |

## Session 5 — 2026-11-20T06:53:33.978Z → 2026-11-20T06:54:15.782Z

Session id: `8d00c893-3e32-4cc0-9d6f-b5f4532b8109`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 41.8s | 43.1s | 42.1s | 0.0s | 0.0s | 41.8s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 9 | 1.8s | 8.8s | 8.8s | 8.8s | 0 |
| orchestrator | 9 | 1.8s | 8.8s | 8.8s | 8.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 4 | 1.3s | 0.5s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 6 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:53:34.445Z | 0.5s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T06:54:01.105Z | 0.2s | 6 | false | false |
| Bash | orchestrator | 2026-11-20T06:53:40.395Z | 0.2s | 2364 | false | false |
| Bash | orchestrator | 2026-11-20T06:53:44.371Z | 0.2s | 13 | false | false |
| Edit | orchestrator | 2026-11-20T06:53:56.133Z | 0.0s | 158 | false | false |
| Edit | orchestrator | 2026-11-20T06:53:53.910Z | 0.0s | 158 | false | false |
| Edit | orchestrator | 2026-11-20T06:53:59.191Z | 0.0s | 158 | false | false |
| Write | orchestrator | 2026-11-20T06:54:04.786Z | 0.0s | 229 | false | false |
| Read | orchestrator | 2026-11-20T06:53:35.096Z | 0.0s | 3111 | false | false |
| Read | orchestrator | 2026-11-20T06:53:50.267Z | 0.0s | 1632 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.40 |
| Cost — claude-opus-5-5 | $0.40 |
| Input tokens (uncached) | 18 |
| Total input tokens (incl. cache) | 343115 |
| Output tokens | 4604 |
| Thinking tokens (main thread) | 639 |
| Cache read tokens | 312253 |
| Cache write tokens | 30844 |
| Cache write tokens, main thread (5m / 1h) | 0 / 30844 |
| Cache hit ratio | 0.9101 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 18 | 343115 | 131 | 312253 | 30844 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 4473 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 15 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.34 |

## Session 6 — 2026-11-20T06:54:19.410Z → 2026-11-20T06:56:22.454Z

Session id: `d6769cfc-555f-4d64-93bb-32d1c4f82e8a`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 03s | 2m 04s | 2m 01s | 0.0s | 0.0s | 2m 03s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 3.0s | 24.0s | 24.7s | 24.7s | 0 |
| orchestrator | 16 | 3.0s | 24.0s | 24.7s | 24.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 9 | 3.3s | 0.5s |
| Read | orchestrator | 21 | 0.9s | 0.4s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:54:19.965Z | 0.5s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:20.933Z | 0.4s | 1897 | false | false |
| Read | orchestrator | 2026-11-20T06:54:35.649Z | 0.4s | 57794 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:24.519Z | 0.3s | 1909 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:27.932Z | 0.3s | 1085 | false | false |
| Bash | orchestrator | 2026-11-20T06:54:22.990Z | 0.3s | 1047 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:16.739Z | 0.3s | 6218 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:33.261Z | 0.3s | 6037 | false | false |
| Bash | orchestrator | 2026-11-20T06:54:42.320Z | 0.2s | 836 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:58.794Z | 0.2s | 1197 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.58 |
| Cost — claude-opus-5-5 | $1.58 |
| Input tokens (uncached) | 32 |
| Total input tokens (incl. cache) | 1565451 |
| Output tokens | 12370 |
| Thinking tokens (main thread) | 6122 |
| Cache read tokens | 1435180 |
| Cache write tokens | 130239 |
| Cache write tokens, main thread (5m / 1h) | 0 / 130239 |
| Cache hit ratio | 0.9168 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 1565451 | 821 | 1435180 | 130239 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 11549 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 32 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.34 |

## Session 7 — 2026-11-20T06:54:19.900Z → 2026-11-20T06:59:35.829Z

Session id: `3569f5fc-cb3f-4456-be5d-c38d4050c33f`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 5m 15s | 5m 17s | 5m 08s | 0.0s | 0.0s | 5m 15s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 44 | 2.4s | 10.4s | 42.5s | 42.5s | 0 |
| orchestrator | 44 | 2.4s | 10.4s | 42.5s | 42.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 32 | 9.2s | 0.6s |
| Read | orchestrator | 28 | 0.9s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:57:34.546Z | 0.6s | 303 | false | false |
| Bash | orchestrator | 2026-11-20T06:54:20.405Z | 0.4s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:16.554Z | 0.4s | 3538 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:20.727Z | 0.4s | 1637 | false | false |
| Bash | orchestrator | 2026-11-20T06:55:09.482Z | 0.3s | 11197 | false | false |
| Bash | orchestrator | 2026-11-20T06:56:13.202Z | 0.3s | 1102 | false | false |
| Bash | orchestrator | 2026-11-20T06:54:22.850Z | 0.3s | 4990 | false | false |
| Bash | orchestrator | 2026-11-20T06:57:44.267Z | 0.3s | 463 | false | false |
| Bash | orchestrator | 2026-11-20T06:56:10.084Z | 0.3s | 2244 | false | false |
| Bash | orchestrator | 2026-11-20T06:58:48.276Z | 0.3s | 976 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.34 |
| Cost — claude-opus-5-5 | $3.34 |
| Input tokens (uncached) | 88 |
| Total input tokens (incl. cache) | 6344122 |
| Output tokens | 31417 |
| Thinking tokens (main thread) | 17151 |
| Cache read tokens | 6159593 |
| Cache write tokens | 184441 |
| Cache write tokens, main thread (5m / 1h) | 0 / 184441 |
| Cache hit ratio | 0.9709 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 88 | 6344122 | 1174 | 6159593 | 184441 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 30243 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 62 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.34 |

## Session 8 — 2026-11-20T06:59:45.975Z → 2026-11-20T07:00:46.406Z

Session id: `f2c62782-1792-4a3b-9931-05ebfd5924d7`

Planning node: `7-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 00s | 1m 01s | 1m 00s | 0.0s | 0.0s | 1m 00s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 8 | 2.3s | 8.6s | 8.6s | 8.6s | 0 |
| orchestrator | 8 | 2.3s | 8.6s | 8.6s | 8.6s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 4 | 1.4s | 0.5s |
| Edit | orchestrator | 3 | 0.1s | 0.0s |
| Read | orchestrator | 8 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T06:59:46.122Z | 0.5s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T07:00:09.680Z | 0.3s | 2171 | false | false |
| Bash | orchestrator | 2026-11-20T06:59:59.579Z | 0.2s | 3003 | false | false |
| Bash | orchestrator | 2026-11-20T06:59:50.074Z | 0.2s | 4592 | false | false |
| Write | orchestrator | 2026-11-20T07:00:35.627Z | 0.0s | 229 | false | false |
| Edit | orchestrator | 2026-11-20T07:00:30.827Z | 0.0s | 226 | false | false |
| Edit | orchestrator | 2026-11-20T07:00:23.107Z | 0.0s | 226 | false | false |
| Read | orchestrator | 2026-11-20T06:59:47.911Z | 0.0s | 3359 | false | false |
| Edit | orchestrator | 2026-11-20T07:00:27.924Z | 0.0s | 226 | false | false |
| Read | orchestrator | 2026-11-20T06:59:48.610Z | 0.0s | 9312 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.56 |
| Cost — claude-opus-5-5 | $0.56 |
| Input tokens (uncached) | 16 |
| Total input tokens (incl. cache) | 351873 |
| Output tokens | 6909 |
| Thinking tokens (main thread) | 1494 |
| Cache read tokens | 306745 |
| Cache write tokens | 45112 |
| Cache write tokens, main thread (5m / 1h) | 0 / 45112 |
| Cache hit ratio | 0.8717 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 16 | 351873 | 61 | 306745 | 45112 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 6848 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 17 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.34 |

## Session 9 — 2026-11-20T07:00:50.175Z → 2026-11-20T07:01:46.380Z

Session id: `dd4fa096-5281-4ca8-85ba-26e2a42fefe9`

Planning node: `8-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 56.2s | 58.0s | 55.3s | 0.0s | 0.0s | 56.2s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 12 | 2.1s | 10.4s | 10.9s | 10.9s | 0 |
| orchestrator | 12 | 2.1s | 10.4s | 10.9s | 10.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 7 | 2.3s | 0.6s |
| Read | orchestrator | 9 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T07:00:50.179Z | 0.6s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:15.840Z | 0.3s | 679 | false | false |
| Bash | orchestrator | 2026-11-20T07:00:58.954Z | 0.3s | 244 | false | false |
| Bash | orchestrator | 2026-11-20T07:00:52.887Z | 0.3s | 4034 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:07.021Z | 0.2s | 527 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:01.460Z | 0.2s | 6843 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:28.969Z | 0.1s | 31 | false | false |
| Write | orchestrator | 2026-11-20T07:01:40.140Z | 0.0s | 223 | false | false |
| Read | orchestrator | 2026-11-20T07:00:54.681Z | 0.0s | 9663 | false | false |
| Read | orchestrator | 2026-11-20T07:01:10.596Z | 0.0s | 10417 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.56 |
| Cost — claude-opus-5-5 | $0.56 |
| Input tokens (uncached) | 24 |
| Total input tokens (incl. cache) | 500809 |
| Output tokens | 5650 |
| Thinking tokens (main thread) | 1517 |
| Cache read tokens | 455829 |
| Cache write tokens | 44956 |
| Cache write tokens, main thread (5m / 1h) | 0 / 44956 |
| Cache hit ratio | 0.9102 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 24 | 500809 | 140 | 455829 | 44956 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 5510 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 18 |
| Time to first token | 1.7s |
| Rate-limit peak | seven_day 0.34 |

## Session 10 — 2026-11-20T07:00:50.205Z → 2026-11-20T07:02:23.321Z

Session id: `cfc0e066-382b-4b5f-8270-a44dd60da47e`

Planning node: `9-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 33s | 1m 34s | 1m 31s | 0.0s | 0.0s | 1m 33s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 2.3s | 7.5s | 10.0s | 10.0s | 0 |
| orchestrator | 17 | 2.3s | 7.5s | 10.0s | 10.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 3.1s | 0.5s |
| Read | orchestrator | 21 | 0.8s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T07:00:50.211Z | 0.5s | 53 | false | false |
| Bash | orchestrator | 2026-11-20T07:00:59.257Z | 0.4s | 566 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:56.338Z | 0.3s | 1097 | false | false |
| Read | orchestrator | 2026-11-20T07:01:09.568Z | 0.3s | 57794 | false | false |
| Bash | orchestrator | 2026-11-20T07:00:53.135Z | 0.3s | 4031 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:45.823Z | 0.2s | 2959 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:50.087Z | 0.2s | 969 | false | false |
| Bash | orchestrator | 2026-11-20T07:02:05.266Z | 0.2s | 31 | false | false |
| Bash | orchestrator | 2026-11-20T07:01:06.674Z | 0.2s | 867 | false | false |
| Read | orchestrator | 2026-11-20T07:01:16.581Z | 0.2s | 31668 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.47 |
| Cost — claude-opus-5-5 | $1.47 |
| Input tokens (uncached) | 34 |
| Total input tokens (incl. cache) | 1461445 |
| Output tokens | 9212 |
| Thinking tokens (main thread) | 2911 |
| Cache read tokens | 1334176 |
| Cache write tokens | 127235 |
| Cache write tokens, main thread (5m / 1h) | 0 / 127235 |
| Cache hit ratio | 0.9129 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 34 | 1461445 | 874 | 1334176 | 127235 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 8338 | 0 | 0 |

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
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.34 |

## Session 11 — 2026-11-20T07:02:59.340Z → 2026-11-20T09:14:07.026Z

Session id: `9c48f681-36c0-480a-ab78-5afef89cc69d`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2h11m | 2h11m | 48m 23s | 0.0s | 0.0s | 2h11m | 40m 53s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 588 | 2.1s | 7.8s | 27.3s | 50.2s | 0 |
| devscene:architecture-reviewer | 28 | 2.8s | 11.0s | 12.3s | 12.3s | 0 |
| devscene:branch-reviewer | 44 | 3.1s | 16.3s | 23.3s | 23.3s | 0 |
| devscene:layer-implementer | 195 | 2.6s | 8.4s | 46.8s | 47.8s | 0 |
| devscene:review-plan-reviewer | 41 | 2.7s | 8.5s | 17.5s | 17.5s | 0 |
| devscene:skeptic-reviewer | 41 | 3.7s | 10.6s | 21.4s | 21.4s | 0 |
| devscene:statistics-plan-writer | 6 | 1.7s | 16.3s | 16.3s | 16.3s | 0 |
| devscene:test-fix-plan-writer | 8 | 2.9s | 14.5s | 14.5s | 14.5s | 0 |
| orchestrator | 225 | 1.7s | 2.3s | 8.9s | 50.2s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 23 | 40m 53s | 4m 39s |
| Bash | devscene:architecture-reviewer | 21 | 5.5s | 0.3s |
| Bash | devscene:branch-reviewer | 31 | 8.2s | 1.4s |
| Bash | devscene:layer-implementer | 165 | 3m 35s | 17.6s |
| Bash | devscene:review-plan-reviewer | 30 | 8.2s | 0.4s |
| Bash | devscene:skeptic-reviewer | 29 | 8.2s | 1.0s |
| Bash | devscene:statistics-plan-writer | 8 | 1.7s | 0.3s |
| Bash | devscene:test-fix-plan-writer | 8 | 1.9s | 0.4s |
| Bash | orchestrator | 285 | 1h20m | 1m 06s |
| Edit | devscene:layer-implementer | 44 | 1.8s | 0.0s |
| Edit | orchestrator | 12 | 0.4s | 0.0s |
| Read | devscene:architecture-reviewer | 27 | 1.5s | 0.4s |
| Read | devscene:branch-reviewer | 29 | 1.2s | 0.3s |
| Read | devscene:layer-implementer | 61 | 3.6s | 0.4s |
| Read | devscene:review-plan-reviewer | 39 | 1.1s | 0.3s |
| Read | devscene:skeptic-reviewer | 19 | 0.9s | 0.4s |
| Read | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Read | devscene:test-fix-plan-writer | 5 | 0.0s | 0.0s |
| Read | orchestrator | 15 | 2.6s | 0.4s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 9 | 0.3s | 0.0s |
| Write | devscene:layer-implementer | 17 | 0.7s | 0.0s |
| Write | devscene:review-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:skeptic-reviewer | 2 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:test-fix-plan-writer | 3 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-20T08:36:42.695Z | 1m 06s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:49:32.308Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T08:35:34.236Z | 1m 04s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:48:25.791Z | 1m 03s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T08:53:51.009Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:54:56.959Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:53:52.252Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:50:40.098Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T08:44:15.010Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-20T07:59:12.897Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 14 | 1m 16s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 13 | 2.7s |
| devscene:layer-implementer | node <repo_root>/schemas/validate.mjs test -s <repo_root>/graphscene/src/graphscene/schemas/flow-graph.schema.json -d <repo_root>/graphscene/tests/fixtures/flow | 9 | 3.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 6 | 44.8s |
| devscene:review-plan-reviewer | git rev-parse --show-toplevel | 3 | 0.6s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit review_item --plan harness-runs/code_reviews/feat_flow_graph_schema_v2_code_review | 4 | 29.5s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_flow_graph_schema_v2_story_plan.md --id  | 6 | 41.7s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 38 | 38m 11s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 37 | 37m 37s |
| orchestrator | cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 23 | 6.3s |
| orchestrator | git status --short | 3 | 0.8s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null | 97 | 54.6s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 1 (cli) | 1m 44s | 15 | 9520 | 32 | 708173 | 652842 | 55299 | 0.0133 |
| devscene:layer-implementer | Implement Task 2 (graphscene) | 4m 02s | 27 | 27954 | 56 | 2102766 | 2017050 | 85660 | 0.0309 |
| devscene:layer-implementer | Implement Task 3 (graphscene) | 3m 49s | 24 | 27493 | 50 | 1592131 | 1524089 | 67992 | 0.0291 |
| devscene:layer-implementer | Implement Task 4 (general) | 4m 04s | 34 | 25032 | 70 | 3863536 | 3740309 | 123157 | 0.031 |
| devscene:layer-implementer | Implement Task 5 (general) | 1m 15s | 14 | 6501 | 30 | 847032 | 793172 | 53830 | 0.0096 |
| devscene:layer-implementer | Implement Task 6 (general) | 2m 07s | 24 | 11494 | 50 | 2361391 | 2260307 | 101034 | 0.0162 |
| devscene:architecture-reviewer | Architecture review of branch | 1m 53s | 19 | 10453 | 40 | 1810072 | 1673018 | 137014 | 0.0144 |
| devscene:branch-reviewer | End-of-branch code review | 4m 39s | 36 | 28978 | 74 | 5394734 | 5178715 | 215945 | 0.0355 |
| devscene:review-plan-reviewer | Meta-review code review | 2m 05s | 19 | 12342 | 40 | 1783098 | 1659635 | 123423 | 0.0159 |
| devscene:branch-reviewer | Adjust code review per meta-review | 1m 10s | 8 | 9051 | 18 | 327048 | 294814 | 32216 | 0.009 |
| devscene:review-plan-reviewer | Meta-review code review (round 2) | 1m 04s | 11 | 6156 | 24 | 587530 | 522630 | 64876 | 0.0081 |
| devscene:layer-implementer | Fix code-review Finding 4 | 29.4s | 7 | 2112 | 16 | 248340 | 214977 | 33347 | 0.0037 |
| devscene:layer-implementer | Fix code-review Finding 1 | 43.9s | 7 | 3941 | 16 | 369145 | 324323 | 44806 | 0.0056 |
| devscene:layer-implementer | Fix code-review Finding 2 | 35.4s | 7 | 2666 | 16 | 344753 | 308395 | 36342 | 0.0045 |
| devscene:layer-implementer | Fix code-review Finding 3 | 37.6s | 8 | 2587 | 18 | 400235 | 362718 | 37499 | 0.0048 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 4m 15s | 41 | 24292 | 84 | 3923093 | 3779290 | 143719 | 0.0325 |
| devscene:review-plan-reviewer | Meta-review skeptic review | 1m 03s | 11 | 6213 | 24 | 561186 | 494252 | 66910 | 0.0081 |
| devscene:layer-implementer | Fix skeptic Finding 1 | 39.0s | 9 | 3343 | 20 | 484922 | 425528 | 59374 | 0.005 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 1m 10s | 8 | 7616 | 18 | 295700 | 254772 | 40910 | 0.009 |
| devscene:architecture-reviewer | Review test fix plan round 1 | 59.6s | 9 | 5187 | 20 | 698238 | 591623 | 106595 | 0.0076 |
| devscene:layer-implementer | Fix test-fix Finding 1 | 1m 01s | 12 | 4193 | 26 | 613031 | 561670 | 51335 | 0.0078 |
| devscene:layer-implementer | Fix test-fix Finding 2 | 42.1s | 7 | 3356 | 16 | 250591 | 226061 | 24514 | 0.0054 |
| devscene:statistics-plan-writer | Write branch statistics | 37.1s | 6 | 4499 | 14 | 216631 | 182181 | 34436 | 0.0047 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $34.34 |
| Cost — claude-opus-5-5 | $34.34 |
| Input tokens (uncached) | 1222 |
| Total input tokens (incl. cache) | 87612167 |
| Output tokens | 299750 |
| Thinking tokens (main thread) | 4213 |
| Cache read tokens | 85554701 |
| Cache write tokens | 2056244 |
| Cache write tokens, main thread (5m / 1h) | 0 / 316011 |
| Cache hit ratio | 0.9765 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 450 | 57828791 | 5707 | 57512330 | 316011 |
| sub-agents | 772 | 29783376 | 244979 | 28042371 | 1740233 |
| remainder | 0 | 0 | 49064 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 20 |
| Sub-agents spawned / failed / killed | 23 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 338 |
| Time to first token | 2.1s |
| Rate-limit peak | seven_day 0.36 |
