### Task 6 — Wire the pilot into `autonomous-watcher.sh`: `PLANNING_DRIVER_PLUGIN_DIR`, `session_exec`, and the setup → driver → engine sequence

**Goal:** Give the watcher the pilot's one switch and the launch sequence it selects:
- **Switch off** (the default): the launch is byte-for-byte today's.
- **Switch on, in a local run of the task engine whose planning is not finished:**
  1. a setup session, the engine with the `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH` clause;
  2. the planning driver;
  3. on the driver's hand-off, the engine session as usual.

Every node session gets the engine's own launch vector from one producer, `session_exec`.

**Depends on:**
- **Task 3**, which produces `pd_drive <branch> <worktree> <log_path>`. The watcher calls it in `<worktree>` with five globals:
  - `PD_PLUGIN_DIR`: the switch's value;
  - `PD_MAIN_REPO`: `$MAIN_REPO`;
  - `PD_SESSION_EXEC`: the string `session_exec`;
  - `PD_FORMATTER`: the formatter `spawn_engine` already chose, or `cat`;
  - `PD_NODE_STALL_SECS`: `0` when `STALL_CHECK_ENABLED` is not `1`, else the larger of `STALL_WARN_SECS` and `STALL_KILL_SECS − POLL_INTERVAL_SECS`. That way a node the driver judges stalled is killed and recorded before the watcher's next pass could judge the whole run stalled from the shared run log.

  `pd_drive` returns `0` (planning handed off), `3` (a clean stop whose park, pause or halt files are written) or `2` (a fault, with one `planning-driver: <cause>` line on stderr).
- **Task 4**, which makes `init` write the three libraries beside the watcher, under `<scriptsDir>/lib/`.

Task 7 implements the engine command's side of the clause literal this task prints. The setup session's behaviour on that clause is not this task's.

### Targets

- `cli/templates/scripts/autonomous-watcher.sh`: the tunable, `session_exec`, the readiness check, the clause and the sequence, the header and the `status` line.
- `cli/test/watcher-planning-driver.test.mjs` (new): its suite.

**Work:**

- [ ] **The switch and its documentation.**
  - Declare `PLANNING_DRIVER_PLUGIN_DIR="${PLANNING_DRIVER_PLUGIN_DIR:-}"` beside the other tunables. Like them, it can be set from the environment or from `watcher.env`.
  - Add `PLANNING_DRIVER_PLUGIN_DIR=<value or empty>` to `print_status`'s `tunables:` line.
  - Add a header paragraph `SCRIPT-DRIVEN PLANNING IS AN OPT-IN PILOT`. It states four things:
    - the switch, its default (empty, meaning off) and why it is a watcher setting rather than a configuration key: a machine-local path, and a not-yet-measured seam;
    - that it pins the plugin every node session resolves;
    - that it is read in local mode only, so a job always takes the orchestrated path;
    - the sequence, and the readiness conditions below.
  - Add a `REPRO` entry that runs one `tick` with the switch set against a stub CLI and shows the three session kinds in the stub's log.
- [ ] **`session_exec <prompt> [extra flag…]`: one producer of the flag vector.**
  - Factor the launch head's `unset` / two `export`s / `exec` into this function. It is defined at top level and reads `spawn_engine`'s locals by dynamic scope: `session_unset_names`, `launch_agent_cli`, `settings_file`, `launch_permission_mode`, `model_args`, `effort_args`, `worktree`, `main_state`, `extra_dir_args` and `log_path`.
  - It runs `exec "$launch_agent_cli" -p "$1"` with exactly the flags the header's flag string lists, in that order, followed by `"${@:2}"`.
  - The engine pipeline's head calls `session_exec "$launch_prompt"` with no extra flag, so its argv is unchanged.
  - The header's flag-string block gains one sentence: the per-node flags `lib/planning-node-lib.sh` appends follow the shared vector.
- [ ] **`planning_driver_ready <branch> <worktree> <state_rel> <engine_kind>`.** It answers ready only when all of these hold:
  - the switch is non-empty;
  - `JOB_MODE` is not `1`;
  - `engine_kind` is `task`;
  - `$SCRIPT_DIR/lib/planning-node-lib.sh`, `planning-record-lib.sh` and `planning-driver-lib.sh` are readable;
  - `<switch>/.claude-plugin/plugin.json` and `<switch>/instructions/task_plan_writing_instructions_core.md` are readable;
  - the run's ledger is absent, or `hr_ledger_phases` reports its first phase `pending`.

  With the switch set and not ready, log one `planning driver off for '<branch>': <reason>` line and launch exactly as today. When ready, `spawn_engine` adds the clause *"PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH: run only the task engine command's steps 1–4 and its script-driven setup step, then end the session; a script runs the planning loop."* to `launch_prompt`, whatever resume or pause clause it also carries.
- [ ] **The sequence in the launch subshell.**
  1. **The setup session.** The pipeline runs as today, through `session_exec`, giving `rc`.
  2. **The driver runs** when `rc` is `0`, there is no `PAUSE_ACK`, there is no top-level `question_<n>.md` without its `answer_<n>.md`, and the ledger exists. The watcher sources the three libraries, sets the five `PD_*` globals and calls `pd_drive`, keeping the host awake across it as the engine head does.
  3. **Map the driver's return:**
     - **`3`** → `rc=0`, so `classify_run_exit` reads the park, pause or ledger from disk exactly as after an engine session;
     - **`2`** → `rc=2`, with one `planning driver failed for '<branch>'` log line;
     - **`0`** → archive the launch's consumed pairs exactly as `classify_run_exit` does (`archive_answered_pair` over the union of `resumed_for_index` and `launch_answered_set`, then clear both fields), so the engine's Override 2(a) cannot hand them to a writer again. Then run the engine pipeline a second time with today's fresh-launch prompt and no clause, and take its `rc`.

  `log_stopped_background_tasks`, `record_run_analytics` and `classify_run_exit` then run once, as today.
- [ ] **`cli/test/watcher-planning-driver.test.mjs`.**
  - Open it with its rule. Use `cli/test/helpers/watcher.mjs`'s fixture and `tick`.
  - The stub CLI tells the three kinds apart and records each argv:
    - the setup session's prompt carries the clause, and the stub writes the ledger and exits 0;
    - a node session carries `--agent`, and the stub answers as Task 5's stub does;
    - the engine session's prompt lacks the clause, and the stub flips every ledger entry.
  - Cases:
    1. **Switch unset.** One session, with no clause and no `--agent` in its argv.
    2. **Switch set.** The setup session first; then node sessions whose argv carries the same `--settings`, `--permission-mode` and `--add-dir` values as the setup session plus `--agent devscene:task-plan-writer` and `--plugin-dir <switch>`; then one engine session without the clause. The record ends `completed`.
    3. **Switch set, and the driver parks.** No engine session follows, and the record is `parked`.
    4. **Switch set to a directory with no `plugin.json`.** One session, with no clause, and the `planning driver off` line in the watcher log.

  This task edits no existing watcher suite. Their passing unchanged is the switch-off evidence the task prompt asks for, and the Run gates round runs them.

**Verification:**

- `cli/test/watcher-planning-driver.test.mjs` passes.
- `git diff` of `autonomous-watcher.sh` shows the engine head's `exec` argv unchanged in content and order, now produced inside `session_exec`. With the switch unset, no new code path runs before the first engine session.
- The main-checkout anchor's export stays only in `session_exec`, in the watcher, and is never in a planning library.
