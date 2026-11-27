### Task 25 — Bring the watcher, architecture, CLI and structured-return documents to the Python driver

**Goal:** Four root documents still describe the bash planning driver (scope register rows 4, 11, 15 and 16). Bring each one to the driver as it now is.

**Depends on:**
- **Task 2.** The watcher's `planning_driver_ready` checks `hr_flow_host_missing … devscene-planning-driver`, and `planning_driver_run` maps `0` / `3` / other.
- **Task 4.** The three libraries are no longer shipped.
- **Task 13.** `host/node_sessions.py` writes the node streams and the manifest.
- **Task 15.** `host/planning_executor.py` refuses a verdict with no findings file.
- **Task 18.** `devscene-planning-driver` is the command.

**Where this task stops.** These four documents only. `docs/flow-graph-walker.md` is **Task 24's**. The scope register's `no-change` rows (`docs/config.md`, `docs/remote-execution.md`, the state-dir READMEs) stay true and are not edited.

### Targets

- `docs/watcher.md`
- `ARCHITECTURE.md`
- `docs/cli.md`
- `docs/structured-agent-returns.md`

**Work:**

- [ ] **`docs/watcher.md`.**
  - Remove the three library rows from the shipped-script table.
  - The `flows/task_plan_writing.graph.json` row names the planning driver as its second reader.
  - *"When a launch takes it"* names the provisioning check (`devscene-planning-driver` runnable from `<scriptsDir>/python/.venv`) in place of the libraries.
  - *"The driver's exit, mapped onto `classify_run_exit`"* gives the statuses and the `consumed:` / `stopped:` lines, citing `commands/planning_driver.py` in place of *"`planning-driver-lib.sh`'s header"*.
  - *"Node sessions, and the run's time"*: node sessions run at most 5 at once, and their streams are written by `host/node_sessions.py`.
- [ ] **`ARCHITECTURE.md`.**
  - In the launch paragraph, *"`lib/planning-node-lib.sh` launches each planning node session through the same `session_exec`"* becomes: the planning driver launches each node session with the watcher's shared vector, which the watcher passes it after `--`.
  - Replace the launch table's `planning-node-lib.sh` row with a row for `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` → `ClaudeExecutor`, driven by `commands/planning_driver.py`, and state its per-node flags: `--agent <plugin>:<agent>`, `--plugin-dir`, and the MCP flags from `host/agent_flags.py`.
  - Keep the paragraph's covering-property invariant true: every launch site is still a row.
- [ ] **`docs/cli.md`.** In *"Two families land in `scriptsDir`"*, drop *"the planning driver's three libraries, which the run watcher sources for the opt-in script-driven planning pilot"*, and drop the deny-list sentence about them. The `flow-host` doctor paragraph's *"the planning driver runs this checkout's walker and environment"* becomes *"the planning driver runs from this checkout's environment"*.
- [ ] **`docs/structured-agent-returns.md`.** The driver's reading of a node's return is `host/session_stream.py` → `judge_session`, called by `ClaudeExecutor`. The findings-file rule is `host/planning_executor.py`'s. Replace the `pnl_reap` citations with these, and keep the decisions' substance. Mark a decision superseded only where its substance changed.
- [ ] Re-run scope register entries A and B. No live sentence in these four files names the bash libraries, `pnl_*`, `prl_*` or `pd_drive`.

**Verification:**

- `git grep -nE 'planning-(driver|node|record)-lib|pnl_[a-z_]+|prl_[a-z_]+|pd_drive' -- docs/watcher.md ARCHITECTURE.md docs/cli.md docs/structured-agent-returns.md` prints nothing outside an entry marked superseded.
- Each repointed citation resolves to a symbol that exists after Tasks 1–18.

**Deviations from plan:**
- `docs/watcher.md`: beyond the five listed bullets, five more sentences were brought to the driver as it now is, because each was false. (1) The `commit-on-branch.sh` row said the planning driver used the plain form. It uses `--artifact` (`host/commit_points.py` → `commit_artifact`). (2) The `lib/unit-commit-lib.sh` row said the watcher sources it ahead of `planning-record-lib.sh`. The watcher no longer sources it. (3) The `### Why only the yes rows…` paragraph named the three libraries. (4) **The node stall rule.** It described a `STALL_CHECK_ENABLED`-gated `max(STALL_WARN_SECS, …)` threshold. It is now the fixed constant `claude_executor.py` → `NODE_INACTIVITY_LIMIT_SECONDS` (2685 s), and the paragraph says that while a set runs the watchdog sees no node traffic until a session ends. (5) **What parks or pauses the driver.** It claimed a `[plan-drive]` line per retry and a park question listing each attempt. The flow host narrates no retry line, and its park detail carries the agent and the reason (`host/run_exits.py` → `SESSION_AGENT`, `SESSION_REASON`). **Where node streams land.** now says formatted lines are written when the session ends, not as they happen (`host/node_sessions.py` → `NodeSessions.record`).
- `ARCHITECTURE.md`: the derivation `grep` now also covers `devscene-flow-host/src/`, so the new `ClaudeExecutor` row's site is reached by the command and does not just sit in the table. The one new hit with no row, `host/session_stream.py`'s module docstring naming `--output-format`, is dispositioned in the covering-property paragraph.
- `docs/structured-agent-returns.md`: two decisions changed in substance and carry a **Superseded 2026-11-27** note; their original text is kept. (a) *The schema lives in its own file*: the jq-1.5 reason for the closed dialect and the `vfail`/`schemafail` cost. The driver now validates with GraphScene's `return_violations`. (b) *A list of structured items*: the driver's per-item failure wording. Every other `pnl_*` / `pd_*` citation was repointed in place, because its decision's substance holds.
- Verification evidence: the two tree guards ran as one `npm test --workspace cli -- test/agent-return-schemas.test.mjs test/no-container-home-paths.test.mjs` with its output piped to `tail`, which the conventions' no-pipe rule forbids. The verdict rests on the printed counts (`# tests 56`, `# pass 56`, `# fail 0`), not on the exit status.
