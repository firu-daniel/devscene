# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix

1. **`task_5_plan.md` (and the story index `feat_structured_outputs_branch_review_story_plan.md` → `## Context`) — the non-halting `error` route depends on a reading `agent_return_contract.md` does not support, so goal 3 is not secured**
   The plan's whole guarantee for goal 3 is that a statistics dispatch site can name its *own* `error` route. The module does not say that. `plugin/instructions/agent_return_contract.md` → `## A return that fails the check` reads: *"After the **third** consecutive failing return for the same dispatch, take the dispatching section's `error` route: `--outcome error` where that section passes outcomes to `flow-walker.sh`; otherwise the flow's blocker route — `<escalate>` where the flow binds it, else stop and report."* The colon defines what the `error` route *is*. There is no "where the section names none" condition. Neither orchestration core runs on `flow-walker.sh`, and both bind `<escalate>`. So under the module as written, a third failing `statistics-plan-writer` return at `plan_orchestration_instructions_core.md` → `### D.1` and at `user_review_fixes_instructions_core.md` → `### D.1` is `<escalate>`d, whatever sentence the site adds. That halts the flow, against the task prompt's goal 3 (*"A failed statistics write still never halts a flow"*). It also contradicts the core's own `<escalate>` row (*"Phase D has exactly one `<escalate>` site"*). Task 5 then forbids the one edit that would close the gap (*"Add no other line to that module"*). Task 6 would write the same unsupported claim into the decision record.
   **Raised against:** "`agent_return_contract.md` → `## A return that fails the check` sends a third failing return down *"the dispatching section's `error` route"*, which falls back to the blocker route only where a section names none." (story index); "Add `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_fixes_instructions.md` and `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions.md` to … `## Who may cite this`. Add no other line to that module." (`task_5_plan.md`)
   **Must hold:** At the end of Task 5, the text an orchestrating session follows sends a third consecutive failing `statistics-plan-writer` return at every dispatch site, both cores' `### D.1` included, to a non-halting report-and-continue route. That outcome must follow from the module's own `## A return that fails the check` wording, not from a sentence at the site that the module's wording overrides. The story index's Context and Task 6's record must describe the mechanism that actually holds.
   **Fix:** In `task_5_plan.md`, add `agent_return_contract.md` → `## A return that fails the check` to `### Targets`. Add a `**Work:**` item that amends that section, which the orchestrating session acts on at run time, so the module allows it under `harness-runs/lessons.md`'s shared-module rule. The amendment lets a dispatching section that names its own `error` route have that route taken, before the `flow-walker.sh` / blocker-route fallbacks. Keep it within the 5-bullet ceiling, for example by folding it into the existing roster bullet. Add a `**Verification:**` bullet that reads the amended sentence. Then correct the story index's Context paragraph *"A failed statistics write still never halts (goal 3)"*. Also correct the module row 8 owning-task cell of `## Scope register` so it names the new edit.

2. **`task_4_plan.md` — the autonomous fork's opening paragraph keeps the old `## Questions` prose form, and the task's own Verification cannot pass**
   `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`'s opening paragraph lists, among the things it does not restate, *"the `## Questions` handling (step 6)"*. That sentence is not in Task 4's `### Targets` list for this file, and no `**Work:**` item touches it. So after Task 4 this fork still names the retired `## Questions` return section. That breaks the task prompt's goal 2 (*"No caller parses these agents' returns line by line in the old prose form"*). It also makes Task 4's own Verification bullet (`grep -n '## Questions' … plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md …` has no hit) impossible to satisfy within the task's targets.
   **Raised against:** "`plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` — the `<ask>` binding row; the *"Both bindings resolve to the **same** file-based channel …"* paragraph; the **Headless / watcher entry point** bullet's trigger clause; the convergence-summary bullet's counts; Override 5's **Trigger** paragraph."
   **Must hold:** Every sentence of the autonomous fork that names `user-review-fix-plan-writer`'s retired `## Questions` return section is in Task 4's `### Targets`. Each gets a `**Work:**` instruction moving it onto the `questions` outcome / field form, so the task's `## Questions` no-hit verification is satisfiable inside its own targets.
   **Fix:** Add the opening paragraph's *"the `## Questions` handling (step 6)"* clause to the autonomous-fork line of `### Targets`. In the forks `**Work:**` bullet, reword it to name the writer's return handling: for example *"the writer's return handling (step 6)"*, matching the supervised fork's not-redefined line.

3. **`task_2_plan.md`, `task_3_plan.md`, `task_4_plan.md` — the `## Questions` greps over `plan_orchestration_instructions_autonomous.md` claim results the tree cannot give**
   The autonomous fork's closed list has two more `## Questions` hits that these bullets do not account for:
   - **Entry 14** (*"… on a writer return that also carries `## Questions` it fires before the `<ask>` park."*) is about `ui-tests-plan-writer`. It is outside this branch's five agents, and no task owns it.
   - **Entry 13** (*"… before any `## Questions` park …"*) is Task 4's and is still present at Task 2's and Task 3's end.

   The bullets fail as follows:
   - **Task 2:** its Verification says the grep "shows only the `skeptic-reviewer` clauses … one in `### C2.1`, one in `### D.2`'s **Review questions** bullet and one in the autonomous observation bullet". In fact entries 13 and 14 also hit.
   - **Task 3:** its Verification says the grep "has no hit". Entries 13 and 14 still hit.
   - **Task 4:** its Verification includes this file in a "has no hit" grep. Entry 14 still hits.

   Each task's `### Targets` says *"No other sentence of this file"*. So an implementer either fails its own verification or edits a sentence no task owns.
   **Raised against:** "`grep -n '## Questions' plugin/instructions/plan_orchestration_instructions_core.md plugin/instructions/plan_orchestration_instructions_autonomous.md` has no hit." (`task_3_plan.md`)
   **Must hold:** Every `**Verification:**` bullet states an outcome the tree can give at that task's end, with the task editing only its own `### Targets` sentences. Hits from sentences another task owns, or that no task owns because they are outside the branch's five agents, are named as expected rather than claimed absent.
   **Fix:**
   - In `task_2_plan.md`, list closed-list entries 13 (Task 4's) and 14 (`ui-tests-plan-writer`'s, out of scope) among the expected hits.
   - In `task_3_plan.md`, state that the only hits left are entries 13 (Task 4's) and 14 (out of scope).
   - In `task_4_plan.md`, either take `plan_orchestration_instructions_autonomous.md` out of the no-hit grep and grep entry 13's sentence alone, or state that entry 14 is the one expected hit.

4. **Story index (`feat_structured_outputs_branch_review_story_plan.md`) → `## Scope register` — derivation entry P2 reaches ledger rules that are not rows (disposition (i))**
   Re-walking P2 (first step `grep -nE '^## |^- ' harness-runs/lessons.md`; decision rule *"a rule is reached when it sits under `## Agent prose`, or names a rename, an agent's return, an outcome or a shared instruction module"*) reaches two rules that have no row:
   - `harness-runs/lessons.md` → `## Adopter-facing documentation` → *"Name an adopter-facing surface with the term adopters already arrive with … rename the prose and add an alias for the flag, and never the configuration key, tool name, check id or any other wire identifier."* This rule names a rename.
   - `harness-runs/lessons.md` → `## Evidence and measurement` → *"A decision rule's outcome is a proposal to the maintainer, not a settled future …"* This rule names an outcome.

   The closure invariant (*"every site any of the four entries reaches appears as a row below"*) therefore does not hold. Command entries C1 and C2, re-run verbatim, and procedure P1, re-walked, reach no site outside the rows.
   **Raised against:** "**Closure invariant:** every site any of the four entries reaches appears as a row below."
   **Must hold:** Every site P2's own decision rule reaches appears as a row of the register, with a disposition and reason.
   **Fix:** Add a row for each of the two rules above, `Evidence` `P2`, each most likely `no-change` with its reason. The first constrains adopter-facing renames, and this branch renames no adopter-facing surface. The second constrains a measurement verdict, and this branch makes none. Alternatively, narrow P2's decision rule so it plainly excludes them, and say so.

## Should Fix

- **`task_4_plan.md`** adds a new `<escalate>` site at the core's `## Flow` step 6: the writer's `blocker`, or its third failing return. It updates the core's `<escalate>` row and the autonomous fork's *"Both bindings resolve …"* paragraph. It does not update the autonomous fork's `<escalate>` binding row. That row (*"It covers the core's **agent/flow-blocker** sites — no user-review file at `## Flow` step 2, and the one five-round cap …"*) then lists the core's sites incompletely. Consider adding that row to the targets.

## Nice to Have

- The story index states the plan "found no point where the record and the task prompt disagree", then explains how it read *"The literal a caller matched before becomes the outcome value it routes on"*. That reading is sound, but the task prompt asks that a reading the record does not settle be said in the plan. The Context already does this, so no change is needed. It is noted only so Task 6's wording stays a record of a choice, not a new rule.
