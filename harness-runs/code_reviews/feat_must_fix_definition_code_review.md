# Code Review: feat_must_fix_definition

## Context

**Branch:** `feat_must_fix_definition`
**Date:** 2026-11-18
**Reviewed:** the whole branch diff against `origin/dev` (this checkout carries no local `dev`): the round-file check and refusal path in the flow walker and its tests, `plugin/instructions/finding_grades.md`, the grading agents moved onto it, the two planning cores, the samples, the decision record, the roadmap and the self-adopted copies. 27 run-artifact files excluded from the reviewed diff.

**Tests:** this review ran no test suite, and it did not execute the walker; the walker findings come from tracing `cli/templates/scripts/flow-walker.sh` by reading it. Whether the suites pass is the Run gates phase's to establish. **Pass 0:** the sweep exited 0 with 0 hits, so 0 became findings. The new-exported-symbol check found two new exports, `mustFixSection` and `plantMalformedReview` in `cli/test/helpers/walker.mjs`, and both have callers outside their defining file. **Parity:** `phases.parity` is `false`, so no parity check applies. **Per-unit reconciliation:** the folder `harness-runs/task_plan_point_reviews/feat_must_fix_definition_task_plan/` does not exist, so there was nothing to carry over. The planning rounds recorded no incidental findings.

The two copies of the walker and of its gate library are byte-identical, no competing grade definition remains under `plugin/`, and the `finding_grades.md` roster matches its citers. One Must Fix remains: a refused gate can be dispatched twice. The other three findings are small.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries top to bottom, and the committing role flips each one to `[x]` as that fix lands. `[ ]` markers anywhere else are informational only.

1. [x] **Finding 4** — Restore the `--skipped` column alignment in the walker header _(layer: cli, general)_
2. [x] **Finding 3** — Name `check-round-file` and its second caller in the watcher's script table _(layer: general)_
3. [x] **Finding 2** — Give the untrusted-instruction Must Fix a class row in `task-plan-reviewer` _(layer: plugin)_
4. [x] **Finding 1** — Keep a gate marked for re-dispatch out of the blocks `current` re-prints _(layer: cli, general)_

---

## Must Fix

### 1. `current` re-prints a refused gate the walker still counts as not out, so the gate is dispatched twice
→ [finding_1.md](feat_must_fix_definition_code_review/finding_1.md)

---

## Should Fix

### 2. `task-plan-reviewer` has no class row for an untrusted-instruction Must Fix
→ [finding_2.md](feat_must_fix_definition_code_review/finding_2.md)

### 3. `docs/watcher.md` omits `check-round-file` and the user-review fix-plan caller
→ [finding_3.md](feat_must_fix_definition_code_review/finding_3.md)

---

## Nice to Have

### 4. The walker header's `--skipped` line lost its column alignment
→ [finding_4.md](feat_must_fix_definition_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
