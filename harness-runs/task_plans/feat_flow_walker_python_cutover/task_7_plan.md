### Task 7 — Move the `flow-walker*` cases that pinned the bash walker's behaviour

**Goal:** The `flow-walker*` suites pass against the Python walker. This task changes exactly the cases that `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **Chosen** names as pinning bash's behaviour, and leaves every case that README says holds unchanged as it is:
- `flow-walker-ui-and-reentry.test.mjs` (4) and (10);
- `flow-walker-resume.test.mjs` (1), (2) and (4);
- `flow-walker.test.mjs` (3);
- `flow-walker.test.mjs` (10) and `flow-walker-ui-and-reentry.test.mjs` (9), which assert only status and prefix;
- `flow-walker-fan-out.test.mjs` (3).

Two cases outside that list change too:
- `flow-walker-ui-and-reentry.test.mjs` (12), the old-library refusal, because the hand-off's own predicate differs from bash's;
- `flow-walker-concurrency.test.mjs` (1), whose concurrency assertions hold but whose closing "no lock left behind" check does not. That README says (1) holds unchanged, but it was written before Task 2 moved `walkerStatePath` onto the per-branch file, which puts the suite's lock path exactly on GraphScene's never-unlinked `.lock` file.

**Depends on:**
- **Task 1**, whose hand-off refuses an old library with exit `2`, an empty stdout, and stderr `flow-walker: <file> predates this walker`, before anything runs and with no state written. A library is old when it cannot be sourced, or once sourced defines no `hr_repo_root` or no `hr_state_dir`, or leaves any of its six `HR_FLOW_HOST_*` layout names unset or empty. A library that merely lacks `hr_phase_enabled` is **not** refused: the hand-off never calls it.
- **Task 2.** Its helper `cli/test/helpers/walker.mjs` provides three things, all of which the cases below rely on; this task edits no helper:
  - `walkerFixture` links every fixture's `<scriptsDir>/python/.venv` to this checkout's provisioned environment (`linkWalkerEnv`);
  - `WALKER_GRAPH_PATH` points at `${INIT_SCRIPTS_DIR}/flows/task_plan_writing.v4.graph.json`;
  - `walkerStatePath(dir, branch = 'feat_x')` is the per-branch file `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`.

**Where this task stops.** The hand-off's own behaviour (the unprovisioned refusal, `check-round-file` without `--flows`, and the leftover flat file) is Task 8's new suite. The bundle and remote round trip are Task 17's.

### Targets

- `cli/test/flow-walker-ui-and-reentry.test.mjs` — cases (11) and (12), and the suite header.
- `cli/test/flow-walker-concurrency.test.mjs` — cases (2), (3) and (4), case (1)'s closing lock assertion, the `lockPath` helper and its doc comment, the `mkdir` / `rmdir` / `utimes` import, and the suite header.
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
- [ ] `flow-walker-concurrency.test.mjs`. Remove (2) *"a lock older than a minute is broken"*, (3) *"a fresh lock held by another call is waited for, never broken"* and (4) *"two calls waiting on a stale lock"*. The command's `flock` locks die with their process, so there is no stale lock and no `rmdir` remedy (README **The locks.**). Lock waiting and timeouts are pinned by `devscene-flow-host/tests/test_flow_walker_concurrency.py`.
- [ ] `flow-walker-concurrency.test.mjs` case (1) — its concurrency assertions stay (every exit `0`, exactly one closer printing the round's result, the two `wait`s recording two distinct gates, `current` reprinting the closer's stdout); its closing lock assertion does **not**. After Task 2, `walkerStatePath(dir)` is `<stateDir>/.flow_walker_state/feat_x.json`, so `` `${walkerStatePath(dir)}.lock` `` is exactly the file GraphScene's `FileStateStore.lock` opens with `O_CREAT` and releases with `flock(LOCK_UN)` and `close`, never unlinking it (`graphscene/src/graphscene/adapters/state_file.py` → `FileStateStore.lock`, `self._lock_path = path.with_name(path.name + ".lock")`). Its existence after a walk is GraphScene's documented behaviour, so `existsSync(lockPath(dir)) === false` would fail every repetition.
  - Drop `assert.equal(existsSync(lockPath(dir)), false, 'a call left the lock directory behind')`.
  - Replace it with the property `flock` gives — no lock is **held** once the calls return: a further `walk(dir, ['current', '--flow', WALKER_FLOW, '--branch', BRANCH])` issued after `runConcurrently` resolves exits `0` with the closer's stdout. The `current` call (1) already makes serves as that check; state in a comment beside it that it is the no-lock-held check, since a held lock would block it until the command's lock timeout and fail it.
  - Remove the `lockPath` helper and its `# CONCURRENCY` doc comment, so no name in the suite stands for the bash walker's lock directory, and drop the imports only the removed cases and helper used (`mkdir`, `rmdir`, `utimes` from `node:fs/promises`, and `existsSync` and `delay` if no kept line uses them).
  - Rewrite the header: the rule becomes *every outcome of simultaneous `next` calls lands and exactly one call prints the round's result*, with no "no call leaves the lock behind" clause; cite `devscene-flow-host/tests/test_flow_walker_concurrency.py` for lock waiting and timeouts; name the three removed behaviours (stale-lock breaking, waiting on a fresh lock directory, two waiters on a stale lock) as deliberately not covered here, because `flock` dies with its process; state that a `.lock` file left beside the state file is GraphScene's documented behaviour and harmless; and drop the `cli/templates/scripts/flow-walker.sh` → `# CONCURRENCY` citation and the two `lock_take` mutation notes, which name the retired walker.
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
- `git grep -n -e 'lockPath' -e 'lock directory behind' -e 'lock_take' -- cli/test/flow-walker-concurrency.test.mjs` prints nothing.
