# Script-driven planning — 2026-11-17T15:47:16Z

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
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 827s 7.490261399999999; #2 architecture_review architecture-reviewer 1/3 PASS 58s 1.4810896000000002; #3 plan_review task-plan-reviewer 1/3 FAIL 248s 3.0587839999999997; #4 plan_writer task-plan-writer 1/3 returned 108s 0.9583396000000001; #5 architecture_review architecture-reviewer 1/3 PASS 107s 1.5964132; #6 plan_review task-plan-reviewer 1/3 FAIL 283s 4.068308999999999; #7 plan_writer task-plan-writer 1/3 returned 39s 0.291693; #8 architecture_review architecture-reviewer 1/3 PASS 29s 0.8162198; #9 plan_review task-plan-reviewer 1/3 PASS 47s 0.496218
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## Implementers reported "no tree guard selected" for changes the configured treeGuards cover
- **category:** agent-contract
- **evidence:** 5 of 11 `layer-implementer` returns this run said no tree guard was selected although the unit changed a path matching a `treeGuards` `covers` glob in `devscene.config.json`: Task 1 (`plugin/agents/review-plan-reviewer.md`, `plugin/schemas/review-plan-reviewer.return.json` — match `plugin/**/*.md`, `plugin/schemas/**`), Task 6 (`docs/structured-agent-returns.md` — a literal `covers` value and `**/*.md`), code-review Findings 4, 3 and 1 (`plugin/instructions/*.md` — match `plugin/**/*.md`). Tasks 2–5 and Finding 2, changing the same kinds of paths, each selected and ran five guards.
- **cost this run:** the guards those 5 units should have run were not run per unit; Phase G round 1 printed `pass`, so no defect shipped from it.

## Implementers piped guard-test output through grep, which the conventions forbid
- **category:** agent-contract
- **evidence:** 4 `layer-implementer` returns (Tasks 3, 4, 5 and code-review Finding 2) self-reported running `npm test --workspace cli -- …` piped through `grep` to read counts; Tasks 3 and 5 re-ran it plain, Task 4 and Finding 2 report the counts from the filtered output.
- **cost this run:** extra guard runs on 2 units; on 2 units the per-unit guard evidence rests on filtered output.

## Reviewers dispatched with `diff_base: dev` found no local `dev` ref in the run copy
- **category:** agent-contract
- **evidence:** the A2 `architecture-reviewer` dispatch (`diff_base: dev`) reported `git diff dev...HEAD` failing with `fatal: bad revision`, and the B.1 `branch-reviewer` reported "this checkout has no local `dev` branch"; both fell back to `origin/dev` (`82ad4406`).
- **cost this run:** none measured — both reviewers recovered by choosing `origin/dev` themselves.
- **hypothesis:** a run copy without a local `<default_branch>` ref makes every `diff_base: <default_branch>` dispatch depend on the agent improvising the remote-tracking ref.

## A branch-reviewer re-dispatch reported Bash denied
- **category:** tooling-gap
- **evidence:** the B.2 re-dispatch `[B · review-plan · iter 2] → branch-reviewer (#12)` reported "Bash was denied in this session, so I rewrote the whole index with Write".
- **cost this run:** the code-review index was rewritten whole instead of edited in place.

## The plan needed 3 review rounds
- **category:** optimization
- **evidence:** `harness-runs/task_plan_reviews/feat_structured_outputs_branch_review/` and `harness-runs/architecture_reviews/feat_structured_outputs_branch_review/` each hold `review_0.md`–`review_2.md` (3 distinct round indices). `task-plan-reviewer`: round 0 FAIL — 4 Must Fix, 1 Should Fix; round 1 FAIL — Must Fix 0 net-new / 1 re-raised (Scope register P2 ledger-rule rows), Should Fix 1 net-new (one-bullet-per-property `### Return fields`) / 1 re-raised (Task 4's autonomous `<escalate>` row); round 2 PASS. `architecture-reviewer` PASS in all three rounds.
- **cost this run:** 2 extra plan rounds (6 of the 9 planning node sessions).
