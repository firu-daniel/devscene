# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_2.md`: the `NOT_A_GRADE` list is not complete, so the new corpus test fails on its first run** — outside this reviewer's layering lens, so non-blocking.
   `finding_2.md` calls its two lists "the complete lists for the corpus once Finding 1 has landed", and its graded-line scan and `uncovered` violation apply to every file under `plugin/agents/`, with or without a table. `plugin/agents/task-plan-writer.md`, in its **Authorization:** bullet, says "a client-only gate is a Must Fix at review." That text matches the `GRADE` alternative `is a Must Fix`. No `NOT_A_GRADE` or `OWN_ROWS` entry names this agent's line, and the agent has no table, so case 1 ("The corpus is clean") reports `task-plan-writer: uncovered`.
   The finding's fallback ("Add an entry only when a row really covers it or it really grades nothing") lets the `cli` unit recover inside its own file, because the line describes a reviewer's grade and grades nothing itself. No plugin edit is needed.
   **Fix:** add `['task-plan-writer', 'a client-only gate is a Must Fix at review']` to `NOT_A_GRADE` in `finding_2.md`.
