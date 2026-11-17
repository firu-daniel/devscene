# Script-driven planning — 2026-11-17T19:18:05Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 757s 6.5243522; #2 architecture_review architecture-reviewer 1/3 PASS 86s 1.5135958; #3 plan_review task-plan-reviewer 1/3 FAIL 257s 3.2298490000000006; #4 plan_writer task-plan-writer 1/3 returned 158s 1.276481; #5 architecture_review architecture-reviewer 1/3 PASS 84s 1.4075951999999998; #6 plan_review task-plan-reviewer 1/3 FAIL 240s 3.3036184; #7 plan_writer task-plan-writer 1/3 returned 36s 0.3693896; #8 architecture_review architecture-reviewer 1/3 PASS 32s 0.6684102; #9 plan_review task-plan-reviewer 1/3 PASS 58s 0.5098418
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The plan needed 3 plan-review rounds to converge
- **category:** optimization
- **evidence:** Convergence churn trip-wire. The plan unit has 3 distinct round indices (0, 1, 2) across `harness-runs/task_plan_reviews/feat_structured_outputs_docs_qa/` and `harness-runs/architecture_reviews/feat_structured_outputs_docs_qa/`. The business-parity gate is off (`phases.parity=false`) and wrote no folder. task-plan-reviewer recorded `verdict: FAIL` on rounds 0 and 1 and `verdict: PASS` on round 2. architecture-reviewer recorded `verdict: PASS` on all three. The net-new vs re-raised split per round could not be determined: those round files hold only severity-section headings (`## Must Fix` / `## Should Fix` / `## Nice to Have`), with no per-finding headings to match across rounds.
- **cost this run:** 2 extra plan-review rounds (6 extra node sessions: #4–#9 in the script-driven planning block above)

## Implemented-branch reviewers were handed a `diff_base` naming a branch absent in this checkout
- **category:** agent-contract
- **evidence:** Four dispatches each reported that the configured `defaultBranch` `dev` has no local branch in this checkout and that they diffed or logged against `origin/dev` instead: architecture-reviewer (A2.1, `diff_base: dev`, #7), branch-reviewer (B.1, #8), review-plan-reviewer (B.2 iteration 0, #9) and statistics-plan-writer (D.1, #19). `git log origin/dev..HEAD` resolves; the local `dev` ref does not exist here.
- **cost this run:** none measured; each agent fell back to `origin/dev` on its own judgement
- **hypothesis:** a guess — the A2.1 dispatch block's `<default_branch>` is a bare branch name, while D.2 already states the base should be the remote-tracking ref.

## Layer-implementers piped test runs that the test-run rule requires in the foreground
- **category:** agent-contract
- **evidence:** Three layer-implementer returns said they had piped a test or tree-guard run through a filter, against `unit_loop_core.md` → `## The test-run rule` point 6: Task 4 (#4) and skeptic Finding 1 (#17) each reran the guards plainly afterwards; code-review Finding 1 (#14) reported its piped counts without a plain rerun.
- **cost this run:** one unit's guard evidence (#14) rests on piped runs only

## The first code review asked a fix to run a test file, which cost one meta-review round
- **category:** agent-contract
- **evidence:** branch-reviewer (#8) wrote `harness-runs/code_reviews/feat_structured_outputs_docs_qa_code_review/finding_1.md` with a `Verification:` paragraph naming `npm test --workspace cli -- test/agent-return-schemas.test.mjs`. That is a test file the fix neither creates nor edits (test-run rule point 4). review-plan-reviewer FAILed the review on it in `harness-runs/review_plan_reviews/feat_structured_outputs_docs_qa/review_0.md`, with must_fix_count 2.
- **cost this run:** 1 extra branch-reviewer re-dispatch (#10) and 1 extra meta-review (#11)

## A review agent's Bash script was denied and it fell back to Write
- **category:** tooling-gap
- **evidence:** The branch-reviewer re-dispatch (B.2 iteration 1, #10) reported that its first attempt to edit the code-review files used a Bash script, which the permission mode denied. It then rewrote the three files with Write.
- **cost this run:** one refused tool call; the edit landed through Write
