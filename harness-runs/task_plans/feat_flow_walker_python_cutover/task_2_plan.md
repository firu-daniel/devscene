### Task 2 — Point the walker-driving test helpers at the Python walker over the branch's own sources

**Goal:** Every `cli` suite that drives the `init`-shipped `flow-walker.sh` runs it against the Python walker, executing **this checkout's** `devscene-flow-host` and `graphscene` sources over the main-built environment. This is the task prompt's decision *"The suites test the branch's Python, not main's"*. The suite of the retired gate library goes.

How the branch's sources are reached, with no environment variable involved:
- `init` writes the shipped packages into every fixture's `<scriptsDir>/python/`, copied from `cli/dist/python/`, which the build stages from this checkout's `devscene-flow-host/` and `graphscene/` (`cli/src/flowHost/stage.ts`).
- Task 1's hand-off puts those shipped sources first on `PYTHONPATH`.
- The helper's only addition is the environment: a fixture's `<scriptsDir>/python/.venv` is a symbolic link to this checkout's provisioned one.

**Depends on:**
- **Task 1**, which fixes the hand-off's interface. This task restates the parts it consumes:
  - `flow-walker.sh` takes its environment, project and sources from its own directory only: `<scriptsDir>/python/.venv`, `<scriptsDir>/python/devscene-flow-host`, and `PYTHONPATH` = the two packages' `src/` directories there, replacing any inherited value. It reads no environment variable to choose any of them;
  - it refuses with exit `2` when `uv` is not on `PATH`, `<env>/pyvenv.cfg` is absent or `<env>/bin/devscene-flow-walker` is not executable;
  - it reads the graph from `<scriptsDir>/flows/task_plan_writing.v4.graph.json`;
  - the walk's state is the command's per-branch file `<stateDir>/.flow_walker_state/<percent-encoded branch>.json` (`devscene-flow-host/src/devscene_flow_host/host/store.py` → `walk_state_path`).
- **Task 4**, which exports `ENV_MARKER_FILE` (`'pyvenv.cfg'`) from `cli/src/flowHost/provision.ts`. `cli/src/flowHost/layout.ts` already exports `flowHostEnvDir(config)`.

**Where this task stops.** It changes the shared helpers and removes one retired suite:
- the suite cases whose **expectations** change (the other-branch refusal, the old-library refusal, the stale-lock cases, the fan-out cause regexes) are Task 7's;
- the new hand-off suite is Task 8's;
- `cli/test/remote-run.test.mjs` and `cli/test/outer-loop-scripts.test.mjs` are Task 17's, and that task consumes `linkWalkerEnv` from here.

### Targets

- `cli/test/helpers/walker.mjs` — the environment link, the graph path, the state path and the availability check.
- `cli/test/helpers/planning-driver.mjs` — the fixture takes a `mainRepo` option, and every repository it runs a walker from carries the environment link.
- `cli/test/helpers/watcher.mjs` — the stub `uv` hands `run` to the real `uv`, and the watcher fixture's main checkout carries the environment link.
- `cli/test/flow-walker-gates.test.mjs` — deleted with the library it tests.

**The interface this task defines, which Tasks 6, 7, 8 and 17 restate:**
- **`linkWalkerEnv(dir)`**, exported from `cli/test/helpers/walker.mjs`. It makes `<dir>/<flowHostEnvDir(dir's config)>` a symbolic link to `<WORKSPACE_ROOT>/<flowHostEnvDir(this checkout's config)>`. Both paths are built through `flowHostEnvDir`, imported from `../../dist/flowHost/layout.js`. Each config is the parsed `devscene.config.json`, read read-only; `flowHostEnvDir` reads only `scriptsDir`, through `outerLoopScriptsDir`. It creates the parent directory if `init` left none, and it replaces nothing that already exists there.
- **`walkerFixture`** calls `linkWalkerEnv` on every fixture it builds, after `init`.
- **`walk(dir, args)`** passes no walker-specific environment.
- **`walkerUnavailable()`** returns a reason, or `false`. Beside the existing `bash` and `jq` checks, it returns a reason when:
  - `uv` is not on `PATH`;
  - `<WORKSPACE_ROOT>/<flowHostEnvDir>/<ENV_MARKER_FILE>` is absent, with `ENV_MARKER_FILE` imported from `../../dist/flowHost/provision.js`;
  - `<that env>/bin/devscene-flow-walker` is not executable.

  The reason names `bash scripts/flow-host-provision.sh`, run outside the sandbox.
- **`WALKER_GRAPH_PATH`** is `${INIT_SCRIPTS_DIR}/flows/task_plan_writing.v4.graph.json`.
- **`walkerStatePath(dir, branch = 'feat_x')`** is `<dir>/<stateDir>/.flow_walker_state/<encoded branch>.json`. The encoding is the one `urllib.parse.quote(branch, safe="")` produces: unreserved `A-Za-z0-9_.-~` kept, every other byte as uppercase `%XX`.

No helper retypes `python`, `.venv`, `devscene-flow-host` or `pyvenv.cfg`: each comes from its owner's export.

**Work:**

- [ ] `walker.mjs`:
  - add `linkWalkerEnv` as above, and call it from `walkerFixture`;
  - repoint `WALKER_GRAPH_PATH` to the format-4 graph, and update its doc comment;
  - change `walkerStatePath` to the per-branch file, taking `branch` with the `'feat_x'` default every current caller relies on;
  - widen `walkerUnavailable()` as above.

  Rewrite the module header. The walker under test is still the copy `init` shipped (its rule stays). It now hands off to the Python command, which runs the shipped sources `init` copied from this build over a linked main-built environment, for the reason above.
- [ ] `planning-driver.mjs`. Let the fixture take a `mainRepo` directory, which the driver body passes as `PD_MAIN_REPO` in place of the literal `$W`. It defaults to the fixture's own directory, so every existing case is unchanged. Call `linkWalkerEnv` on the fixture's own directory unless it was built through `walkerFixture`. Add no walker variable to the fixture's `env`. Task 6 consumes the `mainRepo` option.
- [ ] `watcher.mjs`, following `<state_dir>/lessons.md` → *"When a check moves to reading a field one producer writes, the same change makes every path that stands in for that producer … write the field too"*.
  - Today the stub `uv` it writes (its choice 9) answers every call with `exit 0`, so a walker in a watcher run would print nothing. Make the stub `exec` the real `uv`, resolved on the host's `PATH` when the fixture is built, when its first argument is `run`. Keep `exit 0` for every other call, so `setup-worktree.sh` step 6 stays off the network.
  - Call `linkWalkerEnv` on the watcher fixture's main checkout after its `init`. After Task 6, the planning driver runs that checkout's walker.
  - Record both in the choice-9 comment.

  If the host has no `uv`, the stub keeps `exit 0` for `run` too, and the suites gated on `walkerUnavailable()` skip.
- [ ] Delete `cli/test/flow-walker-gates.test.mjs`. It sources `lib/flow-walker-gates.sh`, which Task 1 deletes. The rules it pinned are pinned on the Python side by `devscene-flow-host/tests/test_round_files.py`, `test_round_evidence.py` and `test_index_evidence.py`.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- `git grep -n -e 'flow-walker-gates' -e '\.graph\.json' -- cli/test/helpers` shows only the format-4 path in `walker.mjs`.
- `git grep -n -e "'\.venv'" -e 'pyvenv\.cfg' -e "'python'" -e 'DEVSCENE_FLOW_HOST_ENV' -e 'DEVSCENE_FLOW_HOST_PROJECT' -- cli/test/helpers` prints nothing.
- `git grep -ln -e 'walkerFixture' -e "flow-walker.sh" -- cli/test` lists only these:
  - files that reach the walker through `walk`, `run`, `runConcurrently` or the planning-driver fixture;
  - `cli/test/init.test.mjs` and `cli/test/outer-loop-scripts.test.mjs`, which name the file and do not run it;
  - `cli/test/remote-run.test.mjs`, which Task 17 points at `linkWalkerEnv`.
- With this checkout's `scripts/python/.venv` provisioned, run `npm run build`, then from the repository root `node --input-type=module -e "import('./cli/test/helpers/walker.mjs').then(async m => { const f = await m.walkerFixture({ parity: false, qa: false }); console.log(m.walkerUnavailable(), (await m.walk(f.dir, ['start', '--flow', 'task_plan_writing', '--branch', 'feat_x', '--skipped', 'none'])).status); await f.cleanup(); })"`. It prints `false 0`.
