# Code Review: fix_planning_node_tool_check

## Context

**Branch:** `fix_planning_node_tool_check`
**Date:** 2026-11-16
**Reviewed:** the whole branch diff against `dev`. This checkout has no local `dev` branch, so the diff was taken against the remote-tracking `origin/dev`. It covers seven files in three segments:
- **The `init` check (Task 1).** `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`, which now refuses on `$extra` only and reports `$missing` on a new `withheld=` key. Also `pnl_reap`'s key list, the module header and REPRO, and `cli/test/planning-node-lib.test.mjs`.
- **The driver's log line (Task 2).** `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_reap_one`, the stub's `withhold` mode in `cli/test/helpers/planning-driver.mjs`, and the new walk case in `cli/test/planning-driver-walk.test.mjs`.
- **The records (Task 3).** The 2.1.325 measurements and the one-way decision of record in `docs/flow-graph-walker.md`, and the unmeasured-facts bullet in `docs/watcher.md`.

8 run-artifact files excluded from the reviewed diff.

**Conclusions:**
- **The protection is kept.** A session with an undeclared `init` tool is still an `agent`-class `error` at once, and a lacking tool cannot mask an extra one (the `mixed` case). A declared `mcp__` tool absent from `init` is never reported as withheld.
- **The rest checks out.** Every changed module header and test header was updated with the change. The bash 3.2 and jq 1.5 floors hold on the added lines. No new exported symbol was added, and no tree-reading test was added.
- **The record is faithful.** Every 2.1.325 fact recorded in `docs/flow-graph-walker.md` matches the task prompt's `## Measured` section and its `## What happened` log line. The measuring machine's absolute path is rendered as `<main checkout>/plugin`. The remaining unmeasured fact is deferred to #379 with its `ROADMAP.md` row, following the precedent this file already sets for #159.
- **Lessons ledger.** Applied the `Trust checks` lessons. The dropped protection, refusing on `missing`, is only needed to catch an unknown agent, and the other route to that is the no-`init` rule, which is measured in `docs/orchestrator-cost-measurement.md` → `## 4.`, the `Unknown agent` row. The narrower-shadow cost is recorded rather than hidden.
- **Not regraded.** The self-adopted copies under `scripts/lib/` are stale on purpose. The story index's **Manual setup required:** line records this, so it is not a finding.
- **Tests.** This review ran no suite. Whether the suites pass is the Run gates phase's to establish.
- **Parity.** `phases.parity` is `false`, so no parity cross-check applies.

One finding remains.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Make the withheld-tools `[plan-drive]` line say that the lack is never refused, not that the session was not refused _(layer: cli, general)_

---

## Must Fix

_None._

## Should Fix

### 1. The withheld-tools log line says "not refused" on sessions the driver did refuse
→ [finding_1.md](fix_planning_node_tool_check_code_review/finding_1.md)

## Nice to Have

_None._

---

## Intentional divergences from the reference implementation (call-out)

_None: `phases.parity` is `false`._
