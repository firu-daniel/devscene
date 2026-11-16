### 1. The placeholder manifest leaves out the plugin directory that every planning node session adds with `--add-dir`

**File:** `cli/templates/scripts/autonomous-watcher.sh` (`spawn_engine`, the block opening "What was absent before this session") — `for add_root in "$worktree" "$main_state" ${extra_dirs[@]+"${extra_dirs[@]}"}; do`. The test is in `cli/test/watcher-planning-driver.test.mjs` (the imports, the fixture's `pass` method and `pilotFixture`'s returned object, and a new test case).

**The problem.** On a bubblewrap host (`HR_PLACEHOLDER_HOST` is `1`), `spawn_engine` writes one placeholder manifest per spawn. The manifest lists every `denyWrite` path that was absent, and `.mcp.json` under each `--add-dir` root, so the placeholder sweep can later remove the 0-byte, read-only placeholder a killed session leaves behind. `docs/sandbox-record.md` → residual 12 measured Claude Code mounting `.mcp.json` placeholders in a session's `--add-dir` roots (`?? harness-runs/.mcp.json` in the main checkout's state directory). It also states the contract this code keeps: the manifest block *"records [`.mcp.json`] under every `--add-dir` root"*.

With the pilot on, every planning node session is launched through `session_exec` with one more `--add-dir`: `lib/planning-node-lib.sh` → `pnl_agent_flags` prints `--plugin-dir "$PNL_PLUGIN_DIR" --add-dir "$PNL_PLUGIN_DIR"`, and `PNL_PLUGIN_DIR` is `PLANNING_DRIVER_PLUGIN_DIR`. The manifest is still built from the engine session's roots only (`$worktree`, `$main_state` and the job-only `extra_dirs`), so `<PLANNING_DRIVER_PLUGIN_DIR>/.mcp.json` is never recorded. The driver kills node sessions by design (`pd_run_set`'s stall kill, `pd_kill_tree`). After a kill, a placeholder `.mcp.json` left at the plugin root is never swept. A plugin root's `.mcp.json` is a file Claude Code reads as that plugin's MCP configuration. So the leftover is not just clutter: it sits in the one directory every later node session, and any other session that loads this plugin, takes its plugin definition from. The `placeholder_manifest_writable_root` check has the same gap: it never tests whether the manifest lies under the plugin directory, which is a session-writable root.

**Fix.** `planning_driver` is set earlier in `spawn_engine` (`local planning_driver="" planning_clause=""`, before the manifest block), so the manifest block can read it. Add the plugin directory as one more root in both places when the pilot is on for this launch:

```bash
    for add_root in "$worktree" "$main_state" ${extra_dirs[@]+"${extra_dirs[@]}"} ${planning_driver:+"$PLANNING_DRIVER_PLUGIN_DIR"}; do
      mcp_paths+=("${add_root%/}/.mcp.json")
    done
```

and

```bash
    elif add_root="$(placeholder_manifest_writable_root "$manifest" "$worktree" "$main_state" ${extra_dirs[@]+"${extra_dirs[@]}"} ${planning_driver:+"$PLANNING_DRIVER_PLUGIN_DIR"})"; then
```

Then extend the comment above the block ("…and `.mcp.json` under each --add-dir root") with one clause: with the planning pilot on, the roots include the plugin directory the node sessions add.

**Test.** Add the case to `cli/test/watcher-planning-driver.test.mjs` in four edits.

1. **Imports.** Change `import { INIT_SCRIPTS_DIR, WORKSPACE_ROOT, runGit } from './helpers/fixture.mjs';` to `import { INIT_SCRIPTS_DIR, WORKSPACE_ROOT, runBash, runGit } from './helpers/fixture.mjs';`, and change `import { createWatcherFixture } from './helpers/watcher.mjs';` to `import { TICK_TIMEOUT_MS, createWatcherFixture } from './helpers/watcher.mjs';`.

2. **`pass` forwards the placeholder-host override.** The override is the second argument of the watcher fixture's `tick` (`cli/test/helpers/watcher.mjs` → `tick(env = {}, { …, placeholderHost = false, timeoutMs = TICK_TIMEOUT_MS } = {})`), which swaps in the probe that reports a bubblewrap host. `pass` today hands `tick` only `{ timeoutMs: PASS_TIMEOUT_MS }`. Change `async pass(plugin = null) {` to `async pass(plugin = null, { env = {}, placeholderHost = false } = {}) {`. Spread `...env` as the last entry of the environment object `pass` hands to `f.tick`, after `GITHUB_ACTIONS: ''`. Change the options argument from `{ timeoutMs: PASS_TIMEOUT_MS }` to `{ timeoutMs: PASS_TIMEOUT_MS, placeholderHost }`. Finding 3 prescribes this same signature; if it has already landed, leave `pass` as it is. Every existing call (`f.pass()`, `f.pass(f.plugin)`) keeps its behaviour.

3. **How the fixture finds the `.absent` manifest.** The manifest path is what `hr_run_profile_absent_file "$(hr_repo_slug <repo>)" <branch>` prints from `<scripts_dir>/lib/harness-run-lib.sh`; it is the run profile's settings path with `.json` replaced by `.absent`. Add this method to the object `pilotFixture` returns, beside `armPauseResume`. It is the `libPath` / `manifestFile` pair of `cli/test/watcher-placeholder-host.test.mjs`'s fixture, folded into one:

   ```js
       /** The `.absent` placeholder manifest the watcher wrote for `BRANCH`'s launch. */
       async manifestFile() {
         const printed = await runBash(
           f.dir,
           ['-c', '. "$1"; hr_run_profile_absent_file "$(hr_repo_slug "$2")" "$3"', '_', join(f.dir, INIT_SCRIPTS_DIR, 'lib', 'harness-run-lib.sh'), f.dir, BRANCH],
           f.watcherEnv(),
           { timeoutMs: TICK_TIMEOUT_MS, signal: t.signal },
         );
         assert.equal(printed.status, 0, printed.stderr);
         return printed.stdout.trim();
       },
   ```

4. **The case.** Add `test('on a placeholder host the pilot launch records the plugin directory .mcp.json in the manifest, and a launch with the switch empty records none', …)`. It opens like the suite's other cases (`const f = await pilotFixture(t); if (f === null) return;`), then runs `await f.armPauseResume()` and `await f.pass(f.plugin, { placeholderHost: true })` — every case in this suite arms the pause-resume pass first, so that the pass launches. It reads `readFileSync(await f.manifestFile(), 'utf8').split('\n')` and asserts that the lines include `` `${f.plugin}/.mcp.json` ``. In a second fixture (`const g = await pilotFixture(t); if (g === null) return;`) it runs `await g.armPauseResume()` and `await g.pass(null, { placeholderHost: true })`, and asserts that no line of `g`'s manifest starts with `` `${g.plugin}/` ``.

That test file is the one this fix edits, so it is the only test the fix runs: `npm test --workspace cli -- test/watcher-planning-driver.test.mjs`.

- **Deviations from plan:** The prescribed test, run as written, failed with no manifest: `pilotFixture` runs the pilot in place (worktree = `f.dir`), and the watcher fixture's default `XDG_STATE_HOME` is `f.dir/home/.local/state`, so the manifest path lies under the session-writable worktree and `placeholder_manifest_writable_root` refuses it (watcher log: `placeholder manifest: not writing … under the session-writable root <f.dir>`). Added `stateHome: join(root, 'state')` to `pilotFixture`'s returned object, gave `manifestFile` an `env` parameter forwarded to `f.watcherEnv(env)`, and the new case passes `{ XDG_STATE_HOME: <fixture>.stateHome }` to both `pass` (through the new `env` option) and `manifestFile`. Also added an `existsSync` assertion before each manifest read so a missing manifest reports `show(f)`. Mutation check: with the `${planning_driver:+…}` root removed from the `mcp_paths` loop the new case fails and the other five pass; restored, all six pass.
