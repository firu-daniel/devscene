# Skeptic Review: feat_flow_graph_schema_v2

## Context

**Branch:** `feat_flow_graph_schema_v2`
**Date:** 2026-11-20
**Reviewed:** the whole branch diff against `origin/dev`. The default branch is `dev`, and this run copy has no local branch for it. The diff covers:

- the format-4 source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`;
- the generic schema at `graphscene/src/graphscene/schemas/flow-graph.schema.json` and its fixtures;
- `graphscene.vocabulary`;
- `scripts/generate-flow-graph-v3.mjs`;
- the `validate:graphscene-schema*` npm scripts and gate legs `3g`–`3i`;
- the documentation edits.

24 run-artifact files excluded from the reviewed diff.

**De-duplicated against:**

- the committed code review `harness-runs/code_reviews/feat_flow_graph_schema_v2_code_review.md` and its Findings 1–4, all applied;
- the planning rounds' incidental leads.

No branch-level parity review exists (`phases.parity` is `false`), and no branch-level architecture review exists for this branch.

**What was verified first-hand:**

- **Callers.** `vocabulary_violations` is exported and called. Legs `3g`/`3h`/`3i` are in the `gr_run_round` list in `scripts/run-gates.sh`. All 15 format-4 fixtures and the format-4 source are wired by name into the two npm scripts. `schemas/validate.mjs` accepts repeated `-d`.
- **Citations.** The generator cites `flow-walker.sh` → `round.held.<gate>`, the refusal "only 'answered' is" and `add_skipped_node`, and these exist. The format-3 `phase` enum and `runModeId` pattern agree with the generator's predicate table.
- **Applied Finding 1 fix.** The stop-reason refusal from code-review Finding 1 is in place in `generate`.
- **Fixtures.** Each schema-negative fixture differs from `valid_generic.json` in exactly the construct it names.

**Headline:** one net-new Must Fix. Gate 3i's own remedy line tells the reader to run `--write`. When the cause is a hand edit of a generated format-3 copy, that command silently overwrites the edit. Gate 3e's findings still point readers at that copy.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Make gate 3i's remedy say the format-3 copy is generated, name the format-4 source and warn that `--write` overwrites _(layer: general)_

---

## Must Fix

### 1. Gate 3i's printed remedy silently discards a hand edit of a format-3 copy
→ [finding_1.md](feat_flow_graph_schema_v2_skeptic_review/finding_1.md)

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. This section is empty.
