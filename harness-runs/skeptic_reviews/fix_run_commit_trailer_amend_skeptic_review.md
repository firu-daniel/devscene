# Skeptic Review: fix_run_commit_trailer_amend

## Context

**Branch:** `fix_run_commit_trailer_amend`
**Date:** 2026-11-16

**Reviewed.** The whole branch diff, adversarially, against `origin/dev`. This run copy has no local `dev` ref, so the diff base is the remote-tracking `dev`. The diff covers 18 files:

- **`cli`:** the three branch-ref rows in `COPY_GIT_PATHS` and the watcher's mirror; the profile template's `attribution` object, the dropped raw-commit grant and the amend deny; and the divergence sentence in `hr_copy_sync_in_var`, with its suites.
- **`plugin`:** the commit guard and `hc_commit_piece_may_ride_along`, `hc_piece_is_never_safe`'s `commit` arm, the committer's read-back, and §1.6.
- **`general`:** five documents under `docs/`.

27 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/fix_run_commit_trailer_amend_code_review.md` (Findings 1–3) and `harness-runs/architecture_branch_reviews/fix_run_commit_trailer_amend_arch_review.md` (Finding 1), each with its per-finding files. There is no parity review, because `phases.parity` is `false`. The planning rounds recorded no incidental findings.

**What was checked first-hand and holds:**

- **Wiring.** `hc_commit_piece_may_ride_along` has its one caller in the guard's ordinary-branch arm. The new suite is picked up by `node --test`.
- **Ride-along test.** I walked these spellings through the code, without a probe:
  - a newline-joined compound: the read loop splits it per line, so `reset` is refused;
  - a `cd` past position 1, including one inside `(`;
  - an env-prefixed `GIT_DIR=` piece;
  - `--git-dir=`, and `-c` on the commit piece itself;
  - two `-C` options;
  - a commit with no `-C` beside another piece's `-C`, where `root` resolves to the other piece's repository and the commit's `bare_root` mismatch refuses it.

  Each one ends SILENT, never `allow`, and every `ask` arm is reached before the ride-along test.
- **The `--amend` prefix test.** It refuses `--a`, `--am`, `--amen` and `--amend`, quoted or not, and leaves `--fixup=amend:<c>` granted.
- **The divergence repair.** The two `update-ref` commands name objects each side holds: sync-in's fetch has already brought the clone's tip into the main checkout.
- **Committer read-back.** `%h%n%B` matches the `commit-tree` message the wrapper builds, one `-m` paragraph per argument.
- **Gate sandbox.** It binds the whole run-copy `.git` read-only anyway, so the three new rows change nothing there.
- **Callers on `error:`.** Both cores route a committer `error:` to `<escalate>` (`plan_orchestration_instructions_core.md`, `user_review_fixes_instructions_core.md`), so the new `landed wrong` return parks.

**Headline.** There is one net-new finding, a Should Fix. Six flow files still tell the orchestrator that the commit wrapper *enforces* "no trailer", and the wrapper's own header and this branch's incident both disprove that. The story index's scope register kept these rows on a reading of the sentence that it does not support. Nothing else rose above the confidence bar. Tests: this review ran no suite and no probe.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Replace the six flow files' false "the wrapper enforces both" trailer guarantee with what the wrapper does _(layer: plugin)_

---

## Must Fix

_None._

---

## Should Fix

### 1. Six flow files still say the commit wrapper "enforces" no trailer, which the incident this branch fixes disproved
→ [finding_1.md](fix_run_commit_trailer_amend_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and no divergence needed check 4's two-leg test.

**Verified-OK: the story's three acknowledged residuals were not re-raised.** The story index states each one itself:

- A plain raw `git commit` in a run is still guard-allowed, and it is held only by the OS-layer ref write-deny, which is owed until CS16.
- `git stash push` is expected to be refused in a run copy.
- A placeholder may be mounted at an absent `.git/packed-refs` on a bubblewrap host. That is benign for reads: git treats a zero-size `packed-refs` as empty.
