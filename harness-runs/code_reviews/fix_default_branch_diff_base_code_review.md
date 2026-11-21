# Code Review: fix_default_branch_diff_base

## Context

**Branch:** `fix_default_branch_diff_base`
**Date:** 2026-11-21
**Reviewed:** the whole branch diff against `origin/dev`, 13 files with 111 insertions and 33 deletions. It covers:

- Task 1: the `diff_base: origin/<default_branch>` dispatch blocks in `plugin/instructions/plan_orchestration_instructions_core.md`, the byte-identical quoted copies in `plugin/agents/architecture-reviewer.md` and `plugin/agents/business-parity-reviewer.md`, and their `<default_branch>` and `diff_base` rows.
- Task 2: the branch, skeptic and review-plan reviewers' diff commands and rows.
- Task 3: the `git log` ranges and their mentions in `plugin/agents/statistics-plan-writer.md`, `plugin/instructions/improvement_observations_instructions.md`, `plugin/instructions/docs_phase_instructions.md`, `plugin/samples/sample_statistics.md` and `plugin/docs/AUTONOMOUS_FLOW.md`.
- Task 4: the new suite `cli/test/diff-base-corpus.test.mjs`.
- Task 5: that suite's `treeGuards` entry in `devscene.config.json`.

11 run-artifact files excluded from the reviewed diff. This run copy has no local `dev`: a bare `git diff dev...HEAD` failed with `fatal: bad revision 'dev...HEAD'`, which is the failure this branch fixes, so the review used `origin/dev`.

**Headline conclusions.**

- **The intent holds across `plugin/`.** `git grep` finds no bare `<default_branch>...HEAD`, `<default_branch>..HEAD` or `diff_base: <default_branch>` left in `plugin/`. The one exception is D.2's sanctioned `git rev-list --count <default_branch>..HEAD` fallback in the two orchestration cores.
- **The dispatch blocks match their quoted copies.** The A1.5.1 and A2.1 blocks are byte-identical to the copies in the two receiving agents.
- **The fallback sentence matches in every copy.** The same sentence appears exactly once in each of the eight files that run `git diff` or `git log` against the base.
- **Tests.** The required suite is present, opens with the rule it enforces, and is registered as a tree guard, so `unit_loop_core.md` → `## The test-run rule` point 8 is met. This review did not run the suite. A probe replicated the suite's two cases against the tree: `bash scripts/scratch-run.sh harness-runs/scratch/diff_base_probe.mjs <repo_root>` printed `offenders []`, eight files selected, and `lacking []`.
- **Pass 0 (a).** `review-sweep.sh` exited `0` with no hits, so no candidates and no findings came from it.
- **Pass 0 (b).** The diff adds one export, `FALLBACK_SENTENCE` in `cli/test/diff-base-corpus.test.mjs`. It has no caller outside its own file. It is a constant in a test suite, which no layer consumes, so it is not an unwired feature. Sibling corpus suites export their tables the same way (`cli/test/untrusted-input-corpus.test.mjs` → `CASES`), so nothing was filed.
- **Parity.** `phases.parity` is `false`, so no parity cross-check runs.
- **Pass 2.** `harness-runs/task_plan_point_reviews/fix_default_branch_diff_base_task_plan/` does not exist, so Pass 2 had nothing to reconcile.
- **Incidental findings.** No planning round recorded any.

Two findings remain. Neither is a Must Fix. Finding 1 also raises a question the user owes (see the return).

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Correct the freshness sentences so a stale `origin/<default_branch>` also widens for a branch cut from an unpushed local `<default_branch>` _(layer: plugin)_
2. [ ] **Finding 2** — Scope `ALLOWED_LITERAL` to the two orchestration cores _(layer: cli)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The freshness sentences claim a stale `origin/<default_branch>` widens the diff only after a merge, but a branch cut from an unpushed local `<default_branch>` widens it too
→ [finding_1.md](fix_default_branch_diff_base_code_review/finding_1.md)

---

## Nice to Have

### 2. `ALLOWED_LITERAL` is stripped from every plugin file, not only from the two orchestration cores its comment names
→ [finding_2.md](fix_default_branch_diff_base_code_review/finding_2.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
