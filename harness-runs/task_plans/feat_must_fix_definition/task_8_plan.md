### Task 8 — Move `layer-reviewer` and `ui-tests-plan-reviewer` onto the definition

**Goal:** The per-unit reviewer and the UI-test plan reviewer grade by `finding_grades.md`, map their triggers to classes, and write the two fields on every Must Fix entry.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` with the four classes, `**Class:**`, `**Failure:**` and `### Checklist triggers`.

### Targets

- `plugin/agents/layer-reviewer.md`
- `plugin/agents/ui-tests-plan-reviewer.md`

**Work:**

- [ ] In `layer-reviewer`, add to `## Read first`: "Read `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md`: it says what each grade means. Grade every finding by it; never restate it." Delete the "Grade every finding by consequence" block. Rewrite the "not downgradable" paragraph to point at `### Must Fix triggers` and `finding_grades.md` → `### Checklist triggers`, keeping the size ladder's own grades. In "Prose volume" replace "the ladder above gives it" with "`finding_grades.md` gives it", using the same wording as `branch-reviewer` and `skeptic-reviewer`.
- [ ] Add `### Must Fix triggers` to `layer-reviewer`. **Broken contract:** parity triggers, hard conventions violations, architecture triggers, missing or off-idiom tests, an unregistered tree-reading test, required-set items, a file over the second size threshold, a trigger the conventions document enumerates, workflow-coherence items, a script's `cd` against orchestrator rules, an inlined restatement and a sample off its split shape. **Wrong behaviour:** a script silently masking failures and a hardcoded absolute path. **Wrong action from operative text:** a command-file description that disagrees with the instruction it chains to.
- [ ] Add `**Class:**` and `**Failure:**` before `**Fix:**` in `layer-reviewer`'s `## Must Fix` template only.
- [ ] In `ui-tests-plan-reviewer`, add the `## Read first` bullet `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. ``, delete the "Grade every finding by consequence" block, and rewrite the "not downgradable" paragraph as above, keeping its sentence that a clean `PASS` is a correct outcome. Add `### Must Fix triggers`. **Broken contract:** index structure, per-test-file structure and index↔per-test correspondence. **Wrong build:** test-attribute parity, asserted values, capability correctness, backend-name parity, `**Depends on:**` ordering and a coverage gap. **Wrong action from operative text:** a laundering-check failure.
- [ ] Add `**Class:**` and `**Failure:**` before `**Fix:**` in `ui-tests-plan-reviewer`'s `## Must Fix` template. Do not add a scripted-check claim: `ui_review` is not a round gate.

**Verification:**

- `grep -nE 'Grade every finding by consequence|would do the wrong thing|[Tt]he rubric|ladder above' plugin/agents/layer-reviewer.md plugin/agents/ui-tests-plan-reviewer.md` prints nothing.
- Both templates show the two fields, and the laundering sentence in `ui-tests-plan-reviewer` is byte-identical to before.

**Deviations from plan:**

- Both agents also name `finding_grades.md` in their unreadable-input stop, as `branch-reviewer`, `skeptic-reviewer` and `task-plan-reviewer` do; without it a new required input has no stated failure route.
- `layer-reviewer`'s **Project-convention compliance** group shares the hard-conventions row: it is the catch-all layer's form of the same trigger, and the plan's list otherwise leaves it with no class.
- `layer-reviewer`'s Should Fix and Nice to Have template lines now exclude the two fields, because their `<same shape, optional>` would otherwise have extended them past `## Must Fix`. Its `## Process` severity sentence now names `finding_grades.md` beside `## Checklist`.
- `**Class:**` uses the `branch-reviewer` / `skeptic-reviewer` rule (a row's class where a row applies) rather than the row-only wording, because these agents can raise a Must Fix under no row.
