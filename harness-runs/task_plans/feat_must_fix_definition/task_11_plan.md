### Task 11 — Update the samples, dispatch discipline and the flow map

**Goal:** The format fixtures show the new fields, dispatch discipline points at the grades file instead of an agent-held rubric, and the flow map lists the new canonical file.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` and defines `**Class:**` and `**Failure:**`.

### Targets

- `plugin/samples/sample_code_review/finding_1.md`
- `plugin/samples/sample_user_review_fix_plan/finding_2.md`
- `plugin/instructions/dispatch_discipline_instructions.md`
- `plugin/docs/AUTONOMOUS_FLOW.md`

**Work:**

- [ ] In `sample_code_review/finding_1.md`, add directly after the `**File:**` line: `**Class:** Wrong behaviour` and `**Failure:** If a user with more stored searches than \`limit\` opens the search surface, then \`SearchPanel\` omits the search they just ran.`
- [ ] In `sample_user_review_fix_plan/finding_2.md`, add the same two fields directly after its site anchor, or after `**Review comments:**` if present. Use the class its described defect meets and a failure sentence built from that file's own description. Keep every title, number and path, so the fixture set stays coherent.
- [ ] In `dispatch_discipline_instructions.md` → **Case 2**, replace both uses of the agent-held rubric wording. The correct move becomes a bare pointer to `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md`, and a restated or adjusted threshold stays barred.
- [ ] Add a row to the canonical file table in `AUTONOMOUS_FLOW.md`, beside the agent-return row: `| What Must Fix, Should Fix and Nice to Have mean (canonical; pointed at by each grading agent) | \`${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md\` |`.

**Verification:**

- `grep -nE 'severity rubric|[Tt]he rubric' plugin/instructions/dispatch_discipline_instructions.md` prints nothing.
- Both sample Must Fix findings carry both fields, and their index titles are unchanged.
