### 2. Profile settings outside the entry lists are dropped without a report, and `profile-drift` passes with them changed

**File:** `cli/src/generators/profileUpgrade.ts` (`profileEntryDelta`, `profileDrift`) — "return PROFILE_ENTRY_LISTS.flatMap((row) => {" and "for (const row of PROFILE_ENTRY_LISTS) {"

**Problem.** Both comparisons look only at `PROFILE_ENTRY_LISTS`. The file `init --upgrade` replaces, and the file `doctor` grades, also holds settings that are not in those lists. The shipped template has `permissions.defaultMode`, `model`, `attribution.*`, `sandbox.enabled`, `sandbox.network.*` and others. A hand edit can add any further key, such as `hooks` or `env`.

`.claude/settings.autonomous.local.json` refuses all of these (`cli/src/generators/profileLocal.ts` → `validatedEntryCount`), so an adopter has no route that keeps one.

**Runtime symptom, and why it is reachable.**

- **The upgrade.** A profile holding a hand-added `env` or `hooks` key, or a changed `permissions.defaultMode`, is replaced by the render. `planProfileUpgrade` computes `delta` from the lists alone, and `upgradeReport` builds its profile lines and its removal warning from `delta`. The run prints `Upgrade complete: 1 file changed.` and names no lost setting. `--dry-run` previews the same silence. The story index names this risk first ("a profile that loses or gains a grant unnoticed").
- **`doctor`.** `profile-drift`, titled "the permission profile matches what this CLI renders", exists to catch "a hand edit or tampering" (`docs/cli.md` → the `profile-drift` bullet). With `hooks` added to the profile, or `permissions.defaultMode` changed, it passes and says the profile holds no entry it cannot account for. `hooks` is the serious case: `cli/src/generators/writeProtection.ts` records that Claude Code runs declared hooks outside the sandbox. No other `doctor` check reads either key. `profile-sandbox` grades only `GRADED_SETTINGS` in `cli/src/generators/sandboxProfile.ts`, and the watcher's `run_profile_check` reads neither.

The evidence is from reading the code. A throwaway-fixture run of the CLI was refused by the permission layer.

**Fix.**

1. In `cli/src/generators/profileUpgrade.ts`, import `README_KEY` from `./profileEntries.js` and add:

   ```ts
   const ENTRY_LIST_PATHS: ReadonlySet<string> = new Set(PROFILE_ENTRY_LISTS.map(({ path }) => path));

   /**
    * The dotted keys outside the entry lists and the rationale block whose value differs between two
    * profiles: a key on one side only, or a different value. Objects are compared key by key, so key
    * order is not a difference.
    */
   export function profileSettingChanges(current: JsonObject, next: JsonObject, parent: readonly string[] = []): readonly string[] {
     const keys = [...new Set([...Object.keys(current), ...Object.keys(next)])];
     return keys.flatMap((key) => {
       if (parent.length === 0 && key === README_KEY) return [];
       const path = [...parent, key];
       const dotted = path.join('.');
       if (ENTRY_LIST_PATHS.has(dotted)) return [];
       const before = current[key];
       const after = next[key];
       if (isJsonObject(before) && isJsonObject(after)) return profileSettingChanges(before, after, path);
       return JSON.stringify(before) === JSON.stringify(after) ? [] : [dotted];
     });
   }
   ```

2. Add `readonly settingChanges: readonly string[];` to `ProfileUpgradePlan`, and return `settingChanges: previous === undefined ? [] : profileSettingChanges(previous, rendered)` from `planProfileUpgrade`.

3. Add `readonly settings: readonly string[];` to `ProfileDrift`, documented as "settings outside the entry lists that differ from the render". Return `{ missing, unaccounted, settings: profileSettingChanges(onDisk, expected) }` from `profileDrift`.

4. In `cli/src/upgrade/report.ts`, add `readonly settingChanges: readonly string[];` to `UpgradeReportInput`, read it in `upgradeReport`, and after the `removedEntriesWarning` push add:

   ```ts
   if (settingChanges.length > 0) {
     const names = settingChanges.join(', ');
     warnings.push(
       dryRun
         ? `${counted(settingChanges.length, 'profile setting')} outside the entry lists would be reset to what this CLI renders: ${names}. ${PROFILE_LOCAL_PATH} cannot hold them; the replaced file would be backed up first.`
         : `${counted(settingChanges.length, 'profile setting')} outside the entry lists ${settingChanges.length === 1 ? 'was' : 'were'} reset to what this CLI renders: ${names}. ${PROFILE_LOCAL_PATH} cannot hold them; the replaced file is under ${backupDir}.`,
     );
   }
   ```

   In `cli/src/upgrade/initUpgrade.ts`, pass `settingChanges: profile.settingChanges` to `upgradeReport`.

5. In `cli/src/doctor/checks.ts` → `PROFILE_DRIFT_CHECK`, destructure `settings` from `drift`. After the `unaccounted` finding add:

   ```ts
   if (settings.length > 0) {
     findings.push(`${PROFILE_PATH} has settings that differ from this CLI's render, from a hand edit, tampering or an earlier release — ${settings.join(', ')}`);
   }
   ```

   Change the remedy condition to `missing.length > 0 || unaccounted.length > 0 || settings.length > 0`. Change the pass message to `${PROFILE_PATH} holds every entry and setting this CLI renders for this configuration, and no entry or setting it cannot account for.${unmeasured}`.

6. In `docs/cli.md`:
   - In the `profile-drift` bullet of `## 7.`, after "from a hand edit or tampering", add: "It also reports any setting outside those lists, such as `permissions.defaultMode` or an added `hooks` key, whose value differs from the render."
   - In `### Updating an adopted repository`, in the paragraph beginning "**The report is what the run changed and what is left for you.**", add "every setting outside the entry lists that this run reset;" to the list of what the run warns about.

7. Tests:
   - In `cli/test/profile-upgrade.test.mjs`, add `settings: []` to each whole-object `assert.deepEqual(drift(...), { missing: ..., unaccounted: ... })`. Add a case that sets `onDisk.hooks = {}` and `onDisk.permissions.defaultMode = 'bypassPermissions'` on a copy of the rendered profile and asserts `drift(repo, onDisk).settings` equals `['permissions.defaultMode', 'hooks']`.
   - In the same file, add a `planProfileUpgrade` case where the existing profile carries `env`, asserting `settingChanges` is `['env']`.
   - In `cli/test/upgrade-report.test.mjs`, add `settingChanges: []` to the `report` helper's input, and add one case for each tense asserting the warning names the key.
   - In `cli/test/doctor-upgrade-drift.test.mjs`, add a case where a profile carrying a `hooks` key makes `profile-drift` warn and name `hooks`.

**Deviations from plan:**

- Step 5 specified `settings.join(', ')`. The `profile-drift` finding JSON-quotes each key instead, as `driftedEntry` does for entries: a raw key holding a line break could print a forged `PASS` line in `doctor`'s report. `cli/test/doctor-upgrade-drift.test.mjs` covers it.
- Step 7 gained one case beyond the list, in `cli/test/init-upgrade.test.mjs`: `.claude/context/cli.md` → `## What "done" means here` requires a command change to be driven through the compiled CLI, and nothing else covers the `settingChanges` wiring in `cli/src/upgrade/initUpgrade.ts`.
- Step 6 (`docs/cli.md`) is outside the `cli` path. The readiness entry is tagged `cli, general`, so the `general` layer's dispatch owns it.
