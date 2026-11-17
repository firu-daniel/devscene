### 2. The `OUTER_LOOP_SCRIPTS` comment names only one sourcer of `unit-commit-lib.sh`

**Site:** `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`, the comment above the `'unit-commit-lib.sh'` row: `// Sourced by \`commit-on-branch.sh\` from its own \`lib/\`, never run.`

**Problem.** The architecture-review fix on this branch (`45f6672f`) made `lib/planning-record-lib.sh` → `prl_artifact_commit` read `ucl_artifact`. The watcher now sources the library for the planning driver too: `cli/templates/scripts/autonomous-watcher.sh` → `PLANNING_DRIVER_LIBS="planning-node-lib unit-commit-lib planning-record-lib planning-driver-lib"`. The library's own header and `docs/watcher.md` both name the second sourcer, but the table comment still names only the wrapper. The `agentInvocable: false` argument it makes still holds, so no behaviour turns on it.

**Fix.** Replace the comment's first sentence so it reads:

```ts
  // Sourced by `commit-on-branch.sh` from its own `lib/`, and by the watcher for the planning
  // driver ahead of `planning-record-lib.sh`; never run. Run directly, it only defines
  // functions, so `false` is a calling convention and no `DENY_SCRIPT_BASENAMES` entry is owed.
```
