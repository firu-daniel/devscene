# Agent return contract

## Resolved values

This file declares no token: every `<…>` name here is defined by its own text at its use site, or bound by the citing flow.

## Reading a return

An orchestrating caller applies this **routing check** to a return before acting on it:

1. Take the reply out of the `Agent` result. The result can carry text before the reply — lines that are each only a complete `<tools-used-before-summary>…</tools-used-before-summary>` element, at column 0 or indented by two spaces, then at most one harness notice line, indented by two spaces and opening `[harness: subagent output matched instruction-shaped pattern(s): `, with blank lines among them, and then a column-0 frame line opening `[Subagent hand-back]` — then the reply, every line of it indented by the same two spaces, then column-0 text after it: a line opening `agentId: ` and a `<usage>` … `</usage>` block. When no notice preceded the frame, the reply's first non-blank line can be that notice. The reply is the indented lines after the frame with those two spaces removed; the element lines, the notice, the frame and the trailer are disregarded. A result with none of them is the reply as it stands.
2. The reply's last fenced block opened with `json` exists, has only whitespace after its closing fence, and parses as one JSON object. Claude Code can rewrite `<` in a control tag to `<\`, so when parsing, read each `<\` whose next character is not `"`, `/` or `\` as those two literal characters rather than as a JSON escape. A field's value keeps them as written.
3. Its `outcome` is one the dispatching section routes on for this dispatch.
4. Every field that section reads for that outcome is present and not empty — except a field that section names as optional, which is not part of the check: absent or empty means none.

## A return that fails the check

A return that fails `## Reading a return` is **not a return**. Record nothing for it, and send the same dispatch again through the dispatching flow's safety contract — a heartbeat and a counted dispatch like any other.

After the **third** consecutive failing return for the same dispatch, take the dispatching section's `error` route: the route that section names as its `error` route, where it names one; otherwise `--outcome error` where that section passes outcomes to `flow-walker.sh`; otherwise the flow's blocker route — `<escalate>` where the flow binds it, else stop and report. Name the agent and the check that failed.

## Who may cite this

These documents point at a section of this file:

- `${CLAUDE_PLUGIN_ROOT}/commands/analyze.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/AUTONOMOUS_FLOW.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/plan_orchestration_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fix_plan_writing_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/qa_test_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/code_review_fixes_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/user_review_fixes_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/prompt_injection_screen.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/docs_phase_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/docs_orchestration_instructions_autonomous.md`

A citer points and never restates; a new citer joins this list.
