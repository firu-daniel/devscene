# Run analytics — feat_flow_walker_python_cutover

## Whole run

| Measure | Value |
|---|---|
| Sessions | 11 (0 incomplete) |
| Engine / planning node sessions | 2 / 9 |
| Span | 1h59m |
| Wall | 1h58m |
| Session wall, summed over sessions | 2h03m |
| Active | 1h34m |
| Host-suspended | 0.0s |
| Idle | 23m 07s |
| Cost | $48.29 |
| Input tokens (uncached) | 1352 |
| Total input tokens (incl. cache) | 91789743 |
| Output tokens | 525504 |
| Thinking tokens (main thread) | 165674 |
| Cache read tokens | 88962615 |
| Cache write tokens | 2825776 |
| Cache write tokens, main thread (5m / 1h) | 0 / 1951453 |
| Cache hit ratio | 0.9692 |
| Requests | 666 |
| Request latency p50 / p90 / p99 / max | 3.2s / 11.6s / 39.5s / 1m 15s |
| Requests over the idle threshold | 0 |
| API retries | 0 |
| Permission denials | 22 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:layer-implementer — Implement Task 17 (cli) — 23m 54s (session 11) |
| Rate-limit peak | seven_day 0.1 |

Wall, Active, Host-suspended and Idle are the run's own: overlapping sessions' time counts once. The summed session wall counts each session's wall in full.

## Planning node sessions

| Session | Node | Wall | Active | Idle | duration_ms | Cost |
|---|---|---|---|---|---|---|
| 2 | 1-plan_writer | 16m 35s | 16m 35s | 0.0s | 16m 36s | $7.71 |
| 3 | 2-architecture_review | 2m 09s | 2m 09s | 0.0s | 2m 10s | $2.15 |
| 4 | 3-plan_review | 7m 10s | 7m 10s | 0.0s | 7m 11s | $5.60 |
| 5 | 4-plan_writer | 8m 23s | 8m 23s | 0.0s | 8m 24s | $3.03 |
| 6 | 5-architecture_review | 1m 59s | 1m 59s | 0.0s | 2m 00s | $2.11 |
| 7 | 6-plan_review | 9m 13s | 9m 13s | 0.0s | 9m 14s | $7.99 |
| 8 | 7-plan_writer | 53.2s | 53.2s | 0.0s | 54.3s | $0.51 |
| 9 | 8-architecture_review | 48.9s | 48.9s | 0.0s | 50.2s | $1.17 |
| 10 | 9-plan_review | 1m 19s | 1m 19s | 0.0s | 1m 19s | $0.75 |

## Network refusals

11 of 11 sessions scanned.

| Session | Context | Tool | Command | Host | Port | Refusal line |
|---|---|---|---|---|---|---|
| 11 | devscene:layer-implementer | Bash | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs test/retrieval-loading.test.mjs test/watcher-main-anchor.test.mjs test/agent-return-schemas.test.mjs test/python-packages-staged.test.mjs test/no-container-home-paths.test.mjs 2>&1 \| tail -15 | registry.npmjs.org | 443 | <sandbox_violations> |
| 11 | devscene:layer-implementer | Bash | npm test --workspace cli -- test/python-packages-staged.test.mjs 2>&1 \| grep -E '^# (tests\|pass\|fail\|skipped)\|^not ok' | registry.npmjs.org | 443 | <sandbox_violations> |

## Possible network attempts in gate logs (best effort)

Lines in finished Run gates logs that carry a proxy refusal string or a plain connect error (`ECONNREFUSED`, `ENETUNREACH`, `EHOSTUNREACH`, `EAI_AGAIN`). They are listed as possible attempts, not refusals. What this list cannot show:

- a test that catches the error and passes leaves no trace;
- a plain connect error cannot be told apart from a host that is unreachable for another reason;
- on macOS, Seatbelt's own violation records go to the system log, not to the test output;
- a test whose name or output quotes one of these strings is listed too.

No Run gates round log was scanned.

## Session 1 — 2026-11-24T21:48:01.047Z → 2026-11-24T21:48:54.793Z

Session id: `4f1e278d-f719-436d-aec8-daa1304d15c5`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 53.7s | 54.9s | 48.2s | 0.0s | 0.0s | 53.7s | 3.9s | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 17 | 1.4s | 2.1s | 4.7s | 4.7s | 0 |
| devscene:prompt-injection-reviewer | 1 | 1.3s | 1.3s | 1.3s | 1.3s | 0 |
| orchestrator | 16 | 1.5s | 2.1s | 4.7s | 4.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 1 | 3.9s | 3.9s |
| Bash | orchestrator | 14 | 7.3s | 4.9s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | orchestrator | 5 | 0.4s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | orchestrator | 2 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T21:48:45.117Z | 4.9s | 607 | false | false |
| Read | orchestrator | 2026-11-24T21:48:34.980Z | 0.3s | 26508 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:03.133Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:12.133Z | 0.2s | 159 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:33.451Z | 0.1s | 1267 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:27.488Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:25.135Z | 0.1s | 158 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:04.942Z | 0.1s | 10981 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:28.532Z | 0.1s | 31 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:04.186Z | 0.1s | 27 | false | false |

#### Polling loops

None.

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 3.9s | 1 | 374 | 4 | 33322 | 11212 | 22106 | 0.0743 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.95 |
| Cost — claude-opus-5-5 | $0.95 |
| Input tokens (uncached) | 36 |
| Total input tokens (incl. cache) | 1027237 |
| Output tokens | 5416 |
| Thinking tokens (main thread) | 372 |
| Cache read tokens | 936648 |
| Cache write tokens | 90553 |
| Cache write tokens, main thread (5m / 1h) | 0 / 68447 |
| Cache hit ratio | 0.9118 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 993915 | 290 | 925436 | 68447 |
| sub-agents | 4 | 33322 | 374 | 11212 | 22106 |
| remainder | 0 | 0 | 4752 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 1 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 25 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.08 |

## Session 2 — 2026-11-24T21:48:57.260Z → 2026-11-24T22:05:32.728Z

Session id: `2d83a1ce-3bff-4d04-8a94-adefc58a787b`

Planning node: `1-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 16m 35s | 16m 36s | 16m 24s | 0.0s | 0.0s | 16m 35s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 67 | 2.8s | 26.7s | 1m 15s | 1m 15s | 0 |
| orchestrator | 67 | 2.8s | 26.7s | 1m 15s | 1m 15s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 53 | 12.0s | 1.7s |
| Edit | orchestrator | 6 | 0.1s | 0.0s |
| Read | orchestrator | 22 | 1.3s | 0.2s |
| Write | orchestrator | 16 | 0.6s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T21:56:34.821Z | 1.7s | 4383 | false | false |
| Bash | orchestrator | 2026-11-24T21:49:32.335Z | 0.3s | 2408 | false | false |
| Bash | orchestrator | 2026-11-24T21:49:29.799Z | 0.3s | 2232 | false | false |
| Read | orchestrator | 2026-11-24T21:49:00.960Z | 0.2s | 63868 | false | false |
| Bash | orchestrator | 2026-11-24T21:58:21.758Z | 0.2s | 2064 | false | false |
| Bash | orchestrator | 2026-11-24T21:48:57.621Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T21:54:16.143Z | 0.2s | 1094 | false | false |
| Bash | orchestrator | 2026-11-24T21:50:34.709Z | 0.2s | 5792 | false | false |
| Bash | orchestrator | 2026-11-24T21:51:34.035Z | 0.2s | 4152 | false | false |
| Read | orchestrator | 2026-11-24T21:49:02.561Z | 0.2s | 30738 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $7.71 |
| Cost — claude-opus-5-5 | $7.71 |
| Input tokens (uncached) | 134 |
| Total input tokens (incl. cache) | 14202356 |
| Output tokens | 111161 |
| Thinking tokens (main thread) | 56763 |
| Cache read tokens | 13863463 |
| Cache write tokens | 338759 |
| Cache write tokens, main thread (5m / 1h) | 0 / 338759 |
| Cache hit ratio | 0.9761 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 134 | 14202356 | 632 | 13863463 | 338759 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 110529 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 98 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.08 |

## Session 3 — 2026-11-24T22:05:35.488Z → 2026-11-24T22:07:44.885Z

Session id: `52e3334c-e64a-42d0-a346-4a82af6d3053`

Planning node: `2-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 2m 09s | 2m 10s | 2m 08s | 0.0s | 0.0s | 2m 09s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 20 | 1.8s | 13.8s | 25.9s | 25.9s | 0 |
| orchestrator | 20 | 1.8s | 13.8s | 25.9s | 25.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 11 | 2.0s | 0.2s |
| Read | orchestrator | 30 | 0.6s | 0.2s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-24T22:06:02.252Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-24T22:05:35.903Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:26.527Z | 0.2s | 1572 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:35.781Z | 0.1s | 1783 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:44.444Z | 0.1s | 773 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:54.615Z | 0.1s | 1216 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:18.932Z | 0.1s | 3299 | false | false |
| Bash | orchestrator | 2026-11-24T22:05:57.325Z | 0.1s | 1095 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:29.443Z | 0.1s | 1171 | false | false |
| Bash | orchestrator | 2026-11-24T22:07:11.289Z | 0.1s | 31 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.15 |
| Cost — claude-opus-5-5 | $2.15 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 2530489 |
| Output tokens | 14754 |
| Thinking tokens (main thread) | 5549 |
| Cache read tokens | 2357543 |
| Cache write tokens | 172906 |
| Cache write tokens, main thread (5m / 1h) | 0 / 172906 |
| Cache hit ratio | 0.9317 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 40 | 2530489 | 925 | 2357543 | 172906 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 13829 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 43 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.08 |

## Session 4 — 2026-11-24T22:05:35.449Z → 2026-11-24T22:12:46.285Z

Session id: `71488728-52b6-458e-881c-d7b6c80e8fdc`

Planning node: `3-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 7m 10s | 7m 11s | 7m 03s | 0.0s | 0.0s | 7m 10s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 59 | 2.3s | 15.1s | 43.7s | 43.7s | 0 |
| orchestrator | 59 | 2.3s | 15.1s | 43.7s | 43.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 42 | 7.6s | 0.3s |
| Read | orchestrator | 39 | 1.4s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T22:05:35.820Z | 0.3s | 59 | false | false |
| Read | orchestrator | 2026-11-24T22:06:03.865Z | 0.3s | 63868 | false | false |
| Bash | orchestrator | 2026-11-24T22:07:40.944Z | 0.2s | 1425 | false | false |
| Bash | orchestrator | 2026-11-24T22:08:04.056Z | 0.2s | 1709 | false | false |
| Read | orchestrator | 2026-11-24T22:06:04.819Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-24T22:09:45.959Z | 0.2s | 3971 | false | false |
| Bash | orchestrator | 2026-11-24T22:09:31.851Z | 0.2s | 21423 | false | false |
| Read | orchestrator | 2026-11-24T22:05:42.853Z | 0.2s | 34952 | false | false |
| Bash | orchestrator | 2026-11-24T22:06:41.173Z | 0.2s | 364 | false | false |
| Bash | orchestrator | 2026-11-24T22:05:38.632Z | 0.2s | 18913 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $5.60 |
| Cost — claude-opus-5-5 | $5.60 |
| Input tokens (uncached) | 118 |
| Total input tokens (incl. cache) | 11949615 |
| Output tokens | 47174 |
| Thinking tokens (main thread) | 27672 |
| Cache read tokens | 11658800 |
| Cache write tokens | 290697 |
| Cache write tokens, main thread (5m / 1h) | 0 / 290697 |
| Cache hit ratio | 0.9757 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 118 | 11949615 | 579 | 11658800 | 290697 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 46595 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 2 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 83 |
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.08 |

## Session 5 — 2026-11-24T22:12:55.970Z → 2026-11-24T22:21:19.794Z

Session id: `3fb5a662-ec4f-4a29-a0b4-2c05811601b5`

Planning node: `4-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 8m 23s | 8m 24s | 8m 21s | 0.0s | 0.0s | 8m 23s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 38 | 2.2s | 27.5s | 36.4s | 36.4s | 0 |
| orchestrator | 38 | 2.2s | 27.5s | 36.4s | 36.4s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 20 | 3.7s | 0.2s |
| Edit | orchestrator | 17 | 0.5s | 0.0s |
| Read | orchestrator | 14 | 0.1s | 0.0s |
| Write | orchestrator | 7 | 0.2s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T22:12:56.491Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T22:15:43.878Z | 0.2s | 119 | false | false |
| Bash | orchestrator | 2026-11-24T22:13:46.131Z | 0.2s | 13239 | false | false |
| Bash | orchestrator | 2026-11-24T22:14:28.562Z | 0.2s | 3661 | false | false |
| Bash | orchestrator | 2026-11-24T22:15:36.931Z | 0.2s | 4454 | false | false |
| Bash | orchestrator | 2026-11-24T22:20:07.405Z | 0.2s | 1636 | false | false |
| Bash | orchestrator | 2026-11-24T22:14:26.287Z | 0.2s | 42 | false | false |
| Bash | orchestrator | 2026-11-24T22:16:19.514Z | 0.1s | 1772 | false | false |
| Bash | orchestrator | 2026-11-24T22:20:52.870Z | 0.1s | 3170 | false | false |
| Bash | orchestrator | 2026-11-24T22:14:03.196Z | 0.1s | 1728 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $3.03 |
| Cost — claude-opus-5-5 | $3.03 |
| Input tokens (uncached) | 76 |
| Total input tokens (incl. cache) | 3834209 |
| Output tokens | 61385 |
| Thinking tokens (main thread) | 23135 |
| Cache read tokens | 3701157 |
| Cache write tokens | 132976 |
| Cache write tokens, main thread (5m / 1h) | 0 / 132976 |
| Cache hit ratio | 0.9653 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 76 | 3834209 | 310 | 3701157 | 132976 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 61075 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 59 |
| Time to first token | 0.9s |
| Rate-limit peak | seven_day 0.08 |

## Session 6 — 2026-11-24T22:21:22.366Z → 2026-11-24T22:23:21.557Z

Session id: `e6c8ceeb-ef04-46c0-9f51-688a42761374`

Planning node: `5-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 59s | 2m 00s | 1m 58s | 0.0s | 0.0s | 1m 59s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 16 | 1.5s | 11.3s | 32.7s | 32.7s | 0 |
| orchestrator | 16 | 1.5s | 11.3s | 32.7s | 32.7s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 8 | 1.5s | 0.2s |
| Read | orchestrator | 31 | 1.1s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-24T22:21:32.711Z | 0.3s | 63868 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:22.893Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T22:22:35.646Z | 0.2s | 2694 | false | false |
| Read | orchestrator | 2026-11-24T22:21:35.618Z | 0.2s | 37125 | false | false |
| Read | orchestrator | 2026-11-24T22:21:35.082Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-24T22:22:44.813Z | 0.2s | 1651 | false | false |
| Bash | orchestrator | 2026-11-24T22:22:29.460Z | 0.1s | 5520 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:27.479Z | 0.1s | 2528 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:23.755Z | 0.1s | 8638 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:32.116Z | 0.1s | 7120 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $2.11 |
| Cost — claude-opus-5-5 | $2.11 |
| Input tokens (uncached) | 32 |
| Total input tokens (incl. cache) | 2100086 |
| Output tokens | 13628 |
| Thinking tokens (main thread) | 7007 |
| Cache read tokens | 1918675 |
| Cache write tokens | 181379 |
| Cache write tokens, main thread (5m / 1h) | 0 / 181379 |
| Cache hit ratio | 0.9136 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 32 | 2100086 | 941 | 1918675 | 181379 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 12687 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 41 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.08 |

## Session 7 — 2026-11-24T22:21:22.409Z → 2026-11-24T22:30:35.517Z

Session id: `e24db539-e8c5-4006-97f5-b60695efe9b2`

Planning node: `6-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 9m 13s | 9m 14s | 9m 04s | 0.0s | 0.0s | 9m 13s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 82 | 2.4s | 17.1s | 52.8s | 52.8s | 0 |
| orchestrator | 82 | 2.4s | 17.1s | 52.8s | 52.8s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 56 | 9.5s | 0.3s |
| Read | orchestrator | 64 | 1.7s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-24T22:22:04.619Z | 0.3s | 63868 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:22.795Z | 0.3s | 59 | false | false |
| Read | orchestrator | 2026-11-24T22:22:07.814Z | 0.2s | 37125 | false | false |
| Bash | orchestrator | 2026-11-24T22:23:08.749Z | 0.2s | 3700 | false | false |
| Read | orchestrator | 2026-11-24T22:22:07.270Z | 0.2s | 30738 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:30.981Z | 0.2s | 1573 | false | false |
| Bash | orchestrator | 2026-11-24T22:24:00.775Z | 0.2s | 446 | false | false |
| Bash | orchestrator | 2026-11-24T22:21:25.728Z | 0.2s | 19072 | false | false |
| Bash | orchestrator | 2026-11-24T22:25:18.477Z | 0.2s | 681 | false | false |
| Bash | orchestrator | 2026-11-24T22:23:27.143Z | 0.1s | 533 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $7.99 |
| Cost — claude-opus-5-5 | $7.99 |
| Input tokens (uncached) | 164 |
| Total input tokens (incl. cache) | 20468588 |
| Output tokens | 60212 |
| Thinking tokens (main thread) | 37779 |
| Cache read tokens | 20123489 |
| Cache write tokens | 344935 |
| Cache write tokens, main thread (5m / 1h) | 0 / 344935 |
| Cache hit ratio | 0.9831 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 164 | 20468588 | 1409 | 20123489 | 344935 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 58803 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 122 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.09 |

## Session 8 — 2026-11-24T22:30:44.730Z → 2026-11-24T22:31:37.991Z

Session id: `6e3f5542-335c-4def-a563-9869a8a74f7a`

Planning node: `7-plan_writer`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 53.2s | 54.3s | 53.1s | 0.0s | 0.0s | 53.2s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 11 | 1.3s | 1.9s | 7.0s | 7.0s | 0 |
| orchestrator | 11 | 1.3s | 1.9s | 7.0s | 7.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 5 | 1.0s | 0.2s |
| Edit | orchestrator | 5 | 0.1s | 0.0s |
| Read | orchestrator | 7 | 0.1s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T22:30:45.125Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T22:30:58.185Z | 0.2s | 2810 | false | false |
| Bash | orchestrator | 2026-11-24T22:30:53.261Z | 0.1s | 1563 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:27.279Z | 0.1s | 30 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:00.663Z | 0.1s | 880 | false | false |
| Write | orchestrator | 2026-11-24T22:31:30.847Z | 0.0s | 241 | false | false |
| Edit | orchestrator | 2026-11-24T22:31:06.912Z | 0.0s | 238 | false | false |
| Edit | orchestrator | 2026-11-24T22:31:18.207Z | 0.0s | 238 | false | false |
| Read | orchestrator | 2026-11-24T22:30:46.838Z | 0.0s | 2380 | false | false |
| Edit | orchestrator | 2026-11-24T22:31:20.363Z | 0.0s | 238 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.51 |
| Cost — claude-opus-5-5 | $0.51 |
| Input tokens (uncached) | 22 |
| Total input tokens (incl. cache) | 451785 |
| Output tokens | 6470 |
| Thinking tokens (main thread) | 463 |
| Cache read tokens | 414048 |
| Cache write tokens | 37715 |
| Cache write tokens, main thread (5m / 1h) | 0 / 37715 |
| Cache hit ratio | 0.9165 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 22 | 451785 | 856 | 414048 | 37715 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 5614 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 0 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 19 |
| Time to first token | 1.0s |
| Rate-limit peak | seven_day 0.09 |

## Session 9 — 2026-11-24T22:31:40.684Z → 2026-11-24T22:32:29.644Z

Session id: `e5366271-9146-4ad4-ae4b-c23876637069`

Planning node: `8-architecture_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 48.9s | 50.2s | 48.6s | 0.0s | 0.0s | 48.9s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 13 | 1.5s | 5.5s | 5.9s | 5.9s | 0 |
| orchestrator | 13 | 1.5s | 5.5s | 5.9s | 5.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 10 | 1.6s | 0.2s |
| Read | orchestrator | 12 | 0.9s | 0.3s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Read | orchestrator | 2026-11-24T22:32:00.451Z | 0.3s | 63868 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:41.105Z | 0.2s | 59 | false | false |
| Read | orchestrator | 2026-11-24T22:32:04.952Z | 0.2s | 30738 | false | false |
| Read | orchestrator | 2026-11-24T22:32:01.555Z | 0.2s | 37125 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:48.500Z | 0.1s | 189 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:43.358Z | 0.1s | 5432 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:06.606Z | 0.1s | 1385 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:57.307Z | 0.1s | 6071 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:15.086Z | 0.1s | 247 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:50.815Z | 0.1s | 8466 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $1.17 |
| Cost — claude-opus-5-5 | $1.17 |
| Input tokens (uncached) | 26 |
| Total input tokens (incl. cache) | 892146 |
| Output tokens | 5337 |
| Thinking tokens (main thread) | 1111 |
| Cache read tokens | 778092 |
| Cache write tokens | 114028 |
| Cache write tokens, main thread (5m / 1h) | 0 / 114028 |
| Cache hit ratio | 0.8722 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 26 | 892146 | 800 | 778092 | 114028 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 4537 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 1 |
| Sub-agents spawned / failed / killed | 0 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 24 |
| Time to first token | 1.1s |
| Rate-limit peak | seven_day 0.09 |

## Session 10 — 2026-11-24T22:31:40.290Z → 2026-11-24T22:32:59.367Z

Session id: `06a18245-e1d0-46a6-a62b-bb934d474366`

Planning node: `9-plan_review`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1m 19s | 1m 19s | 1m 16s | 0.0s | 0.0s | 1m 19s | — | none |

### Idle gaps (over 120 s)

None.

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 20 | 2.3s | 6.1s | 11.9s | 11.9s | 0 |
| orchestrator | 20 | 2.3s | 6.1s | 11.9s | 11.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Bash | orchestrator | 16 | 2.9s | 0.2s |
| Read | orchestrator | 4 | 0.0s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-24T22:31:40.679Z | 0.2s | 59 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:03.508Z | 0.2s | 6400 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:29.554Z | 0.2s | 6261 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:15.191Z | 0.1s | 959 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:20.722Z | 0.1s | 7903 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:24.544Z | 0.1s | 182 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:53.894Z | 0.1s | 10636 | false | false |
| Bash | orchestrator | 2026-11-24T22:32:01.716Z | 0.1s | 442 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:49.895Z | 0.1s | 8615 | false | false |
| Bash | orchestrator | 2026-11-24T22:31:42.867Z | 0.1s | 5343 | false | false |

#### Polling loops

None.

### Sub-agents

None.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $0.75 |
| Cost — claude-opus-5-5 | $0.75 |
| Input tokens (uncached) | 40 |
| Total input tokens (incl. cache) | 960817 |
| Output tokens | 8368 |
| Thinking tokens (main thread) | 2477 |
| Cache read tokens | 911002 |
| Cache write tokens | 49775 |
| Cache write tokens, main thread (5m / 1h) | 0 / 49775 |
| Cache hit ratio | 0.9482 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 40 | 960817 | 812 | 911002 | 49775 |
| sub-agents | 0 | 0 | 0 | 0 | 0 |
| remainder | 0 | 0 | 7556 | 0 | 0 |

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
| Time to first token | 0.7s |
| Rate-limit peak | seven_day 0.09 |

## Session 11 — 2026-11-24T22:33:29.860Z → 2026-11-24T23:47:06.977Z

Session id: `108ce193-1465-4b85-b751-c3788d2c9e1c`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h13m | 1h13m | 36m 21s | 0.0s | 23m 07s | 50m 29s | 1h08m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-24T23:03:58.315Z | 4m 13s | devscene:layer-implementer | tool_running |
| 2026-11-24T23:08:26.738Z | 4m 27s | devscene:layer-implementer | tool_running |
| 2026-11-24T23:13:12.669Z | 4m 28s | devscene:layer-implementer | tool_running |
| 2026-11-24T23:27:57.944Z | 3m 19s | devscene:layer-implementer | tool_running |
| 2026-11-24T23:31:26.188Z | 3m 20s | devscene:layer-implementer | tool_running |
| 2026-11-24T23:35:21.412Z | 3m 17s | devscene:layer-implementer | tool_running |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 323 | 4.2s | 9.1s | 35.1s | 48.6s | 0 |
| devscene:layer-implementer | 269 | 4.5s | 9.5s | 37.7s | 48.6s | 0 |
| orchestrator | 54 | 2.9s | 5.6s | 14.9s | 14.9s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 9 | 1h08m | 23m 54s |
| Bash | devscene:layer-implementer | 207 | 55m 12s | 4m 28s |
| Bash | orchestrator | 41 | 54.7s | 7.7s |
| Edit | devscene:layer-implementer | 85 | 2.8s | 0.0s |
| Read | devscene:layer-implementer | 89 | 2.7s | 0.4s |
| Read | orchestrator | 11 | 2.0s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:layer-implementer | 5 | 0.2s | 0.0s |
| Write | orchestrator | 1 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | devscene:layer-implementer | 2026-11-24T23:13:12.669Z | 4m 28s | 137 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:08:26.738Z | 4m 27s | 1718 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:03:58.315Z | 4m 13s | 10040 | true | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:35:21.412Z | 3m 41s | 14414 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:35:20.681Z | 3m 39s | 942 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:35:19.881Z | 3m 29s | 561 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:35:19.030Z | 3m 24s | 767 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:35:18.335Z | 3m 20s | 2510 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:31:26.188Z | 3m 20s | 2507 | false | false |
| Bash | devscene:layer-implementer | 2026-11-24T23:27:57.944Z | 3m 19s | 7568 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:layer-implementer | bash scripts/typecheck.sh | 6 | 43.8s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.4s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 5 | 3m 37s |
| devscene:layer-implementer | npm test --workspace cli -- test/planning-driver-walk.test.mjs | 3 | 10m 01s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> --push --unit task --plan harness-runs/story_plans/feat_flow_walker_python_cutover_story_plan.md | 8 | 49.6s |
| orchestrator | ls <repo_root>/harness-runs/STOP <repo_root>/harness-runs/PAUSE <main_repo>/harness-runs/AUTONOMOUS_STOP 2>/dev/null; cat <repo_root>/harness-runs/.dispatch_cou | 8 | 1.3s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:layer-implementer | Implement Task 3 (cli) | 5m 49s | 43 | 26419 | 88 | 4300332 | 4179758 | 120486 | 0.0791 |
| devscene:layer-implementer | Implement Task 4 (cli) | 5m 39s | 36 | 28068 | 74 | 2613667 | 2527485 | 86108 | 0.0768 |
| devscene:layer-implementer | Implement Task 1 (cli) | 4m 46s | 32 | 22566 | 66 | 3152800 | 3030735 | 121999 | 0.0649 |
| devscene:layer-implementer | Implement Task 2 (cli) | 3m 05s | 19 | 17963 | 40 | 1584076 | 1498628 | 85408 | 0.0421 |
| devscene:layer-implementer | Implement Task 16 (cli) | 3m 43s | 25 | 17982 | 52 | 1575660 | 1502330 | 73278 | 0.0505 |
| devscene:layer-implementer | Implement Task 17 (cli) | 23m 54s | 49 | 26841 | 100 | 5562226 | 5420573 | 141553 | 0.3247 |
| devscene:layer-implementer | Implement Task 5 (cli) | 2m 19s | 15 | 8922 | 32 | 729432 | 685660 | 43740 | 0.0316 |
| devscene:layer-implementer | Implement Task 6 (cli) | 12m 38s | 24 | 11104 | 50 | 1487559 | 1414453 | 73056 | 0.1718 |
| devscene:layer-implementer | Implement Task 7 (cli) | 6m 31s | 26 | 12892 | 54 | 2560417 | 2453774 | 106589 | 0.0887 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $16.31 |
| Cost — claude-opus-5-5 | $16.31 |
| Input tokens (uncached) | 664 |
| Total input tokens (incl. cache) | 33372415 |
| Output tokens | 191599 |
| Thinking tokens (main thread) | 3346 |
| Cache read tokens | 32299698 |
| Cache write tokens | 1072053 |
| Cache write tokens, main thread (5m / 1h) | 0 / 219836 |
| Cache hit ratio | 0.9679 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 108 | 9806246 | 1539 | 9586302 | 219836 |
| sub-agents | 556 | 23566169 | 172757 | 22713396 | 852217 |
| remainder | 0 | 0 | 17303 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 16 |
| Sub-agents spawned / failed / killed | 9 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 65 |
| Time to first token | 1.3s |
| Rate-limit peak | seven_day 0.1 |
