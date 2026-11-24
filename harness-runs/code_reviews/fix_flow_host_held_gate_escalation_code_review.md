# Code Review: fix_flow_host_held_gate_escalation

## Context

**Branch:** `fix_flow_host_held_gate_escalation`
**Date:** 2026-11-24
**Reviewed:** the whole branch diff against `origin/dev`: three files, 51 insertions and 18 deletions, all in the `devscene-flow-host` layer.
- Task 1 states the host's held-gate order as a *"The rule:"* bullet in `devscene-flow-host/src/devscene_flow_host/host/round_gates.py`. It drops the matching *"Deliberately not covered"* bullet and the `TODO: @claude` comment at `_redispatch`. It rewrites `devscene-flow-host/tests/test_round_gates.py`'s header and the existing held-gate case's docstring, and adds `test_a_held_error_waits_while_its_refused_sibling_is_refused_again`.
- Task 2 moves the rule into `devscene-flow-host/README.md` → **Recording a gate.**, removes the *"One departure from the bash walker remains"* paragraph, and moves **The held-gate escalation** from **Still open** to **Chosen** in `## Differences from flow-walker.sh`.

8 run-artifact files excluded from the reviewed diff.

**Headline conclusions.**
- **Executable code.** The diff to `round_gates.py` touches only the module docstring and the deleted comment. No executable line moves, which is what the story index's first `Top risks:` entry required. #465's `RevisionFindingsStore` handling and `commands/render.py` → `_refused` are therefore unchanged.
- **The new case's literals.** They were checked against the rule and against `cli/templates/scripts/flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar, not against the code. `plan_round`'s `gates` order is `business_parity_review, architecture_review, plan_review` (`cli/templates/scripts/flows/task_plan_writing.v4.graph.json`). So the first held gate is `architecture_review`, `held` lists `architecture_review` and then `plan_review`, and one `refused:` line goes with the gate held by its third refusal. Each of these matches the expected `Stop`. Together, the two cases pin both arms of "once every re-dispatched gate has a verdict or is held".
- **Citations.** Every citation the README's new **Chosen** entry carries resolves: `flow-walker.sh` → `ROUNDS`, `STATE` and `record_in_set`; `flow-walker-resume.test.mjs` → *"(8) with the saved walk deleted and two of three round files committed, start dispatches only the third gate at counter 0"*; `flow-walker-fan-out.test.mjs` → (5), (7), (9), (10) and (11); and both `test_round_gates.py` case names.
- **Stale references.** A `git grep` over `devscene-flow-host`, `docs`, `ROADMAP.md` and `ARCHITECTURE.md` finds no `#472`, `held-gate` or `TODO: @claude` reference left stale. The three remaining `TODO: @claude` markers in `commands/render.py` belong to #475.
- **Tests.** This review ran no test, so the Run gates phase establishes whether they pass.
- **Pass 0.** `review-sweep.sh` exited `0` with no hits, so no finding came from it. Half (b) found no new exported symbol: the only added definition is a `pytest` case.
- **Other sources.** The planning rounds' `## Incidental findings (not gating)` grep returned no leads. `phases.parity` is `false`, so no parity check ran.
- **Pass 2.** The per-unit findings root `harness-runs/task_plan_point_reviews/fix_flow_host_held_gate_escalation_task_plan/` does not exist, so Pass 2 had nothing to reconcile.

One wording finding is left.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Cite the held-gate rule by file in the test header instead of "rule above" _(layer: devscene-flow-host)_

---

## Must Fix

_None._

---

## Should Fix

_None._

---

## Nice to Have

### 1. The test header points at "`round_gates`' rule above", but that rule is in another file
→ [finding_1.md](fix_flow_host_held_gate_escalation_code_review/finding_1.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so this section is empty.
