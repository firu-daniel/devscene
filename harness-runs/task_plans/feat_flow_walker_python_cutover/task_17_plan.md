### Task 17 — Bring the bundle and shipped-set suites to the walker's directory and the new shipped set

**Goal:** Every existing suite that seeds or asserts the remote bundle's walker entry moves to the directory form Task 3 defines, and the shipped-set test matches the set Task 1 leaves. The real-walker round trip runs against the Python walker over this checkout's sources.

**Depends on:**
- **Task 1**, which removes `lib/flow-walker-gates.sh` from the shipped set and adds `flows/task_plan_writing.v4.graph.json` (`0o644`) beside `flow-walker.sh` (`0o755`) and the format-3 `flows/task_plan_writing.graph.json` (`0o644`).
- **Task 2**, which exports these from `cli/test/helpers/walker.mjs`:
  - `linkWalkerEnv(dir)`, which links `<dir>/<scriptsDir>/python/.venv` to this checkout's provisioned environment through `flowHostEnvDir`. The hand-off then runs the shipped sources `init` copied from this build;
  - `walkerUnavailable()`;
  - `walkerStatePath(dir, branch)`.
- **Task 3**, which defines the bundle's walker entry:
  - **Shape.** `<bundle>/flow_walker_state/` is a **directory**. It holds every regular file under `<state_dir>/.flow_walker_state/`, at any depth, whose base name is exactly `<enc>.json`, at the same relative path.
  - **`<enc>`** is the branch as `urllib.parse.quote(branch, safe="")` encodes it.
  - **What never travels.** `.lock` files and every other branch's files.
  - **Copy discipline.** Every copy and restore goes through `hr_remote_bundle_source_ok` and `hr_remote_copy_tree`'s link discipline.
  - **Old bundles.** A bundle whose `flow_walker_state` is a regular file is not restored.

**Where this task stops.** It edits no script and no helper. `cli/test/check-machine-paths.test.mjs` is untouched: Task 12's widened filter still drops the flat `harness-runs/.flow_walker_state` hit and still prints `./nested/.flow_walker_state`, which that suite asserts.

### Targets

- `cli/test/outer-loop-scripts.test.mjs` — the bundle cases and `WALKER_FILES`.
- `cli/test/remote-run.test.mjs` — the walker-state round trip.
- `cli/test/remote-save-links.test.mjs` — `COPIED`, the honest-save case, (F)'s `.flow_walker_state` subtest, and the header's `RED ONCE` notes.

**Work:**

- [ ] `outer-loop-scripts.test.mjs`, the bundle cases:
  - bring them to the directory form: the `walker:` entry, the expected bundle listing and the planted `flow_walker_state` content;
  - plant `<branch>.json` and one record per subdirectory for the run's branch, plus one file for another branch that must not travel;
  - add a case that a regular-file `flow_walker_state` in a bundle is not restored.
- [ ] `outer-loop-scripts.test.mjs`:
  - set `WALKER_FILES` to `flow-walker.sh` (`0o755`), `flows/task_plan_writing.v4.graph.json` (`0o644`) and `flows/task_plan_writing.graph.json` (`0o644`);
  - retitle that test and its comment, which name the gate library.
- [ ] `remote-run.test.mjs`:
  - call `linkWalkerEnv` on each checkout that runs `flow-walker.sh`, and gate the real-walker cases on `walkerUnavailable()`;
  - make `WALKER` the per-branch directory, and the planted bundle content a directory;
  - run the round trip (start in one checkout, bundle, restore in another, `current` there) on a branch name carrying a `/`, so Task 3's encoding mirror is exercised end to end;
  - update the expected bundle listing.
- [ ] `remote-save-links.test.mjs`:
  - in `COPIED`, replace the flat `'.flow_walker_state': 'flow_walker_state'` source with `.flow_walker_state/feat_x.json` and one record `.flow_walker_state/revision_findings/feat_x.json`, each expected at `flow_walker_state/<same relative path>` in the bundle;
  - bring the honest-save case's expected file set and bytes to that;
  - retarget (F)'s `.flow_walker_state` linked-file subtest at the per-branch file `.flow_walker_state/feat_x.json`, a link there, and expect its skip line;
  - update the filter at the `['PAUSE_PROGRESS.md', '.flow_walker_state', …]` list and the header's `RED ONCE` notes that name `flow_walker_state`.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run each of this task's three edited test files through `npm test --workspace cli -- test/<name>.test.mjs`: `outer-loop-scripts`, `remote-run` and `remote-save-links`.
- `git grep -n -e "'\.flow_walker_state': " -e 'flow-walker-gates' -- cli/test` prints nothing.
