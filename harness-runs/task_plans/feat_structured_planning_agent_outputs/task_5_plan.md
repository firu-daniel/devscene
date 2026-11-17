### Task 5 — Give `architecture-reviewer` and `business-parity-reviewer` a `## Return schema` covering every mode

**Goal:** Make the two branch-and-plan reviewers return one JSON object each, declared once in a `## Return schema` section that covers **every** mode and sub-case they run in — plan-review mode at insertion points 1, 3 and (architecture only) 4, implemented-solution mode at insertion point 2, and the business-parity disabled-phase no-op — because an agent has one return contract.

**Depends on:** Task 1 (the dialect, the canonical sentence in `plugin/instructions/agent_return_contract.md` → `## The return block`, the `### Return fields` rule) and Task 4, which restated `plugin/instructions/plan_review_rounds.md` → `## The round file`'s return lines by outcome and field — both agents' plan-review `PASS` paragraphs keep pointing there.

**The returns this task declares** (the story index `## Context` field table — Tasks 6, 8, 9, 10 and 11 read exactly these names):

- Both agents: `outcome` `PASS` with optional `findings_file` (string) — present in plan-review sub-cases (a) and (b), where a round file is always written, and absent in sub-case (c) and implemented-solution mode, where a clean or advisory `PASS` returns no path; `outcome` `FAIL` with required `findings_file` (the flat `review_{iteration}.md` in plan-review mode, the **index** in implemented-solution mode) and `must_fix_count` (integer, `minimum` 1); `outcome` `blocker` with required `blocker` (string).
- `business-parity-reviewer` only: its `PASS` variant also declares optional `reason` (string), carried only by the disabled-phase no-op to name the disabled phase.

**Where this task stops.** Every caller of these returns is a later task: the planning gates (Task 6), Phases A1.5, A2 and G.2 and the Done summary (Task 8), the user-review fix-plan gates (Task 9), the driver (Tasks 10–11). The findings files, review indexes, per-finding files and the `## Findings-folder / index-path convention` section are unchanged; so is each agent's `## Unsolicited dispatch guidance` block, which `plugin/instructions/dispatch_discipline_instructions.md` owns byte-for-byte.

### Targets

- `plugin/agents/architecture-reviewer.md`
- `plugin/agents/business-parity-reviewer.md`

**Work:**

- [ ] `architecture-reviewer.md` → `## Output contract`: keep every sub-heading's **file** obligations (`### Plan-review mode (a) and (b) PASS`, `### Clean review (both modes)`, `### Sub-case (c) advisory PASS`, `### Plan-review mode FAIL (insertion points 1, 3 and 4)`, `### Implemented-solution mode FAIL (insertion point 2)`) and replace each fenced return block with the outcome and fields that case returns. Replace `### Return lines (both modes on FAIL)` with the canonical sentence and a `### Return fields` subsection — `outcome`, `findings_file`, `must_fix_count`, `blocker` — saying which case carries `findings_file` and what it points at. Keep the sentence on the optional `## Unsolicited dispatch guidance` placement. Add `## Return schema` directly after `## Output contract`, before `## Findings-folder / index-path convention`.
- [ ] `architecture-reviewer.md`, the body: `## Invocation contract` → **Your return is parsed, not read.** (the caller routes on the `outcome` value, exactly one of the schema's, and passes `findings_file` in sub-cases (a) and (b) on both outcomes); `## Read first` → **A cited path you cannot read is a finding, not a fallback.** (the `blocker` outcome in place of any verdict).
- [ ] `business-parity-reviewer.md`: the same `## Output contract` rewrite over its own sub-headings (`### Plan-review mode PASS`, `### Clean review (both modes)`, `### Plan-review mode FAIL (insertion points 1 and 3)`, `### Implemented-solution mode FAIL (insertion point 2)`, `### Return lines (both modes on FAIL)`), with `### Return fields` — `outcome`, `findings_file`, `must_fix_count`, `reason`, `blocker`. Add `## Return schema` after `## Output contract`, before `## Findings-folder / index-path convention`. Rewrite the disabled-phase paragraph under the opening (a dispatch with the phase off returns an `outcome` of `PASS` with `reason` naming the disabled phase, writes no file, reads nothing), `## Invocation contract` → **Your return is parsed, not read.**, and `## Read first`'s unreadable-path rule.
- [ ] Hold both definitions' word budgets (`.claude/context/plugin.md` → `## Writing agent prose`): the schema replaces the retired return blocks; no check, scope boundary or mode rule is cut.

**Verification:**

- In both files, `git grep -nE '^verdict: |^findings_file: |^must_fix_count: ' -- plugin/agents/architecture-reviewer.md plugin/agents/business-parity-reviewer.md` prints only the `verdict:` line inside each flat findings-file format block, and no return block.
- Walk each mode and sub-case in `## Invocation contract` and confirm `## Output contract` names the outcome and the fields it returns, and that the schema admits exactly that object: sub-case (a)/(b) `PASS` with `findings_file`; sub-case (c) clean and advisory `PASS` and implemented-solution `PASS` without it; every `FAIL` with both fields; the disabled-phase `PASS` with `reason` (parity only).
- Every `## Return schema` property has exactly one `### Return fields` bullet and the reverse; the canonical sentence is byte-identical to Task 1's; each schema matches its rows of the story index `## Context` field table.
- `git diff` shows no hunk inside either file's `## Unsolicited dispatch guidance` section.
