### Task 3 — Add `review-sweep.sh` to the outer-loop script table as agent-invocable

**Goal:** Make `devscene init` write `review-sweep.sh` into every adopter's `scriptsDir`, and grant the end-of-branch reviewer the one allow rule it needs to run it in an unattended run.

**Depends on:** Task 2, which adds `cli/templates/scripts/review-sweep.sh`. A row arrives with or after its template, never before it (`cli/src/generators/outerLoopScripts.ts` → the header's `## Scope this release`).

**The one permission.** `agentInvocable: true` on this row is the single allow rule this branch adds. The permission-profile generator already renders every agent-invocable row into its repo-relative and repo-root-absolute pair (`cli/src/generators/permissionProfile.ts`, driven by `OUTER_LOOP_SCRIPTS`), so this task edits no profile code and no profile template. The row carries **no** `runsUnsandboxed`: the script only reads, and its main-checkout copy runs sandboxed. `branch-reviewer` (Task 8) is the dispatched agent that runs it.

### Targets

- `cli/src/generators/outerLoopScripts.ts` — the row and the header's inventory.
- `cli/templates/scripts/README.md` — the directory's inventory of the outer-loop family.

**Work:**

- [ ] `OUTER_LOOP_SCRIPTS`: add `Object.freeze({ file: 'review-sweep.sh', mode: 0o755, agentInvocable: true })`, placed after every library row it sources (`lib/harness-run-lib.sh`), per the table's own ordering rule.
- [ ] `outerLoopScripts.ts` doc text:
  - name the review sweep in the module header's opening inventory;
  - in the `agentInvocable` doc comment, add it to the list of scripts a dispatched agent runs, as the review sweep the end-of-branch reviewer runs from the main checkout.
- [ ] `cli/templates/scripts/README.md`: name the review sweep in the paragraph opening "The other family in this directory is not generated."

**Verification:**

- `bash scripts/typecheck.sh` exits zero.
- `git grep -n -F "'review-sweep.sh'" -- cli/src` prints this one row. Any other `.sh` literal for it in `cli/src` is a second source of the table (`.claude/context/cli.md` → **One string, one producer.**).
- The generated profile's allow entries for this row come from the table alone: no line of `permissionProfile.ts` changed.
