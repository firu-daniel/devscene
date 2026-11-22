# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **Task 5 (`task_5_plan.md`), with Task 3 (`task_3_plan.md`): no task changes the existing case that Task 3's scoping of check 8's graph-wide clause breaks**
   Task 3 runs check 8's graph-wide clause (*"a dispatch node routing a fail verdict with no increment is a gate of exactly one round"*) only when `review_loops(graph)` is non-empty. The existing case `graphscene/tests/engine/test_static_check.py` → `test_gate_in_round_a_gate_in_zero_rounds_is_named` plants a graph with **no round at all**: `a` routes `done` and `rejected` to terminal `t`. It asserts exactly `[Violation("nodes.a", "gate-in-round: node 'a' routes a fail verdict with no increment and is a gate of 0 round nodes, not exactly one")]`. After Task 3 that graph declares no review loop, so `static_violations` returns `[]` and the case fails. Task 3 does not target the test file. It claims *"On every graph that loads today this task returns the identical list"*, which says nothing about this graph, because the graph does not load today. Task 5 owns the test file but forbids the edit.
   **Raised against:** task_5_plan.md: "Every existing case and `_NEGATIVES` stays unchanged."
   **Must hold:** The task that owns `graphscene/tests/engine/test_static_check.py` must change every existing case whose expected list moves under Task 3's scoping, and name each one. After the branch, the suite must pass with the existing cases' expectations matching the new scoping.
   **Class:** Wrong build
   **Failure:** If the implementer follows Task 5 as written and leaves `test_gate_in_round_a_gate_in_zero_rounds_is_named` unchanged, then the Phase G whole-suite run of `tests/engine/test_static_check.py` fails on that case: it gets `[]` where it expects the `nodes.a` gate-in-round violation.
   **Fix:** In `task_5_plan.md`, replace *"Every existing case … stays unchanged"* with a bullet that rewrites `test_gate_in_round_a_gate_in_zero_rounds_is_named`. Plant a review loop in its graph (for example `_base()` plus a node `z` routing `rejected` → `t` with no increment, which still yields `gate of 0 round nodes` for `z`). Add the no-round graph as its own case asserting `[]`. Keep every other existing case unchanged, and name this one exception. In `task_3_plan.md`, add the exact sentence *"One existing planted case changes: `test_gate_in_round_a_gate_in_zero_rounds_is_named`, whose graph declares no round; Task 5 rewrites it."* to `**Where this task stops.**`. Task 3 must still not edit the test file.

## Should Fix
1. **Scope register (`feat_graphscene_review_loop_pattern_story_plan.md`): the lessons-ledger procedure reaches a rule that has no row (disposition (i))**
   I re-walked the standing-artifact procedure over `harness-runs/lessons.md`. Its decision rule (*"a rule is reached when it names a flow graph"*) reaches one rule the register does not list: `## Agent prose` → *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space; when it is carried over from an old literal, keep the literal's words and drop its spacing."* That rule names a graph's routed values. The plan does comply: the new fixture's ids (`release_checks`, `lint`, `license`, `accepted`, `rejected`, `crashed`) are single tokens. So the missing row would be `no-change` with that reason. Add it. The command entry re-ran cleanly, and every site it reached (rows 1–7) is a row.

## Nice to Have
1. **Task 8 (`task_8_plan.md`), `ROADMAP.md` edit:** taking *"the review loop's rules on the engine"* out of **Left:** leaves *"the walker's port onto it"* with `it` pointing at nothing. Name the antecedent, for example *"the walker's port onto the engine"*.
2. **Task 6 (`task_6_plan.md`):** `Walker` takes a `PredicateHost` as well as the store. Name the file's existing `DictHost` (`graphscene/tests/facade/test_walking.py`) as the host for the new walk, so the implementer does not have to work it out.
