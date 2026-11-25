# Code Review: feat_graphscene_execution_rules

## Context

**Branch:** `feat_graphscene_execution_rules`
**Date:** 2026-11-25
**Reviewed:** the whole branch diff against `origin/dev`: 16 files, all in the `graphscene` layer. That covers the new `model/run_control.py` (Task 1); `engine/safety.py` and `engine/breaker.py` (Task 2); `engine/attempts.py` (Task 3); `engine/set_execution.py` (Task 4); the public-surface additions in both `__init__.py` files and `graphscene/README.md` (Task 5); the caller-side suite `tests/facade/test_execution_rules.py` (Task 6); and each module's own suite. 18 run-artifact files were excluded from the reviewed diff.

**Conventions.** Every rule in `.claude/context/graphscene.md` is met:

- Each new module sits in the right layer. `engine` imports only `model` and the standard library, and `model` imports only the standard library.
- Each module opens with a docstring carrying *"The rule:"* and *"Deliberately not covered"*, and has its own suite under `tests/<layer>/`.
- Each new public name is in both `__all__` lists in the same order, and in `_EXPECTED` / `_DEFINED_IN`.
- The README's `## What it is` and `## The layers` rows were updated.
- Every model type is `@dataclass(frozen=True)`.
- No added line is over 100 characters.

**Tests.** This review ran no suite. Whether the tests pass is for the Run gates phase to establish.

**Pass 0 sweep.** `review-sweep.sh` exited `0` with no hits, so no hit became a finding. The new-exported-symbol caller check found every new name re-exported through `graphscene.facade` and the package root and exercised by the branch's suites. The task prompt names exactly that as this milestone's caller set ("The public surface and its tests are this branch's callers"), so no name is dead.

**Parity.** `phases.parity` is `false`, so no parity review ran. The branch moves the planning driver's rules (`cli/templates/scripts/lib/planning-driver-lib.sh`, described in `docs/flow-graph-walker.md` → `## 5. The two drivers`). Those rules were read where the engine's docstrings cite them. One divergence came out of that reading: Finding 1, confirmed by a probe run through `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/breaker_retry_probe.py`.

**Other inputs.**

- The planning rounds carried no `## Incidental findings (not gating)` section.
- `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_graphscene_execution_rules_task_plan/`) does not exist, so Pass 2 was a no-op.
- The story's scope register records `.claude/context/graphscene.md` → *"running a node … are the host's"* as a `stale-rule` entry. That is a conventions-document refresh, not a fix on this branch.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 3** — Say in `execution.py` that `execute_set` applies the stall deadline, not #484 _(layer: graphscene)_
2. [x] **Finding 4** — Document that a cancelled run takes a `seq` but writes no `Launch` row _(layer: graphscene)_
3. [x] **Finding 2** — Word the breaker's halt as sets that had an undelivered result _(layer: graphscene)_
4. [x] **Finding 1** — Leave the undelivered breaker unchanged on an infrastructure-only retry pass _(layer: graphscene)_

---

## Must Fix

### 1. An infrastructure-only retry pass resets the undelivered breaker, so a flapping provider parks the node as a failure instead of tripping the breaker
→ [finding_1.md](feat_graphscene_execution_rules_code_review/finding_1.md)

---

## Should Fix

### 2. The breaker's halt says "consecutive sets delivered nothing" even when those sets delivered other nodes' outcomes
→ [finding_2.md](feat_graphscene_execution_rules_code_review/finding_2.md)

### 3. `execution.py` still says the run deadline is the caller's and #484's, though `execute_set` now applies it
→ [finding_3.md](feat_graphscene_execution_rules_code_review/finding_3.md)

### 4. A run cancelled by `execute_set`'s own cancellation or by a sibling's defect takes a `seq` but writes no `Launch` row, and nothing says so
→ [finding_4.md](feat_graphscene_execution_rules_code_review/finding_4.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
