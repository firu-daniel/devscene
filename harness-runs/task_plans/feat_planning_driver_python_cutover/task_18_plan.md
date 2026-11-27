### Task 18 — Add the `devscene-planning-driver` command over the planning run

**Goal:** Add the console script the watcher launches, `devscene-planning-driver = "devscene_flow_host.commands.planning_driver:main"`. It parses the command line the story index's `## Context` fixes, runs `run_planning` then `act_on_exit`, flushes observations on every exit, and answers with the contract's statuses and one stdout line.

**Depends on:**
- **Task 2.** The watcher calls `hr_flow_host_exec "$SCRIPT_DIR" devscene-planning-driver --branch … --worktree … --main-repo … --plugin-dir … --flows … --log … --formatter … [--plugin-dir-added] -- <agent_cli> <shared flags…>`. It reads `0` with `consumed: …`, `3` with `stopped: <kind>`, and anything else as a fault.
- **Task 1.** It declares `HR_FLOW_HOST_DRIVER='devscene-planning-driver'` in `cli/templates/scripts/lib/harness-run-lib.sh`, whose mirror comment says `devscene-flow-host`'s suite holds it equal. This task's test is that holder.
- **Task 16.** `host/planning_run.py` → `PlanningRequest` and `async run_planning(request) -> PlanningOutcome`.
- **Task 17.** `host/run_exits.py` → `async act_on_exit(outcome, *, graph, repo_root, main_repo, state_dir, branch, wrapper, observations, narrate, now) -> StopKind`, one of `handed_off`, `park`, `pause`, `undelivered`, `stop`, `cap` or `kill_switch`. This command passes `graph` as the loaded planning graph, `repo_root` as `--worktree`, `main_repo` as `--main-repo`, `wrapper` as the same `<main_repo>/<scripts_dir>/commit-on-branch.sh` Task 16 builds from `read_config(main_repo).scripts_dir`, and `now` as the current UTC time.
- **Task 11.** `Observations.flush(…)`.

**Where this layer stops.** Rendering and exit statuses are the `commands` layer's, never a reader's or the host's (`.claude/context/devscene-flow-host.md` → `## Errors`). This module decides no walk step.

### Targets

- `devscene-flow-host/src/devscene_flow_host/commands/planning_driver.py` (new)
- `devscene-flow-host/pyproject.toml` — `[project.scripts]` gains `devscene-planning-driver`
- `devscene-flow-host/tests/test_planning_driver_command.py` (new)

**Work:**

- [ ] **The parser.**
  - **Required flags:** `--branch`, `--worktree`, `--main-repo`, `--plugin-dir`, `--flows`, `--log` and `--formatter`, each a non-empty value.
  - **`--plugin-dir-added`** is optional and takes no value.
  - **After `--`:** at least the agent CLI.
  - **Usage errors.** A missing, empty or unknown flag, or a missing `--` / agent CLI, is a usage error with a one-line cause naming the flag.
- [ ] **The steps of `main(argv, stdout, stderr) -> int`.**
  - Load `<flows>/task_plan_writing.graph.json` through `graphscene.load_graph_file`. The flow name is the `FLOW = "task_plan_writing"` `Final`.
  - Resolve `stateDir` from the worktree's configuration.
  - Make a scratch directory with `tempfile.mkdtemp`, removed in a `finally`, file by file and then the directory, never recursively.
  - Build the `PlanningRequest`:
    - `environ=os.environ`;
    - `venv` = `sys.prefix` as a `Path` when it differs from `sys.base_prefix`, else `None`;
    - `narrate` appends `[plan-drive] <line>\n` to `--log`.
  - Run `run_planning`, then `act_on_exit`, then always `Observations.flush`, after first adding the session-table observation *"Script-driven planning node sessions (devscene-planning-driver returned <status>)"* when any session ran.
- [ ] **The exit statuses.**
  - **Handed off.** `handed_off` writes exactly `consumed:` plus ` <i>` per consumed index, and a newline, to stdout, and returns `0`.
  - **Clean stops.** Each other kind writes `stopped: <kind>` and returns `3`. The kinds are `park`, `pause`, `undelivered`, `stop`, `cap` and `kill-switch`, with `kill_switch` written as `kill-switch`.
  - **Faults.** Each of the following writes one `planning-driver: <cause>` line to stderr, with a newline in the cause flattened, writes nothing to stdout, and returns `2`:
    - a usage error;
    - a `RecordError`, `GraphError`, `CommitPointError` or `OSError`;
    - a `ValueError` or `LookupError` out of construction;
    - any other `Exception`, as `internal error: <type>: <message>`.

    The cause is also narrated to the log. Only `KeyboardInterrupt` and `SystemExit` escape.
  - **The docstring** states this contract under *"The rule:"*, as `commands/flow_walker.py`'s states its own, and carries a *"Deliberately not covered"* list: deciding any walk step or the run's entry, which is `host/planning_run.py`'s; acting on a `RunExit` — narration, parks, pause files, partial commits — which is `host/run_exits.py`'s; and reading any record, which is `records`'.
- [ ] **`pyproject.toml`.** Add `devscene-planning-driver = "devscene_flow_host.commands.planning_driver:main"` under `[project.scripts]`, beside `devscene-flow-walker`. No dependency changes and no re-lock.
- [ ] **`tests/test_planning_driver_command.py`:**
  - its header rule;
  - each usage refusal's exact stderr text, with exit `2` and empty stdout;
  - a fully resolved ledger giving exit `0` and stdout `consumed:\n`;
  - a planted kill switch giving exit `3` and `stopped: kill-switch\n`;
  - a graph directory without the graph giving exit `2` naming the file;
  - one subprocess run of the module through `sys.executable -m devscene_flow_host.commands.planning_driver`, writing to the real stdout;
  - the console-script declaration: `[project.scripts]` in `devscene-flow-host/pyproject.toml` maps `devscene-planning-driver` to this module's `main`;
  - the mirror: `cli/templates/scripts/lib/harness-run-lib.sh`, read read-only, carries the line `HR_FLOW_HOST_DRIVER='devscene-planning-driver'`. Its assertion message names the remedy: edit both together.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_driver_command.py` passes.
- `bash scripts/python-service.sh --package devscene-flow-host lint` and `… typecheck` exit zero.
- `commands/planning_driver.py` reaches the walk only through `host/planning_run.py` and `host/run_exits.py`, never `Walker`'s own methods.
