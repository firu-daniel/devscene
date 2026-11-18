### Task 9 — Add the `--upgrade` report

**Goal:** Turn the outcome of an upgrade or a dry run into the exact lines an adopter needs to act on, as a pure function that can be tested alone.

**Depends on:** Task 5, for `ProfileEntryDelta`, which is `{ readonly list: string; readonly added: readonly string[]; readonly removed: readonly string[] }`. Task 6, for `OUTER_LOOP_SCRIPTS` paths through `outerLoopRelativePath`, `WATCHER_SCRIPT_NAME` and `RESTART_WATCHER_SCRIPT_NAME`. Task 1, for `WriteResult` with `effect` and `backupPath`.

**Where this task stops.** It reads no file and prints nothing. Task 10 gathers the inputs and sends the three returned lists through the `Reporter`, together with the notes and warnings `resolveUpgradeTarget` and `planProfileUpgrade` return, which this function does not take.

### Targets

- `cli/src/upgrade/report.ts` (new)
- `cli/test/upgrade-report.test.mjs` (new)

**Work:**

- [ ] Create the module with a header stating that it owns the wording of the `--upgrade` report and, in the words *"The rule this module exists to enforce"*, that it is a pure function which reads no file and prints nothing. Export `upgradeReport(input): { readonly notes: readonly string[]; readonly warnings: readonly string[]; readonly result: string }`. `input` is `{ dryRun, repoRoot, scriptsDir, applied: readonly WriteResult[], delta: readonly ProfileEntryDelta[], previousUnreadable, localAdditionCount, backupDir, localFileIgnored: boolean | undefined, cliVersion, pluginVersion }`, and `scriptsDir` is the `outerLoopScriptsDir(config)` value.
- [ ] Profile lines: for each list with a change, name the list and every entry added and removed, in the tense `dryRun` calls for. Entries removed get one warning saying the generator does not produce them, that they were not moved automatically, and that anything still wanted belongs in `PROFILE_LOCAL_PATH` followed by another `init --upgrade`.
- [ ] Run lines: name the backup directory only when a backup was taken. Print the restart instruction, built with `scriptInvocation(scriptsDir, RESTART_WATCHER_SCRIPT_NAME)` from `cli/src/generators/scripts.ts`, when the watcher or a `lib/` row was created or replaced, since the running daemon holds the code it parsed and sourced. A real run's `result` states how many files changed, or that the repository is already current; a dry run's states what would change.
- [ ] Warnings: `localFileIgnored === false` names the file and says a plain `init` merges the ignore rule. A readable `pluginVersion` that differs from `cliVersion` names both and says to run `init --upgrade` from the CLI matching the plugin. `previousUnreadable` says the old profile could not be compared.
- [ ] `upgrade-report.test.mjs`: cover each line above in both tenses, the no-change case, no restart line when only the profile changed, no version line when `pluginVersion` is `undefined`, and the restart line reading `bash scripts/restart-watcher.sh` for a `scriptsDir` of `scripts` and `bash restart-watcher.sh` for a `scriptsDir` of `.`. All output is plain ASCII.

**Verification:**

- `cli/test/upgrade-report.test.mjs` passes.
- `report.ts` imports no `node:fs` function and calls no `console` method.

**Deviations from plan:** The plan's removed-entries warning sends anything still wanted to `PROFILE_LOCAL_PATH`; `readLocalAdditions` refuses every key outside `LOCAL_ADDITION_LISTS`, and a removed entry can come from another list. The warning therefore limits that advice to the four accepted lists, read from `LOCAL_ADDITION_LISTS`.
