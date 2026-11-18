# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **Task 6 adds a Must Fix check that its own trigger table leaves without a class** — `task_6_plan.md`.
   The third Work bullet creates `### Must Fix entries (Must Fix)` in `review-plan-reviewer.md`: a missing field, or a class or sentence that does not hold, "is a Must Fix against the review". The fourth bullet then spells out the contents of `### Must Fix triggers`, and that list does not name the new section. The task prompt requires "Every checklist trigger still graded Must Fix maps to a class", so an implementer following the list as written ships a Must Fix check with no class. Two listed rows overlap it only in part: "per-finding structure" could cover a missing field, and "a false positive" could cover a class that does not hold. Those rows carry different classes, so the new check has no single class either way. Round 0 raised the same gap against Task 5's table.
   **Raised against:** "**Broken contract** for index structure, per-finding structure, correspondence and the round-suffix match; **Wrong build** for a finding file an implementer cannot act on, a forbidden test run, a false positive, a missed check, an unactionable gate and a parity citation that does not hold."
   **Must hold:** Every check `review-plan-reviewer.md` grades Must Fix after this task, `### Must Fix entries` included, is assigned exactly one class by the task's `### Must Fix triggers` list.
   **Fix:** Name `### Must Fix entries` in the `### Must Fix triggers` bullet under one class, and state that it takes precedence over the per-finding-structure and false-positive rows for a missing or unsupported `**Class:**` / `**Failure:**`. Add a `**Verification:**` bullet that walks each Must Fix check in the finished agent against the table.

## Should Fix
1. **A refused gate re-dispatched through `current` still counts as not running** — `task_2_plan.md`. `render_set` keeps printing a block for a gate with a redo mark, so `current` re-dispatches it, but only the join clears that mark. If a sibling then records its outcome while the refused gate is back in flight, the walker sees nothing outstanding and prints that gate's dispatch again. The planning driver survives this, because the later return overwrites its pending output. An orchestrating session resuming a saved walk would send a duplicate reviewer, and the second return would hit the existing "already recorded" or "not pending" refusal. Add a case for this sequence and state the intended behaviour.

2. **Register row 58's reason does not cover the sentence this branch makes incomplete** — story index (`feat_must_fix_definition_story_plan.md`), `## Scope register`. `docs/watcher.md` describes `flow-walker.sh` as printing the planning loop's next action "(`start`, `next`, `current`)", run by "the orchestrating session of a planning flow". Task 2 adds `check-round-file`, and Task 12 has the user-review fix-plan flow run it. The row's reason speaks only of the driver's behaviour. Nothing fails while the line stays, so this is descriptive only, but the reason should address it or the line should gain the fourth subcommand.
