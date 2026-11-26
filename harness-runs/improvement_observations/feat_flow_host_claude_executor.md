# Script-driven planning — 2026-11-26T12:45:04Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 496s 4.078769000000001; #2 architecture_review architecture-reviewer 1/3 PASS 70s 1.1619624; #3 plan_review task-plan-reviewer 1/3 PASS 298s 3.6101824
- **cost this run:** 3 node session(s)

# Task run (Phase D)

## The B.2 meta-reviewer had a Bash spot-check refused
- **category:** tooling-gap
- **evidence:** Phase B.2 `review-plan-reviewer` (dispatch #8) over `harness-runs/code_reviews/feat_flow_host_claude_executor_code_review.md` reported, in its return: "I could not run a planned spot-check command because the Bash call was refused. I covered the same ground with targeted greps and file reads instead." The return did not name the refused command.
- **cost this run:** 1 refused tool call; the meta-review substituted greps and file reads for the spot-check

## The skeptic reviewer could not read the issue a deferral named
- **category:** tooling-gap
- **evidence:** Phase C2 `skeptic-reviewer` (dispatch #11) reported, in its return: "I couldn't open issue #484 because `gh` was refused." Its Must Fix (`harness-runs/skeptic_reviews/feat_flow_host_claude_executor_skeptic_review/finding_1.md`) judges a deferral to #484 without reading #484.
- **cost this run:** 1 refused tool call; the finding's reasoning rests on the executor's interface alone, not on the issue it names

## A row-G.4 implementer implemented a fix after its named test passed before the edit
- **category:** agent-contract
- **evidence:** Phase G round 1, `layer-implementer` (dispatch #16) on `harness-runs/test_fix_plans/feat_flow_host_claude_executor_task_round_1/finding_1.md` ran `devscene-flow-host/tests/test_session_process.py` before editing (8 passed), then implemented the fix rather than returning `already_passing`, and returned the flag: "Row G.4: the named test passed before the edit, but the unit was not closed as already_passing. The finding diagnoses an intermittent race and the fix site lacked the fix, so the fix was implemented and a deviation was recorded in finding_1.md." Commit af973bc2.
- **cost this run:** none measured; round 2 gates passed after the commit
- **hypothesis:** (guess) the already-passing close does not distinguish a finding diagnosed as an intermittent race from one an earlier fix already cleared

# User-review fix round 1 — executor agent prompt builder, host-flag, pairing-rule and issue-number docs

## Per-unit layer reviewers could not run the package's lint, typecheck or tests
- **category:** tooling-gap
- **evidence:** Phase A, `layer-reviewer` on Item 1 (dispatch #2) reported: "I did not run the package lint (`bash scripts/python-service.sh --package devscene-flow-host lint`) because the permission mode denied it." `layer-reviewer` on Item 4 (dispatch #8) reported: "I could not run the tests, lint or typecheck: running them was refused in this session's \"don't ask\" mode. My PASS rests on reading the code and the plan, not on a green run." The `layer-implementer` dispatches on the same items (#1, #7) ran `bash scripts/typecheck.sh` and `bash scripts/python-service.sh --package devscene-flow-host test tests/test_claude_executor.py` successfully.
- **cost this run:** 2 of 4 per-unit reviews passed on reading alone; the Must Fix item's review (Item 4) ran no check of its own
- **hypothesis:** (guess) the reviewer's tool surface or the session's permission profile does not grant the `python-service.sh` invocations the implementer is granted

## A per-unit reviewer looked for the default branch under the wrong name
- **category:** agent-contract
- **evidence:** Phase A, `layer-reviewer` on Item 3 (dispatch #6) reported: "I couldn't confirm that the branch adds no other issue numbers: neither `main` nor `origin/main` exists as a ref in this checkout, so a diff against the default branch wasn't possible." `devscene.config.json` `defaultBranch` is `dev`, and `origin/dev..HEAD` resolves in this checkout.
- **cost this run:** one acceptance check in the Item 3 review (no other issue numbers added by the branch) was not made

## The user-review fix-plan fork met a task-engine ledger with no round header
- **category:** agent-contract
- **evidence:** At fix-plan Setup, `harness-runs/flow_progress/feat_flow_host_claude_executor_progress.md` held the task engine's ledger (`# Flow progress — feat_flow_host_claude_executor   (engine: task)`, no `round <n>`). `autonomous_pause_and_ledger.md` §1.4's user-review cases compare a header round that this ledger does not carry. The orchestrator handled it as "older round → re-seed" and committed the re-seeded user-review ledger in 6559fe58, carrying the `P0` `screened:` line into `R0`.
- **cost this run:** none measured; one orchestrator judgement call at a point the three cases do not name

## Per-unit layer reviewer produced no change on any unit
- **category:** optimization
- **evidence:** `layer-reviewer` ran on all 4 Phase A units (dispatches #2, #4, #6, #8), each returned `PASS` at iteration 0, and `harness-runs/user_review_fix_plan_point_reviews/feat_flow_host_claude_executor_fix_plan/` was never created (the commit wrapper skipped `item_1`–`item_4` as absent).
- **cost this run:** 4 dispatches, 0 findings
