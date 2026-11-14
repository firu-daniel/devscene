### Task 5 — Test the driver end to end with a stub agent CLI: walk, sets, held binding, park, STOP, PAUSE, cap and observations

**Goal:** Pin `pd_drive`'s behaviour through the copies `init` ships, with a stub agent CLI standing in for every node session. This is the test task Task 3 names for `lib/planning-driver-lib.sh`. Every case of the task prompt's `## Tests` section maps to a case here, except the last (*"With the switch off, the orchestrated path's existing tests pass unchanged"*), which is Task 6's.

**Depends on:**
- **Task 4**, which makes `init` write the three libraries under `<scriptsDir>/lib/`. So this suite drives the shipped copies, never the templates, by the rule `cli/test/helpers/walker.mjs` states for the walker.
- **Task 3's contract**, restated here so the suite does not guess. `pd_drive <branch> <worktree> <log_path>` is run in `<worktree>` with these globals:
  - `PD_PLUGIN_DIR`, `PD_MAIN_REPO`, `PD_FORMATTER`;
  - `PD_SESSION_EXEC`: the name of a function that runs `exec <agent cli> -p "$1" … "${@:2}"`;
  - `PD_NODE_STALL_SECS`.

  It returns 0 on hand-off, 3 on a clean stop (park, pause, STOP, cap, kill switch, escalation park) and 2 on a fault. Node streams land at `${log_path%.log}.planning/<seq>-<node>.stream.jsonl`.
- **Task 1's result rules**, restated: a session with no `init` event is `error`, so is an outcome its node does not declare, and so is a `FAIL`, or a round gate's `PASS`, with no `findings_file`. A session with no `result` event is `undelivered`.

### Targets

- `cli/test/helpers/planning-driver.mjs` (new): the shared fixture and stub.
- `cli/test/planning-driver-walk.test.mjs` (new): the walk, the sets and the held binding.
- `cli/test/planning-driver-control.test.mjs` (new): park, STOP, PAUSE, cap, retry and observations.

**Work:**

- [ ] **`helpers/planning-driver.mjs`.** Open it with the rule it enforces, as `helpers/walker.mjs` does. Its fixture:
  - Builds the repository with `cli/test/helpers/fixture.mjs`, with `phases.parity` `true` (so a round's set is three gates) and `phases.qa` `false`, and runs `init`. Its bare `origin` gives `push-branch.sh` a remote. It seeds the task prompt and a task-engine ledger whose `## Run mode` reads `skipped: none` and `phases: parity=true, qa=false, docs=false`, with `P0` `[x]`.
  - Copies, into a plugin directory under the system temp directory, this checkout's `plugin/.claude-plugin/plugin.json`, the six planning agents' files and `plugin/instructions/task_plan_writing_instructions_core.md`. A case may edit that copy.
  - Uses a stub agent CLI, an executable script, that reads `--agent`, `-p` and `--json-schema` from its argv. It appends `<agent> <start ms>` and `<agent> <end ms>` to a calls log, and sleeps a per-call time from a canned script keyed by agent and call index. A gate call plants the round file the prompt's `findings_folder:` and `iteration:` name, carrying `verdict: <PASS|FAIL>`; a `task-plan-writer` call writes the story index and one per-task file at the paths its prompt names. The stub then prints `stream-json` lines: an `init` event whose `tools` are the agent file's list, then a `result` event with `subtype: success`, `total_cost_usd` and `structured_output`. A script entry can instead say `no-init`, `no-result`, `undeclared` or `friction: <text>`, or touch a file such as `STOP` or `PAUSE` mid-call.
  - Exposes `drive(t, fixture)`. It runs `bash -c` through the fixture helper's runner, sourcing the shipped `lib/harness-run-lib.sh` and the three planning libraries and defining the stub `session_exec`, then calls `pd_drive`. It returns the exit status, the run log, the calls log, `git log --format=%s` and the clarification directory's files.
  - Never spreads `process.env` into a child without the fixture helper's isolation, and never aims at this checkout.
- [ ] **`planning-driver-walk.test.mjs`.** Open it with its rule. Cases:
  1. **A full walk.** A canned walk of writer `returned`, round 0 with `architecture_review` `FAIL`, writer revision, round 1 all `PASS` returns 0. `git log` carries, in order, `chore: Plan round 0 for feat_x`, `chore: Plan round 1 for feat_x`, `chore: Flow progress P1 for feat_x` and `chore: Flow progress P3 for feat_x`, and no `chore: Add task plan for feat_x`. Override 6 has already committed every path Override 4 stages, so its wrapper call exits 3, which is the common outcome that override names. The ledger reads `P1` and `P3` `[x]`. The revision writer's prompt opens `Revise the task plan per findings at` and names round 0's three files in `gates` order.
  2. **A set runs concurrently.** The three round-0 gates' recorded intervals overlap: the latest start is before the earliest end. With the stub finishing them in reverse `gates` order, the round closes once, with exactly one `chore: Plan round 0` commit.
  3. **One `error` in a set.** `architecture_review` returns `error` at once while the other two `PASS` after a delay. Neither sibling is killed: both end in the calls log and both round files exist. Exactly one `question_1.md` is written, carrying `held: architecture_review error`, and the return is 3.
  4. **An undeclared outcome.** A `plan_review` returning `SHIP` is held as `error` and parks like case 3.
  5. **A session with no `init` event** is held as `error`.
  6. **The core extraction.** With the copied core, the first prompt line of the writer's initial dispatch is `Write the task plan.`, and each gate's prompt carries `findings_folder: <stateDir>/<gate folder>/feat_x/`.
- [ ] **`planning-driver-control.test.mjs`.** Open it with its rule. Cases:
  1. **`<ask>`.** The writer returns `questions` with a `return` text. That writes `question_1.md` opening `Raised by: task-plan-writer (script-driven planning)` with the text, logs `PARKED: feat_x — 1 question(s) at`, and returns 3. After an `answer_1.md` is written, a second `pd_drive` continues the saved walk: the calls log shows no second fresh `start` writer prompt, and the resumed writer's prompt carries `=== BEGIN UNTRUSTED DATA` around the answer.
  2. **STOP.** A STOP present before a set launches no gate and returns 3. A STOP the stub creates while a set runs lets every session of the set finish, commits the round, and launches nothing after.
  3. **PAUSE.** A PAUSE the stub creates mid-set is honoured at the join: the round's commit lands, `PAUSE_ACK` and a `PAUSE_PROGRESS.md` entry exist, and the return is 3. With `PAUSE` and `PAUSE_ACK` removed, a second `pd_drive` dispatches the writer revision next and no gate again.
  4. **Undelivered three times.** One gate `no-result` three times running ends in a `chore: Plan round 0 partial for feat_x` commit and `PAUSE_ACK`. The next `pd_drive` dispatches only that gate.
  5. **The cap.** The plugin copy's core edited to `MAX_TOTAL_DISPATCHES = 3` halts before round 0's set. The calls log holds no gate, the run log carries `Halted: exceeded MAX_TOTAL_DISPATCHES (3).`, and the return is 3.
  6. **Observations.** After case 5's halt and after a hand-off, the fixture's `<stateDir>/improvement_observations/feat_x.md` carries a `# Script-driven planning — ` label, a `flow-efficiency` block naming every session, and the stub's `friction:` text under the node that reported it. `git log` carries `chore: Log improvement observations for feat_x`, and the file holds no fixture absolute path.

**Verification:**

- `cli/test/planning-driver-walk.test.mjs` and `cli/test/planning-driver-control.test.mjs` pass, each run on its own through the single-file test command.
- Every expected literal in the two suites is written in the suite, never read from the graph, the walker or the library under test: subjects, prompt first lines, `Raised by:` lines and halt messages.
