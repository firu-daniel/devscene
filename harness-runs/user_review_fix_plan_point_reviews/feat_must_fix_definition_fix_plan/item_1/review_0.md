# plugin review — 1. `branch-reviewer` grades a failed two-leg divergence Must Fix with no table row — iteration 0

## Should Fix
1. **A failed Leg 1 now matches two `### Must Fix triggers` rows with different classes** — `plugin/agents/branch-reviewer.md` (`### Must Fix triggers`) — "so each trigger has exactly one class"
   The added row is byte-exact to the plan and correctly placed, but it overlaps an existing own row. `## Output contract` grades a failed Leg 1 as "dropping the intended part is a **Must Fix**". That dropped part is also a reference behaviour present in the source and absent from the diff, which Pass 1 step 5 grades Must Fix and the row "A `<reference_impl>` behaviour missing from the diff, or waived by a fabricated or miscited authorization (Pass 1 step 5), while `phases.parity` is `true`" classes **Wrong behaviour**. The new row classes the same finding **Broken contract**.

   The table's opening sentence promises one class per trigger, but its exclusion rule only removes an own-row trigger from a **group** row, so it does not settle a clash between two own rows. `## Findings format` says a finding "takes that row's class", so `branch-reviewer` reaches either class for the same defect. The reader who goes wrong is `branch-reviewer` on a Leg 1 failure: taking the missing-behaviour row, it writes `**Class:** Wrong behaviour`, while `skeptic-reviewer` (check 4) and `business-parity-reviewer` (failed leg) both give **Broken contract**.

   This is not a Must Fix: `review-plan-reviewer` only requires one of the four classes and `flow-walker-gates.sh` only a non-empty `**Class:**`, so no consumer decision turns on which one is written.

   Confirmed by reading only, no probe run: the two rows and the `## Output contract` bullet in `plugin/agents/branch-reviewer.md`, the sibling tables, `plugin/agents/review-plan-reviewer.md` (`**Class:**` requirement) and `cli/templates/scripts/lib/flow-walker-gates.sh`.

   **Fix:** leave both row cells unchanged, because `harness-runs/user_reviews/feat_must_fix_definition_fix_plan/finding_2.md` names each literally in `OWN_ROWS`. In `plugin/agents/branch-reviewer.md` → `### Must Fix triggers`, append this sentence to the paragraph ending "so each trigger has exactly one class.":

   ```markdown
   A behaviour dropped by a divergence claimed as intentional takes the two-leg row's class, not the missing-behaviour row's.
   ```
