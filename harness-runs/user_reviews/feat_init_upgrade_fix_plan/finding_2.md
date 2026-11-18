### 2. `init --upgrade --dry-run` has no mismatch note matching the new refusal

**File:** `cli/src/upgrade/preconditions.ts` (`runRegistryNotes`) — "return [`a real --upgrade run would refuse: ${refusal}`];"

**Also changes:** `cli/src/upgrade/initUpgrade.ts` (`runInitUpgrade`) — "pluginCliCommand: pluginVersion === undefined ? undefined : pinnedCliCommand(pluginVersion),"; `cli/test/init-upgrade.test.mjs`; `cli/test/plugin-cli-version.test.mjs`.

**Depends on Finding 1**, which adds `cli/src/machine/pluginCliVersion.ts` and `pluginVersionNotes({ mismatch, dryRun })` in `preconditions.ts`, and calls that function from `runInitUpgrade` before `new WritePlan()`. At that point the function returns `[]` under `dryRun`.

A dry run is the preview of a real run, so it must say that the real run would refuse on a mismatch and still list what would change. The run-registry refusals already behave this way through `runRegistryNotes`. Without this fix, a dry run falls through to `upgradeReport`'s old warning, which tells the adopter to pin the CLI to the plugin's version.

An unreadable plugin version already yields no mismatch from Finding 1's `pluginCliMismatch`, so the upgrade proceeds with nothing compared. This finding keeps that and adds a test for it in dry-run mode.

**Fix:**

- [ ] Give the run-registry note and the new note one prefix: a module constant in `preconditions.ts` holding `a real --upgrade run would refuse: `, used by `runRegistryNotes` with its output unchanged.
- [ ] In `pluginVersionNotes`, under `dryRun` with a mismatch, return one note: that prefix followed by `` `${pluginCliMismatchSummary(mismatch)}; ${pluginCliMismatchRemedy(mismatch)}` ``. The real-run refusal is unchanged.
- [ ] In `runInitUpgrade`, pass `pluginVersion: dryRun ? undefined : pluginVersion` to `upgradeReport`, and derive `pluginCliCommand` from that same value, so a dry run does not print the note and the old pinned warning together. Finding 3 revises this condition and Finding 5 replaces the two fields.
- [ ] In `cli/test/init-upgrade.test.mjs`, add a dry-run case with a recorded plugin of another version: exit `0`, the note on stdout, the usual `Dry run:` result and profile lines still printed, no `npx <package>@<plugin version>` text on either stream, and a byte-identical tree.
- [ ] Add a dry-run case with a recorded plugin root whose manifest is unreadable: exit `0` and no `a real --upgrade run would refuse` line.
- [ ] In `cli/test/plugin-cli-version.test.mjs`, add pure cases for `pluginVersionNotes` under `dryRun`, with and without a mismatch.
