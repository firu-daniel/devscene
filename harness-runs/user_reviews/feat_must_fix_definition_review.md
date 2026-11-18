Add a corpus test that keeps each reviewer agent's `### Must Fix triggers` table aligned with the checks that agent grades Must Fix.

Each of the 8 reviewer agents with a table (`architecture-reviewer`, `branch-reviewer`, `business-parity-reviewer`, `layer-reviewer`, `review-plan-reviewer`, `skeptic-reviewer`, `task-plan-reviewer`, `ui-tests-plan-reviewer`) now states its Must Fix triggers in two places: the checklist text marks a check Must Fix, and the table gives that check its class. Nothing keeps the two aligned. This has already drifted on this branch: plan review rounds 0 and 1 each caught a trigger missing from a table, and code-review finding 2 caught a laundering-related trigger with no row after implementation.

The test must fail when:
1. a check an agent's definition grades Must Fix is covered by no row of that agent's table, either its own row or a group row that names the section it sits in;
2. a table row names a class other than the four in `plugin/instructions/finding_grades.md`;
3. a table row names a check group or section heading that no longer exists in that agent's file;
4. an agent that cites `finding_grades.md` and grades checklist triggers Must Fix has no table.

Prose that mentions Must Fix without grading a check (the output format, return fields, round-file template, the verdict rule) must not count as a trigger. Show that the test catches real drift: removing a row, or adding an ungraded Must Fix check, must make it fail. If some phrasing cannot be told apart reliably, use an explicit, narrow exception list rather than a loose pattern, and keep the test's matching simple enough to maintain.
