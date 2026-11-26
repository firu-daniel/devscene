# Skeptic Review: feat_graphscene_run_mode

## Context

**Branch:** `feat_graphscene_run_mode`
**Date:** 2026-11-26
**Reviewed:** the whole branch diff against `origin/dev`, 12 files, all in the `graphscene` layer:
- The sliding window in `graphscene/src/graphscene/engine/set_execution.py` → `_run_pass`.
- The run loop `graphscene/src/graphscene/engine/run_loop.py` → `start_run` / `continue_run` / `_drive`.
- `ExecutionLimits.max_concurrent_dispatches` and `RunExit` in `graphscene/src/graphscene/model/run_control.py`.
- The public-surface and README changes, and the engine, model and facade suites.

13 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/feat_graphscene_run_mode_code_review.md` and its two findings. Both are test-coverage gaps, now fixed. No branch-level architecture review and no parity review exists for this branch, and `phases.parity` is `false`. `harness-runs/lessons.md` holds no entry this finding repeats, and the planning rounds' `## Incidental findings (not gating)` grep returned no leads.

**Checks run:**
- **Check 1, wiring.** `start_run`, `continue_run` and `RunExit` are re-exported through `graphscene/src/graphscene/facade/__init__.py` and the package root. They are a library surface; the story names no in-repo caller (#423 and #424 build on it).
- **Check 2.** The parity leg is off. No host, region or address assembly is in the diff.
- **Check 3, citations.** The claims were opened and confirmed:
  - The lone-dispatch detail rule (`walker.py` → `_step`, "detail is recorded only for a gate of an open round").
  - Every `Walker` call going through `asyncio.to_thread`.
  - The window taking `seq` and attempt at start.
  - The window never starting a queued dispatch after a cancellation.
  - The story's claim that the existing `test_set_execution.py` cases are unchanged: only the header and imports moved.
- **Check 4.** No divergence is marked intentional.
- **Check 5, runtime.** I read the window's top-up, the timeout and the cancel paths, the record-then-halt ordering in `_drive`, and the refusal precedence. They hold. One runtime fault was found and confirmed by an executed probe. `_drive`'s `Wait` branch loops forever when the saved `pending` is itself a `Wait`. The library's own codec and model accept that state, so `continue_run` hangs instead of returning a `RunExit`.

**Headline:** one net-new Must Fix, a small engine-local change with its test.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Return a `Refused` from `_drive` when `Walker.current()` itself returns a `Wait`, instead of looping forever _(layer: graphscene)_

---

## Must Fix

### 1. `_drive` spins forever when the saved walk's `pending` is a `Wait`: `continue_run` never returns
→ [finding_1.md](feat_graphscene_run_mode_skeptic_review/finding_1.md)

---

## Should Fix

_None._

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, and no divergence was marked intentional, so this section is empty.
