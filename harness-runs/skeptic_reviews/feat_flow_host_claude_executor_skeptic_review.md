# Skeptic Review: feat_flow_host_claude_executor

## Context

**Branch:** `feat_flow_host_claude_executor`
**Date:** 2026-11-26
**Reviewed:** the whole-branch diff against `origin/dev`, 14 files, all in the `devscene-flow-host` layer:
- `records/plugin_contracts.py`;
- `host/session_stream.py`, `host/session_process.py` and `host/claude_executor.py`;
- the README and `__init__.py` docstrings;
- four test suites with their support modules.

14 run-artifact files were excluded from the reviewed diff.

**De-duplicated against** the committed code review `harness-runs/code_reviews/feat_flow_host_claude_executor_code_review.md` and its two findings (group kill on every path, both applied; private path helpers, applied). No branch-level architecture review exists for this branch, and `phases.parity` is `false`, so there was no parity review and check 2's parity leg did not run.

**Planning leads.** The planning rounds' `## Incidental findings (not gating)` sections hold no entries.

**What was verified and holds:**
- `graphscene/src/graphscene/model/execution.py` says an undeclared outcome is *"the walk's to refuse, never the executor's to check"*.
- `NODE_INACTIVITY_LIMIT_SECONDS = 2685.0` matches `autonomous-watcher.sh` → `planning_driver_run`'s `STALL_KILL_SECS - POLL_INTERVAL_SECS` under the defaults (2700, 15, with `STALL_WARN_SECS` 1200 below it).
- `judge_session`'s clause order and reasons match `PNL_REAP_JQ`.
- The `--json-schema` rationale matches the task prompt's 2.1.332 measurement.
- No caller in production is expected, by the prompt's `## Decided (2026-11-25)`.
- Overriding a result with a stall matches `pd_reap_one`.

**Headline.** One net-new Must Fix. What the session produced never leaves `ClaudeExecutor.run`: the stdout stream, the stderr tail, the exit status and the validated return object. `session_process.py` defers writing the stream to #484, but #484 is never handed it. The return fields the pilot's driver reads (`questions`, `tasks_count`, `tests_count`, `reason`) are validated and then discarded.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Carry the stream, stderr tail, exit status and validated return object out of `ClaudeExecutor.run` on `SessionUsage` _(layer: devscene-flow-host)_

---

## Must Fix

### 1. The session's stream, stderr tail, exit status and validated return object never leave `ClaudeExecutor.run`, so the #484 deferral cannot hold and the return fields the pilot reads are lost
→ [finding_1.md](feat_flow_host_claude_executor_skeptic_review/finding_1.md)

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

Two divergences from `PNL_REAP_JQ`, both documented, survive check 4:

- **An undeclared outcome is `Completed`.** Leg 1: the pilot's refusal is intended, but GraphScene moves it to the walk. Leg 2: no precedent in the layer conflicts.
- **The findings-file presence check is left to `host/round_gates.py` → `record_outcome`.** Leg 1: `Dispatch` cannot tell a round gate from a writer. Leg 2: `record_outcome` is the existing precedent.

For the user to confirm: an `init` granting undeclared tools is classed `agent`, kept from the pilot, although GraphScene defines `agent` as *"the agent finished and reported that it failed"*.
