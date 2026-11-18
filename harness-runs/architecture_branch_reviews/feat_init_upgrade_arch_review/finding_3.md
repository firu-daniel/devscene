### 3. Resolve daemon-loaded script paths through the outer-loop table's owner

**Severity:** Must Fix

**Site:** `cli/src/upgrade/report.ts` → `daemonLoadedPaths`, quoted: `(script) => join(repoRoot, scriptsDir, ...outerLoopRelativePath(script).split('/')),`

**Problem.** The report module rebuilds where an outer-loop script lands by joining the parts by hand. Every other reader outside `outerLoopScripts.ts` that needs a script's absolute path calls `outerLoopScriptPath`: `cli/src/daemon/backend.ts`, `cli/src/commands/doctor.ts`, `cli/src/doctor/checks.ts`, `cli/src/generators/sandboxProfile.ts` and `cli/src/generators/writeProtection.ts`.

The same function also decides which table rows a running daemon has loaded, through a local `SOURCED_SUBDIR = 'lib'`. That is a fact about the shipped script set, held in a module whose header says it owns "the wording" of the report.

**Rule violated.**

- `.claude/context/conventions.md` → `### Where a new responsibility goes`: "A responsibility that already has a home does not get a second one."
- `.claude/context/cli.md` → `## How a module in this layer is written` → **One string, one producer**: the shipped tables "are single declarations of their sets and are read rather than copied".
- `cli/src/generators/outerLoopScripts.ts` → `outerLoopScriptPath` states the reason: readers resolve through it "rather than joining the three parts again, so no reader can look for a script somewhere the writer would not have put it".

**Fix.**

1. In `cli/src/generators/outerLoopScripts.ts`, export the answer from the table's owner:

   ```ts
   /** The scripts a running daemon has already loaded: the watcher and the libraries it sources. */
   export function daemonLoadedScriptPaths(repoRoot: string, config: HarnessConfig): ReadonlySet<string> {
     return new Set(
       OUTER_LOOP_SCRIPTS.filter(({ file, subdir }) => file === WATCHER_SCRIPT_NAME || subdir === 'lib').map((script) =>
         outerLoopScriptPath(repoRoot, config, outerLoopRelativePath(script)),
       ),
     );
   }
   ```

2. In `cli/src/upgrade/initUpgrade.ts`, pass `daemonLoadedPaths: daemonLoadedScriptPaths(repoRoot, config)` to `upgradeReport`, and stop passing `repoRoot`.
3. In `cli/src/upgrade/report.ts`:
   - Replace `UpgradeReportInput.repoRoot` with `readonly daemonLoadedPaths: ReadonlySet<string>`. Keep `scriptsDir`, which the restart command needs.
   - Delete the local `daemonLoadedPaths` function and `SOURCED_SUBDIR`.
   - Remove the `join`, `OUTER_LOOP_SCRIPTS`, `WATCHER_SCRIPT_NAME` and `outerLoopRelativePath` imports.
   - Test `input.daemonLoadedPaths.has(path)`. `upgradeReport` stays pure.
4. In `cli/test/upgrade-report.test.mjs`, pass the new input in place of `repoRoot`.
5. In `cli/test/outer-loop-upgrade.test.mjs`, add a case for `daemonLoadedScriptPaths`, including a nested `scriptsDir`.
