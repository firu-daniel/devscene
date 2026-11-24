# Code Review: feat_flow_walker_compat_command

## Context

**Branch:** `feat_flow_walker_compat_command`
**Date:** 2026-11-24
**Reviewed:** the whole branch diff against `origin/dev`, read segment by segment:
- **`host`:** the kept findings record `RevisionFindingsStore` and how `record_outcome`, `start_walk` and `current_step` write, clear and read it (Task 1), and `HarnessPredicateHost.last_refusal` (Task 2).
- **`commands`:** `render` (Task 3), `parse` (Task 4), the `devscene-flow-walker` entry point `main` with its exit-status mapping and the `[project.scripts]` entry (Task 5), and the concurrency suite (Task 6).
- **Documentation:** the package README's `## The command line` and `## Differences from flow-walker.sh` (Task 7), and the `ROADMAP.md` GraphScene row (Task 8).
- **Comparison with bash:** every rendered block, the argument checks, the exit codes and the `revision_findings` lifecycle were checked against `cli/templates/scripts/flow-walker.sh`'s `OUTPUT`, `EXIT CODES`, `# --- Arguments`, `next`, `start` and `close_round`.

14 run-artifact files excluded from the reviewed diff.

**Tests and wiring.**
- Every new module comes with its suite: `tests/test_revision_findings.py`, `tests/test_render.py`, `tests/test_arguments.py`, `tests/test_flow_walker.py` and `tests/test_flow_walker_concurrency.py`. The edited `tests/test_predicates.py`, `tests/test_re_entry.py` and `tests/test_round_gates.py` pin the new behaviour.
- Each new test opens with *"The rule this file exists to enforce"*. Each plants its repository under `tmp_path` and reads only the checkout's own graph file, read-only.
- No new test reads a tree of files, so no `treeGuards` entry is owed.
- This review ran no suite. Whether the tests pass is for the Run gates phase to establish.
- Every new public function and class has a caller outside the file that defines it: `render`, `parse`, `main`, `failure`, `RevisionFindingsStore`, `revision_findings_path` and `last_refusal`.

**Pass 0 sweep.** `review-sweep.sh` exited `0` with 0 hits, so no finding came from it. The incidental-findings grep found no `## Incidental findings (not gating)` section in this branch's `task_plan_reviews` or `architecture_reviews` rounds. The other three folders do not exist.

**Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/feat_flow_walker_compat_command_task_plan/` does not exist, so there was nothing to reconcile.

**Parity.** `phases.parity` is `false`, so no parity cross-check ran.

**Conclusion.** The wire grammar, the exit codes and the kept findings record match bash or are listed as differences under the task prompt's **Decided (2026-11-24)**. One finding remains: a module docstring that misstates when the record is cleared.

**Open question.** Three **Still open** differences in the README carry `TODO: @claude` markers but no roadmap item. They are a question in the return, not a finding.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Correct `RevisionFindingsStore`'s module rule: a round's close clears the record rather than writing the closed round's files _(layer: devscene-flow-host)_

---

## Must Fix

_None._

---

## Should Fix

### 1. `RevisionFindingsStore`'s module rule says a round close writes the closed round's files into the record, but the host clears it
→ [finding_1.md](feat_flow_walker_compat_command_code_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
