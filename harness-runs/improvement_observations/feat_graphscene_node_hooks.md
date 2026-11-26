# Script-driven planning — 2026-11-26T19:44:14Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 1450s 10.001178400000002; #2 architecture_review architecture-reviewer 1/3 FAIL 204s 2.486666200000001; #3 plan_review task-plan-reviewer 1/3 FAIL 481s 5.269194; #4 plan_writer task-plan-writer 1/3 returned 139s 1.0827422000000002; #5 architecture_review architecture-reviewer 1/3 FAIL 159s 2.1989639999999997; #6 plan_review task-plan-reviewer 1/3 FAIL 417s 4.6054829999999995; #7 plan_writer task-plan-writer 1/3 returned 77s 0.5079212; #8 architecture_review architecture-reviewer 1/3 PASS 65s 1.268459; #9 plan_review task-plan-reviewer 1/3 PASS 104s 0.8049627999999999
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** convergence churn on the plan unit — 3 distinct round indices (0, 1, 2) across `harness-runs/task_plan_reviews/feat_graphscene_node_hooks/` and `harness-runs/architecture_reviews/feat_graphscene_node_hooks/` (business-parity gate skipped, `phases.parity` false); rounds 0 and 1 `verdict: FAIL`, round 2 `verdict: PASS`. By finding title, round over round in each root: task-plan-reviewer round 0 → 6 titled findings; round 1 → 2 net-new, 4 re-raised; round 2 → 0 titled. architecture-reviewer round 0 → 3 titled findings; round 1 → 1 net-new, 2 re-raised (both Should Fix: the `commands/render.py` → `_block` variant-rule copies in Tasks 11/14, and the duplicated `ui_test_index` constant in Tasks 13/14); round 2 → 0 titled.
- **cost this run:** 2 extra plan-review rounds (6 node sessions beyond the first round, per the script-driven planning block above)
- **hypothesis:** the two architecture Should Fix items re-raised in round 1 were raised again, unfiled, by the Phase A2 architecture-reviewer's PASS return on the implemented branch — the plan converged with them still open.

## Commands refused by the permission layer during implementation
- **category:** tooling-gap
- **evidence:** orchestrator: a compound read-only `wc -l …; grep -n '^#' …` over the plugin instructions directory (main checkout) was refused in don't-ask mode, as was `grep -h -m1 '^### Task ' harness-runs/task_plans/feat_graphscene_node_hooks/task_{1..17}_plan.md` (brace expansion); both were redone with the Read tool. Sub-agent returns (layer-implementer): Task 1 — "The permission system refused a `python3` editing script"; Task 16 — "My first attempt to run all seven in one call was refused, so I ran them one at a time"; code-review Finding 3 — "A separate check that the edited file still parses as JSON was refused by the permission mode, so I did not run it".
- **cost this run:** 5 refused calls; one verification (JSON parse of `graphscene/src/graphscene/schemas/flow-graph.schema.json`) left to the Run gates phase

## A unit reported no tree guard selected where a `covers` glob matched its change
- **category:** agent-contract
- **evidence:** the layer-implementer for code-review Finding 3 (commit 6dd27609, edit to `graphscene/src/graphscene/schemas/flow-graph.schema.json`) returned "No tree guard was selected", while the Task 2 and Task 3 implementers on the same branch each ran `tests/test_layers.py` as the guard selected by `graphscene/src/graphscene/**`, and the B.2 review-plan-reviewer return stated that "Finding 3's edit matches `graphscene/src/graphscene/**`, which selects `tests/test_layers.py`".
- **cost this run:** one tree guard not run for that unit (the Run gates round 1 `pass` covered the tree afterwards)
