### 3. The planning driver's undelivered-dispatch self-pause sends a notification that does not name the error

**Files:**
- `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_undelivered`) — `PD_STRIKES=$((PD_STRIKES + 1))`. This is where the retry happens; the code here stays as it is.
- `cli/templates/scripts/autonomous-watcher.sh` (`planning_driver_run`, the `case "$pd_rc" in` arm `3)`) — `log "planning driver stopped '$branch' cleanly; classifying from its park, pause or ledger"`
- `cli/templates/scripts/autonomous-watcher.sh` (`classify_run_exit`, the non-job PAUSE_ACK arm) — `notify paused "$branch" "$log_path" "drop $state_rel/RESUME in $worktree to continue"`
- `cli/test/watcher-planning-driver.test.mjs` (the stub source `STUB_SOURCE`, the fixture's `pass` method, and a new test case)

**The problem.** `harness-runs/lessons.md` → `## Unattended control loops` has this rule: *"Every automatic retry in an unattended path is bounded by a count or a deadline. When the bound is reached, send exactly one notification naming the error and the manual way on, then stop retrying."* The diff adds a retry of that kind. When a set of planning node sessions is undelivered, `pd_undelivered` re-dispatches it: at once on the first strike, and after a backoff capped at 60s on the second. On the third consecutive undelivered set it commits the partial round, calls `prl_pause "planning (API overload)" …` and returns 3. A delivered set resets `PD_STRIKES` to 0 (`pd_main`, the `out` arm), and so does any other set result (the `*` arm). The **bound holds**.

The **notification does not meet the rule**. `prl_pause` only writes `PAUSE_PROGRESS.md` and `PAUSE_ACK`; it sends no notification. `planning_driver_run` maps the driver's 3 to 0. `classify_run_exit` then sees `PAUSE_ACK`. The pilot excludes job mode, so it always takes the local arm, which sends exactly one notification: `notify paused "$branch" "$log_path" "drop $state_rel/RESUME in $worktree to continue"`. `autonomous-notify.sh` renders that as *"Run '<branch>' is paused. Drop '<state_dir>/RESUME' in its working copy to continue. drop …/RESUME in … to continue"*. That gives the manual way on, but nothing in it names the error. An operator gets the same message for a pause they asked for, and nothing says that planning stopped because three consecutive dispatches went undelivered. The reason is only in `PAUSE_PROGRESS.md` and the run log, and the rule wants it in the notification. Job mode does name it (`"paused itself on API overload — …"`), but that path is never reached here.

**Fix.** Carry the driver's pause reason from `planning_driver_run` to `classify_run_exit` in a watcher global. Both run in the same launch subshell: `spawn_engine` calls them one after the other inside `( … ) &`. Only the local arm's detail changes, and only when the driver self-paused on undelivered dispatches.

1. In `planning_driver_run`, add one line as the first statement after the two `local` lines (before `clar="$state_abs/clarifications/$branch"`):

   ```bash
     PLANNING_DRIVER_PAUSE_DETAIL=""
   ```

2. In `planning_driver_run`'s `case "$pd_rc" in`, change the `3)` arm to:

   ```bash
       3)
         log "planning driver stopped '$branch' cleanly; classifying from its park, pause or ledger"
         if [ "${PD_STRIKES:-0}" -ge 3 ]; then
           PLANNING_DRIVER_PAUSE_DETAIL="paused itself on API overload: three consecutive planning dispatches undelivered — "
         fi
         return 0
         ;;
   ```

3. In `classify_run_exit`'s non-job PAUSE_ACK arm, replace the `notify paused` line with:

   ```bash
       notify paused "$branch" "$log_path" "${PLANNING_DRIVER_PAUSE_DETAIL:-}drop $state_rel/RESUME in $worktree to continue"
   ```

   Every other caller of `classify_run_exit` reaches it with the variable unset, and `${…:-}` expands that to nothing under `set -u`. Their notification stays byte-identical.

4. Add one sentence to the header comment above `planning_driver_run` (the one ending "…the pairs it left out stay for that session and classify_run_exit."): *"A 3 after three consecutive undelivered sets sets PLANNING_DRIVER_PAUSE_DETAIL, which classify_run_exit prefixes to its local `paused` notification so that the one notification names the error."*

5. Add the test to `cli/test/watcher-planning-driver.test.mjs`:
   - **The stub's undelivered session.** In `STUB_SOURCE`'s node branch (`if (qualified !== '') {`), move the three lines that read the agent's tools — `const text = readFileSync(join(flag('--plugin-dir'), 'agents', agent + '.md'), 'utf8');`, `const toolsLine = …` and `const tools = toolsLine.slice('tools:'.length)…` — up to sit directly after `record({ kind: 'node', agent });`, unchanged. Directly after them, add:

     ```js
       if (mode.undelivered === true) {
         process.stdout.write(JSON.stringify({ type: 'system', subtype: 'init', session_id: 'stub', tools }) + '\n');
         process.exit(0);
       }
     ```

     The init event must carry the agent's **real** `tools` list. `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ` tests the init tools first and reaps a mismatch as `error` ("the agent tools do not match its init event: …"); only when they match does it reach `elif ($res | type) != "object"` and reap the session as `undelivered` ("no result event"). An init with `tools: []` would be reaped as `error`, so `pd_undelivered` would never run. With the real list and no `result` event this is the same shape as the `no-result` mode of `cli/test/helpers/planning-driver.mjs`, which pushes the init event with the agent's tools and leaves out only the `result`. Exiting before the decision block also means the undelivered session writes no plan or review file. The `events` array further down still uses `tools`, so it needs no change.
   - **The `pass` method.** Change `async pass(plugin = null) {` to `async pass(plugin = null, { env = {}, placeholderHost = false } = {}) {`. Spread `...env` as the last entry of the environment object `pass` hands to `f.tick`, after `GITHUB_ACTIONS: ''`. Change the options argument from `{ timeoutMs: PASS_TIMEOUT_MS }` to `{ timeoutMs: PASS_TIMEOUT_MS, placeholderHost }`. Finding 1 prescribes this same signature; if it has already landed, leave `pass` as it is. Every existing call (`f.pass()`, `f.pass(f.plugin)`) keeps its behaviour.
   - **The case.** Add `test('switch set, and every node dispatch is undelivered: the run pauses and its one paused notification names the overload', …)`. It opens like the suite's other cases (`const f = await pilotFixture(t); if (f === null) return;`), then does `await f.setMode({ undelivered: true })`, `await f.armPauseResume()` and `await f.pass(f.plugin, { env: { PD_BACKOFF_SECS: '0' } })`. It asserts that `f.record().status` is `'paused'`, that `f.notifications().filter((n) => n.event === 'paused' && n.branch === BRANCH)` has length 1, and that the one entry's `detail` includes `'three consecutive planning dispatches undelivered'`. It also asserts that no entry of `f.calls()` has `kind === 'engine'`.

   That test file is the one this fix edits, so it is the only test the fix runs: `npm test --workspace cli -- test/watcher-planning-driver.test.mjs`.
