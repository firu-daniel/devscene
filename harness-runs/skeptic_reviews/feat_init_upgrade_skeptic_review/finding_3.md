### 3. The restart command the upgrade report prints fails on a repository adopted through `npx`

**File:** `cli/src/upgrade/report.ts` (`upgradeReport`) — "const restart = scriptInvocation(scriptsDir, RESTART_WATCHER_SCRIPT_NAME);"

**Problem.** When the watcher or a library changes, the report says `A running daemon keeps the code it already loaded: restart it with bash scripts/restart-watcher.sh`. `docs/cli.md` → `### Updating an adopted repository` prints the same bare command in a fenced block.

`cli/templates/scripts/restart-watcher.sh` resolves its CLI with `cli="${DEVSCENE_CLI:-devscene}"`, and stops when that first word is not on `PATH`:

```text
restart-watcher.sh: 'devscene' is not on PATH — nothing was restarted
```

The documented adoption and upgrade route is `npx devscene`, which installs no `devscene` binary on `PATH`. The architecture review's Finding 4 relied on the same fact for the report's own commands.

**Runtime symptom, and why it is reachable.** An adopter who follows the documented route, upgrades a changed watcher and pastes the printed line gets exit 1. The daemon keeps running the old code until they work out the variable from the error text. The repository already documents the working form: `docs/development.md` and `docs/outer-loop-verification.md` both give `DEVSCENE_CLI="npx devscene@<version>" bash <scriptsDir>/restart-watcher.sh`.

**Fix.** Print that form, pinned to the CLI that performed the upgrade.

1. In `cli/src/upgrade/report.ts`:
   - Add to `UpgradeReportInput`:

     ```ts
     /** The `pinnedCliCommand(cliVersion)` value: what the restart script runs the daemon verbs through. */
     readonly cliCommand: string;
     ```

   - Read `cliCommand` from `input` in `upgradeReport`, and change the restart line to:

     ```ts
     const restart = `DEVSCENE_CLI="${cliCommand}" ${scriptInvocation(scriptsDir, RESTART_WATCHER_SCRIPT_NAME)}`;
     ```

2. In `cli/src/upgrade/initUpgrade.ts` → `runInitUpgrade`, add `const cliVersion = ownManifestString('version');` before the `upgradeReport` call, pass `cliVersion` as the `cliVersion` field, and add `cliCommand: pinnedCliCommand(cliVersion)`.

3. In `docs/cli.md` → `### Updating an adopted repository`, change the fenced `bash <scriptsDir>/restart-watcher.sh` to:

   ```bash
   DEVSCENE_CLI="npx devscene@<version>" bash <scriptsDir>/restart-watcher.sh
   ```

4. Update both test files that pin the restart line:
   - In `cli/test/upgrade-report.test.mjs`:
     - Add `cliCommand: 'npx devscene@1.2.3'` to the `report` helper's input.
     - Change the two expected restart lines to end in `DEVSCENE_CLI="npx devscene@1.2.3" bash scripts/restart-watcher.sh`.
     - The test `the restart line follows scriptsDir, including the repository root` keeps its `endsWith(' bash restart-watcher.sh')` assertion unchanged.
   - In `cli/test/init-upgrade.test.mjs` → the test `the restart line appears when the watcher changes, and not otherwise`:
     - After `const restart = scriptInvocation(repo.scriptsDir, RESTART_WATCHER_SCRIPT_NAME);`, add:

       ```js
       const { name, version } = readJson(join(PACKAGE_ROOT, 'package.json'));
       const pinned = `DEVSCENE_CLI="npx ${name}@${version}" ${restart}`;
       ```

     - Change the two assertions to `restart the daemon afterwards with ${pinned}` and `restart it with ${pinned}`.
     - Keep the `!quiet.stderr.includes(restart)` assertion unchanged. `readJson`, `join` and `PACKAGE_ROOT` are already imported in this file.
