# cli review — ### 4. The fail-closed boundary is unpinned and two documents describe the old behaviour — iteration 1

## Should Fix
1. **Two headers say the `<usage>` block is required; the code makes it optional** — `cli/templates/scripts/prompt-injection-screen.sh` (VERDICT header) — "`agentId: ` line followed by nothing but one `<usage>` block"; `cli/test/prompt-injection-verdict.test.mjs` (file header) — "`agentId:` line\n * followed by nothing but its `<usage>` block"
   `pis_unwrap_vlines` accepts an `agentId: ` line with no `<usage>` block after it: `usage` stays 0, and only `usage = 1`, a block left open, is refused. The function's own comment says this correctly: "then at most one `<usage>` … `</usage>` block". The script's VERDICT header and the test file's header say "nothing but one" / "nothing but its" block. A reader can take that as "the block is required", which the code does not enforce. No test pins either reading. Confirmed by reading the loop (`[ "$usage" != 1 ] || return 0`), not by a probe.
   **Fix:** Write "an `agentId: ` line followed by nothing but at most one `<usage>` block" in both headers, to match the function comment. Optionally add a SAFE row such as `['as the whole Agent result with a bare agentId trailer', wrapped(SAFE, TRAILER.split('\n')[0])]` so the accepted shape is pinned.

## Nice to Have
1. **Header lines overrun the wrap width** — `cli/templates/scripts/prompt-injection-screen.sh` (VERDICT header) — "`agentId: ` line followed by nothing but one `<usage>` block — is unwrapped to the reply first"; `cli/test/prompt-injection-verdict.test.mjs` (file header) — "which is unwrapped to the reply first. The one notice has two accepted placements: indented by two"
   The edited lines run well past the width of the comment lines around them. Re-wrap them to match.
