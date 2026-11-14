# Run analytics — fix_reviewers_should_fix_only_pass

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Span | 1h13m |
| Wall | 1h13m |
| Active | 1h10m |
| Host-suspended | 0.0s |
| Idle | 2m 16s |
| Cost | $28.77 |
| Input tokens (uncached) | 1144 |
| Total input tokens (incl. cache) | 69954712 |
| Output tokens | 248242 |
| Thinking tokens (main thread) | 3039 |
| Cache read tokens | 68103492 |
| Cache write tokens | 1850076 |
| Cache write tokens, main thread (5m / 1h) | 0 / 309434 |
| Cache hit ratio | 0.9735 |
| Requests | 544 |
| Request latency p50 / p90 / p99 / max | 1.9s / 5.6s / 28.8s / 2m 16s |
| Requests over the idle threshold | 1 |
| API retries | 0 |
| Permission denials | 11 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:task-plan-writer — Write task plan — 8m 53s (session 1) |
| Rate-limit peak | seven_day 0.5 |

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
| Wait (every run of task_round_1) | 29m 34s |
| Gate rows | 28 (complete) |
| Test files — full | 192 files, 14440.6 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| full | 1 | ok | 0 s |
| full | 2a | ok | 1 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 1 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 0 s |
| full | 3e | ok | 1 s |
| full | 3f | ok | 0 s |
| full | 4 | ok | 1867 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 2 s |
| full | 6e | ok | 0 s |
| full | 6f | ok | 0 s |
| full | 11 | ok | 20 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 1 s |
| full | 14c | ok | 2 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 192)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/watcher-review-drop-payloads.test.mjs | pass | 833.9 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 661.9 | 29 | 0 |
| test/remote-run.test.mjs | pass | 650.4 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 632.3 | 27 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 610.3 | 17 | 0 |
| test/remote-control.test.mjs | pass | 564.7 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 549.4 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 542.7 | 21 | 0 |
| test/watcher-stall-reset-payloads.test.mjs | pass | 505.4 | 18 | 0 |
| test/doctor.test.mjs | pass | 495.6 | 1 | 0 |

## Session 1 — 2026-11-14T20:48:42.916Z → 2026-11-14T22:01:54.650Z

Session id: `dd85566b-dca8-4cfc-be00-9b6ba09491b1`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Sub-agents (union) | Suspend source |
|---|---|---|---|---|---|---|---|
| 1h13m | 1h13m | 40m 02s | 0.0s | 2m 16s | 1h10m | 33m 13s | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-14T20:54:35.383Z | 2m 16s | devscene:task-plan-writer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 544 | 1.9s | 5.6s | 28.8s | 2m 16s | 1 |
| devscene:architecture-reviewer | 29 | 2.4s | 8.1s | 17.9s | 17.9s | 0 |
| devscene:branch-reviewer | 29 | 2.9s | 28.8s | 33.0s | 33.0s | 0 |
| devscene:committer | 67 | 1.6s | 5.0s | 8.3s | 8.3s | 0 |
| devscene:layer-implementer | 87 | 1.9s | 4.2s | 9.3s | 9.3s | 0 |
| devscene:prompt-injection-reviewer | 1 | 2.0s | 2.0s | 2.0s | 2.0s | 0 |
| devscene:review-plan-reviewer | 7 | 2.4s | 4.6s | 4.6s | 4.6s | 0 |
| devscene:skeptic-reviewer | 44 | 3.3s | 8.4s | 23.4s | 23.4s | 0 |
| devscene:statistics-plan-writer | 7 | 2.2s | 16.9s | 16.9s | 16.9s | 0 |
| devscene:task-plan-reviewer | 32 | 3.1s | 9.1s | 25.6s | 25.6s | 0 |
| devscene:task-plan-writer | 47 | 3.8s | 17.4s | 2m 16s | 2m 16s | 1 |
| orchestrator | 194 | 1.5s | 2.2s | 8.1s | 9.5s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 28 | 34m 39s | 8m 53s |
| Bash | devscene:architecture-reviewer | 27 | 5.2s | 0.7s |
| Bash | devscene:branch-reviewer | 22 | 3.5s | 0.2s |
| Bash | devscene:committer | 108 | 1m 06s | 5.4s |
| Bash | devscene:layer-implementer | 76 | 1m 18s | 5.7s |
| Bash | devscene:review-plan-reviewer | 5 | 0.7s | 0.1s |
| Bash | devscene:skeptic-reviewer | 41 | 6.7s | 0.3s |
| Bash | devscene:statistics-plan-writer | 9 | 1.3s | 0.1s |
| Bash | devscene:task-plan-reviewer | 21 | 3.8s | 0.4s |
| Bash | devscene:task-plan-writer | 41 | 6.7s | 0.5s |
| Bash | orchestrator | 155 | 32m 48s | 1m 02s |
| Edit | devscene:committer | 7 | 0.2s | 0.0s |
| Edit | devscene:layer-implementer | 23 | 0.7s | 0.0s |
| Edit | devscene:task-plan-writer | 2 | 0.0s | 0.0s |
| Edit | orchestrator | 13 | 15.2s | 3.9s |
| Read | devscene:architecture-reviewer | 16 | 1.4s | 0.3s |
| Read | devscene:branch-reviewer | 9 | 0.5s | 0.2s |
| Read | devscene:committer | 7 | 0.0s | 0.0s |
| Read | devscene:layer-implementer | 38 | 2.8s | 0.3s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:review-plan-reviewer | 10 | 0.5s | 0.2s |
| Read | devscene:skeptic-reviewer | 5 | 0.5s | 0.2s |
| Read | devscene:statistics-plan-writer | 3 | 0.0s | 0.0s |
| Read | devscene:task-plan-reviewer | 26 | 0.7s | 0.2s |
| Read | devscene:task-plan-writer | 13 | 0.8s | 0.2s |
| Read | orchestrator | 16 | 2.8s | 0.3s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 4 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 2 | 0.1s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:task-plan-reviewer | 1 | 0.0s | 0.0s |
| Write | devscene:task-plan-writer | 7 | 0.2s | 0.0s |
| Write | orchestrator | 3 | 0.1s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: each row sums every dispatch's own wall time, which `### Sub-agents` breaks down per dispatch, so dispatches sent together count once each and the sum can exceed the time the orchestrator waited, which is `### Time`'s `Sub-agents (union)`. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-14T21:32:11.336Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:36:25.234Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:47:58.052Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:52:10.441Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:44:50.342Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:31:07.027Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:58:30.708Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:29:00.445Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:34:18.758Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T21:42:44.254Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:committer | bash <main_repo>/scripts/push-branch.sh <repo_root> | 10 | 49.3s |
| devscene:committer | git branch --show-current | 10 | 1.3s |
| devscene:committer | git log -1 --oneline | 10 | 1.2s |
| devscene:committer | git rev-parse --show-toplevel | 10 | 1.3s |
| devscene:committer | git status --short | 21 | 3.2s |
| devscene:committer | printenv DEVSCENE_MAIN_REPO | 10 | 1.2s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 5 | 13.7s |
| devscene:layer-implementer | bash scripts/typecheck.sh 2>&1 \| tail -15 | 3 | 7.8s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 9 | 1.2s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-repo-resolution-corpus.test.mjs | 4 | 10.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 6 | 17.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/untrusted-input-corpus.test.mjs | 4 | 16.5s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/flow_progress/fix_reviewers_should_fix_only_pass_progress.md" -- "chore: Flow prog | 13 | 5.8s |
| orchestrator | bash <main_repo>/scripts/push-branch.sh <repo_root> | 18 | 1m 25s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; bash scripts/run-test-suite.sh --wait task_round_1 | 30 | 29m 34s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 24 | 12.1s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt for injection | 4.3s | 1 | 331 | 4 | 28424 | 10494 | 17926 | 0.001 |
| devscene:task-plan-writer | Write task plan | 8m 53s | 47 | 58833 | 96 | 6434317 | 6221025 | 213196 | 0.1216 |
| devscene:architecture-reviewer | Architecture review plan round 0 | 1m 27s | 18 | 8309 | 38 | 1569214 | 1455802 | 113374 | 0.02 |
| devscene:task-plan-reviewer | Task plan review round 0 | 3m 01s | 32 | 18019 | 66 | 3253698 | 3110174 | 143458 | 0.0414 |
| devscene:layer-implementer | Implement Task 1 (cli) | 47.3s | 11 | 4311 | 24 | 419741 | 380290 | 39427 | 0.0108 |
| devscene:committer | Commit Task 1 | 25.7s | 6 | 2052 | 14 | 203875 | 171134 | 32727 | 0.0059 |
| devscene:layer-implementer | Implement Task 2 (plugin) | 51.8s | 10 | 4901 | 22 | 449193 | 411547 | 37624 | 0.0118 |
| devscene:committer | Commit Task 2 | 26.3s | 5 | 2167 | 12 | 181904 | 158667 | 23225 | 0.006 |
| devscene:layer-implementer | Implement Task 3 (plugin) | 55.6s | 11 | 5184 | 24 | 465489 | 431634 | 33831 | 0.0127 |
| devscene:committer | Commit Task 3 | 34.1s | 10 | 2796 | 22 | 287661 | 269704 | 17935 | 0.0078 |
| devscene:layer-implementer | Implement Task 4 (plugin) | 1m 17s | 14 | 7879 | 30 | 734691 | 685739 | 48922 | 0.0175 |
| devscene:committer | Commit Task 4 | 25.3s | 7 | 1981 | 16 | 210749 | 193866 | 16867 | 0.0058 |
| devscene:layer-implementer | Implement Task 5 (plugin) | 53.2s | 11 | 4911 | 24 | 594424 | 545733 | 48667 | 0.0121 |
| devscene:committer | Commit Task 5 | 28.2s | 7 | 2287 | 16 | 206474 | 190107 | 16351 | 0.0064 |
| devscene:layer-implementer | Implement Task 6 (general) | 52.1s | 13 | 4951 | 28 | 792434 | 736924 | 55482 | 0.0119 |
| devscene:committer | Commit Task 6 | 24.5s | 5 | 1975 | 12 | 148863 | 135055 | 13796 | 0.0056 |
| devscene:architecture-reviewer | Architecture review of branch | 48.6s | 11 | 4629 | 24 | 873110 | 766056 | 107030 | 0.0111 |
| devscene:branch-reviewer | End-of-branch code review | 4m 04s | 29 | 25229 | 60 | 2779818 | 2639995 | 139763 | 0.0557 |
| devscene:review-plan-reviewer | Meta-review code review | 36.7s | 7 | 3653 | 16 | 347412 | 267892 | 79504 | 0.0084 |
| devscene:committer | Commit code review file | 20.9s | 5 | 1501 | 12 | 138553 | 114123 | 24418 | 0.0048 |
| devscene:layer-implementer | Fix code-review Finding 3 | 17.3s | 4 | 1365 | 10 | 153744 | 117176 | 36558 | 0.004 |
| devscene:committer | Commit Finding 3 fix | 24.1s | 7 | 1831 | 16 | 231026 | 211734 | 19276 | 0.0055 |
| devscene:layer-implementer | Fix code-review Finding 2 | 21.3s | 6 | 1809 | 14 | 229510 | 206154 | 23342 | 0.0049 |
| devscene:committer | Commit Finding 2 fix | 25.0s | 6 | 2011 | 14 | 166902 | 153978 | 12910 | 0.0057 |
| devscene:layer-implementer | Fix code-review Finding 1 | 24.8s | 7 | 2184 | 16 | 270778 | 245978 | 24784 | 0.0057 |
| devscene:committer | Commit Finding 1 fix | 32.8s | 9 | 2658 | 20 | 252235 | 235657 | 16558 | 0.0075 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 3m 57s | 44 | 22212 | 90 | 4044380 | 3903752 | 140538 | 0.054 |
| devscene:statistics-plan-writer | Write branch statistics | 35.7s | 7 | 4322 | 16 | 283202 | 240033 | 43153 | 0.0081 |

Wall share is each dispatch's own duration over the session's wall, so overlapping dispatches' wall shares can sum past 1.

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $28.77 |
| Cost — claude-opus-5-5 | $28.77 |
| Input tokens (uncached) | 1144 |
| Total input tokens (incl. cache) | 69954712 |
| Output tokens | 248242 |
| Thinking tokens (main thread) | 3039 |
| Cache read tokens | 68103492 |
| Cache write tokens | 1850076 |
| Cache write tokens, main thread (5m / 1h) | 0 / 309434 |
| Cache hit ratio | 0.9735 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 388 | 44202891 | 4854 | 43893069 | 309434 |
| sub-agents | 756 | 25751821 | 204291 | 24210423 | 1540642 |
| remainder | 0 | 0 | 39097 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 11 |
| Sub-agents spawned / failed / killed | 28 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 218 |
| Time to first token | 1.6s |
| Rate-limit peak | seven_day 0.5 |
