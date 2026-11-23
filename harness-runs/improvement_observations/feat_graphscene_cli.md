# Script-driven planning — 2026-11-23T12:08:37Z

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
- **evidence:** #4 plan_writer (task-plan-writer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #8 architecture_review (architecture-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #9 plan_review (task-plan-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 374s 3.264444; #2 architecture_review architecture-reviewer 1/3 FAIL 97s 1.3619184; #3 plan_review task-plan-reviewer 1/3 PASS 242s 3.206408600000001; #4 plan_writer task-plan-writer 1/3 returned 182s 1.2079722000000002; #5 architecture_review architecture-reviewer 1/3 PASS 56s 0.9976842000000001; #6 plan_review task-plan-reviewer 1/3 FAIL 185s 2.4914457999999997; #7 plan_writer task-plan-writer 1/3 returned 33s 0.303493; #8 architecture_review architecture-reviewer 1/3 PASS 43s 0.8518387999999998; #9 plan_review task-plan-reviewer 1/3 PASS 49s 0.4718226000000001
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## Task plan took 3 review rounds to converge
- **category:** optimization
- **evidence:** round files `harness-runs/task_plan_reviews/feat_graphscene_cli/review_0.md`–`review_2.md` and `harness-runs/architecture_reviews/feat_graphscene_cli/review_0.md`–`review_2.md` (3 distinct round indices; no business-parity folder, `phases.parity` false). `verdict:` lines: round 0 architecture FAIL / plan-review PASS; round 1 architecture PASS / plan-review FAIL; round 2 both PASS. Net-new vs re-raised split per round: unmeasurable — the round files list findings under `## Must Fix` / `## Should Fix` / `## Nice to Have` with no per-finding heading, so no heading exists to match across rounds.
- **cost this run:** 2 failing plan rounds (9 planning node sessions, per the script-driven block above)

## Unit implementers disagreed on whether the `**/*.md` tree guard was selected
- **category:** agent-contract
- **evidence:** `devscene.config.json` → `treeGuards` maps `test/no-container-home-paths.test.mjs` to `**/*.md`. The Task 4 implementer (changed `graphscene/README.md`) reported that guard selected and ran it (1 pass). The Task 5 implementer (changed `ROADMAP.md`, `docs/development.md`, commit 8f694090) reported "Tree guards: none selected"; the code-review Finding 3 implementer (changed `graphscene/README.md`, `graphscene/src/graphscene/facade/cli.py`, commit cdd56998) reported "No tree guard was selected"; the code-review Finding 1 implementer (changed `graphscene/README.md`, commit b824c455) reported running no test and named no guard.
- **cost this run:** the guard was skipped at unit level on 3 of the 4 units whose diff matched it; Phase G round 1 passed, so no defect slipped through this time
- **hypothesis:** (guess) the implementers matched `**/*.md` against only the paths they thought of as code

## The worked `uv run … graphscene` command was refused to the Task 4 implementer
- **category:** tooling-gap
- **evidence:** the Task 4 implementer's return (commit eb6ade9e) states the direct `uv run --frozen --no-sync --project graphscene graphscene check …` invocation was refused by the permission layer; it recorded the README line as an evidence downgrade in `harness-runs/task_plans/feat_graphscene_cli/task_4_plan.md`, verified only by reading the wrapper and `graphscene/pyproject.toml`.
- **cost this run:** the documented `uv run` command form in `graphscene/README.md` → `## The command line` shipped without being run

## The plan recorded a stale conventions rule this branch falsifies
- **category:** tooling-gap
- **evidence:** `harness-runs/story_plans/feat_graphscene_cli_story_plan.md` → `## Scope register` row 3 records a `stale-rule` corpus-staleness entry: `.claude/context/graphscene.md` → `## The model and its wire forms` ("The walk-state document is the other wire form") is falsified by Tasks 1–3, which add the step and round-resume documents (`graphscene/src/graphscene/adapters/walk_json.py`) and the check document (`graphscene/src/graphscene/adapters/check_json.py`) as wire forms. The writer's `corpus_staleness` return itself reached the earlier planning session, not this one; this entry is taken from the committed story index.
- **cost this run:** a follow-up restatement of that section of `.claude/context/graphscene.md` is owed
