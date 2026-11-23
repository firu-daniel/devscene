# Skeptic Review: fix_analyze_provenance_line_growth

## Context

**Branch:** `fix_analyze_provenance_line_growth`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev` (`defaultBranch`). That is `plugin/agents/conventions-writer.md`, `plugin/agents/conventions-reviewer.md`, `plugin/commands/analyze.md` and the new `cli/test/conventions-provenance-line.test.mjs`. I checked them against the task prompt and the story plan. 20 run-artifact files were excluded from the reviewed diff.
**De-duplicated against:** `harness-runs/code_reviews/fix_analyze_provenance_line_growth_code_review.md` and its three findings. No parity review exists (`phases.parity` is `false`) and no architecture review exists. The planning rounds left no incidental findings.

**Headline conclusions:**
- **Check 1 (wiring).** The bound is reached on the writer's `write`, `merge` and fix paths, on the reviewer's document pass and corpus pass, and in (4a). One route is still open. On a (4b) section `write`, the session that composes `.claude/CLAUDE.md` gets no area-level, no-per-file bound for the section's provenance note, because the only sentence carrying the bound is scoped to `merge` (Finding 1).
- **Check 3 (citations).** Every new cross-file pointer resolves: `conventions-writer.md` → `## The document`, `conventions-reviewer.md` → `## The corpus pass — what to verify`, and `analyze.md` → `(4b)`.
- **Checks 2 and 4.** Check 2's parity leg is inert, and no runtime address is involved. There is no intentional divergence to re-grade.
- **New suite.** It sits under `cli/test/` and matches the `node --test` default pattern, so the runner picks it up. Its phrases match the text the three files now carry.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Bound the (4b) provenance note on `write` as well as on `merge` _(layer: plugin)_

---

## Must Fix

None.

---

## Should Fix

### 1. On a (4b) section `write`, nothing bounds the provenance note to this pass at directory or area level
→ [finding_1.md](fix_analyze_provenance_line_growth_skeptic_review/finding_1.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, and neither the plan nor the code marks any divergence as intentional, so this section is empty.
