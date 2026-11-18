### Task 2 — Read and validate the local permission additions file

**Goal:** Define `.claude/settings.autonomous.local.json` and the one reader that decides whether its contents may reach a permission profile.

**Where this task stops.** It reads and validates only. Task 3 protects and ignores the file, and Task 4 merges the result into the rendered profile.

### Targets

- `cli/src/generators/profileEntries.ts`
- `cli/src/generators/profileLocal.ts` (new)
- `cli/test/profile-local.test.mjs` (new)

**Work:**

- [ ] `profileEntries.ts`: export `PROFILE_LOCAL_PATH = `${CLAUDE_DIR}/settings.autonomous.local.json``, documented beside `PROFILE_PATH`.
- [ ] `profileLocal.ts`: create the module with a header stating its rule in the words *"The rule this module exists to enforce"*: the file may only add entries, and only to the four lists. Export `LOCAL_ADDITION_LISTS` (`permissions.allow`, `permissions.ask`, `permissions.deny`, `sandbox.filesystem.denyWrite`, using `SANDBOX_KEY`), `interface LocalAdditions { readonly fragment: JsonObject; readonly count: number }`, and `readLocalAdditions(repoRoot: string): LocalAdditions | undefined`.
- [ ] What counts as absent: `readLocalAdditions` returns `undefined` when the path does not exist, when it is a 0-byte regular file, and when it is a character device that reads empty. Those last two are the bubblewrap placeholder shapes (`docs/sandbox-verification.md` → F9). A symlink, a directory, or any other shape throws `HarnessError` naming the path.
- [ ] What is refused, each as a `HarnessError` naming the file and the offending key or entry: a file tracked at `HEAD` (`pathAtRef`), invalid JSON, a non-object root, any key outside the four lists at any depth, a list that is not an array, a non-string or blank entry, an entry containing a `FORBIDDEN_IN_ENTRY` needle, and an entry carrying an unsubstituted token (`containsToken`). The tracked-file message says the file is machine-local, and that a remote job must never merge one.
- [ ] `profile-local.test.mjs`: import the compiled module and drive it against throwaway git fixtures. Cover each absent shape, a valid file with all four lists, each refusal with its message naming the key or entry, a symlink, a tracked file, and duplicates preserved for the merge to resolve. `count` is the number of entries the file lists.

**Verification:**

- `cli/test/profile-local.test.mjs` passes.
- A file setting `sandbox.enabled`, `permissions.defaultMode` or a top-level `_README` is refused with that key named.
- `profileLocal.ts` imports neither `permissionProfile.ts` nor `writeProtection.ts`.

**Deviations from plan:** `profileLocal.ts` also exports `readLocalFileText(path)`, which the plan does not list. A test cannot create a character device at the local file's path without privilege, so the empty-device shape is driven through this path-level reader against `/dev/null`; `readLocalAdditions` calls it for every shape.
