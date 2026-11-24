# Script-driven planning — 2026-11-23T19:14:38Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 732s 4.6800408000000004; #2 architecture_review architecture-reviewer 1/3 FAIL 106s 1.6955102; #3 plan_review task-plan-reviewer 1/3 FAIL 332s 3.796982; #4 plan_writer task-plan-writer 1/3 returned 91s 0.7181429999999999; #5 architecture_review architecture-reviewer 1/3 PASS 100s 1.2240498; #6 plan_review task-plan-reviewer 1/3 FAIL 231s 3.551578; #7 plan_writer task-plan-writer 1/3 returned 29s 0.2918774; #8 architecture_review architecture-reviewer 1/3 PASS 40s 0.5635816; #9 plan_review task-plan-reviewer 1/3 PASS 50s 0.5809682
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The plan needed 3 review rounds
- **category:** optimization
- **evidence:** convergence churn — unit: the plan; round indices 0, 1, 2 across `harness-runs/task_plan_reviews/feat_flow_host_round_files/` and `harness-runs/architecture_reviews/feat_flow_host_round_files/` (no business-parity folder; parity off). Rounds 0 and 1 carry `verdict: FAIL` in `task_plan_reviews/…/review_0.md`, `review_1.md` and `architecture_reviews/…/review_0.md`; round 2 PASS in both. Per root, by finding title: task-plan-reviewer round 1 = 3 net-new, 4 re-raised from round 0 (Task 1/4 no consumer, Task 3 non-UTF-8, Task 8 case (12), Task 6 `entry` name); round 2 = 1 net-new, 0 re-raised. architecture-reviewer round 1 = 3 net-new, 0 re-raised; round 2 = no findings.
- **cost this run:** 9 planning node sessions (per the script-driven block above) for one plan unit

## Two plan gates raised the same finding in the same round, twice
- **category:** optimization
- **evidence:** reviewer overlap — unit: the plan. Round 0: `task_plan_reviews/feat_flow_host_round_files/review_0.md` Must Fix 2 and `architecture_reviews/feat_flow_host_round_files/review_0.md` Must Fix 1 both title `task_4_plan.md` retyping `ROUND_PLACEHOLDER` in `host/paths.py`. Round 1: `task_plan_reviews/…/review_1.md` Must Fix 1 and `architecture_reviews/…/review_1.md` Should Fix 2 both title `task_9_plan.md` naming one departure where Task 7 writes two `TODO: @claude` markers.
- **cost this run:** 2 duplicated findings across 2 rounds

## Compound or brace-expanded shell commands were refused in the unattended mode
- **category:** tooling-gap
- **evidence:** orchestrator: `cd plugin/instructions (main checkout); wc -l …; grep -n …` refused ("running in don't ask mode"); `grep -h -m1 '^### Task' harness-runs/task_plans/feat_flow_host_round_files/task_{1,2,…,10}_plan.md` refused, re-issued with ten literal paths and allowed. Sub-agent returns: Task 2 layer-implementer "My first attempt chained the three test runs into one command, and it was refused"; Task 10 layer-implementer "a combined command was refused".
- **cost this run:** 4 refused tool calls, each re-issued in a simpler form
- **hypothesis:** (guess) brace expansion and `;`-chained commands fall outside the safe-compound allow.

## Tree-guard selection for Markdown edits differed between units
- **category:** agent-contract
- **evidence:** `devscene.config.json` `treeGuards` maps `test/no-container-home-paths.test.mjs` to `**/*.md`. The Task 7, Task 9 (`devscene-flow-host/README.md`) and Task 10 (`ROADMAP.md`, `docs/development.md`) layer-implementer returns ran it; the Phase C Item 1 return (`devscene-flow-host/README.md`, code-review Finding 2) said "none selected, because the change touches nothing under `src/` or `pyproject.toml`", and the Item 2 return (`ROADMAP.md`, Finding 1) said "none selected, since the change touches a document only".
- **cost this run:** 2 unit commits (89e0f55c, 6e559e3e) landed Markdown edits without the guard `## The test-run rule` point 7 selects; Phase G round 1 passed afterwards
