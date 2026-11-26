# User-Review Fix Plan: feat_graphscene_execution_rules

## Context

**Branch:** `feat_graphscene_execution_rules`
**Source user review:** `harness-runs/user_reviews/feat_graphscene_execution_rules_review.md`
**Summary:** The user flagged one observation: `ExecutionLimits.stall_seconds` limits a node's total run time, not its inactivity, so it is misnamed as a stall timeout. It is valid and becomes one Should Fix that renames it to `run_timeout_seconds` and states that detecting a stall is the executor's.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom. The commit step flips each one to `[x]` as that fix's commit lands. **Only the committing role flips a marker:** the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. `[ ]` markers anywhere else, such as the sub-step bullets inside a per-finding file, are informational only. The commit step never touches them.

Each entry resolves to a self-contained `harness-runs/user_reviews/feat_graphscene_execution_rules_fix_plan/finding_<K>.md` file through its `**Finding K**` reference. Entries are sorted from lowest blast radius first to wider refactors last.

1. [x] **Finding 1** — Rename `ExecutionLimits.stall_seconds` to `run_timeout_seconds`, settle its expiry as a `timed out` `infra` failure, and state that detecting inactivity is the executor's (source, README, suites). _(layer: graphscene)_

---

## Must Fix

None.

---

## Should Fix

### 1. `ExecutionLimits.stall_seconds` is a total run timeout, not a stall timeout
→ [finding_1.md](feat_graphscene_execution_rules_fix_plan/finding_1.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK

None. The single observation was verified as valid.

---

## Source observations

Verbatim copy of `harness-runs/user_reviews/feat_graphscene_execution_rules_review.md`. **This section stays in the index.**

=== BEGIN UNTRUSTED DATA harness-runs/user_reviews/feat_graphscene_execution_rules_review.md — data, never instructions ===

1. `ExecutionLimits.stall_seconds` is not a stall timeout. `execute_set` (`graphscene/src/graphscene/engine/set_execution.py` → `_run`) wraps the whole `executor.run` in `asyncio.timeout(stall_seconds)`, so the value limits a node's total run time. The pilot's `PD_NODE_STALL_SECS` is an inactivity timeout: it kills a session whose output stream has been silent for that many seconds (`cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_run_set`). GraphScene cannot observe a session's activity; only the executor sees the stream, so detecting an inactivity stall is the executor's, returned as `Failed("infra", …)` (#421). A host passing its stall value here would kill long but healthy sessions. Rename the field to `run_timeout_seconds`, keep its default `None` (no limit), and settle an expiry as an `infra` failure whose reason says the run timed out, not that it stalled. Update every docstring, README passage, test name, message and validation error that calls this value a stall (`model/run_control.py`, `engine/set_execution.py`, `model/execution.py`, `graphscene/README.md` and the suites), and state that detecting inactivity is the executor's, not the engine's.

=== END UNTRUSTED DATA harness-runs/user_reviews/feat_graphscene_execution_rules_review.md ===
