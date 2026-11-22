# Code Review: feat_graphscene_review_loop_pattern

## Context

**Branch:** `feat_graphscene_review_loop_pattern`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`: 22 files, +655 / -69. 17 run-artifact files were excluded from the reviewed diff. The diff covers:
- the new engine module `graphscene/src/graphscene/engine/review_loop.py` and its suite (Task 1);
- the walk's writer and gate dispatch routed through it (Task 2);
- checks 8 and 9 split into round rules and review-loop rules (Task 3);
- `writer` / `counter` / `convergingFrom` made an optional group in the schema, the model and the builder, with the `valid_plain_round.json` and `schema_negative_writer_without_counter.json` fixtures (Task 4);
- the plain-round engine and facade cases (Tasks 5 and 6);
- `graphscene/README.md` (Task 7);
- the root `package.json` scripts, `ROADMAP.md` and `docs/development.md` (Task 8).

**Pass 0.**
- **Grep sweep:** `review-sweep.sh` exited `0`, with 0 hits and so 0 findings.
- **Caller check:** every new exported symbol (`ReviewLoop`, `review_loop`, `review_loops`, `is_converging`) has callers outside its defining file, in `engine/static_check.py` and `engine/transitions.py`. None is dead.

**Pass 2.** The supplied `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_graphscene_review_loop_pattern_task_plan/`) does not exist, so there was nothing to reconcile. Pass 2 was a no-op. The planning rounds' `## Incidental findings (not gating)` sections gave no leads.

**Tests.** Every accompanying item the `graphscene` and `general` conventions documents require is present:
- the new module's opening docstring with *"The rule:"*;
- its own suite, `graphscene/tests/engine/test_review_loop.py`, which opens with *"The rule this file exists to enforce"*;
- the new schema negative, wired into `validate:graphscene-schema:negative`, `_FIXTURE_NAMES` and `_SCHEMA_NEGATIVES` (path `nodes.review_round`);
- the new valid fixture, listed in `validate:graphscene-schema` and `_FIXTURE_NAMES`.

This review ran no suite. Whether the tests pass is for the Run gates phase to establish.

**Behaviour.** I checked the split of checks 8 and 9 against the walk:
- A non-verdict, non-held gate outcome on a plain round is still refused at run time by `record_gate`.
- A gate shared by two plain rounds is still caught by round rule 9 (i).
- The harness graph `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` declares `writer` on `plan_round`, so it keeps every clause.
- No reader of the three keys remains outside `review_loop.py`, `references.py` and `static_check.py`.

**Parity.** Not applicable: `phases.parity` is `false`.

Three findings follow, none of them a Must Fix.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 3** — Rejoin the stub line "key order; within" in the `references.py` module docstring _(layer: graphscene)_
2. [ ] **Finding 2** — Drop the stale "the builder require them" docstring and "become optional" comment, and test `review_loop` on the built plain-round fixture _(layer: graphscene)_
3. [ ] **Finding 1** — Test the round-node schema dependency clauses beyond writer-without-counter _(layer: graphscene)_

---

## Must Fix

_None._

---

## Should Fix

### 1. Two schema dependency clauses the branch adds are never exercised: a writer-less round carrying `plan`, `revisionNote`, `counter` or `convergingFrom`, and a writer with no `convergingFrom`
→ [finding_1.md](feat_graphscene_review_loop_pattern_code_review/finding_1.md)

### 2. `test_review_loop.py` and `review_loop.py` still say the three review-loop fields are required, which Task 4 made false
→ [finding_2.md](feat_graphscene_review_loop_pattern_code_review/finding_2.md)

---

## Nice to Have

### 3. The reflowed `references.py` docstring leaves a stub line, "key order; within"
→ [finding_3.md](feat_graphscene_review_loop_pattern_code_review/finding_3.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

Empty: `phases.parity` is `false`, so there is no reference implementation to diverge from.
