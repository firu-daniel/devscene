### Task 1 — Switch off commit attribution and drop the raw commit grant in the run profile template

**Goal:** Change the unattended run profile so that a run's sessions are never told to append Claude Code's attribution lines to a commit, and so that the profile no longer grants a raw `git commit` and denies the amend outright. Every commit a run makes still goes through the excluded `commit-on-branch.sh`.

**Where this task stops.** It edits the template and adds one test. It does not touch `cli/src/generators/writeProtection.ts` or the watcher's per-run rows, which are **Task 2's**: that task also edits `cli/test/profile.test.mjs`, so this task puts its assertions in a new suite of its own. It does not touch the plugin guard that auto-allows `git commit`, which is **Task 4's**. It writes no document under `docs/`, which is **Tasks 6 and 7's**. The rendered copies of this template are re-rendered by hand after merge (story index → `Manual setup required`), not by this task.

### Targets

- `cli/templates/claude/settings.autonomous.json` — the run profile template.
- `cli/test/profile-commit-attribution.test.mjs` (new) — drives `init` against a throwaway fixture and asserts the rendered profile's three changes.

**Work:**

- [ ] `settings.autonomous.json`: add a top-level `"attribution": {"commit": "", "pr": ""}`, placed after `"model"` and before `"sandbox"`. Write the object form, never `"attribution": false`. That form needs Claude Code v2.1.281 or later, and an older version skips the whole settings file that holds it. A `-p` session ignores an invalid settings file silently (`docs/sandbox-record.md` → `## 6. The residuals`, item 11), so on an older Claude Code the `false` form would start the run without this profile's sandbox block and `deny` rules. Set no `sessionUrl` key: `attribution.sessionUrl` applies only to cloud and Remote Control sessions, and an unattended run is a local or job `-p` session.
- [ ] `settings.autonomous.json` `permissions`: remove `"Bash(git commit:*)"` from `allow`, and add `"Bash(git commit --amend:*)"` to `deny`. No flow issues a raw commit in an unattended run. Every commit point calls the main checkout's excluded `commit-on-branch.sh`. Add no other entry to any list: no new permission.
- [ ] `settings.autonomous.json` `_README`: add one paragraph, `COMMIT ATTRIBUTION IS OFF, AND ONLY THE COMMIT WRAPPER COMMITS: …`, placed after the `` `deny` IS A FLOOR… `` paragraph. It covers four points:
  - **What the attribution key removes.** It removes Claude Code's instruction to end commit messages and pull-request bodies with its attribution lines, which is where the trailer in a run's commit came from.
  - **Why the object form.** The object form, not `false`, because of the v2.1.281 floor and the silent skip.
  - **Who still decides on trailers.** The adopter's own commit-message policy still decides whether a commit carries a trailer: an agent that commits adds one only where that policy requires it.
  - **Why no raw commit is granted.** `git commit` is no longer in `allow`, because every commit a run makes goes through the excluded commit wrapper, and the amend is denied because a raw amend in a run copy moves that copy's branch alone. Say also that the harness plugin's commit guard withholds its own `allow` for an amend, which ties the deny to the guard the way the floor paragraph ties `Bash(git branch -D:*)` to `hc_piece_is_never_safe`.

  Keep the paragraph one string, ASCII-safe like its neighbours, and carry no `{{…}}` token.
- [ ] `cli/test/profile-commit-attribution.test.mjs`: a new suite whose header opens with the rule it enforces, *"the unattended profile switches off Claude Code's commit attribution in its object form, grants no raw `git commit` and denies the amend"*, following `.claude/context/conventions.md` → `## The testing bar`. Build a throwaway fixture with `cli/test/helpers/fixture.mjs`, run the compiled CLI's `init` against it, read the written `.claude/settings.autonomous.json`, and assert:
  - `attribution` deep-equals `{ commit: '', pr: '' }`;
  - `permissions.allow` holds no entry equal to `Bash(git commit:*)` and none starting `Bash(git commit`;
  - `permissions.deny` includes `Bash(git commit --amend:*)`;
  - one `_README` line starts `COMMIT ATTRIBUTION IS OFF`.

  This suite reads one fixed file per fixture. It is not a tree-reading test and owes no `treeGuards` entry.

**Verification:**

- `cli/test/profile-commit-attribution.test.mjs` passes, run through `npm test --workspace cli -- test/profile-commit-attribution.test.mjs`.
- `bash scripts/typecheck.sh` exits 0.
- The rendered profile still parses as one JSON object, and its `_README` paragraphs stay one string each.
