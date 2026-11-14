### 1. `test-fix-plan-writer` and `ui-tests-plan-writer` may still reject a Should Fix or Nice to Have under `## Rejected findings`

**Files:**
- `plugin/agents/test-fix-plan-writer.md` (`## Revision mode`) — "apply only its Must Fix items, re-run"
- `plugin/agents/ui-tests-plan-writer.md` (`## Invocation contract`, the revision paragraph) — "apply only the Must Fix items to the relevant file(s)"

**Problem.** The task prompt's rule 2: *"A plan writer re-dispatched after a failing round applies (or rejects) the round's Must Fix items and never acts on a Should Fix or Nice to Have item, whichever gate's file it sits in."* Recording a rejection counts as acting on an item. That is why Task 2's `plugin/instructions/plan_review_rounds.md` → `## The writer's revision` item 3 says: *"Never apply, record under `## Rejected findings` or name in the revision note a Should Fix or Nice to Have item"*.

Those two writers do not follow `## The writer's revision`: neither cites `plan_review_rounds.md`. The story's scope register says so for `test-fix-plan-writer` (row 9: *"this writer cites no shared module, so its own sentence is its only statement of rule 2"*). Each of them still carries the shared recorded-rejection block, unchanged:

> **A reviewer finding you judge wrong is resolved or recorded — never only answered in your return.** Record it as one line of a `## Rejected findings` section at the END of the index …

That block applies to any reviewer finding, not just a Must Fix. Both writers receive FAIL files that also contain `## Should Fix` / `## Nice to Have` sections: the architecture gate's sub-case (c) file, and the UI-test plan review file. So when a writer judges one of those Should Fix items wrong, its own definition tells it to record the item under `## Rejected findings`. Its revision sentence ("apply only … Must Fix items") limits what it *applies*, not what it *rejects*.

The story plan kept the block unchanged (rows 41–42) because "only a Must Fix reaches it" under `## The writer's revision`. That holds for `task-plan-writer` and `user-review-fix-plan-writer`, which cite that section. It does not hold for these two writers. Rule 2 is therefore still not stated for two writers the prompt puts in scope (*"plus the writers those loops re-dispatch"*). The README `cli/templates/state-dir/test_fix_plan_reviews/README.md` now describes a contract that this writer's definition does not enforce.

**Fix.** Leave the shared block byte-identical. It is shared by four writers, and rows 39–42 keep it. Instead, close the gap in each writer's own revision sentence:

1. `plugin/agents/test-fix-plan-writer.md` → `## Revision mode`. Replace
   `apply only its Must Fix items, re-run`
   with
   `apply only its Must Fix items — never apply, or record under `## Rejected findings`, a Should Fix or Nice to Have item — re-run`

2. `plugin/agents/ui-tests-plan-writer.md` → the revision paragraph under `## Invocation contract`. Replace
   `apply only the Must Fix items to the relevant file(s).`
   with
   `apply only the Must Fix items to the relevant file(s), and never apply, or record under `## Rejected findings`, a Should Fix or Nice to Have item.`
   Leave the next sentence, `Same shape as the `task-plan-writer`'s revision mode.`, unchanged. It stays true after this edit.

Both edits are prose and need no test run.
