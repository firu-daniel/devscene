### Task 3 — Add `review-sweep.sh` to the outer-loop script table as agent-invocable

**Goal:** Make `devscene init` write `review-sweep.sh` into every adopter's `scriptsDir`, and grant the end-of-branch reviewer the one allow rule it needs to run it in an unattended run.

**Depends on:**
- **Task 2**, which adds `cli/templates/scripts/review-sweep.sh`. A row arrives with or after its template, never before it (`cli/src/generators/outerLoopScripts.ts` → the header's `## Scope this release`).
- **Task 1**, which already edited `cli/test/init.test.mjs` for the skeleton and reserved-target cases. This task's one edit to that file is the `OUTER_LOOP_SCRIPT_FILES` subtraction list, and it touches none of Task 1's cases.

**The one permission.** `agentInvocable: true` on this row is the single allow rule this branch adds. The permission-profile generator already renders every agent-invocable row into its repo-relative and repo-root-absolute pair (`cli/src/generators/permissionProfile.ts`, driven by `OUTER_LOOP_SCRIPTS`), so this task edits no profile code and no profile template. The row carries **no** `runsUnsandboxed`: the script only reads, and its main-checkout copy runs sandboxed. `branch-reviewer` (Task 8) is the dispatched agent that runs it.

### Targets

- `cli/src/generators/outerLoopScripts.ts` — the row and the header's inventory.
- `cli/templates/scripts/README.md` — the directory's inventory of the outer-loop family.
- `cli/test/outer-loop-scripts.test.mjs` — the `init`-driven case the new artifact lands with.
- `cli/test/init.test.mjs` — the `OUTER_LOOP_SCRIPT_FILES` subtraction list only.

**What accompanies the row.** The row makes `init` copy a new `create-if-absent` artifact into every adopter's `scriptsDir`, so it lands with an idempotence assertion, a `--force`-takes-a-`.bak` assertion beside it, and a case driving the compiled CLI against a throwaway fixture (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, rows *A generated or copied artifact* and *An outer-loop script*; `.claude/context/cli.md` → `## What "done" means here`). Task 2's `cli/test/review-sweep.test.mjs` copies the template by hand and never runs `init`, so it does not cover this.

**Work:**

- [ ] `OUTER_LOOP_SCRIPTS`: add `Object.freeze({ file: 'review-sweep.sh', mode: 0o755, agentInvocable: true })`, placed after every library row it sources (`lib/harness-run-lib.sh`), per the table's own ordering rule.
- [ ] Doc text:
  - `outerLoopScripts.ts`: name the review sweep in the module header's opening inventory, and in the `agentInvocable` doc comment add it to the list of scripts a dispatched agent runs, as the review sweep the end-of-branch reviewer runs from the main checkout;
  - `cli/templates/scripts/README.md`: name the review sweep in the paragraph opening "The other family in this directory is not generated."
- [ ] `cli/test/outer-loop-scripts.test.mjs`: add a case `'the review sweep lands verbatim under scriptsDir, a re-run keeps an edited copy, and --force leaves a .bak'`, modelled on `'the task-offer check lands verbatim under scriptsDir, and a re-run keeps an edited copy'`, with its own `REVIEW_SWEEP_SCRIPT = 'review-sweep.sh'` and `REVIEW_SWEEP_SCRIPT_MODE = 0o755` constants beside it. Through `initOk` on a `fixtureFor(t, { files: nodeProjectFiles() })` fixture, assert:
  - after the first `init`, `<SCRIPTS_DIR>/review-sweep.sh` equals the bytes of `cli/templates/scripts/review-sweep.sh` (`TEMPLATE_SCRIPTS`);
  - `copiesOf(snapshot, REVIEW_SWEEP_SCRIPT)` is exactly `[<SCRIPTS_DIR>/review-sweep.sh]`, so it is written only under `scriptsDir`;
  - its mode `& 0o777` is `0o755`;
  - after a hand-appended line and a second plain `init`, the edited bytes are unchanged;
  - after `initOk(dir, ['--force'])`, `<path>.bak` holds the edited bytes and `<path>` is the template's bytes again, as the `'--force regenerates an edited outer-loop script only after leaving its content in a .bak'` case asserts for the library.
- [ ] `cli/test/init.test.mjs` → `OUTER_LOOP_SCRIPT_FILES`: append `'review-sweep.sh'`, so `writtenWrappers` and `scriptPaths` subtract it and the wrapper-family assertions (`assert.deepEqual(await writtenWrappers(dir), [])`, `assert.deepEqual(scriptPaths(profile, 'allow'), [])`) never grade the new script or its two agent-invocable profile entries as a wrapper. Edit nothing else in the file; Task 1's cases are Task 1's.

**Verification:**

- `bash scripts/typecheck.sh` exits zero.
- `npm test --workspace cli -- test/outer-loop-scripts.test.mjs` passes. It is this task's own edited test file.
- `npm test --workspace cli -- test/init.test.mjs` passes. It is this task's own edited test file.
- `git grep -n -F "'review-sweep.sh'" -- cli/src` prints this one row. Any other `.sh` literal for it in `cli/src` is a second source of the table (`.claude/context/cli.md` → **One string, one producer.**).
- The generated profile's allow entries for this row come from the table alone: no line of `permissionProfile.ts` changed.
