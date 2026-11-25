### Task 14 — Update the remote, sandbox and watcher documents for the walker's directory and shipped set

**Goal:** The three documents that describe the walker state the remote bundle carries, and the shipped walker files, say what Tasks 1 and 3 made true:
- the bundle carries **one branch's** walk files from `<state_dir>/.flow_walker_state/` as the directory `<bundle>/flow_walker_state/`;
- a pre-cutover bundle's flat file is not restored;
- the restore writes those files under the same link discipline;
- the walker ships with its format-4 graph and without a gate library.

**Depends on:**
- **Task 1.** The shipped set is `flow-walker.sh` (`0o755`), `flows/task_plan_writing.v4.graph.json` and `flows/task_plan_writing.graph.json` (each `0o644`). `lib/flow-walker-gates.sh` is gone, and the hand-off hands each call to `devscene-flow-walker`.
- **Task 3.** `<bundle>/flow_walker_state/` is a directory holding every regular file under `<state_dir>/.flow_walker_state/` whose base name is the branch's percent-encoded name plus `.json`, at its relative path, never a `.lock` and never another branch's. Its copy and restore go through `hr_remote_bundle_source_ok` and `hr_remote_copy_tree`'s link discipline. A bundle whose `flow_walker_state` is a regular file is not restored.

### Targets

- `docs/remote-execution.md` → **The walker state.**
- `docs/sandbox-record.md` → residuals 4 and 5, which name `.flow_walker_state` as one file that `restore` writes and `write` copies.
- `docs/watcher.md` → the shipped-script table rows `lib/flow-walker-gates.sh`, `flows/task_plan_writing.graph.json` and `flow-walker.sh`.

**Work:**

- [ ] `docs/remote-execution.md` **The walker state.**: rewrite to the directory form above. It is gitignored and never committed, and it loses its dot for `actions/upload-artifact`. Only the run's branch's files travel. A pre-cutover flat file in an older bundle is dropped, and the walk starts fresh through the orchestrator's `current` → exit 1 → `start`.
- [ ] `docs/sandbox-record.md` residuals 4 and 5: in each list of what `restore` writes and what `write` copies, replace `.flow_walker_state` with the branch's walk files under `.flow_walker_state/`. Keep each residual's finding as it stands, because the link discipline is unchanged.
- [ ] `docs/watcher.md`:
  - remove the `lib/flow-walker-gates.sh` row;
  - add a `flows/task_plan_writing.v4.graph.json` row: the planning loop's format-4 graph, read by `flow-walker.sh`'s hand-off as `--flows`, data, not agent-invocable;
  - reword the `flows/task_plan_writing.graph.json` row's reader to the planning driver's node list;
  - reword the `flow-walker.sh` row to say it hands each call to `devscene-flow-walker`.

  Keep each row's agent-invocable column as `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS` sets it.

**Verification:**

- `git grep -n -e 'flow-walker-gates' -e 'flow_walker_state`, without its dot' -- docs/remote-execution.md docs/sandbox-record.md docs/watcher.md` shows no claim that the state is one file.
- The rows of `docs/watcher.md`'s table match `OUTER_LOOP_SCRIPTS`'s walker rows one for one: `flow-walker.sh`, and the two `flows/` files.

**Deviations from plan:**
- Residual 4 (`docs/sandbox-record.md`): the plan said to keep the finding as it stands because the link discipline is unchanged. It changed for the walk files. On `29f6f57f^`, `hr_remote_bundle_restore` ran `cp` onto `.flow_walker_state` without any link test. Now each walk file goes through `hr_remote_link_free_var` on every component of its target path, leaf included. So residual 4 now names that test, and its finding is narrowed to "each other `mkdir -p` and `cp`".
- Residual 5 and **The walker state.**: the plan said the walker files go through `hr_remote_copy_tree`. `hr_remote_bundle_write` does not do that. It finds them with a `find` that does not follow links, gates each one with `hr_remote_bundle_source_ok` and copies only regular files. Both documents describe that mechanism and do not name `hr_remote_copy_tree` for it.
- `docs/watcher.md`: also rewrote the sentence in **Why only the `yes` rows carry a profile entry** that said "the walker's two: its gate library is sourced and its graph is read, both by `flow-walker.sh`". It now says "the two graphs, which are read and never run". The plan did not list this sentence, but leaving it would contradict the rows the plan changed.
- Verification: the plan's `git grep` pattern contains a backtick and a quote, so it is not a well-formed shell string. I ran it as `git grep -n -e 'flow-walker-gates' -e 'flow_walker_state`, without its dot' -e 'gate library'` and `git grep -n '\.flow_walker_state[^/]'` over the three documents. Neither found a match. I checked the rows against `OUTER_LOOP_SCRIPTS` by reading both. `bash scripts/typecheck.sh` printed `PASS: typecheck`.
