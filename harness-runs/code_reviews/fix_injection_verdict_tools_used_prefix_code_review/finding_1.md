### 1. The 2026-11-18 prefix measurement names no Claude Code version range

**File:** `docs/structured-agent-returns.md` (`## 3. Measured, and not yet measured`) — "**Measured, 2026-11-18: what can precede the frame.**"

`.claude/context/conventions.md` → `## Documents of record` requires a measured fact to be recorded so that "a later version that behaves differently is detectable". Both earlier measurements in this section name the Claude Code version they were taken on. This one names no version for its streams. The only version in the paragraphs is 2.1.327, in the closing sentence about the park, so a maintainer asking when the prefix appeared reads that sentence and concludes the tools-used line arrived with 2.1.327.

The streams say otherwise. Taking each stream's `claude_code_version` from its first `system` / `init` event, the 87 streams in the main checkout's `harness-runs/autonomous_logs/` span 2.1.287 to 2.1.327. Among results with text ahead of the frame, the lowest version carrying the notice is 2.1.292 and the lowest carrying the tools-used element is 2.1.299.

**Fix:** in that paragraph, replace

```
this branch's own included. They are gitignored, so a run copy does not carry them.
```

with

```
this branch's own included, recorded under Claude Code 2.1.287 to 2.1.327 (each stream's `claude_code_version`, from its first `system` / `init` event). The notice first appears in a 2.1.292 stream and the tools-used element in a 2.1.299 stream. The streams are gitignored, so a run copy does not carry them.
```

Change nothing else in the paragraph or the table.

**Deviations from plan:** The fix text gives 2.1.299 as where the tools-used element first appears; implemented as 2.1.311, with the sentence reworded to say how a result's version is taken. 2.1.299 is the first `init` version of `chore_sbx_flow_probe.stream.jsonl`, but that stream carries a second `init` at 2.1.319, and both of its tools-used results follow it (stream lines 256 and 2558, timestamped 2026-11-06). Attributing each result to the latest `init` event ahead of it, the lowest version carrying the element is 2.1.311 (`feat_unattended_sandbox_measurement.stream.jsonl` line 2349, 2026-10-26; `fix_run_analytics_token_accounting.stream.jsonl` line 276, 2026-10-27). Publishing 2.1.299 would misdate the element by the defect this finding exists to remove. Nine of the 87 streams carry two versions, so the range's parenthetical names the `init` events rather than each stream's first one, and the paragraph says so. Confirmed unchanged by the same probe: range 2.1.287 to 2.1.327 (over first `init` events and over all of them), notice lowest at 2.1.292 by either attribution, and the section's table counts (4575 / 113 / 57 / 7, total 4752). Measured with throwaway probes under `harness-runs/scratch/`, run through `scripts/scratch-run.sh` over the main checkout's `harness-runs/autonomous_logs/`.
