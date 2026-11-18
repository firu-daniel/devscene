### Task 5 — Add the profile upgrade planner, entry delta and drift comparison

**Goal:** Give `init --upgrade` and `doctor` one shared answer to what the profile should be and how the file on disk differs from it.

**Depends on:** Task 1 (`replace-if-changed`), Task 2 (`readLocalAdditions`, `PROFILE_LOCAL_PATH`), and Task 4 (`renderProfile`'s `localAdditions` option and `isToolchainEntry`).

**Where this task stops.** It plans and compares. Task 10 calls `planProfileUpgrade`, Task 9 words its delta, and Task 11 calls `profileDrift`.

### Targets

- `cli/src/generators/profileUpgrade.ts` (new)
- `cli/test/profile-upgrade.test.mjs` (new)

**Work:**

- [ ] Create the module with its rule in the header: `--upgrade` and `doctor` compare against one render. Export `PROFILE_ENTRY_LISTS` (`permissions.allow`, `permissions.ask`, `permissions.deny`, `permissions.additionalDirectories`, `sandbox.filesystem.denyWrite`) and `interface ProfileEntryDelta { readonly list: string; readonly added: readonly string[]; readonly removed: readonly string[] }`.
- [ ] `renderCurrentProfile({ repoRoot, config, referenceToolchainPath?, pluginRootEntries?, dryRun?, warn?, note? }): JsonObject`: call `renderProfile` with `workRoot` from `core/paths.ts`, no `written` lists so the selection comes from the configuration, `force: true` so the existing plugin-root carry-forward runs, and `localAdditions: readLocalAdditions(repoRoot)`.
- [ ] `profileEntryDelta(current: JsonObject | undefined, next: JsonObject): readonly ProfileEntryDelta[]`: per list, the strings only in `next` and only in `current`, in file order. `planProfileUpgrade({ repoRoot, config, plan, referenceToolchainPath?, dryRun })` renders, reads the existing profile tolerantly, enqueues `{ path, policy: 'replace-if-changed', content, label: 'unattended permission profile' }`, and returns `{ path, repoPath, previous, rendered, delta, localAdditionCount, previousUnreadable, warnings, notes }`.
- [ ] `profileDrift({ repoRoot, config, onDisk }): { missing: readonly ProfileEntry[]; unaccounted: readonly ProfileEntry[] }`, where `ProfileEntry` is `{ list, entry }`. `missing` is the render minus the disk. `unaccounted` is the disk minus the render, minus the same render with `pluginRootEntries: true`, minus entries `isToolchainEntry` accepts. A refusal from the local file or the render propagates to the caller.
- [ ] `profile-upgrade.test.mjs`: import the compiled module and use fixtures wired by the compiled CLI. Cover an unchanged profile having an empty delta, a retired entry appearing in `removed`, a missing script entry appearing in `added`, a local entry surviving a second render, carried plugin-root entries staying, an unreadable profile being planned as a replacement with `previousUnreadable`, `profileDrift` reporting both directions, and a toolchain-shaped entry being accounted for only with parity on.

**Verification:**

- `cli/test/profile-upgrade.test.mjs` passes.
- `planProfileUpgrade` called twice over an unchanged repository produces byte-identical content.
- The module makes no filesystem write of its own.
