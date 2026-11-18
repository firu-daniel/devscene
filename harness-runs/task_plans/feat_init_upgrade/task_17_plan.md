### Task 17 — Bring the root ignore file and the notes-app example in step

**Goal:** Apply this branch's rendered changes to the root ignore file and the notes-app example, so neither disagrees with what the CLI now generates.

**Depends on:** Task 3 for the ignore line and protection entries, and Task 4 for the rewritten `_README` lines.

**What may change in the example.** `examples/notes-app/README.md` separates a frozen capture from a live fixture. `.claude/settings.autonomous.json`, `.gitignore` and the README's statement of that profile's figures are live. Its `devscene/` run artifacts and the prose of its `.claude/CLAUDE.md` and `.claude/context/` stay untouched.

The story index's `## Scope register` rows 65, 66, 71 and 82 to 87 are this task's register sites.

### Targets

- `.gitignore`
- `examples/notes-app/.gitignore`
- `examples/notes-app/.claude/settings.autonomous.json`
- `examples/notes-app/README.md`

**Work:**

- [ ] Root `.gitignore`: add `.claude/settings.autonomous.local.json` and its comment directly after the `.claude/settings.autonomous.json` rule, matching the template's wording. `examples/notes-app/.gitignore`, which has no such rule because the example commits its profile: add the same path directly after the `.claude/settings.local.json` rule, with a comment saying the file holds one machine's additions to the committed profile and is never committed.
- [ ] `examples/notes-app/.claude/settings.autonomous.json`: add `/workspace/notes-app/.claude/settings.autonomous.local.json` to `sandbox.filesystem.denyWrite` and `Edit(//workspace/notes-app/.claude/settings.autonomous.local.json)` to `permissions.deny`, each at the position the generator gives it after the profile's own entry.
- [ ] Same file: replace the `UNATTENDED SETTINGS PROFILE`, `COMPLETENESS IS LOAD-BEARING`, `THE PACKAGE MANAGER`, `` `deny` IS A FLOOR ``, `THE BROWSER HALF`, `THE ALLOWED TOOL SET`, `THE PORT PROBE` and `THE PHASE'S OWN HELPER SCRIPTS` `_README` lines with the templates' new text, and add the new path and reason to the write-protection `_README` line, with this repository's paths replaced by the example's `/workspace` paths as the README's three clauses describe.
- [ ] `examples/notes-app/README.md`: add this re-render to the profile's history and update each figure by running the README's own `grep` commands from `examples/notes-app/`.

**Verification:**

- `jq empty examples/notes-app/.claude/settings.autonomous.json` exits 0.
- Every figure in the README's profile paragraph equals the output of the command listed beside it.
- `git diff --name-only -- examples/notes-app` lists only the three example targets.
- `grep -n '/Users/' examples/notes-app/.claude/settings.autonomous.json` finds nothing.
- Re-running the story index's D1, D5 and D6 entries reaches the example's profile only at sites the register lists.

**Deviations from plan:** The Goal's "neither disagrees with what the CLI now generates" is not fully met, because the Work list is limited to this branch's changes and was implemented as written. A real `init --upgrade` from the built CLI, run in a throwaway copy of the example and passed through the README's three clauses, matches the example on all eight replaced `_README` lines and on the new local-file clause and entries. It still differs on drift that predates this branch, left alone here: the render adds `attribution`, the `COMMIT ATTRIBUTION IS OFF` `_README` line, `Bash(git commit --amend:*)` in `deny`, the `scripts/review-sweep.sh` allow, `Edit` and `denyWrite` entries, and the `.git/HEAD`, `.git/refs/heads` and `.git/packed-refs` run-copy protections, and the `FOUR COMMANDS RUN OUTSIDE THE SANDBOX` and write-protection `_README` lines also differ, their wording not compared beyond the new clause; the example alone carries `Bash(git commit:*)` in `allow`.
