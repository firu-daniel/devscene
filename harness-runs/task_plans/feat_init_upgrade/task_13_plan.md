### Task 13 — Update the CLI package and template READMEs

**Goal:** Make the READMEs shipped with the templates state the route and files this branch adds.

**Depends on:** Task 10, for the shipped command, and Task 3, for the ignore rule.

The story index's `## Scope register` rows 62, 69 and 70 are this task's sites.

### Targets

- `cli/templates/scripts/README.md`
- `cli/templates/claude/README.md`
- `cli/templates/repo/README.md`

**Work:**

- [ ] `cli/templates/scripts/README.md`: where the outer-loop family's refresh command is given, replace the fenced `npx devscene init --force` with a fenced `npx devscene init --upgrade`, and say that this family is replaced when its bytes differ while the wrapper family stays as written.
- [ ] `cli/templates/claude/README.md`: in the paragraph on the profile and its fragments, add that `.claude/settings.autonomous.local.json` is an adopter file rather than a template, may only add entries to the four lists, and is merged at render time.
- [ ] `cli/templates/repo/README.md`: in the paragraph on the managed ignore block, name the local additions file among the machine-local files it ignores.

**Verification:**

- `grep -n 'init --upgrade' cli/templates/scripts/README.md` finds the fenced command on a line of its own.
- Re-running the story index's D2 entry reaches `cli/templates` only at sites the register lists.
