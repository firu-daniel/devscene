# Skeptic Review: feat_flow_walker_python_cutover

## Context

**Branch:** `feat_flow_walker_python_cutover`
**Date:** 2026-11-25

**What was reviewed.** The whole branch diff against `origin/dev`, 50 files, reviewed adversarially segment by segment:
- the `flow-walker.sh` hand-off and its retired gate library;
- the `HR_FLOW_HOST_*` layout mirror, `hr_walk_state_name`, and the per-branch walker-state bundle write and restore in `lib/harness-run-lib.sh`;
- provisioning failing rather than skipping, in `hr_flow_host_provision`, `flow-host-provision.sh` and `setup-worktree.sh` step 6;
- `init`'s default build, `--no-provision-python` and the probe seam;
- `doctor`'s `uv` and `flow-host` grades;
- the planning driver running the main checkout's walker;
- the test helpers and suites;
- gate 6a's filter;
- the prose under `docs/`, `plugin/`, the `cli` READMEs and `devscene-flow-host/`.

37 run-artifact files excluded from the reviewed diff.

**De-duplicated against.** Only one committed review exists: the code review, `harness-runs/code_reviews/feat_flow_walker_python_cutover_code_review.md`, with Findings 1–4, all fixed. There is no parity review (`phases.parity` is `false`) and no branch-level architecture review. No planning round recorded an incidental finding.

**Checks run.**
- **Check 1, wiring.** Every new symbol has a live caller across every `layers[].path`: `hr_walk_state_name` in the bundle write and restore; the six `HR_FLOW_HOST_*` names in `hr_flow_host_provision` and `flow-walker.sh`; `ENV_MARKER_FILE`, `FLOW_HOST_SOURCE_DIRNAME` and `FLOW_HOST_PROVISION_PROBE_ENV` in `init`, `layout.ts` and the test helpers; `--no-provision-python` in `parseInitFlags` and `run`. `pd_main` now builds `PD_WALKER` from `PD_MAIN_REPO` and runs it with the worktree as its working directory.
- **Check 2.** The parity leg is off. For the runtime-address leg, the hand-off's launch composes to `UV_PROJECT_ENVIRONMENT=<dir>/python/.venv PYTHONPATH=<dir>/python/devscene-flow-host/src:<dir>/python/graphscene/src … --project <dir>/python/devscene-flow-host`, matching #478's launch line. `hr_walk_state_name` matches `quote(branch, safe="")` and the host's four `<enc>.json` record paths.
- **Check 3, citations.** The cited `lessons.md` → `## Trust checks`, `devscene-flow-host/README.md` → `## The command line`, `## What it reads, answers and keeps` and `## Differences from flow-walker.sh` all resolve and say what is claimed.
- **Check 4.** The one intentional divergence is that another branch is no longer refused. It is recorded under **Chosen**, and per-branch stores make the bash refusal moot.
- **Check 5.** The flat-file deletion runs before the provisioning refusal and skips a link. Provisioning now fails rather than skipping. `doctor --remote-job` warns, after code-review Finding 2.

**Headline.** No net-new behavioural defect. One stale description that this branch's own Task 9 edit left false is a Should Fix.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Say in `cli/templates/scripts/README.md` that `init` builds the walker's environment by default, with `--no-provision-python` to skip it _(layer: cli)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `cli/templates/scripts/README.md` still says `init` builds the walker's environment only "when asked (`--provision-python`, or yes at its prompt)"
→ [finding_1.md](feat_flow_walker_python_cutover_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section has no entries.
