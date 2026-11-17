# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix

1. **`task_1_plan.md` — sentences still in the old `qa-tester` return form are missing from `### Targets` and `**Work:**`**
   Task 1 says it moves every `qa-tester` caller onto the return object. For `user_review_fixes_instructions_core.md` it lists only the opening bullet, `### QA.1+`'s two clauses, `### D.2`'s QA bullet and the `## Stop conditions` bullet. Two more sentences in that file describe the old return:
   - The `<escalate>` row of the bindings table: *"**and by the cited `## Phase E — QA testing`** (dev-server start failure, an unmarked per-test `qa-tester` `error:`, the `MAX_QA_ROUNDS` cap)"*.
   - The `## Phase QA` lead note: *"the qa-tester invocation contract, the `verdict: FAIL` → commit-the-QA-review-then-fix-loop sequence"*.

   Task 1's verification will not catch the first one. Its regex `unmarked .?error` needs the word `error` right after `unmarked `, but here the words `per-test \`qa-tester\`` sit between them.

   `plugin/agents/qa-tester.md` has the opposite problem. Two `## How it tests` sentences carry `must_fix_count: 0`: the finding-elements bullet (*"(`## Output contract` → `### 2. Some tests fail`, `must_fix_count: 0`)"*) and the omitted-setup-step sub-bullet. `### 2.` also has the lead-in *"Then return exactly (3 lines):"*. Task 1's own Verification grep (`'verdict: (PASS|FAIL)|must_fix_count:|findings_file:'` over `qa-tester.md`) hits the `must_fix_count: 0` lines. But `### Targets` does not list them, and the Work says *"Keep each sentence's other words; add none"*. The task as written cannot pass its own Verification.
   **Raised against:** "`plugin/instructions/user_review_fixes_instructions_core.md` — the opening *"Reviewers return 1 line …"* bullet, `### QA.1+`'s per-test mark-pass clause and its round-PASS sentence, `### D.2`'s **QA (Phase QA)** bullet's blocked clause, and the `## Stop conditions` bullet"
   **Must hold:** Task 1's `### Targets` and `**Work:**` name every sentence in its files that states `qa-tester`'s old return form (`verdict:` lines, `must_fix_count:` / `findings_file:` lines, an `error:` line in any wording). Its Verification greps match every such wording, including `unmarked per-test … error:`. No Verification bullet requires an edit that the Work does not schedule.
   **Fix:** In `task_1_plan.md`, add the `<escalate>` binding row's Phase E clause and the `## Phase QA` lead note's `verdict: FAIL` clause to the `user_review_fixes_instructions_core.md` target, each with its rewrite. The first becomes an `outcome` of `blocker` or a third failing return; the second becomes an `outcome` of `FAIL`. For `qa-tester.md`, add the two `must_fix_count: 0` sentences (they become `` `must_fix_count` `` of `0`) and `### 2.`'s "(3 lines)" lead-in. Widen the first Verification regex so it also matches `unmarked per-test` (for example, `unmarked [^.]*error`).

2. **Story index (`feat_structured_outputs_docs_qa_story_plan.md`) — Scope register row 5 lists too few sentences for Task 1**
   Row 5 (`user_review_fixes_instructions_core.md`, `change`, Task 1) lists the sentences Task 1 owns in that file. It leaves out the `<escalate>` binding row's *"an unmarked per-test `qa-tester` `error:`"* clause and the `## Phase QA` lead note's *"the `verdict: FAIL` → commit-the-QA-review-then-fix-loop sequence"*. The site is already a row, so this is disposition (iii): the row's reason cell is incomplete. Derivation entry C2's alternative `unmarked .?error` has the same blind spot as Task 1's grep. The file is reached anyway, through other alternatives, so this is not a missing-site finding.
   **Raised against:** "Task 1 (the opening *"Reviewers return 1 line …"* bullet, `### QA.1+`'s mark-pass clause and round-PASS sentence, `### D.2`'s **QA** bullet's blocked clause, the `## Stop conditions` `qa-tester` bullet)"
   **Must hold:** Every register row that enumerates sentences for its owning task lists each sentence in that file that carries the old return form, and matches the owning task's `### Targets`.
   **Fix:** Add the two clauses to row 5's "Owning task or reason" cell, matching Must Fix 1.

3. **Story index (`feat_structured_outputs_docs_qa_story_plan.md`) — Scope register rows 37 and 38 give a false reason for `no-change`**
   Rows 37 and 38 mark `plugin/commands/branch-implement-plan-semi-autonomous.md` and `plugin/commands/branch-implement-user-review-semi-autonomous.md` as `no-change` because each *"dispatches `qa-tester` and reads no return"*. Both files contain the orchestrator instruction *"you do not review specialist output beyond reading the 1-3 line contract each agent returns"*. That sentence tells the session to read each dispatched agent's return, `qa-tester` included, in the old line form. After this branch, no agent returns a 1-3 line contract. That falls inside the scope predicate (*"No caller parses these agents' returns line by line in the old prose form"*) and the constraint *"No caller is left reading a field its agent no longer returns, at the end of any task"*. This is disposition (iii): the rows exist, but their disposition and reason are wrong.
   **Raised against:** "| 37 | `plugin/commands/branch-implement-plan-semi-autonomous.md` | — | C1 | `no-change` | A Phase E summary that dispatches `qa-tester` and reads no return |"
   **Must hold:** Every register row whose file tells an orchestrator to read one of the five agents' returns in the old line form has disposition `change` and an owning task. That task's file lists the sentence in `### Targets` and rewrites it in `**Work:**`.
   **Fix:** In the story index, change rows 37 and 38 to `change` and name an owning `plugin` task. Task 1 is already at 20 points and 5 `**Work:**` bullets, so Task 2 is a natural fit; otherwise split. In that task's file, add both commands' "1-3 line contract" sentence to `### Targets`, with a rewrite saying the orchestrator reads each agent's return object as its dispatching section states.

## Should Fix

- **Story index — derivation entry P1 does not say how a glob is handled.** The task prompt's backticked `plugin/agents/*.md` and `plugin/schemas/*.return.json` are patterns, not paths. P1's traversal ("every backticked repository path") and decision rule do not say whether a glob reaches every file it matches. Re-walked literally, it could reach all 22 agent definitions. State that a glob is not a path, or name the sites it reaches.

## Nice to Have

- **Story index — layer order.** The readiness list ships the `cli` task after the four `plugin` tasks, against the configured order `cli`, `plugin`, `general`. `## Context` argues this, and no dependency link points forward, so this is not a finding. Task 5's file restates the reason, which is enough.
