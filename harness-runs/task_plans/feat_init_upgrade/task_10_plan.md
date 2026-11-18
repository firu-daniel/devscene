### Task 10 — Wire `init --upgrade` end to end

**Goal:** Ship the command: one run that upgrades the outer-loop scripts and the permission profile, reports what changed, and leaves every other file alone.

**Depends on:** Task 1 (`WriteContext.backupDir`), Task 5 (`planProfileUpgrade`), Task 6 (`planOuterLoopScriptUpgrade`), Task 7 (`installedPluginVersion`), Task 8 (`resolveUpgradeTarget`) and Task 9 (`upgradeReport`).

### Targets

- `cli/src/upgrade/initUpgrade.ts` (new)
- `cli/src/commands/init.ts`
- `cli/test/init-upgrade.test.mjs` (new)

**Work:**

- [ ] `init.ts`: add `InitFlags.upgrade`, an `UPGRADE_FLAG = '--upgrade'` switch row in `INIT_OPTIONS` and its entry in `parseInitFlags`. In `run`, right after parsing and before any repository is resolved, refuse `--upgrade` with the global `--force`, and with every `INIT_OPTIONS` flag given other than `--upgrade` and `--reference-toolchain-path`, naming the flag. Then return `runInitUpgrade`.
- [ ] `initUpgrade.ts`: export `runInitUpgrade(ctx, { referenceToolchainPath, assertRepositoryAllowed }): number`. `assertRepositoryAllowed` is `selfAdoptionOf`, passed from `init.ts`, so `HARNESS_SELF_ADOPT=1` opens this repository as it does for `init`. In order: `resolveUpgradeTarget`, a new `WritePlan`, `planOuterLoopScriptUpgrade`, `planProfileUpgrade`, then one `plan.apply` with `force: false`. A refused local file therefore stops the run before any write.
- [ ] Backups and report: `backupDir` is `<gitCommonDir>/devscene/upgrade-backups/<UTC timestamp to the millisecond>`. After applying, gather `pathIsIgnored` (only when the local file exists), `installedPluginVersion` and `ownManifestString('version')`, then send `upgradeReport`'s `notes`, `warnings` and `result` through `ctx.report`. Return `EXIT.OK`.
- [ ] `init-upgrade.test.mjs`, repository scope, on a wired fixture with filled `.claude/CLAUDE.md`, conventions documents, `.claude/review-sweep.md`, `.claude/devscene-task-offer.md`, an edited wrapper, ledgers and state-directory READMEs: only outer-loop scripts and the profile change, and `git status` shows nothing else; a second run changes nothing and adds no backup; a changed file's old bytes are under the common directory's backup tree; `--dry-run` leaves the tree byte-identical and names added and removed profile entries; `--force` with `--upgrade` and another `init` flag with `--upgrade` are refused byte-identically; an active run is refused.
- [ ] `init-upgrade.test.mjs`, behaviour scope: a deleted agent-invocable script and its stripped entries return to `allow`, `deny` and `denyWrite`; a local entry appears and survives a further upgrade; a local file setting another key is refused with scripts and profile byte-identical; a retired generated entry disappears and is reported; a script running during the upgrade finishes on its original contents, using a script that blocks on a marker file the test creates after the upgrade; the restart line appears when the watcher changes.

**Verification:**

- `cli/test/init-upgrade.test.mjs` passes.
- `init --help` lists `--upgrade`.
- A plain `init` over the same fixture behaves as it did: an edited outer-loop script and the existing profile are both kept.
