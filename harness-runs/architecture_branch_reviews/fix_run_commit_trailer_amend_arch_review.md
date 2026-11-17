# Architecture review — fix_run_commit_trailer_amend

## Context

This reviews branch `fix_run_commit_trailer_amend` on 2026-11-16, diffed against `dev`. This run copy has no local `dev` ref, so the diff base resolved to its remote-tracking `origin/dev`. The diff covers 18 files across the `cli` layer (`cli/src/generators/writeProtection.ts`, the profile template, the watcher's `COPY_GIT_PATHS` mirror, `hr_copy_sync_in_var` in `harness-run-lib.sh`, and three suites), the `plugin` layer (the committer contract, the commit guard, `hc_piece_is_never_safe` and the hooks README, `autonomous_pause_and_ledger.md` §1.6) and the `general` layer (five documents under `docs/`). 21 run-artifact files excluded from the reviewed diff.

Headline: the `cli` and `general` segments respect their layers. The new ref rows land in the owning table `COPY_GIT_PATHS`, and the declared watcher mirror and the `profile.test.mjs` assertion change with them in the same change. The profile change is a template under `cli/templates/` and has its own fixture-driven suite. The divergence sentence stays in its single producer, `hr_copy_sync_in_var`. No import or run-time edge crosses between `cli/` and `plugin/`. The guard change carries its README row, its REPRO lines and its `docs/guard-verification.md` re-measurement. There is one Must Fix. The commit guard now decides which other pieces may ride along on its `allow`, using a private remit set, a private leading-`cd` test and a private composition scan. That answer belongs to the shared library, `plugin/hooks/lib/harness-config-lib.sh`.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Commit guard re-derives the ride-along answer the shared library owns _(layer: plugin)_

## Must Fix

### 1. The commit guard re-derives the ride-along answer the shared library owns

→ [finding_1.md](fix_run_commit_trailer_amend_arch_review/finding_1.md)
