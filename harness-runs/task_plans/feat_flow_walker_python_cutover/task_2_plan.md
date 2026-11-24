### Task 2 — Point the walker-driving test helpers at the Python walker over the branch's own sources

**Goal:** Every `cli` suite that drives the `init`-shipped `flow-walker.sh` runs it against the Python walker, with **this checkout's** `devscene-flow-host` and `graphscene` sources first on `PYTHONPATH` over the main-built environment. This is the task prompt's decision *"The suites test the branch's Python, not main's"*. The suite of the retired gate library goes.

**Depends on:** Task 1, which fixes the hand-off's interface. This task restates the parts it consumes:
- `flow-walker.sh` takes its environment from `DEVSCENE_FLOW_HOST_ENV` and its project from `DEVSCENE_FLOW_HOST_PROJECT`, each used when set and non-empty;
- it refuses with exit `2` when `uv` is not on `PATH`, `<env>/pyvenv.cfg` is absent or `<env>/bin/devscene-flow-walker` is not executable;
- it reads the graph from `<scriptsDir>/flows/task_plan_writing.v4.graph.json`;
- the walk's state is the command's per-branch file `<stateDir>/.flow_walker_state/<percent-encoded branch>.json` (`devscene-flow-host/src/devscene_flow_host/host/store.py` → `walk_state_path`).

**Where this task stops.** It changes the shared helpers and removes one retired suite. The suite cases whose **expectations** change (the other-branch refusal, the stale-lock cases, the fan-out cause regexes) are Task 7's. The new hand-off suite is Task 8's. `cli/test/remote-run.test.mjs` and `cli/test/outer-loop-scripts.test.mjs` are Task 3's, and that task consumes `walkerEnv` from here.

### Targets

- `cli/test/helpers/walker.mjs` — the environment, the graph path, the state path and the availability check.
- `cli/test/helpers/planning-driver.mjs` — the driver fixture's environment carries `walkerEnv()`, and the fixture takes a `mainRepo` option.
- `cli/test/helpers/watcher.mjs` — the stub `uv` hands `run` to the real `uv`, and the watcher fixture's environment carries `walkerEnv()`.
- `cli/test/flow-walker-gates.test.mjs` — deleted with the library it tests.

**The interface this task defines, which Tasks 3, 7 and 8 restate:**
- `walkerEnv()` is exported from `cli/test/helpers/walker.mjs` and returns `{ DEVSCENE_FLOW_HOST_ENV, DEVSCENE_FLOW_HOST_PROJECT, PYTHONPATH }`:
  - the environment is `<WORKSPACE_ROOT>/<this checkout's scriptsDir>/python/.venv`, with `scriptsDir` read read-only from `<WORKSPACE_ROOT>/devscene.config.json`;
  - the project is `<WORKSPACE_ROOT>/devscene-flow-host`;
  - `PYTHONPATH` is `<WORKSPACE_ROOT>/devscene-flow-host/src` then `<WORKSPACE_ROOT>/graphscene/src`, joined with `path.delimiter`.
- `walk(dir, args)` passes `walkerEnv()` to `runBash`.
- `WALKER_GRAPH_PATH` is `${INIT_SCRIPTS_DIR}/flows/task_plan_writing.v4.graph.json`.
- `walkerStatePath(dir, branch = 'feat_x')` is `<dir>/<stateDir>/.flow_walker_state/<encodeURIComponent-equivalent of branch>.json`. The encoding is the one `urllib.parse.quote(branch, safe="")` produces: unreserved `A-Za-z0-9_.-~` kept, every other byte as uppercase `%XX`.

**Work:**

- [ ] `walker.mjs`:
  - add `walkerEnv()` as above, and have `walk` pass it;
  - repoint `WALKER_GRAPH_PATH` to the format-4 graph, and update its doc comment;
  - change `walkerStatePath` to the per-branch file, taking `branch` with the `'feat_x'` default every current caller relies on;
  - have `walkerUnavailable()` return a reason, in addition to the `bash` and `jq` checks, when `uv` is not on `PATH`, `<env>/pyvenv.cfg` is absent or `<env>/bin/devscene-flow-walker` is not executable. The reason names `bash scripts/flow-host-provision.sh`, run outside the sandbox.

  Rewrite the module header: the walker under test is still the copy `init` shipped (its rule stays), and it now hands off to the Python command run over this checkout's sources, for the reason above.
- [ ] `planning-driver.mjs`:
  - merge `walkerEnv()` into the fixture's `env` (the object at its `env: {` block), so the driver's own `bash "$PD_WALKER"` child inherits it, keeping every key the fixture already sets;
  - let the fixture take a `mainRepo` directory that the driver body passes as `PD_MAIN_REPO` in place of the literal `$W`, defaulting to the fixture's own directory, so every existing case is unchanged. Task 6 consumes this option.
- [ ] `watcher.mjs`, following `<state_dir>/lessons.md` → *"When a check moves to reading a field one producer writes, the same change makes every path that stands in for that producer … write the field too"*. Today the stub `uv` it writes (its choice 9) answers every call with `exit 0`, so a walker in a watcher run copy would print nothing. Make the stub `exec` the real `uv`, resolved on the host's `PATH` when the fixture is built, when its first argument is `run`; keep `exit 0` for every other call. Merge `walkerEnv()` into the environment the watcher fixture runs under, so the planning driver's walker inherits it. Record both in the choice-9 comment. If the host has no `uv`, the stub keeps `exit 0` for `run` too, and the suites gated on `walkerUnavailable()` skip.
- [ ] Delete `cli/test/flow-walker-gates.test.mjs`. It sources `lib/flow-walker-gates.sh`, which Task 1 deletes. The rules it pinned are pinned on the Python side by `devscene-flow-host/tests/test_round_files.py`, `test_round_evidence.py` and `test_index_evidence.py`.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- `git grep -n -e 'flow-walker-gates' -e '\.graph\.json' -- cli/test/helpers` shows only the format-4 path in `walker.mjs`.
- `git grep -ln -e 'walkerFixture' -e "flow-walker.sh" -- cli/test` lists only these: files that reach the walker through `walk`, `run`, `runConcurrently` or the planning-driver fixture; `cli/test/init.test.mjs` and `cli/test/outer-loop-scripts.test.mjs`, which name the file and do not run it; and `cli/test/remote-run.test.mjs`, which Task 3 points at `walkerEnv()`.
- With this checkout's `scripts/python/.venv` provisioned, `node --input-type=module -e "import('./cli/test/helpers/walker.mjs').then(m => console.log(m.walkerUnavailable(), m.walkerEnv()))"`, run from the repository root after `npm run build`, prints `false` and the three paths above.
