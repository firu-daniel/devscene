### Task 7 — Move the `flow-walker*` cases that pinned the bash walker's behaviour

**Goal:** The `flow-walker*` suites pass against the Python walker. This task changes exactly the cases that `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **Chosen** names as pinning bash's behaviour, and leaves every case that README says holds unchanged as it is:
- `flow-walker-ui-and-reentry.test.mjs` (4) and (10);
- `flow-walker-resume.test.mjs` (1), (2) and (4);
- `flow-walker.test.mjs` (3);
- `flow-walker.test.mjs` (10) and `flow-walker-ui-and-reentry.test.mjs` (9), which assert only status and prefix;
- `flow-walker-fan-out.test.mjs` (3).

One case outside that README changes too, because the hand-off's own predicate differs from bash's: `flow-walker-ui-and-reentry.test.mjs` (12), the old-library refusal.

**Depends on:**
- **Task 1**, whose hand-off refuses an old library with exit `2`, an empty stdout, and stderr `flow-walker: <file> predates this walker`, before anything runs and with no state written. A library is old when it cannot be sourced, or once sourced defines no `hr_repo_root` or no `hr_state_dir`, or leaves any of its six `HR_FLOW_HOST_*` layout names unset or empty. A library that merely lacks `hr_phase_enabled` is **not** refused: the hand-off never calls it.
- **Task 2.** Its helper `cli/test/helpers/walker.mjs` provides three things, all of which the cases below rely on; this task edits no helper:
  - `walkerFixture` links every fixture's `<scriptsDir>/python/.venv` to this checkout's provisioned environment (`linkWalkerEnv`);
  - `WALKER_GRAPH_PATH` points at `${INIT_SCRIPTS_DIR}/flows/task_plan_writing.v4.graph.json`;
  - `walkerStatePath(dir, branch = 'feat_x')` is the per-branch file `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`.

**Where this task stops.** The hand-off's own behaviour (the unprovisioned refusal, `check-round-file` without `--flows`, and the leftover flat file) is Task 8's new suite. The bundle and remote round trip are Task 17's.

### Targets

- `cli/test/flow-walker-ui-and-reentry.test.mjs` — cases (11) and (12), and the suite header.
- `cli/test/flow-walker-concurrency.test.mjs` — cases (2), (3) and (4), and the suite header.
- `cli/test/flow-walker-fan-out.test.mjs` — cases (5) and (6).
- `cli/test/flow-walker-resume.test.mjs` — every use of the saved walk's path.

**Work:**

- [ ] `flow-walker-ui-and-reentry.test.mjs` (11):
  - retitle it to *"next for a branch with no walk of its own is refused, and the started branch's walk is unchanged"*;
  - assert exit `1`, an empty stdout, and stderr matching `^flow-walker: no walk in progress at .*feat_y\.json: run 'start' first$`;
  - assert the `feat_x` file's bytes are unchanged, through `walkerStatePath(dir)`.

  This is README **The walk's state.**: another branch's walk is never read and never refused, and only a mismatched flow is. Update the suite header's sentence on other-branch refusals.
- [ ] `flow-walker-ui-and-reentry.test.mjs` (12), the old-library refusal. Today it renames `hr_phase_enabled() {` to `hr_phase_enabled_absent() {` in the fixture's `lib/harness-run-lib.sh`. That function is not in Task 1's predicate, so the hand-off would launch the command and `start` would exit `0`.
  - Rename `hr_state_dir() {` to `hr_state_dir_absent() {` instead, a function the predicate checks.
  - Retitle the case to name `hr_state_dir`.
  - Keep its assertions: `status 2`, an empty stdout, stderr matching `/^flow-walker: .*harness-run-lib\.sh predates this walker/`, and no file at `walkerStatePath(dir)`.
  - Update its comment and the header sentence that names the bash walker's `hr_phase_enabled` check.
- [ ] `flow-walker-concurrency.test.mjs`. Remove (2) *"a lock older than a minute is broken"*, (3) *"a fresh lock held by another call is waited for, never broken"* and (4) *"two calls waiting on a stale lock"*. The command's `flock` locks die with their process, so there is no stale lock and no `rmdir` remedy (README **The locks.**). Lock waiting and timeouts are pinned by `devscene-flow-host/tests/test_flow_walker_concurrency.py`. Keep (1) unchanged. Rewrite the header, citing that file and naming the three removed behaviours as deliberately not covered here, with the reason.
- [ ] `flow-walker-fan-out.test.mjs`:
  - (5) matches `/the walk has finished/`, GraphScene's words;
  - (6) matches `/name the gate with node/`;
  - (3)'s `/not pending in round 0/` stays.

  Note in a comment beside `assertRefused` that these causes are GraphScene's wording (README **Refusal texts no caller parses.**).
- [ ] `flow-walker-resume.test.mjs`. Every place that deletes, reads or compares the saved walk goes through `walkerStatePath(dir, branch)` for the branch the case walks. A case that deleted the flat file to simulate a lost walk deletes the per-branch file; the records under `round_refusals/`, `revision_findings/` and `printed_reads/` stay unless the case's subject is losing them. Change no expected action.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run each of this task's four edited test files through `npm test --workspace cli -- test/<name>.test.mjs`: `flow-walker-ui-and-reentry`, `flow-walker-concurrency`, `flow-walker-fan-out` and `flow-walker-resume`. Each passes with its `# skip` count at 0 on a host where `walkerUnavailable()` is false, so a pass is not a skip.
- `git grep -n -e 'the walk finished' -e 'name the gate with --node' -e 'older than a minute' -e 'hr_phase_enabled_absent' -- cli/test` prints nothing.
