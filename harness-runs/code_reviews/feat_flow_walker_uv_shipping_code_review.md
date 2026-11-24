# Code Review: feat_flow_walker_uv_shipping

## Context

**Branch:** `feat_flow_walker_uv_shipping`
**Date:** 2026-11-24
**Reviewed:** the whole branch diff against `origin/dev` — 45 files, +2433/−65: the build-time staging of `graphscene/` and `devscene-flow-host/` into `cli/dist/python/` and the layout module that names it (Task 1), the `init` / `init --upgrade` writer for `<scriptsDir>/python/` (Task 2), `flow-host-provision.sh` and `hr_flow_host_provision` (Task 3), `setup-worktree.sh` step 6 (Task 4), the write protection of the main checkout's `<scriptsDir>/python/` (Task 5), the managed `.gitignore` rule (Task 6), `init --provision-python` and the upgrade rebuild warning (Task 7), `doctor`'s `uv` and `flow-host` checks (Task 8), the pinned `setup-uv` step in the shipped `devscene-run.yml` (Task 9), the READMEs and `docs/` (Tasks 10, 11, 13), and the self-adopted carry-over with its two symlinks and tree guard (Task 12). 28 run-artifact files excluded from the reviewed diff.

Every module added under `cli/src/` opens with its header and rule; every new suite opens with the rule it enforces, and each new artifact class carries its idempotence and `--force`-takes-a-`.bak` assertions (`cli/test/flow-host-packages.test.mjs`). No case reaches the network or the shared `uv` cache: every suite that reaches `uv` stubs it, and `cli/test/helpers/watcher.mjs` puts a stub first on every watcher pass's `PATH`. The self-adopted `scripts/` copies of `flow-host-provision.sh`, `setup-worktree.sh` and `lib/harness-run-lib.sh` are byte-identical to their templates. Whether the suites pass is the Run gates phase's to establish; this review ran none. The Pass 0 sweep (`review-sweep.sh`, exit 1) printed 5 hits, all in `cli/src/flowHost/stage.ts`, and none became a finding: the `Direct process exit` hit is the header sentence that says the module never calls `process.exit()`; the three `Filesystem mutation outside its owner` hits and the `Recursive removal` hit are the build step writing and clearing this package's own `dist/python/`, which `.claude/context/conventions.md` → `### Where a new responsibility goes` scopes outside `cli/src/core/writer.ts`'s monopoly (that monopoly covers writes into an adopting repository), done in process rather than by a shelled-out `rm -rf`, and argued in the module header. The new-exported-symbol caller check found every new export called outside its defining file across the six `layers[].path` scopes, `flowHostProjectDir` only from `cli/test/`. The planning rounds carry no `## Incidental findings (not gating)` section. Pass 2 was a no-op: `harness-runs/task_plan_point_reviews/feat_flow_walker_uv_shipping_task_plan/` does not exist. `phases.parity` is `false`, so no parity cross-check ran. The four findings below are what is left: three Should Fix, all in what `init` and `doctor` tell a person, and one Nice to Have.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 4** — Move `upgrade/report.ts`'s `node:path` import ahead of its relative imports _(layer: cli)_
2. [ ] **Finding 2** — Declare `SKIPPED_MARKER` as a mirror of the library's skip prefix and test `init --provision-python` with no `uv` on `PATH` _(layer: cli)_
3. [ ] **Finding 1** — Key `init`'s package-written and environment-not-built notes on what the plan actually wrote _(layer: cli)_
4. [ ] **Finding 3** — Name `npm run build` as `flow-host`'s drift remedy where the packages are links _(layer: cli)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `init` re-run says the walker's environment "is not built" when it is, and that package files "were written" when none were
→ [finding_1.md](feat_flow_walker_uv_shipping_code_review/finding_1.md)

### 2. `provisionFlowHost` keys a false-success decision on an undeclared, untested copy of the library's `SKIPPED` wording
→ [finding_2.md](feat_flow_walker_uv_shipping_code_review/finding_2.md)

### 3. `doctor`'s `flow-host` drift remedy in the self-adopted repository names `init --upgrade`, which skips the packages there
→ [finding_3.md](feat_flow_walker_uv_shipping_code_review/finding_3.md)

---

## Nice to Have

### 4. `upgrade/report.ts` imports `node:path` after a relative import
→ [finding_4.md](feat_flow_walker_uv_shipping_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
