### Task 5 — Move `task-plan-reviewer` and its register gaps onto the definition

**Goal:** `task-plan-reviewer` grades by `finding_grades.md`, maps every Must Fix trigger to a class, and grades each verified scope-register gap by what the gap would cause.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` (the four class names, the failure sentence, `**Class:**` and `**Failure:**`, and `### Checklist triggers`) and adds both fields to `plan_review_rounds.md` → `## The Must Fix entry`.

### Targets

- `plugin/agents/task-plan-reviewer.md`

**Work:**

- [ ] Add one `## Read first` bullet: `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. ``
- [ ] Open `## What to check` with `### Must Fix triggers`, a table of check group or trigger to class, stating that a trigger named on its own row is excluded from any group row that would otherwise contain it, so each trigger has exactly one class. **Broken contract:** story-index structure, per-task-file structure, index↔file correspondence, every `### Architecture` bullet, `### Granularity & tags`, parity triggers, required-set items, work on application-level shared state that does not follow the owning layer's source-of-truth-and-mirror path, a repeated `<state_dir>/lessons.md` lesson, and a register that is absent when owed or out of position. **Wrong build:** a missing prompt requirement, the cross-task-interface bullet of `### Per-task-file structure` (an interface not restated on both sides, or two files claiming to create the same file), the **Tasks sequence bottom-up** bullet of `### Architecture` (a dependency on a later task, or a dependent ordered before its dependency), an unconsumed unit, a silent infrastructure assumption, an unrepresented lifecycle behaviour, a forbidden test run in each form `### Completeness` lists, and a register gap whose missed site must change for the work to function, including a finding that lists both kinds of gap. **Wrong behaviour:** a client-only or missing server-side gate. **Wrong action from operative text:** a laundering-check failure, a derivation command that cannot be executed, and a register gap whose only Must Fix sites are commands or steps the change makes fail. Keep the laundering sentence byte-identical.
- [ ] Regrade one trigger that maps to no class: index-level `### Sources of truth` / `### Targets` present becomes a Should Fix, because no reader acts on them. Leave every other trigger's grade unchanged.
- [ ] Rewrite the register dispositions so a verified gap is always reported and its grade comes from `finding_grades.md`, wherever the missed site lives. A gap that would lead to a wrong implementation or a wrong action, with a completed failure sentence, is a Must Fix: for example, an omitted site that must change for the feature to work, or a documented command the change makes fail. A missed site that only describes the project, where nothing goes wrong while it stays stale, is a Should Fix under `## Should Fix`. Disposition (i) and disposition (ii) each produce at most one Must Fix and one Should Fix per round, splitting a gap that covers both kinds and listing every site in the finding of its own grade. Keep "strictly wider" corrected derivation entries with the Must Fix when one exists, and otherwise with the Should Fix. The register's structure, derivation duty, closure test and converging variant do not change.
- [ ] Add `**Class:**` and `**Failure:**` to the `## Output contract` findings template, after `**Must hold:**`. Keep `## Should Fix` optional and state nothing new about how the writer treats it.

**Verification:**

- `grep -c 'finding_grades.md' plugin/agents/task-plan-reviewer.md` reports at least 1, and the `### Must Fix triggers` table names only the four class names from Task 4.
- Walking each line `grep -n 'Must Fix' plugin/agents/task-plan-reviewer.md` prints against the finished table shows every trigger still graded Must Fix has exactly one class, and the only regraded trigger is index-level `### Sources of truth` / `### Targets`.
- Reading the register bullet shows a stale descriptive site alone leaves the round at `verdict: PASS` with that site under `## Should Fix`, while a site whose omission would produce a wrong result or a failing documented command gives `verdict: FAIL`.
- `git diff -- plugin/agents/task-plan-reviewer.md` changes no return field.
