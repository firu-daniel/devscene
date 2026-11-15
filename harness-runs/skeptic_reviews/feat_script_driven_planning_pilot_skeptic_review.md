# Skeptic Review: feat_script_driven_planning_pilot

## Context

**Branch:** `feat_script_driven_planning_pilot`
**Date:** 2026-11-15
**Reviewed:** the whole branch diff, read adversarially, against the default branch `dev`. No local `dev` ref exists in this checkout, so the base was `origin/dev...HEAD`. The diff covers 26 files: the three planning libraries, the watcher wiring, the shipped-table rows, the stub-driven suites, step 4a, the core's note, the observation intake's second writer, and the docs.

30 run-artifact files excluded from the reviewed diff.

**De-duplicated against:**
- The committed code review `harness-runs/code_reviews/feat_script_driven_planning_pilot_code_review.md` and its five findings. All five are applied.
- `harness-runs/lessons.md`.
- The planning rounds' architecture reviews under `harness-runs/architecture_reviews/feat_script_driven_planning_pilot/`. They carry no `## Incidental findings (not gating)` section, and neither does any other planning-round folder.

No parity review exists, because `phases.parity` is `false`, so check 2's parity leg did not apply. No end-of-branch architecture review exists.

**What was checked first-hand, beyond the code review:**
- **Check 1 (wiring).** Every function the driver calls in `lib/harness-run-lib.sh` exists: `hr_lane_mtime`, `hr_top_level_answered_pairs`, `hr_max_question_index`, `hr_ledger_phases`, `hr_phase_enabled`, `hr_state_path`, `hr_state_dir` and `hr_scripts_dir`. No template or test still calls the removed watcher-local `max_question_index` or `top_level_answered_pairs`.
- **Check 3 (citations).** Every anchor the new docs and plugin text cite resolves:
  - `docs/orchestrator-cost-measurement.md` → `## 4.` and **Three things a launcher must handle:**;
  - `docs/flow-graph-walker.md` → `### Item 8` → **What a second driver must do.** and `### Not yet measured, and the hand step that measures it`;
  - `docs/watcher.md` → `### Script-driven planning (opt-in pilot)`;
  - `autonomous_pause_and_ledger.md` §2.2 **A round's set.**, §2.3 and §2.5.
- **The driver against the autonomous fork's Overrides 2, 5 and 6.** Read line by line: the entry order, the saved-walk vetoes, PAUSE once per set, STOP per block, the cap against the whole set, round commits before ledger flips, the partial-commit round number and the three-strike overload pause all match.
- **The watcher's stall watchdog.** It reads the run log as well as the run stream, and node output is formatted into the run log as it happens. So node streams that reach `.stream.jsonl` only at reap do not starve the watchdog.

**Headline.** One net-new Must Fix. On a resume that enters at `convergence`, `pd_handoff` decides Override 3's UI-test-plan commit before it works out the UI-test variant from disk. So a plan written before an interruption is never committed, although Override 5 says Overrides 3 and 4 both run again on that path. The task plan prescribed the same order (`task_3_plan.md`: *"`yes` exactly when a `report: ui_test passed` line is present"*), so the plan carries the defect too.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Work out the UI-test variant before Override 3's commit decision in `pd_handoff`, so a convergence-entry resume commits a written UI-test plan _(layer: cli)_

---

## Must Fix

### 1. A resume entering at `convergence` never re-runs Override 3, so an uncommitted UI-test plan stays uncommitted
→ [finding_1.md](feat_script_driven_planning_pilot_skeptic_review/finding_1.md)

---

## Should Fix

_None._

---

## Nice to Have

_None._

---

## Intentional divergences — confirm

_None: `phases.parity` is `false`, so there is no reference implementation to diverge from, and the diff marks no divergence from the autonomous fork as intentional._
