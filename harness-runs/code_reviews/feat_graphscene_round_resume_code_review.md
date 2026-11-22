# Code Review: feat_graphscene_round_resume

## Context

**Branch:** `feat_graphscene_round_resume`
**Date:** 2026-11-22
**Reviewed:** the whole branch diff against `origin/dev`. That covers the `RoundResume` model type in `graphscene/src/graphscene/model/walk_state.py` (Task 1), `enter_round` in `graphscene/src/graphscene/engine/rounds.py` (Task 2), the keyword-only `resume` argument and its refusals (`_unplaceable`) on `Walker.start` in `graphscene/src/graphscene/engine/walker.py` (Task 3), the public-surface export in both `__all__` lists, the `graphscene/README.md` rows and the end-to-end facade case in `graphscene/tests/facade/test_walking.py` (Task 4), and the GraphScene row in `ROADMAP.md` (Task 5), plus the suites in `graphscene/tests/engine/test_rounds.py`, `graphscene/tests/engine/test_walker.py`, `graphscene/tests/model/test_walk_state.py` and `graphscene/tests/test_public_surface.py`. 11 run-artifact files excluded from the reviewed diff.

**Pass 0.** (a) `bash <MAIN_REPO>/scripts/review-sweep.sh --repo <repo_root>` exited `0`: 0 hits, so 0 findings. The sweep document came from `origin/dev`, because this run copy has no local `dev` ref. (b) The diff adds two non-test definitions under `graphscene/src`. `RoundResume` has call sites in `engine/walker.py`, `facade/__init__.py` and `__init__.py`. `enter_round` has its call site in `engine/walker.py` → `Walker.start`. The search covered every `layers[].path` scope, and neither symbol is dead.

**Judgment pass.** `enter_round` records every resumed record through the existing `record_gate`. So the refusal texts for an undeclared outcome and for a neither-verdict-nor-held outcome, the report update, the held join and the close all stay in one place, with no second copy of the join. I traced `open_round` → `close_round` → `follow_edge` in `graphscene/src/graphscene/engine/transitions.py` for each of these cases: all gates skipped with records given (`due` resolves to `()`, so each record is refused), a partial resume (the trimmed `DispatchSet` becomes `draft.pending`, so `current` re-returns it), a complete FAIL (`advance` raises the round number and the writer dispatches at *n + 1*), and a held record (the first held edge in `gates` order). Each matches what `next` would do from the same position. Every `start` refusal returns before `WalkDraft.fresh`, inside the lock, and leaves the store unwritten; each refusal case asserts `MemoryStore.writes` unchanged. The walk-state document stays `"version": 1` (`adapters/walk_json.py` is untouched; the facade case asserts `saved["version"] == 1` through `FileStateStore`). The public name is in both `__all__` lists in the same position, and in `_EXPECTED` and `_DEFINED_IN`. Each changed module docstring states its rule. Each changed suite opens with *"The rule this file exists to enforce"*, and refusals are asserted with exact text. I checked all of this by reading the diff and the surrounding source. This review ran no suite, so whether the suites pass is the gates phase's to establish.

**Carried state, not a finding.** `.claude/context/graphscene.md` → `## The walk` still says *"only `start` replaces a saved walk, setting every counter and round number to 0"*, which Task 3 makes false for a resumed round. A conventions document is not an implementer's target. The story plan's scope register (row 3) records it as `stale-rule` for a supervised `/devscene:analyze graphscene` re-run or a hand edit, so it gets no readiness entry here.

`phases.parity` is `false`, so no parity cross-check ran. No planning round carried an `## Incidental findings (not gating)` lead. `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_graphscene_round_resume_task_plan/`) does not exist, so Pass 2 is a no-op. No findings.

---

## Phase 2 Readiness — Ordered Fix List

No fixable findings: this list is empty.

---

## Must Fix

None.

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None: `phases.parity` is `false`, so there is no reference implementation to diverge from.
