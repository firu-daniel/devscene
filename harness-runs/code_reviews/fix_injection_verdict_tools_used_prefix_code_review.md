# Code Review: fix_injection_verdict_tools_used_prefix

## Context

**Branch:** `fix_injection_verdict_tools_used_prefix`
**Date:** 2026-11-18
**Reviewed:** the whole branch diff against `origin/dev` (this run copy has no local `dev`): `pis_is_tools_used_line` and the `pis_unwrap_vlines` change in `cli/templates/scripts/prompt-injection-screen.sh`, the byte-identical self-adopted `scripts/prompt-injection-screen.sh`, the new cases in `cli/test/prompt-injection-verdict.test.mjs`, `plugin/instructions/agent_return_contract.md` → `## Reading a return` step 1, and the new measurement in `docs/structured-agent-returns.md`. 14 run-artifact files excluded from the reviewed diff.

**Tests.** All four task-prompt acceptance criteria have cases. This review ran no suite; the Run gates phase establishes whether they pass. The two functions were exercised directly under `/bin/bash` 3.2: the measured prefix and a column-0 line unwrap, and a three-space indent, an empty element, a trailing CR, a split tag, a lone tag and a tag in the trailer all stay wrapped. Run over the 177 recorded results that carry text ahead of the frame, the function unwrapped the 113 tag-prefixed ones and left the 64 carrying the harness notice wrapped, as the story index decides.

**Pass 0.** The grep sweep exited 0 with 0 hits, so none became findings. The new-exported-symbol check had nothing to check: the diff adds no export.

**Measurement.** The table in `docs/structured-agent-returns.md` was re-derived from the 87 streams in the main checkout's `harness-runs/autonomous_logs/` and matches: 4752 framed results, split 4575 / 113 / 57 / 7, with the stated element contents and no tag after a frame. The story's scope-register sweep reaches no site outside its rows, apart from the two lines this branch added. `phases.parity` is `false`, so no parity check applies.

**Conclusion.** Pass 1 found no defect. The one finding below is a Should Fix carried over from the Task 4 per-unit review, which still applies.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — State the Claude Code version range of the 2026-11-18 prefix measurement _(layer: general)_

---

## Must Fix

None.

---

## Should Fix

### 1. The 2026-11-18 prefix measurement names no Claude Code version range
→ [finding_1.md](fix_injection_verdict_tools_used_prefix_code_review/finding_1.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None: `phases.parity` is `false`.
