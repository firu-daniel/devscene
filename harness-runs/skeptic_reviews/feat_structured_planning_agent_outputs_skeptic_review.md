# Skeptic Review: feat_structured_planning_agent_outputs

## Context

**Branch:** `feat_structured_planning_agent_outputs`
**Date:** 2026-11-16

**What was reviewed.** The whole-branch diff against `origin/dev`, 35 files. `devscene.config.json` → `defaultBranch` is `dev`, and this checkout has no local `dev` ref, so the remote-tracking ref was the diff base. 31 run-artifact files excluded from the reviewed diff.

**De-duplicated against.** The committed code review `harness-runs/code_reviews/feat_structured_planning_agent_outputs_code_review.md` and its Findings 1–4. Those findings, and the fixes for them now on the branch, are out of scope here. There is no committed architecture branch review for this branch, and `phases.parity` is `false`, so there is no parity review either.

**What was checked adversarially.**
- **Wiring.** `pnl_load_schemas`, `pnl_agent_schema_scan`, `object_file=` → `PD_OBJ_<node>` → `pd_ret_field` / `pd_ask_park` are all reached from `pnl_init` / `pd_reap_one`.
- **The return-block extraction in `PNL_REAP_JQ`.** Checked against the jq 1.5 floor and the contract's "last `json` fence, whitespace after" rule.
- **Every `agent_return_contract.md` heading citation, and the `**A dispatch that did not return**` anchor.** All resolve.
- **The dropped `harness_friction` and `--json-schema` paths.** No surviving reader in `cli/templates`.
- **The six schemas against the planning graph's outcome keys.** They agree.
- **The orchestrator-path callers in every mode.** The planning forks were brought in line, but one cited-section escalation list was not.

**Headline conclusion.** The branch adds new `<escalate>` arms for a gate `blocker` and for a third failed routing check, and updates the forks' trigger lists for them. The one closed list it missed is the autonomous user-review-fix fork's, for the new G.2 architecture-gate arm. On that site a headless run halts without a park (Finding 1).

---

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Add the G.2 architecture gate's `blocker` / third-failed-routing-check arm to the autonomous user-review-fix fork's closed `<escalate>` list and its Phase G origin mapping _(layer: plugin)_

---

## Must Fix

### 1. The autonomous user-review-fix fork's closed `<escalate>` list omits the new G.2 architecture-gate `blocker` / routing-check escalation
→ [finding_1.md](feat_structured_planning_agent_outputs_skeptic_review/finding_1.md)

---

## Should Fix

None.

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from. No divergence marked intentional on this branch survived to need a call-out. The one the story index marks as accepted is the post-merge forced self-adopt of this repository's own `scripts/lib/` copies (`## Context` → **Manual setup required**), and it is a documented manual step, not a code divergence.
