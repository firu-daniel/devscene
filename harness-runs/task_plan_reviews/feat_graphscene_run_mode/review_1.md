# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **Scope register misses three sites its own procedure entry reaches** — story index (`feat_graphscene_run_mode_story_plan.md`), `## Scope register`.
   Disposition (i). I re-ran the command entry, `git grep -l -E '#484|run loop|[Ss]tep mode|not yet built' -- '*.md' ':!harness-runs/**' ':!examples/**'`. It prints exactly the four files in rows 1 and 6–8. I also re-walked the procedure entry over `graphscene/README.md`. Its decision rule is *"a sentence or row is reached when it … states what the `engine` layer holds"*. That rule reaches these sites, and none of them is a row:
   - `## What it is` prose: "Its `engine` layer holds the vocabulary check, the static checker and the walker, `Walker`, …". Row 1 anchors only the `#484` sentence of this paragraph.
   - `## What it is` prose: "The engine holds the execution rules: the per-set safety contract, the per-node retry and failure settlement, the undelivered breaker, and `execute_set`, …".
   - `## The layers` bullet **New work goes by what it is.**: "A check or a walk over the model, and its rounds, goes in `engine`."

   Task 4's Row 1 work replaces only the `#484` sentence. Once the branch lands, the first two sentences describe an `engine` layer without its run loop. That is descriptive prose, not a failing step, so this is not a Must Fix.
   **Fix:** add one row per site. Either give the two `## What it is` sentences `change` (Task 4) or record why `no-change` holds. Give the bullet `no-change`, with the reason that a run loop is a walk over the model and so already belongs in `engine`.

2. **Task 4's step-mode-unchanged check cannot fail** — `task_4_plan.md`, `**Verification:**`.
   The bullet reads: "`git diff -- graphscene/src/graphscene/facade/cli.py graphscene/src/graphscene/engine/walker.py` is empty. Step mode and the command line are unchanged." With no base, `git diff` shows only the working tree's unstaged changes. Tasks 1–3 are committed before Task 4 runs, so the bullet cannot detect an edit any earlier task made to either file. It only re-checks Task 4's own uncommitted diff.
   **Fix:** compare against the branch's base, so the bullet covers the whole branch. For example, diff against the merge base with the default branch, `git diff dev... -- graphscene/src/graphscene/facade/cli.py graphscene/src/graphscene/engine/walker.py`. Alternatively, state that the check covers this task's diff only.

## Nice to Have

1. **Task 3 asks for a lint and typecheck run the loop already makes** — `task_3_plan.md`, `**Verification:**`: "`bash scripts/python-service.sh --package graphscene lint` and `… typecheck` pass." `.claude/context/graphscene.md` → `## Tests` says the layer's `ruff` and `mypy` checks are part of every unit's run through `commands.typecheck`. Neither is a test run, so this is not a test-run-rule breach. The bullet only adds a second run of checks the unit already gets. Consider saying instead that the unit's `commands.typecheck` run covers both new files under `mypy` `strict`.
