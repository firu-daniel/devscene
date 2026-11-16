### Task 2 — Ship the library with the outer-loop scripts and pin the planning driver's subjects against its artifact table

**Goal:** Make `init` write `lib/unit-commit-lib.sh` into every adopter's `scriptsDir` beside the wrapper that will source it. Then pin the planning driver's hardcoded fixed subjects and path sets against the library's artifact table, so the two cannot drift silently (the task prompt's **One subject, one source** constraint). The planning driver itself keeps its subjects and its plain wrapper calls.

**Depends on:** Task 1, which creates `cli/templates/scripts/lib/unit-commit-lib.sh`. Task 1 exports `ucl_artifact <kind> <state_dir> <branch> <round> <iteration> <entry>`, which sets `UCL_SUBJECT` and the array `UCL_PATHS`. Its kinds `task-plan`, `plan-round`, `ui-test-plan`, `ledger-flip` and `observations` are the ones the driver's callers mirror.

**Where this task stops.** It does not wire the library into `commit-on-branch.sh` (Task 3), and it does not change what `prl_commit` or any `prl_*` caller commits.

### Targets

- `cli/src/generators/outerLoopScripts.ts` — one `OUTER_LOOP_SCRIPTS` row.
- `cli/templates/scripts/README.md` — the not-generated family's library list.
- `cli/templates/scripts/lib/planning-record-lib.sh` — the header comment only.
- `cli/test/outer-loop-scripts.test.mjs` — the shipped-library assertion.
- `cli/test/planning-subjects-drift.test.mjs` (new).

**Work:**

- [ ] **The table row.** In `OUTER_LOOP_SCRIPTS`, add `Object.freeze({ file: 'unit-commit-lib.sh', subdir: 'lib', mode: 0o644, agentInvocable: false })`.
  - **Position.** Place it after `RUN_LIBRARY_SCRIPT_NAME`'s row and before `commit-on-branch.sh`'s row, under the table's own ordering rule: each library lands before the script that sources it.
  - **Comment.** Give it the same kind of comment the planning libraries carry: sourced by `commit-on-branch.sh`, never run, so `false` is a calling convention and no `DENY_SCRIPT_BASENAMES` entry is owed.
  - **Write protection.** None is owed: `cli/src/generators/writeProtection.ts` → `protectedPaths` already protects the whole `lib` directory.
- [ ] **`cli/templates/scripts/README.md`.** Name `lib/unit-commit-lib.sh` in the not-generated family beside the other libraries, as the library `commit-on-branch.sh` sources for its unit and artifact front end.
- [ ] **`planning-record-lib.sh` header.** The header's "The rule this library exists to enforce" paragraph says each write is the one the autonomous planning fork makes "by the same two wrapper calls". Rewrite that clause to say what is now true. The fork issues `commit-on-branch.sh --artifact <kind> --push` as one call; this library keeps the plain form and its own push, under the same fixed subjects and path sets. `cli/test/planning-subjects-drift.test.mjs` holds those equal to `lib/unit-commit-lib.sh`'s artifact table. Change no function body.
- [ ] **`cli/test/outer-loop-scripts.test.mjs`.** Add an assertion, in the shape of the `PLANNING_LIBRARIES` case, that `lib/unit-commit-lib.sh` lands verbatim at `<scriptsDir>/lib/unit-commit-lib.sh` with mode `644`, for both the generated and the relocated `scriptsDir`, and that a re-run keeps it. Do not fold it into `PLANNING_LIBRARIES`: its comment names the planning driver.
- [ ] **`cli/test/planning-subjects-drift.test.mjs`.**
  - **Header.** It opens with its rule: each fixed subject and path set the planning driver hardcodes equals the library's artifact-table row byte-for-byte.
  - **How it runs.** In a `bash` subprocess it sources `lib/harness-run-lib.sh`, `lib/planning-record-lib.sh` and `lib/unit-commit-lib.sh` from `cli/templates/scripts`. It sets `PRL_BRANCH`, `PRL_STATE_DIR`, `PRL_WORKTREE` and `PRL_MAIN_REPO` to throwaway values under `os.tmpdir()`, and **redefines `prl_commit`** to print its subject and paths NUL-separated and return 0.
  - **What it compares.** It calls each of these and compares its output with the matching `ucl_artifact` call:
    - `prl_round_commit 3` → `plan-round`, round `3`
    - `prl_convergence_commits yes` → `ui-test-plan`, then `task-plan`
    - `prl_ledger_flip P1` → `ledger-flip`, entry `P1`, against a ledger file holding `- [ ] P1.`
    - `prl_observe` plus `prl_observe_flush` → `observations`
  - **Partial rounds.** `prl_partial_commit`'s `chore: Plan round <n> partial for <branch>` is driver-only, with no orchestrator commit point. The header says so and exempts it by name.
  - **Registration.** It reads two fixed files, not a tree, so it is not a tree guard and owes no `treeGuards` entry.

**Verification:**

- `npm test --workspace cli -- test/planning-subjects-drift.test.mjs` and `npm test --workspace cli -- test/outer-loop-scripts.test.mjs`, each from the repository root as one plain foreground command, exit zero with `fail 0`.
- Run the drift suite once with one character of `chore: Add task plan for` changed in the working-tree copy of `planning-record-lib.sh`. Confirm it fails, then restore the file. `git diff -- cli/templates/scripts/lib/planning-record-lib.sh` must then show only the header-comment change.
- `bash scripts/typecheck.sh` passes for the `outerLoopScripts.ts` edit.
