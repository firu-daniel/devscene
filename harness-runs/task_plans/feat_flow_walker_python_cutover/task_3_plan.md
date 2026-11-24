### Task 3 — Declare the flow host's layout names once in the gate library, carry one branch's walk files in the remote bundle, and fail provisioning without `uv` or a project

**Goal:** Three changes to `cli/templates/scripts/lib/harness-run-lib.sh`, which is why they share a task:

1. **The layout names, declared once.** The literals `hr_flow_host_provision` keeps as locals become library-level names in `THE FLOW HOST'S ENVIRONMENT`, the one shell mirror `cli/src/flowHost/layout.ts`'s `MIRRORS.` header declares. Task 1's hand-off and `hr_flow_host_provision` both read them, so no second shell copy of the layout exists.
2. **The remote state bundle.** It stops copying `<state_dir>/.flow_walker_state` as one flat file and carries **one branch's** walk files from the directory the Python walker keeps there.
3. **`hr_flow_host_provision`.** With the walker now needed, it **fails** where it used to print `SKIPPED` and pass (no `uv`, or no project), so `setup-worktree.sh` step 6 fails the bootstrap. This is the task prompt's *"Decided (2026-11-24, after #478)"*.

**Depends on:** none. This task ships first.

**Where this task stops.** This task edits no test file:
- Task 16 brings the provisioning and bootstrap suites to the failing outcomes, and holds the new mirror names equal to their owners in `cli/test/flow-host-provision.test.mjs`.
- Task 17 brings the bundle suites to the directory form.

It does not edit `cli/src/flowHost/provision.ts`. Task 4 owns that module: it exports `ENV_MARKER_FILE`, which this task's `HR_FLOW_HOST_ENV_MARKER` mirrors, and removes `SKIPPED_MARKER` and its mirror note once this task's lines no longer carry the prefix.

### Targets

- `cli/templates/scripts/lib/harness-run-lib.sh`:
  - the `THE FLOW HOST'S ENVIRONMENT` header, the new layout names, and `hr_flow_host_provision`;
  - the file header's `MIRROR OF cli/src/flowHost/layout.ts` paragraph;
  - the `THE REMOTE STATE BUNDLE.` header, `hr_remote_names_var`, `hr_remote_bundle_write`, `hr_remote_bundle_restore`.
- `cli/src/flowHost/layout.ts` — the `MIRRORS.` header paragraph, and a new exported `FLOW_HOST_SOURCE_DIRNAME`.
- `cli/templates/scripts/setup-worktree.sh` — the header's step 6 paragraph.
- `cli/templates/scripts/flow-host-provision.sh` — its header's outcome list.

**The layout names, as this task defines them.** These are library-level assignments in `THE FLOW HOST'S ENVIRONMENT`, set when the library is sourced. Tasks 1 and 16 restate them.

| Name | Value | Mirrors |
|---|---|---|
| `HR_FLOW_HOST_DIRNAME` | `python` | `layout.ts` → `FLOW_HOST_DIRNAME` |
| `HR_FLOW_HOST_PROJECT` | `devscene-flow-host` | `layout.ts` → `FLOW_HOST_PROJECT` |
| `HR_FLOW_HOST_GRAPHSCENE` | `graphscene` | `layout.ts` → `FLOW_HOST_PACKAGES`, its entry other than `FLOW_HOST_PROJECT` |
| `HR_FLOW_HOST_ENV_DIRNAME` | `.venv` | `layout.ts` → `FLOW_HOST_ENV_DIRNAME` |
| `HR_FLOW_HOST_SOURCE_DIRNAME` | `src` | `layout.ts` → `FLOW_HOST_SOURCE_DIRNAME` (new, this task) |
| `HR_FLOW_HOST_ENV_MARKER` | `pyvenv.cfg` | `provision.ts` → `ENV_MARKER_FILE` (exported by Task 4) |

**The bundle's walker entry, as this task defines it.** `<bundle>/flow_walker_state/` is a **directory**, still without the dot, because `actions/upload-artifact` skips hidden files.
- **What it holds.** Every regular file under `<state_dir>/.flow_walker_state/`, at any depth, whose base name is exactly `<enc>.json`, at the same relative path.
- **`<enc>`** is the run's branch, percent-encoded as `devscene-flow-host/src/devscene_flow_host/host/store.py` → `walk_state_path` encodes it: `urllib.parse.quote(branch, safe="")`, with unreserved `A-Za-z0-9_.-~` kept and every other byte as uppercase `%XX`.
- That set is the branch's walk `<enc>.json` and its records under `round_refusals/`, `revision_findings/` and `printed_reads/`. The directory names are deliberately **not** spelled in bash, so a record the host adds later travels without an edit here.
- `.lock` files and every other branch's files are never carried (`<state_dir>/lessons.md` → *"A command scoped to one branch reads and writes that branch's state only"*).
- **Restore** places each carried file back at the same relative path under `<state_dir>/.flow_walker_state/`, under the existing `differs` withhold rule.
- **A bundle whose `flow_walker_state` is a regular file** — a pre-cutover bundle — is not restored. Its walk counts as lost, and the walk starts fresh through the orchestrator's `current` → exit 1 → `start` recovery, as the task prompt decides for a leftover flat file.

**Work:**

- [ ] Layout names in `harness-run-lib.sh`:
  - add the six assignments above to `THE FLOW HOST'S ENVIRONMENT`;
  - drop `hr_flow_host_provision`'s `flow_dir` / `flow_project` / `flow_env` locals and build its paths from the names;
  - rewrite the section's mirror table to the six rows above, naming `cli/test/flow-host-provision.test.mjs` as the test that holds them equal, and naming the two readers, `hr_flow_host_provision` and `flow-walker.sh`;
  - widen the file header's `MIRROR OF cli/src/flowHost/layout.ts` paragraph the same way, and add `provision.ts` → `ENV_MARKER_FILE`.
- [ ] `layout.ts`:
  - export `FLOW_HOST_SOURCE_DIRNAME = 'src'`, with a doc comment, and use it in `isShippedPythonFile` in place of the `'src'` literal;
  - rewrite the `MIRRORS.` paragraph: the shell mirror is the `HR_FLOW_HOST_*` names in `harness-run-lib.sh` → `THE FLOW HOST'S ENVIRONMENT`, read by `hr_flow_host_provision` and `flow-walker.sh`, and held equal by `cli/test/flow-host-provision.test.mjs`.
- [ ] Bundle write and restore:
  - **write:** copy the branch's files as above, through `hr_remote_bundle_source_ok` on each source and `hr_remote_copy_tree`'s link discipline, so no link is copied and no source under a link is read;
  - **restore:** make each target directory, and refuse a link on the way exactly as the existing restore paths do;
  - **encoding:** add one small function that prints a branch's encoded name, byte by byte under `LC_ALL=C`, and use it in both directions.

  Rewrite the header table row `<bundle>/flow_walker_state` and the `WHO READS EACH FILE` sentence for the walker state. Declare the encoding as a mirror of `host/store.py` → `walk_state_path`, held by `cli/test/remote-run.test.mjs`'s round trip (Task 17).
- [ ] `hr_flow_host_provision`:
  - no `uv` on `PATH` prints `flow-host: provision: failed — uv is not on PATH; install uv, then run bash <env_scripts_dir>/flow-host-provision.sh outside the sandbox` and returns `1`;
  - no `pyproject.toml` prints `flow-host: provision: failed — no flow host at <project>; run npx devscene init --upgrade` and returns `1`;
  - the synced, failed-sync and empty-argument outcomes are unchanged.

  Update the function's outcome table, and drop the header's `skip prefix … mirrored by … SKIPPED_MARKER` line.
- [ ] Headers: `setup-worktree.sh` → step 6, *"No `uv` on PATH, or no project there, prints one `SKIPPED` line and passes"*, and `flow-host-provision.sh`'s outcome list, both to the failing outcomes.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- `bash -c 'set -u; . cli/templates/scripts/lib/harness-run-lib.sh; printf "%s\n" "$HR_FLOW_HOST_DIRNAME" "$HR_FLOW_HOST_PROJECT" "$HR_FLOW_HOST_GRAPHSCENE" "$HR_FLOW_HOST_ENV_DIRNAME" "$HR_FLOW_HOST_SOURCE_DIRNAME" "$HR_FLOW_HOST_ENV_MARKER"'`, run from the repository root, prints the six values of the table, in its order.
- `git grep -n -e "flow_dir=" -e "flow_env=" -e "flow_project=" -- cli/templates/scripts` prints nothing.
- `git grep -n 'provision: SKIPPED' -- cli/templates` prints nothing.
- `git grep -n 'HR_REMOTE_WALKER' -- cli/templates/scripts` shows no `cp` of a single walker file.

**Deviations from plan:**
- `setup-worktree.sh` step 6's own locals `flow_src` / `flow_env` were renamed `flow_src_scripts` / `flow_env_scripts`, an edit beyond the header paragraph the Targets name: the `git grep -e "flow_env=" … -- cli/templates/scripts` check above matched `flow_env="$top"` there and could not print nothing otherwise. Behaviour is unchanged.
- Evidence downgrade: the second Verification bullet (`bash -c 'set -u; . cli/templates/scripts/lib/harness-run-lib.sh; printf …'`) was refused by the tool layer ("Permission to use Bash has been denied because Claude Code is running in don't ask mode"), and so was a `bash -n` parse of the library and a bash probe of `hr_walk_state_name`. The six values rest on reading the assignments in `THE FLOW HOST'S ENVIRONMENT`; the library's parse rests on `bash scripts/typecheck.sh`'s check-shell-parse step under `/bin/bash` 3.2.57, which passed. `hr_walk_state_name`'s equality with `store.py` → `walk_state_path` is unexecuted here and is held by Task 17's `cli/test/remote-run.test.mjs` round trip.
