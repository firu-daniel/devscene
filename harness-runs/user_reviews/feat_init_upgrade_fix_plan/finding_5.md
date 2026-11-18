### 5. `doctor` and the upgrade report tell the adopter to pin the CLI back

**File:** `cli/src/doctor/checks.ts` (`PLUGIN_CLI_VERSION_CHECK`) — "from the CLI of the plugin's version"

**Also changes:** `cli/src/upgrade/report.ts` (`upgradeReport`, `UpgradeReportInput`) — "from the CLI of the plugin's version."; `cli/src/upgrade/initUpgrade.ts` (`runInitUpgrade`) — "pluginCliCommand"; `cli/test/doctor-upgrade-drift.test.mjs`; `cli/test/upgrade-report.test.mjs`; `cli/test/init-upgrade.test.mjs`.

**Depends on Findings 1 and 3.** Finding 1 adds `cli/src/machine/pluginCliVersion.ts`, exporting `PluginCliMismatch`, `pluginCliMismatch(pluginVersion, cliVersion)`, `pluginCliMismatchSummary(mismatch)` and `pluginCliMismatchRemedy(mismatch)`. Finding 3 leaves `runInitUpgrade` handing the report the plugin version only when `target.selfAdopted` is true.

Both messages currently send the adopter to `npx devscene@<plugin version> init --upgrade`, which can pin the CLI back to an older plugin. They must follow the same rule as the refusal: update whichever half is older. The doctor check stays a warning and keeps its two pass cases.

**Fix:**

- [ ] In `PLUGIN_CLI_VERSION_CHECK`, compute `pluginCliMismatch(pluginVersion, cliVersion)`. Keep the unreadable-version and matching-version `pass` lines as they are. For a mismatch, return `` warn(`${pluginCliMismatchSummary(mismatch)}. ${sentenceCase(pluginCliMismatchRemedy(mismatch))}`) ``, or an equivalent that capitalizes only the first letter of the remedy sentence.
- [ ] Rewrite the check's doc comment: the remedy now updates whichever half is older, and the sentence saying it pins the plugin's version goes. Remove the `pinnedCliCommand` use here only. The import stays, because other checks in the file use it.
- [ ] In `cli/src/upgrade/report.ts`, replace `pluginVersion` and `pluginCliCommand` on `UpgradeReportInput` with `pluginMismatch: PluginCliMismatch | undefined`, documented as set only for a self-adopted run. Replace the old warning with one built from the summary and remedy, starting `The installed plugin is version …`. `cliVersion` remains only if something else in the function still reads it; remove the field if nothing does.
- [ ] In `runInitUpgrade`, pass `pluginMismatch: target.selfAdopted ? mismatch : undefined`, and remove the `pinnedCliCommand(pluginVersion)` argument. `cliCommand: pinnedCliCommand(cliVersion)` stays, because the watcher restart line needs it.
- [ ] In `cli/test/doctor-upgrade-drift.test.mjs`, update the "warns about a plugin of another version" case. With the older `OTHER_VERSION`, assert both versions, `claude plugin update devscene@devscene`, the restart text, `npx <package>@latest init --upgrade`, and no `@${OTHER_VERSION}`. Add a plugin newer than the CLI: the warning names the `@latest` upgrade and not the plugin update. Keep the matching-version pass.
- [ ] In `cli/test/upgrade-report.test.mjs`, update the `report` helper defaults and the three cases using `pluginVersion` and `pluginCliCommand`, including the plain-ASCII case. Assert the exact warning for a plugin-older and a CLI-older mismatch in both modes, and no warning when `pluginMismatch` is `undefined`.
- [ ] In `cli/test/init-upgrade.test.mjs`, tighten Finding 3's self-adopted case to assert the forward remedy and the absence of an `@<plugin version>` pin.
