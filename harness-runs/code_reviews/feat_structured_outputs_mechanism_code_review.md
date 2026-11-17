# Code Review: feat_structured_outputs_mechanism

## Context

**Branch:** `feat_structured_outputs_mechanism`
**Date:** 2026-11-17
**Reviewed:** the whole branch diff against the default branch `dev`, read as `origin/dev...HEAD` because this run copy has no local `dev`. It covers 14 files:

- **Task 1:** the object-item branch of `PNL_REAP_JQ` → `vfail`, with its `planning-node-lib.test.mjs` case.
- **Task 2:** the dialect, nested-bullet and nested-citation checks in `cli/test/agent-return-schemas.test.mjs`, plus its extension to `cli/templates/scripts/**`.
- **Task 3:** the `verdict` verb's rewrite onto `PIS_JQ_VERDICT`, with its malformed-input matrix.
- **Task 4:** `agent_return_contract.md` → `## Reading a return` step 1, and the screen's pointer at it.
- **Task 5:** `prompt-injection-reviewer`'s schema file, its `### Return fields` and the `untrusted_input.md` row.
- **Task 6:** the three decisions and the measured `Agent` result in `docs/structured-agent-returns.md`.
- **Task 7:** the pointers in `docs/flow-graph-walker.md` and `docs/watcher.md`, and the eval set's counting.

17 run-artifact files excluded from the reviewed diff.

**Headline conclusions:**

- **Tests.** Every behaviour change carries its own case: the object-item `vfail` failures, the dialect and annotation bad samples, the script-citation sample, and the malformed matrix the story's `Top risks:` asks for. That matrix covers the retired forms, a bare object, prose, the trailer, the indentation, an extra key, an unknown id, an empty `findings` and a `blocker` object. This review ran no suite; whether the suite passes is the Run gates phase's to establish. `agent-return-schemas.test.mjs` already had a `treeGuards` entry for `cli/templates/scripts/**`.
- **Scope.** No caller of the agent still parses `verdict:` / `finding:` lines. The remaining `verdict: SAFE` / `verdict: UNSAFE` strings are the script's own stdout wire and dated records, as the story's scope register states. The self-adopted `scripts/` copies are left to the declared post-merge re-render.
- **Parity.** Off (`phases.parity` is `false`).
- **Findings.** One fail-open edge on the tripwire's passing path (Finding 1), and one vacuity gap in the new citation test (Finding 2).

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — Assert the script-citation check found a citation _(layer: cli)_
2. [x] **Finding 1** — Require the SAFE block's text to be the SAFE object, not only its parse _(layer: cli)_

---

## Must Fix

### 1. The verdict verb passes a return whose text carries an `UNSAFE` outcome, through a duplicate `outcome` key
→ [finding_1.md](feat_structured_outputs_mechanism_code_review/finding_1.md)

---

## Should Fix

### 2. The script-citation check passes when it finds no citation, so the screen's header can drop out of it silently
→ [finding_2.md](feat_structured_outputs_mechanism_code_review/finding_2.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation to diverge from, and this section carries no parity call-out.
