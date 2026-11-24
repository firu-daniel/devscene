# Skeptic Review: fix_flow_host_held_gate_escalation

## Context

**Branch:** `fix_flow_host_held_gate_escalation`
**Date:** 2026-11-24
**Reviewed:** the adversarial pass over the whole branch diff against `origin/dev`. It covers three files in the `devscene-flow-host` layer: `README.md`, `src/devscene_flow_host/host/round_gates.py` (docstring and deleted `TODO` only) and `tests/test_round_gates.py`. 10 run-artifact files excluded from the reviewed diff. It is de-duplicated against `harness-runs/code_reviews/fix_flow_host_held_gate_escalation_code_review.md` and its one finding. No parity review applies, because `phases.parity` is `false`, and no architecture branch review exists for this branch. The planning rounds' incidental-findings grep returned no leads.

**What was checked.**
- **Check 1 (wiring).** No executable line changed, so there is no new caller to find.
- **Check 2.** The parity leg is inert. No runtime address is involved.
- **Check 4.** The task prompt's **Decided** section authorizes the held-gate divergence.
- **Check 3 (citations).** I checked whether each citation in the README's new **Chosen** entry supports its claim, not only whether it resolves. One does not. The entry says bash's `start` reopens only the missing gates and cites resume test (8). But the refused file on disk reads `unreadable`, so `start` reopens the whole set, which is resume test (9). That is Finding 1.

**Headline.** No Must Fix. One Should Fix, a README-only correction.

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Correct the bash resume mechanism and suite case in the README's held-gate **Chosen** entry _(layer: devscene-flow-host)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The Chosen entry says bash's resume reopens only the missing gates, but a refused file makes it reopen the whole set
→ [finding_1.md](fix_flow_host_held_gate_escalation_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Out of scope / verified-OK (intentional divergences / call-outs)

- **The held-gate order itself.** The host re-dispatches the refused gates and then escalates at the round's next join. Bash escalates at once. The task prompt's **Decided** section (2026-11-24) records this as the host's chosen order, and `round_gates.py`'s executable lines are unchanged. Both of the new test case's expected `Stop` values follow `flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar in `plan_round`'s `gates` order. Please confirm.
