### Task 3 — Write-protect and ignore the local additions file

**Goal:** Stop a session granting itself permissions through `.claude/settings.autonomous.local.json`, and keep that file out of git in every newly merged ignore block.

**Depends on:** Task 2, which exports `PROFILE_LOCAL_PATH` from `cli/src/generators/profileEntries.ts`.

**Where this task stops.** It protects the main checkout's copy only, because a run loads no other copy. `--upgrade` does not write `.gitignore`: Tasks 9 and 11 warn when an existing local file is not ignored.

### Targets

- `cli/src/generators/writeProtection.ts`
- `cli/src/generators/repoRoot.ts`
- `cli/templates/repo/gitignore`
- `cli/test/profile-local-protection.test.mjs` (new)

**Work:**

- [ ] `writeProtection.ts` → `protectedPaths`: add `{ path: join(repoRoot, PROFILE_LOCAL_PATH), kind: 'file', reason }` directly after the `PROFILE_PATH` entry. The reason states that its entries are merged into the profile every run is rendered from. Update the module header's list of the set.
- [ ] `repoRoot.ts` and `cli/templates/repo/gitignore`: add a `{{permissionProfileLocalPath}}` token rendered from `PROFILE_LOCAL_PATH`, on its own line after `{{permissionProfilePath}}`, with a comment saying the file holds one machine's additions and is never committed.
- [ ] `profile-local-protection.test.mjs`: on a fixture wired by the compiled CLI, assert the absolute path is in `sandbox.filesystem.denyWrite`, its exact `Edit` rule is in `permissions.deny`, `doctor`'s `profile-write-protection` line passes, git ignores the path (`ignoredAmong`), `jobSurfacePaths` includes `.claude/settings.autonomous.local.json`, and `copySurfacePaths` does not. The last pair is why the shell mirror `hr_run_protected_rel_paths` needs no change.

**Verification:**

- `cli/test/profile-local-protection.test.mjs` passes.
- A second `init` on the fixture reports `.gitignore` kept.
- `hr_run_protected_rel_paths` in `cli/templates/scripts/lib/harness-run-lib.sh` is unchanged.
