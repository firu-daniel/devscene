# Script-driven planning — 2026-11-20T07:02:49Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #9 plan_review (task-plan-reviewer), round 2: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 724s 5.3918114; #2 architecture_review architecture-reviewer 1/3 PASS 120s 1.6473864; #3 plan_review task-plan-reviewer 1/3 FAIL 280s 3.291101799999999; #4 plan_writer task-plan-writer 1/3 returned 45s 0.4013546; #5 architecture_review architecture-reviewer 1/3 PASS 126s 1.5764760000000002; #6 plan_review task-plan-reviewer 1/3 FAIL 319s 3.3361386; #7 plan_writer task-plan-writer 1/3 returned 63s 0.560489; #8 architecture_review architecture-reviewer 1/3 PASS 60s 0.5639098; #9 plan_review task-plan-reviewer 1/3 PASS 96s 1.4690911999999998
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## A graphscene unit's own Python test and strict mypy did not run inside the unit, so a type error first surfaced at Run gates
- **category:** tooling-gap
- **evidence:** Task 2 implementer (dispatch #2) returned "skipped, no single-file command stated (`.claude/context/graphscene.md` → `## Not determined`)" for `graphscene/tests/test_flow_graph_schema.py`. The Task 3 implementer (dispatch #3) ran `bash scripts/python-service.sh --package graphscene test tests/test_vocabulary.py` but reported "Mypy `strict` and ruff were not run". Run gates round 1 (`harness-runs/test_run_logs/feat_flow_graph_schema_v2/task_round_1.log`) then failed gate 13f on `graphscene/src/graphscene/vocabulary.py`, fixed by commit 43f4184c.
- **cost this run:** one extra Run gates round (round 2), plus a test-fix-plan-writer, an architecture-reviewer and one implementer dispatch
- **hypothesis:** the graphscene conventions document states no per-unit test or type-check command, though the Task 3 implementer found one that worked.

## A planning-round review file carried an absolute machine path into a commit, caught only by gate 6a in Phase G
- **category:** agent-contract
- **evidence:** `harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/review_1.md` (committed by the planning round-1 commit 7a1fc52f) named the plugin's absolute install path under the home directory twice. Run gates round 1 failed gate 6a on it, and commit da23f7fe rewrote both to `${CLAUDE_PLUGIN_ROOT}`.
- **cost this run:** one test-fix finding and one implementer dispatch; shared with the gate round in the entry above

## architecture-reviewer's PASS left a Should Fix it reported in no committed file
- **category:** silent-failure
- **evidence:** Phase A2 dispatch #7 returned `{"outcome": "PASS"}` and wrote no index, while its prose reported one Should Fix: `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` sits under `cli/templates/`, which `init` never writes and which `cli/templates/README.md` says holds only files `init` writes. The finding exists only in the session transcript.
- **cost this run:** one Should Fix not carried to any readiness list or Done-summary bullet

## A layer-implementer edited two Markdown files but reported no tree guard selected
- **category:** agent-contract
- **evidence:** the implementer for code-review Finding 2 (dispatch #14, commit f5b551b9) edited `docs/development.md` and `docs/flow-graph-walker.md`, and its return said "no tree guard was selected". `devscene.config.json` → `treeGuards` maps `test/no-container-home-paths.test.mjs` to `**/*.md`. The implementer for Finding 3 (dispatch #15), editing `docs/flow-graph-walker.md`, did select and run that guard.
- **cost this run:** one unit committed without its selected tree guard run; the guard first ran at Phase G

## The configured default branch has no local ref in this checkout, so four agents fell back to `origin/dev` on their own
- **category:** tooling-gap
- **evidence:** `git log --format='%h %s%n%b' --name-only dev..HEAD` failed with `fatal: ambiguous argument 'dev..HEAD': unknown revision`. architecture-reviewer (#7), branch-reviewer (#8), skeptic-reviewer (#16) and statistics-plan-writer (#23) each reported diffing or logging against `origin/dev` instead.
- **cost this run:** none measured; each agent noted the substitution in its return

## The plan needed 3 review rounds
- **category:** optimization
- **evidence:** `harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/` and `harness-runs/architecture_reviews/feat_flow_graph_schema_v2/` each hold `review_0.md`–`review_2.md`, which is 3 distinct round indices. The task-plan-reviewer files read `verdict: FAIL`, `FAIL`, `PASS`. The net-new vs re-raised split is unmeasurable: the round files carry their findings under `## Must Fix` / `## Should Fix` section headings only, with no per-finding heading to match across rounds.
- **cost this run:** 2 extra plan rounds (9 planning node sessions, per the script-driven block above)
