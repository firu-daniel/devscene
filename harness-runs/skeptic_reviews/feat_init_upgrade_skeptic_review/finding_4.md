### 4. The carry-forward warning tells the adopter to re-add an entry by hand, which the next replacement deletes

**File:** `cli/src/generators/permissionProfile.ts` (`appendCarriedPluginRootEntries`) — "Nothing re-derives ${object}: add ${object} back by hand."

**Problem.** The `notPreserved` warning covers an absolute `allow` entry outside this checkout and outside every resolved plugin root, a reference-implementation `Read` being the usual case. It ends: "Nothing re-derives them: add them back by hand."

This branch makes `.claude/settings.autonomous.json` a generated file, so that advice no longer works:

- `carriedPluginRootEntries` puts the same entry back in `notPreserved` on the next `init --upgrade` or `--force`, so the entry is removed again.
- Until then, `doctor`'s `profile-drift` reports it as an entry "nothing here accounts for, from a hand edit or tampering".

**Runtime symptom, and why it is reachable.** The first `init --upgrade` on a profile holding such an entry prints two conflicting remedies. This warning says to add it back by hand. `upgradeReport`'s `removedEntriesWarning` says it belongs in `.claude/settings.autonomous.local.json`. An adopter who follows this one loses the grant at the next upgrade, and an unattended run's reads under that directory are then refused again. The local file is the route that lasts: an entry it supplies is skipped by the carry-forward and merged by the render.

**Fix.**

1. In `cli/src/generators/permissionProfile.ts`, in that warning, replace

   ```text
   Nothing re-derives ${object}: add ${object} back by hand. Left behind:
   ```

   with

   ```text
   Nothing re-derives ${object}: add ${object} to ${PROFILE_LOCAL_PATH}, then run \`${UPGRADE_COMMAND}\`. Left behind:
   ```

   `PROFILE_LOCAL_PATH` is already imported there and `UPGRADE_COMMAND` is already declared in the module. Leave the two "Re-add it by hand" and "lines to paste" warnings for plugin-root entries as they are: those entries are carried forward.

2. In `cli/test/init.test.mjs`:
   - Change `const BY_HAND_REMEDY = 'back by hand';` to `const LOCAL_FILE_REMEDY = 'to .claude/settings.autonomous.local.json, then run';`, and rename its two uses.
   - Change the assertion `reported.includes('add it back by hand')` to `reported.includes('add it to .claude/settings.autonomous.local.json')`.
