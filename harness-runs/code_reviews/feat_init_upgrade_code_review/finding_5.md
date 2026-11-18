### 5. `doctor`'s check comments still say the profile is the adopter's hand-tuned file

**File:** `cli/src/doctor/checks.ts` — the doc comments of the six sites below, each located by its quoted text

This branch makes `.claude/settings.autonomous.json` a generated file, with the adopter's additions in `.claude/settings.autonomous.local.json`. It rewrote the matching statements in `docs/cli.md` § 7 for `command-permissions`, `profile-paths`, `profile-write-protection` and `plugin-permissions`, but the comments those paragraphs describe still give the old reason for each check's grade. Two also say the no-root count is "the same set" `init --force` carries, which is no longer exact: local entries are counted there and not carried, and `init --upgrade` carries the set too. `.claude/context/cli.md` → `## What "done" means here` holds a change to the statements of the module it edits, and a maintainer grading these checks would reason from a retired ownership model.

**Fix:** make these six comment edits and change no code.

1. Quoted text: "the repository still runs in the foreground, and the\n * profile is a file the adopter owns. **The absent wrapper". Replace "profile is a file the adopter owns." with "profile is generated, so a re-render restores what it lacks."

2. Quoted text: "because a hand-tuned profile is a file the adopter may deliberately have pointed elsewhere." Replace with "because an entry from the local additions file may deliberately point elsewhere."

3. Quoted text, in the comment above `PROFILE_DENY_FLOOR_CHECK`: "the profile is\n * a file the adopter owns and may deliberately have restructured, and a run missing an entry is". Replace "the profile is a file the adopter owns and may deliberately have restructured, and a run" with "the profile is generated, so a re-render restores the floor, and a run".

4. Quoted text, in the comment above `PROFILE_WRITE_PROTECTION_CHECK`: "the profile is a file the\n * adopter owns and may deliberately have restructured, a run missing an entry is worse-defended". Replace "the profile is a file the adopter owns and may deliberately have restructured, a run" with "the profile is generated, so a re-render restores what it lacks, a run".

5. Quoted text, in the comment above `PLUGIN_PERMISSIONS_CHECK`: "machine-local gap with an operator remedy, and the profile is a file the adopter owns. And when no". Replace with "machine-local gap with an operator remedy. And when no".

6. Two places say the same thing about the no-root count:
   - In the comment above `PLUGIN_PERMISSIONS_CHECK`, replace "and it is the same set `init --force`\n * carries forward unverified on that arm" with "and it is the set `init --force` and\n * `init --upgrade` carry forward unverified on that arm, less any entry the local file supplies or the\n * profile records as local".
   - In the code comment beginning "Counted, never named.", replace "they are the\n      // set `init --force` carries forward unverified on this same arm." with "they are the\n      // set `init --force` and `init --upgrade` carry forward unverified on this same arm, less any\n      // entry the local file supplies or the profile records as local."

Keep the surrounding comment wrapped at its existing width. No test file changes, so this fix runs no test file.
