# Code review — `feat_structured_outputs_setup`

**Context.** Branch `feat_structured_outputs_setup`, reviewed 2026-11-17 against `dev`. This run copy has no local `dev` ref, so the diff base was `origin/dev`, whose merge base with `HEAD` is `3cf3787a`. Reviewed: the whole branch diff, 8 files, +336 / −67. Those files are the two new schemas `plugin/schemas/conventions-reviewer.return.json` and `plugin/schemas/conventions-writer.return.json`; the `## Output contract` rewrites in `plugin/agents/conventions-reviewer.md` and `plugin/agents/conventions-writer.md`; the reader moves in `plugin/commands/analyze.md`; the roster line in `plugin/instructions/agent_return_contract.md`; and the decision-record and design-doc updates in `docs/structured-agent-returns.md` and `docs/analyze.md`. 15 run-artifact files excluded from the reviewed diff.

Headline conclusions:
- The mechanism is adopted as the decision record states. Each agent has a closed-dialect schema, a `### Return fields` subsection and the canonical return-block sentence verbatim. `analyze.md` points at `agent_return_contract.md` and is listed in its `## Who may cite this`. No fallback to the old `key: value` form remains in any caller.
- The literal `Reviewer finding not applied — ` is unchanged in all three files that carry it: 3 / 1 / 2 occurrences in the writer / reviewer / command, identical before and after the branch.
- `cli/test/agent-return-schemas.test.mjs` discovers both new schemas by directory scan. No suite change was needed, and no tree-reading test was added, so no `treeGuards` registration is owed.
- The tests were not run by this review: the suite runs at Phase G.
- `phases.parity` is `false`, so no parity cross-check applies.
- Pass 2 was a no-op: the supplied `per_task_findings_root` does not exist.
- The branch carries one Must Fix: a shipped schema description names the old field the rename removed. Three Should Fix and two Nice to Have items are left behind by the prose-to-object move.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Drop the old `action_taken` name from the writer schema's outcome descriptions _(layer: plugin)_
2. [ ] **Finding 2** — Treat an empty `conventions-reviewer.findings` as none in `analyze.md` (4c) _(layer: plugin)_
3. [ ] **Finding 3** — Describe a shared-document divergence as an item with three parts, not "one line" _(layer: plugin)_
4. [ ] **Finding 5** — Reword the writer's corpus-`findings` lead-in, which still says "the line itself" _(layer: plugin)_
5. [ ] **Finding 6** — Align the writer's return-value sentence with the return-block contract _(layer: plugin)_
6. [ ] **Finding 4** — Re-spell Gate 8's corpus-review `findings:` references as `conventions-reviewer.findings` _(layer: general)_

## Must Fix

### 1. Drop the old `action_taken` name from the writer schema's outcome descriptions
→ [finding_1.md](feat_structured_outputs_setup_code_review/finding_1.md)

## Should Fix

### 2. Treat an empty `conventions-reviewer.findings` as none in `analyze.md` (4c)
→ [finding_2.md](feat_structured_outputs_setup_code_review/finding_2.md)

### 3. Describe a shared-document divergence as an item with three parts, not "one line"
→ [finding_3.md](feat_structured_outputs_setup_code_review/finding_3.md)

### 4. Re-spell Gate 8's corpus-review `findings:` references as `conventions-reviewer.findings`
→ [finding_4.md](feat_structured_outputs_setup_code_review/finding_4.md)

## Nice to Have

### 5. Reword the writer's corpus-`findings` lead-in, which still says "the line itself"
→ [finding_5.md](feat_structured_outputs_setup_code_review/finding_5.md)

### 6. Align the writer's return-value sentence with the return-block contract
→ [finding_6.md](feat_structured_outputs_setup_code_review/finding_6.md)

## Call-outs — intentional divergences to confirm

None. `phases.parity` is `false`, so there is no reference implementation to diverge from.
