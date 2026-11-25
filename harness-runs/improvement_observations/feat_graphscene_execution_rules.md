# Script-driven planning — 2026-11-25T17:45:38Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 416s 3.425723; #2 architecture_review architecture-reviewer 1/3 PASS 95s 1.4993064; #3 plan_review task-plan-reviewer 1/3 FAIL 211s 2.5877398000000005; #4 plan_writer task-plan-writer 1/3 returned 72s 0.5227178; #5 architecture_review architecture-reviewer 1/3 PASS 102s 1.4023636; #6 plan_review task-plan-reviewer 1/3 FAIL 237s 2.3557088000000004; #7 plan_writer task-plan-writer 1/3 returned 41s 0.3744620000000001; #8 architecture_review architecture-reviewer 1/3 PASS 39s 0.5241560000000001; #9 plan_review task-plan-reviewer 1/3 PASS 59s 0.9182226
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## Committed plan-revision notes carried an absolute checkout path, failing Run gates round 1 on gate 6a
- **category:** agent-contract
- **evidence:** `bash scripts/run-test-suite.sh --wait task_round_1` printed `fail harness-runs/test_run_logs/feat_graphscene_execution_rules/task_round_1.log`; the `test-fix-plan-writer` return names gate `6a no machine paths` as the only failure (`run-gates: 1 failed, 30 passed`), at line 2 of `harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_1.md` and `task_plan_revision_2.md`, both committed by the script-driven planning rounds (`0b5ad8ac`, `aa43310b`). Fixed by `359708c3`; round 2 printed `pass`.
- **cost this run:** one extra Run gates round, plus 3 dispatches (test-fix-plan-writer, architecture-reviewer gate, layer-implementer)
- **hypothesis:** (guess, from the test-fix-plan-writer's return) the revision-note template in `plugin/instructions/plan_review_rounds.md` copies the review path exactly as handed, and the script-driven driver handed an absolute one.

## The plan's corpus-staleness entry reached no artifact this session could read
- **category:** silent-failure
- **evidence:** `harness-runs/story_plans/feat_graphscene_execution_rules_story_plan.md` → `## Scope register` row 9 says the stale sentence in `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` was "Recorded as a `stale-rule` entry in `corpus_staleness`". Planning ran script-driven in an earlier session, so this session never received a `task-plan-writer.corpus_staleness` field; the Phase A2 `architecture-reviewer` return states it "could not find that record under `harness-runs/`".
- **cost this run:** the `stale-rule` debt (`.claude/context/graphscene.md` vs `execute_set` now running a dispatch set) is carried here and in the Done summary only by hand, from the story plan's prose.

## The statistics writer could not list the user-review folder
- **category:** tooling-gap
- **evidence:** the D.1 `statistics-plan-writer` return: "I could not check this by listing `harness-runs/user_reviews/`, because that command was blocked. I relied on the first-write prompt".
- **cost this run:** `user_review_issues = 0` in `harness-runs/branch_statistics/feat_graphscene_execution_rules/statistics.md` rests on the prompt's assumption, not on a listing.

## The plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** plan-review rounds 0, 1, 2 across `harness-runs/task_plan_reviews/feat_graphscene_execution_rules/` and `harness-runs/architecture_reviews/feat_graphscene_execution_rules/` (no business-parity folder; `phases.parity` is false). `task_plan_reviews` round 0 `verdict: FAIL`, round 1 `verdict: FAIL`, round 2 `verdict: PASS`; `architecture_reviews` PASS in all three. Net-new vs re-raised split: unmeasurable from headings — the round files carry only severity-section headings (`## Must Fix` / `## Should Fix` / `## Nice to Have`), no per-finding headings.
- **cost this run:** 3 rounds, 9 planning node sessions (per the script-driven block above).
