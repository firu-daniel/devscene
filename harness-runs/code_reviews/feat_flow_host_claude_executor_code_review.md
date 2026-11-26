# Code Review: feat_flow_host_claude_executor

## Context

**Branch:** `feat_flow_host_claude_executor`
**Date:** 2026-11-26
**Reviewed:** the whole branch diff against `origin/dev`, all in the `devscene-flow-host` layer:
- the plugin reader `records/plugin_contracts.py` (Task 1);
- the transcript judge `host/session_stream.py` (Task 2);
- the process supervisor `host/session_process.py` (Task 3);
- `ClaudeExecutor` with its usage sink and inactivity limit in `host/claude_executor.py` (Task 4);
- the package README and the `__init__.py` docstrings (Task 5);
- the four new test suites and their support modules `tests/fake_claude.py` and `tests/session_events.py`.

That is 14 files, +1974/−8. 11 run-artifact files excluded from the reviewed diff.

**Conventions.** Every new source module opens with a *"The rule:"* docstring and a *"Deliberately not covered"* or *"Deliberately not checked"* list. The record reader has:
- its `Final` name constants;
- a docstring naming the bash readers it reads as (`pnl_init`, `pnl_agent_tools_var`, `pnl_load_schemas`);
- one `RecordError` case per unreadable shape, each asserting the exact message.

Imports keep the layer order: `records` imports no `graphscene`, and `host` reaches `graphscene` through its public surface only. No runtime dependency was added. `NODE_INACTIVITY_LIMIT_SECONDS` is named for what it measures, as the lessons ledger requires.

**Tests.** Every new module ships its own suite, each with its *"The rule this file exists to enforce"* header. No test added on this branch reads a tree of files, so no `treeGuards` entry is owed. This review ran no suite: whether the suites pass is the Run gates phase's to establish.

**Pass 0.** The main checkout's `scripts/review-sweep.sh`, run against this checkout with `--repo`, exited `0` with 0 hits, so the sweep produced 0 findings.

The new-exported-symbol caller check ran over every `layers[].path` scope. Each new public class and function has a caller outside its defining file, either in another module or in a test, except `agent_definition_path` and `return_schema_path` (Finding 2). The task prompt's `## Decided (2026-11-25)` makes the public surface and its tests this branch's callers until #484 and #424, and that was checked against the prompt.

**Planning leads.** The planning rounds' `## Incidental findings (not gating)` sections held no entries.

**Parity.** `phases.parity` is `false`, so no parity cross-check ran.

**Probe.** One probe was run under `harness-runs/scratch/`, through the package's `probe` form. It confirmed Finding 1 on a fake session.

**Two-pass mode.** No per-task findings exist under `harness-runs/task_plan_point_reviews/feat_flow_host_claude_executor_task_plan/`, so Pass 2 had nothing to reconcile.

**Corpus staleness.** The story index's scope register records stale lines in two conventions documents, `.claude/context/conventions.md` and `.claude/context/devscene-flow-host.md`. They still describe the package as holding "executor configuration", and the `host` row does not list the executor. Those documents are not plannable targets and are routed to `corpus_staleness`, so this review files no finding for them.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — Make `agent_definition_path` and `return_schema_path` private in `records/plugin_contracts.py` _(layer: devscene-flow-host)_
2. [ ] **Finding 1** — Kill the session's process group on every path out of `run_session` and bound the post-EOF waits _(layer: devscene-flow-host)_

---

## Must Fix

### 1. `run_session` kills the group only while the leader runs, so a member that outlives a normal exit is left behind, and one holding stderr stops the run from ever returning
→ [finding_1.md](feat_flow_host_claude_executor_code_review/finding_1.md)

---

## Should Fix

### 2. `agent_definition_path` and `return_schema_path` are public but nothing outside their own module calls them
→ [finding_2.md](feat_flow_host_claude_executor_code_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from and this section is empty.
