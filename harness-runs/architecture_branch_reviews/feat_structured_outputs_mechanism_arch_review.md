# Architecture review — feat_structured_outputs_mechanism

## Context

Branch `feat_structured_outputs_mechanism`, reviewed 2026-11-17 against `origin/dev`. The configured base `dev` has no local ref in this checkout, so the diff was taken as `origin/dev...HEAD`. Reviewed in implemented-solution mode: 14 changed files in three segments.

- **`cli`:** `cli/templates/scripts/lib/planning-node-lib.sh`, `cli/templates/scripts/prompt-injection-screen.sh` and three suites under `cli/test/`.
- **`plugin`:** `plugin/agents/prompt-injection-reviewer.md`, three instruction modules, and the new `plugin/schemas/prompt-injection-reviewer.return.json`.
- **`general`:** `docs/structured-agent-returns.md`, `docs/flow-graph-walker.md`, `docs/watcher.md` and `evals/prompt-injection-reviewer/README.md`.

15 run-artifact files excluded from the reviewed diff.

**Headline.** The layering holds:

- The new schema sits in `plugin/schemas/`, outside the component-discovery directory.
- The script caller keeps its own check and names `plugin/` only in header prose, so neither shipped half reaches into the other at run time.
- The decisions and the measured `Agent` result went to `docs/`.
- Each changed unit lands with its suite.

One single-owner breach remains. `plugin/instructions/prompt_injection_screen.md` paraphrases `agent_return_contract.md` → `## Reading a return` step 1 instead of only pointing at it.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Point at Reading a return step 1 without paraphrasing it in the screen's step 3 _(layer: plugin)_

## Must Fix

### 1. Point at Reading a return step 1 without paraphrasing it in the screen's step 3
→ [finding_1.md](feat_structured_outputs_mechanism_arch_review/finding_1.md)
