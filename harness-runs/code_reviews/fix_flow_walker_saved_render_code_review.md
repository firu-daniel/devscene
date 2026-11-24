# Code Review: fix_flow_walker_saved_render

## Context

**Branch:** `fix_flow_walker_saved_render`
**Date:** 2026-11-24
**Reviewed:** the whole branch diff against `origin/dev`: 12 files, all in the `devscene-flow-host` layer.
- The new host record `host/printed_reads.py` (`PrintedReads`, `read_printed`, `PrintedReadsStore`, Task 1).
- Its writers `record_outcome` (`host/round_gates.py`) and `start_walk`, and its reader `current_step` (`host/re_entry.py`) (Task 2).
- `commands/render.py`, now printing from `HostStep.printed` with the three `TODO: @claude` markers removed, plus the `records/index_evidence.py` docstring (Task 3).
- The command-level pins in `tests/test_flow_walker.py` (Task 4).
- The README's **Printed reads.** paragraph, the narrowed **Chosen** *"`current` re-renders"* entry and the emptied **Still open** list (Task 5).
- The suites that ship with each task.

11 run-artifact files excluded from the reviewed diff.

**Tests.** Every changed module has its accompanying suite: `tests/test_printed_reads.py` (new, with the *"The rule this file exists to enforce"* header), `tests/test_re_entry.py`, `tests/test_round_gates.py`, `tests/test_render.py`, `tests/test_index_evidence.py` and `tests/test_flow_walker.py`. Expected values are literals. No tree-reading test was added, so no `treeGuards` registration is owed. This review ran no suite; whether they pass is the Run gates phase's to establish.

**Pass 0 sweep.** `review-sweep.sh` exited `0` with no hits. The new-exported-symbol caller check over every `layers[].path` found callers outside the defining file for `PrintedReads`, `read_printed`, `PrintedReadsStore` and `printed_reads_path`. `PRINTED_READS_DIRECTORY` is used only inside `printed_reads.py`, as `REFUSALS_DIRECTORY` and `REVISION_FINDINGS_DIRECTORY` are. It is the `Final` directory constant `.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth` requires, not an unwired feature.

**Other checks.** The story's claim that the third difference is not one holds. `cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_index_evidence` prints `evidence: … ## Rejected findings` only `if (!rj)`, then every open `- ` line under any such heading in file order, which is what `read_index_evidence` collects and `render` prints. Imports point down only (`host` imports `records` and `graphscene`'s public surface). Every new record write happens under `RefusalStore`'s lock. No planning-round incidental findings were filed for this branch. Per-unit review folders: none exist under `harness-runs/task_plan_point_reviews/fix_flow_walker_saved_render_task_plan/`, so Pass 2 carried nothing over.

**Parity.** `phases.parity` is `false`, so there was no parity cross-check.

**Findings.** Two remain. Finding 1, a stale printed-reads record after a read fault, was confirmed by a probe run.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 2** — Pin a walk refusal inside `record_outcome`'s lock leaving the printed reads byte-identical _(layer: devscene-flow-host)_
2. [ ] **Finding 1** — Clear the printed-reads record when `read_printed` raises after the walk is saved _(layer: devscene-flow-host)_

---

## Must Fix

### 1. A read fault after the walk is saved leaves the previous step's printed reads, so `current` prints the new step from them
→ [finding_1.md](fix_flow_walker_saved_render_code_review/finding_1.md)

---

## Should Fix

### 2. The refused-result pin never reaches the lock, so the story's top risk (a write on a walk refusal) is untested
→ [finding_2.md](fix_flow_walker_saved_render_code_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
