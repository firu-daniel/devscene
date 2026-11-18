### 5. Move the upgrade refusal's run grading out of core

**Severity:** Should Fix

**Site:** `cli/src/core/runRegistry.ts` → `readActiveRuns` and `ActiveRuns`, quoted: `return pidNumber(pid) === undefined || pidIsAlive(pid);`

**Problem.** The module header states its rule as "the registry file's parsing and record walk live here once, and each caller keeps its own grading". `doctor` keeps its grading in `liveRunCount`. The upgrade refusal does not keep its own: `readActiveRuns` is that grading, it sits on the shared floor, and `cli/src/upgrade/preconditions.ts` is its only production caller. What counts as "cannot be proved idle" is a decision of the upgrade refusal.

**Rule source.**

- `.claude/context/cli.md` → `## Naming and file layout`: "a module lives in the area whose responsibility it serves".
- `.claude/context/conventions.md` → `## Shared code, and where it lives`: `cli/src/core/` is for what two `cli/src` areas need.
- `.claude/context/cli.md` → `## What "done" means here`: a change satisfies the rule its module header states, or amends the header.

This is graded Should Fix because the conventions say what belongs in `core/` without forbidding a single-caller module there, and the header names this function openly.

**Fix.**

1. Move `ActiveRuns` and `readActiveRuns` to `cli/src/upgrade/preconditions.ts`, exported so the suite can still reach them.
2. In `cli/src/core/runRegistry.ts`, export `pidNumber`, which the moved function needs. Remove the `nameList` import, and rewrite the header sentence that describes `readActiveRuns`.
3. In `cli/test/upgrade-inputs.test.mjs`, import `readActiveRuns` from `../dist/upgrade/preconditions.js`.
