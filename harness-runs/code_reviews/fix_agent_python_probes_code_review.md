# Code Review: fix_agent_python_probes

## Context

**Branch:** `fix_agent_python_probes`
**Date:** 2026-11-21
**Reviewed:** the whole branch diff against `origin/dev`. This run copy has no local `dev`. The diff covers 12 files:

- `scripts/python-service.sh`: the new `probe` and `check` verbs, and root placement through `hr_script_root` (Task 1).
- `scripts/typecheck.sh`: the per-unit Python check and its `BLOCKED` grading (Task 2).
- The two `cli` suites that pin them, `cli/test/python-service.test.mjs` and `cli/test/check-shell-parse.test.mjs` (Tasks 3 and 4).
- The new shared module `plugin/instructions/probe_route.md`, the five citing agent definitions and the `unit_loop_core.md` roster entry (Tasks 5 and 6).
- `docs/development.md` → Gate 13, the `init --force` bullet and Gate 16 (Task 7).

19 run-artifact files excluded from the reviewed diff.

**Headline conclusions.**

- **Pass 0 sweep.** `review-sweep.sh` exited `0`: 0 hits, 0 findings.
- **Caller check.** The diff adds no exported TypeScript symbol. The two new shell verbs and the new module all have callers: `check` is called by `scripts/typecheck.sh`, and `probe` is cited by `probe_route.md` → `## The route` (through the conventions document's wrapper) and by `docs/development.md`. `probe_route.md` is cited by exactly the five agents its `## Who may cite this` roster lists, and `unit_loop_core.md`'s `## The test-run rule` roster now lists `probe_route.md`.
- **Tests.** The tests each touched layer requires are present. Whether they pass is the Run gates phase's to establish; this review ran no suite.
- **The probe route works.** I wrote `harness-runs/scratch/branch_review_fix_agent_python_probes.py` (it imports `graphscene`, prints `len(graphscene.__all__)` and its arguments, then exits `5`) and ran `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_fix_agent_python_probes.py a b`. It printed `graphscene public names: 27` and `args ['a', 'b']` and exited `5`, so the package environment was reached and the file's status came back unchanged. A `..` path (`probe harness-runs/scratch/../scratch/…`) exited `2` with the `carries '..'` refusal line.
- **Disclosure.** I am running under the main checkout's copy of `branch-reviewer`, which predates this branch's probe-file exception. Writing that probe file therefore went beyond the write bound my loaded definition states. The file is gitignored by `harness-runs/scratch/*` and is not committed.
- **Parity.** `phases.parity` is `false`, so no parity cross-check runs here.
- **Two-pass mode.** `per_task_findings_root` (`harness-runs/task_plan_point_reviews/fix_agent_python_probes_task_plan/`) does not exist, so Pass 2 was a no-op.
- **Planning leads.** The planning rounds' `## Incidental findings (not gating)` sections gave no lead.

**One item is not a fix here.** `.claude/context/graphscene.md` → `## Tests` still says *"The layer's `mypy` `strict` check is not part of a unit's run: `commands.typecheck` (`scripts/typecheck.sh`) does not reach it"*. This branch makes that sentence false. The story plan routes it to a `stale-rule` entry, but no committed artifact on the branch records one. It is raised in the return's `questions`, because no implementing run may edit a conventions document.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 2** — Move the not-run `<typecheck_cmd>` note requirement out of `layer-implementer`'s evidence-downgrade list into its own sentence _(layer: plugin)_
2. [ ] **Finding 1** — Give `typecheck.sh`'s `BLOCKED` line the install-`uv` remedy as well as `provision`, and update the test and Gate 13 quote that pin it _(layer: cli, general)_

---

## Must Fix

### 1. `typecheck.sh`'s `BLOCKED` line sends a host with no `uv` to `provision`, which skips and leaves the check `BLOCKED`
→ [finding_1.md](fix_agent_python_probes_code_review/finding_1.md)

---

## Should Fix

_None._

---

## Nice to Have

### 2. The not-run `<typecheck_cmd>` clause in `layer-implementer`'s evidence-downgrade list attaches its note requirement mid-list
→ [finding_2.md](fix_agent_python_probes_code_review/finding_2.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section is empty.
