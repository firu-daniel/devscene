### 2. Two UI-test agent definitions still name the retired return literals `verdict: FAIL` and `no_ui: true`

**Files:**
- `plugin/agents/ui-tests-plan-writer.md` → `## Invocation contract`, the **Revision (per reviewer findings)** line: "on a `verdict: FAIL` iteration"
- `plugin/agents/ui-tests-plan-reviewer.md` → `## Process` step 0 (**No-plan guard (check FIRST).**): "the writer's `no_ui: true` path"

**The problem.** This branch retires both literals as returns of these two agents. `ui-tests-plan-reviewer` now returns an `outcome` of `FAIL`. Unlike the other three reviewers, its findings file has no `verdict:` line, so `verdict: FAIL` in the UI-test loop can only mean the retired return line. `ui-tests-plan-writer` now returns an `outcome` of `no_ui` and never prints `no_ui: true`. Both sentences sit in durable agent text, which is read on every dispatch, and both still name the old wire form. The story index's first `Top risks:` entry names this risk: a reader left with a retired form of one of these six returns. Neither sentence routes anything today (step 0 tests whether the index exists on disk, and the writer's line only says when it is dispatched), so no consumer acts wrongly on either one. That is why this is Should Fix rather than Must Fix. `cli/test/agent-return-schemas.test.mjs` catches only the `` `<agent>.<field>` `` citation form, so it misses both.

**Fix.**

1. In `plugin/agents/ui-tests-plan-writer.md`, change

   > sent by `${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md` → `## UI-test-plan write loop` step 1 on a `verdict: FAIL` iteration:

   to

   > sent by `${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md` → `## UI-test-plan write loop` step 1 after the reviewer's `FAIL` outcome:

2. In `plugin/agents/ui-tests-plan-reviewer.md` → `## Process` step 0, change "the writer's `no_ui: true` path" to "the writer's `no_ui` outcome".

Neither edit adds words to its definition. No test is owed: both are prose-only edits to agent definitions.
