# Code Review: feat_graphscene_executor_interface

## Context

**Branch:** `feat_graphscene_executor_interface`
**Date:** 2026-11-25
**Reviewed:** the whole branch diff against `origin/dev`, all of it in the `graphscene` layer. It covers:
- the `Executor` protocol and the `Completed` / `Failed` results in `graphscene/src/graphscene/model/execution.py` (Task 1);
- `return_violations` in `graphscene/src/graphscene/adapters/return_schema.py` (Task 2);
- `StubExecutor` and its script types in `graphscene/src/graphscene/adapters/stub_executor.py` (Task 3);
- the two `__all__` lists, `graphscene/tests/test_public_surface.py` and `graphscene/README.md` (Task 4);
- the three new suites.

The diff is 12 files, +631 / −10. 10 run-artifact files excluded from the reviewed diff.

**What holds.**
- Every new module has its opening docstring with *"The rule:"* and *"Deliberately not covered"*, sits in the layer `.claude/context/graphscene.md` → `## The internal layers` puts it in, and has its own suite under the mirroring `tests/<layer>/`.
- `jsonschema` stays in `adapters`, and `model/execution.py` imports only the standard library and `graphscene.model.walk_actions`.
- The public names are in both `__all__` lists in the same order, appended after `"LedgerPassage"`, with matching `_EXPECTED` and `_DEFINED_IN` entries.
- The README's `## What it is` rows, the `adapters` layer row and the protocol bullet are updated, as scope-register rows 1–4 and 6 require.
- The contract the story plan fixes matches the code: `Completed(outcome, detail)` maps onto `Walker.next(outcome, node, detail)`, `FailureClass` is `Literal["infra", "agent", "undelivered"]`, and `kind` is a `ClassVar`.

**Tests.** No test-run conclusion is claimed here. This review ran no suite; the Run gates phase establishes pass or fail.

**Pass 0.**
- The sweep (`bash <MAIN_REPO>/scripts/review-sweep.sh --repo <repo_root>`) exited `0`: 0 hits, 0 findings.
- The new-exported-symbol caller check found every new export imported outside its defining file, by `graphscene/src/graphscene/facade/__init__.py` and the new suites. The task prompt states that the public surface and the stub's tests are this branch's only callers until #421 and #484, so no un-wired finding is raised.

**Parity.** Off (`phases.parity` is `false`).

**Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_graphscene_executor_interface_task_plan/` does not exist, so there was nothing to reconcile. The planning rounds' `## Incidental findings (not gating)` sections yielded no lead.

**Headline.** Finding 1 is the one Must Fix. `return_violations` reuses a pattern translator that, once it is handed arbitrary schemas, passes `patternProperties` regexes through untranslated, which breaks a lessons-ledger rule, and rewrites instance data under `const` / `enum`. A probe confirmed both.

**Open question.** One question is left for the maintainer, returned beside this review rather than filed as a finding. A `$ref` that does not resolve makes `return_violations` raise jsonschema's `_WrappedReferencingError`, which is not a `ValueError`. That contradicts its rule *"no `jsonschema` exception type crosses this boundary"*. A remote `$ref` also attempts a network fetch; the probe's connection to `example.invalid:443` was refused by the sandbox. Closing this needs either a new runtime dependency (`referencing`, to pass an empty `Registry` and catch `Unresolvable`) or an import of jsonschema's private `_RefResolutionError`. Adding a runtime dependency is the maintainer's decision under `.claude/context/graphscene.md` → `## What it may depend on`.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 3** — Refuse a NaN delay in `_check_delay` _(layer: graphscene)_
2. [ ] **Finding 2** — Test the stub's cancellation during a scripted delay _(layer: graphscene)_
3. [ ] **Finding 1** — Make `_ecma_patterns` walk by keyword position: translate `patternProperties` keys, leave `const` / `enum` / `default` / `examples` data untouched _(layer: graphscene)_

---

## Must Fix

### 1. The pattern translator `return_violations` reuses ignores keyword position: `patternProperties` keys pass through untranslated, and data under `const` / `enum` / `default` / `examples` gets rewritten
→ [finding_1.md](feat_graphscene_executor_interface_code_review/finding_1.md)

---

## Should Fix

### 2. The stub's cancellation during a scripted delay is promised but never tested
→ [finding_2.md](feat_graphscene_executor_interface_code_review/finding_2.md)

---

## Nice to Have

### 3. `_check_delay` accepts a NaN delay
→ [finding_3.md](feat_graphscene_executor_interface_code_review/finding_3.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None. `phases.parity` is `false`, so there is no reference implementation to diverge from.
