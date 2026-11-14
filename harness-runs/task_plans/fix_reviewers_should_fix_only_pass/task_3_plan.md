### Task 3 — Drop the Should Fix / Nice to Have revision duties from the three plan writers

**Goal:** Make each writer that a plan-review loop re-dispatches act on the round's Must Fix items only (the task prompt's rule 2). Do it by deleting the writers' own paraphrase of the retired duty. No writer restates the new rule if it can point at the shared contract.

**Depends on:** Task 2, which deletes item 3 of `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The writer's revision` and states in its place, once, that the writer acts on the round's Must Fix items only. `task-plan-writer` and `user-review-fix-plan-writer` already cite that section by its unchanged heading `## The writer's revision`. This task removes the words that would contradict it and adds no restatement. `test-fix-plan-writer` cites no shared module (it is not on that file's `## Who may cite this` roster), so its own sentence is its only statement and gets the narrowing in place.

**Leave these alone:**
- **`user-review-fix-plan-writer`'s own classification of the user's observations.** `## Process` sorts them into Valid (Must Fix), Valid (Should Fix) and Nice to Have, with `## Must Fix` / `## Should Fix` / `## Nice to Have` index sections. That is not a reviewer finding, and the task prompt (What changes item 2) keeps it unchanged.
- **The recorded-rejection paragraph** (*"**A reviewer finding you judge wrong is resolved or recorded …**"*) in all three files. It is a byte-identical block shared by five writers. After Task 2 only a Must Fix reaches it (story index `## Scope register`, rows 39–41).

### Targets

- `plugin/agents/task-plan-writer.md`
- `plugin/agents/user-review-fix-plan-writer.md`
- `plugin/agents/test-fix-plan-writer.md`

**Work:**

- [ ] `task-plan-writer.md` → `## Revision mode`, the paragraph opening "Follow `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The writer's revision`:". Delete the clause "apply or reject each Should Fix, ". Keep the rest of that sentence's clauses, in order.
- [ ] `task-plan-writer.md` → `## Revision mode`, first paragraph. Delete the sentence "Add no Nice to Have item unless the orchestrator explicitly told you to." Its exception contradicts rule 2, and the cited `## The writer's revision` now owns the rule.
- [ ] `user-review-fix-plan-writer.md` → `## Revision mode`, the paragraph opening "Follow `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md` → `## The writer's revision`:". Delete the clause "apply or reject each Should Fix, ". Keep "a user-feedback revision writes one note line per feedback item" and "Never act on an `## Incidental findings (not gating)` entry." unchanged.
- [ ] `test-fix-plan-writer.md` → `## Revision mode`, first sentence: "apply only the requested changes" becomes **apply only its Must Fix items**. This matches `ui-tests-plan-writer`'s existing "apply only the Must Fix items". The rest of the paragraph stays: the quality-check rerun, the "never re-diagnose" clause and the `**Authorised by:**` clause.

**Verification:**

- `git grep -nE "apply or reject each Should Fix|Add no Nice to Have item" -- plugin` prints no line.
- `git grep -n "apply only the requested changes" -- plugin` prints only the `user-review-fix-plan-writer.md` line. Its output must be a subset of the story index's `## Scope register` rows (row 8).
- Each of the three files' `## Revision mode` sections is shorter than before, with no new sentence. The change adds no behaviour of its own, so it must not raise any definition's up-front word count (`.claude/context/plugin.md` → `## Writing agent prose`).
- `git grep -n "Valid (Should Fix)" -- plugin/agents/user-review-fix-plan-writer.md` still prints its classification line, unchanged.
