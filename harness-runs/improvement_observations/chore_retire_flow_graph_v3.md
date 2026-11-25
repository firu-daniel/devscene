# Script-driven planning — 2026-11-25T12:00:24Z

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
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #7 plan_writer (task-plan-writer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 737s 6.801318399999998; #2 architecture_review architecture-reviewer 1/3 PASS 100s 1.975575; #3 plan_review task-plan-reviewer 1/3 FAIL 338s 4.321160800000001; #4 plan_writer task-plan-writer 1/3 returned 82s 0.6891713999999999; #5 architecture_review architecture-reviewer 1/3 FAIL 125s 1.9707877999999999; #6 plan_review task-plan-reviewer 1/3 PASS 368s 5.063525599999999; #7 plan_writer task-plan-writer 1/3 returned 62s 0.46949399999999997; #8 architecture_review architecture-reviewer 1/3 PASS 35s 0.5240256; #9 plan_review task-plan-reviewer 1/3 PASS 105s 1.3743278
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## A layer-implementer's single-file test run was refused, so an edited suite shipped unrun until Phase G
- **category:** tooling-gap
- **evidence:** Task 4 (layer `graphscene`) edited `graphscene/tests/engine/test_static_check.py` and reported its single-file run "skipped because the stated command was refused (running in don't ask mode)". In the same session Task 5's implementer ran `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py` for nine suites without a refusal. Source: the two `layer-implementer` returns (Task 4, commit 7dd269ec; Task 5, commit 8ef1fb13).
- **cost this run:** one edited test file was not run by its unit; the only check on it was Phase G's round-1 whole-suite run (which passed)
- **hypothesis:** (guess) the Task 4 implementer issued the graphscene test in a form the unattended profile does not allow-list, rather than the `python-service.sh` form the Task 5 implementer used.

## Implementer verification commands were refused by the permission layer and replaced with weaker evidence
- **category:** tooling-gap
- **evidence:** Task 1's `layer-implementer` reported that a compound `rm && cp` was refused, and so was `diff <(git show …)`. It replaced the planned byte diff with a line and byte count (commit b7667cf2). Task 7's `layer-implementer` reported that `bash -n scripts/run-gates.sh` and `rmdir` were refused. The `rmdir` refusal left an empty untracked `schemas/flow-graph-check/` directory on disk (commit dcf3e7f2). Source: those two returns.
- **cost this run:** two planned verifications were downgraded to indirect evidence: Task 1's byte diff and Task 7's shell parse, which the typecheck's shell-parse step stood in for. One stray empty directory was left in the run copy.

## Conventions documents falsified by this branch's work were left stale
- **category:** tooling-gap
- **evidence:** The story index's `## Scope register` rows 1–3 (`harness-runs/story_plans/chore_retire_flow_graph_v3_story_plan.md`) record `stale-rule` debt in `corpus_staleness`. It falls in three passages: `.claude/context/conventions.md` → `## The testing bar` (cites `task_plan_writing.v4.graph.json`); the same file's `## What accompanies a new unit of each kind` rows on negative schema fixtures and check fixtures (cite `schemas/flow-graph-check/` and `scripts/check-flow-graph.sh`, both deleted by Task 7); and `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` (names the `.v4` path). The Phase B `branch-reviewer` returned the same three passages as a `questions` item, and Task 5's implementer flagged the first one. This session did not see the `task-plan-writer` return, because planning ran script-driven in an earlier session.
- **cost this run:** a follow-up restatement of those three conventions passages is owed. Until it lands, the fixture row tells an implementer to run a command that no longer exists.

## The task plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** The plan's rounds are the distinct round indices across `harness-runs/task_plan_reviews/chore_retire_flow_graph_v3/` and `harness-runs/architecture_reviews/chore_retire_flow_graph_v3/`, which are `review_0`–`review_2`, so 3 rounds (no business-parity folder, because parity is off). Rounds 0 and 1 carry `verdict: FAIL` (the plan review in round 0, the architecture review in round 1). Finding headings, each round diffed against its predecessor in the same root:
  - **Plan-review root.** Round 0: 6 net-new. Round 1: 2 net-new, 3 re-raised. Round 2: 1 net-new, 4 re-raised.
  - **Architecture root.** Round 0: 0 findings. Round 1: 2 net-new. Round 2: 0 findings.
  - **The `docs/watcher.md` "two graphs" sentence.** Raised as Should Fix in plan-review round 0, re-raised in rounds 1 and 2, then filed as Phase B code-review Finding 1 (fixed in commit fc33c3c2).
- **cost this run:** 3 plan rounds (9 planning node sessions, per the script-driven block above), plus one Phase B finding the plan rounds had already named.
