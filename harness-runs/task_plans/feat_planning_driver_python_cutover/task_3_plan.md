### Task 3 — Retire the bash planning driver's three libraries from the shipped set

**Goal:** Delete `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh` from `cli/templates/scripts/`, and their rows from the shipped table. After Task 2 nothing sources them, as the task prompt decides: *"The bash driver (`lib/planning-*-lib.sh`) is retired"*. Also repoint every code comment that names them.

**Depends on:** Task 2, after which the watcher no longer sources the libraries.

**Where this task stops.**
- **The suites.** It deletes no suite that sources the libraries. That is **Task 4's**, and those suites fail between this task and Task 4.
- **The READMEs.** They are **Task 6's**.
- **The documents.** They are **Tasks 24–25's**.
- **Adopters.** It writes no cleanup of an adopter's already-shipped copies. `<state_dir>/lessons.md` → *"A rename declared breaking ships no compatibility path"*: an old copy left in an adopter's `<scripts_dir>/lib/` is sourced by nothing.

### Targets

- `cli/templates/scripts/lib/planning-node-lib.sh` (deleted)
- `cli/templates/scripts/lib/planning-record-lib.sh` (deleted)
- `cli/templates/scripts/lib/planning-driver-lib.sh` (deleted)
- `cli/src/generators/outerLoopScripts.ts` — the three `OUTER_LOOP_SCRIPTS` rows and every comment naming them
- `cli/templates/scripts/lib/unit-commit-lib.sh` — header lines naming `lib/planning-record-lib.sh` / `prl_artifact_commit`
- `cli/templates/scripts/run-analytics.sh` — the `NODE SESSIONS` header paragraph
- `cli/test/outer-loop-scripts.test.mjs` — the `PLANNING_LIBRARIES` case
- `cli/test/run-analytics-node-overlap.test.mjs` — its header's `pnl_reap` citation

**Work:**

- [ ] Delete the three templates. In `outerLoopScripts.ts`:
  - remove the three rows;
  - rewrite the comment above the `unit-commit-lib.sh` row (*"driver ahead of `planning-record-lib.sh`"*) to name that row's own readers;
  - rewrite the comment above the `task_plan_writing.graph.json` row so it names its two readers: `flow-walker.sh`'s `--flows`, and the planning driver `devscene-planning-driver`, which the watcher hands `--flows`.
- [ ] `unit-commit-lib.sh` header: the artifact table's second reader is now `devscene-flow-host`'s commit points. They call `commit-on-branch.sh --artifact <kind>`, so the table is read through the wrapper (`devscene-flow-host/src/devscene_flow_host/host/commit_points.py` → `commit_artifact`). Drop both lines that name `lib/planning-record-lib.sh`.
- [ ] `run-analytics.sh` → `NODE SESSIONS`: the manifest `${stream%.stream.jsonl}.planning/node-sessions.jsonl` is unchanged. One `{"session_id", "seq", "node"}` line per node session, `seq` a string, is now written by the planning driver, `devscene-planning-driver` in the shipped `devscene-flow-host` package, which the watcher launches (Task 2), not by `pnl_reap`. Change only the citation; the reading rules stay word for word. Name the command, not a module: the module path is the flow host's to choose, and its README names it (Task 23).
- [ ] `outer-loop-scripts.test.mjs`: replace the case *"the planning driver's three libraries land verbatim under scriptsDir/lib, and a re-run keeps them"* with one asserting that `init`, for a generated config's `scriptsDir` and for a relocated one, writes none of `lib/planning-node-lib.sh`, `lib/planning-record-lib.sh` and `lib/planning-driver-lib.sh`. Remove `PLANNING_LIBRARY_MODE` if nothing else reads it.
- [ ] `run-analytics-node-overlap.test.mjs`: the header's *"`pnl_reap` appends each node's stream"* names the planning driver, `devscene-planning-driver`, instead. That is the only edit.

**Verification:**

- `npm test --workspace cli -- test/outer-loop-scripts.test.mjs` passes, including the new not-shipped case.
- `npm test --workspace cli -- test/run-analytics-node-overlap.test.mjs` passes. Its header is the only line changed.
- `git grep -nE 'planning-(driver|node|record)-lib|pnl_reap|prl_artifact_commit' -- cli/src cli/templates` prints nothing.
- `commands.typecheck` exits zero over the edited `outerLoopScripts.ts`.
