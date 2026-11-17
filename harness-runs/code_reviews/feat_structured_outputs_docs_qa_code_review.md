# Code Review: feat_structured_outputs_docs_qa

## Context

**Branch:** `feat_structured_outputs_docs_qa`
**Date:** 2026-11-17
**Reviewed:** the whole branch diff against `origin/dev`. The configured `defaultBranch` is `dev`, and this run copy has no local `dev` branch, so the review compared against its remote-tracking ref. The diff covers 25 files in three segments:

- **QA segment (Tasks 1–2):** `qa-tester`, the two mobile stubs, their three new schemas, `plugin/agents/README.txt`, the Phase E / Phase QA / supervised QA callers and the two semi-autonomous implement commands.
- **Docs segment (Tasks 3–4):** `docs-writer` and `docs-reviewer`, their two new schemas, the docs-phase and docs-catalog callers, and the `untrusted_input.md`, `agent_return_contract.md` and `improvement_observations_instructions.md` edits.
- **Closing segment (Tasks 5–6):** the every-agent rule in `cli/test/agent-return-schemas.test.mjs`, the decision record `docs/structured-agent-returns.md`, and `ROADMAP.md`.

18 run-artifact files excluded from the reviewed diff.

**Headline conclusions:**

- **Coverage.** `plugin/agents/` holds 22 definitions and `plugin/schemas/` holds 22 return schemas, one for each.
- **Tests.** The suite's new `checkSchemaCoverage` has a real-tree test and a bad-sample test. The one new export is a check function inside the suite and is called from that file, so it is not an unwired feature.
- **Old return literals.** A grep across `plugin/`, `cli/templates/` and `docs/` (research records excluded) found none left for the five agents: no `verdict:` lines, `error: blocked`, `doc_path:`, `targets: none` or `missed_docs:` remain in any caller. Every routing caller points at `agent_return_contract.md` → `## Reading a return`, names its own `error` route, and halts on `blocker` but never on `blocked`.
- **`general` layer (`ROADMAP.md`, `docs/structured-agent-returns.md`).** Checked against `.claude/context/conventions.md` → `## Documents of record` and the `A prose document under docs/` row of `## What accompanies a new unit of each kind`. The check is clean on three counts:
  - **Reader and ownership.** The decision record still states who reads it (`**Who reads this:**`, now "a maintainer changing an agent's return or adding an agent") and what it owns (`**What it owns.**`, unchanged by this branch).
  - **Deferrals.** No remaining deferral cites a roadmap number this branch renumbered or removed. The `#380` pointers are gone from every tracked file outside `harness-runs/`. The `ROADMAP.md` index renumbering (rows 19–51 become 18–50 after the `Structured agent outputs` row is dropped) changes only that file's priority column, and no document cites that column by number: a `git grep` for `Priority <n>` and for numbered `ROADMAP.md` citations outside `harness-runs/` and `examples/` returns nothing. The legend in `docs/development.md` → `## 6. The roadmap this tree defers to` uses its own numbering (items 3–35). This branch does not edit it, and the renumbering does not affect it.
  - **The `Done` row.** The `Structured agent outputs` row of `ROADMAP.md`, now `Done`, cites the test that delivers it (`cli/test/agent-return-schemas.test.mjs`) and the decision record (`docs/structured-agent-returns.md`).
- **Parity.** `phases.parity` is `false`, so no parity cross-check ran.
- **Pass 0.** The grep half was skipped because this definition's sweep list has no regexes filled in, which is a configuration gap. The caller-check half did run.
- **Two-pass mode.** The supplied `per_task_findings_root` does not exist, so Pass 2 had nothing to reconcile.
- **Planning leads.** The planning rounds' `## Incidental findings (not gating)` sections contain no leads.

The three findings below are what is left: one Should Fix about citation form and two wording leftovers.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — Drop the two line-form leftovers in `qa-tester.md` _(layer: plugin)_
2. [x] **Finding 3** — Un-nest the report-don't-substitute sentence in `plugin/agents/README.txt` _(layer: plugin)_
3. [x] **Finding 1** — Cite the three bare return-field reads as `<agent>.<field>` _(layer: plugin)_

---

## Must Fix

_None._

---

## Should Fix

### 1. Three return-field reads use a bare field name instead of the `<agent>.<field>` citation form
→ [finding_1.md](feat_structured_outputs_docs_qa_code_review/finding_1.md)

---

## Nice to Have

### 2. `qa-tester.md` keeps two phrases written for the old line-form return
→ [finding_2.md](feat_structured_outputs_docs_qa_code_review/finding_2.md)

### 3. The report-don't-substitute sentence in `plugin/agents/README.txt` nests two em-dash asides
→ [finding_3.md](feat_structured_outputs_docs_qa_code_review/finding_3.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

`phases.parity` is `false`, so there is no reference implementation and this section is empty.
