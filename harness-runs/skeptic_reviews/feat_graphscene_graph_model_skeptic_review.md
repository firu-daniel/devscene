# Skeptic Review: feat_graphscene_graph_model

## Context

**Branch:** `feat_graphscene_graph_model`
**Date:** 2026-11-20

**Reviewed:** the whole-branch diff against `origin/dev`. This is a run copy, so there is no local `dev` ref. The diff covers 14 files and +1229 / −70 lines:

- `graphscene/src/graphscene/errors.py`, `model.py`, `loader.py`, `vocabulary.py` and `__init__.py`.
- Their tests under `graphscene/tests/`.
- `graphscene/README.md`, `docs/development.md` and `ROADMAP.md`.

15 run-artifact files excluded from the reviewed diff.

**De-duplicated against** the committed code review, `harness-runs/code_reviews/feat_graphscene_graph_model_code_review.md`, and its findings 1–3:

- the strict-`mypy` `_strings` annotation;
- the `ruff` failures in two test files;
- the integral-float `TypeError` in `_int`.

All three are fixed on the branch. No parity review exists for this branch, because `phases.parity` is `false`. No end-of-branch architecture review exists either; only `harness-runs/architecture_reviews/feat_graphscene_graph_model/review_0.md` from planning was present. The planning rounds carry no `## Incidental findings (not gating)` section.

**Adversarial checks.**

- **Check 1 (wiring).** Every new symbol is reached: `load_graph_file` → `load_graph` → schema, then `vocabulary_violations`, then `build_flow_graph`, and every public name is in `__all__`. No caller outside `graphscene/` uses the changed `vocabulary_violations` return type.
- **Check 2.** The parity leg is off. No runtime address is assembled.
- **Check 3 (citations).** "gate 13's leg `13g`" in `docs/development.md` resolves to `scripts/run-gates.sh` → `13g`. The issue numbers come from the task prompt.
- **Check 4.** No divergence is marked intentional.

**Headline.** The new loader is wired, but its validity contract leaks in two places. Python's `re` reads the schema's `pattern`s more loosely than ECMA-262 / `ajv`, so `load_graph` returns graphs that gate 3g's `ajv` rejects (Finding 1, Must Fix). A non-UTF-8 file escapes as `UnicodeDecodeError` instead of a parse-stage `GraphError` (Finding 2, Should Fix).

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom. The committing role flips each one to `[x]` as that fix's commit lands. Each entry resolves to `harness-runs/skeptic_reviews/feat_graphscene_graph_model_skeptic_review/finding_<K>.md` through its `**Finding K**` reference.

1. [x] **Finding 2** — Read `load_graph_file`'s file as bytes and turn a failed UTF-8 decode into a parse-stage `GraphError`, with a loader test _(layer: graphscene)_
2. [x] **Finding 1** — Match the schema's `pattern`s as ECMA-262 in the loader's validator, so a trailing newline or a `.` against a line terminator is rejected as `ajv` rejects it _(layer: graphscene)_

---

## Must Fix

### 1. `load_graph` accepts strings the schema's `pattern`s reject, because Python's `re` reads `$` and `.` differently from ECMA-262 and `ajv`
→ [finding_1.md](feat_graphscene_graph_model_skeptic_review/finding_1.md)

---

## Should Fix

### 2. `load_graph_file` raises `UnicodeDecodeError`, not a parse-stage `GraphError`, on a file that is not UTF-8
→ [finding_2.md](feat_graphscene_graph_model_skeptic_review/finding_2.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. No divergence on this branch is marked intentional, so this section is empty.
