# Skeptic Review: feat_structured_outputs_docs_qa

## Context

**Branch:** `feat_structured_outputs_docs_qa`
**Date:** 2026-11-17
**Reviewed:** the whole branch diff against `origin/dev`. The configured `defaultBranch` is `dev`, and this run copy has no local `dev` branch. The diff is 25 files. 23 run-artifact files excluded from the reviewed diff.

**De-duplicated against:**

- the committed code review `harness-runs/code_reviews/feat_structured_outputs_docs_qa_code_review.md` and its three findings;
- `harness-runs/lessons.md`.

No parity review exists (`phases.parity` is `false`), and no architecture branch review exists for this branch. The planning rounds carry no incidental-finding leads.

**What was checked, adversarially:**

- **Wiring.** The new `checkSchemaCoverage` is called by the real-tree test and by a bad-sample test. The suite passes 57/57.
- **Callers.** Every caller of the five agents routes on the new outcomes. A grep across `plugin/`, `cli/templates/`, `docs/` and the root documents found no `error: blocked`, `targets: none`, `doc_path:`, `missed_docs:`, `parity_gaps:`, unmarked-`error:` or `1-3 line` reader left. No site halts on `blocked`.
- **Citations.** The decision record's claims checked out:
  - the `qa-tester` dispatch sites name their `error` routes (`plan_orchestration_instructions_core.md` E.2, `qa_test_instructions.md` step 4);
  - the quoted `docs-reviewer` disabled-phase text;
  - the `roadmap item N` citations, which use `docs/development.md` §6's own numbering and not the renumbered index.
- **Plan divergences.** Both of the story's stated divergences from the prompt are supported by the corpus: the stubs have no dispatching caller (`plugin/agents/README.txt`), and `phase_disabled` follows from distinct `const` values.

**Headline:** no Must Fix. Two Should Fix findings remain, both in the docs phase's `## Loop`. Task 3's plan grouped two dispatches whose state differs under one route, which changed behaviour that no prompt point authorized.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Commit the docs-phase INDEX without the review the new pointer drags in _(layer: plugin)_
2. [ ] **Finding 2** — Commit and flag, not skip, a doc whose fix-loop writer re-dispatch takes the `error` route _(layer: plugin)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The docs phase's INDEX step now inherits a review it never had and still says "commit it"
→ [finding_1.md](feat_structured_outputs_docs_qa_skeptic_review/finding_1.md)

### 2. A writer that fails during the docs phase's fix loop is told to "skip this target", which leaves an already-written doc uncommitted
→ [finding_2.md](feat_structured_outputs_docs_qa_skeptic_review/finding_2.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. The plan's two declared divergences from the task prompt passed both legs of the divergence test:

- the stubs' `blocker`-only schema, given no dispatching caller;
- `docs-reviewer`'s `phase_disabled` outcome in place of a disabled `PASS`.

They are not fixes.
