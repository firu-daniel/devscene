# Code Review: feat_flow_walker_python_cutover

## Context

**Branch:** `feat_flow_walker_python_cutover`
**Date:** 2026-11-25
**Reviewed:** the whole branch diff against `origin/dev`, across 49 files, segment by segment:
- the hand-off `cli/templates/scripts/flow-walker.sh`, with the gate library and its suite retired (Tasks 1, 7, 8);
- the layout mirror, provisioning failure and per-branch remote bundle in `lib/harness-run-lib.sh` (Task 3);
- `init`'s default build and its probe seam (Task 4);
- `doctor`'s `uv` and `flow-host` grades (Task 5);
- the planning driver running the main checkout's walker (Task 6);
- the test helpers and the provisioning, bootstrap and bundle suites (Tasks 2, 16, 17);
- the `cli` READMEs (Task 9), the plugin's graph names (Task 10) and the `devscene-flow-host` README and docstrings (Task 11);
- gate 6a's filter (Task 12);
- the walker's decisions of record and the startup-cost slot (Task 13);
- the remote, sandbox, watcher and `docs/cli.md` prose (Tasks 14, 15).

32 run-artifact files excluded from the reviewed diff.

**Tests.** Every accompanying test the touched layers' conventions documents require is present:
- the hand-off's own suite, `cli/test/flow-walker-hand-off.test.mjs`;
- the moved `flow-walker*` cases;
- the default-build and seam cases in `cli/test/init-provision-python.test.mjs`;
- the `doctor` grades in `cli/test/doctor-flow-host.test.mjs`;
- the layout mirror in `cli/test/flow-host-provision.test.mjs`;
- the per-branch bundle round trip and the pre-cutover bundle in `cli/test/outer-loop-scripts.test.mjs`;
- the driver's main-checkout walker in `cli/test/planning-driver-walk.test.mjs`.

Whether they pass is for the Run gates phase to establish, because this review runs no suite. No test the branch adds reads a tree of repository files, so no `treeGuards` entry is owed.

**Pass 0 sweep.** `review-sweep.sh` exited `0`: no hits, so no candidate became a finding. In the new-exported-symbol caller check, every symbol the branch adds has a caller outside its defining file, searched across every `layers[].path`:
- `FLOW_HOST_SOURCE_DIRNAME`, `ENV_MARKER_FILE` and `FLOW_HOST_PROVISION_PROBE_ENV`;
- `hr_walk_state_name` and the six `HR_FLOW_HOST_*` names;
- `linkWalkerEnv`.

**Parity.** `phases.parity` is `false`, so no parity cross-check was run.

**Two-pass mode.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_flow_walker_python_cutover_task_plan/` does not exist, so Pass 2 had nothing to reconcile. No planning round recorded an incidental finding.

**Probe.** Finding 1 rests on one probe, `bash scripts/scratch-run.sh harness-runs/scratch/pyc_probe.py <checkout>/scripts/python/.venv/bin/python`. It showed the walker environment's interpreter writing `__pycache__` beside a `PYTHONPATH` source. The rest of Finding 1, and all of Finding 2, were confirmed by reading only, as each finding says.

**What is left.** Two Must Fix findings and two Should Fix findings, below.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Drop the retired gate library from `docs/cli.md`'s list of outer-loop scripts _(layer: general)_
2. [x] **Finding 3** — Bring `remote-run.sh`'s REPRO to the per-branch walker-state directory _(layer: cli)_
3. [x] **Finding 1** — Launch the walker with `PYTHONDONTWRITEBYTECODE=1` so no bytecode lands beside the shipped sources _(layer: cli, devscene-flow-host)_
4. [ ] **Finding 2** — Warn rather than fail `flow-host` under `--remote-job`, whose bootstrap builds the environment after the preflight _(layer: cli, general)_

---

## Must Fix

### 1. The hand-off lets Python write `__pycache__` into the shipped sources, and the next unit commit stages the bytecode under `<scriptsDir>/python/`
→ [finding_1.md](feat_flow_walker_python_cutover_code_review/finding_1.md)

### 2. `doctor --remote-job` fails `flow-host` where script-driven planning is on, so a remote job stops at its preflight, before the step that builds the environment
→ [finding_2.md](feat_flow_walker_python_cutover_code_review/finding_2.md)

---

## Should Fix

### 3. `remote-run.sh`'s REPRO still plants a flat `flow_walker_state` and expects `restore` to put `.flow_walker_state` back
→ [finding_3.md](feat_flow_walker_python_cutover_code_review/finding_3.md)

### 4. `docs/cli.md` still lists "the flow walker with its gate library" among the outer-loop scripts `init` writes
→ [finding_4.md](feat_flow_walker_python_cutover_code_review/finding_4.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section has no entries.
