# Code Review: feat_structured_planning_agent_outputs

## Context

**Branch:** `feat_structured_planning_agent_outputs`
**Date:** 2026-11-16
**Reviewed:** the whole branch diff against `origin/dev`, 35 files.
- `plugin`: the new shared module `plugin/instructions/agent_return_contract.md` (Task 1), the `## Return schema` and `### Return fields` of the six planning agents (Tasks 2–5), and every orchestrator-path caller of their returns across the planning, implementation, user-review-fix, fix-plan and QA flows (Tasks 6–9).
- `cli`: the driver switch in `cli/templates/scripts/lib/planning-node-lib.sh` and `planning-driver-lib.sh` from `--json-schema` / `structured_output` to the return block, with the driver stubs and suites rewritten to match (Tasks 10–12), and the new static suite `cli/test/agent-return-schemas.test.mjs` (Task 13).
- `general`: `docs/structured-agent-returns.md` and the corrected `docs/flow-graph-walker.md`, `docs/watcher.md`, `ARCHITECTURE.md` and `docs/analyze.md`, plus the suite's two `treeGuards` entries (Tasks 14–15).

`devscene.config.json` → `defaultBranch` is `dev`. This checkout has no local `dev` branch, so the diff base is the remote-tracking ref `origin/dev` (merge base `d953d476`). 26 run-artifact files excluded from the reviewed diff.

**Headline conclusions.**
- The six schemas, their `### Return fields`, the module's roster and every `` `<agent>.<field>` `` citation agree with one another and with the planning graph's outcome keys.
- The re-derivation greps turn up no orchestrator-path caller still parsing a retired `verdict:`, `## Questions` or `no_ui: true` return of these six agents. Two agent definitions still name a retired literal in prose (Finding 2).
- Every stub that stands in for a node session now emits only `result` text ending in a return block, as `<state_dir>/lessons.md` requires of a check that moves to a new field.
- The new tree-reading suite is registered in `treeGuards` in this same branch.
- This review ran no test. Whether the suites pass is for the Run gates round to establish.
- `phases.parity` is `false`, so no parity cross-check applies.
- The defect that matters: the two drivers disagree on a return the contract says both treat alike. That is Finding 1.

Per-unit review folder `harness-runs/task_plan_point_reviews/feat_structured_planning_agent_outputs_task_plan/` does not exist (per-unit review was off), so there was nothing to carry over.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the committing role flips each one to `[x]` as that fix's commit lands: the `committer` agent in every flow that dispatches one, and the orchestrator itself in the supervised fix flow, which dispatches none. `[ ]` markers anywhere else, such as sub-step bullets inside per-finding files, are informational only. They are never the iteration source, and the committer never touches them.

Each entry resolves to `harness-runs/code_reviews/feat_structured_planning_agent_outputs_code_review/finding_<K>.md` through its `**Finding K**` reference. The leading `N.` is the ship order; `K` is the finding's own number.

1. [ ] **Finding 2** — Replace the retired `verdict: FAIL` / `no_ui: true` literals in the two UI-test agent definitions _(layer: plugin)_
2. [ ] **Finding 4** — Make `pnl_load_schemas` report a dispatch node with no string `agent` at `pnl_init` _(layer: cli)_
3. [ ] **Finding 3** — Narrow the suite's roster check to the `plugin/**/*.md` set its `treeGuards` entry covers _(layer: cli)_
4. [ ] **Finding 1** — Class a round gate's `PASS`, or a `FAIL`, with no `findings_file` as infrastructure in `PNL_REAP_JQ`, so the driver re-dispatches it as the contract says _(layer: cli, general)_

---

## Must Fix

### 1. The driver parks a round gate's `PASS` with no `findings_file` at once, where the contract and the orchestrator path re-dispatch it up to three times
→ [finding_1.md](feat_structured_planning_agent_outputs_code_review/finding_1.md)

---

## Should Fix

### 2. Two UI-test agent definitions still name the retired return literals `verdict: FAIL` and `no_ui: true`
→ [finding_2.md](feat_structured_planning_agent_outputs_code_review/finding_2.md)

---

## Nice to Have

### 3. The roster check in `agent-return-schemas.test.mjs` reads every file under `plugin/`, but the suite is registered only for `plugin/**/*.md`
→ [finding_3.md](feat_structured_planning_agent_outputs_code_review/finding_3.md)

### 4. `pnl_load_schemas` skips a dispatch node with no string `agent`, so its own "names no agent" fault can never fire
→ [finding_4.md](feat_structured_planning_agent_outputs_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

These are not fixes and do not appear in the Phase 2 Readiness list. `phases.parity` is `false` in `devscene.config.json`, so there is no reference implementation to diverge from, and this section has no parity call-out.
