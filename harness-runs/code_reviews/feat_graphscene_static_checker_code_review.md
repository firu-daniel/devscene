# Code Review: feat_graphscene_static_checker

## Context

**Branch:** `feat_graphscene_static_checker`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`, 23 files. That covers:

- the new reference check, `graphscene/src/graphscene/engine/references.py` (Task 1);
- the static checker with its five graph checks and six `static_negative_*.json` fixtures, `graphscene/src/graphscene/engine/static_check.py` (Task 2);
- the vocabulary check moved onto `FlowGraph`, and loading reordered to schema → build → vocabulary → static, with the new `Stage` member `"static"` (Task 3);
- the `static_violations` export and the loader cases (Task 4);
- `graphscene/README.md` (Task 5);
- the `validate:graphscene-schema` wiring, `docs/development.md` **Gate 3** and the `ROADMAP.md` GraphScene row (Task 6).

12 run-artifact files were excluded from the reviewed diff.

**Pass 0.** The sweep (`review-sweep.sh`) exited `0`: no hits, so no findings. The new-exported-symbol caller check covered every layer path. It found three new or changed public top-level functions, and each one is called outside the file that defines it:

- `reference_violations` is called from `engine/static_check.py`;
- `static_violations` is called from `facade/loading.py` and re-exported in both `__all__` lists;
- `vocabulary_violations` is called from `facade/loading.py`.

**Tests.** Every test the graphscene conventions require is present:

- one planted case per clause in `tests/engine/test_references.py` and `tests/engine/test_static_check.py`;
- the six static negatives, each in its `_NEGATIVES` list and in `_STATIC_NEGATIVES` in `tests/facade/test_loading.py`, and listed in `validate:graphscene-schema`;
- the `_EXPECTED` and `_DEFINED_IN` entries in `tests/test_public_surface.py`;
- the existing expected `Violation` values in `tests/engine/test_vocabulary.py`, all unchanged.

No new test reads a tree of repository files, so no new `treeGuards` entry is owed. This review ran no test suite; whether the tests pass is for the Run gates phase.

**Probes.** Each was run with `bash scripts/python-service.sh --package graphscene probe <file under harness-runs/scratch/>`.

- Every `static_negative_*.json` file fails `load_graph` at stage `static` with exactly the one violation its test expects.
- `valid_generic.json` has no static violation.
- The harness's own format-4 graph, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, loads clean through the new static stage.
- A probe of the check-9 report order is Finding 1.
- A probe of an undeclared `resumeOutcome` is the question in the return. No stage refuses it. The gap was already there before this branch, and closing it is a scope decision, so it is not filed here as a finding.

**Parity.** Parity is off (`phases.parity` is `false`).

**Conventions.** The plan recorded that `.claude/context/graphscene.md` → `## Errors and the loading order` and `## Example` (with `## The model and its wire form`) are now stale, as are `.claude/context/conventions.md`'s rejected-fixture row. It filed this as `corpus_staleness` for a supervised `/devscene:analyze` re-run, not as an edit on this branch. Reconciling the per-unit reviews was a no-op: the `per_task_findings_root` folder does not exist.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — State `round-fan-out`'s real report order in the `static_check.py` and `test_static_check.py` docstrings _(layer: graphscene)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `static_check.py` says each check reports nodes in key order, but `round-fan-out` does not
→ [finding_1.md](feat_graphscene_static_checker_code_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

_Empty: `phases.parity` is `false`._
