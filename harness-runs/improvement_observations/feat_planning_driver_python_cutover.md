# Script-driven planning — 2026-11-27T08:25:31Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 3 denial(s)
- **cost this run:** 3 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 3 denial(s)
- **cost this run:** 3 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #4 plan_writer (task-plan-writer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #9 plan_review (task-plan-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #10 plan_writer (task-plan-writer), round 3: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #11 architecture_review (architecture-reviewer), round 3: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 1022s 8.752796000000004; #2 architecture_review architecture-reviewer 1/3 FAIL 200s 2.6552548000000002; #3 plan_review task-plan-reviewer 1/3 FAIL 249s 3.4886142000000007; #4 plan_writer task-plan-writer 1/3 returned 357s 2.4934704; #5 architecture_review architecture-reviewer 1/3 PASS 179s 2.7020375999999997; #6 plan_review task-plan-reviewer 1/3 FAIL 404s 5.7442302000000005; #7 plan_writer task-plan-writer 1/3 returned 71s 0.5570168000000001; #9 plan_review task-plan-reviewer 1/3 PASS 64s 0.7980353999999998; #8 architecture_review architecture-reviewer 1/3 FAIL 72s 1.0155406; #10 plan_writer task-plan-writer 1/3 returned 42s 0.3487338; #11 architecture_review architecture-reviewer 1/3 PASS 40s 0.8111628000000002; #12 plan_review task-plan-reviewer 1/3 PASS 59s 0.6596788
- **cost this run:** 12 node session(s)

## Corpus staleness the script-driven planning dropped: three stale-rule entries
- **category:** tooling-gap
- **evidence:** stale-rule `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet ("Every caller launches it through `flow-walker.sh`") — the watcher now launches `devscene-planning-driver` through `hr_flow_host_exec`; owes a restatement naming `hr_flow_host_exec` as the one launch route for `flow-walker.sh` and the watcher alike. stale-rule `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` ("every caller launches it through `flow-walker.sh`'s hand-off") — same cause, same restatement. stale-rule `.claude/context/conventions.md` → `## Commit-message policy` ("the planning driver reads the same table (`cli/templates/scripts/lib/planning-record-lib.sh` → `prl_artifact_commit`)") — that library is deleted; owes a restatement naming `devscene-flow-host/src/devscene_flow_host/host/commit_points.py` → `commit_artifact`, through `commit-on-branch.sh --artifact`.
- **cost this run:** three conventions sentences left stale with no other record; each owes a supervised `/devscene:analyze` re-run or a hand edit

# Task run (Phase D)

## The plan needed 4 review rounds before every gate passed
- **category:** optimization
- **evidence:** convergence churn on the plan unit: round files `review_0.md`–`review_3.md` exist in both `harness-runs/task_plan_reviews/feat_planning_driver_python_cutover/` and `harness-runs/architecture_reviews/feat_planning_driver_python_cutover/` (4 distinct round indices). `verdict: FAIL` lines: round 0 (plan-review, architecture), round 1 (plan-review), round 2 (architecture); round 3 all PASS. The net-new vs re-raised split could not be measured: the round files carry no per-finding headings (only `## Must Fix` / `## Should Fix` / `## Nice to Have`), and the Phase-D exception reads headings only.
- **cost this run:** 12 planning node sessions across 4 rounds (the driver's session table above)

## Implementers could not run `bash -n` or `bash -c` in the run copy, and one worked around the refusal
- **category:** tooling-gap
- **evidence:** Task 1's `layer-implementer` return: "Running `bash -n` on each file directly was refused; the type check's shell-parse step covers it." Task 2's return: "`bash -n`: refused, not run", and "a direct `bash -c` check of bash 3.2 array slicing was refused. I then ran the same check as a `.py` probe through `scripts/scratch-run.sh`", disclosed in `harness-runs/task_plans/feat_planning_driver_python_cutover/task_2_plan.md`; its probe file `harness-runs/scratch/slice_probe.py` was left behind because `rm` was refused.
- **cost this run:** shell syntax of the two edited watcher scripts was verified only through `bash scripts/typecheck.sh`'s parse step; one refused check was re-run by another route
- **hypothesis:** a guess — the run copy's profile allows no direct `bash -n <file>` form for shell scripts the unit edits

## Implementers piped targeted test and tree-guard output through `tail` despite the foreground rule
- **category:** agent-contract
- **evidence:** Task 2's return: "Two earlier runs were piped through `tail`; the reported pass is the unpiped rerun." Task 4's return: "My first run of the guards piped the output through `tail`, which the foreground rule does not allow." Task 25's return: the two selected tree guards were run "as one command and piped the output through `tail` … so I'm relying on the printed counts … rather than the exit status", with no unpiped rerun. Rule: `plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 6.
- **cost this run:** Task 25's tree-guard result rests on piped counts rather than an exit status; Tasks 2 and 4 each spent a rerun

# User-review fix round 1 — live node output, undelivered observation, PD_BACKOFF_SECS, tree guards, held-session log check

## The single-file Python test command was refused in some unit sessions and ran in others
- **category:** tooling-gap
- **evidence:** refused with "Claude Code is running in don't ask mode": dispatch #3 (`layer-implementer`, Finding 5, `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_driver_walk.py`), #4 (`layer-reviewer`, Finding 5, the same command with a `::` test selector), #8 (`layer-reviewer`, Finding 2 graphscene layer, its test run), #10 (`layer-reviewer`, Finding 2 devscene-flow-host layer, three test files) and #18 (`layer-reviewer`, test-fix Finding 1, its shell commands). The same `bash scripts/python-service.sh --package … test <file>` form ran and passed in #5, #6, #7, #9, #11, #12 and #13. The `test-fix-plan-writer` (#15) also reported `printenv HOME` refused.
- **cost this run:** Finding 5's new assertion was committed with no test run before Run gates; three reviews (#8, #10, #18) passed on reading alone
- **hypothesis:** a guess — the refusal tracks something per session rather than the command string

## The fix-plan writer put a home-directory path into the fix-plan index, which failed Run gates round 1
- **category:** agent-contract
- **evidence:** `harness-runs/test_run_logs/feat_planning_driver_python_cutover/review_1_round_1.log` failed only gate `6a no machine paths` (30 passed, 1 failed). The hit was the `## Source observations` lead sentence of `harness-runs/user_reviews/feat_planning_driver_python_cutover_fix_plan.md`, written by `user-review-fix-plan-writer` (#1 of the fix-plan half), which cited the plugin's `instructions/untrusted_input.md` by absolute path instead of `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md`. Fixed by test-fix commit 528e643f; round 2 passed.
- **cost this run:** one extra Run gates round plus 4 dispatches (#15–#18)

## The per-unit layer reviewer passed every unit with no fix iteration
- **category:** optimization
- **evidence:** zero-yield phase: `layer-reviewer` ran 8 times across 6 units (Findings 3, 5, 4 single-layer; Finding 2 graphscene + devscene-flow-host; Finding 1 devscene-flow-host + general; test-fix Finding 1), and every return was `PASS` at iteration 0, so no reviewer caused a fix. Three of those reviews wrote a findings file with Should Fix or Nice to Have items that were not acted on: `harness-runs/user_review_fix_plan_point_reviews/feat_planning_driver_python_cutover_fix_plan/item_2/review_0.md`, `…/item_1/review_0.md`, `…/item_1/review_1.md`.
- **cost this run:** 8 of 19 fix-half dispatches
