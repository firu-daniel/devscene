# Skeptic Review: feat_graphscene_review_loop_pattern

## Context

**Branch:** `feat_graphscene_review_loop_pattern`
**Date:** 2026-11-22

**What I reviewed.** The whole-branch diff against `origin/dev`, since `defaultBranch` is `dev`: 22 files, +697 / -76. 22 run-artifact files were excluded from the reviewed diff. I read it segment by segment:
- the new `graphscene/src/graphscene/engine/review_loop.py`;
- the walk's dispatch in `transitions.py`;
- the split of checks 8 and 9 in `static_check.py`;
- `references.py`;
- the schema `dependencies`, the model and the builder;
- the engine and facade tests, the two new fixtures, `package.json`, `ROADMAP.md`, `docs/development.md` and `graphscene/README.md`.

I checked the story index's claims against the code, `rounds.py` and `transitions.py` → `open_round` / `close_round`. I also checked them against the harness graph `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, where `plan_round` declares `writer`, `counter` and `convergingFrom`. Both validators honour the draft-07 `dependencies` keyword: `Draft7Validator` in `graphscene/src/graphscene/adapters/schema.py`, and the default `ajv` export in `schemas/validate.mjs`.

**De-duplicated against:** `harness-runs/code_reviews/feat_graphscene_review_loop_pattern_code_review.md` and its three findings: the untested schema dependency clauses, the stale docstring and comment, and the stub docstring line. No parity review exists, because `phases.parity` is `false`. No architecture branch review exists for this branch. The planning rounds' `## Incidental findings (not gating)` sections gave no leads.

**Headline.** Check 1 holds: every new helper has a caller, and no reader of the three keys remains outside `review_loop.py`, `references.py` and `static_check.py`. Check 3 does not hold. The story gates check 8's graph-wide clause on the graph declaring a review loop, and justifies that by saying check 3 still refuses an uncapped fail cycle. Check 3's successor relation leaves out a round's fan-out, and it relies on that clause to make the omission safe. An executed probe shows that a plain-round graph with an uncapped fail cycle through the fan-out loads and walks with no cap. One finding follows, a Must Fix, and its fix was verified by probe against every fixture and every existing static-check case.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Walk a round's fan-out in check 3 for every fail edge but a gate's own, so an uncapped fail cycle through a plain round is refused _(layer: graphscene)_

---

## Must Fix

### 1. On a graph with no review loop, an uncapped fail cycle through a plain round's fan-out passes every static check and walks forever
→ [finding_1.md](feat_graphscene_review_loop_pattern_skeptic_review/finding_1.md)

---

## Should Fix

_None._

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. Three of the story's choices survived check 4. Each is a split the story argued clause by clause, and I verified the walk dependence of each:
- **Round rules 8 (gates are dispatch nodes), 9 (i) and 9 (iii) stay on every round.** `open_round` asserts every gate is a `DispatchNode`. `record_gate` never follows a verdict edge's `to`, and `open_round` never follows a skip's `to`.
- **9 (ii) and 9 (iv) are review-loop only.** A plain round with only a pass-verdict gate closes on pass. No writer exists to check.
- **9 (v) is review-loop only, so a plain round may be opened from any node.** This is walkable. The cycle it enables is Finding 1's concern, and the fix places it in check 3, not in 9 (v).
