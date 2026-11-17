### 6. Align the writer's return-value sentence with the return-block contract

**Severity:** Nice to Have

**Site:** `plugin/agents/conventions-writer.md` → `## Output contract`, the opening line *"Your final message IS your return value (not a human chat). Field names byte-stable."*

**Problem.** The canonical sentence that follows makes the return value the fenced `json` object at the end of the reply, and the decision record (`docs/structured-agent-returns.md` → `### The return block`) allows prose above it. "Your final message IS your return value" is the old prose-return wording, and it now points the other way.

The sibling agent edited on this branch already uses the aligned form: `plugin/agents/conventions-reviewer.md` → `## Output contract` reads *"That object is your return value; you write no file, on either axis. Field names byte-stable."*

The phrase "Field names byte-stable" must stay. Both `plugin/instructions/mention_reading.md` and `.claude/context/plugin.md` → `## Wires: dispatch in, return out` quote it from this section.

**Fix.** In `## Output contract`, delete the line

> Your final message IS your return value (not a human chat). Field names byte-stable.

Then insert, directly after the canonical sentence (`End your reply with your return object: …`) and before `### Return fields`, the line

> That object is your return value (not a human chat). Field names byte-stable.

Leave a blank line on either side of it.
