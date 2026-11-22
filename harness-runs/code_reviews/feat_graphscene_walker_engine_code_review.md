# Code Review: feat_graphscene_walker_engine

## Context

**Branch:** `feat_graphscene_walker_engine`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`, which is 23 files. They are:

- the walk's actions and state in `graphscene/src/graphscene/model/` (`walk_actions.py`, `walk_state.py`; Tasks 1–2);
- the walk in `graphscene/src/graphscene/engine/` (`transitions.py`, `rounds.py`, `walker.py`; Tasks 3–5);
- the JSON codec and the locked file store in `graphscene/src/graphscene/adapters/` (`walk_json.py`, `state_file.py`; Tasks 6–7);
- the public surface in `graphscene/src/graphscene/__init__.py` and `facade/__init__.py`, with `graphscene/tests/test_public_surface.py` (Task 8);
- `graphscene/README.md` (Task 9) and `ROADMAP.md` (Task 10);
- the suites under `graphscene/tests/` that ship with these.

19 run-artifact files excluded from the reviewed diff.

**Conclusions:**

- **Tests.** Every new module has its own suite at `graphscene/tests/<layer>/test_<module>.py`, as `.claude/context/graphscene.md` → `## What accompanies a new module` requires. Each suite opens with *"The rule this file exists to enforce"*, uses no mocking aid and hand-writes its expected values. Whether the suites pass is for the Run gates phase to establish: this review ran no suite.
- **Layer rules.** The import direction holds: `engine` imports `model` only, `adapters` imports `model` and the standard library, and only `facade` combines them. Both `__all__` lists and `_EXPECTED` / `_DEFINED_IN` carry the 21 new names in the same order. The `_EXPECTED[7:28]` bound covers exactly the 21 `flow_graph` names.
- **Pass 0 sweep (a).** The main checkout's `scripts/review-sweep.sh`, run with `--repo` set to this checkout's root, exited `0` with no hits: 0 candidates, 0 findings. The sweep document was read from `origin/dev`, because this checkout has no local `dev` branch.
- **Pass 0 caller check (b).** Every new exported name has a caller outside its defining file, searched over every `layers[].path`:
  - `Walker` and `FileStateStore` are re-exported from `facade/__init__.py`.
  - The `walk_actions` and `walk_state` types are used in `engine`, `adapters` and `facade`.
  - `state_to_json` and `state_from_json` are used by `state_file.py`.
  - `arrive`, `follow_edge`, `take_binding`, `open_round`, `close_round` and `record_gate` are used by `rounds.py` and `walker.py`.
- **Parity.** `phases.parity` is `false`, so no parity cross-check ran.
- **Other inputs.** The planning rounds' review folders hold no `## Incidental findings (not gating)` section for this branch. `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_graphscene_walker_engine_task_plan/`) does not exist, so Pass 2 had nothing to reconcile.
- **Not a finding: a stale conventions sentence.** `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` says the library *"keeps no persisted or shared state"*, and `StateStore` / `FileStateStore` now make that false. A conventions document is not a fix target for this loop, and the story index's scope register, row 1, already routes the sentence to `corpus_staleness` as a `stale-rule` entry.

Finding 1 was confirmed by a probe run through `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/walker_stale_skip_probe.py`, whose output is recorded in the finding. Two findings remain.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 2** — Remove the unused `open_gates` keyword and its false comment from `arrive` _(layer: graphscene)_
2. [ ] **Finding 1** — Clear a node's `skipped` entry on an arrival where no skip holds, so a cap stop counts a gate dispatched after an earlier skip _(layer: graphscene)_

---

## Must Fix

### 1. A gate skipped on an earlier arrival keeps its `skipped` entry after it is dispatched, so a cap stop's `round_counts` drops a gate that ran
→ [finding_1.md](feat_graphscene_walker_engine_code_review/finding_1.md)

---

## Should Fix

### 2. `arrive` declares an `open_gates` keyword no caller passes, and its comment says the walker uses it
→ [finding_2.md](feat_graphscene_walker_engine_code_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
