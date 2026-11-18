### 3. The new refusal must not stop the harness repository's self-adopted upgrade

**File:** `cli/src/upgrade/preconditions.ts` (`resolveUpgradeTarget`) — "request.assertRepositoryAllowed(repoRoot);"

**Also changes:** `cli/src/upgrade/initUpgrade.ts` (`InitUpgradeOptions`, `runInitUpgrade`) — "readonly assertRepositoryAllowed: (repoRoot: string) => unknown;"; `cli/test/init-upgrade.test.mjs`; `cli/test/upgrade-preconditions.test.mjs`; `cli/test/plugin-cli-version.test.mjs`.

**Depends on Findings 1 and 2**, which add `pluginVersionNotes({ mismatch, dryRun })`, call it from `runInitUpgrade` before `new WritePlan()`, and stop passing the plugin version to `upgradeReport` under `--dry-run`.

In this repository `dev` changes between releases while the version number stays the same, and the installed plugin copy can lag the checkout. `docs/development.md` documents `HARNESS_SELF_ADOPT=1 node cli/dist/cli.js init --upgrade` as the way to regenerate this repository's adoption, so a refusal here would block that route. A mismatch there has to stay a warning.

`selfAdoptionOf` in `cli/src/commands/init.ts` already gives the right answer and is already passed as `assertRepositoryAllowed`. It returns `true` only past both harness-identity tests with the variable at exactly `1`, so the variable stays inert in every other repository. `resolveUpgradeTarget` currently discards that return value.

**Fix:**

- [ ] In `preconditions.ts`, add `selfAdopted: boolean` to `UpgradeTarget`, set from `request.assertRepositoryAllowed(repoRoot) === true`. Compare with `=== true` because the suite's stubs return `undefined` or a number. Type the callback as returning `boolean` in `UpgradeTargetRequest` and `InitUpgradeOptions`, and state in its doc comment that `true` means the deliberate self-adoption.
- [ ] Add `selfAdopted` to `pluginVersionNotes`' argument. When it is `true`, the function returns `[]` for real and dry runs alike.
- [ ] In `runInitUpgrade`, pass `target.selfAdopted`, and pass the plugin version to `upgradeReport` only when `target.selfAdopted` is true, replacing Finding 2's `dryRun` condition. A non-self-adopted real run with a mismatch has already refused, and its dry run has already printed the note, so the report warning now speaks only for self-adoption, in both modes.
- [ ] In `cli/test/init-upgrade.test.mjs`, extend the fixture pattern of the existing test that writes `.claude-plugin/marketplace.json` and a `cli/package.json` carrying this package's name. With a recorded plugin of another version and `HARNESS_SELF_ADOPT=1`, assert for a real run: exit `0`, both versions in a stderr warning, and a replaced edited script. Assert for a dry run: exit `0`, the warning, and no `a real --upgrade run would refuse` line for the version.
- [ ] Add a case proving the variable is inert elsewhere: an ordinary wired fixture with `HARNESS_SELF_ADOPT=1` and a mismatching plugin still exits `1` with a byte-identical tree.
- [ ] In `cli/test/upgrade-preconditions.test.mjs`, assert `selfAdopted` is `true` only for a callback returning `true`. In `cli/test/plugin-cli-version.test.mjs`, cover `pluginVersionNotes` with `selfAdopted: true`.
