# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **Scope register misses a site its own procedure entry reaches** — story index (`feat_graphscene_run_mode_story_plan.md`), `## Scope register`.
   Disposition (i). I re-walked the procedure entry ("Derivation entry — sites inside `graphscene/README.md`"). Its traversal covers "the `## The layers` table rows and bullets", and its decision rule reaches any sentence that "states what the `engine` layer holds". That reaches one site that is not a row:
   - `graphscene/README.md` → `## The layers`, the bullet "**New work goes by what it is.** A check or a walk over the model, and its rounds, goes in `engine`."
   The run loop is a walk over the model, so the bullet stays true and its disposition would be `no-change`. No site that must change is missed, which is why this is not a Must Fix. The register's closure invariant still fails until the bullet is a row with its `no-change` reason.
   I re-ran the command entry verbatim. It printed exactly the four files rows 1 and 6–8 cover.

2. **Task 2 leaves the test file's header stating the rule it replaces** — `task_2_plan.md`.
   The module docstring of `graphscene/tests/engine/test_set_execution.py` opens "The rule this file exists to enforce: `execute_set` … launches each dispatch concurrently under the optional run timeout …". Task 2 changes that rule to a sliding window of `max_concurrent_dispatches`, adds the window's cases to this file and rewrites `set_execution.py`'s own docstring. It never updates this header. Once the task lands, the header will understate what the file enforces. This is a doc comment, so it is not a Must Fix (`finding_grades.md` → `## Never a Must Fix on its own`). Adding a `**Work:**` clause to restate the header's rule with the window would fix it.

## Nice to Have

1. **`## Context` carries a bulleted list** — story index. The sample's Context is prose paragraphs only. The "Settled here and stated once" bullets are clear and load-bearing, so this is a style point only.
