# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix

1. **Story index (`feat_structured_outputs_branch_review_story_plan.md`) → `## Scope register`: derivation entry P2 reaches a ledger rule that has no row (disposition (i))**
   I re-walked P2. Its first step is `grep -nE '^## |^- ' harness-runs/lessons.md`, and its decision rule reads *"a rule is reached when it sits under `## Agent prose`, or names a rename, an agent's return, an outcome or a shared instruction module"*. That walk reaches one rule that is not a row:
   - `harness-runs/lessons.md` → `## Evidence and measurement` → *"Grade a write probe on what reached the disk, never on the call's exit status. "Call succeeded, nothing on disk" is an outcome of its own and never reads as "refused"."* This rule names an outcome. Row 81 was admitted for the same reason: the decision-rule rule *"A decision rule's outcome is a proposal to the maintainer …"* is a row because it names an outcome.

   I also re-ran command entries C1 and C2 verbatim from the checkout root, and re-walked procedure P1. Every site they reach is already a row (rows 1–73). So the closure invariant (*"every site any of the four entries reaches appears as a row below"*) fails on this one site only.
   **Raised against:** "**Closure invariant:** every site any of the four entries reaches appears as a row below."
   **Must hold:** Every site that P2's own decision rule reaches appears as a row of the register, with a disposition and a reason. Alternatively, P2's decision rule plainly excludes that site.
   **Fix:** Add one row for `harness-runs/lessons.md` → `## Evidence and measurement` → *"Grade a write probe on what reached the disk …"*, with `Evidence` `P2, names an outcome` and `Disposition` `no-change`. A suitable reason: the rule grades a write probe's result, and this branch writes and grades no probe. Or narrow P2's decision rule so it reaches only rules about an agent's or a script's routed outcome, and say so. Then re-check rows 79 and 81 against the narrowed rule.

## Should Fix

- **`task_4_plan.md`** (repeated from round 0, not acted on). Task 4 makes the fix-plan core's `## Flow` step 6 a new `<escalate>` site: the writer's `blocker`, or its third failing return. Task 4 updates the core's `<escalate>` row and the autonomous fork's *"Both bindings resolve …"* paragraph. It does not update the autonomous fork's `<escalate>` binding row in `user_review_fix_plan_writing_instructions_autonomous.md`. That row still reads *"It covers the core's **agent/flow-blocker** sites — no user-review file at `## Flow` step 2, and the one five-round cap …"*, which then lists the core's sites incompletely. Consider adding that row's site list to Task 4's targets.
- **`task_4_plan.md`, `task_5_plan.md`.** Each `### Return fields` instruction lists *"the four counts"* as one item, and neither says *"one bullet per property"* as Tasks 1 and 2 do. `cli/test/agent-return-schemas.test.mjs` → `checkOutputContract` reads one top-level bullet per backticked name. A combined bullet such as `` - `valid_must_fix`, `valid_should_fix`, … (integer) `` would register only its first name and fail the tree guard. State one bullet per property, each annotated `(integer)`.
