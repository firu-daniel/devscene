### Task 3 — Retire the `cli` suites that pinned the bash driver's internals

**Goal:** Delete the `cli` suites that source the bash libraries or pin their internals. Each case they pin is either a bash-internal detail or a behaviour that a named `devscene-flow-host` suite pins again against the Python driver. Each deleted suite's behaviours, and where they go, are listed below, so nothing is dropped silently (the story index's first `Top risks:` entry).

**Depends on:** Task 2, after which the watcher no longer sources the libraries. This task ships **ahead of** Task 4, which deletes the libraries: `devscene.config.json` → `treeGuards` maps `cli/templates/scripts/**` to `test/agent-return-schemas.test.mjs`, and that guard reads `cli/templates/scripts/lib/planning-driver-lib.sh` at module load (`const DRIVER = …`, `const driverText = read(DRIVER);`). This task removes that read, so Task 4's own guard run no longer touches the deleted file.

**Where this task stops.**
- **The libraries.** It deletes none of them. They still exist after this task, sourced by nothing. Deleting them, their shipped-table rows and the code comments naming them is **Task 4's**, including the header of `cli/test/run-analytics-node-overlap.test.mjs` and the `PLANNING_LIBRARIES` case of `cli/test/outer-loop-scripts.test.mjs`.
- **The replacements.** It writes no replacement suite. The replacements are **Task 19's** (the walk), **Task 20's** (parks, stops, retries, observations) and **Task 21's** (the return fields). Each `**Depends on:**` the driver tasks that come after this one. Between this task and those, the behaviours are unpinned. That gap is bounded by the branch, and Phase G runs after all of them.

### Targets

- `cli/test/planning-node-lib.test.mjs` (deleted)
- `cli/test/planning-record-lib.test.mjs` (deleted)
- `cli/test/planning-subjects-drift.test.mjs` (deleted)
- `cli/test/planning-driver-walk.test.mjs` (deleted)
- `cli/test/planning-driver-control.test.mjs` (deleted)
- `cli/test/helpers/planning-driver.mjs` (deleted)
- `cli/test/agent-return-schemas.test.mjs` — the `DRIVER` constant, `checkDriverCalls`, the two `pd_ret_field` cases and the header clause naming `pd_ret_field`

**Work:**

- [ ] Delete the six files. Before deleting, confirm with `git grep -n "helpers/planning-driver.mjs" -- cli/test` that nothing outside the five deleted suites imports the helper.
- [ ] `agent-return-schemas.test.mjs`:
  - remove `DRIVER`, `driverText`, `checkDriverCalls`, the case *"every pd_ret_field call in the driver names a declared field"* and the bad-sample case *"a pd_ret_field call naming an undeclared field is rejected"*;
  - remove the header's *"`pd_ret_field` call in the driver"* clause;
  - keep every other case unchanged.
  - The driver's field reads are pinned again by Task 21, against the Python driver's names.

**Where each retired behaviour goes.** This map is the record. It lives in this file, which the plan commit lands, and the implementer writes it nowhere else: the commit step builds the subject and the body. Two suites' behaviours go nowhere, for the reasons given here:
  - `planning-subjects-drift` held `prl_*`'s subjects to `ucl_artifact`. The Python driver commits through `commit-on-branch.sh --artifact <kind>`, so the wrapper's own table is the one source, and no drift is possible.
  - `planning-node-lib`'s `PNL_CORE_BLOCKS` agreement is already held by `devscene-flow-host/tests/test_core_agreement.py`, check 10 (the graph's `promptSource` against the core).
  - The session judgement and the per-agent flags are pinned by `devscene-flow-host`'s `test_session_stream.py`, and by Task 14's `test_agent_flags.py`.
  - The `planning-driver-walk` cases go to Task 19.
  - The `planning-driver-control` cases go to Task 20.

**Verification:**

- `npm test --workspace cli -- test/agent-return-schemas.test.mjs` passes, every remaining case included.
- `git grep -nE 'planning-driver\.mjs|pd_ret_field|pd_drive|pnl_|prl_' -- cli/test` prints no hit outside two headers this task does not own: `cli/test/run-analytics-node-overlap.test.mjs` (its `pnl_reap` citation, which Task 4 repoints) and `cli/test/watcher-planning-driver.test.mjs` (its comment naming the helper, which Task 5 rewrites).
