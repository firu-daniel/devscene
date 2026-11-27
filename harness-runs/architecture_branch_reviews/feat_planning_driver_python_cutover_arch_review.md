# Architecture review — feat_planning_driver_python_cutover

## Context

Branch `feat_planning_driver_python_cutover`, reviewed 2026-11-27 against `origin/dev...HEAD` (iteration 0). Reviewed: the new `devscene-flow-host` modules (`commands/planning_driver.py`; `host/agent_flags.py`, `node_sessions.py`, `observations.py`, `planning_executor.py`, `planning_run.py`, `run_control.py`, `run_exits.py`, `run_records.py`; `records/core_limits.py`, `mcp_servers.py`) and their suites; the `records` extensions (`config.py`, `ledger.py`, `clarifications.py`); the `cli` template changes (`autonomous-watcher.sh`, `flow-walker.sh`, `lib/harness-run-lib.sh` → `hr_flow_host_missing` / `hr_flow_host_exec`, the three deleted `lib/planning-*-lib.sh`, `outerLoopScripts.ts`); the docstring-only `graphscene` edits; and the `plugin` and `docs/` prose. 40 run-artifact files excluded from the reviewed diff.

Headline: the layering holds. Every new module sits in the internal layer its work belongs to. Imports point down only (`commands` → `host` → `records`), `records` imports no `graphscene`, and `graphscene` is reached only through its public surface. Exit statuses are decided in `commands` alone. The new console-script name is mirrored in `harness-run-lib.sh` with its owner declared and a test holding it. Every new module carries *"The rule:"* and *"Deliberately not covered"*, and every new module has its own suite. One Must Fix remains. The watcher now launches the flow host other than through `flow-walker.sh`, which two conventions documents state as the rule. The story plan says this deviation is recorded as a `stale-rule` entry, but that entry exists nowhere, because this branch's own script-driven planning dropped `corpus_staleness`.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Record the three stale conventions sentences the cutover falsified, which no channel carries _(layer: general)_
2. [x] **Finding 4** — Register the driver's return-field check as a tree guard over `plugin/schemas/**` _(layer: general)_
3. [ ] **Finding 3** — Compose the main checkout's commit-wrapper path in one place, not in `commands` and `host` both _(layer: devscene-flow-host)_
4. [ ] **Finding 2** — Stop using `RecordError` for a host write collision and a host-side ledger check _(layer: devscene-flow-host)_

## Must Fix

### 1. Record the three stale conventions sentences the cutover falsified, which no channel carries
→ [finding_1.md](feat_planning_driver_python_cutover_arch_review/finding_1.md)

## Should Fix

### 2. Stop using `RecordError` for a host write collision and a host-side ledger check
→ [finding_2.md](feat_planning_driver_python_cutover_arch_review/finding_2.md)

### 3. Compose the main checkout's commit-wrapper path in one place, not in `commands` and `host` both
→ [finding_3.md](feat_planning_driver_python_cutover_arch_review/finding_3.md)

### 4. Register the driver's return-field check as a tree guard over `plugin/schemas/**`
→ [finding_4.md](feat_planning_driver_python_cutover_arch_review/finding_4.md)
