# Code Review: feat_graphscene_graph_model

## Context

**Branch:** `feat_graphscene_graph_model`
**Date:** 2026-11-20
**Reviewed:** the whole branch diff against `origin/dev`. This is a run copy, so there is no local `dev` ref. The diff covers 14 files and +1215 / −71 lines: `Violation` / `GraphError` with the `vocabulary_violations` return-type change (Task 1), the typed model `graphscene.model` (Task 2), the loader `graphscene.loader` (Task 3), the package's public `__all__` and `graphscene/README.md` (Task 4), and the `docs/development.md` and `ROADMAP.md` records (Task 5), plus their tests. 11 run-artifact files excluded from the reviewed diff.

**Tests.** Every new module ships with its own suite: `test_errors.py`, `test_model.py`, `test_loader.py` and `test_public_surface.py`. The reviewer ran `bash scripts/python-service.sh --package graphscene test`, and all 102 cases pass. The package's other two gate-13 legs do not pass on this branch:

- `typecheck` exits 1 on two strict-`mypy` errors in `vocabulary.py` (Finding 1).
- `lint` exits 1 on an unsorted import and an unformatted file among the new tests (Finding 2).

**Behaviour.** The model mirrors the format-4 schema key for key, and was checked against `graphscene/src/graphscene/schemas/flow-graph.schema.json` definition by definition. Node-id references stay `str`. No harness name appears, and the boundary holds. One behaviour defect was found. `Draft7Validator` accepts an integral float such as `3.0` as an `integer`, but the builder refuses one with a `TypeError`. So `load_graph` raises a non-`GraphError` on a graph both validators accept (Finding 3).

**Pass 0.** The sweep (`review-sweep.sh`) exited 0 with 0 hits, so 0 findings came from it. The new-exported-symbol caller check found every new public `def` / `class` under `graphscene/src` referenced outside its defining file (by `__init__.py`, `loader.py` or `vocabulary.py`). No dead symbol.

**Pass 2.** `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_graphscene_graph_model_task_plan/`) does not exist, so there were no per-unit findings to reconcile. The planning rounds carry no `## Incidental findings (not gating)` section. `phases.parity` is `false`, so there is no parity cross-check and the call-out section below is empty.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom. The committing role flips each one to `[x]` as that fix's commit lands. Each entry resolves to `harness-runs/code_reviews/feat_graphscene_graph_model_code_review/finding_<K>.md` through its `**Finding K**` reference.

1. [x] **Finding 1** — Restore `_strings`'s `list[str]` return annotation in `vocabulary.py` so strict `mypy` passes _(layer: graphscene)_
2. [ ] **Finding 2** — Sort the `test_model.py` import block and collapse the two one-element assertion tuples in `test_loader.py` so `ruff` passes _(layer: graphscene)_
3. [ ] **Finding 3** — Accept an integral float where the schema takes an integer in the model's `_int`, with a loader test _(layer: graphscene)_

---

## Must Fix

### 1. `_strings` in `vocabulary.py` was re-annotated `list[Violation]`, so the package's strict `mypy` fails
→ [finding_1.md](feat_graphscene_graph_model_code_review/finding_1.md)

### 2. Two new test files fail the package's `ruff` lint: an unsorted import in `test_model.py` and two unformatted assertions in `test_loader.py`
→ [finding_2.md](feat_graphscene_graph_model_code_review/finding_2.md)

### 3. `load_graph` raises `TypeError` on a graph the schema accepts when an integer field is written as an integral float (`3.0`)
→ [finding_3.md](feat_graphscene_graph_model_code_review/finding_3.md)

---

## Should Fix

_None._

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
