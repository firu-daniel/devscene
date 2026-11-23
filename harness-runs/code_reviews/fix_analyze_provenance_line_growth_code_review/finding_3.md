### 3. The writer's new provenance bullet carries rationale the writer does not act on

**File:** `plugin/agents/conventions-writer.md` → `## The document`, the bullet "**Write a document-level provenance line describing this pass only.**", at "; git history records them."

The bullet says *"It carries no earlier pass forward — no earlier mode, fix pass or hand-edit clause; git history records them."* The instruction ends at "hand-edit clause". The clause *"git history records them"* tells the writer why the harness can drop history, and the writer does nothing with that. No reader of this file reaches a different action without it. `.claude/context/plugin.md` → `## Writing agent prose` says *"Drop rationale the agent does not act on"*, and *"A change to an agent definition adds only the words its new or changed behaviour needs — no rationale"*. The writer definition is loaded on every write, merge and fix dispatch, so the clause costs context on every one of them.

**Fix:** in that bullet, replace
`no earlier mode, fix pass or hand-edit clause; git history records them.`
with
`no earlier mode, fix pass or hand-edit clause.`

`cli/test/conventions-provenance-line.test.mjs` asserts on `'carries no earlier pass forward'` and not on the removed clause, so the change keeps it passing. This fix creates and edits no test file, so it runs none. The full suite runs in the Run gates phase.
