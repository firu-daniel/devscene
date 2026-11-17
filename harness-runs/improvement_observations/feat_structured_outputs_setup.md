# Script-driven planning — 2026-11-17T17:35:57Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
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
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 623s 4.3899084; #2 architecture_review architecture-reviewer 1/3 PASS 56s 1.1882632; #3 plan_review task-plan-reviewer 1/3 FAIL 149s 2.0723682; #4 plan_writer task-plan-writer 1/3 returned 29s 0.2866576; #5 architecture_review architecture-reviewer 1/3 PASS 60s 1.1093608; #6 plan_review task-plan-reviewer 1/3 FAIL 169s 2.3625726; #7 plan_writer task-plan-writer 1/3 returned 21s 0.27623220000000004; #8 architecture_review architecture-reviewer 1/3 PASS 30s 0.5959948; #9 plan_review task-plan-reviewer 1/3 PASS 46s 0.4661972
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## Every diff_base: dev reviewer fell back to origin/dev because the run copy has no local dev ref
- **category:** agent-contract
- **evidence:** the A2 architecture-reviewer, Phase B branch-reviewer, Phase C2 skeptic-reviewer and D.1 statistics-plan-writer returns each reported that `dev` (devscene.config.json `defaultBranch`) has no local ref in this checkout (`git diff dev...HEAD` → `bad revision`) and that they used `origin/dev` instead; the A2 dispatch block carried `diff_base: dev` as `plan_orchestration_instructions_core.md` → `### A2.1` spells it
- **cost this run:** 4 of 14 dispatches had to resolve a diff base other than the one they were handed; each agent improvised the fallback
- **hypothesis:** (guess) the outer loop cuts the branch from `origin/<default_branch>` and never creates the local ref, as D.2's Branch-delivery bullet already notes for its own count

## Implementers ran tree guards in a form the conventions document forbids
- **category:** agent-contract
- **evidence:** 4 of 9 `layer-implementer` returns said so themselves — Task 1 ("piped that run's output through `grep`"), Task 2 ("a `cd` prefix and a pipe"), code-review Finding 3 ("named five files where the document names one, and I piped the output through `grep` … the exit status was not recorded"), code-review Finding 5 ("piped that output through `grep`")
- **cost this run:** the guard results for those 4 units rest on filtered counts rather than the command's exit status

## A unit reported no tree guard selected for a path four guards cover
- **category:** silent-failure
- **evidence:** the code-review Finding 2 implementer (commit a4ad711f, changed path `plugin/commands/analyze.md`) returned "No tree guard was selected", while devscene.config.json `treeGuards` lists `plugin/**/*.md` as the `covers` of `test/main-repo-resolution-corpus.test.mjs`, `test/untrusted-input-corpus.test.mjs`, `test/commit-step-calls.test.mjs` and `test/agent-return-schemas.test.mjs`
- **cost this run:** 4 guards unrun for that unit; caught only by Phase G round 1, which passed

## The plan needed 3 review rounds (convergence churn)
- **category:** optimization
- **evidence:** distinct round indices 0, 1, 2 across `harness-runs/task_plan_reviews/feat_structured_outputs_setup/` and `harness-runs/architecture_reviews/feat_structured_outputs_setup/` (no business-parity folder; parity off). task-plan-reviewer: round 0 FAIL, 2 findings (net-new); round 1 FAIL, 3 findings — 1 re-raised (the `task_3_plan.md` decision-record paragraph naming the old `action_taken:` field), 2 net-new; round 2 PASS, 0 findings. architecture-reviewer PASS in all 3 rounds
- **cost this run:** 3 plan rounds, 9 planning node sessions

## architecture-reviewer produced no finding in any of its 4 dispatches
- **category:** optimization
- **evidence:** plan-gate rounds 0–2 each `verdict: PASS` (`harness-runs/architecture_reviews/feat_structured_outputs_setup/review_0.md`–`review_2.md`) and the Phase A2 implemented-branch review returned `PASS` with no file written
- **cost this run:** 4 dispatches, 0 findings
