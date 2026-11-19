### Task 2 — Describe the tools-used prefix in `## Reading a return` step 1

**Goal:** Make the routing check's first step describe the tools-used lines that can precede the frame, and define the reply so those indented lines are never taken for part of it.

**Depends on:** Task 1, which fixes the accepted shape: a tools-used line is exactly `<tools-used-before-summary>`, one or more characters that are neither `<` nor `>`, then `</tools-used-before-summary>`, at column 0 or indented by exactly two spaces, alone on its line, ahead of the frame only. This task states that shape for orchestrating readers and changes no script.

### Targets

- `plugin/instructions/agent_return_contract.md` — `## Reading a return` step 1.

**Work:**

- [ ] Replace step 1 with this text, keeping the heading, the numbering and steps 2 to 4 unchanged:

  > 1. Take the reply out of the `Agent` result. The result can carry text before the reply — lines that are each only a complete `<tools-used-before-summary>…</tools-used-before-summary>` element, at column 0 or indented by two spaces, with blank lines among them, and then a column-0 frame line opening `[Subagent hand-back]` — then the reply, every line of it indented by the same two spaces, then column-0 text after it: a line opening `agentId: ` and a `<usage>` … `</usage>` block. The reply is the indented lines after the frame with those two spaces removed; the element lines, the frame and the trailer are disregarded. A result with none of them is the reply as it stands.

**Verification:**

- `grep -n 'tools-used-before-summary' plugin/instructions/agent_return_contract.md` reports step 1 and no other line.
- Step 1 contains "the indented lines after the frame", and the section's other steps and `## Who may cite this` are byte-unchanged in `git diff`.
