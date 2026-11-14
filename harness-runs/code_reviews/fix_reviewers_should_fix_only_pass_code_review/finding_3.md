### 3. The revision-note template's `Unrequested changes:` line still says "no finding asked for", while the README now says "no Must Fix"

**File:** `plugin/instructions/plan_review_rounds.md` (`## The writer's revision`, the revision-note template block) — "Unrequested changes: <every file changed that no finding asked for, or none>"

**Problem.** Task 2 made the revision note Must-Fix-only. Item 3 says to never name a Should Fix or Nice to Have in it, and the closing line now reads "One line per Must Fix." The template's last line still describes `Unrequested changes:` as every file changed "that no **finding** asked for".

Task 1 and Task 6 changed both README copies (`cli/templates/state-dir/plan_revisions/README.md` and `harness-runs/plan_revisions/README.md`) to describe that part of the note as *"every file it changed that no Must Fix asked for"*. So the template that owns the format and the README that describes it now give two different definitions.

A writer that changed a file for a Should Fix, which item 3 forbids, would leave that file out of `Unrequested changes:` under the template's wording, because "a finding asked for" it. Under the README's wording it would list the file. The converging reviewer that checks "every change the writer made" (`## Converging mode`) is the reader that loses the change when the template's wording is followed.

`Unrequested changes:` is quoted nowhere else in `plugin/`, `cli/` or `docs/`, so this line is its only owner.

**Fix.** In `plugin/instructions/plan_review_rounds.md` → `## The writer's revision`, replace the template line

`Unrequested changes: <every file changed that no finding asked for, or none>`

with

`Unrequested changes: <every file changed that no Must Fix asked for, or none>`

Change nothing else in the block. The edit is prose and needs no test run.
