# Architecture review — round 2

verdict: PASS
review_mode: converging

## Should Fix
1. **`task_4_plan.md` — the new header choice makes the helper's header title and a doc comment inaccurate.** The new **Work:** bullet says to *"Add a numbered choice to the module header, beside choices 1–8"*. `cli/test/helpers/watcher.mjs`'s header section is titled `## Eight non-obvious choices`, so a ninth choice makes that count wrong. The stub also goes in `<recorderDir>/bin` and is put first on the watcher's `PATH`, but the `RECORDER_DIR` doc comment says the recorders' directory is *"never on the machine's `PATH`"*. The comment means the operator's `PATH`, not the child's, so it still holds as meant, but it now reads like a contradiction. `.claude/context/cli.md` → `## What "done" means here` says a change either satisfies its module's header or amends it in the same edit. The task should say to retitle the section and to qualify that comment. This is a stale count and a comment, so it is not a Must Fix (`finding_grades.md` → `## Never a Must Fix on its own`).
