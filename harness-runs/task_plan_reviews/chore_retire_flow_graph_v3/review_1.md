# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix
1. **Story index (`chore_retire_flow_graph_v3_story_plan.md`) → `## Scope register`: no derivation entry reaches a site this branch makes false (disposition ii).** Raised in round 0 as Should Fix 1. It is still neither resolved in the plan nor recorded under `## Rejected findings`.
   - **The site.** `docs/watcher.md` → the paragraph opening **Why only the `yes` rows carry a profile entry, and why that is not the reachability answer.** It still says *"except the two graphs, which are read and never run"*.
   - **Why it becomes false.** Task 9 merges the shipped-scripts table's two `flows/…` rows into one, so the paragraph's count no longer holds.
   - **Why the register misses it.** Re-running entry A verbatim and entry B's first step reaches no line of it.
   - **What that entry is.** The phrase appears only on files that are already rows (rows 6 and 19) and on this paragraph.
   - **Sites newly reached:** `docs/watcher.md` → that paragraph.
   - **Corrected entry A**, strictly wider: add `|two graphs` to its `-E` alternatives. The paragraph then gets a `change` row owned by Task 9, which already targets `docs/watcher.md`. Task 9's Work should then cover it.
   - **Grade.** Should Fix: the sentence describes the shipped set, and no step fails.
2. **`task_6_plan.md`: the contract does not say whether the revision-note clauses of check 6 still run when the step-2 table yields no backticked path.** Raised in round 0 as Should Fix 2. Still unaddressed.
   - **What the bash checker does.** In `scripts/check-flow-graph.sh` → `run_checks`, the `revision_note` checks sit outside the `if [ -z … ]` / `else` on the table. They run whatever the table yielded.
   - **The test it affects.** A port of that behaviour gives the document-side case *"the step-2 table's backticks stripped"* two findings: the *"refusing to pass"* one, plus `findings-folder-in-core: revision note '<dir>' is not in <core> ## Setup step 2 table`.
   - **What the plan says.** The case only says it *"asserts its 'refusing to pass' finding"*.
   - **Fix.** State the full expected list for that case, and whether the revision-note clauses run when the table is empty.
3. **`task_6_plan.md`: two contract clauses have no case, although the bullet promises "one per clause".**
   - **The rule.** `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here` requires *"one case per clause it enforces"*.
   - **First missing clause.** Check 7's *"A graph with no `iteration` counter has path `counters` and reason `cap-matches-core: graph has no counters.iteration`"*. It has no case. A loaded graph cannot drop the counter that `plan_round` names, but `dataclasses.replace` on the public, frozen `FlowGraph` can.
   - **Second missing clause.** *"A missing owner document … reads as empty"*: no document-side case deletes a document outright. Only a section or line is changed.
   - **Fix.** Add both cases, or say in the suite header, under *"Deliberately not covered"*, why each is left out.
4. **`task_6_plan.md`: the graph-side cases say each asserts *"the exact single `Violation`"*, but the contract gives the absent-flow case two.** *"A flow `CORE_FOR_FLOW` lacks"* yields two violations, both with path `flow`: one `findings-folder-in-core` and one `cap-matches-core`. The bullet lists exceptions for the revision-note case (both findings) and the cap case (one per anchor), but not for this one. State that the absent-flow case asserts both.

## Nice to Have
1. **`task_9_plan.md`**: the **Decision-record rule** says each decision's *"**Decision**, **Reason** and **Cost** text stays as decided"*. Yet the Work edits `### Item 2` → **Cost.** in place, as live text. Raised in round 0 and still unaddressed. Name Item 2's **Cost.** as the rule's one exception, so the rule and the Work bullet agree.
