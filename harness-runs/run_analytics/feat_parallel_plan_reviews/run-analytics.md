# Run analytics — feat_parallel_plan_reviews

## Whole run

| Measure | Value |
|---|---|
| Sessions | 1 (0 incomplete) |
| Span | 3h39m |
| Wall | 3h39m |
| Active | 3h35m |
| Host-suspended | 0.0s |
| Idle | 4m 12s |
| Cost | $88.05 |
| Input tokens (uncached) | 3310 |
| Total input tokens (incl. cache) | 214116309 |
| Output tokens | 929296 |
| Thinking tokens (main thread) | 6050 |
| Cache read tokens | 208826978 |
| Cache write tokens | 5286021 |
| Cache write tokens, main thread (5m / 1h) | 0 / 420044 |
| Cache hit ratio | 0.9753 |
| Requests | 1576 |
| Request latency p50 / p90 / p99 / max | 2.0s / 7.4s / 34.4s / 2m 06s |
| Requests over the idle threshold | 2 |
| API retries | 0 |
| Permission denials | 41 |
| Sub-agents failed / killed | 0 / 0 |
| Slowest sub-agent | devscene:task-plan-writer — Write task plan — 23m 05s (session 1) |
| Rate-limit peak | seven_day 0.48 |

## Network refusals

1 of 1 sessions scanned.

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
| Wait (every run of task_round_1) | 30m 26s |
| Gate rows | 28 (complete) |
| Test files — full | 192 files, 15068.2 s summed |

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
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 1928 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 2 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 6f | FAIL | 0 s |
| full | 11 | ok | 17 s |
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
| test/watcher-review-drop-payloads.test.mjs | pass | 788.0 | 21 | 0 |
| test/remote-run.test.mjs | pass | 646.9 | 130 | 0 |
| test/watcher-remote-job.test.mjs | pass | 625.4 | 29 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 602.6 | 27 | 0 |
| test/doctor.test.mjs | pass | 577.2 | 1 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 575.8 | 17 | 0 |
| test/remote-control.test.mjs | pass | 565.1 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 548.2 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 511.5 | 21 | 0 |
| test/watcher-stall-reset-payloads.test.mjs | pass | 467.4 | 18 | 0 |

### Round task_round_2 — pass

| Measure | Value |
|---|---|
| Wait (every run of task_round_2) | 33m 07s |
| Gate rows | 28 (complete) |
| Test files — full | 192 files, 16012.8 s summed |

| Phase | Gate | Status | Seconds |
|---|---|---|---|
| focused | 6f | ok | 0 s |
| full | 1 | ok | 0 s |
| full | 2a | ok | 3 s |
| full | 2b | ok | 0 s |
| full | 2c | ok | 0 s |
| full | 2d | ok | 0 s |
| full | 2e | ok | 0 s |
| full | 3a | ok | 1 s |
| full | 3b | ok | 2 s |
| full | 3c | ok | 1 s |
| full | 3d | ok | 1 s |
| full | 3e | ok | 0 s |
| full | 3f | ok | 1 s |
| full | 4 | ok | 2036 s |
| full | 6a | ok | 2 s |
| full | 6b | ok | 0 s |
| full | 6c | ok | 1 s |
| full | 6d | ok | 3 s |
| full | 6e | ok | 0 s |
| full | 11 | ok | 16 s |
| full | 13a | BLOCKED | 0 s |
| full | 13b | BLOCKED | 0 s |
| full | 13c | BLOCKED | 0 s |
| full | 13d | SKIPPED | 0 s |
| full | 14a | ok | 2 s |
| full | 14c | ok | 1 s |
| full | 14d | SKIPPED | 0 s |
| full | 16 | ok | 2 s |

#### Slowest test files — full (10 of 192)

| File | Status | Seconds | Tests | Failed |
|---|---|---|---|---|
| test/watcher-review-drop-payloads.test.mjs | pass | 815.2 | 21 | 0 |
| test/watcher-remote-job.test.mjs | pass | 652.2 | 29 | 0 |
| test/remote-run.test.mjs | pass | 649.8 | 130 | 0 |
| test/watcher-placeholder-host.test.mjs | pass | 629.8 | 27 | 0 |
| test/doctor.test.mjs | pass | 614.9 | 1 | 0 |
| test/watcher-remote-dispatch.test.mjs | pass | 603.7 | 17 | 0 |
| test/remote-control.test.mjs | pass | 565.2 | 83 | 0 |
| test/remote-control-review.test.mjs | pass | 549.7 | 33 | 0 |
| test/watcher-run-profile.test.mjs | pass | 537.1 | 21 | 0 |
| test/watcher-stall-reset-payloads.test.mjs | pass | 491.2 | 18 | 0 |

## Session 1 — 2026-11-14T16:24:58.414Z → 2026-11-14T20:04:51.704Z

Session id: `f1f60ee7-8efd-4bbb-ae22-dc362e00847c`

### Time

| Wall | duration_ms | duration_api_ms | Host-suspended | Idle | Active | Suspend source |
|---|---|---|---|---|---|---|
| 3h39m | 3h39m | 2h20m | 0.0s | 4m 12s | 3h35m | none |

### Idle gaps (over 120 s)

| Start | Length | Context | Class |
|---|---|---|---|
| 2026-11-14T17:23:02.270Z | 2m 06s | devscene:layer-implementer | in_flight_request |
| 2026-11-14T18:18:51.873Z | 2m 06s | devscene:layer-implementer | in_flight_request |

### Request latency

| Context | Requests | p50 | p90 | p99 | Max | Over threshold |
|---|---|---|---|---|---|---|
| all | 1576 | 2.0s | 7.4s | 34.4s | 2m 06s | 2 |
| devscene:architecture-reviewer | 75 | 2.2s | 8.8s | 37.0s | 37.0s | 0 |
| devscene:branch-reviewer | 43 | 3.6s | 21.1s | 28.0s | 28.0s | 0 |
| devscene:committer | 250 | 1.6s | 4.3s | 6.2s | 6.7s | 0 |
| devscene:layer-implementer | 511 | 2.2s | 5.9s | 40.6s | 2m 06s | 2 |
| devscene:prompt-injection-reviewer | 1 | 1.2s | 1.2s | 1.2s | 1.2s | 0 |
| devscene:review-plan-reviewer | 18 | 2.3s | 7.1s | 7.9s | 7.9s | 0 |
| devscene:skeptic-reviewer | 38 | 2.7s | 17.7s | 30.7s | 30.7s | 0 |
| devscene:statistics-plan-writer | 9 | 1.9s | 18.2s | 18.2s | 18.2s | 0 |
| devscene:task-plan-reviewer | 138 | 3.5s | 17.3s | 33.5s | 33.6s | 0 |
| devscene:task-plan-writer | 156 | 4.7s | 21.2s | 1m 14s | 1m 30s | 0 |
| devscene:test-fix-plan-writer | 14 | 2.1s | 4.3s | 9.3s | 9.3s | 0 |
| orchestrator | 323 | 1.4s | 2.0s | 6.7s | 8.0s | 0 |

### Tool time

| Tool | Context | Calls | Total | Max |
|---|---|---|---|---|
| Agent — sub-agent wall time | orchestrator | 79 | 2h19m | 23m 05s |
| Bash | devscene:architecture-reviewer | 48 | 7.2s | 0.2s |
| Bash | devscene:branch-reviewer | 31 | 4.8s | 0.3s |
| Bash | devscene:committer | 340 | 3m 27s | 5.6s |
| Bash | devscene:layer-implementer | 434 | 11m 33s | 34.2s |
| Bash | devscene:review-plan-reviewer | 17 | 2.7s | 0.2s |
| Bash | devscene:skeptic-reviewer | 33 | 5.4s | 0.3s |
| Bash | devscene:statistics-plan-writer | 11 | 1.5s | 0.1s |
| Bash | devscene:task-plan-reviewer | 97 | 16.5s | 0.5s |
| Bash | devscene:task-plan-writer | 107 | 21.3s | 2.4s |
| Bash | devscene:test-fix-plan-writer | 11 | 1.7s | 0.2s |
| Bash | orchestrator | 377 | 1h07m | 1m 02s |
| Edit | devscene:committer | 28 | 1.0s | 0.0s |
| Edit | devscene:layer-implementer | 247 | 9.2s | 0.0s |
| Edit | devscene:task-plan-writer | 39 | 1.5s | 0.0s |
| Edit | orchestrator | 13 | 24.1s | 4.4s |
| Read | devscene:architecture-reviewer | 94 | 4.8s | 0.3s |
| Read | devscene:branch-reviewer | 14 | 1.5s | 0.3s |
| Read | devscene:committer | 41 | 0.5s | 0.0s |
| Read | devscene:layer-implementer | 158 | 9.3s | 0.3s |
| Read | devscene:prompt-injection-reviewer | 2 | 0.0s | 0.0s |
| Read | devscene:review-plan-reviewer | 6 | 0.7s | 0.2s |
| Read | devscene:skeptic-reviewer | 5 | 0.3s | 0.2s |
| Read | devscene:statistics-plan-writer | 2 | 0.0s | 0.0s |
| Read | devscene:task-plan-reviewer | 114 | 3.0s | 0.2s |
| Read | devscene:task-plan-writer | 46 | 3.2s | 0.5s |
| Read | devscene:test-fix-plan-writer | 4 | 0.2s | 0.2s |
| Read | orchestrator | 16 | 14.1s | 4.0s |
| Skill | orchestrator | 1 | 0.0s | 0.0s |
| Write | devscene:architecture-reviewer | 3 | 0.0s | 0.0s |
| Write | devscene:branch-reviewer | 5 | 0.1s | 0.0s |
| Write | devscene:layer-implementer | 18 | 0.7s | 0.0s |
| Write | devscene:statistics-plan-writer | 1 | 0.0s | 0.0s |
| Write | devscene:task-plan-reviewer | 3 | 0.0s | 0.0s |
| Write | devscene:task-plan-writer | 31 | 1.1s | 0.0s |
| Write | devscene:test-fix-plan-writer | 2 | 0.0s | 0.0s |
| Write | orchestrator | 3 | 0.0s | 0.0s |

`Agent` / `Task` rows are sub-agent wall time: how long the orchestrator was blocked on each dispatch, which `### Sub-agents` breaks down per dispatch. They are not time spent in a tool.

#### Slowest calls (sub-agent dispatches excluded)

| Tool | Context | Started | Duration | Result bytes | Error | Permission denied |
|---|---|---|---|---|---|---|
| Bash | orchestrator | 2026-11-14T18:54:48.988Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:29:31.796Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T18:59:05.546Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:35:01.081Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:50:55.862Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:33:55.646Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:31:46.383Z | 1m 02s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T18:51:37.473Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T18:55:54.385Z | 1m 01s | 19 | true | false |
| Bash | orchestrator | 2026-11-14T19:05:28.394Z | 1m 01s | 19 | true | false |

#### Polling loops

| Context | Command | Count | Total |
|---|---|---|---|
| devscene:architecture-reviewer | git rev-parse --show-toplevel | 5 | 0.6s |
| devscene:committer | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> harness-runs/story_plans/feat_parallel_plan_reviews_story_plan.md harness-runs/task_plans/feat_p | 5 | 2.8s |
| devscene:committer | bash <main_repo>/scripts/push-branch.sh <repo_root> | 31 | 2m 31s |
| devscene:committer | cat <repo_root>/devscene.config.json | 4 | 0.5s |
| devscene:committer | git branch --show-current | 30 | 4.1s |
| devscene:committer | git log -1 --oneline | 30 | 3.9s |
| devscene:committer | git rev-parse --show-toplevel | 30 | 4.1s |
| devscene:committer | git status --short | 74 | 11.6s |
| devscene:committer | grep -n "scriptsDir\\|stateDir" <repo_root>/devscene.config.json | 3 | 0.3s |
| devscene:committer | grep -n -i "commit" <repo_root>/.claude/context/conventions.md | 5 | 0.6s |
| devscene:committer | grep -n -i "commit" <repo_root>/.claude/context/conventions.md \| head -40 | 5 | 0.7s |
| devscene:committer | grep -n -i -A40 "^## .*commit" <repo_root>/.claude/context/conventions.md | 5 | 0.6s |
| devscene:committer | printenv DEVSCENE_MAIN_REPO | 30 | 3.8s |
| devscene:layer-implementer | bash scripts/typecheck.sh | 25 | 1m 18s |
| devscene:layer-implementer | git -C <repo_root> diff --stat | 3 | 0.4s |
| devscene:layer-implementer | git diff --name-only HEAD | 10 | 14.9s |
| devscene:layer-implementer | git ls-files --others --exclude-standard | 10 | 12.2s |
| devscene:layer-implementer | git rev-parse --show-toplevel | 31 | 4.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/flow-walker-concurrency.test.mjs | 5 | 1m 47s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-anchor-isolation.test.mjs | 8 | 44.7s |
| devscene:layer-implementer | npm test --workspace cli -- test/main-repo-resolution-corpus.test.mjs | 4 | 7.4s |
| devscene:layer-implementer | npm test --workspace cli -- test/no-container-home-paths.test.mjs | 11 | 41.1s |
| devscene:layer-implementer | npm test --workspace cli -- test/shipped-scripts-mktemp.test.mjs | 5 | 10.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/untrusted-input-corpus.test.mjs | 4 | 12.0s |
| devscene:layer-implementer | npm test --workspace cli -- test/watcher-main-anchor.test.mjs | 7 | 57.9s |
| devscene:task-plan-reviewer | git rev-parse --show-toplevel | 3 | 0.4s |
| devscene:task-plan-writer | git grep -lE "comes \*\*before\*\*\|ahead of the (architecture\|structural\|\*\*architecture)\|\*\*ahead of\*\* the architecture\|nested ahead\|in sequence on\|step 7\ | 3 | 1.3s |
| devscene:task-plan-writer | git rev-parse --show-toplevel | 3 | 0.3s |
| orchestrator | bash <main_repo>/scripts/commit-on-branch.sh --repo <repo_root> "harness-runs/story_plans/feat_parallel_plan_reviews_story_plan.md" "harness-runs/task_plans/fea | 4 | 3.5s |
| orchestrator | bash <main_repo>/scripts/push-branch.sh <repo_root> | 20 | 1m 38s |
| orchestrator | bash scripts/flow-walker.sh next --flow task_plan_writing --branch feat_parallel_plan_reviews --outcome returned | 3 | 0.7s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_1 | 30 | 30m 26s |
| orchestrator | bash scripts/run-test-suite.sh --wait task_round_2 | 33 | 33m 07s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null | 64 | 36.9s |
| orchestrator | ls harness-runs/STOP harness-runs/PAUSE 2>/dev/null; cat harness-runs/.dispatch_counter 2>/dev/null \|\| echo 0 | 75 | 32.6s |

### Sub-agents

| Type | Description | Duration | Requests | Output tokens | Input tokens (uncached) | Total input tokens (incl. cache) | Cache read tokens | Cache write tokens | Wall share |
|---|---|---|---|---|---|---|---|---|---|
| devscene:prompt-injection-reviewer | Screen task prompt | 3.1s | 1 | 278 | 4 | 30976 | 10469 | 20503 | 0.0002 |
| devscene:task-plan-writer | Write task plan | 23m 05s | 116 | 144424 | 234 | 36376878 | 35894169 | 482475 | 0.105 |
| devscene:architecture-reviewer | Architecture plan review | 1m 44s | 16 | 11137 | 34 | 1726443 | 1584397 | 142012 | 0.0079 |
| devscene:task-plan-reviewer | Task plan review | 7m 45s | 67 | 47957 | 136 | 12358790 | 12102152 | 256502 | 0.0353 |
| devscene:task-plan-writer | Revise task plan | 3m 48s | 19 | 25580 | 40 | 1260524 | 1167918 | 92566 | 0.0173 |
| devscene:architecture-reviewer | Architecture plan review r1 | 2m 29s | 16 | 16214 | 34 | 1718424 | 1567128 | 151262 | 0.0113 |
| devscene:task-plan-reviewer | Task plan review r1 | 6m 25s | 51 | 40627 | 104 | 8716556 | 8479460 | 236992 | 0.0292 |
| devscene:task-plan-writer | Revise task plan r2 | 3m 11s | 21 | 22802 | 44 | 1486077 | 1391901 | 94132 | 0.0145 |
| devscene:architecture-reviewer | Architecture plan review r2 | 36.7s | 10 | 3433 | 22 | 537077 | 468909 | 68146 | 0.0028 |
| devscene:task-plan-reviewer | Task plan review r2 | 1m 32s | 20 | 9389 | 42 | 1515176 | 1418406 | 96728 | 0.007 |
| devscene:layer-implementer | Implement Task 1 | 1m 27s | 13 | 7972 | 28 | 586764 | 536010 | 50726 | 0.0066 |
| devscene:committer | Commit Task 1 | 29.4s | 10 | 2424 | 22 | 277516 | 249197 | 28297 | 0.0022 |
| devscene:layer-implementer | Implement Task 2 | 53.6s | 11 | 5504 | 24 | 437372 | 406862 | 30486 | 0.0041 |
| devscene:committer | Commit Task 2 | 26.0s | 6 | 2120 | 14 | 221763 | 198387 | 23362 | 0.002 |
| devscene:layer-implementer | Implement Task 3 | 7m 14s | 33 | 47962 | 68 | 3109003 | 2989467 | 119468 | 0.0329 |
| devscene:committer | Commit Task 3 | 25.7s | 8 | 2117 | 18 | 218065 | 191443 | 26604 | 0.002 |
| devscene:layer-implementer | Implement Task 4 | 3m 49s | 21 | 22920 | 44 | 1375720 | 1299985 | 75691 | 0.0174 |
| devscene:committer | Commit Task 4 | 32.2s | 11 | 2603 | 24 | 299720 | 285420 | 14276 | 0.0024 |
| devscene:layer-implementer | Implement Task 5 | 1m 37s | 13 | 9768 | 28 | 770687 | 711251 | 59408 | 0.0074 |
| devscene:committer | Commit Task 5 | 28.3s | 9 | 2273 | 20 | 261989 | 245013 | 16956 | 0.0021 |
| devscene:layer-implementer | Implement Task 6 | 2m 22s | 16 | 9031 | 34 | 875281 | 816278 | 58969 | 0.0108 |
| devscene:committer | Commit Task 6 | 30.0s | 9 | 2482 | 20 | 315571 | 293184 | 22367 | 0.0023 |
| devscene:layer-implementer | Implement Task 7 | 3m 43s | 22 | 21863 | 46 | 1541675 | 1461904 | 79725 | 0.017 |
| devscene:committer | Commit Task 7 | 25.8s | 7 | 2179 | 16 | 205954 | 190598 | 15340 | 0.002 |
| devscene:layer-implementer | Implement Task 8 | 1m 46s | 13 | 9057 | 28 | 741429 | 687214 | 54187 | 0.008 |
| devscene:committer | Commit Task 8 | 26.2s | 6 | 2199 | 14 | 188507 | 170642 | 17851 | 0.002 |
| devscene:layer-implementer | Implement Task 9 | 4m 41s | 35 | 30042 | 72 | 3475925 | 3367344 | 108509 | 0.0213 |
| devscene:committer | Commit Task 9 | 26.6s | 7 | 2110 | 16 | 206899 | 191478 | 15405 | 0.002 |
| devscene:layer-implementer | Implement Task 26 | 2m 48s | 24 | 17084 | 50 | 1607057 | 1537588 | 69419 | 0.0127 |
| devscene:committer | Commit Task 26 | 26.8s | 7 | 2252 | 16 | 203377 | 188132 | 15229 | 0.002 |
| devscene:layer-implementer | Implement Task 10 | 36.9s | 7 | 2964 | 16 | 266523 | 240551 | 25956 | 0.0028 |
| devscene:committer | Commit Task 10 | 30.2s | 10 | 2560 | 22 | 276288 | 259836 | 16430 | 0.0023 |
| devscene:layer-implementer | Implement Task 11 | 41.2s | 12 | 3436 | 26 | 471121 | 443557 | 27538 | 0.0031 |
| devscene:committer | Commit Task 11 | 31.9s | 9 | 2608 | 20 | 236338 | 223110 | 13208 | 0.0024 |
| devscene:layer-implementer | Implement Task 12 | 1m 43s | 20 | 10927 | 42 | 1341332 | 1271225 | 70065 | 0.0078 |
| devscene:committer | Commit Task 12 | 25.5s | 7 | 2093 | 16 | 216100 | 198075 | 18009 | 0.0019 |
| devscene:layer-implementer | Implement Task 17 | 1m 16s | 15 | 8035 | 32 | 1057168 | 985354 | 71782 | 0.0058 |
| devscene:committer | Commit Task 17 | 29.4s | 10 | 2384 | 22 | 287399 | 269663 | 17714 | 0.0022 |
| devscene:layer-implementer | Implement Task 13 | 1m 29s | 22 | 8665 | 46 | 1411163 | 1346161 | 64956 | 0.0068 |
| devscene:committer | Commit Task 13 | 29.7s | 9 | 2355 | 20 | 249107 | 233600 | 15487 | 0.0023 |
| devscene:layer-implementer | Implement Task 14 | 31.1s | 7 | 3075 | 16 | 283832 | 256291 | 27525 | 0.0024 |
| devscene:committer | Commit Task 14 | 30.4s | 10 | 2496 | 22 | 266958 | 252538 | 14398 | 0.0023 |
| devscene:layer-implementer | Implement Task 15 | 1m 02s | 12 | 6665 | 26 | 618555 | 575404 | 43125 | 0.0047 |
| devscene:committer | Commit Task 15 | 28.3s | 9 | 2118 | 20 | 249661 | 234718 | 14923 | 0.0021 |
| devscene:layer-implementer | Implement Task 16 | 1m 11s | 14 | 7508 | 30 | 744548 | 693122 | 51396 | 0.0054 |
| devscene:committer | Commit Task 16 | 32.4s | 9 | 2690 | 20 | 262440 | 246083 | 16337 | 0.0025 |
| devscene:layer-implementer | Implement Task 18 | 32.7s | 7 | 3510 | 16 | 280853 | 253886 | 26951 | 0.0025 |
| devscene:committer | Commit Task 18 | 25.8s | 8 | 2125 | 18 | 222500 | 208381 | 14101 | 0.002 |
| devscene:layer-implementer | Implement Task 19 | 2m 26s | 25 | 17031 | 52 | 1892747 | 1809708 | 82987 | 0.0111 |
| devscene:committer | Commit Task 19 | 26.0s | 6 | 2352 | 14 | 202983 | 183320 | 19649 | 0.002 |
| devscene:layer-implementer | Implement Task 20 | 2m 13s | 18 | 13907 | 38 | 1401723 | 1323549 | 78136 | 0.0101 |
| devscene:committer | Commit Task 20 | 28.2s | 9 | 2345 | 20 | 265675 | 247546 | 18109 | 0.0021 |
| devscene:layer-implementer | Implement Task 21 | 4m 23s | 29 | 37004 | 60 | 2258310 | 2146279 | 111971 | 0.02 |
| devscene:committer | Commit Task 21 | 28.1s | 9 | 2310 | 20 | 252962 | 236623 | 16319 | 0.0021 |
| devscene:layer-implementer | Implement Task 24 | 57.8s | 14 | 5593 | 30 | 702373 | 659076 | 43267 | 0.0044 |
| devscene:committer | Commit Task 24 | 28.2s | 8 | 2430 | 18 | 225115 | 211014 | 14083 | 0.0021 |
| devscene:layer-implementer | Implement Task 22 | 2m 02s | 27 | 12712 | 56 | 2436880 | 2339331 | 97493 | 0.0093 |
| devscene:committer | Commit Task 22 | 26.3s | 8 | 2091 | 18 | 224482 | 209644 | 14820 | 0.002 |
| devscene:layer-implementer | Implement Task 23 | 43.8s | 9 | 4340 | 20 | 462067 | 419359 | 42688 | 0.0033 |
| devscene:committer | Commit Task 23 | 27.4s | 8 | 2325 | 18 | 251179 | 233058 | 18103 | 0.0021 |
| devscene:layer-implementer | Implement Task 25 | 1m 04s | 13 | 7228 | 28 | 650221 | 603738 | 46455 | 0.0049 |
| devscene:committer | Commit Task 25 | 31.6s | 10 | 2500 | 22 | 276509 | 260065 | 16422 | 0.0024 |
| devscene:architecture-reviewer | Branch architecture review | 1m 44s | 25 | 9397 | 52 | 2554228 | 2384813 | 169363 | 0.0079 |
| devscene:branch-reviewer | End-of-branch code review | 5m 20s | 43 | 31929 | 88 | 6652590 | 6427925 | 224577 | 0.0243 |
| devscene:review-plan-reviewer | Meta-review code review | 1m 04s | 18 | 6022 | 38 | 1446988 | 1347909 | 99041 | 0.0049 |
| devscene:committer | Commit code review | 19.4s | 5 | 1409 | 12 | 144275 | 118830 | 25433 | 0.0015 |
| devscene:layer-implementer | Fix code-review Finding 2 | 18.2s | 5 | 1483 | 12 | 189846 | 153172 | 36662 | 0.0014 |
| devscene:committer | Commit Finding 2 fix | 25.0s | 6 | 1986 | 14 | 165129 | 152552 | 12563 | 0.0019 |
| devscene:layer-implementer | Fix Finding 1 (cli layer) | 2m 01s | 16 | 9953 | 34 | 824289 | 775727 | 48528 | 0.0092 |
| devscene:layer-implementer | Fix Finding 1 (general layer) | 1m 38s | 14 | 7170 | 30 | 795305 | 744608 | 50667 | 0.0075 |
| devscene:committer | Commit Finding 1 fix | 25.7s | 8 | 2145 | 18 | 222663 | 208600 | 14045 | 0.002 |
| devscene:skeptic-reviewer | Adversarial skeptic review | 4m 11s | 38 | 24230 | 78 | 3511757 | 3355883 | 155796 | 0.0191 |
| devscene:test-fix-plan-writer | Write test fix plan round 1 | 1m 00s | 14 | 6064 | 30 | 693020 | 635521 | 57469 | 0.0046 |
| devscene:architecture-reviewer | Review test fix plan | 40.4s | 8 | 4078 | 18 | 552009 | 446603 | 105388 | 0.0031 |
| devscene:committer | Commit test fix plan | 20.1s | 5 | 1394 | 12 | 147183 | 121025 | 26146 | 0.0015 |
| devscene:layer-implementer | Test fix item 1 (cli) | 1m 03s | 12 | 4967 | 26 | 465370 | 424052 | 41292 | 0.0048 |
| devscene:layer-implementer | Test fix item 1 (general) | 1m 01s | 12 | 4139 | 26 | 536308 | 500929 | 35353 | 0.0046 |
| devscene:committer | Commit test fix item 1 | 24.4s | 7 | 1964 | 16 | 190047 | 177108 | 12923 | 0.0019 |
| devscene:statistics-plan-writer | Write branch statistics | 40.8s | 9 | 4972 | 20 | 305380 | 268625 | 36735 | 0.0031 |

### Cost and tokens

| Measure | Value |
|---|---|
| Cost | $88.05 |
| Cost — claude-opus-5-5 | $88.05 |
| Input tokens (uncached) | 3310 |
| Total input tokens (incl. cache) | 214116309 |
| Output tokens | 929296 |
| Thinking tokens (main thread) | 6050 |
| Cache read tokens | 208826978 |
| Cache write tokens | 5286021 |
| Cache write tokens, main thread (5m / 1h) | 0 / 420044 |
| Cache hit ratio | 0.9753 |
| Token source | result.modelUsage |

#### Token attribution

| Context | Input tokens (uncached) | Total input tokens (incl. cache) | Output tokens | Cache read tokens | Cache write tokens |
|---|---|---|---|---|---|
| orchestrator | 646 | 91827615 | 9384 | 91406925 | 420044 |
| sub-agents | 2664 | 122288694 | 839487 | 117420053 | 4865977 |
| remainder | 0 | 0 | 80425 | 0 | 0 |

Remainder: tokens the session total holds that neither the orchestrator's requests nor the dispatches' transcripts account for.

### Reliability

| Measure | Value |
|---|---|
| API retries | 0 |
| Permission denials | 41 |
| Sub-agents spawned / failed / killed | 79 / 0 / 0 |
| terminal_reason | completed |
| stop_reason | end_turn |
| Turns | 491 |
| Time to first token | 1.2s |
| Rate-limit peak | seven_day 0.48 |
