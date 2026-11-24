### Task 3 — Carry one branch's walk files in the remote bundle, and fail provisioning without `uv` or a project

**Goal:** Two changes to `cli/templates/scripts/lib/harness-run-lib.sh`, which is why they share a task:

1. **The remote state bundle.** It stops copying `<state_dir>/.flow_walker_state` as one flat file and carries **one branch's** walk files from the directory the Python walker keeps there.
2. **`hr_flow_host_provision`.** With the walker now needed, it **fails** where it used to print `SKIPPED` and pass (no `uv`, or no project), so `setup-worktree.sh` step 6 fails the bootstrap. This is the task prompt's *"Decided (2026-11-24, after #478)"*.

**Depends on:** Task 1 and Task 2.
- **Task 1** removes `lib/flow-walker-gates.sh` from the shipped set and adds `flows/task_plan_writing.v4.graph.json`. This task brings `cli/test/outer-loop-scripts.test.mjs` → `WALKER_FILES` to that set.
- **Task 2** exports `walkerEnv()` from `cli/test/helpers/walker.mjs`, returning `{ DEVSCENE_FLOW_HOST_ENV, DEVSCENE_FLOW_HOST_PROJECT, PYTHONPATH }` for the hand-off. This task passes it to the real-walker calls in `cli/test/remote-run.test.mjs`.

**Where this task stops.** It does not edit `cli/src/flowHost/provision.ts` or `cli/test/init-provision-python.test.mjs`. Task 4 owns both, and that task removes `provision.ts` → `SKIPPED_MARKER` and its mirror note once this task's lines no longer carry the prefix.

### Targets

- `cli/templates/scripts/lib/harness-run-lib.sh`:
  - the `THE REMOTE STATE BUNDLE.` header, `hr_remote_names_var`, `hr_remote_bundle_write`, `hr_remote_bundle_restore`;
  - the `THE FLOW HOST'S ENVIRONMENT` header and `hr_flow_host_provision`.
- `cli/templates/scripts/setup-worktree.sh` — the header's step 6 paragraph.
- `cli/templates/scripts/flow-host-provision.sh` — its header's outcome list.
- `cli/test/outer-loop-scripts.test.mjs` — the bundle cases and `WALKER_FILES`.
- `cli/test/remote-run.test.mjs` — the walker-state round trip.
- `cli/test/flow-host-provision.test.mjs` — the two skip cases.

**The bundle's walker entry, as this task defines it.** `<bundle>/flow_walker_state/` is a **directory**, still without the dot, because `actions/upload-artifact` skips hidden files. It holds every regular file under `<state_dir>/.flow_walker_state/`, at any depth, whose base name is exactly `<enc>.json`, at the same relative path. `<enc>` is the run's branch, percent-encoded as `devscene-flow-host/src/devscene_flow_host/host/store.py` → `walk_state_path` encodes it: `urllib.parse.quote(branch, safe="")`, with unreserved `A-Za-z0-9_.-~` kept and every other byte as uppercase `%XX`.
- That set is the branch's walk `<enc>.json` and its records under `round_refusals/`, `revision_findings/` and `printed_reads/`. The directory names are deliberately **not** spelled in bash, so a record the host adds later travels without an edit here.
- `.lock` files and every other branch's files are never carried (`<state_dir>/lessons.md` → *"A command scoped to one branch reads and writes that branch's state only"*).
- **Restore** places each carried file back at the same relative path under `<state_dir>/.flow_walker_state/`, under the existing `differs` withhold rule.
- **A bundle whose `flow_walker_state` is a regular file** — a pre-cutover bundle — is not restored. Its walk counts as lost, and the walk starts fresh through the orchestrator's `current` → exit 1 → `start` recovery, as the task prompt decides for a leftover flat file.

**Work:**

- [ ] Bundle write and restore:
  - **write:** copy the branch's files as above, through `hr_remote_bundle_source_ok` on each source and `hr_remote_copy_tree`'s link discipline, so no link is copied and no source under a link is read;
  - **restore:** make each target directory, and refuse a link on the way exactly as the existing restore paths do;
  - **encoding:** add one small function that prints a branch's encoded name, byte by byte under `LC_ALL=C`, and use it in both directions.

  Rewrite the header table row `<bundle>/flow_walker_state` and the `WHO READS EACH FILE` sentence for the walker state. Declare the encoding as a mirror of `host/store.py` → `walk_state_path`, held by `cli/test/remote-run.test.mjs`'s round trip.
- [ ] `hr_flow_host_provision`:
  - no `uv` on `PATH` prints `flow-host: provision: failed — uv is not on PATH; install uv, then run bash <env_scripts_dir>/flow-host-provision.sh outside the sandbox` and returns `1`;
  - no `pyproject.toml` prints `flow-host: provision: failed — no flow host at <project>; run npx devscene init --upgrade` and returns `1`;
  - the synced, failed-sync and empty-argument outcomes are unchanged.

  Update the function's outcome table, and drop the header's `skip prefix … mirrored by … SKIPPED_MARKER` line. Update `setup-worktree.sh` → step 6, *"No `uv` on PATH, or no project there, prints one `SKIPPED` line and passes"*, and `flow-host-provision.sh`'s header to the failing outcomes.
- [ ] `outer-loop-scripts.test.mjs`:
  - bring the bundle cases to the directory form — the `walker:` entry, the expected bundle listing and the planted `flow_walker_state` content — with a fixture that plants `<branch>.json` and one record per subdirectory for the run's branch, plus one file for another branch that must not travel;
  - add a case that a regular-file `flow_walker_state` in a bundle is not restored;
  - set `WALKER_FILES` to `flow-walker.sh` (`0o755`), `flows/task_plan_writing.v4.graph.json` (`0o644`) and `flows/task_plan_writing.graph.json` (`0o644`), and retitle that test and its comment, which name the gate library.
- [ ] `remote-run.test.mjs`:
  - pass `walkerEnv()` to every `runBash` call of `flow-walker.sh`;
  - make `WALKER` the per-branch directory, and the planted bundle content a directory;
  - run the round trip (start in one checkout, bundle, restore in another, `current` there) on a branch name carrying a `/`, so the encoding mirror is exercised end to end;
  - update the expected bundle listing.
- [ ] `flow-host-provision.test.mjs`: the *"no flow host"* and *"no uv on PATH"* cases assert exit `1` and the `failed —` lines above, with `uv` never run. Restate the suite header's rule, *"a `SKIPPED` line and exit 0"*, to the new outcomes.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run this task's three edited test files, each through `npm test --workspace cli -- test/<name>.test.mjs`: `outer-loop-scripts`, `remote-run` and `flow-host-provision`.
- `git grep -n 'provision: SKIPPED' -- cli/templates` prints nothing.
- `git grep -n 'HR_REMOTE_WALKER' -- cli/templates/scripts` shows no `cp` of a single walker file.
