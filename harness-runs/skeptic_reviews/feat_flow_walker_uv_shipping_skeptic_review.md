# Skeptic Review: feat_flow_walker_uv_shipping

## Context

**Branch:** `feat_flow_walker_uv_shipping`
**Date:** 2026-11-24

**Reviewed:** the whole-branch diff against `origin/dev`, 45 files, read adversarially, segment by segment:

- the staging, layout and provisioning modules under `cli/src/flowHost/`;
- the package writer `cli/src/generators/flowHostPackages.ts`, and its `init` and `init --upgrade` wiring;
- `flow-host-provision.sh`, `hr_flow_host_provision` and `setup-worktree.sh` step 6;
- the write protection in `cli/src/generators/writeProtection.ts`, and the job surface derived from it;
- the managed `.gitignore` rule;
- `doctor`'s `uv` and `flow-host` checks;
- the `setup-uv` step in the shipped `devscene-run.yml`;
- the self-adopted carry-over with its two `scripts/python/` symlinks.

33 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** the committed code review `harness-runs/code_reviews/feat_flow_walker_uv_shipping_code_review.md` and its four findings (the init notes, `SKIPPED_MARKER`, the self-adopted drift remedy, the import order). No branch-level parity review exists, because `phases.parity` is `false`. No branch-level architecture review exists for this branch either. The planning rounds carry no `## Incidental findings (not gating)` section.

**What the checks found:**

- **Check 1 (wiring):** every new export has a caller, the provisioning route is reached from `init`, `setup-worktree.sh` and the remote job, and `uv` is set up before `Bootstrap the checkout`.
- **Check 2 (runtime addresses):** the composed paths resolve. `<scriptsDir>/python/devscene-flow-host` reaches `../graphscene` as a sibling. The shipped `pyproject.toml`s name no `readme` or other file outside `pyproject.toml`, `uv.lock` and `src/`.
- **Check 3 (citations):** every citation checked resolves and says what is claimed: `harness-runs/lessons.md` → `## Trust checks`, `scripts/python-service.sh` → `WHO RUNS lock, sync AND provision`, `.claude/context/cli.md` → `## What "done" means here`, and `cli/src/commands/doctor.ts` → `runNotifier`.

**Headline:** one net-new Must Fix. In this self-adopted repository the main checkout's `scripts/python/` holds links, so Task 5's protection covers the links and not the package trees that step 6 builds outside the sandbox. A run session's file tools can still write those trees.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Write-protect the link targets of `<scriptsDir>/python/<pkg>` in `protectedPaths` _(layer: cli)_

---

## Must Fix

### 1. In the self-adopted repository the write protection of `scripts/python/` covers two symlinks, not the package trees `setup-worktree.sh` step 6 builds outside the sandbox
→ [finding_1.md](feat_flow_walker_uv_shipping_skeptic_review/finding_1.md)

---

## Should Fix

_None._

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. The plan marks no divergence as intentional, so check 4 had nothing to re-grade.
