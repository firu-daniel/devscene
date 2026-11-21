# Script-driven planning — 2026-11-21T09:42:14Z

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
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 3 denial(s)
- **cost this run:** 3 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
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
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 833s 5.830770799999999; #2 architecture_review architecture-reviewer 1/3 PASS 97s 1.4217936; #3 plan_review task-plan-reviewer 1/3 FAIL 370s 3.501637400000001; #4 plan_writer task-plan-writer 1/3 returned 168s 0.9284681999999999; #5 architecture_review architecture-reviewer 1/3 PASS 102s 1.2822122; #6 plan_review task-plan-reviewer 1/3 FAIL 323s 3.2087528000000005; #7 plan_writer task-plan-writer 1/3 returned 49s 0.3181648; #8 architecture_review architecture-reviewer 1/3 PASS 48s 0.5306138; #9 plan_review task-plan-reviewer 1/3 PASS 91s 0.6100256
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** convergence churn on the plan unit: 3 distinct round indices (0, 1, 2) across `harness-runs/task_plan_reviews/fix_agent_python_probes/` and `harness-runs/architecture_reviews/fix_agent_python_probes/` (no business-parity folder, `phases.parity` false). `task_plan_reviews/…/review_0.md` and `review_1.md` carry `verdict: FAIL`, `review_2.md` `verdict: PASS`; every architecture round `verdict: PASS`. Per round, by finding title: round 1 — 1 net-new (the `layer-implementer.md` restatement Must Fix), 2 re-raised from round 0 (the readiness-order Should Fix and the orphaned `<scripts_dir>` Should Fix); round 2 — 2 net-new, 0 re-raised.
- **cost this run:** 2 extra plan rounds (writer + architecture-reviewer + task-plan-reviewer each)

## End-of-branch reviewers could not resolve the `dev` diff base in the run copy
- **category:** agent-contract
- **evidence:** Phase A2 dispatched `architecture-reviewer` with `diff_base: dev`; its return reports `git diff dev...HEAD` failed with "bad revision" because the run copy has no local `dev` branch, and it reviewed against `origin/dev`. `branch-reviewer` (Phase B), `review-plan-reviewer` (B.2), `skeptic-reviewer` (C2) and `statistics-plan-writer` (D.1, `git log dev..HEAD`) each reported the same missing ref and the same fallback to `origin/dev`.
- **cost this run:** 5 dispatches each spent a failed command and an improvised base; none blocked
- **hypothesis:** the agents' `<default_branch>` diff commands assume a local ref a fresh run copy does not carry.

## Implementer commands refused by the permission layer
- **category:** tooling-gap
- **evidence:** Task 1's `layer-implementer` return: the throwaway-fixture command it meant to use to exercise the no-library fallback of `scripts/python-service.sh` and `check` with no `uv` on `PATH` was refused, so both paths shipped verified by reading only. Task 7's `layer-implementer` return: its scripted comparison of the C2 derivation against the scope register was refused, and it compared by reading instead.
- **cost this run:** 2 verifications downgraded to code reading

## branch-reviewer ran the main checkout's copy of its definition, not the branch's
- **category:** agent-contract
- **evidence:** Phase B `branch-reviewer` return: it ran the main checkout's `plugin/agents/branch-reviewer.md`, which predates this branch's Task 6 probe-file exception, so its probe file `harness-runs/scratch/branch_review_fix_agent_python_probes.py` was written outside the write bound its loaded definition states.
- **cost this run:** one review-file write outside the agent's stated bound (gitignored, not committed)
