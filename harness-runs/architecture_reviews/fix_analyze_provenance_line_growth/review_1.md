# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_4_plan.md` — the planned test header points at a heading whose roster bars it.** The second sub-bullet of Task 4's header Work item says the header carries **Not a tree guard**, citing `plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8's boundary. That section's own `**Who may cite this.**` paragraph says *"no document beyond this roster may point at this heading"*. The roster names `docs/config.md` and `docs/cli.md` from outside the plugin, but no `cli/test` file. No test enforces the roster (a grep of `cli/test` for the heading finds nothing), and the citation would only sit in a code comment, so no failure sentence can be completed. It grades Should Fix under `plugin/instructions/finding_grades.md` → `## Never a Must Fix on its own`. Suggested change: state the boundary in the header's own words ("reads three fixed files, not a tree, so it owes no `treeGuards` entry") with no pointer to that heading. The other option is to add the new test file to that roster in the same change, but that edits a fourth `plugin` file outside Tasks 1–3's targets.

## Nice to Have

1. **`task_4_plan.md` — slice markers are indented.** In `plugin/commands/analyze.md`, the `**(4a) The conventions documents**`, `**(4b) The \`project\` target` and `**(4c) The review` lines each start with the step's three-space list indent. "The line opening `…`" works only if the implementer trims leading whitespace before matching. Saying so in the Work bullet would remove the ambiguity. This is about wording and is outside the layering lens.
