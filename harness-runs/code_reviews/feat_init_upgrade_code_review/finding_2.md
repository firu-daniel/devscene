### 2. An upgrade without `--reference-toolchain-path` removes a parity repository's toolchain grants, and the toolchain warning's command does not restore them

**File:** `cli/src/generators/permissionProfile.ts` (`appendToolchainAllowances`) — "Re-run init with ${TOOLCHAIN_FLAG} <absolute path> to add one entry per parity.toolchainCommands value"

The reference-toolchain `allow` entries exist only when the run is given `--reference-toolchain-path`. The upgrade render replaces the profile, and the carry-forward does not preserve these entries: `Bash(<dir>/<command>:*)` is neither of the shapes `pluginRootEntryTarget` recognises. So on a repository with `phases.parity` on, every `init --upgrade` without the flag removes them. `doctor`'s `profile-drift` remedy names that bare command too.

The run does warn, but the warning says "Re-run init with --reference-toolchain-path <absolute path>". An adopter who does that literally runs a plain `init`. The profile already exists, so `writePermissionProfile` enqueues it under `create-if-absent`, the write engine keeps it, and no entry is added. The grants stay missing, and under `dontAsk` the unattended parity run's toolchain calls are refused.

The operator is not left with nothing. The `--upgrade` row of `docs/cli.md` § 2 and the flag's summary in `cli/src/commands/init.ts` both say `--upgrade` accepts `--reference-toolchain-path`, and `removedEntriesWarning` in `cli/src/upgrade/report.ts` lists each removed entry and sends it to the local additions file. The defect is narrower: the toolchain warning names a command that does nothing, `docs/cli.md` → `### Updating an adopted repository` omits the flag, and no test covers this warning on an upgrade.

**Fix:** name the working command. In `cli/src/generators/permissionProfile.ts`, beside `DOCTOR_COMMAND`, add:

```ts
/** The run that re-renders a profile already on disk, which a plain `init` keeps. */
const UPGRADE_COMMAND = 'npx devscene init --upgrade';
```

`DOCTOR_COMMAND` is declared below `appendToolchainAllowances`; that is safe because the constant is read only when the function runs. Then replace the warning's closing sentence, so the message reads:

```ts
    warn(
      `the parity phase is on and no ${TOOLCHAIN_FLAG} was given, so the reference implementation's own toolchain is not allow-listed: it usually sits outside the checkout, where no other entry in the permission profile reaches it. Run \`${UPGRADE_COMMAND} ${TOOLCHAIN_FLAG} <absolute path>\` to add one entry per parity.toolchainCommands value; a plain re-run keeps the existing profile`,
    );
```

In `docs/cli.md` → `### Updating an adopted repository`, directly after the fenced `npx devscene@<version> init --upgrade` block, add:

````markdown
With `phases.parity` on, name the reference toolchain on every upgrade. Its entries are rendered only from this flag, so a run without it removes them:

```bash
npx devscene@<version> init --upgrade --reference-toolchain-path <absolute path>
```
````

In `cli/test/profile-upgrade.test.mjs`, add a case using the `parityOn` configuration shape of the test `a toolchain-shaped entry is accounted for only with the parity phase on`: `planned({ ...repo, config: parityOn }).result.warnings` holds a line containing `init --upgrade --reference-toolchain-path <absolute path>`. That test file is the only one this fix edits, so it is the only test the fix runs.
