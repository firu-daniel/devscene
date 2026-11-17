# Skeptic Review: feat_structured_outputs_unit_loop

## Context

**Branch:** `feat_structured_outputs_unit_loop`
**Date:** 2026-11-17

**What was reviewed.** The whole branch diff against the default branch `dev`. This run copy has no local `dev` ref, so the diff base is `origin/dev`. The diff covers 12 files:
- the three new return schemas `plugin/schemas/layer-reviewer.return.json`, `plugin/schemas/layer-implementer.return.json` and `plugin/schemas/test-fix-plan-writer.return.json`;
- the three agents' `## Output contract` rewrites;
- the callers moved onto the outcome form: `unit_loop_core.md`, `plan_orchestration_instructions_core.md`, `user_review_fixes_instructions_core.md`, `user_review_fixes_instructions_autonomous.md` and `untrusted_input.md`;
- the `## Who may cite this` roster of `agent_return_contract.md`.

18 run-artifact files were excluded from the reviewed diff.

**De-duplicated against.** `harness-runs/code_reviews/feat_structured_outputs_unit_loop_code_review.md` and its four findings, all applied:
1. `flags` on the dispositioned outcomes;
2. quoting `cause` on an off-row `already passing`;
3. the stop-condition findings-path clause;
4. the stale "carry the marker" wording.

No parity review exists, because `phases.parity` is `false`. No architecture branch review exists for this branch. No planning round for this branch carries an `## Incidental findings (not gating)` section.

**What was checked.**
- **Wiring (check 1).** Every escalation route the branch added reaches a stop-condition entry and a binding-table row. The return schemas are read only by the planning driver (`planning-node-lib.sh`) and by `cli/test/agent-return-schemas.test.mjs`. That matches `docs/structured-agent-returns.md` → `### Validation on each path, and why no validator script`, which gives orchestrating sessions the routing check instead.
- **Citations (check 3).** The decision-record rules the story plan cites are present and say what the plan claims: *"Everything a caller routes or records on is a field"*, *"The literal a caller matched before becomes the outcome value it routes on"* and the `error:` → outcome decision.
- **Leftover readers of the old form.** A repo-wide grep finds no plugin or template caller still reading these three agents' old prose forms.
- **Outcome names (check 4, Leg 2).** `returned`, `questions` and `blocker` match the precedent the earlier schemas set.

**Headline.** One net-new defect. The autonomous user-review fork keeps a closed list of the sites its `<escalate>` reroute covers. That list lost the off-row `already passing` escalation in the move to outcomes, so it now disagrees with the unit loop and with its own core's binding row.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Add the off-row `already passing` escalation to the autonomous user-review fork's closed `<escalate>` list _(layer: plugin)_

---

## Must Fix

_None._

---

## Should Fix

### 1. The autonomous user-review fork's closed `<escalate>` list no longer covers an `already passing` return on a row other than `G.4`
→ [finding_1.md](feat_structured_outputs_unit_loop_skeptic_review/finding_1.md)

---

## Nice to Have

_None._

---

## Intentional divergences (call-outs, not fixes)

_None. `phases.parity` is `false`, and no divergence in this diff is marked intentional._
