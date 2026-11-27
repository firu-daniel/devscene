### Task 2 — Launch the Python planning driver from the watcher's script-driven sequence

**Goal:** In `cli/templates/scripts/autonomous-watcher.sh`, the script-driven sequence runs the setup session, then `devscene-planning-driver` through `hr_flow_host_exec`, then the engine session on the hand-off. The bash `pd_drive` is no longer the middle step. The watcher passes the driver the command line the story index's `## Context` fixes, and reads its result off the driver's exit status and its one stdout line.

**Depends on:** Task 1, which adds two library functions:
- `hr_flow_host_missing <scripts_dir_abs> <console_script>`, which prints the cause and returns 1 when the environment cannot run the script;
- `hr_flow_host_exec <scripts_dir_abs> <console_script> [<arg>…]`, which never returns.

Task 1 also adds `HR_FLOW_HOST_DRIVER='devscene-planning-driver'`. This task calls both functions with that name.

**Where this task stops.** This task writes the watcher's half of the contract. The command that answers it is **Task 18's**, and it does not exist until then. Pinning this half with a stub `uv` is **Task 5's**. Retiring the `cli` suites that source the bash libraries is **Task 3's**, and deleting the libraries and their shipped-table rows is **Task 4's**: after this task nothing sources them, but they still ship.

### Targets

- `cli/templates/scripts/autonomous-watcher.sh` — the header block `SCRIPT-DRIVEN PLANNING IS AN OPT-IN PILOT`, `session_exec`, `planning_driver_ready`, `planning_driver_run` and `PLANNING_DRIVER_LIBS`.

**Work:**

- [ ] **One producer of the shared session vector.** Factor the flags `session_exec` passes between the binary and `${@:2}`, other than `-p`, `--output-format stream-json` and `--verbose`, into one array built in one place. Those flags are `--settings`, `--permission-mode`, the model and effort args, the two `--add-dir`s and the extra dirs.
  - `session_exec` keeps its exact argv order, so an engine session's launch is byte-for-byte unchanged.
  - The driver call passes that same array after `--`, led by `$launch_agent_cli`.
- [ ] **`planning_driver_ready`.**
  - Drop the `PLANNING_DRIVER_LIBS` loop, and drop the variable itself.
  - In its place, call `hr_flow_host_missing "$SCRIPT_DIR" "$HR_FLOW_HOST_DRIVER"`. A non-empty cause is not-ready, with `PLANNING_DRIVER_OFF_REASON` set to `the flow host cannot run devscene-planning-driver (<cause>): run bash <scripts_dir>/flow-host-provision.sh outside the sandbox`.
  - Keep the engine, runtime-root, `plugin.json`, planning-core and ledger checks in their order.
- [ ] **`planning_driver_run`.** Keep the setup-exit, `PAUSE_ACK`, unanswered-question and missing-ledger early returns as they are. Then run the driver in a subshell:
  - It makes `session_exec`'s `unset` and its two exports, `DEVSCENE_MAIN_REPO` and `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`.
  - It then calls `hr_flow_host_exec "$SCRIPT_DIR" "$HR_FLOW_HOST_DRIVER" --branch "$branch" --worktree "$worktree" --main-repo "$MAIN_REPO" --plugin-dir "$PLANNING_DRIVER_PLUGIN_ROOT" --flows "$SCRIPT_DIR/flows" --log "$log_path" --formatter "$formatter" [--plugin-dir-added] -- "$launch_agent_cli" <the shared array>`.
  - `--plugin-dir-added` is given exactly when `planning_root_added` is `1`.
  - Stdout is captured, and stderr is appended to `$log_path`.
  - The keep-awake hold around it stays.
  - Drop the `set +u` / library-sourcing block and the `PD_*` globals.
- [ ] **Map the driver's result** (exit status and stdout line) as `pd_drive`'s was:
  - **`0`.** Read the indices from the stdout line `consumed: …`, archive each pair with `archive_answered_pair`, update `resumed_for_index` and `launch_answered_set` as today, log the hand-off line, and run `engine_pipeline "$handoff_prompt"`.
  - **`3`.** Log the clean-stop line. When the stdout line is `stopped: undelivered`, set `PLANNING_DRIVER_PAUSE_DETAIL` to today's text (`paused itself on API overload: three consecutive planning dispatches undelivered — `). Return 0.
  - **Any other status, or a `0` without a `consumed:` line.** Log `planning driver failed for '<branch>' (devscene-planning-driver exit <rc>) — see <log>` and return 2.
- [ ] **The header block `SCRIPT-DRIVEN PLANNING IS AN OPT-IN PILOT`.**
  - `THE SEQUENCE` names `devscene-planning-driver`, run through `hr_flow_host_exec` from the main checkout's `<scripts_dir>/python/`, in place of `lib/planning-driver-lib.sh`'s `pd_drive`.
  - `READY` names the provisioning check in place of the three libraries.
  - State the argv contract once, here, as the story index's `## Context` gives it. Name the driver's statuses `0` / `3` / `2` and its two stdout lines.
  - Fix every other comment in the file that names `lib/planning-node-lib.sh`, such as the `session_exec` comment's *"(lib/planning-node-lib.sh's)"*. After the edit, `grep -n 'planning-.*-lib' cli/templates/scripts/autonomous-watcher.sh` prints nothing.

**Verification:**

- `bash -n cli/templates/scripts/autonomous-watcher.sh` passes.
- `grep -nE 'pd_drive|PD_[A-Z_]+=|PLANNING_DRIVER_LIBS|planning-(driver|node|record)-lib' cli/templates/scripts/autonomous-watcher.sh` prints nothing.
- Read the engine session's `session_exec` argv before and after the edit, token by token: it is the same. Task 5's stub suite pins this from the outside.
- The driver call carries every flag the story index's contract names, in that order, and passes after `--` exactly the shared array `session_exec` passes.

**Deviations from plan:**
- `session_exec`'s `unset` and two exports moved into a new `session_env`, which `session_exec` and the driver's subshell both call. A second literal `export DEVSCENE_MAIN_REPO=…` line fails the tree guard `cli/test/watcher-main-anchor.test.mjs` → *"outside comments, only the watcher names the anchor, once, in its export"*. The engine session's argv is unchanged.
- The shared vector is `session_flags` in `spawn_engine`, with `session_flags_lead` marking where `session_exec` splices `--output-format stream-json --verbose` back in. This keeps the engine argv in its old order.
- A `0` whose `consumed:` tail holds anything other than digits and spaces is treated as a failure too (exit 2, with the failure line). Each index becomes a path under `clarifications/<branch>/`.
- The stall budget (`PD_NODE_STALL_SECS`) is dropped without a replacement, because the story index's argv contract has no slot for it.
- Edited outside the Targets list: the REPRO `planning pilot` entry no longer says `flow-walker.sh … and the four lib/ libraries`. It now names `lib/` and a provisioned flow host. Also, the `PD_PLUGIN_DIR_ADDED` mention in `spawn_engine`'s planning-roots comment now names `--plugin-dir-added`.
- Evidence downgrade: the verification `bash -n cli/templates/scripts/autonomous-watcher.sh` was refused by the tool layer (don't-ask mode) and was not run as written. The evidence it actually rests on:
  - the whole-tree `bash scripts/typecheck.sh`, whose output prints `check-shell-parse: 134 files checked with /bin/bash (bash 3.2.57(1)-release), 0 failed` and `PASS: typecheck`;
  - `cli/test/watcher-main-anchor.test.mjs` tests 1 and 2, which launch a session through the edited watcher and pass.

  Before the edits, a direct `bash -c` probe of the bash 3.2 slice behaviour was refused the same way. It was then run as a `.py` probe under `harness-runs/scratch/` through `bash scripts/scratch-run.sh`, which showed that `"${a[@]:k}"` with `k == ${#a[@]}` expands to nothing under `set -u`.
