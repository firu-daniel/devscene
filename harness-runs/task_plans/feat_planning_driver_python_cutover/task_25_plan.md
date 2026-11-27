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
