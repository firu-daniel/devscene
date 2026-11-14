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

  `pd_drive` returns `0` (planning handed off), `3` (a clean stop whose park, pause or halt files are written) or `2` (a fault, with one `planning-driver: <cause>` line on stderr). It also sets **`PD_CONSUMED_SET`**: the space-separated indices, spelled as `hr_top_level_answered_pairs` prints them, of the answered pairs it appended to a resumed writer's prompt, or empty. That set is the top-level answered pairs minus the two origins the driver leaves out (a `Phase G` origin, and the prompt-injection screen's), so it is a subset of the launch's recorded `launch_answered_set`.
- **Task 4**, which makes `init` write the three libraries beside the watcher, under `<scriptsDir>/lib/`.
- **Task 5**, whose stub behaviour this task's suite restates below rather than imports, so that this file alone defines what its suite's stub does.
- **Task 10**, which already moved `max_question_index` and `top_level_answered_pairs` out of this file into `lib/harness-run-lib.sh` as `hr_max_question_index` and `hr_top_level_answered_pairs`, and renamed every call site here. This task edits the watcher on top of that state, adds no definition of either, and calls them only by the `hr_` names.

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
     - **`0`** → archive **only the set the driver consumed**: `archive_answered_pair` once per index of `PD_CONSUMED_SET`, so the engine's Override 2(a) cannot hand those answers to a writer again. Then remove exactly those indices from the registry's `resumed_for_index` and `launch_answered_set`, leaving every other index in place. A pair the driver left out (a `Phase G` origin, or the prompt-injection screen's) is therefore neither archived here nor dropped from the record: it stays at the top level for the engine session, and `classify_run_exit` archives it after that session through the union it reads today. Then run the engine pipeline a second time with today's fresh-launch prompt and no clause, and take its `rc`.

  `log_stopped_background_tasks`, `record_run_analytics` and `classify_run_exit` then run once, as today.
- [ ] **`cli/test/watcher-planning-driver.test.mjs`.**
  - Open it with its rule. Use `cli/test/helpers/watcher.mjs`'s fixture and `tick`.
  - The switch's value is a plugin directory the suite builds under the system temp directory, copying this checkout's `plugin/.claude-plugin/plugin.json`, every planning agent file under `plugin/agents/` that the graph's nodes name, and `plugin/instructions/task_plan_writing_instructions_core.md`.
  - The stub CLI tells the three kinds apart and records each argv to a calls log:
    - **the setup session**: its `-p` prompt carries `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`. The stub writes the task-engine ledger with `P0` `[x]` and `P1`–`P3` `[ ]` and its `## Run mode` block, and exits 0;
    - **a node session**: its argv carries `--agent <plugin name>:<agent>`. The stub prints `--output-format stream-json` lines on stdout: first an `init` event whose `tools` are exactly the list on the named agent file's `tools:` line, then a `result` event with `subtype: success`, a `total_cost_usd` number and `structured_output` carrying the four keys `outcome`, `findings_file`, `return` and `harness_friction` (an empty list). By agent:
      - `task-plan-writer`: writes a story index and one per-task file at the paths its prompt names, then answers `outcome: returned` with `findings_file: null`; when the case is the park case, it writes nothing and answers `outcome: questions` with a non-empty `return` text;
      - a plan gate (`task-plan-reviewer`, `architecture-reviewer`, `business-parity-reviewer`): writes `<findings_folder>review_<iteration>.md` from its prompt's `findings_folder:` and `iteration:` lines, carrying `verdict: PASS`, and answers `outcome: PASS` with `findings_file` set to that path;
      - `ui-tests-plan-writer`: answers `outcome: no_ui`;
    - **the engine session**: its prompt lacks the clause and its argv lacks `--agent`. The stub flips every ledger entry to `[x]` and exits 0.
  - The suite writes the stub itself and imports nothing from `cli/test/helpers/planning-driver.mjs`; every literal it asserts on is spelled in the suite.
  - Cases:
    1. **Switch unset.** One session, with no clause and no `--agent` in its argv.
    2. **Switch set.** The setup session first; then node sessions whose argv carries the same `--settings`, `--permission-mode` and `--add-dir` values as the setup session plus `--agent devscene:task-plan-writer` and `--plugin-dir <switch>`; then one engine session without the clause. The record ends `completed`.
    3. **Switch set, and the driver parks.** No engine session follows, and the record is `parked`.
    4. **Switch set to a directory with no `plugin.json`.** One session, with no clause, and the `planning driver off` line in the watcher log.
    5. **Hand-off archives only what the driver consumed.** The channel is seeded with an answered pair parked by `task-plan-writer` and an answered pair whose question names a `Phase G` origin, and a story index exists. After the driver hands off, the writer's pair is under `answered/` before the engine session starts (the stub records the channel's top level at the engine session's start), the `Phase G` pair is still at the top level at that point, and both are under `answered/` once the run is classified.

  This task edits no existing watcher suite. Their passing unchanged is the switch-off evidence the task prompt asks for, and the Run gates round runs them.

**Verification:**

- `cli/test/watcher-planning-driver.test.mjs` passes.
- `git diff` of `autonomous-watcher.sh` shows the engine head's `exec` argv unchanged in content and order, now produced inside `session_exec`. With the switch unset, no new code path runs before the first engine session.
- The main-checkout anchor's export stays only in `session_exec`, in the watcher, and is never in a planning library.
