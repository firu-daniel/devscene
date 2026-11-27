# Skeptic Review: feat_planning_driver_python_cutover

## Context

**Branch:** `feat_planning_driver_python_cutover`
**Date:** 2026-11-27
**Reviewed:** the whole branch diff against `origin/dev`, read adversarially in five segments:

- the watcher's launch of `devscene-planning-driver` (`planning_driver_ready`, `planning_driver_run`, `session_env`, `session_flags`) and `lib/harness-run-lib.sh` → `hr_flow_host_missing` / `hr_flow_host_exec`;
- the composition and drive in `host/planning_run.py` and `commands/planning_driver.py`;
- the exit actions in `host/run_exits.py`, `host/run_records.py` and `host/observations.py`;
- the sinks and executor wrappers in `host/node_sessions.py`, `host/planning_executor.py` and `host/agent_flags.py`;
- the `records` readers.

The retired bash driver (`lib/planning-driver-lib.sh` and `lib/planning-node-lib.sh` at `origin/dev`) was read function by function as the claimed spec. GraphScene's `engine/set_execution.py` was read for the retry, backoff and `Launch` semantics.

48 run-artifact files excluded from the reviewed diff.

**De-duplicated against:**

- `harness-runs/code_reviews/feat_planning_driver_python_cutover_code_review.md`: findings 1–2, plus the four questions its Context lists;
- `harness-runs/architecture_branch_reviews/feat_planning_driver_python_cutover_arch_review.md`: findings 1–4.

`phases.parity` is `false`, so no parity review exists and check 2's parity leg is inert.

**Headline.** No new caller gap was found. Every new host module is on the chain `devscene-planning-driver` → `run_planning` / `act_on_exit`, and the watcher reaches the command through `hr_flow_host_exec`. Every docstring citation of a retired bash function was opened at `origin/dev` and matches.

One net-new defect remains: a pilot behaviour that was dropped without being marked. An escalation park for a gate whose every attempt failed for an infrastructure reason no longer lists those attempts (Finding 1, Should Fix).

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Keep each node's infrastructure-attempt log and list it in an escalation park, as `pd_session_detail` did _(layer: devscene-flow-host)_

---

## Must Fix

_None._

---

## Should Fix

### 1. An escalation park for a gate whose three attempts all failed for an infrastructure reason no longer lists those attempts
→ [finding_1.md](feat_planning_driver_python_cutover_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so no reference-implementation divergence is called out. Each divergence below from the retired bash pilot is authorised by the task prompt or the story plan, and the authorisation was confirmed at its source:

- **`NODE_INACTIVITY_LIMIT_SECONDS` is fixed at 2685.0.** The watcher's `STALL_KILL_SECS - POLL_INTERVAL_SECS` is no longer derived. Source: the task prompt's lead names the constant.
- **The driver process itself runs after `session_env`'s `unset`.** Source: the story plan → *"The environment."*
- **At most 5 dispatches run at once.** Source: the task prompt, `## Decided (2026-11-26)`.
