### Task 13 — Update the CLI template READMEs and re-run statements

**Goal:** Make the READMEs, workflow comments and script text shipped with the templates state the route and files this branch adds.

**Depends on:** Task 10, for the shipped command, and Task 3, for the ignore rule.

The story index's `## Scope register` rows 62, 69, 70, 88, 89, 92, 95, 97, 98 and 105 are this task's sites. Replace words in place, and change no executable statement other than the two watcher message strings below. The self-adopted copies under `scripts/` are not this task's: the register's rows 96, 99 and 100 record why.

### Targets

- `cli/templates/scripts/README.md`
- `cli/templates/claude/README.md`
- `cli/templates/repo/README.md`
- `cli/templates/repo/mcp.retrieval.json`
- `cli/templates/github/workflows/devscene-trigger.yml`
- `cli/templates/github/workflows/devscene-control.yml`
- `cli/templates/github/workflows/devscene-run.yml`
- `cli/templates/scripts/task-offer-check.sh`
- `cli/templates/scripts/autonomous-watcher.sh`

**Work:**

- [ ] `cli/templates/scripts/README.md`: where the outer-loop family's refresh command is given, replace the fenced `npx devscene init --force` with a fenced `npx devscene init --upgrade`, and say that this family is replaced when its bytes differ while the wrapper family stays as written.
- [ ] `cli/templates/claude/README.md`: in the paragraph on the profile and its fragments, add that `.claude/settings.autonomous.local.json` is an adopter file rather than a template, may only add entries to the four lists, and is merged at render time. `cli/templates/repo/README.md`: in the paragraph on the managed ignore block, name the local additions file among the machine-local files it ignores.
- [ ] `devscene-trigger.yml` and `devscene-control.yml`, **WHO WRITES IT**: keep `init --force` after a `.bak` as the workflow's own route, and stop saying it shares the scripts' re-run contract. `devscene-run.yml`, the comment on the `deliver` step: the scripts that lack the verb are ones not yet brought current by `init --upgrade`.
- [ ] `task-offer-check.sh`, **TWO SETTLED STATES**: name `init --upgrade` as the upgrade route for every outer-loop script. `autonomous-watcher.sh`: in the `PLANNING_DRIVER_OFF_REASON` message and the `run analytics` log message, change `` `devscene init --force` rewrites it `` to `` `devscene init --upgrade` rewrites it ``.
- [ ] `cli/templates/repo/mcp.retrieval.json`, `_comment_docs_retrieval`: say that turning retrieval on after the profile was written needs `init --upgrade` to reach it.

**Verification:**

- `grep -n 'init --upgrade' cli/templates/scripts/README.md` finds the fenced command on a line of its own.
- `jq empty cli/templates/repo/mcp.retrieval.json` exits 0.
- Re-running the story index's D2, D5 and D6 entries reaches `cli/templates` only at sites the register lists, and each `change` row's site now states the new route.
