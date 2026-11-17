## Task plan needed 3 plan-review rounds before PASS
- **category:** optimization
- **evidence:** `harness-runs/task_plan_reviews/feat_committer_as_script/` and `harness-runs/architecture_reviews/feat_committer_as_script/` each hold `review_0.md`, `review_1.md`, `review_2.md` (3 distinct round indices; rounds 0 and 1 carry `verdict: FAIL`, round 2 passed). Per root, by finding title: task-plan-reviewer round 1 — 3 re-raised from round 0, 5 net-new; round 2 — 0 re-raised, 1 net-new (Nice to Have). architecture-reviewer round 1 — 2 re-raised from round 0, 3 net-new; round 2 — 0 re-raised, 1 net-new (Nice to Have).
- **cost this run:** two extra writer revisions and two extra rounds of both plan gates before P1.

## Two plan gates raised the same finding on the same plan round
- **category:** optimization
- **evidence:** round 1 of the task plan: `harness-runs/task_plan_reviews/feat_committer_as_script/review_1.md` Must Fix 1 and `harness-runs/architecture_reviews/feat_committer_as_script/review_1.md` Must Fix 1 carry the identical title "`task_1_plan.md` names a tree guard the task neither creates nor edits."
- **cost this run:** one duplicated Must Fix across task-plan-reviewer and architecture-reviewer in one round.

## Run gates round 1 was redone after the resume
- **category:** optimization
- **evidence:** `harness-runs/PAUSE_PROGRESS.md` records the pause in Phase G with `harness-runs/test_fix_plans/feat_committer_as_script_task_round_1.md` and its finding folder untracked (G.3 had not run). On resume G.0 took the "Untracked" arm: `bash scripts/run-test-suite.sh task_round_1` answered `pending` and ran the whole round again (a finished `harness-runs/test_run_logs/feat_committer_as_script/task_round_1.verdict` was already on disk), then `test-fix-plan-writer` rewrote the round-1 draft (dispatch #1 this session) before the architecture gate and G.3 commit.
- **cost this run:** one full gate run (both gates) and one test-fix-plan-writer dispatch repeated.
