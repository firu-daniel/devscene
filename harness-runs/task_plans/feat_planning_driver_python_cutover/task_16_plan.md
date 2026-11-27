### Task 16 — Compose the planning run and drive it with `start_run` / `continue_run` in `host/planning_run.py`

**Goal:** `run_planning` composes every host piece the task prompt's leads name, decides the entry, and drives the walk once to its `RunExit`. It returns that exit with what Task 17 needs to act on it. This is the step that wires #423's pieces: until now, none of them was called outside its suites.

**Depends on:** Tasks 9, 11, 12, 13, 14 and 15, which produce the pieces this module consumes:
- **Task 9.** `records/core_limits.py` → `read_max_total_dispatches(plugin_dir) -> int`, and `records/config.py` → `read_config(repo_root).scripts_dir: str`, `scriptsDir` read as `hr_scripts_dir` reads it, repo-relative with no trailing `/`, `devscene-scripts` by default.
- **Task 11.** `host/observations.py` → `Observations`.
- **Task 12.** `host/run_control.py` → `FileRunSignals(repo_root, state_dir)`, `FileDispatchCounter(repo_root, state_dir)` with `reset()`, `kill_switch_present(main_repo) -> bool`, `planning_limits(dispatch_cap) -> ExecutionLimits` and `UNDELIVERED_LIMIT = 3`.
- **Task 13.** `host/node_sessions.py` → `NodeSessions(*, log_path, formatter, observations, narrate)`, which is both the `UsageSink` and the `LaunchSink`, with `rows` and `return_document(node)`.
- **Task 14.** `records/mcp_servers.py` → `read_mcp_servers(worktree) -> Mapping[str, object]`, which raises `RecordError` on an unreadable `.mcp.json`; and `host/agent_flags.py` → `session_args(shared, plugin_dir, *, plugin_dir_added)`, `agent_args(contracts, mcp_servers, scratch)` and `session_env(environ, *, venv)`.
- **Task 15.** `host/planning_executor.py` → `PlanningExecutor(inner, *, graph, repo_root, state_dir, branch)` and `clear_revision_findings(repo_root, state_dir, branch)`.

It also uses the existing #421 / #423 pieces with their present signatures:
- `decide_planning_entry(walker, repo_root, state_dir, branch)`, which returns `PlanningDone`, `ContinueWalk(outcome, pairs)` or `StartWalk(entry, resume, pairs)`;
- `CorePromptBuilder(graph, *, plugin_dir, repo_root, state_dir, branch, pairs)` with `.consumed`;
- `ClaudeExecutor(*, command, plugin_dir, plugin_name, cwd, contracts, inactivity_limit_seconds, usage_sink, agent_prompt_builder, session_args, agent_args, env)`;
- `NODE_INACTIVITY_LIMIT_SECONDS`;
- `read_plugin_name(plugin_dir)` and `read_agent_contract(plugin_dir, agent)`;
- `PlanningHooks(graph, *, repo_root, state_dir, branch, commit_wrapper)`;
- `open_walker(repo_root, branch, graph)`.

**Where this task stops.** It returns the `RunExit`, and does nothing with it beyond what hooks did during the run. Hand-off logging, pause files, partial commits and parks are **Task 17's**. Flushing observations and exit statuses are **Task 18's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` (new)
- `devscene-flow-host/tests/test_planning_run.py` (new)
- `devscene-flow-host/tests/fake_planning_agent.py` (new) — the scripted fake agent CLI that Tasks 19 and 20 also drive

**Work:**

- [ ] **The two types, and the preflight.**
  - `PlanningRequest` is a frozen dataclass of: `branch`, `worktree`, `main_repo`, `plugin_dir`, `graph` (a loaded `FlowGraph`), `log_path`, `formatter`, `plugin_dir_added`, `command` (the agent CLI as a one-tuple), `shared_args`, `environ`, `venv`, `scratch`, `observations` and `narrate`.
  - `PlanningOutcome` is a frozen dataclass of:
    - `kind`: one of `done`, `kill_switch`, `stop_file` or `run`;
    - `exit: RunExit | None`;
    - `consumed: tuple[int, ...]`;
    - `last_round: int | None`;
    - `pending_round: int | None`, the round number of the walk's pending dispatch when the run halted;
    - `sessions: NodeSessions | None`.
  - **The preflight in `async run_planning(request) -> PlanningOutcome`**, in `pd_main`'s order:
    - **Kill switch.** When `kill_switch_present(main_repo)`, return `kind="kill_switch"` and dispatch nothing.
    - **STOP file.** When the worktree's `STOP` is present, return `kind="stop_file"`.
    - **No ledger.** A missing ledger raises `RecordError("the flow-progress ledger '<stateDir>/flow_progress/<branch>_progress.md' does not exist; the setup session creates it")`.
    - **Then** reset the counter, open the walker and call `decide_planning_entry`. `PlanningDone` returns `kind="done"` with `consumed=()`.
- [ ] **The composition.**
  - **The prompt builder.** `CorePromptBuilder` gets the entry's `pairs`.
  - **The contracts.** One `read_agent_contract` per distinct `agent` of the graph's dispatch nodes.
  - **The executor.** `ClaudeExecutor` is constructed with:
    - `command=request.command`, `cwd=worktree` and `plugin_name=read_plugin_name(plugin_dir)`;
    - `inactivity_limit_seconds=NODE_INACTIVITY_LIMIT_SECONDS`;
    - `usage_sink=sessions` and `agent_prompt_builder=builder`;
    - `session_args=session_args(shared_args, plugin_dir, plugin_dir_added=…)`;
    - `agent_args=agent_args(contracts, read_mcp_servers(worktree), scratch)`;
    - `env=session_env(environ, venv=venv)`.

    It is wrapped in `PlanningExecutor`.
  - **The hooks.** `PlanningHooks` gets the main checkout's commit wrapper, `main_repo / read_config(main_repo).scripts_dir / "commit-on-branch.sh"`, the `scripts_dir` attribute Task 9 adds. This module reads no configuration key itself: every value it takes from `devscene.config.json` comes through `read_config`. The run is handed a `HookHost` wrapper, `_DrivenHooks`. It delegates every call to `PlanningHooks`, and on each `commit_plan_round` call:
    - records the passage's round number as `last_round`;
    - calls `clear_revision_findings`, as `record_outcome` clears on a `RoundPassage`.

    `provides` is `PlanningHooks.provides`.
- [ ] **The run.**
  - **`StartWalk`.** `start_run(walker, executor, signals=FileRunSignals(…), counter=…, sink=sessions, limits=planning_limits(read_max_total_dispatches(plugin_dir)), failure_outcome="error", undelivered_limit=UNDELIVERED_LIMIT, entry=…, resume=…, hooks=_DrivenHooks(…))`.
  - **`ContinueWalk`.** `continue_run(…, outcome=…)`, with the same keywords.
  - **After the run.** When the exit is a `Halt`, set `pending_round` from `walker.current()`: a `Dispatch`'s `round_number`, or the first dispatch's of a `DispatchSet`, or `None`.
  - **Return** `kind="run"` with the exit, `builder.consumed`, `last_round` and `sessions`.
  - **Docstring.** *"The rule:"* names `pd_main` / `pd_entry` / `pd_run_set`, retired. *"Deliberately not covered"*: acting on the exit, exit statuses, and the observation flush.
- [ ] **`tests/fake_planning_agent.py`, the fake agent CLI.** A test-support module with its own docstring rule, run as `sys.executable fake_planning_agent.py <script.json> <argv…>`.
  - **What it reads.** It reads its agent from `--agent <plugin>:<agent>`, and that agent's `tools:` line from `--plugin-dir`.
  - **What it records.** It appends one JSON line per call to the script's calls log: `agent`, `prompt` (the `-p` value), `argv`, the environment's `VIRTUAL_ENV` / `PYTHONPATH`, and start and end times.
  - **What it answers.** It prints an `init` event carrying those tools and a `success` result. The result text ends in a ```` ```json ```` return block valid against `plugin/schemas/<agent>.return.json`. That block is the script's next scripted return for that agent, or a default one:
    - the writer returns `returned` with a `tasks_count`;
    - a reviewer returns `PASS`.
  - **Findings files.** For a reviewer it writes the findings file named by the prompt's `findings_folder:` / `iteration:` lines, with one verdict line.
  - **Scripted failures.** A scripted entry may instead ask for no `init`, a result with `is_error`, a missing return block, or a sleep.
- [ ] **`tests/test_planning_run.py`** uses the real planning graph and the real planning core, read-only. Its scenarios use `fake_planning_agent.py`, a fake `commit-on-branch.sh` that logs its argv, as `tests/test_planning_hooks.py` → `_plant_wrapper` does, and a minimal ledger. Cases:
  - its header rule;
  - the kill switch dispatches nothing;
  - STOP dispatches nothing;
  - all of `P1`–`P3` resolved gives `done`;
  - a fresh walk runs to an `End`, with the wrapper's calls in order: `plan-round` 0, `ledger-flip` P1, …, `task-plan`, `ledger-flip` P3;
  - a planted PAUSE gives a `Halt("pause")` with `pending_round` set;
  - an answered pair is consumed and reported in `consumed`;
  - a node session's environment, recorded by the fake, carries no `VIRTUAL_ENV` or `PYTHONPATH`;
  - at most 5 node sessions run at once, from the fake's recorded start and end times. Order only is asserted, no duration.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_run.py` passes.
- `grep -nE 'devscene\.config\.json|scriptsDir|\.mcp\.json' devscene-flow-host/src/devscene_flow_host/host/planning_run.py` prints no hit outside its docstring.
- `planning_run.py` imports from `graphscene` only through its public surface (`from graphscene import …`, never a submodule), and from `devscene_flow_host` only through each name's defining module, never the package root.

**Deviations from plan:**
- `PlanningRequest.command` is typed `tuple[str, ...]`, not a one-tuple: the suite's agent CLI is `(sys.executable, fake_planning_agent.py, <script.json>)`, as the plan's own `fake_planning_agent.py` bullet runs it; production passes a one-tuple through the same field.
- `tests/test_planning_run.py` adds one case beyond the plan's list, the missing ledger's exact `RecordError` message, which the preflight bullet specifies.
