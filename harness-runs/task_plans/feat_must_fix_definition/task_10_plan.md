### Task 10 — Move the fix-plan writers and `qa-tester` onto the definition

**Goal:** The three agents that assign grades outside a review file use `finding_grades.md`, and each Must Fix finding file they write carries the two fields.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` with the four classes, the failure sentence, `**Class:**` and `**Failure:**`.

### Targets

- `plugin/agents/user-review-fix-plan-writer.md`
- `plugin/agents/test-fix-plan-writer.md`
- `plugin/agents/qa-tester.md`

**Work:**

- [ ] Add a pointer to each file's reading list, `## Read on demand (no auto-loaded context)` in the two writers and `## Read first` in `qa-tester`: `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. `` In the two writers, state that it is read before grading, whatever the observation or failure touches.
- [ ] In `user-review-fix-plan-writer` → `## Process` step 3, replace the three valid-grade bullets with: **Valid (Must Fix)**, **Valid (Should Fix)** and **Valid (Nice to Have)**, each "the observation is real and `finding_grades.md` gives it this grade". A user's observation settles whether the issue is real; the grade still comes from that file. Keep **Invalid** and **Needs clarification** unchanged.
- [ ] In `user-review-fix-plan-writer` → the per-finding file description, and in `## Process` step 5's quality checks, require `**Class:**` and `**Failure:**` directly after the site anchor (after `**Review comments:**` where that line is present) on each file listed under `## Must Fix`.
- [ ] In `test-fix-plan-writer`, reword the `## Must Fix` index bullet to "one entry per failure fixable on the branch". State that a failing test or type check is **Wrong behaviour** and any other failing gate is **Broken contract**. Each `finding_<K>.md` carries `**Class:**` and `**Failure:**` after its `**Failing test:**` line, the sentence naming the gate or test and quoting the failure. Add the check to `## Quality checks before returning`.
- [ ] In `qa-tester` → `### 2. Some tests fail`, require both fields on each per-finding file listed under `## Must Fix`. Keep the rule that a Should Fix alone gives `outcome: FAIL` with `must_fix_count` `0`.

**Verification:**

- `grep -nE 'real and impactful|every fixable failure' plugin/agents/user-review-fix-plan-writer.md plugin/agents/test-fix-plan-writer.md` prints nothing.
- All three files name `finding_grades.md`, and no return field changes in `git diff`.
