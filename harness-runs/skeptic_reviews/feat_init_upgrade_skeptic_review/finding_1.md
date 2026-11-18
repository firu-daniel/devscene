### 1. A remote run's record blocks `init --upgrade`, although the task prompt limits the refusal to local runs

**File:** `cli/src/upgrade/preconditions.ts` (`readActiveRuns`) — "return pidNumber(pid) === undefined || pidIsAlive(pid);"

**Problem.** The task prompt's `## Writing files safely` says: "`--upgrade` refuses while the run registry shows an active **local** run." `readActiveRuns` does not separate local from remote records. It counts every `status: running` record whose `pid` holds no number, on the assumption that the pid is "not yet written".

A remote run's record always has that shape, and its pid is never written:

- `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_remote_record_init` writes `execution github-actions` and `pid ""`.
- `cli/templates/scripts/autonomous-watcher.sh` → `launch_remote_run` then writes `status running` once the dispatch returns 0.
- `docs/remote-execution.md` → `**Liveness.**`: "A remote record carries an empty `pid`, and the registry is its only liveness source".

**Runtime symptom, and why it is reachable.** On a repository with `execution.target: github-actions`, once a run is dispatched, `npx devscene init --upgrade` exits 1 with `refusing to upgrade: runs are active on <branch> (...); wait for them to finish or stop them`. The job runs in its own GitHub Actions checkout, so replacing the local scripts and profile cannot disturb it. The refusal lasts as long as the record says `running`. That status is refreshed only by a best-effort `remote-run.sh sync`, so a watcher that is not running leaves the upgrade blocked after the job has ended. `--dry-run` prints the same false "a real --upgrade run would refuse" note.

**Precedent.** The same question already has the right answer next door. `cli/templates/scripts/restart-watcher.sh` selects active runs with `(.value.execution != "github-actions")` and lists remote records as `remote (not affected by a restart)`. `docs/remote-execution.md` states that behaviour in the paragraph quoted above.

**Fix.**

1. In `cli/src/upgrade/preconditions.ts`, add `type HarnessExecutionTarget` to the existing `../config/model.js` import, and add beside `REFUSAL_PREFIX`:

   ```ts
   /** The `execution` value of a run record whose run executes in a remote job, not on this machine. */
   const REMOTE_EXECUTION: HarnessExecutionTarget = 'github-actions';
   ```

2. In `readActiveRuns`, make the filter:

   ```ts
   .filter(({ record }) => {
     if (record['status'] !== RUNNING_STATUS || record['execution'] === REMOTE_EXECUTION) return false;
     const pid = record['pid'];
     return pidNumber(pid) === undefined || pidIsAlive(pid);
   })
   ```

3. Add this sentence to the `readActiveRuns` doc comment: "A record whose `execution` is `github-actions` is not active here: its run executes in a remote job, has no local pid, and uses none of the files an upgrade replaces."

4. In `docs/cli.md` → `### Updating an adopted repository`, replace the bullet "the run registry records a `running` run whose pid is alive or not yet written, or cannot be read, because a replacement cannot then show that nothing is executing;" with "the run registry records a local `running` run whose pid is alive or not yet written, or cannot be read, because a replacement cannot then show that nothing is executing (a record with `execution: github-actions` runs in a remote job and does not count);".

5. In `cli/test/upgrade-preconditions.test.mjs`, beside the test `an active run refuses, naming only the active branch and the remedy`, add two tests using the file's `repository`, `registryFile` and `resolveIn` helpers:
   - A registry of `{ runs: { feat_remote: { status: 'running', execution: 'github-actions', pid: '' } } }`: `resolveIn(dir)` returns with `notes` equal to `[]`.
   - A registry of `{ runs: { feat_starting: { status: 'running', pid: '' } } }`: the call is refused through `assertRefused`, matching `/feat_starting/`, so a local run whose pid is not yet written still counts.
