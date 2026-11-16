# Architecture review — round 2

verdict: PASS
review_mode: converging

## Should Fix

1. **`task_3_plan.md` — "runs no test file" reads as a limit on the unit's test runs.** The new sentence in **What this task does not do.** (*"Task 5 is this library's test task: this task writes and runs no test file."*) uses the wording round 1's Fix prescribed. Task 3 creates `cli/templates/scripts/lib/planning-driver-lib.sh`, and that path matches the `covers` globs of two `treeGuards` entries: `cli/templates/scripts/**/*.sh` and `cli/templates/scripts/**`. So `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 7 still has the unit run those guards. Point 4 says no plan sentence limiting a unit's test runs cancels point 7, so the sentence is not a breach. It could still mislead an implementer. Suggested fix: change the wording to "this task writes no test file of its own".
