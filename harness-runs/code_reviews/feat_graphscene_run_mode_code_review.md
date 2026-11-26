# Code Review: feat_graphscene_run_mode

## Context

**Branch:** `feat_graphscene_run_mode`
**Date:** 2026-11-26
**Reviewed:** the whole branch diff against `origin/dev`, 12 files, all in the `graphscene` layer:
- `ExecutionLimits.max_concurrent_dispatches` and the `RunExit` alias in `graphscene/src/graphscene/model/run_control.py` (Task 1).
- The sliding window in `graphscene/src/graphscene/engine/set_execution.py` → `_run_pass` (Task 2).
- The new run loop `graphscene/src/graphscene/engine/run_loop.py` → `start_run` / `continue_run` / `_drive` (Task 3).
- The public-surface additions, the README rows and the facade suite `graphscene/tests/facade/test_run_mode.py` (Task 4).
- The engine and model suites that ship with them.

13 run-artifact files excluded from the reviewed diff.

**Conventions.** The `graphscene` layer's rules are met:
- The engine imports only `model` and the standard library.
- The new module opens with *"The rule:"* and *"Deliberately not covered:"*, has its README row, and has its own suite, `tests/engine/test_run_loop.py`.
- The three new public names are in both `__all__` lists, in the same order, and in `_EXPECTED` / `_DEFINED_IN`.
- `ExecutionLimits` refuses an out-of-range window with the exact `ValueError` text.
- No `#484` reference survives outside `harness-runs/`.

Every accompanying test the conventions require is present. Whether they pass is the Run gates phase's to establish; this review ran no suite.

**Behaviour, checked by reading and by probe.** I read `_drive` against `Walker` and `graphscene/src/graphscene/engine/rounds.py` → `record_gate`:
- A partial round saves its pending as a cut-down `DispatchSet`, not a `Wait`, so `continue_run` → `Walker.current()` cannot loop on a `Wait`.
- A mid-set `Halt` saves every settled record before it returns.
- The window takes `seq` and attempt at start, keeps the wait for a slot outside `run_timeout_seconds`, and starts nothing more once cancelled.

Two probes, run with `bash scripts/python-service.sh --package graphscene probe <file>`, confirmed three behaviours: a half-recorded round resumes over a real `FileStateStore`, a gate's detail is saved, and a refused gate record leaves its siblings recorded. None of the three has a test case. Those gaps are the two findings below; both are test-coverage gaps, and no Must Fix was found.

**Pass 0.**
- The `review-sweep.sh` grep sweep exited `0`: 0 hits, 0 findings.
- The new-exported-symbol caller check covered every `layers[].path`. `start_run`, `continue_run` and `RunExit` are each imported outside their defining file, by `graphscene/src/graphscene/facade/__init__.py`. Nothing is unwired.

**Other sources.**
- The planning rounds' `## Incidental findings (not gating)` grep returned no entries.
- The per-unit findings root `harness-runs/task_plan_point_reviews/feat_graphscene_run_mode_task_plan/` does not exist, because per-unit review was off, so Pass 2 had nothing to reconcile.
- Parity: `phases.parity` is `false`; no parity check ran.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Add the gate-detail and refusal-keeps-siblings cases to `test_run_loop.py` _(layer: graphscene)_
2. [ ] **Finding 2** — Add a mid-round STOP and `continue_run` resume over a real `FileStateStore` to `test_run_mode.py` _(layer: graphscene)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `test_run_loop.py` has no case for two clauses of the run loop's rule: a gate's detail is recorded, and a refused record does not stop its siblings being recorded
→ [finding_1.md](feat_graphscene_run_mode_code_review/finding_1.md)

### 2. The story's top risk "resume a half-recorded round … over a real `FileStateStore`" has no case: `test_run_mode.py` only halts between sets
→ [finding_2.md](feat_graphscene_run_mode_code_review/finding_2.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
