### 2. A corpus fix the session applies to `.claude/CLAUDE.md` has no rule keeping it out of the section's provenance note

**File:** `plugin/commands/analyze.md` → step 4 (4b), the paragraph opening "**Corpus findings against this file, and who applies them.**", at "**applied by this session and never dispatched**"; and `cli/test/conventions-provenance-line.test.mjs` → the test `'analyze.md (4b) points at the bound rather than copying it'`

Task 1 closed the fix-pass route for the conventions documents. `plugin/agents/conventions-writer.md` → `## The fix dispatch` now says *"A fix adds nothing to the provenance line: it belongs to the pass the line already describes."* The `project` target has no writer, though. Its corpus findings are *"applied by this session and never dispatched"* (`plugin/commands/analyze.md` → (4b)), and the session is bound to the writer's rules only through *"`## The document` and `## House rules`"* (the paragraph opening "**The two sections this session composes are bound by the writer's own content rules, by reference.**"). It is not bound to `## The fix dispatch`. So when the session applies a corpus fix inside a section it wrote, nothing tells it to leave that section's provenance note alone.

This repository's own `.claude/CLAUDE.md` shows what happens: its project-paragraph note carries *"the audience and self-adoption blocks reduced to pointers by the corpus pass"*. That is the fix-pass history the task prompt asks to stop, and it applies to the (4b) notes as well (*"The same shape applies to the `project` target's per-section provenance notes"*). The story plan names this route as its second top risk (*"the fix dispatch … and the `project` target's (4b) notes"*), but only the writer's half of it is closed.

Confirmed by reading `plugin/commands/analyze.md` → (4b) and `plugin/agents/conventions-writer.md` → `## The fix dispatch`. No probe can show what a session writes.

**Fix:**

1. In `plugin/commands/analyze.md` → (4b), replace
   `corpus finding naming this `document_path` is, on **`fixable`**, **applied by this session and never`
   `dispatched**: no writer may touch this file`
   with
   `corpus finding naming this `document_path` is, on **`fixable`**, **applied by this session and never`
   `dispatched**, and adds nothing to that section's provenance note, as a writer's fix adds nothing to its`
   `line: no writer may touch this file`
   Re-wrap the lines of that paragraph to the file's existing width, as the rest of (4b) is wrapped.
2. In `cli/test/conventions-provenance-line.test.mjs`, the test `'analyze.md (4b) points at the bound rather than copying it'`, add `"adds nothing to that section's provenance note"` to the `present` array after `'whose per-section counterpart is the provenance note above'`. The new phrase sits inside the (4b)→(4c) slice the test already reads, and it contains none of the phrases in the test's `absent` array.

The only test this fix runs is the suite it edits: `npm test --workspace cli -- test/conventions-provenance-line.test.mjs`, from the repository root, as one plain foreground command. The full suite runs later, in the Run gates phase.
