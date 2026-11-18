# general review — ### 1. The 2026-11-18 prefix measurement names no Claude Code version range — iteration 0

## Must Fix
1. **The new version figures are recorded with no command that produces them** — `docs/structured-agent-returns.md` (`## 3. Measured, and not yet measured`) — "Taking each result's version from the latest `init` event ahead of it, the lowest version carrying the notice is 2.1.292 and the lowest carrying the tools-used element is 2.1.311."
   `.claude/context/conventions.md` → `## Documents of record` requires that "A measured fact states what was measured, the command and the exact message". This edit adds four measured facts: the range 2.1.287 to 2.1.327, nine streams carrying two versions, the notice's lowest version and the element's lowest version. The only command in the paragraph is the existing one, which it describes as printing "the text ahead of the frame"; its output holds no version. The probes that produced the figures are described in the `**Deviations from plan:**` of `harness-runs/code_reviews/fix_injection_verdict_tools_used_prefix_code_review/finding_1.md` as throwaway files under `harness-runs/scratch/`, so they are not on record either.

   The figures themselves are correct, and the 2.1.311 deviation is sound. A probe over the 87 streams in the main checkout's `harness-runs/autonomous_logs/` (`bash scripts/scratch-run.sh harness-runs/scratch/verify_prefix_versions.py <logs dir>`) showed: range 2.1.287 to 2.1.327 by first and by all `init` events; 9 two-version streams; table counts 4575 / 113 / 57 / 7 of 4752; notice lowest 2.1.292; element lowest 2.1.311 by latest `init`, and 2.1.299 only under first-`init` attribution, from `chore_sbx_flow_probe.stream.jsonl`. The defect is only that the document gives no way to reproduce them, and the attribution rule is exactly what moved the answer from 2.1.299 to 2.1.311.
   **Class:** Broken contract
   **Failure:** If a maintainer runs the paragraph's command over a later set of streams to check whether "the lowest carrying the tools-used element is 2.1.311" still holds, then its output contains no version at all, so the figure cannot be re-derived or compared.
   **Fix:** Leave the paragraph and the table as they are. Immediately before the paragraph opening "`pis_unwrap_vlines` accepts the tools-used lines", add this sentence and the two commands:

   The version figures come from two further commands, each run once per stream: the first prints the stream's distinct `claude_code_version` values, the second one `<version> tools-used` or `<version> notice` line per occurrence, `<version>` being that of the latest `init` event ahead of the result.

   ```
   jq -R -r -s '[split("\n")[] | fromjson? | objects | select(.type == "system" and .subtype == "init") | .claude_code_version] | unique | join(" ")' <state_dir>/autonomous_logs/<branch>.stream.jsonl
   ```

   ```
   jq -R -r -s '[split("\n")[] | fromjson? | objects] as $ev | [$ev[] | select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and (.name == "Agent" or .name == "Task")) | .id] as $ids | foreach $ev[] as $e (null; if $e.type == "system" and $e.subtype == "init" then $e.claude_code_version else . end; . as $v | $e | select(.type == "user") | .message.content[]? | select(.type == "tool_result" and (.tool_use_id as $t | any($ids[]; . == $t))) | (.content | if type == "string" then . elif type == "array" then ([.[] | select(.type == "text") | .text] | join("\n")) else tojson end) as $t | ($t | index("[Subagent hand-back]")) as $f | select($f != null) | $t[0:$f] as $p | (select($p | contains("<tools-used-before-summary>")) | "\($v) tools-used"), (select($p | contains("[harness: subagent output matched")) | "\($v) notice"))' <state_dir>/autonomous_logs/<branch>.stream.jsonl
   ```

   Both were executed over all 87 streams. The first gave 87 lines, 9 of them with two versions, lowest 2.1.287 and highest 2.1.327. The second exited 0 on every stream and gave 120 `tools-used` lines (113 + 7) and 64 `notice` lines (57 + 7), lowest 2.1.311 and 2.1.292, matching the table and the paragraph.
