### Task 10 — Wire `init --upgrade` end to end

**Goal:** Ship the command: one run that upgrades the outer-loop scripts and the permission profile, reports what changed, and leaves every other file alone.

**Depends on:** Task 1 (`WriteContext.backupDir`), Task 5 (`planProfileUpgrade`), Task 6 (`planOuterLoopScriptUpgrade`), Task 7 (`installedPluginVersion`), Task 8 (`resolveUpgradeTarget`) and Task 9 (`upgradeReport`).

**The contracts this task calls.**

- `resolveUpgradeTarget({ cwd: string, dryRun: boolean, assertRepositoryAllowed: (repoRoot: string) => unknown }): UpgradeTarget`, from `cli/src/upgrade/preconditions.ts`. It returns `{ repoRoot: string, config: HarnessConfig, gitCommonDir: string, notes: readonly string[] }` and throws `HarnessError` on a refusal. Under `dryRun`, `notes` carries each refusal a real run would make for an active or unreadable run registry.
- `planOuterLoopScriptUpgrade({ repoRoot, config, plan }): OuterLoopScriptsResult`, from `cli/src/generators/outerLoopScripts.ts`. This task reads only its `scriptsDir: string`, the `outerLoopScriptsDir(config)` value. The result's `notes` describe plain `init` and are not printed here.
- `planProfileUpgrade({ repoRoot, config, plan, referenceToolchainPath?, dryRun }): { path: string, repoPath: string, previous: JsonObject | undefined, rendered: JsonObject, delta: readonly ProfileEntryDelta[], localAdditionCount: number, previousUnreadable: boolean, warnings: readonly string[], notes: readonly string[] }`, from `cli/src/generators/profileUpgrade.ts`. `ProfileEntryDelta` is `{ list: string, added: readonly string[], removed: readonly string[] }`. A refused local file throws.
- `installedPluginVersion(repoRoot?: string): string | undefined`, from `cli/src/machine/plugins.ts`.
- `upgradeReport({ dryRun: boolean, repoRoot: string, scriptsDir: string, applied: readonly WriteResult[], delta: readonly ProfileEntryDelta[], previousUnreadable: boolean, localAdditionCount: number, backupDir: string, localFileIgnored: boolean | undefined, cliVersion: string, pluginVersion: string | undefined }): { notes: readonly string[], warnings: readonly string[], result: string }`, from `cli/src/upgrade/report.ts`.

### Targets

- `cli/src/upgrade/initUpgrade.ts` (new)
- `cli/src/commands/init.ts`
- `cli/test/init-upgrade.test.mjs` (new)

**Work:**

- [ ] `init.ts`: add `InitFlags.upgrade`, an `UPGRADE_FLAG = '--upgrade'` switch row in `INIT_OPTIONS` and its entry in `parseInitFlags`. In `run`, right after parsing and before any repository is resolved, refuse `--upgrade` with the global `--force`, and with every `INIT_OPTIONS` flag given other than `--upgrade` and `--reference-toolchain-path`, naming the flag. Then return `runInitUpgrade`.
- [ ] `initUpgrade.ts`: open with a header stating that the module orders and reports the `--upgrade` run and, in the words *"The rule this module exists to enforce"*, that only the outer-loop scripts and the permission profile are planned, and that all refusals and planning finish before one `plan.apply`, so a refused run writes nothing. Export `runInitUpgrade(ctx, { referenceToolchainPath, assertRepositoryAllowed }): number`. `assertRepositoryAllowed` is `selfAdoptionOf`, passed from `init.ts`, so `HARNESS_SELF_ADOPT=1` opens this repository as it does for `init`. In order: `resolveUpgradeTarget` with `ctx.cwd` and `ctx.flags.dryRun`, a new `WritePlan`, `planOuterLoopScriptUpgrade`, `planProfileUpgrade`, then one `plan.apply` with `force: false`. A refused local file therefore stops the run before any write.
- [ ] Backups and report: `backupDir` is `<gitCommonDir>/devscene/upgrade-backups/<UTC timestamp to the millisecond>`. After applying, gather `pathIsIgnored` (only when the local file exists), `installedPluginVersion` and `ownManifestString('version')`, and pass the script result's `scriptsDir` to `upgradeReport`. Through `ctx.report`, on real and dry runs alike and in this order: `target.notes` and the profile plan's `notes` with `info`, the profile plan's `warnings` with `warn`, `upgradeReport`'s `notes` with `info`, its `warnings` with `warn`, and its `result` with `result`. Return `EXIT.OK`.
- [ ] `init-upgrade.test.mjs`, repository scope, on a wired fixture with filled `.claude/CLAUDE.md`, conventions documents, `.claude/review-sweep.md`, `.claude/devscene-task-offer.md`, an edited wrapper, ledgers and state-directory READMEs: only outer-loop scripts and the profile change, and `git status` shows nothing else; a second run changes nothing and adds no backup; a changed file's old bytes are under the common directory's backup tree; `--dry-run` leaves the tree byte-identical and names added and removed profile entries; `--force` with `--upgrade` and another `init` flag with `--upgrade` are refused byte-identically; an active run is refused, and the same fixture under `--dry-run` exits `0`, stays byte-identical and prints the would-refuse note.
- [ ] `init-upgrade.test.mjs`, behaviour scope: a deleted agent-invocable script and its stripped entries return to `allow`, `deny` and `denyWrite`; a local entry appears and survives a further upgrade; a local file setting another key is refused with scripts and profile byte-identical; a retired generated entry disappears and is reported; a note or warning the profile render emits is printed on both a real run and a dry run; a script running during the upgrade finishes on its original contents, using a script that blocks on a marker file the test creates after the upgrade; the restart line appears when the watcher changes.

**Verification:**

- `cli/test/init-upgrade.test.mjs` passes.
- `init --help` lists `--upgrade`.
- A plain `init` over the same fixture behaves as it did: an edited outer-loop script and the existing profile are both kept.
