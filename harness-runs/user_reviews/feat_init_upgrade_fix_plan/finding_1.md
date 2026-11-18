### 1. `init --upgrade` writes first and only warns about a version mismatch

**File:** `cli/src/upgrade/initUpgrade.ts` (`runInitUpgrade`) — "const pluginVersion = installedPluginVersion(repoRoot);"

**Also changes:** `cli/src/upgrade/preconditions.ts` (`REFUSAL_PREFIX`) — "const REFUSAL_PREFIX = 'refusing to upgrade';"; a new module `cli/src/machine/pluginCliVersion.ts`; a new suite `cli/test/plugin-cli-version.test.mjs`; `cli/test/init-upgrade.test.mjs`.

`runInitUpgrade` calls `plan.apply` and only afterwards reads `installedPluginVersion(repoRoot)`, so a mismatch reaches the adopter as a warning from `upgradeReport` after the scripts and the profile were replaced. The repository can then hold files from a CLI that does not match its plugin. The user has decided that the plugin and the CLI are released together and must match on a machine, so a readable mismatch has to stop the run before anything is planned or written.

No version comparison exists under `cli/src`, and the refusal has to know which half is older.

**Fix:**

- [ ] Create `cli/src/machine/pluginCliVersion.ts`, with a module header stating *"The rule this module exists to enforce"*: one comparison and one wording serve the refusal, the dry-run note, the upgrade report and `doctor`, the complete warning sentence has this one producer, and no remedy pins the CLI to an older plugin. It exports:
  - `PluginCliMismatch`: `{ pluginVersion: string; cliVersion: string; older: 'plugin' | 'cli' | 'unknown' }`.
  - `pluginCliMismatch(pluginVersion: string | undefined, cliVersion: string): PluginCliMismatch | undefined`. It returns `undefined` when `pluginVersion` is `undefined` or the two strings are identical. Otherwise it orders them by semantic-version precedence: numeric `major.minor.patch`, so `0.10.0` is newer than `0.9.0`; a prerelease sorts below its release; prerelease identifiers compare left to right, numeric ones numerically, numeric below alphanumeric, and a shorter list below a longer one with the same prefix. A version that does not parse, or two different strings of equal precedence such as `1.2.3+a` and `1.2.3+b`, gives `older: 'unknown'`.
  - `pluginCliMismatchSummary(mismatch)`: `the installed plugin is version <plugin> and this CLI is version <cli>`.
  - `pluginCliMismatchRemedy(mismatch)`. For `older: 'cli'`: ``run `npx devscene@latest init --upgrade` ``. For `'plugin'` and `'unknown'`: ``update the plugin with `claude plugin update devscene@devscene`, restart any open session, then run `npx devscene@latest init --upgrade` ``. The `'unknown'` case takes the longer route because both steps are correct whichever half is behind.
  - `pluginCliMismatchWarning(mismatch)`: the complete warning sentence used by `doctor` and the upgrade report, `The installed plugin is version <plugin> and this CLI is version <cli>. <the remedy with its first letter capitalized>.` Build it from the summary and the remedy. The capitalization is a private helper of this module and is not exported.
  - Build the commands from `PLUGIN_KEY` (`cli/src/generators/projectSettings.ts`) and `pinnedCliCommand('latest')` (`cli/src/generators/githubWorkflows.ts`), never from retyped package names.
- [ ] In `cli/src/upgrade/preconditions.ts`, add and export `pluginVersionNotes({ mismatch, dryRun }): readonly string[]`, a pure function. With no mismatch, or under `dryRun` for now, it returns `[]`. Otherwise it throws `HarnessError` with `` `${REFUSAL_PREFIX}: ${pluginCliMismatchSummary(mismatch)}; ${pluginCliMismatchRemedy(mismatch)}` ``. Findings 2 and 3 extend this function.
- [ ] In `runInitUpgrade`, immediately after `resolveUpgradeTarget` and before `new WritePlan()`, read `installedPluginVersion(repoRoot)` and `ownManifestString('version')`, compute the mismatch, and call `pluginVersionNotes`. Print its result with the existing notes, after `target.notes`.
- [ ] Keep this call out of `resolveUpgradeTarget`. `cli/test/upgrade-preconditions.test.mjs` calls that function in process with no scratch `CLAUDE_CONFIG_DIR`, so a read there would grade the host's real plugin.
- [ ] Add `cli/test/plugin-cli-version.test.mjs`, opening with the rule it enforces. Cover: unreadable and identical versions give no mismatch; plugin older; CLI older; `0.9.0` against `0.10.0`; a prerelease against its release; an unparsable version and equal-precedence build metadata give `'unknown'`; each remedy's exact text; the exact text of `pluginCliMismatchWarning` for each `older` value (`'plugin'`, `'cli'` and `'unknown'`); no remedy contains the older version as an `@` pin.
- [ ] In `cli/test/init-upgrade.test.mjs`, add a helper that records a plugin root under `repo.home` with a `.claude-plugin/plugin.json` of a chosen version. Add cases for a plugin older and a CLI older than this CLI. Each asserts exit `1`, the expected remedy on stderr, a byte-identical tree through `snapshotTree`, and no backup run. Add a case where the recorded root has no readable manifest: the upgrade succeeds.

A real run in this repository under `HARNESS_SELF_ADOPT=1` is refused on a mismatch until Finding 3 lands. The readiness order places Finding 3 in the same run.
