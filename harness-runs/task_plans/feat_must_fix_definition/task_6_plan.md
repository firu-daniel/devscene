### Task 6 — Make `review-plan-reviewer` check and regrade Must Fix entries

**Goal:** A code or skeptic review's Must Fix finding must carry a class and a failure sentence that hold up. `review-plan-reviewer` rejects one that does not, and its "reserved for" list is gone.

**Depends on:** Task 4, which creates `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` with the four classes, the failure sentence and the `**Class:**` / `**Failure:**` fields. Task 7 makes `branch-reviewer` and `skeptic-reviewer` write these fields in each Must Fix `finding_<N>.md`, directly after the site anchor. Task 11 adds them to `sample_code_review/finding_1.md`, the format this reviewer validates against.

### Targets

- `plugin/agents/review-plan-reviewer.md`

**Work:**

- [ ] Add the `## Read first` bullet: `` `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` — what each grade means. Grade every finding by it; never restate it. ``
- [ ] In `### False positives (Must Fix)`, replace the "Should Fix or Nice to Have items dressed up as Must Fix" bullet with: a finding under `## Must Fix` that does not meet `finding_grades.md` is a false positive against the review.
- [ ] Add `### Must Fix entries (Must Fix)` under `## What to check`. For each `finding_<N>.md` the index lists under `## Must Fix`, check that it carries `**Class:**` naming one of the four classes and `**Failure:**` completing the sentence, that the `<step>` exists in the diff or the review quotes it, and that the result can be checked. A missing field, or a class or sentence that does not hold, is a Must Fix against the review. Its `**Fix:**` tells the author to supply the missing field when the finding qualifies, and otherwise to move the index pointer to `## Should Fix`, keeping the finding file and its readiness entry.
- [ ] Add `### Must Fix triggers`: **Broken contract** for index structure, per-finding structure, correspondence and the round-suffix match; **Wrong build** for a finding file an implementer cannot act on, a forbidden test run, a false positive, a missed check, an unactionable gate and a parity citation that does not hold.
- [ ] Add `**Class:**` and `**Failure:**` to this agent's own findings template in `## Output contract`, before `**Fix:**`.

**Verification:**

- `grep -nE 'Must Fix is reserved for|dressed up as Must Fix' plugin/agents/review-plan-reviewer.md` prints nothing.
- Reading the new section shows a Must Fix finding file with no `**Failure:**` line produces `outcome: FAIL`, and the fix keeps the fix loop's readiness entry valid.
