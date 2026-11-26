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
