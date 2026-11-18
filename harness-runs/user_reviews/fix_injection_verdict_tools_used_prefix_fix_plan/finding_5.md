### 5. Every other agent's return holding a neutralized control tag fails the routing check

**File:** `plugin/instructions/agent_return_contract.md` (`## Reading a return` step 2) — "and parses as one JSON object."
**Class:** Wrong action from operative text
**Failure:** If an orchestrating session applies `## Reading a return` step 2 to a return whose JSON string Claude Code rewrote to hold `<\system-reminder>`, then the block does not parse because `\s` is an invalid escape, the return counts as no return and the same dispatch is sent again, up to the third failure taking the section's `error` route.

**Targets:** `plugin/instructions/agent_return_contract.md`, `docs/structured-agent-returns.md`.

**Depends on:** Finding 3, whose `pis_parse_verdict` repair this reading matches, and Finding 4, which rewrites step 1 of the same section and writes the `docs/structured-agent-returns.md` sentence this finding extends.

## Problem

Finding 3 repairs the neutralized `<\` for the one return a script parses. Every other agent's return is read by the orchestrating session under `## Reading a return`, and step 2 requires its last `json` block to parse as one JSON object, with no allowance for that rewrite.

The rewrite does reach replies: six `Agent` results in the 87 recorded streams hold `<\` followed by a byte other than `"`, `/` or `\` after the frame, each alongside the notice. None of the 146 `json` blocks in those replies holds it yet, so this failure has not been recorded. `jq` refuses the form: `{"a":"<\system-reminder>"}` gives `Invalid escape`. As Finding 3 shows, other tags do not fail but decode wrongly: `<\tool_use_error>` parses with a tab in place of `\t`.

A failed check is not a return (`## A return that fails the check`), so re-dispatching costs up to three dispatches, and the same input is likely to produce the same text each time.

No `result` event in the recorded streams holds the form, so the driver's `PNL_REAP_JQ` path is not part of this finding.

## Fix

### 1. Update `## Reading a return` step 2

Replace step 2 of `plugin/instructions/agent_return_contract.md` → `## Reading a return` with:

> 2. The reply's last fenced block opened with `json` exists, has only whitespace after its closing fence, and parses as one JSON object. Claude Code can rewrite `<` in a control tag to `<\`, so when parsing, read each `<\` whose next character is not `"`, `/` or `\` as those two literal characters rather than as a JSON escape. A field's value keeps them as written.

Leave the section's heading, its other steps and `## Who may cite this` unchanged. Step 1 is Finding 4's edit.

### 2. Record it in `docs/structured-agent-returns.md`

In the paragraph Finding 4 writes, directly after the sentence ending "`SAFE` is still compared against the unrepaired text.", add:

> `agent_return_contract.md` → `## Reading a return` step 2 gives an orchestrating session the same reading of `<\` for every other agent's return, so a return quoting a control tag is not re-dispatched as unparsable.

The old paragraph's closing sentence about the recorded park still comes last.
