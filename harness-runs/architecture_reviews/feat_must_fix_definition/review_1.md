# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_6_plan.md` — the reviewer's new check still lands before the sample that overrides it.** Rule source: `.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent` ("Contract before consumer, always").
   Task 6 now calls itself the owner of the placement contract, but `plugin/agents/review-plan-reviewer.md` → `## Read first` names `sample_code_review/finding_1.md` as "the **format specification** you validate against" and says "Where a check below and a fixture disagree, the fixture wins". Until Task 11 adds the two fields to that sample, the new `### Must Fix entries (Must Fix)` check disagrees with the file that overrides it. The finished branch is coherent; the commits from Task 6 up to Task 11 are not.
   **Raised against:** "It edits no producer and no sample."
   **Must hold:** The format fixture `review-plan-reviewer` defers to shows `**Class:**` and `**Failure:**` no later than the task that makes the reviewer require them.
   **Fix:** Move the `sample_code_review/finding_1.md` edit from Task 11 into Task 6, adding that file to Task 6's targets and removing it from Task 11's. Update the register row for that sample to name Task 6.

2. **`task_4_plan.md` — `plan_review_rounds.md` would restate routing its readers do not act on.** Rule source: `.claude/context/plugin.md` → `## Writing agent prose` ("Each rule is stated once"), and `<state_dir>/lessons.md` → `## Agent prose` ("A shared instruction module carries only what its runtime reader acts on").
   The readers of `## The Must Fix entry` are the reviewers that write entries. They act on the entry's shape and on the rule that a refused file is replaced, which Task 4 already puts in `## The round file`. What happens to a refused gate next is owned by the walker's `ROUNDS` header (Task 2) and by the user-review core's **The round's set** paragraph (Task 12), so this sentence becomes a third statement of it, on text every plan reviewer loads each dispatch.
   **Raised against:** "the gate is dispatched again within the round, and its third refusal escalates"
   **Must hold:** `## The Must Fix entry` states what makes an entry or file invalid, and the re-dispatch and escalation route has one owner per flow.
   **Fix:** In Task 4, end the stated check at "is refused and does not reach the writer", and leave the re-dispatch and third-refusal wording to Tasks 2 and 12.
