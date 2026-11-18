# Code Review: feat_review_sweep_in_conventions

## Context

**Branch:** `feat_review_sweep_in_conventions`
**Date:** 2026-11-18
**Reviewed:** the whole branch diff against the default branch (`dev`). This run copy carries no local `dev`, so the base was `origin/dev`, and that missing local ref is Finding 1. The diff covers:

- the `.claude/review-sweep.md` skeleton, `REVIEW_SWEEP_PATH` and the `sweep` reserved target (Task 1);
- `review-sweep.sh` and `cli/test/review-sweep.test.mjs` (Task 2);
- its `OUTER_LOOP_SCRIPTS` row (Task 3);
- the `review-sweep` doctor check (Task 4);
- the `conventions-writer`, `conventions-reviewer`, `/devscene:analyze` and `branch-reviewer` contract changes (Tasks 5–8);
- the self-adopted `scripts/review-sweep.sh` and the watcher table row (Task 9);
- the documentation (Task 10).

24 files were reviewed. 22 run-artifact files were excluded from the reviewed diff.

**Tests.** Every accompanying test the touched layers' conventions documents require is present except one: the review-sweep document's conditional `--force` keep has no case (Finding 3). Whether the tests pass is for the Run gates phase to establish; this review runs no suite. `scripts/review-sweep.sh` is byte-identical to its template. The `main_repo_resolution.md` roster count (28) matches its list.

**The script's rows and its wiring are coherent:**

- The row format is stated identically in the skeleton, in `conventions-writer.md` → `## The sweep document` and in the script's parser.
- `branch-reviewer`'s new `<MAIN_REPO>` row is byte-identical to its siblings in the corpus.
- `cli/src/core/writer.ts` and `docs/cli.md` §3 carry the new `create-if-absent` row.
- The new outer-loop script's required accompanying set (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, the *An outer-loop script* row) was checked member by member. All three hold:
  - **(i) The shipped-table row.** `cli/src/generators/outerLoopScripts.ts` → "Object.freeze({ file: 'review-sweep.sh', mode: 0o755, agentInvocable: true })" sets `agentInvocable: true` on purpose. The row's own comment gives the reason: "Run by `branch-reviewer` from the main checkout".
  - **(ii) The permission-profile entries.** `cli/src/generators/permissionProfile.ts` generates the allow entries from that flag (`OUTER_LOOP_SCRIPTS.filter((script) => script.agentInvocable)`). `cli/test/profile.test.mjs` checks this for every row of `OUTER_LOOP_SCRIPTS`, so the new row is covered without a case of its own.
  - **(iii) The deny-list entry.** There is none, by design: `branch-reviewer` must be able to run the script. The row comment says "no `DENY_SCRIPT_BASENAMES` entry, because it must be reachable", and the `DENY_SCRIPT_BASENAMES` list in `plugin/hooks/autonomous-script-allowlist-guard.sh` does not name `review-sweep.sh`.

**But the script cannot run where it is deployed.** In a run copy the default branch exists only as `origin/<default_branch>`, so every semi-autonomous and autonomous review gets exit `2` (Finding 1).

**Pass 0.** Half (a), the grep sweep, did not run. The sweep list in the `branch-reviewer` definition this review ran under has no regexes, which is a configuration gap; it is the gap this branch closes. Half (b), the new-exported-symbol caller check, found one new export, `REVIEW_SWEEP_PATH`. It has callers outside its defining file (`cli/src/doctor/checks.ts` → `REVIEW_SWEEP_CHECK`), so nothing is un-wired.

**Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_review_sweep_in_conventions_task_plan/` does not exist, so Pass 2 had nothing to reconcile. No planning round recorded an incidental finding. `phases.parity` is `false`, so no parity cross-check ran.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Type the generator's `sweep` target against `RESERVED_ANALYZE_TARGETS` _(layer: cli)_
2. [x] **Finding 2** — State that the `sweep` target's `scope` is the repository root in `conventions-writer`'s `scope` row _(layer: plugin)_
3. [x] **Finding 3** — Test the review-sweep document's second-`--force` keep path _(layer: cli)_
4. [x] **Finding 1** — Resolve the sweep base as `origin/<default_branch>` in a run copy that has no local default branch _(layer: cli, plugin, general)_

---

## Must Fix

### 1. `review-sweep.sh` refuses every run copy, because a run copy has no local `<default_branch>`
→ [finding_1.md](feat_review_sweep_in_conventions_code_review/finding_1.md)

---

## Should Fix

### 2. `conventions-writer`'s `scope` row reads as if `sweep` were a scope value
→ [finding_2.md](feat_review_sweep_in_conventions_code_review/finding_2.md)

### 3. The review-sweep document's `--force` keep path has no test
→ [finding_3.md](feat_review_sweep_in_conventions_code_review/finding_3.md)

---

## Nice to Have

### 4. The generator spells the `sweep` target as an untyped literal, where `doctor` types it against the reserved list
→ [finding_4.md](feat_review_sweep_in_conventions_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
