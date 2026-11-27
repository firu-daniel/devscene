# Story: Script-driven planning on GraphScene — the Python planning driver replaces the bash driver

## Context

This branch moves script-driven planning (`execution.scriptDrivenPlanning`) from the bash driver (`cli/templates/scripts/lib/planning-driver-lib.sh`, `planning-node-lib.sh`, `planning-record-lib.sh`) to GraphScene's run mode. It is part of #376 and depends on #419, #421 and #423. The switch stays opt-in. The watcher still decides who drives planning, the orchestrator session or the driver. It still runs a setup session first and hands off to the engine session afterwards. What changes is the middle step: the bash `pd_drive` gives way to a Python command, `devscene-planning-driver`, in `devscene-flow-host`. That command walks the planning graph in-process with `graphscene.start_run` / `continue_run` and runs no walker subprocess. Every node runs through the harness's `ClaudeExecutor` (#421). Every commit and ledger flip runs through `PlanningHooks` (#423). The entry is decided by `decide_planning_entry` (#423). Once the command exists the bash libraries have no reader, so this branch deletes them, together with the suites that pinned their internals. The behaviour those suites pinned is pinned again against the Python driver.

**What the driver keeps from the bash pilot.** Wherever the run-mode pieces leave a rule to the host, the driver behaves as the pilot did. The cases:
- **STOP and PAUSE.** The STOP and PAUSE files and the global kill switch work as before.
- **The dispatch counter.** It lives at `<stateDir>/.dispatch_counter` and is reset at each drive.
- **The dispatch cap.** It is `MAX_TOTAL_DISPATCHES`, read from the planning core.
- **Retries.** An infrastructure failure is retried alone, up to three attempts with a 60 s backoff. Three undelivered sets in a row pause the run.
- **Parks.** The `<ask>` park carries the writer's `questions`, one `## Q<k>` section per item. The `<escalate>` park makes a `plan-round-partial` commit first whenever gates are held.
- **Pause files.** A pause commits `plan-round-partial`, then writes `PAUSE_PROGRESS.md` and `PAUSE_ACK`.
- **Node records.** Each node's stream goes to `<seq>-<node>.stream.jsonl` and is appended to the run stream. The `node-sessions.jsonl` manifest is kept, because `run-analytics.sh` reads it.
- **Observations and the hand-off summary.** The improvement-observation blocks are committed as `observations`. The hand-off summary lines are logged as before.
- **Corpus staleness.** As the task prompt decides, the driver drops `corpus_staleness` exactly as the pilot does.
- **The concurrency limit.** One value is new: at most **5** dispatches run at once. It is a `devscene-flow-host` constant passed as `ExecutionLimits(max_concurrent_dispatches=5, …)`, not a `devscene.config.json` key.

**The walk's state stays where it is.** `FileStateStore` keeps the walk at `<stateDir>/.flow_walker_state/`. A remote job already carries that directory across job boundaries in its `harness-state` bundle. When the saved walk is unusable, `decide_planning_entry` rebuilds the entry from the ledger and the round files. Remote runs need no separate wiring: `autonomous-watcher.sh job` goes through the same `planning_driver_ready` and launch function.

**The command-line contract between the watcher and the driver.** It is stated here once. Task 2 writes the watcher's side, and Task 18 writes the command's side.

```
devscene-planning-driver --branch <branch> --worktree <worktree> --main-repo <main_repo>
    --plugin-dir <plugin_dir> --flows <flows_dir> --log <log_path> --formatter <formatter>
    [--plugin-dir-added] -- <agent_cli> [<shared session flag>…]
```

- **The arguments:**
  - `--worktree` is the run copy. It is the walk's repository root and the sessions' working directory.
  - `--main-repo` is the main checkout. The commit wrapper `<main_repo>/<scriptsDir>/commit-on-branch.sh` is resolved from it, as is the global kill switch `<main_repo>/<stateDir>/AUTONOMOUS_STOP`.
  - `--flows` is the main checkout's `<scriptsDir>/flows`.
  - `--log` is the run log. The driver writes four things from it:
    - its narration, as lines prefixed `[plan-drive] `;
    - each node's formatted output;
    - each node's stream, under `${log%.log}.planning/`;
    - the run stream, `${log%.log}.stream.jsonl`.
  - `--formatter` is the watcher's stream formatter, a path or `cat`. It runs as one argv word with a node's stream on stdin, and its stdout is appended to the log.
  - `--plugin-dir-added` is given when the shared vector already carries `--add-dir <plugin_dir>`.
  - After `--`, the first word is the agent CLI. The rest are the shared session flags: the watcher's `session_exec` vector without `-p`, `--output-format` and `--verbose`, which the executor sets itself.
- **Exit statuses and stdout:**
  - **`0`, handed off.** Either the walk reached `<terminal_handoff>`, or `P1`–`P3` were already resolved. Stdout is exactly one line: `consumed:`, then ` <i>` for each answered-pair index appended to a writer's prompt, in `CorePromptBuilder.consumed` order.
  - **`3`, a clean stop, with its files written.** Stdout is exactly one line, `stopped: <kind>`. `<kind>` is one of:
    - `park`;
    - `pause`, for a PAUSE file;
    - `undelivered`, for the self-pause after three undelivered sets;
    - `stop`, for a STOP file;
    - `cap`;
    - `kill-switch`.
  - **`2`, a fault.** Stdout is empty, and stderr carries one `planning-driver: <cause>` line.
- **The environment.** The command inherits the environment the watcher's launch subshell gives it, after the `unset` and the two exports `session_exec` makes. Each node session inherits the same environment, minus the variables the flow host's own launch adds (Task 14).

**The layer order, and why the `cli` tasks come first.** This repository configures `cli` ahead of `devscene-flow-host`, so the `cli` tasks ship first:
- **They depend on no later task.** They fix the contract above.
- **They are checked against a stub.** Task 5 pins the watcher's side with a stub `uv` on `PATH`, so neither its verification nor Task 2's needs the Python command to exist yet.
- **The `devscene-flow-host` tasks implement the contract,** and they `**Depends on:**` the `cli` task that fixed it.
- **The end-to-end behaviour moves to `pytest`.** The walk, the parks, the stops and the retries are pinned in `devscene-flow-host`'s `pytest` suites (Tasks 19–21). Those suites drive the real command against a fake agent CLI, a planted commit wrapper and the shipped planning graph and core.
- **The bash suites are retired, not rewritten.** The `cli` suites that sourced the bash libraries pinned those libraries' internals, so Task 3 retires them instead of rewriting them. Task 3 ships ahead of Task 4, which deletes the libraries, because a tree guard Task 4's change selects (`test/agent-return-schemas.test.mjs`) read `planning-driver-lib.sh` until Task 3 removed that read.

**The Python module map, one owner each:**

| Module | What it owns | Task |
|---|---|---|
| `records/core_limits.py` | Reads `MAX_TOTAL_DISPATCHES` | 9 |
| `records/clarifications.py` | The next question index (`max_question_index`) | 9 |
| `records/config.py` | `scriptsDir`, as `HarnessConfig.scripts_dir` (added beside `stateDir` and `phases`) | 9 |
| `records/ledger.py` | The `## Run mode` section's `- skipped:` value and `- ignored:` entries (`read_run_mode_entries`) | 10 |
| `host/run_records.py` | The park and pause files | 10 |
| `host/observations.py` | The observation blocks and their commit | 11 |
| `host/run_control.py` | STOP / PAUSE / kill switch, the dispatch counter and the execution limits | 12 |
| `host/node_sessions.py` | The usage and `Launch` sinks: node streams, manifest, formatted log, session table | 13 |
| `records/mcp_servers.py` | The worktree's `.mcp.json` servers, read into a plain value | 14 |
| `host/agent_flags.py` | The session args, the per-agent MCP flags (cut from `records/mcp_servers.py`'s value) and the session environment | 14 |
| `host/planning_executor.py` | The findings-file and round-file checks, and the kept revision findings, over `ClaudeExecutor` | 15 |
| `host/planning_run.py` | Composes everything and runs `start_run` / `continue_run` | 16 |
| `host/run_exits.py` | Acts on each `RunExit` | 17 |
| `commands/planning_driver.py` | The contract above | 18 |

**Issue numbers leave GraphScene and the flow host.** As the task prompt decides, when this branch completes no source, test or README under `graphscene/` or `devscene-flow-host/` names an issue number. Tasks 8, 22 and 23 own the known sites. Each sentence keeps what it says, minus the number. The closing invariant is `git grep -nE '#[0-9]+' -- graphscene devscene-flow-host`: it must print no hit.

**Top risks:**
1. **Behaviour silently lost.** A behaviour the bash driver had and its suites pinned could be dropped when the suites are deleted. This covers the `<ask>` park's `## Q<k>` sections, the partial commit before an escalation with held gates, the undelivered self-pause, and the node manifest that `run-analytics.sh` reads. Task 3 retires a suite only together with a statement of which of Tasks 19–21 re-pins each behaviour — the map under `task_3_plan.md` → **Where each retired behaviour goes**, which the plan commit lands — and Tasks 19 and 20 port the cases one for one.
2. **The flow host's environment leaking into agent sessions.** The driver runs under `uv run`. Without a scrub, every node session would inherit the flow host's `VIRTUAL_ENV`, `PYTHONPATH` and venv `PATH` entry. Task 14 strips them, and its test asserts their absence.
3. **The run-mode cutover skipping the host's round-file refusal.** Run mode records through `Walker.next` directly, bypassing `record_outcome`, so a malformed round file would be recorded as a verdict. Task 15's `PlanningExecutor` turns it into an `infra` failure, which is retried alone and held as `error` on the third attempt. Task 19 pins the refusal end to end.

**Manual setup required:**
- After every task has landed, a person runs a real planning run on a throwaway branch with `execution.scriptDrivenPlanning` on, once locally and once as a remote job, as the task prompt's leads ask. It is the only check that drives a real `claude` through the watcher, the `uv` launch and the Python driver. It depends on Tasks 2, 16, 17 and 18.
- After the merge, a person re-renders this repository's self-adopted `scripts/` from a fresh self-adopt of `dev`, as #481 and #493 did. This repository runs with `scriptDrivenPlanning` on, and its own `scripts/autonomous-watcher.sh` and `scripts/lib/planning-*-lib.sh` stay the bash pilot until that re-render. It depends on Tasks 1, 2 and 4.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The loop walks the `[ ]` entries below from top to bottom.

- **Only the committing role flips a marker.** In every flow that runs the unit loop, that role is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs none, it is the orchestrator itself.
- **An implementer never changes a marker here**, and never edits any other line of this section, in an index a run is iterating.
- **`[ ]` markers anywhere else are informational only.** The sub-step bullets inside the per-task files are progress markers for the implementer. The commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_planning_driver_python_cutover/task_<K>_plan.md`. The entries follow the configured layer order, with the catch-all layer last.

1. [x] **Task 1** — Launch a flow-host console script through one library route, and hand `flow-walker.sh` to it _(layer: cli)_ _(points: 15)_
2. [x] **Task 2** — Launch the Python planning driver from the watcher's script-driven sequence _(layer: cli)_ _(points: 20)_
3. [x] **Task 3** — Retire the `cli` suites that pinned the bash driver's internals _(layer: cli)_ _(points: 10)_
4. [ ] **Task 4** — Retire the bash planning driver's three libraries from the shipped set _(layer: cli)_ _(points: 15)_
5. [ ] **Task 5** — Pin the watcher's side of the driver hand-off against a stub `uv`, locally and in job mode _(layer: cli)_ _(points: 20)_
6. [ ] **Task 6** — Describe the Python planning driver in the `cli` package's two READMEs _(layer: cli)_ _(points: 8)_
7. [ ] **Task 7** — Name the Python planning driver in the planning core and the autonomous flow document _(layer: plugin)_ _(points: 8)_
8. [ ] **Task 8** — Remove the issue numbers from GraphScene's run loop, set execution and command line _(layer: graphscene)_ _(points: 5)_
9. [ ] **Task 9** — Read the planning core's dispatch cap, a branch's highest question index and the configured `scriptsDir` as records _(layer: devscene-flow-host)_ _(points: 20)_
10. [ ] **Task 10** — Write the driver's park and pause files in `host/run_records.py`, and read the ledger's run-mode entries _(layer: devscene-flow-host)_ _(points: 20)_
11. [ ] **Task 11** — Collect, flush and commit the driver's improvement observations in `host/observations.py` _(layer: devscene-flow-host)_ _(points: 15)_
12. [ ] **Task 12** — Answer STOP, PAUSE and the dispatch counter, and fix the planning limits, in `host/run_control.py` _(layer: devscene-flow-host)_ _(points: 10)_
13. [ ] **Task 13** — Record each node session's stream, manifest line, formatted log and session-table row in `host/node_sessions.py` _(layer: devscene-flow-host)_ _(points: 20)_
14. [ ] **Task 14** — Read the worktree's MCP servers as a record, and build the session args, per-agent MCP flags and session environment in `host/agent_flags.py` _(layer: devscene-flow-host)_ _(points: 20)_
15. [ ] **Task 15** — Check findings and round files, and keep revision findings, in `host/planning_executor.py` _(layer: devscene-flow-host)_ _(points: 20)_
16. [ ] **Task 16** — Compose the planning run and drive it with `start_run` / `continue_run` in `host/planning_run.py` _(layer: devscene-flow-host)_ _(points: 20)_
17. [ ] **Task 17** — Act on each `RunExit` — hand-off, pause, halt, park — in `host/run_exits.py` _(layer: devscene-flow-host)_ _(points: 20)_
18. [ ] **Task 18** — Add the `devscene-planning-driver` command over the planning run _(layer: devscene-flow-host)_ _(points: 20)_
19. [ ] **Task 19** — Pin the driver's walk end to end against a fake agent CLI _(layer: devscene-flow-host)_ _(points: 20)_
20. [ ] **Task 20** — Pin the driver's parks, stops and retries end to end _(layer: devscene-flow-host)_ _(points: 20)_
21. [ ] **Task 21** — Hold every return field the driver reads to its agent's return schema _(layer: devscene-flow-host)_ _(points: 8)_
22. [ ] **Task 22** — Point the host's docstrings at the run driver and remove their issue numbers _(layer: devscene-flow-host)_ _(points: 10)_
23. [ ] **Task 23** — Document the planning driver and its command in `devscene-flow-host/README.md` _(layer: devscene-flow-host)_ _(points: 15)_
24. [ ] **Task 24** — Record the cutover in `docs/flow-graph-walker.md` _(layer: general)_ _(points: 20)_
25. [ ] **Task 25** — Bring the watcher, architecture, CLI and structured-return documents to the Python driver _(layer: general)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"The bash driver (`lib/planning-*-lib.sh`) is retired when this branch's suites pass on GraphScene."* A second quote from the same prompt joins it: *"When this branch completes, no code in `graphscene/` or `devscene-flow-host/` mentions an issue number."*

**Derivation entry A — corpus files naming the bash driver's code (command).** Re-run it verbatim from the repository root: `git grep -l -E 'planning-(driver|node|record)-lib|pd_drive|pnl_[a-z_]+|prl_[a-z_]+|PNL_CORE_BLOCKS' -- '*.md' ':!harness-runs'`

**Derivation entry B — corpus files describing the planning driver (command).** Re-run it verbatim: `git grep -l -i -E 'planning driver' -- '*.md' ':!harness-runs'`

**Derivation entry C — Markdown under the two Python packages naming an issue number (command).** Re-run it verbatim: `git grep -l -E '#[0-9]+' -- 'graphscene/*.md' 'devscene-flow-host/*.md'`

**Derivation entry D — corpus files stating how the flow host is launched (command).** Re-run it verbatim: `git grep -l -E 'through .flow-walker\.sh|launches it through' -- '*.md' ':!harness-runs'`

**Derivation entry E — lessons-ledger rows about the planning driver (procedure).**
- **Artifact:** `harness-runs/lessons.md`. Its first step is runnable: `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when its text names a `driver`, or its attribution names `feat_script_driven_planning_pilot`.

**Closure invariant:** every site any derivation entry reaches appears as a row below. Re-running entries A–D prints no path that is missing from the table, and walking entry E reaches no rule that is missing from it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## Commit-message policy` (*"the planning driver reads the same table (`cli/templates/scripts/lib/planning-record-lib.sh` → `prl_artifact_commit`)"*) | — | A, B | `no-change` | A conventions document is never a planned target. The retirement falsifies this sentence, so it is recorded as a `stale-rule` entry in `corpus_staleness` |
| 2 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet (*"Every caller launches it through `flow-walker.sh`"*) | — | D | `no-change` | A conventions document is never a planned target. The watcher now launches `devscene-planning-driver` through `hr_flow_host_exec` (Task 1), which falsifies this sentence; recorded as a `stale-rule` entry in `corpus_staleness` |
| 3 | `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` (*"every caller launches it through `flow-walker.sh`'s hand-off"*) | — | D | `no-change` | A conventions document is never a planned target; recorded as a `stale-rule` entry in `corpus_staleness` |
| 4 | `ARCHITECTURE.md` → the session-launch paragraph and the `planning-node-lib.sh` row of its launch table | — | A, B | `change` | Task 25 |
| 5 | `cli/README.md` → the outer-loop paragraph (*"the planning driver's three libraries (`lib/planning-*-lib.sh`)"*) | — | B | `change` | Task 6 |
| 6 | `cli/templates/scripts/README.md` → its opening paragraph (the three libraries, and *"the watcher's planning driver … runs `flow-walker.sh`"*) | — | A, B | `change` | Task 6 |
| 7 | `cli/templates/state-dir/improvement_observations/README.md` (*"the watcher's planning driver also writes labelled blocks … also commits and pushes its own blocks"*) | — | B | `no-change` | Still true: Task 11 keeps the labelled blocks and their `observations` commit |
| 8 | `cli/templates/state-dir/improvement_suggestions.md` (*"its planning driver also writes to it during planning"*) | — | B | `no-change` | Still true (Task 11) |
| 9 | `cli/templates/state-dir/run_analytics/README.md` (*"the driver's node-session manifest beside the run's stream"*) | — | B | `no-change` | Still true: Task 13 writes the same manifest, in the same place and the same shape |
| 10 | `devscene-flow-host/README.md` → the planning-hooks and entry sections (*"until the run-mode cutover (#424)"*), the command-line section, and the differences section (*"#419"*, *"#472"*) | — | A, B, C, D | `change` | Task 23 |
| 11 | `docs/cli.md` → *"Two families land in `scriptsDir`"* (the three libraries, and their deny-list sentence) | — | B | `change` | Task 25. Its `flow-host` doctor paragraph (*"the planning driver runs this checkout's walker and environment"*) is reviewed in the same task |
| 12 | `docs/config.md` → the `execution.scriptDrivenPlanning` row | — | B | `no-change` | Still true: the key, its default and the setup → driver → engine sequence are unchanged |
| 13 | `docs/flow-graph-walker.md` → `## 5. The two drivers` and the decisions naming `planning-*-lib.sh`, `pnl_init`, `pnl_reap` and `PNL_CORE_BLOCKS` | — | A, B, D | `change` | Task 24 |
| 14 | `docs/remote-execution.md` → *"A job takes script-driven planning on the same terms as a local run"* | — | B | `no-change` | Still true: the job runs the same `spawn_engine` and `planning_driver_ready`, as the task prompt decides |
| 15 | `docs/structured-agent-returns.md` → the driver's reading of a node's return (*"On the driver, a return with no block …"*) and its `pnl_reap` citations | — | A, B | `change` | Task 25 |
| 16 | `docs/watcher.md` → the shipped-script table rows for the three libraries, *"Node sessions, and the run's time"*, *"When a launch takes it"* and *"The driver's exit, mapped onto `classify_run_exit`"* | — | A, B | `change` | Task 25 |
| 17 | `plugin/docs/AUTONOMOUS_FLOW.md` → the routing row (*"on the opt-in script-driven path, by the watcher's planning driver"*, which no longer runs `flow-walker.sh`) | — | B | `change` | Task 7 |
| 18 | `plugin/instructions/improvement_observations_instructions.md` (*"a script-driven planning run, whose driver committed the file before Phase D"*) | — | B | `no-change` | Still true (Task 11) |
| 19 | `plugin/instructions/task_plan_writing_instructions_core.md` → its opening paragraph (*"the watcher's planning driver (`<scripts_dir>/lib/planning-driver-lib.sh`)"*, *"`<scripts_dir>/lib/planning-node-lib.sh` keys on"*) | — | A, B | `change` | Task 7 |
| 20 | `harness-runs/lessons.md` → *"When a change makes one run's sessions overlap, the run's headline time is the union of their intervals"* | — | E | `no-change` | Still holds: Task 13 keeps the manifest `run-analytics.sh` computes the union from |
| 21 | `harness-runs/lessons.md` → *"An opt-in switch for a run behaviour whose benefit holds in every execution mode is one every mode reads"* | — | E | `no-change` | Still holds: the switch stays `execution.scriptDrivenPlanning`, and the plugin root is still derived at run time (Task 2) |
| 22 | `harness-runs/lessons.md` → *"An unattended driver retries a unit's infrastructure-class failure … alone and a bounded number of times before parking"* | — | E | `no-change` | Still holds: Task 16 passes `ExecutionLimits(max_attempts=3, …)`, and Task 20 pins the retry |
