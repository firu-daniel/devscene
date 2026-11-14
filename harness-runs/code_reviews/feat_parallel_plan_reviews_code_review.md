# Code Review: feat_parallel_plan_reviews

## Context

**Branch:** `feat_parallel_plan_reviews`
**Date:** 2026-11-14
**Reviewed:** the whole branch diff against `defaultBranch` (`dev`), 36 commits, 62 files. This run copy has no local `dev` ref, so the diff base is `origin/dev`. 37 run-artifact files excluded from the reviewed diff.

The diff covers:
- **cli:** the gate library's `fw_round_evidence`; the format-3 planning graph; the walker's fan-out, `--node` recording, `wait`, held binding, join, set-aware `start`/`current` and its `mkdir` lock; the walker suites, the new fan-out and concurrency suites and the commit-path suite; run analytics' union sub-agent wall time and the overlap-aware idle-gap class.
- **plugin:** the round module, both loop cores, their forks, the two entry commands, the pause module and the two flow documents.
- **general:** the flow-graph schema and its fixtures, the `round-fan-out` check, this checkout's self-adopted walker, graph and analytics copies (byte-identical to the templates), `docs/flow-graph-walker.md` `### Item 8`, `docs/converging-plan-reviews.md`, row BG11 of `docs/sandbox-verification.md`, and `ROADMAP.md`.

**Tests.** Every behaviour in the task prompt's `## Tests` list has a case:
- `cli/test/flow-walker-fan-out.test.mjs` covers the set, any-order joins, refusals, skipped gates and the held binding.
- `cli/test/flow-walker-concurrency.test.mjs` covers simultaneous recording, the stale lock and the fresh lock.
- `cli/test/flow-walker-resume.test.mjs` cases (1), (8), (9), (11) and (12) cover resume, partial return and pause-at-join.
- `cli/test/flow-walker.test.mjs` cases (12)–(14) cover the counter per round, `{open_gates}` and the review mode.
- The new negative `schemas/negative/flow-graph-schema-round-without-parallel.json` is wired into `validate:flow-graph:negative`.
- `check-flow-graph.sh` item 9 has its fixture.

This review ran no suite; whether the tests pass is the Run gates phase's to establish. The new suites read fixed files rather than a tree, so they owe no `treeGuards` entry.

**Sweeps.** Pass 0's grep sweep list is not filled for this project (a configuration gap). A hand sweep of the added lines found no `rm -rf`, `git add -A`/`.`, `console.`, `process.exit` or machine path. The diff adds no new exported symbol for the caller check. `phases.parity` is `false`, so no parity review applies. Pass 2 had nothing to reconcile: `harness-runs/task_plan_point_reviews/feat_parallel_plan_reviews_task_plan/` does not exist.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 2** — Restate the semi-autonomous plan command's sentence that orders the architecture gate ahead of the plan review _(layer: plugin)_
2. [ ] **Finding 1** — Guard the walker's stale-lock break with a break lock so two waiters can never both hold the lock _(layer: cli, general)_

---

## Must Fix

None.

---

## Should Fix

### 1. Two calls waiting on a stale walker lock can both break it, so two calls hold the lock at once
→ [finding_1.md](feat_parallel_plan_reviews_code_review/finding_1.md)

### 2. The semi-autonomous plan command still says the architecture gate runs ahead of the plan review
→ [finding_2.md](feat_parallel_plan_reviews_code_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false` in `devscene.config.json`, so there is no reference implementation to diverge from, and this section has no entries.
