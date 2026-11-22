# Skeptic Review: feat_graphscene_walker_engine

## Context

**Branch:** `feat_graphscene_walker_engine`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`, 23 files, read adversarially:

- `graphscene/src/graphscene/model/` (`walk_actions.py`, `walk_state.py`);
- `engine/` (`transitions.py`, `rounds.py`, `walker.py`);
- `adapters/` (`walk_json.py`, `state_file.py`);
- the public surface, `graphscene/README.md`, `ROADMAP.md` and the suites.

I read the engine against `cli/templates/scripts/flow-walker.sh` and the `cli/test/flow-walker*.test.mjs` suites, which the task prompt names as the expected behaviour. I walked the harness's own format-4 graph through the public `Walker` in a probe.

22 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/feat_graphscene_walker_engine_code_review.md` and its two findings: the stale `skipped` entry and the unused `open_gates` keyword, both applied. No business-parity branch review exists, because `phases.parity` is `false`. No architecture branch review exists for this branch. The planning rounds hold no `## Incidental findings (not gating)` section. `harness-runs/lessons.md` has no entry covering this.

**Checks run:**

1. **Wiring.** `Walker`, `FileStateStore`, the codec and every transition have callers.
2. **Spec.** The parity leg is inert. No runtime address is assembled.
3. **Citations.** The one citation, `graphscene/README.md` → `## The boundary`, resolves and says what is claimed.
4. **Intentional divergences.** None is declared.
5. **Runtime.** The lock, the atomic replace, the held join, caps, `{cap}` / `{open_gates}` and the converging flag match the bash walker.

**Headline.** One net-new Must Fix. An interrupt on a revision writer (`<ask>` on `plan_writer` after a failed `plan_round`) loses the closed round's records, so the resumed revision is dispatched with `closed_round=()`. A probe confirmed it. The bash suites the task prompt names as expected behaviour assert the opposite.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Carry the closed round through an interrupt so a resumed revision writer keeps its gate records _(layer: graphscene)_

---

## Must Fix

### 1. Resuming an interrupted revision writer drops its closed round, so the re-dispatched revision has no gate records to revise against
→ [finding_1.md](feat_graphscene_walker_engine_skeptic_review/finding_1.md)

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None. No divergence on this branch is marked intentional, and `phases.parity` is `false`.
