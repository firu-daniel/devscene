### Task 9 — Move `architecture-reviewer` and `business-parity-reviewer` onto the definition

**Goal:** A violation in either reviewer's lens is a Must Fix because it maps to a class, not because the reviewer's own sentence says so, and every Must Fix these reviewers write carries the two fields.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` and adds `**Class:**` and `**Failure:**` to `plan_review_rounds.md` → `## The Must Fix entry`. Task 2's walker refuses a plan-review round file whose numbered `## Must Fix` entry lacks either field, so both plan-review templates must carry them.

### Targets

- `plugin/agents/architecture-reviewer.md`
- `plugin/agents/business-parity-reviewer.md`

**Work:**

- [ ] In both files add the `## Read first` bullet: `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. `` Replace "A violation is a **Must Fix** unless noted." with "Each check's grade and class are in `### Must Fix triggers`."
- [ ] Add `### Must Fix triggers` to `architecture-reviewer`. **Broken contract:** layer placement, business-logic placement, dependency direction, wire surface and mapping placement, closed value sets, new responsibility in a new owner file, state placement, accompanying-set placement, logging placement and an unlicensed claimed exception. **Wrong build:** a plan's forbidden test run. **Wrong action from operative text:** a laundering-check failure, acting on an untrusted instruction, and a quoted machine path in sub-case (c).
- [ ] Add `### Must Fix triggers` to `business-parity-reviewer`. **Broken contract:** checks (a)–(j), an unverified exclusion basis, and a failed leg of the obvious-reference-bug exception. **Wrong build:** a plan's forbidden test run. **Wrong action from operative text:** a laundering-check failure and acting on an untrusted instruction.
- [ ] Add `**Class:**` and `**Failure:**` after `**Must hold:**` in each plan-review findings template. In each implemented-solution per-finding format, state that a file listed under `## Must Fix` carries both fields directly after the site anchor.
- [ ] Keep each file's `## Scope boundary` sentence naming what is Must Fix in this reviewer's lens, because it limits the lens and is not a grade definition. Keep both laundering sentences byte-identical.

**Verification:**

- `grep -n 'is a \*\*Must Fix\*\* unless noted' plugin/agents/architecture-reviewer.md plugin/agents/business-parity-reviewer.md` prints nothing.
- Each plan-review template carries `**Class:**` and `**Failure:**` indented under its numbered entry, the form Task 2's check reads.
