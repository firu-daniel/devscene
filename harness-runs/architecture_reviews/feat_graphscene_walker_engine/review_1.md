# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`task_7_plan.md`, `task_6_plan.md` and the story index's decision "The file store raises errors of its own": a malformed state file is reported as a builtin `ValueError`, not through `GraphError`.** Carried from round 0 and still open. `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` says the library "reports through return values and `GraphError` only". `## Errors and the loading order` scopes "a new rejecting stage is a new `Stage` member, never a second error type" to the graph-loading stages, and a state-file read is not one of them. That is why this stays a Should Fix: no failure sentence can be completed. Either route the codec's `<path>: <reason>` refusals through `GraphError` with a new `Stage` member and `Violation` values (Tasks 6, 7 and 9 together), or keep the builtin error and record the "`GraphError` only" sentence as a `stale-rule` entry in `corpus_staleness`, as story scope-register row 1 already does for "keeps no persisted or shared state". The lock's `TimeoutError` is an `OSError` subclass, and the existing rule that an `OSError` propagates (`graphscene/src/graphscene/adapters/json_file.py` → *"The rule:"*) already covers it.

2. **`task_1_plan.md` / `task_2_plan.md`: `graphscene/src/graphscene/model/__init__.py`'s docstring goes stale.** Carried from round 0 and still open. Its first line reads "the typed flow-graph model and the one error shape every stage reports in". After Tasks 1 and 2, `model` also holds the walk's actions, its state and the two Protocols. Task 5 updates `engine/__init__.py`'s first line and Task 7 updates `adapters/__init__.py`'s, but no task updates `model/__init__.py`'s. Add the same one-line edit to Task 1's or Task 2's Targets, leaving *"The rule:"* unchanged. This is a docstring, so it is never a Must Fix on its own (`finding_grades.md` → `## Never a Must Fix on its own`).
