`feat_planning_driver_python_cutover` switches script-driven planning from the bash driver to GraphScene. Part of #376.

## Decided (2026-11-23)

- **The script driver stays opt-in through `execution.scriptDrivenPlanning`**, launched by the watcher, now over the Python walker that #419 makes the only one. The bash driver (`lib/planning-*-lib.sh`) is retired when this branch's suites pass on GraphScene. This replaces "perhaps with the bash driver behind a flag for a while"; the flag that remains chooses who drives (the orchestrator session or this driver), not which walker runs.
- **`uv` is already required by #419**, so this branch adds no new requirement. Making the graph driver the default for headless runs is #425's.

## Decided (2026-11-26)

- **The harness runs at most 5 dispatches at once, as a `devscene-flow-host` constant.** When the planning driver calls GraphScene's `start_run` / `continue_run`, it passes `ExecutionLimits(max_concurrent_dispatches=5, …)`. GraphScene's own default of 10 (`graphscene/src/graphscene/model/run_control.py`, from #484) is for hosts that set none. The value is not a `devscene.config.json` key: the flow host is the harness's own implementation of its flows, so values that tune them stay in it.
- **When this branch completes, no code in `graphscene/` or `devscene-flow-host/` mentions an issue number.** Branches before it may leave references such as `(#421)` or `(#423)` in docstrings and comments, including `graphscene/src/graphscene/engine/run_loop.py`, `set_execution.py`, `facade/cli.py` and `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` as of #484. This branch removes every one of them, whichever branch added it, in source and tests alike, keeping what each sentence says without the number.

## Decided (2026-11-27)

- **The walk stays in the file store; no ledger-backed store.** `FileStateStore` (`devscene-flow-host/src/devscene_flow_host/host/store.py`) keeps the walk at `<stateDir>/.flow_walker_state/`, gitignored. It already survives the three interruptions: a pause, a stop or a crash leaves the run copy, and with it the file, in place; a remote job carries `.flow_walker_state` across job boundaries in its `harness-state` bundle (`cli/templates/scripts/lib/harness-run-lib.sh` → `hr_remote_names_var`, `HR_REMOTE_WALKER_FILE`). When the saved walk is missing or unusable, #423's `decide_planning_entry` rebuilds the entry from the ledger's `P1`–`P3`, the answered pairs and the round files, as `pd_entry` does.
- **The corpus-staleness record is not this branch's.** It goes to a follow-up that adds a per-run summary file (the Done summary as a fixed-structure file, with its owed-before-merge and owed-after-merge sections). This branch keeps the bash pilot's behaviour, which drops `corpus_staleness`.
- **Remote runs stay on the same path, and must not break.** A remote job runs `autonomous-watcher.sh job`, which goes through the same launch function and `planning_driver_ready` test as a local launch (`cli/templates/github/workflows/devscene-run.yml`), so the cutover reaches remote runs with no separate wiring. What remote adds: the job needs `uv` and the provisioned packages (#478's `setup-uv`), and anything the driver must keep across a job boundary has to be in the bundle (the walk is, under `.flow_walker_state`; so is a `planning` directory).

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- The `planning-*` and `watcher-planning-driver` suites pass against GraphScene, with tests that pinned bash internals rewritten against behaviour.
- The watcher's `execution.scriptDrivenPlanning` path launches the planning driver's entry in `devscene-flow-host/` (#418), which runs the planning graph on GraphScene with the harness's executor (#421), GraphScene's run loop (#484) and hooks (#423).
- **Wiring #423's pieces** _(from #423's branch, `feat_graphscene_node_hooks`)._ #423 built every host piece and called none of them outside its suites; acting on them is this branch's (`decide_planning_entry`'s docstring says so):
  - `decide_planning_entry(walker, repo_root, state_dir, branch)` (`host/planning_entry.py`) returns `PlanningDone`, `ContinueWalk` or `StartWalk`, ported from `pd_entry` in its order. The driver maps them to nothing, `continue_run` and `start_run`. Archiving the consumed answered pairs stays the watcher's.
  - `CorePromptBuilder(graph, plugin_dir, repo_root, state_dir, branch, pairs)` (`host/agent_prompts.py`) is the `AgentPromptBuilder` ported from `pnl_prompt`. It takes the writer pairs at construction and appends them once, to the first writer dispatch it builds, and returns the same text for a repeated build. Pass it the pairs the entry decision kept.
  - `PlanningHooks` (`host/planning_hooks.py`) is the `HookHost` passed as `start_run(..., hooks=...)` / `continue_run(..., hooks=...)`. It implements the graph's `commit_plan_round`, `flip_ledger` and `commit_convergence` hooks (Overrides 3, 4 and 6, and Override 5's ledger flips) through the main checkout's commit wrapper (`host/commit_points.py`). From the cutover the bash driver's own commits and flips (`pd_act`, `pd_handoff`, `prl_round_commit`, `prl_convergence_commits`, `prl_ledger_flip`) go, or every commit happens twice.
  - Hooks run in run mode only: step mode and `flow-walker.sh` run none.
- **Pause, park and escalation are this branch's** _(from #423's branch)._ #423 made the ledger flips hooks but left the rest of Override 5 to the run driver, because none of it is a node or round event; each arrives as a `RunExit` the driver acts on: a `Halt("pause")` with its `plan-round-partial` commit, an `<ask>` park (questions from `SessionUsage.return_document`, as `pd_ask_park` reads them), and an `<escalate>` park with its partial commit.
- **Constructing the harness's executor** _(from #421's branch, `feat_flow_host_claude_executor`)._ `ClaudeExecutor` (`devscene-flow-host/src/devscene_flow_host/host/claude_executor.py`) takes everything from the host:
  - `plugin_name` from `read_plugin_name`, and one `AgentContract` per agent from `read_agent_contract` (`records/plugin_contracts.py`);
  - `inactivity_limit_seconds=NODE_INACTIVITY_LIMIT_SECONDS` (2685.0, the pilot's effective `PD_NODE_STALL_SECS`);
  - the `AgentPromptBuilder`: #423's `CorePromptBuilder` (above);
  - `session_args`, the shared flags (sandbox, permission mode, settings, model), passed through unchanged. They must include `--add-dir <plugin_dir>`, which the executor does not add (`pnl_agent_flags`);
  - `agent_args`, each agent's MCP flags as `pnl_agent_flags` builds them: `--disallowedTools mcp__*`, or `--strict-mcp-config --mcp-config <the worktree's .mcp.json cut to the agent's servers>`.

  The executor refuses any host flag it sets itself (`EXECUTOR_FLAGS`).
- **The usage sink is this branch's** _(from #421's branch)._ `usage_sink.record(SessionUsage)` is called once per `run` that returns, just before the return, so a node's usage record comes just before its next `Launch` row. Pair the two on `node`, with an equal `result` as the check. A `Launch` row written by the total-run timeout has no usage record, and is not a pairing fault. `SessionUsage` also carries what the pilot's driver reads elsewhere:
  - `stream`, to write as the pilot's `<seq>-<node>.stream.jsonl`;
  - `return_document`, for `pd_ask_park`'s `questions` and `pd_ret_field`'s `tasks_count`, `tests_count` and `reason`;
  - `stderr_tail` and `returncode`;
  - `started_at`, `duration_seconds` and `total_cost_usd`, for the observation rows;
  - `agent_prompt`.
- **The bash driver reads the format-5 graph already** _(from #459's and #423's branches)._ #459 retired the format-3 graph and shipped the planning graph under `<scriptsDir>/flows/task_plan_writing.graph.json`; #423 raised it to format 5 (`promptSource`, `vocabulary.hooks`, `before` / `after`). `PNL_GRAPH`, `PNL_REAP_JQ` and `PD_ROUND_GATES` read it without edits, and `PNL_CORE_BLOCKS` is held to the graph's `promptSource` by a `cli` case until this branch retires it. Retiring `lib/planning-*-lib.sh` leaves no reader of an older format.
- **`Dispatch.prompt` is `Dispatch.prompt_variant`** _(from #423's branch)._ #423 renamed it, so that it is not mistaken for the agent prompt, and raised the walk-state document's version with it.
- **Issue numbers left by #423.** Besides the files named above, #423 added `#424` and `#325` references in `graphscene/` and `devscene-flow-host/`; the decided removal covers them.
- `docs/flow-graph-walker.md` brought up to date.
- A real planning run on a throwaway branch, as a user step, local and remote.

## Depends on

#419, #421, #423
