# Code Review: fix_run_commit_trailer_amend

## Context

**Branch:** `fix_run_commit_trailer_amend`
**Date:** 2026-11-16
**Reviewed:** the whole branch diff against `dev`. This run copy has no local `dev` ref, so the diff base is `origin/dev`. The diff covers 18 files:
- **`cli`** (Tasks 1–3): the three branch-ref rows in `COPY_GIT_PATHS` and the watcher's `RUN_PROFILE_COPY_GIT_PATHS` mirror; the profile template's `attribution` object, the dropped `Bash(git commit:*)` grant, the new `Bash(git commit --amend:*)` deny and its `_README` lines; the divergence sentence in `hr_copy_sync_in_var`; and the suites `profile.test.mjs`, `clone-sync.test.mjs` case (d2) and the new `profile-commit-attribution.test.mjs`.
- **`plugin`** (Tasks 4–5 and the arch-review Finding 1 fix): the commit guard's every-piece walk, `hc_piece_is_never_safe`'s `commit` arm, the new `hc_commit_piece_may_ride_along`, the hooks README, the committer's read-back and `landed wrong` return, and `autonomous_pause_and_ledger.md` §1.6.
- **`general`** (Tasks 6–7): `docs/sandbox-verification.md` rows AT1, AT2, CS16, CS16 (Linux) and PD32 with the CS3 notes; the CG1–CG16 block in `docs/guard-verification.md`; and `docs/cli.md`, `docs/watcher.md`, `docs/sandbox-record.md` residual 19 and `docs/development.md`.

23 run-artifact files excluded from the reviewed diff.

**Headline.** The `cli` and `general` segments hold together:
- The new rows land in the owning table, and the declared mirror and its assertion change in the same edit.
- The divergence sentence keeps `have diverged` and stays in its single producer, and case (d2) runs the repair it prints.
- The new suite opens on its rule and drives the compiled CLI against a throwaway fixture.
- Every unmeasured protection is graded `owed`.
- `phases.parity` is `false`, so no parity cross-check applies.

Pass 0:
- The grep-sweep regex table in this agent's definition is an unfilled stub, so half (a) ran no project regexes. That is a configuration gap, not a clean sweep.
- Half (b): the one new shared symbol, `hc_commit_piece_may_ride_along`, has its caller in `git-commit-branch-guard.sh`.
- No line coordinate was added to a durable file.

Pass 2 was a no-op: `harness-runs/task_plan_point_reviews/fix_run_commit_trailer_amend_task_plan/` does not exist.

What remains is in the commit guard:
- It still grants a second commit, or an `add`, into a **different** repository on the `allow` it computed for the first. A protected branch there is included (Finding 1).
- Its rows of record predate the library move that changed its `cd` decisions (Finding 2).
- The README does not disclose that a commit message's own `$`, backtick, `<` or `>` now costs the `allow` (Finding 3).

Tests: this review ran no suite.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 3** — Disclose in the hooks README that a commit message's own prose costs the commit guard's `allow` _(layer: plugin)_
2. [x] **Finding 1** — Grant a ride-along git piece only when it runs in the repository the commit guard judged _(layer: plugin)_
3. [ ] **Finding 2** — Re-drive and record the commit-guard rows against the library-owned ride-along answer _(layer: general)_

---

## Must Fix

### 1. The commit guard lets a commit into a different repository ride along on its `allow`
→ [finding_1.md](fix_run_commit_trailer_amend_code_review/finding_1.md)

### 2. The commit-guard rows of record predate the library move and miss the decisions it changed
→ [finding_2.md](fix_run_commit_trailer_amend_code_review/finding_2.md)

---

## Should Fix

### 3. The hooks README's commit-guard row hides that a commit message's own prose now costs the `allow`
→ [finding_3.md](fix_run_commit_trailer_amend_code_review/finding_3.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
