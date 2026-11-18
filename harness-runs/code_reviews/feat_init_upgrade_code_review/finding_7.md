### 7. `renderCurrentProfile` is exported for `init --upgrade` and `doctor`, but only a test calls it

**File:** `cli/src/generators/profileUpgrade.ts` (`renderCurrentProfile`) — "export function renderCurrentProfile(options: RenderCurrentProfileOptions): JsonObject {"

The story index lists `renderCurrentProfile` among what "`--upgrade` and `doctor` need to know about the profile". Neither calls it: `planProfileUpgrade` and `profileDrift` each read the local additions once and call the private `renderWith`. Its only callers are three lines of `cli/test/profile-upgrade.test.mjs`, so the suite exercises a production entry point that no production path takes.

**Fix:** remove the export and point the tests at the renderer they are really exercising.

In `cli/src/generators/profileUpgrade.ts`:

- Delete `renderCurrentProfile` and its doc comment.
- Change `/** What {@link renderCurrentProfile} takes. */` to `/** What {@link renderWith} takes, beyond the local additions. */`.
- Remove `export` from `interface RenderCurrentProfileOptions`.

In `cli/test/profile-upgrade.test.mjs`:

- Remove `renderCurrentProfile` from the `profileUpgrade.js` import, and add `import { dirname } from 'node:path';` if `dirname` is not already imported.
- Add `import { renderProfile } from '../dist/generators/permissionProfile.js';`.
- Add this helper beside the file's other helpers:

  ```js
  const freshRender = (repo) => renderProfile({ repoRoot: repo.dir, config: repo.config, workRoot: dirname(repo.dir) });
  ```

- Replace each of the three calls with `freshRender(repo)`, keeping the `.permissions` access at the first. None of the three tests writes a local additions file, and `renderProfile` does not carry entries forward by default, which is what the first two ask for and what the third does not depend on.
- Rename the test `carried plugin-root entries stay, and renderCurrentProfile can leave them out` to `carried plugin-root entries stay, and a fresh render leaves them out`.

That test file is the only one this fix edits, so it is the only test the fix runs.
