### Task 1 — State the advisory-PASS file and the Must-Fix-only revision note in the three adopter run-artifact README templates

**Goal:** Make the three adopter README templates under `cli/templates/state-dir/` that describe a plan-review folder or the revision note true under this branch's rules. A plan review with no Must Fix is a `PASS`. A passing review that raised a Should Fix or Nice to Have still writes its file, as a record for a human that no loop reads. A review with no finding at all writes nothing. A writer's revision note names Must Fix items only.

**Where this layer stops.** This task edits only the templates an adopter receives. This repository's own live copies under `harness-runs/` are **Task 6's**: Task 6 makes them byte-identical to the three files this task leaves behind, so write each template as the final text. There is no live copy of `ui_test_plan_reviews/README.md`, because `phases.qa` is `false` here. The agent behaviour these READMEs describe is delivered by the plugin tasks: Task 2 (`plan_review_rounds.md`), Task 4 (`architecture-reviewer` sub-case (c)) and Task 5 (`ui-tests-plan-reviewer`). This task restates none of their contract text. It describes only what lands in the folder and who reads it.

### Targets

- `cli/templates/state-dir/test_fix_plan_reviews/README.md`
- `cli/templates/state-dir/ui_test_plan_reviews/README.md`
- `cli/templates/state-dir/plan_revisions/README.md`

**Work:**

- [ ] `test_fix_plan_reviews/README.md`. The opening line "per failed plan review" and the third paragraph's "Files appear one per failed review" become one file per review that raised a finding.
  - The second paragraph's "only when it has findings to write, so a plan approved on the first pass leaves no folder behind" becomes true for a pass **with no finding at all**.
  - Add, once, that a file with no `## Must Fix` section is a passing review: its Should Fix / Nice to Have items are a record for a human, and the test fix-plan writer is not re-dispatched with it.
  - Keep the sentence that the writer "applies the Must Fix items".
- [ ] `ui_test_plan_reviews/README.md`.
  - The third paragraph's "A file appears only for a failed gate: a PASS touches no disk" becomes this: a file appears for every review that raised a finding; a passing one carries only Should Fix / Nice to Have, a record no loop reads; and a PASS with no finding touches no disk.
  - The fourth paragraph's "a plan that passed on the first gate" becomes a plan that passed on the first gate with no finding.
  - The second paragraph's reader sentence stays, because the writer is re-dispatched only on a failed gate.
- [ ] `plan_revisions/README.md`. "per finding of the round" becomes per **Must Fix** of the round. A Should Fix or Nice to Have is never named in a note and never recorded under `## Rejected findings`; say so in no more words than the change needs.
- [ ] Edit no other README under `cli/templates/state-dir/`. In particular, `test_fix_point_reviews/README.md`'s "per failed unit review" describes a `layer-reviewer` point review, which is out of scope (story index `## Scope register`, row 54).

**Verification:**

- `git grep -nE "per failed plan review|one per failed review|PASS touches no disk|per finding of the round" -- cli/templates/state-dir` prints no line.
- `git grep -nE "per failed" -- cli/templates/state-dir` prints only the `test_fix_point_reviews/README.md` line. Its output must be a subset of the story index's `## Scope register` rows.
- Read each of the three templates end to end. The rule is that no sentence may still imply a passing review writes nothing, or that a writer acts on a Should Fix. The `<state_dir>` and `${CLAUDE_PLUGIN_ROOT}` placeholders must be untouched, and no adopter value may appear as a literal.
