### Task 9 — Add the `--upgrade` report

**Goal:** Turn the outcome of an upgrade or a dry run into the exact lines an adopter needs to act on, as a pure function that can be tested alone.

**Depends on:** Task 5, for `ProfileEntryDelta`. Task 6, for `OUTER_LOOP_SCRIPTS` paths through `outerLoopRelativePath` and `WATCHER_SCRIPT_NAME`. Task 1, for `WriteResult` with `effect` and `backupPath`.

**Where this task stops.** It reads no file and prints nothing. Task 10 gathers the inputs and sends the three returned lists through the `Reporter`.

### Targets

- `cli/src/upgrade/report.ts` (new)
- `cli/test/upgrade-report.test.mjs` (new)

**Work:**

- [ ] Export `upgradeReport(input): { readonly notes: readonly string[]; readonly warnings: readonly string[]; readonly result: string }`. `input` is `{ dryRun, repoRoot, scriptsDir, applied: readonly WriteResult[], delta: readonly ProfileEntryDelta[], previousUnreadable, localAdditionCount, backupDir, localFileIgnored: boolean | undefined, cliVersion, pluginVersion }`.
- [ ] Profile lines: for each list with a change, name the list and every entry added and removed, in the tense `dryRun` calls for. Entries removed get one warning saying the generator does not produce them, that they were not moved automatically, and that anything still wanted belongs in `PROFILE_LOCAL_PATH` followed by another `init --upgrade`.
- [ ] Run lines: name the backup directory only when a backup was taken. Print the restart instruction `bash <scriptsDir>/restart-watcher.sh` when the watcher or a `lib/` row was created or replaced, since the running daemon holds the code it parsed and sourced. A real run's `result` states how many files changed, or that the repository is already current; a dry run's states what would change.
- [ ] Warnings: `localFileIgnored === false` names the file and says a plain `init` merges the ignore rule. A readable `pluginVersion` that differs from `cliVersion` names both and says to run `init --upgrade` from the CLI matching the plugin. `previousUnreadable` says the old profile could not be compared.
- [ ] `upgrade-report.test.mjs`: cover each line above in both tenses, the no-change case, no restart line when only the profile changed, and no version line when `pluginVersion` is `undefined`. All output is plain ASCII.

**Verification:**

- `cli/test/upgrade-report.test.mjs` passes.
- `report.ts` imports no `node:fs` function and calls no `console` method.
