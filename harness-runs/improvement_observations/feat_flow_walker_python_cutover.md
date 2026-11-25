# Script-driven planning — 2026-11-24T22:33:22Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #4 plan_writer (task-plan-writer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #8 architecture_review (architecture-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 998s 7.706520599999998; #2 architecture_review architecture-reviewer 1/3 FAIL 133s 2.1499965999999997; #3 plan_review task-plan-reviewer 1/3 FAIL 434s 5.601288000000002; #4 plan_writer task-plan-writer 1/3 returned 506s 3.032043400000001; #5 architecture_review architecture-reviewer 1/3 PASS 122s 2.107455; #6 plan_review task-plan-reviewer 1/3 FAIL 556s 7.9890738; #7 plan_writer task-plan-writer 1/3 returned 55s 0.5140176; #8 architecture_review architecture-reviewer 1/3 PASS 51s 1.1746864000000001; #9 plan_review task-plan-reviewer 1/3 PASS 80s 0.7479203999999999
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The plan needed 3 review rounds before converging
- **category:** optimization
- **evidence:** rounds 0, 1, 2 in harness-runs/task_plan_reviews/feat_flow_walker_python_cutover/ and harness-runs/architecture_reviews/feat_flow_walker_python_cutover/ (commits 1405ecc1, 11e70e1c, dbb28bde). Round 0: task-plan-reviewer `verdict: FAIL`, architecture-reviewer `verdict: FAIL`; round 1: task-plan-reviewer FAIL, architecture-reviewer PASS; round 2: both PASS. Net-new vs re-raised split not measurable: the round files carry findings under severity headings only, with no per-finding heading to match across rounds.
- **cost this run:** 9 planning node sessions (per the script-driven block above)

## A Phase A implementer park's answer has no stated reader once planning is resolved
- **category:** agent-contract
- **evidence:** harness-runs/clarifications/feat_flow_walker_python_cutover/question_1.md opens `Raised by: layer-implementer (Phase A, Task 7 …)`; the ledger had P0/P1/P3 `[x]` and P2 `[-]`. The implementation fork's `<escalate>` says a non-Phase-G answer "is fed back via the planner's resumability branch (Override 2(a))", which appends it to a task-plan-writer dispatch, while the core's `## What you must NOT do` says not to open a park's answer before Phase D. The orchestrator instead passed the question/answer paths on `context_notes:` lines to Phase A dispatches #1 (Task 7) and #5 (Task 11), recorded in harness-runs/dispatch_additions/feat_flow_walker_python_cutover.md.
- **cost this run:** routing of the answer improvised; one answer half (README difference record) carried to a later task's dispatch
- **hypothesis:** (guess) the Phase A/B/C park-answer reader is defined for the user-review flow's "On resume" paragraph but not for the task flow's implementation half

## A planning-round review committed an absolute machine path that failed gate 6a
- **category:** agent-contract
- **evidence:** harness-runs/architecture_reviews/feat_flow_walker_python_cutover/review_0.md line 23 (written by the round-0 architecture_review planning node, commit 1405ecc1) cited `unit_loop_core.md` by the plugin root's absolute path; Run gates round 1 failed gate 6a on it (harness-runs/test_run_logs/feat_flow_walker_python_cutover/task_round_1.log), fixed by test fix 4 (a372777e)
- **cost this run:** one test-fix finding and one implementer dispatch (#24); one of round 1's four failures

## Agents could not delete their own throwaway probe files
- **category:** tooling-gap
- **evidence:** question_1.md Q1 parked the run because `rm` of the implementer's probe cli/test/zz-resume-head-probe.test.mjs was refused for implementer and orchestrator alike; this session the branch-reviewer (dispatch #11) reported its cleanup of harness-runs/scratch/pyc_probe.py refused, and the Phase C implementer (dispatch #15) left harness-runs/scratch/pyc_mutation.mjs
- **cost this run:** one park awaiting a human deletion; two leftover scratch files (gitignored)

## Implementers reported no tree guard selected for changes the treeGuards globs cover
- **category:** agent-contract
- **evidence:** returns of dispatch #4 (Task 10: plugin/commands/*.md, plugin/docs/AUTONOMOUS_FLOW.md — covered by `plugin/**/*.md` and `**/*.md`), #6 (Task 12: docs/development.md — `**/*.md`), #8 (Task 14: docs/*.md — `**/*.md`), #13 (code-review Finding 4: docs/cli.md — `**/*.md`), #16 (code-review Finding 1, devscene-flow-host layer: devscene-flow-host/README.md — `**/*.md`), #21 (skeptic Finding 1: cli/templates/scripts/README.md — `cli/templates/scripts/**`, `**/*.md`) each stated no tree guard was selected; treeGuards in devscene.config.json
- **cost this run:** 6 units committed without their guard runs; Run gates round 2 passed, so no failure surfaced from it
