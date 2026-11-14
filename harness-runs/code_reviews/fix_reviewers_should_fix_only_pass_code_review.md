# Code Review: fix_reviewers_should_fix_only_pass

## Context

**Branch:** `fix_reviewers_should_fix_only_pass`
**Date:** 2026-11-14
**Reviewed:** the whole branch diff against the default branch (`defaultBranch: dev`). This run copy has no local `dev`, so the diff base is `origin/dev`. 13 files changed, all of them prose:
- Task 1 and Task 6: the three adopter run-artifact README templates and their two live copies.
- Task 2: `plan_review_rounds.md` → the new `## The verdict` and the Must-Fix-only `## The writer's revision`.
- Task 3: the three writers.
- Task 4: `architecture-reviewer` / `business-parity-reviewer` and the G.3 existence-guard sentence.
- Task 5: `ui-tests-plan-reviewer`.

11 run-artifact files excluded from the reviewed diff.

**Headline conclusions:**
- **Tests.** The branch adds no code and no test, and no task needed one. No tree-reading test reads the changed text: `cli/test` cites `plan_review_rounds.md` only by its `## The round file` heading, which is unchanged.
- **Wire strings.** Every verdict return and every quoted literal is byte-identical, including the implemented-solution *"Do not write any file when PASS"*. The callers' routing (G.2 → G.3, and the walker's `ui_review`) still works for the new advisory-PASS files: the G.3 existence guard picks them up, and so do the autonomous fork's commit of `ui_test_plan_reviews/<branch>/` and the semi-autonomous fork's.
- **README copies.** The two live README copies are byte-identical to their templates (`git diff --no-index --exit-code`).
- **Pass 0.** The grep half's sweep list is an empty stub, which is a configuration gap. The caller check found no new exported symbol.
- **Parity.** Not run: `phases.parity` is `false`.

**Remaining gaps:**
- Two in-scope writers can still reject a Should Fix under their unchanged recorded-rejection block, because neither follows `## The writer's revision`.
- Two citer paraphrases and one template line still use the pre-branch "finding" wording.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 3** — Make the revision-note template's `Unrequested changes:` line say "no Must Fix" _(layer: plugin)_
2. [ ] **Finding 2** — Align the two writers' paraphrase of `## The writer's revision` item 1 with its Must Fix wording _(layer: plugin)_
3. [ ] **Finding 1** — State in `test-fix-plan-writer` and `ui-tests-plan-writer` that a Should Fix or Nice to Have is never applied or recorded under `## Rejected findings` _(layer: plugin)_

---

## Must Fix

### 1. `test-fix-plan-writer` and `ui-tests-plan-writer` may still reject a Should Fix or Nice to Have under `## Rejected findings`
→ [finding_1.md](fix_reviewers_should_fix_only_pass_code_review/finding_1.md)

---

## Should Fix

### 2. Two writers paraphrase `## The writer's revision` item 1 in words it no longer uses ("every finding")
→ [finding_2.md](fix_reviewers_should_fix_only_pass_code_review/finding_2.md)

### 3. The revision-note template's `Unrequested changes:` line still says "no finding asked for", while the README now says "no Must Fix"
→ [finding_3.md](fix_reviewers_should_fix_only_pass_code_review/finding_3.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

Empty: `phases.parity` is `false`, so there is no reference implementation to diverge from.
