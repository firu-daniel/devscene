### Task 9 — Read the reviewers' and the UI-test writer's returns in the user-review fix-plan, user-review fix and QA flows

**Goal:** Make the three flows outside planning that dispatch one of the six agents — the user-review fix-plan gates, the user-review fix flow's QA augment, and the supervised QA flow — read the return object through `plugin/instructions/agent_return_contract.md` → `## Reading a return`, route on its `outcome`, and name each field in the citation form.

**Depends on:** Task 1 (`## Reading a return`, `## A return that fails the check`, `## Citing a field`) and Tasks 3 and 5, which declare the fields read here:

- `business-parity-reviewer` and `architecture-reviewer`, plan-review sub-case (b): an `outcome` of `PASS` or `FAIL`, each carrying `` `business-parity-reviewer.findings_file` `` / `` `architecture-reviewer.findings_file` ``; `FAIL` also `must_fix_count`; `blocker` with `blocker`.
- `ui-tests-plan-writer`, augment and initial-write modes: `returned` with `` `ui-tests-plan-writer.ui_test_index` ``, `` `ui-tests-plan-writer.ui_test_files_dir` ``, `` `ui-tests-plan-writer.tests_count` ``; `no_ui` with `` `ui-tests-plan-writer.reason` ``; `questions` with `` `ui-tests-plan-writer.questions` `` and, when the augment wrote files before asking, the same three plan fields; `blocker`.

**Where this task stops.** `user-review-fix-plan-writer`'s own `## Questions` and every fork site that routes on it (`plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`) are another agent's return and #380's. The planning flow's readers are Tasks 6–7; the implementation flow's are Task 8.

### Targets

- `plugin/instructions/user_review_fix_plan_writing_instructions_core.md`
- `plugin/instructions/user_review_fixes_instructions_core.md`
- `plugin/instructions/user_review_fixes_instructions_autonomous.md`
- `plugin/instructions/user_review_fixes_instructions_semi_autonomous.md`
- `plugin/instructions/qa_test_instructions.md`

**Work:**

- [ ] `user_review_fix_plan_writing_instructions_core.md` → `## Flow` steps 7 and 8: **Parse the return:** read it per `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return`, record the `outcome` and the gate's `findings_file` (citation form) on `PASS` and on `FAIL`. The held-binding paragraph under step 7 (**The round's set — due gates, join, held binding.**): a gate's `blocker` outcome — and a return the module's check failed three times — is the held binding, `<escalate>`d once at the join as today. The **Round close** text's `<findings_file>` stays bound from those fields.
- [ ] `user_review_fixes_instructions_core.md` → `### QA.0 Resolve the round suffix, then augment the UI-test plan` step 2: read the writer's return per `## Reading a return`; the `no_ui` outcome skips QA.1+ (record the Done-summary line as today); the `questions` outcome routes the `questions` items through `<ask>`; on `returned`, bind `<ui_test_index>` / `<ui_test_files_dir>` from the writer's fields; a `blocker` outcome, or the third failed check, goes to `<escalate>`.
- [ ] `user_review_fixes_instructions_autonomous.md`: the `<ask>` row (the writer's `questions` outcome) and `## Override L — commit the QA.0 UI-test plan augment (autonomous fork only)` → **Trigger.** (fires when the return carries `` `ui-tests-plan-writer.ui_test_index` `` — a `returned` outcome, or a `questions` outcome that carries it — before the questions are routed, as today).
- [ ] `user_review_fixes_instructions_semi_autonomous.md`: the `<ask>` row (surface the writer's `questions` items, verbatim).
- [ ] `qa_test_instructions.md` → `### 1. Ensure a UI-test plan exists` step 4: read the writer's return per `## Reading a return`; report the three plan fields on `returned`; on `no_ui`, tell the user there is nothing to QA with `` `ui-tests-plan-writer.reason` `` and stop; on `questions`, surface the items verbatim and stop until answered; on `blocker` or the third failed check, stop and report. Add each core's pointer, and only the cores' and `qa_test_instructions.md`'s — Task 1's roster lists exactly these three of this task's files.

**Verification:**

- `git grep -nE 'verdict: (PASS|FAIL)|no_ui: true|ui_test_index:|## Questions|findings_file:' -- plugin/instructions/user_review_fix_plan_writing_instructions_core.md plugin/instructions/user_review_fixes_instructions_core.md plugin/instructions/user_review_fixes_instructions_autonomous.md plugin/instructions/user_review_fixes_instructions_semi_autonomous.md plugin/instructions/qa_test_instructions.md` prints only lines about `user-review-fix-plan-writer`, `test-fix-plan-writer`, `qa-tester` or another agent outside the six, and none reading a return of the six.
- Every `` `<agent>.<field>` `` citation in the five files names a property the story index `## Context` field table lists for that agent.
- `git grep -ln 'agent_return_contract' -- plugin` now lists exactly the module and the six roster members of its `## Who may cite this`.

**Deviations from plan:**

- `user_review_fixes_instructions_core.md` → the context-discipline "Reviewers return …" bullet also gained the `architecture-reviewer` exception (mirroring Task 8's edit to `plan_orchestration_instructions_core.md`), since this flow reaches that reviewer through the cited G.2 gate and the first Verification grep would otherwise print a line about one of the six.
- `user_review_fixes_instructions_autonomous.md` → the `<escalate>` / `<ask>` reroute's closed list gained the writer's `blocker` outcome and its third failed routing check, because the core's QA.0 now routes both to `<escalate>` and that list is closed.
- `user_review_fix_plan_writing_instructions_core.md` → the two run-mode-gate sentences ("the join counts it exactly as a `verdict: PASS`") now read "an `outcome` of `PASS`", for the same Verification grep.
- Verification bullet 1: `user_review_fixes_instructions_autonomous.md` → `(a) Fix-plan convergence gates` keeps "a `verdict: FAIL` line" — it describes the round file's content (`plan_review_rounds.md` → `## The round file`), not a return. The QA flow's `ui_test_index:` hit is the `qa-tester` dispatch argument.
- Verification bullet 3: `git grep -ln 'agent_return_contract' -- plugin` lists the six roster members only; the module does not contain its own name, so it is not listed. Matches the roster in `## Who may cite this`.
