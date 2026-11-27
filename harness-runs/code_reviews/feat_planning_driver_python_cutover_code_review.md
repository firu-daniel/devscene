# Code Review: feat_planning_driver_python_cutover

## Context

**Branch:** `feat_planning_driver_python_cutover`
**Date:** 2026-11-27
**Reviewed:** the whole branch diff against `origin/dev`, in seven segments:

- the watcher's launch of `devscene-planning-driver` (`autonomous-watcher.sh` → `planning_driver_ready`, `planning_driver_run`, `session_env`, `session_flags`) and the shared launch route (`lib/harness-run-lib.sh` → `hr_flow_host_missing`, `hr_flow_host_exec`, `flow-walker.sh`);
- the retirement of the three `lib/planning-*-lib.sh` libraries and their `cli` suites (`outerLoopScripts.ts`, `outer-loop-scripts.test.mjs`, `agent-return-schemas.test.mjs`, `watcher-planning-driver.test.mjs`);
- the new `devscene-flow-host` `records` readers (`core_limits.py`, `mcp_servers.py`, and the `config.py`, `ledger.py`, `clarifications.py` extensions);
- the new `host` modules (`run_control.py`, `run_records.py`, `observations.py`, `node_sessions.py`, `agent_flags.py`, `planning_executor.py`, `planning_run.py`, `run_exits.py`);
- the command `commands/planning_driver.py` and its console-script entry;
- the `pytest` suites, among them the end-to-end `test_planning_driver_walk.py` and `test_planning_driver_control.py` and the new `test_driver_return_fields.py` with its two `treeGuards` entries;
- the docstring-only `graphscene` and `plugin` edits, and the prose in `ARCHITECTURE.md`, `docs/` and the READMEs.

40 run-artifact files excluded from the reviewed diff.

**Headline.** No test suite was run by this review; whether they pass is Run gates' to establish. Every new module has its own suite.

- **The Pass 0 sweep** (`review-sweep.sh`, exit `0`) printed no hits, so none became a finding.
- **The caller check (half (b))** found nothing dead. Every new public function and class is either on the driver's call chain (`devscene-planning-driver` → `commands/planning_driver.py` → `run_planning` / `act_on_exit` and the modules they compose) or used inside its own module.
- **Parity** does not apply: `phases.parity` is `false`.
- **The incidental-findings grep** over the planning rounds' `## Incidental findings (not gating)` sections found no lead.
- **Pass 2** had nothing to reconcile: `per_task_findings_root`, `harness-runs/task_plan_point_reviews/feat_planning_driver_python_cutover_task_plan/`, does not exist.

The four architecture-branch-review findings have already landed, and none is repeated here. Each bash-driver behaviour the story plan lists — STOP, PAUSE, the kill switch, the counter, the cap, retries, parks, pause files, node records, observations — was traced to a Python owner.

One cross-module defect remains (Finding 1, confirmed by an executed probe). `NodeSessions` pairs a usage record with its `Launch` row only on equal results, but `PlanningExecutor` changes a result after its usage was recorded. So every session it refuses is logged as a total-run timeout and loses its row.

Four further items need a decision rather than a fix, so they are returned as questions, not findings:

- the new Python tree guard covers `plugin/` and `cli/` paths whose units run it through `npm test`, which exits `1` with `Could not find 'tests/test_driver_return_fields.py'` (probe executed);
- a node's formatted output and run-stream events now reach the run log only when its session ends;
- the bash driver's per-strike undelivered observation is gone;
- the two end-to-end suites spend GraphScene's real 60-second backoffs.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below top to bottom, and the committing role flips each one to `[x]` as that fix lands. That role is the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised fix flow, which runs none. `[ ]` markers anywhere else are informational only.

Each entry resolves to `harness-runs/code_reviews/feat_planning_driver_python_cutover_code_review/finding_<K>.md` through its `**Finding K**` reference.

1. [x] **Finding 2** — Replace the plan task numbers in the flow host's docstrings with the files they mean _(layer: devscene-flow-host)_
2. [x] **Finding 1** — Pair a session whose `Completed` result `PlanningExecutor` turned into `Failed("infra")` with its `Launch` row _(layer: devscene-flow-host)_

---

## Must Fix

### 1. `NodeSessions` never pairs a session whose `Completed` result `PlanningExecutor` turned into `Failed("infra")`, so its row is blanked and the log claims a total-run timeout
→ [finding_1.md](feat_planning_driver_python_cutover_code_review/finding_1.md)

---

## Should Fix

### 2. The flow host's docstrings cite this branch's plan task numbers, which no reader can resolve after the merge
→ [finding_2.md](feat_planning_driver_python_cutover_code_review/finding_2.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
