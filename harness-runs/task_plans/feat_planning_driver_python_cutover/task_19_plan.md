### Task 19 — Pin the driver's walk end to end against a fake agent CLI

**Goal:** Pin the walk behaviours that the retired `cli/test/planning-driver-walk.test.mjs` pinned against `pd_drive`, now against `devscene-planning-driver`. Each case runs the command's `main` end to end, over the shipped planning graph and planning core, with a fake agent CLI and a planted commit wrapper. The lead *"The `planning-*` and `watcher-planning-driver` suites pass against GraphScene"* is met here for the walk.

**Depends on:**
- **Task 18.** `commands/planning_driver.py` → `main(argv, stdout, stderr) -> int`, under the story index's command-line contract.
- **Task 16.** `tests/fake_planning_agent.py`, the scripted fake agent CLI. It writes a calls log of `agent`, `prompt`, `argv` and the environment, writes reviewers' findings files, and plays scripted failures: no `init`, `is_error`, a missing return block, a sleep.

**Where this task stops.** The parks, stops, retries and observations are **Task 20's**. The return-field pin is **Task 21's**.

### Targets

- `devscene-flow-host/tests/test_planning_driver_walk.py` (new)

**Work:**

- [ ] **The fixture and header.** Write the suite's header: *"The rule this file exists to enforce"*, the rule the retired suite stated, re-said against the Python driver. Build a shared fixture under `tmp_path`:
  - a git repository with a `devscene.config.json` (`stateDir` `devscene`), a task prompt and a ledger whose `P0` is closed;
  - a planted `commit-on-branch.sh` that logs each `--artifact` call;
  - a plugin directory carrying the real `.claude-plugin/plugin.json`, the six planning agents, their `schemas/*.return.json`, and the real `instructions/task_plan_writing_instructions_core.md`, all copied read-only from `plugin/`;
  - `--flows` pointing at `cli/templates/scripts/flows`.

  Every expected literal is written in the test, never read from the graph or the code under test.
- [ ] **A full walk.** Writer; round 0 with `architecture-reviewer` `FAIL`; the revision; round 1 all `PASS`; the hand-off. Assert:
  - the wrapper calls, in order: `plan-round` 0, `plan-round` 1, `ledger-flip` P1, …, `task-plan`, `ledger-flip` P3. There is no `task-plan` before the round that converged;
  - the ledger's `P1` and `P3` are `[x]`;
  - the revision prompt's first line is `Revise the task plan per findings at devscene/business_parity_reviews/feat_x/review_0.md, devscene/architecture_reviews/feat_x/review_0.md, devscene/task_plan_reviews/feat_x/review_0.md.`;
  - each gate is dispatched twice;
  - exit `0`, and stdout `consumed:\n`.
- [ ] **The round's gates run as one concurrent set that closes once.** Assert from the fake's calls log:
  - the three gates of round 0 all start before any of them ends;
  - the round commit lands once per round;
  - with a scripted sleep on one gate, the round still closes once, after its last gate.
- [ ] **A session whose return the driver cannot take is held as `error` while its siblings run to their end, then parks.** One case for each:
  - a return failing its schema on all three attempts;
  - a gate `PASS` whose schema-valid return omits `findings_file`;
  - no `init` event, three times.

  Each asserts a `held:` section for the gate in the park's `question_1.md`, the siblings' calls completing, and exit `3` with `stopped: park`. One more case: a gate `PASS` whose round file has no verdict line, three times, which parks the same way (Task 15's round-file rule, end to end).
- [ ] **A hand-off logs the `tasks_count` the writer's return object carries.** The log carries `[plan-drive] tasks_count: 3` for a scripted `tasks_count: 3`. Also: a session whose `init` event lacks a declared tool is not refused, and the log names it as withheld.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_driver_walk.py` passes.
- No case writes inside this checkout. Every path the suite writes sits under `tmp_path`, as `.claude/context/conventions.md` → `## The testing bar` requires.

**Deviations from plan:**

- The revision prompt's first line carries **absolute** paths, `<repo>/devscene/business_parity_reviews/feat_x/review_0.md, …`, rather than the plan's relative ones. `host/session_stream.py` → rule 10 resolves every `findings_file` against the session's working directory, so the relative form cannot reach the prompt. The test asserts the absolute literal built from the planted repository root.
- The wrapper calls are logged as the sibling suites log them (`plan-round --round 0`, `ledger-flip --entry P1`, `task-plan`, `ledger-flip --entry P3`). An `observations` call follows the `P3` flip, because the observation flush commits after the hand-off. The order is therefore asserted as a subsequence, and `P3` is not asserted as the last call.
- `tests/fake_planning_agent.py` cannot omit a declared `findings_file` or withhold a declared tool, and Task 16 owns that file. The suite's agent CLI, planted under `tmp_path`, hands the fake a second plugin copy, so the fake and the driver read different contracts: one has the `architecture-reviewer` `PASS` branch without `findings_file`, the other has the `task-plan-writer` `tools:` line without `Glob, Grep`. The no-verdict case scripts a relative `findings_file` that names a file planted in the repository with no verdict line. The fake's default `FAIL` has no `must_fix_count`, so it fails the schema; the full walk therefore scripts `{"outcome": "FAIL", "must_fix_count": 1}`.
- **Source change, `host/node_sessions.py`.** No host module narrated `SessionUsage.withheld_tools`, so "the log names it as withheld" had nothing to pin. A usage with withheld tools is now narrated as `WITHHELD_LINE`, using the retired `pnl_reap` text: `#<seq> <node> (<agent>): the init event lacks declared tools [<tools>] (a lacking tool is never refused)`.
- **Source change, `host/run_exits.py` → `_session_detail`.** `json.dumps` received the session's `return_document`, a `MappingProxyType`, and raised `TypeError`. Every held-gate park whose session had returned a document exited `2` with `internal error`. The fix renders `dict(document)`.
- Observed and left as it is: when `PlanningExecutor` rewrites a `Completed` into `Failed` (a refused round file), `NodeSessions` cannot pair the `Launch` and narrates `no usage record for <node> (total-run timeout)`. The narration is wrong, but `tests/test_node_sessions.py` → `test_a_mismatched_result_is_not_paired` pins the pairing rule, so changing it is a decision outside this task.
- Each held case takes about 122 s, because it waits through `host/run_control.py` → `BACKOFF_SECONDS` (60 s) twice. Whether a mocking aid may shorten that is `.claude/context/conventions.md` → `## Not determined`, so no case shortens it.
