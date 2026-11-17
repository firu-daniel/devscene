# Code Review: feat_structured_outputs_unit_loop

## Context

**Branch:** `feat_structured_outputs_unit_loop`
**Date:** 2026-11-17
**Reviewed:** the whole branch diff against the default branch `dev` (this run copy has no local `dev` ref, so the diff base is `origin/dev`, merge base `b07ff5c8`). That covers 12 files: the three new return schemas `plugin/schemas/layer-reviewer.return.json`, `plugin/schemas/layer-implementer.return.json` and `plugin/schemas/test-fix-plan-writer.return.json`, the three agent definitions' `## Output contract` / `### Return fields` rewrites, and the callers moved onto the field-citation form. The callers are `plugin/instructions/unit_loop_core.md`, `plugin/instructions/plan_orchestration_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_autonomous.md`, `plugin/instructions/untrusted_input.md` and the `## Who may cite this` roster of `plugin/instructions/agent_return_contract.md`. 12 run-artifact files excluded from the reviewed diff.

**Headline.** The adoption is mechanically sound. Each schema is in the closed dialect. Each definition carries the canonical return-block sentence verbatim and a `### Return fields` list that names exactly the schema's properties. `npm test --workspace cli -- test/agent-return-schemas.test.mjs` passes 44 of 44, and `npm test --workspace cli -- test/run-gates-park-answer.test.mjs` passes 8 of 8, so every text G.2 pins is still byte-identical. A grep across `plugin/`, `cli/templates/` and `docs/` for the old return literals (`blocker: prohibited`, `prohibited — `, `already passing — `, `pending — questions for user`, `item 7`, `fix_plan_file:`, `not_fixable:`) finds no caller of these three agents still reading the old prose form. The commit-body cause agreement (goal 3) holds: `layer-implementer.cause` and the detail file's `**Cause:** ` line are tied by the same sentence in both record paragraphs, and `ucl_record_cause` still reads the detail file.

**Pass 0.** Half (a) is disabled because this project's sweep list carries no regexes. That is a configuration gap, not a clean sweep. Half (b) found no new exported symbol: the diff adds only Markdown and JSON, and the static suite above loads and holds the three new schema files.

**Parity.** `phases.parity` is `false`, so nothing was cross-checked against a reference implementation, and the call-out section below is empty.

**Not a finding.** `.claude/context/plugin.md` → `## Wires: dispatch in, return out` still states *"A return is a fenced block of `key: value` lines"*, citing `layer-reviewer.md` and `layer-implementer.md`. This branch falsifies that rule. The story plan's scope register (row 15) already routes it to a `stale-rule` entry, because a conventions document is not a plannable target.

**Pass 2.** The supplied `per_task_findings_root` (`harness-runs/task_plan_point_reviews/feat_structured_outputs_unit_loop_task_plan/`) does not exist because per-unit review was off in this flow, so nothing was carried over.

What remains is one contract gap that drops a mandatory report on two of the implementer's outcomes, plus three wording defects in the moved callers.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Replace the stale "carry the marker" wording in `### The dispositioned outcome` with the outcome form _(layer: plugin)_
2. [x] **Finding 2** — Quote `layer-implementer.cause` when an `already passing` outcome escalates on a row other than `G.4` _(layer: plugin)_
3. [x] **Finding 3** — Stop attaching "naming the latest findings file path" to a `layer-reviewer` blocker in both cores' stop conditions _(layer: plugin)_
4. [x] **Finding 1** — Let `layer-implementer` return `flags` on its `prohibited` and `already passing` outcomes _(layer: plugin)_

---

## Must Fix

### 1. `layer-implementer` cannot return `flags` on `prohibited` or `already passing`, so a mandatory untrusted-input report from a dispositioned layer has nowhere to go
→ [finding_1.md](feat_structured_outputs_unit_loop_code_review/finding_1.md)

---

## Should Fix

### 2. An `already passing` outcome that escalates on a row other than `G.4` has nothing for the escalation to quote
→ [finding_2.md](feat_structured_outputs_unit_loop_code_review/finding_2.md)

### 3. The stop-condition bullets name a findings file path for a `layer-reviewer` blocker, which writes no findings file
→ [finding_3.md](feat_structured_outputs_unit_loop_code_review/finding_3.md)

### 4. `### The dispositioned outcome` still says the implementer's return "carr[ies] the marker"
→ [finding_4.md](feat_structured_outputs_unit_loop_code_review/finding_4.md)

---

## Nice to Have

_None._

---

## Intentional divergences from the reference implementation (call-outs, not fixes)

_None. `phases.parity` is `false`._
