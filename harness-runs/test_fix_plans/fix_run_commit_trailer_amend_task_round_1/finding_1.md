### 1. Placeholder-host profile test still counts three kept `COPY_GIT_PATHS` rows

**Site:** `cli/test/watcher-run-profile.test.mjs`, in the test `on a placeholder host a clone's per-run copy re-roots the base's trio globs at every other sibling`, the line `assert.equal(kept.length, 3);` (around line 433, navigation hint only), directly after `const kept = COPY_GIT_PATHS.filter((row) => row.bubblewrapDenyWrite);`.

**Failing test:** `cli/test/watcher-run-profile.test.mjs` — `on a placeholder host a clone's per-run copy re-roots the base's trio globs at every other sibling`

**Failure (from the log, gate 4 `npm test`):**

```
not ok 1988 - on a placeholder host a clone's per-run copy re-roots the base's trio globs at every other sibling
  location: 'cli/test/watcher-run-profile.test.mjs:395:1'
  error: |-
    Expected values to be strictly equal:

    6 !== 3

  expected: 3
  actual: 6
  operator: 'strictEqual'
  stack: |-
    TestContext.<anonymous> (cli/test/watcher-run-profile.test.mjs:433:10)
```

(The location and stack-frame paths, absolute `file://` URLs in the log, are rewritten to their repo-relative form.)

**Classification:** new this round (round 1; no earlier logs). Fixable on the branch.

**Diagnosis:** This branch's Task 1 (commit `cda236e7`, "Write-deny the run copy's branch-ref store and HEAD") appended three rows to `cli/src/generators/writeProtection.ts` → `COPY_GIT_PATHS` — `.git/HEAD` (`file`), `.git/refs/heads` (`directory`) and `.git/packed-refs` (`file`) — each with `bubblewrapDenyWrite: true`. The shell mirror in `cli/templates/scripts/autonomous-watcher.sh` → `RUN_PROFILE_COPY_GIT_PATHS` was updated to match (its last three lines are `.git/HEAD file deny`, `.git/refs/heads directory deny`, `.git/packed-refs file deny`), and `cli/test/profile.test.mjs` was updated, but `cli/test/watcher-run-profile.test.mjs` was not touched by that commit. The table now has three `omit` rows (`commondir`, `config.worktree`, `objects/info/http-alternates`) and six `deny` rows, so `omitted.length` is still 3 (line 432 passes) while `kept.length` is 6. The assertion at line 433 is a stale hard-coded count of the table's shape, not a defect in the production code: the loop that follows (`for (const row of kept)`) already checks each kept row against `denyWrite` and `permissions.deny` by exact path, so it covers the three new rows once the count is corrected.

**Fix:**

- [ ] In `cli/test/watcher-run-profile.test.mjs`, change `assert.equal(kept.length, 3);` to `assert.equal(kept.length, 6);`, keeping `assert.equal(omitted.length, 3);` as is. The count pins the table's shape deliberately (three trio rows plus three branch-ref-store rows kept), so update the literal rather than deleting the assertion or deriving it from the table.
- [ ] If the test's own comment or the `makeSiblings` / file header prose near this test describes the kept set as three rows or as "the trio" when it means the kept rows, amend that wording in the same edit so it names six kept rows (the original three plus `.git/HEAD`, `.git/refs/heads`, `.git/packed-refs`). Do not touch prose that means the three `omit` rows (the "trio globs").
- [ ] Leave `cli/src/generators/writeProtection.ts` and `cli/templates/scripts/autonomous-watcher.sh` unchanged: they already agree with each other.
