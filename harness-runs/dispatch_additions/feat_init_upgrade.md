## [A · Task 3 · cli · iter 0] → layer-implementer  (#4)
- **added:** `context_notes:`
- **verbatim:** context_notes: An earlier dispatch of this same task left uncommitted changes in the working tree and ended without a return object (`git status --short`).
- **why the agent could not derive it:** the task file and story index do not record that dispatch #3 of this task already ran and returned no return object; only the session transcript holds that

## [A · Task 11 · cli · iter 0] → layer-implementer  (#13)
- **added:** `context_notes:`
- **verbatim:** context_notes: An earlier dispatch of this same task left uncommitted changes in the working tree and ended without a return object (`git status --short`).
- **why the agent could not derive it:** the task file and story index do not record that dispatch #12 of this task already ran and returned no return object; only the session transcript holds that

## [D · docs fix · general · iter 0] → layer-implementer  (#51)
- **added:** `outside the sanctioned form`
- **verbatim:** Fix three stale passages in `docs/cli.md`, at the operator's request. There is no task file for this unit. Change only `docs/cli.md`, and do not commit. 1. The bullet "`--force` upgrades `create-if-absent` only" (§3): its sentences "One route replaces an artifact with **no `--force` at all**" and "So the whole of what the table permits is:" must account for `init --upgrade`. Source: harness-runs/task_plan_reviews/feat_init_upgrade/review_4.md, Must Fix 1 ("Must hold"). 2. The `command-permissions` bullet (§7): "carrying the plugin-root entries forward" must carry the local-entry exception. Keep the check's printed remedy as it is. Source: the same file, Must Fix 2 ("Must hold"). 3. The bullet "**Every wrapper anchors itself, then forwards its arguments.**" (§5): "Both families are `create-if-absent`, so an already-wired repository picks up this placement only through `init --force`" must state the route for each family as the code has it. Take every behaviour you state from the shipped code under `cli/src/upgrade/`, `cli/src/generators/` and `cli/src/core/writer.ts`.
- **why the agent could not derive it:** no governing instruction defines this dispatch; the operator asked for it after the Phase D completion check halted, and no plan or review file assigns the work
