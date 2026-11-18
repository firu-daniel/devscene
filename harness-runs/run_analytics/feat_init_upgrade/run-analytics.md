# Run analytics — feat_init_upgrade

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Engine / planning node sessions | 1 / 0 |
| Span | 55.7s |
| Wall | 55.7s |
| Session wall, summed over sessions | 55.7s |
| Active | 55.7s |
| Host-suspended | 0.0s |
| Idle | 0.0s |
| Cost | $0.78 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 628146 |
| Output tokens | 5954 |
| Thinking tokens (main thread) | 1244 |
| Cache read tokens | 552497 |
| Cache write tokens | 75621 |
| Cache write tokens, main thread (5m / 1h) | 0 / 57389 |
| Cache hit ratio | 0.8796 |
| Requests | 12 |
| Request latency p50 / p90 / p99 / max | 1.9s / 4.9s / 11.4s / 11.4s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:prompt-injection-reviewer — Screen user review file — 8.6s (session 1) |
| Rate-limit peak | seven_day 0.22 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Network refusals

1 of 1 sessions scanned.

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
| Wait (every run of task_round_1) | — |
| Gate rows | 28 (complete) |
| Test files — full | 219 files, 7639.5 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 1 s |
| full | 2a | ok | 2 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 0 s |
| full | 3b | ok | 1 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 988 s |
| full | 6a | ok | 1 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 9 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 1 s |
| full | 14d | ok | 1 s |
| full | 16 | ok | 1 s |

#### Slowest test files — full (10 of 219)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/remote-run.test.mjs | pass | 358.0 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 331.1 | 29 | 0 |
| test/remote-control.test.mjs | pass | 323.3 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 302.5 | 33 | 0 |
| test/doctor.test.mjs | pass | 267.6 | 1 | 0 |
| test/planning-driver-control.test.mjs | pass | 249.1 | 15 | 0 |
| test/remote-trigger.test.mjs | pass | 229.1 | 37 | 0 |
| test/remote-control-mention.test.mjs | pass | 224.3 | 47 | 0 |
| test/run-test-suite.test.mjs | pass | 212.3 | 50 | 0 |
| test/watcher-review-drop-payloads.test.mjs | pass | 205.9 | 21 | 0 |

## Session 1 — 2026-11-18T14:09:44.456Z → 2026-11-18T14:10:40.181Z

Session id: `be953955-20a0-448c-93ae-b8ed2dc69ac0`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 55.7s | 57.6s | 56.2s | 0.0s | 0.0s | 55.7s | 8.6s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 12 | 1.9s | 4.9s | 11.4s | 11.4s | 0 |
| devscene:prompt-injection-reviewer | 2 | 1.2s | 4.5s | 4.5s | 4.5s | 0 |
| orchestrator | 10 | 1.9s | 11.4s | 11.4s | 11.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 8.6s | 8.6s |
| Bash | orchestrator | 13 | 2.2s | 0.2s |
| Grep | devscene:prompt-injection-reviewer | 2 | 0.1s | 0.1s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.1s | 0.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-18T14:09:48.324Z | 0.2s | 2046 | false | false |
| Bash | orchestrator | 2026-11-18T14:10:28.542Z | 0.2s | 56 | false | false |
| Bash | orchestrator | 2026-11-18T14:10:15.145Z | 0.2s | 95 | true | false |
| Bash | orchestrator | 2026-11-18T14:09:57.876Z | 0.1s | 269 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:50.471Z | 0.1s | 56 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:55.483Z | 0.1s | 32 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:52.219Z | 0.1s | 6276 | true | false |
| Bash | orchestrator | 2026-11-18T14:09:49.971Z | 0.1s | 17 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:48.822Z | 0.1s | 45 | false | false |
| Bash | orchestrator | 2026-11-18T14:09:49.522Z | 0.1s | 27 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen user review file | 8.6s | 2 | 903 | 6 | 45677 | 27439 | 18232 | 0.1551 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.78 |
| Cost — claude-opus-5-5 | $0.78 |
| Input tokens (uncached) | 28 |
| Total input tokens (incl. cache) | 628146 |
| Output tokens | 5954 |
| Thinking tokens (main thread) | 1244 |
| Cache read tokens | 552497 |
| Cache write tokens | 75621 |
| Cache write tokens, main thread (5m / 1h) | 0 / 57389 |
| Cache hit ratio | 0.8796 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 22 | 582469 | 92 | 525058 | 57389 |
| sub-agents | 6 | 45677 | 903 | 27439 | 18232 |
| remainder | 0 | 0 | 4959 | 0 | 0 |

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
| Time to first token | 1.8s |
| Rate-limit peak | seven_day 0.22 |
