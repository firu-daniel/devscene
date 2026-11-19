# cli review — ### 4. The fail-closed boundary is unpinned and two documents describe the old behaviour — iteration 0

## Must Fix
1. **Text after the trailer still returns `SAFE`, so the fail-closed boundary is neither met nor pinned** — `cli/templates/scripts/prompt-injection-screen.sh` (`pis_unwrap_vlines`) — "if pis_is_tools_used_line "${PIS_VLINES[$i]}" || pis_is_notice_line "${PIS_VLINES[$i]}"; then"
   The user's requirement (`harness-runs/user_reviews/fix_injection_verdict_tools_used_prefix_review.md`, point 4) is that "every other text around the frame stays malformed". After the `agentId: ` line, the last loop of `pis_unwrap_vlines` refuses only an exact tools-used line and an exact two-space notice; everything else after the trailer is dropped. The new table pins only the case the script already refuses (`an indented notice after the trailer`), and the header this unit rewrote in `cli/test/prompt-injection-verdict.test.mjs` now says "a notice anywhere else" parks, which is not true.

   Executed: a throwaway copy of the test file's helpers, run with `node --test` against the unmodified template through `init` and the real `verdict` verb. Each return below is `wrapped(SAFE, ...)`, and each exited 0 and printed `verdict: SAFE`:
   - `${TRAILER}\n${NOTICE_TEXT}` (the exact notice at column 0)
   - `${TRAILER}\n${HARNESS_NOTICE.replace('a finding', 'a hint')}` (an altered notice, indented)
   - `${TRAILER}\nNote.` (prose)

   Exposure is narrower than a reply-borne bypass: every reply line is indented, so a reply cannot itself author a line after a column-0 trailer. This is read from the unwrap shape and was not tested against a live harness. The stated requirement is still unmet.
   **Class:** Wrong behaviour
   **Failure:** If `prompt-injection-screen.sh verdict` is given a framed `SAFE` result followed by `Note.` or a column-0 harness notice after its `agentId:` trailer, then it exits 0 and prints `verdict: SAFE` instead of parking one `malformed-verdict` finding.
   **Fix:** In `pis_unwrap_vlines`, replace the last loop's two-predicate refusal with a closed trailer shape: after the `agentId: ` line accept only blank lines and the `<usage>` block, for example lines matching `^(<usage>)?[a-z_]+: [0-9]+(</usage>)?$`, with the block closed once and nothing but blank lines after it; on anything else `return 0`. Check that shape against the recorded streams `docs/structured-agent-returns.md` §3 names before relying on it. Apply the same edit to `scripts/prompt-injection-screen.sh` so the two copies stay identical, and update the function's comment. Add these rows to the `malformed —` table: `['a column-0 notice after the trailer', wrapped(SAFE, `${TRAILER}\n${NOTICE_TEXT}`)]`, `['an altered notice after the trailer', wrapped(SAFE, `${TRAILER}\n${HARNESS_NOTICE.replace('a finding', 'a hint')}`)]`, `['prose after the trailer', wrapped(SAFE, `${TRAILER}\nNote.`)]`.
