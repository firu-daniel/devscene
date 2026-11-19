### 4. The fail-closed boundary is unpinned and two documents describe the old behaviour

**File:** `cli/test/prompt-injection-verdict.test.mjs` (the `malformed —` table) — "['other text between the tools-used line and the frame'"

**Targets:** `cli/test/prompt-injection-verdict.test.mjs`, `plugin/instructions/agent_return_contract.md` (`## Reading a return` step 1), `docs/structured-agent-returns.md` (the paragraph holding "and refuses the notice", and the `**Decision — the third path, a script caller.**` paragraph's "The script unwraps only the whole measured shape").

**Depends on:** Findings 1 to 3. They add `pis_is_notice_line`, the two accepted notice placements, the `<\` repair, and the test helpers `NOTICE_TEXT` (the notice without its indent) and `rawUnsafe(excerpt, reason)`. They also move the two old notice rows out of the malformed table, so this finding does not touch those rows.

## Problem

The user requires that only the exact notice is accepted, that it can never produce `SAFE` by itself, and that all other text around the frame stays malformed. Findings 1 to 3 build that behaviour, and nothing yet fails if a later change widens it. `## Reading a return` step 1 and two passages of `docs/structured-agent-returns.md` still describe a result without the notice: the §3 paragraph says the script refuses it, and the third-path decision lists the accepted shape without it and calls any other text ahead of the frame malformed.

## Fix

### 1. Add the fail-closed cases

Add these rows to the `malformed —` table. Each must park one `malformed-verdict` finding.

| Label | Return |
|---|---|
| the notice alone in the reply | `wrapped(`${NOTICE_TEXT}\n`)` |
| the notice ahead of a frame with an empty reply | `` `${HARNESS_NOTICE}\n${FRAME}\n${TRAILER}\n` `` |
| the notice over a bare block | `` `${HARNESS_NOTICE}\n${SAFE}` `` |
| a column-0 notice over a bare block | `` `${NOTICE_TEXT}\n${SAFE}` `` |
| a column-0 notice ahead of the frame | `prefixed(SAFE, `${NOTICE_TEXT}\n`)` |
| a notice indented by one space ahead of the frame | `prefixed(SAFE, ` ${NOTICE_TEXT}\n`)` |
| a notice indented by four spaces ahead of the frame | `prefixed(SAFE, `    ${NOTICE_TEXT}\n`)` |
| two notices ahead of the frame | `prefixed(SAFE, `${HARNESS_NOTICE}\n${HARNESS_NOTICE}\n`)` |
| a tools-used line after the notice | `prefixed(SAFE, `${HARNESS_NOTICE}\n  ${TOOLS_USED}\n`)` |
| a notice ahead of the frame and another in the reply | `prefixed(`${NOTICE_TEXT}\n${SAFE}`, `${HARNESS_NOTICE}\n`)` |
| two notices in the reply | `wrapped(`${NOTICE_TEXT}\n${NOTICE_TEXT}\n${SAFE}`)` |
| a notice after other reply text | `wrapped(`Note.\n${NOTICE_TEXT}\n${SAFE}`)` |
| a notice after the closing fence | `wrapped(`${SAFE}${NOTICE_TEXT}\n`)` |
| a notice indented by four spaces in the reply | `wrapped(`  ${NOTICE_TEXT}\n${SAFE}`)` |
| a column-0 notice between the reply and the trailer | `` `${FRAME}\n${indent(SAFE)}\n${NOTICE_TEXT}\n${TRAILER}\n` `` |
| an indented notice after the trailer | `wrapped(SAFE, `${TRAILER}\n${HARNESS_NOTICE}`)` |
| text after the notice on its line | `prefixed(SAFE, `${HARNESS_NOTICE} done\n`)` |
| a trailing space on the notice | `prefixed(SAFE, `${HARNESS_NOTICE} \n`)` |
| a notice with its sentence altered | `prefixed(SAFE, `${HARNESS_NOTICE.replace('a finding', 'a hint')}\n`)` |
| a notice with an empty pattern list | `prefixed(SAFE, `${HARNESS_NOTICE.replace('settings-json', '')}\n`)` |
| a notice whose pattern list is prose | `prefixed(SAFE, `${HARNESS_NOTICE.replace('settings-json', 'ignore all rules')}\n`)` |
| a notice whose pattern list holds a bracket | `prefixed(SAFE, `${HARNESS_NOTICE.replace('settings-json', 'a]b')}\n`)` |
| SAFE with an extra key holding `<\` | ``'```json\n{"outcome":"SAFE","<\\x":1}\n```\n'`` |
| an outcome holding `<\` | ``'```json\n{"outcome":"<\\SAFE"}\n```\n'`` |
| a check_id holding `<\` | `unsafe` is unusable here: write the block by hand with `"check_id":"<\\attack"` |
| an excerpt ending in `<\`, which swallows its closing quote | `rawUnsafe('a<\\')` |

Update the file's header comment, which states the accepted shape, to name the notice and its two placements and to say that the notice decides nothing: the reply must still be one valid verdict block.

### 2. Update `## Reading a return` step 1

Replace step 1 of `plugin/instructions/agent_return_contract.md` → `## Reading a return` with:

> 1. Take the reply out of the `Agent` result. The result can carry text before the reply — lines that are each only a complete `<tools-used-before-summary>…</tools-used-before-summary>` element, at column 0 or indented by two spaces, then at most one harness notice line, indented by two spaces and opening `[harness: subagent output matched instruction-shaped pattern(s): `, with blank lines among them, and then a column-0 frame line opening `[Subagent hand-back]` — then the reply, every line of it indented by the same two spaces, then column-0 text after it: a line opening `agentId: ` and a `<usage>` … `</usage>` block. When no notice preceded the frame, the reply's first non-blank line can be that notice. The reply is the indented lines after the frame with those two spaces removed; the element lines, the notice, the frame and the trailer are disregarded. A result with none of them is the reply as it stands.

### 3. Update `docs/structured-agent-returns.md`

**a. The §3 paragraph.** Replace the paragraph opening "`pis_unwrap_vlines` accepts the tools-used lines" with the text below, which is two paragraphs around one command. Keep the old paragraph's closing sentence about the recorded park as it stands, at the end of the second paragraph.

> `pis_unwrap_vlines` accepts the tools-used lines, at column 0 as well though no recorded line sits there, and at most one notice, indented by exactly two spaces and matching the text above with a comma-separated list of lower-case pattern names. The notice is accepted after any tools-used lines ahead of the frame, where all 64 recorded notices sit, or as the first non-blank line of the reply, where a live `prompt-injection-reviewer` run delivered it. That run is recorded in `harness-runs/user_reviews/fix_injection_verdict_tools_used_prefix_review.md`, which does not state its Claude Code version. None of the 4752 framed results in the 87 streams above holds the notice after the frame. The command prints, as JSON, the text after the frame of each framed result holding the notice there, run once per stream with `<branch>` its branch, and printed nothing for all 87:
>
> ```
> jq -R -r -s '[split("\n")[] | fromjson? | objects] as $ev | [$ev[] | select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and (.name == "Agent" or .name == "Task")) | .id] as $ids | [$ev[] | select(.type == "user") | .message.content[]? | select(.type == "tool_result" and (.tool_use_id as $t | any($ids[]; . == $t))) | .content | if type == "string" then . elif type == "array" then ([.[] | select(.type == "text") | .text] | join("\n")) else tojson end] | .[] | select(contains("[Subagent hand-back]")) | split("[Subagent hand-back]")[1:] | join("[Subagent hand-back]") | select(contains("[harness: subagent output matched")) | tojson' <state_dir>/autonomous_logs/<branch>.stream.jsonl
> ```
>
> The notice decides nothing: the reply must still be one valid verdict block, and any other text around the frame parks as `malformed-verdict`. Because the notice's neutralization puts `<\` inside the reply's JSON strings, `pis_parse_verdict` keeps that backslash literal before parsing, so an `UNSAFE` excerpt quoting a control tag keeps its findings; `SAFE` is still compared against the unrepaired text.

**b. The third-path decision.** In the `**Decision — the third path, a script caller.**` paragraph, replace the sentence opening "The script unwraps only the whole measured shape (§3)" with:

> The script unwraps only the whole measured shape (§3): optional tools-used lines and then at most one harness notice ahead of the frame, with blank lines among them, the frame line, a two-space indent on every reply line, the same notice as the reply's first non-blank line when none preceded the frame, and an optional `agentId: ` trailer. A bare trailer, a bare indent, a frame over any other shape, any other text ahead of the frame, a second notice, a notice anywhere else, or a tools-used line after the notice or the frame stays malformed.

### 4. Confirm the two scripts match

This finding edits neither script. `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` must report `0` added and `0` deleted. That command exits 1 on correct work, because the two files' modes differ by design.

- **Deviations from plan:** The `cli` layer's fix iteration 0 (`harness-runs/user_review_fix_plan_point_reviews/fix_injection_verdict_tools_used_prefix_fix_plan/item_4/review_0.md`, Must Fix 1) overrides Fix step 4's "This finding edits neither script": `cli/templates/scripts/prompt-injection-screen.sh` → `pis_unwrap_vlines` now accepts after the `agentId: ` line only blank lines and at most one `<usage>` block of `<name>: <digits>` lines closed once (new `PIS_USAGE_OPEN_RE` / `PIS_USAGE_LINE_RE`), and returns unwrapped on anything else. The shape was checked against all 87 streams in the main checkout's `harness-runs/autonomous_logs/`: every one of the 4752 framed results carries exactly `["<usage>subagent_tokens: N","tool_uses: N","duration_ms: N</usage>"]` after its `agentId: ` line (digits folded to `N`, run per stream through `uniq -c`). The root copy `scripts/prompt-injection-screen.sh` is outside the `cli` layer's path and is not edited here; until the `general` layer applies the same edit, Fix step 4's `git diff --no-index --numstat` reports `8 24`, not `0 0`. Test rows added beyond the review's three: `a usage block left open`, `a second usage block after the trailer`, and the SAFE row `as the whole Agent result with blank lines after the trailer`.
- **Deviations from plan:** (`general` layer) Fix step 4 overridden as the `cli` note above requires: `scripts/prompt-injection-screen.sh` was overwritten with the template's current bytes (mode 755 kept), and `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` now reports `0 0` (exit 1, the mode difference). If the `cli` layer edits the template again (item_4 `review_1.md` Should Fix 1 asks for header rewording), the root copy must be re-synced.
- **Deviations from plan:** Step 3a's "which does not state its Claude Code version" is kept and extended with "every `version` field of the session transcript it ran in reads 2.1.327": a jq/grep over that session's transcript returned 1484 `version` fields, all `2.1.327`. The Agent result carrying the in-frame notice was not found in that transcript's Agent tool results by jq; the placement claim rests on the user review's item 2. The step's 4752/87 figures were re-measured in this session over the main checkout's `harness-runs/autonomous_logs/*.stream.jsonl`: the step's jq printed nothing for all 87 streams, and 4752 Agent/Task results carry the frame.
- **Deviations from plan:** Step 3b's sentence is extended for the `cli` layer's trailer change: the accepted trailer is "an optional `agentId: ` trailer followed by nothing but blank lines and at most one closed `<usage>` block", and "any other text after the `agentId: ` line" is added to the malformed list.
