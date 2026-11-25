# Skeptic Review: feat_graphscene_executor_interface

## Context

**Branch:** `feat_graphscene_executor_interface`
**Date:** 2026-11-25
**Reviewed:** the whole-branch diff against `origin/dev`, 14 files, all in the `graphscene` layer. That covers `model/execution.py`, `adapters/return_schema.py`, `adapters/stub_executor.py`, the keyword-position rewrite of `_ecma_patterns` in `adapters/schema.py` (code-review Finding 1's fix), both `__all__` lists, the README and the new suites. 14 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/feat_graphscene_executor_interface_code_review.md` and its Findings 1–3, all applied. That includes its open question on an unresolvable `$ref` raising `_WrappedReferencingError`. No parity review exists (`phases.parity` is `false`), and no architecture branch review exists for this branch. The planning rounds' `## Incidental findings (not gating)` sections gave no lead.

**Adversarial checks.**
- **Check 1 (wiring).** The task prompt states that the public surface and the stub's suites are the only callers until #421 and #484. I confirmed the prompt says this. Every new export is imported by `graphscene/src/graphscene/facade/__init__.py` and a suite. `_DATA_KEYWORDS` and `_NAMED_SUBSCHEMAS` are consumed by `_ecma_patterns`, which both `_validator` and `return_violations` call.
- **Check 2.** The parity leg is off. No runtime address is assembled.
- **Check 3 (citations).** Every cited source resolves:
  - `.claude/context/docs-retrieval.md` → *"Async code is driven with `asyncio.run(…)`"*;
  - `Walker.next(outcome, node, detail)` in `engine/walker.py`;
  - the `kind` `ClassVar` precedent in `model/walk_actions.py`;
  - the two `harness-runs/lessons.md` rules;
  - the *"failed the schema the executor names"* phrase in `model/execution.py`.

  The one claim that does not hold is Task 2's *"`validator_for(…, default=Draft7Validator)` honours a declared `$schema`"*, which is Finding 1.
- **Check 4.** No divergence is marked intentional.
- **Check 5.** Cancellation is re-raised on both the stall and the delay path. The concurrent-finish test is deterministic, because two `sleep(0)` calls resume in FIFO order. `requires-python >=3.11` makes `TimeoutError` the right exception for `asyncio.wait_for`.

**Headline.** One Must Fix and one Should Fix, both in `return_violations`. Probes confirmed both: `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_probe.py` and `… probe harness-runs/scratch/skeptic_probe2.py`.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — Correct the `Any`-cast comment in `return_violations`: a non-JSON value is reported only where a keyword checks it _(layer: graphscene)_
2. [x] **Finding 1** — Refuse a `$schema` that names no draft jsonschema recognises in `return_violations`, instead of silently applying draft-07 _(layer: graphscene)_

---

## Must Fix

### 1. `return_violations` silently validates a schema with an unrecognised `$schema` as draft-07, so the draft the schema declares is never applied
→ [finding_1.md](feat_graphscene_executor_interface_skeptic_review/finding_1.md)

---

## Should Fix

### 2. The comment justifying the `Any` cast in `return_violations` claims a non-JSON value is reported as a violation, and it is not
→ [finding_2.md](feat_graphscene_executor_interface_skeptic_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None. `phases.parity` is `false`, and no divergence on this branch is marked intentional.
