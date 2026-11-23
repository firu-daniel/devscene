# Code Review: fix_analyze_provenance_line_growth

## Context

**Branch:** `fix_analyze_provenance_line_growth`
**Date:** 2026-11-23
**Reviewed:** the whole branch diff against `origin/dev`:
- Task 1: the writer's provenance-line bullet and the fix-dispatch sentence in `plugin/agents/conventions-writer.md`.
- Task 2: check (1), and the corpus pass's `project`-member bullet, in `plugin/agents/conventions-reviewer.md`.
- Task 3: the (4a) restatement and the (4b) note rules in `plugin/commands/analyze.md`.
- Task 4: the new `cli/test/conventions-provenance-line.test.mjs`.

15 run-artifact files were excluded from the reviewed diff.

**Headline conclusions:**
- **Tests.** The new suite opens with its rule-and-not-covered header and sits at the right path. It reads three fixed files rather than a tree, so `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8's boundary applies and no `treeGuards` entry is owed. I ran a scratch copy of the suite against this checkout, with only the `WORKSPACE_ROOT` import replaced by an argument: `bash scripts/scratch-run.sh harness-runs/scratch/provenance_probe.mjs <repo_root>`. It reported `# tests 4`, `# pass 4`, `# fail 0` with exit 0. This review ran no other suite.
- **The wording.** The three files carry the bound's phrases as the story plan fixes them.
- **Stale wording.** A grep of `plugin`, `docs`, `cli/src`, `cli/templates` and the root prose documents for `footer`, `provenance line` / `provenance note` and `corrected by the review fix` found no other site still stating the old obligation.
- **Pass 0 sweep.** `review-sweep.sh` exited 0: no hits, so none became findings. The caller check found no new exported symbol.
- **Pass 2.** `harness-runs/task_plan_point_reviews/fix_analyze_provenance_line_growth_task_plan/` does not exist, so there were no carry-overs.
- **Planning rounds.** They left no incidental findings.
- **Parity.** `phases.parity` is `false`.

**What is left:**
- Two places where the new rule's coverage is incomplete: the reviewer's corpus-pass text contradicts itself about check (1), and the session's own corpus fixes to `.claude/CLAUDE.md` are not bound by the fix-pass rule.
- One clause of rationale in the writer's new bullet.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 3** — Drop the "git history records them" rationale from the writer's provenance bullet _(layer: plugin)_
2. [ ] **Finding 1** — State check (1)'s provenance-line exception everywhere the corpus pass says check (1) does not run _(layer: plugin)_
3. [ ] **Finding 2** — Keep the session's corpus fixes to `.claude/CLAUDE.md` out of the section's provenance note, and hold the phrase in the suite _(layer: cli, plugin)_

---

## Must Fix

None.

---

## Should Fix

### 1. `conventions-reviewer.md` says check (1) both does and does not run on the corpus pass's `project` member
→ [finding_1.md](fix_analyze_provenance_line_growth_code_review/finding_1.md)

### 2. A corpus fix the session applies to `.claude/CLAUDE.md` has no rule keeping it out of the section's provenance note
→ [finding_2.md](fix_analyze_provenance_line_growth_code_review/finding_2.md)

### 3. The writer's new provenance bullet carries rationale the writer does not act on
→ [finding_3.md](fix_analyze_provenance_line_growth_code_review/finding_3.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section is empty.
