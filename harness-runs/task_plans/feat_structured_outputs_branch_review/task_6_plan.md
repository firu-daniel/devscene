### Task 6 — Record `statistics-plan-writer`'s `not_written` outcome in the decision record

**Goal:** `docs/structured-agent-returns.md` → *An agent's own `error:` return becomes an outcome, never `error`* records the decision this branch took for `statistics-plan-writer`. Its sentence naming that agent among those that *"return `error:` today"* stays true.

**Depends on:** Task 5, which gave `statistics-plan-writer` the outcomes `written` and `not_written`, the latter carrying its cause in a `cause` field. Every caller now continues past a `not_written` return and past a third return that fails the routing check: the plan and user-review orchestration cores' `### D.1`, `plugin/instructions/code_review_instructions.md` step 6.2, and `## Phase 3` step 2 of `plugin/instructions/code_review_fixes_instructions.md` and of `plugin/instructions/user_review_fixes_instructions.md`. This task documents that decision; it changes no plugin file.

**How this task's implementer reads the conventions.** This is the catch-all layer's task, and its target is a document of record under `docs/`. `.claude/context/conventions.md` → `## Documents of record` and `### Where a new responsibility goes` (*"a measured fact or a decision of record — `docs/`, and nowhere else"*) are the rules it answers to.

### Targets

- `docs/structured-agent-returns.md` — the decision *An agent's own `error:` return becomes an outcome, never `error`* under `## 1. The decisions`. **No other section.** `## 3. Measured, and not yet measured` gains nothing: the change relies on no fact about the `Agent` result or the `result` event that `## Reading a return` step 1 and the 2026-11-17 measurement do not already record.

**Work:**

- [ ] **The decision paragraph.** In *"An agent that returns `error:` today — `qa-tester` and `statistics-plan-writer` among them — has that return renamed …"*, drop `statistics-plan-writer` from the list of agents that return `error:` today.
- [ ] **The record of this branch's choice.** After *"This branch renames no agent's return; the outcome each such agent takes is decided by the branch that adopts it."*, add the decision `feat_structured_outputs_branch_review` took, in two or three sentences:
  - `statistics-plan-writer`'s `error:` return, which every caller treated as non-halting, became the outcome `not_written`, with its cause in `cause` (`plugin/schemas/statistics-plan-writer.return.json`).
  - The rule's *"The literal a caller matched before becomes the outcome value it routes on"* could not apply, because the old literal was the bare `error:`. *"named for the result it reports and never `error` or `blocker`"* decided the name.
  - Every dispatch site names that same non-halting route as its `error` route under `plugin/instructions/agent_return_contract.md` → `## A return that fails the check`, so a third failing return does not halt the flow either.

  Cite the agent's schema file and the module by repo-relative path, the form a document outside the plugin uses (`### Citing the module`).
- Leave `### Cost`'s sentence on a caller matching *"a prefix such as `error: blocked — `"* unchanged: that is `qa-tester`'s, which a later branch adopts.

**Verification:**

- `grep -n 'statistics-plan-writer' docs/structured-agent-returns.md` shows the agent named only in the new record of this branch's decision, never in the *"today"* list.
- `grep -n 'not_written' docs/structured-agent-returns.md` hits the new sentences, and `grep -n '"const": "not_written"' plugin/schemas/statistics-plan-writer.return.json` hits, so the record names the outcome the schema declares.
- `### The return block`'s canonical sentence, the section the authoring-document check reads, is byte-identical to before the edit: `git diff -- docs/structured-agent-returns.md` shows changes inside `## 1. The decisions` only.
