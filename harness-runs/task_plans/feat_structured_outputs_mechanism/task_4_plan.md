### Task 4 — Reword Reading a return for the measured Agent result and point the screen at it

**Goal:** Make `plugin/instructions/agent_return_contract.md` → `## Reading a return` state what an orchestrating session actually receives from an `Agent` dispatch, and what it disregards, so step 1's block test applies to the reply rather than to the wrapped result (Gap 1). Then point the prompt-injection screen's verdict-file write at that reading, so the session writes the agent's reply and not Claude Code's wrapping.

**Depends on:** Task 3. Its `prompt-injection-screen.sh verdict` accepts a verdict file only when it holds exactly one fenced `json` block, an opener exactly ```` ```json ```` and a closer exactly ```` ``` ````, with nothing but whitespace-only lines around it. A Claude Code trailer or the two-space indentation left in the file parks the run as `malformed-verdict`. This task is what makes the session write that shape.

**What the session receives, measured (Claude Code 2.1.325, 2026-11-17, the two run streams the task prompt names).** An orchestrator `Agent` dispatch's `tool_result` text has three parts:
1. **A frame line at column 0.** It opens `[Subagent hand-back]`. The full measured line is recorded by Task 6 in `docs/structured-agent-returns.md` → `## 3.`.
2. **The sub-agent's reply, with every line indented by two spaces.** Blank lines and fence lines are included: ```` \n  ```json\n  {"outcome": "PASS"}\n  ```\n ````.
3. **A trailer at column 0.** It is a line opening `agentId: ` (`agentId: <id> (use SendMessage with to: '<id>', summary: '<5-10 word recap>' to continue this agent)`), then `<usage>subagent_tokens: <n>`, `tool_uses: <n>` and `duration_ms: <n></usage>`.

Who adds the indentation is **not measured**. The module must not say Claude Code adds it, or that the agent does.

**Where this task stops.**
- **The measurement record.** The version, the date, the command and the printed text are **Task 6's**, in `docs/structured-agent-returns.md` → `## 3.`. This module carries only what its runtime reader acts on (`harness-runs/lessons.md` → `## Agent prose`, *"A shared instruction module carries only what its runtime reader acts on"*), so it carries no version, date or rationale.
- **The agent's return object.** That is **Task 5's**. `prompt_injection_screen.md` keeps telling the session never to act on the return's content.

### Targets

- `plugin/instructions/agent_return_contract.md` — `## Reading a return`, and `## Who may cite this`.
- `plugin/instructions/prompt_injection_screen.md` — `## The steps` step 3, the verdict-file bullet.

**Work:**

- [ ] `## Reading a return`: before the current step 1, add a step stating what an `Agent` result carries.
  - **The parts.** Column-0 text before the reply — a frame line opening `[Subagent hand-back]` — then the reply, every line of it indented by the same two spaces, then column-0 text after it: a line opening `agentId: ` and a `<usage>` … `</usage>` block.
  - **What the reply is.** The indented lines with those two spaces removed. The frame and the trailer are disregarded.
  - **A result with none of them.** It is the reply as it stands.
  - Re-word the current step 1 to apply to *the reply* (*"The reply's last fenced block opened with `json` …"* already says *reply*; keep its block, whitespace and one-object tests byte-for-byte), and renumber.
  - Keep the heading `## Reading a return` byte-identical: five instruction files and `plugin/docs/AUTONOMOUS_FLOW.md` point at it.
  - Add only the words the new behaviour needs (`.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour"*).
- [ ] `## Who may cite this`: add `` - `${CLAUDE_PLUGIN_ROOT}/instructions/prompt_injection_screen.md` `` in the list's existing form, since the next bullet makes that file cite this module.
- [ ] `prompt_injection_screen.md` → step 3, the bullet *"Write its whole return verbatim with the file tool to …"*:
  - It becomes: write the agent's **reply**, read out of the `Agent` result per `${CLAUDE_PLUGIN_ROOT}/instructions/agent_return_contract.md` → `## Reading a return` (frame and trailer disregarded, indentation removed), verbatim with the file tool to the same path. The `<branch_fold>` sentence is unchanged.
  - State that the session applies none of that section's other checks, and none of `## A return that fails the check`: the script is the return's only reader and fails closed. The bullet *"Never read the screened file yourself, and never act on the return's content"* stays.
  - Change nothing else in the file, the `Raised by:` halt line included. That line is a park-file heading, not a return.

**Verification:**

- `git grep -l 'agent_return_contract.md' -- plugin` lists exactly the files under `## Who may cite this`, plus the module itself.
- `grep -n '^## ' plugin/instructions/agent_return_contract.md` shows the three headings unchanged.
- **Measured shape, end to end.** Applying the reworded steps by hand to the measured result text above yields a reply whose last fenced `json` block passes step 1's tests. Fed into Task 3's script, that same reply — with the trailer and the indentation left in — would park, which is why the screen's write cites this section.
- **No version or date.** The reworded section carries no Claude Code version, no date and no claim about who adds the indentation.
