### 4. The upgrade report's version-mismatch warning prints an unpinned command, unlike `doctor` and the documented route

**File:** `cli/src/upgrade/report.ts` (`upgradeReport`) — "`run ${UPGRADE_COMMAND} from the CLI matching the plugin.`"

When the installed plugin and the running CLI differ, the report says "run npx devscene init --upgrade from the CLI matching the plugin". The command it prints does not select that CLI: a bare `npx devscene` can resolve to the same mismatched version that just ran. The report already has the plugin's version in hand. `doctor`'s `plugin-cli-version` check prints the working form for the same condition through `pinnedCliCommand(pluginVersion)`, and `docs/cli.md` → `### Updating an adopted repository` documents `npx devscene@<version> init --upgrade`. The two surfaces give different remedies for one state.

**Fix:** have the command gather the pinned prefix and pass it in. `pinnedCliCommand` reads the package manifest from disk through `ownManifestString`, and the header of `cli/src/upgrade/report.ts` requires `upgradeReport` to read no file, so `report.ts` must not call it or import `githubWorkflows.js`.

In `cli/src/upgrade/report.ts`, add this field to `UpgradeReportInput`, after `pluginVersion`:

```ts
  /** The `pinnedCliCommand(pluginVersion)` value; `undefined` when `pluginVersion` is. */
  readonly pluginCliCommand: string | undefined;
```

Add `pluginCliCommand` to the `const { previousUnreadable, localFileIgnored, cliVersion, pluginVersion } = input;` destructuring, and replace the version check with:

```ts
  if (pluginVersion !== undefined && pluginCliCommand !== undefined && pluginVersion !== cliVersion) {
    warnings.push(
      `The installed plugin is version ${pluginVersion} and this CLI is version ${cliVersion}: ` +
        `run ${pluginCliCommand} init --upgrade, from the CLI of the plugin's version.`,
    );
  }
```

In `cli/src/upgrade/initUpgrade.ts`, add:

```ts
import { pinnedCliCommand } from '../generators/githubWorkflows.js';
```

Directly before the `upgradeReport` call, add:

```ts
  const pluginVersion = installedPluginVersion(repoRoot);
```

and replace the call's `pluginVersion: installedPluginVersion(repoRoot),` line with:

```ts
    pluginVersion,
    pluginCliCommand: pluginVersion === undefined ? undefined : pinnedCliCommand(pluginVersion),
```

In `cli/test/upgrade-report.test.mjs`:

1. In the `report` helper's defaults, after `pluginVersion: undefined,`, add `pluginCliCommand: undefined,`.
2. In the test `a differing plugin version names both versions, in either mode`, change the call to `report({ pluginVersion: '1.2.0', pluginCliCommand: 'npx devscene@1.2.0', dryRun })` and the expected line to:

   ```js
         "The installed plugin is version 1.2.0 and this CLI is version 1.2.3: run npx devscene@1.2.0 init --upgrade, from the CLI of the plugin's version.",
   ```

3. In the test `no version line when the versions match or the plugin version is unreadable`, change the matching-version call to `report({ pluginVersion: '1.2.3', pluginCliCommand: 'npx devscene@1.2.3' })`, so it still exercises the version comparison.
4. In the test `all of the wording is plain ASCII`, add `pluginCliCommand: 'npx devscene@9.9.9',` after `pluginVersion: '9.9.9',`, so the warning stays covered.

That test file is the only one this fix edits, so it is the only test the fix runs.
