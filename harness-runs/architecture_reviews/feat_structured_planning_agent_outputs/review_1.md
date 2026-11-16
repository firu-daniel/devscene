# Architecture review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_2_plan.md` — a Verification bullet names a tree guard the task neither creates nor edits.** Source: `plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 4 (*"No plan names a tree guard the task neither creates nor edits … the guard run is the loop's, never the plan's"*; *"every reviewer of one raises a breach as a **Must Fix**"*).
   This round's revision added a Verification bullet to Task 2 that ends by naming `cli/test/untrusted-input-corpus.test.mjs` and saying the grep "keeps the registered `treeGuards` suite … green — point 7's guard run covers it". Task 2's only target is `plugin/agents/task-plan-writer.md`. It neither creates nor edits that suite. Point 7 already selects the guard from the changed path (`plugin/**/*.md`), so naming it in the plan adds nothing, and point 4 forbids it. The grep half of the bullet is sound and should stay: it is a check on the task's own target, not a test run.
   **Raised against:** "which keeps the registered `treeGuards` suite `cli/test/untrusted-input-corpus.test.mjs` green — point 7's guard run covers it."
   **Must hold:** No line of `task_2_plan.md` names a test file or tree guard that Task 2 neither creates nor edits. The check that `plugin/agents/task-plan-writer.md` does not carry the report literal `Untrusted instruction not followed — ` stays, as a grep on that file.
   **Fix:** In Task 2's Verification, keep `` `git grep -nF 'Untrusted instruction not followed — ' -- plugin/agents/task-plan-writer.md` prints nothing: the report literal stays at its two homes only (`untrusted_input.md` and `docs_orchestration_instructions_autonomous.md`) ``. Delete the clause from "which keeps the registered `treeGuards` suite" to the end of the bullet. Do not name any other guard in its place.

## Should Fix
1. **`task_1_plan.md` — the module uses the citing flow's `<escalate>` binding but no placeholder-resolution statement is planned for it.** This carries over from round 0 and is still unaddressed. Source: `.claude/context/plugin.md` → `## The placeholder vocabulary` (*"Two `<…>` vocabularies exist and conflating them is silent"*). Task 1's `## A return that fails the check` routes a third failure to "`<escalate>` where the flow binds it, else stop and report". The plan also says the module "declares no binding". Two things are missing:
   - A **Placeholder resolution.** paragraph under `## Resolved values`, in the form `plugin/instructions/untrusted_input.md` uses for `<ask>`.
   - A statement that `<escalate>` is the citing flow's mode-contract binding, which this module neither declares nor supplies, and that a citer with no `<escalate>` (`qa_test_instructions.md`) takes the stop-and-report arm.

   Add both to Task 1.
2. **`task_4_plan.md` — `plan_review_rounds.md` → `## The round file` would state the reviewers' return fields as bare names.** This carries over from round 0 and is still unaddressed. Source: `.claude/context/conventions.md` → `### Where a new responsibility goes` (*"A responsibility that already has a home does not get a second one"*), read with the story index's decision 3. Task 4 writes "an `outcome` of `PASS` carrying `findings_file` … `must_fix_count`" in bare form. Task 13's citation check therefore cannot see it, so renaming a reviewer's field would leave this sentence stale with no test failing. Either point at each reviewer's `## Return schema` without naming fields, or name them in `## Citing a field`'s form for the four reviewers that cite the section.
