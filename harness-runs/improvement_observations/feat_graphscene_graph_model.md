# Script-driven planning — 2026-11-20T13:57:38Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 474s 3.3080396000000003; #2 architecture_review architecture-reviewer 1/3 PASS 96s 1.4020237999999998; #3 plan_review task-plan-reviewer 1/3 PASS 176s 1.8854878000000004
- **cost this run:** 3 node session(s)

# Task run (Phase D)

## Reviewers and writers could not use the dispatched `dev` diff base in the run copy, which has no local `dev` ref
- **category:** agent-contract
- **evidence:** the A2 `architecture-reviewer`, B `branch-reviewer` and C2 `skeptic-reviewer` dispatches carried `diff_base: dev` / the branch's default branch, and each return reported that `git diff dev...HEAD` failed and it diffed against `origin/dev` instead; the D.1 `statistics-plan-writer` return reported `git log dev..HEAD` failed and it read `origin/dev..HEAD`; the orchestrator's own Phase-D `git log --format='%h %s%n%b' --name-only dev..HEAD` exited 128 (`fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree.`)
- **cost this run:** 5 diff/log commands failed and were re-issued against `origin/dev`, with each agent choosing the substitute base itself
- **hypothesis:** the run copy was cut from `origin/dev` and never created a local `dev`, so every `<default_branch>..HEAD` form other than D.2's explicit `origin/<default_branch>` one misses

## Reviewers could not execute Python probes in the run copy
- **category:** tooling-gap
- **evidence:** B `branch-reviewer` return: "couldn't run a probe because the command was refused" (finding 3, `jsonschema` integral-float behaviour); B.2 `review-plan-reviewer` return: "the sandbox refused the Python call"; C2 `skeptic-reviewer` return: "the sandbox refused every attempt to execute Python" — all three confirmed behaviour by reading library source instead
- **cost this run:** 3 reviewer dispatches graded findings without a reproduction; code-review finding 3 and skeptic finding 1 shipped as read-only proofs

## The test-fix-plan writer was refused `printenv HOME` for its machine-path check
- **category:** tooling-gap
- **evidence:** G.2 `test-fix-plan-writer` return (round 1): "My permissions blocked `printenv HOME`, so I took the home directory from the sandbox paths"
- **cost this run:** 1 refused tool call; the machine-path check ran on an inferred home directory

## Package-level lint/type defects reached end-of-branch review and the Run gates instead of being caught per unit
- **category:** flow-efficiency
- **evidence:** code-review findings 1 (strict `mypy`, `graphscene/src/graphscene/vocabulary.py`, from Task 1 commit d753acd3) and 2 (`ruff`, `graphscene/tests/test_model.py` / `graphscene/tests/test_loader.py`); Run gates round 1 `fail harness-runs/test_run_logs/feat_graphscene_graph_model/task_round_1.log` on leg `13e GraphScene lint` (`I001`, `graphscene/src/graphscene/loader.py`) introduced by skeptic-fix commit c3cc8d01; every implementer return stated it did not run the package's `mypy`/`ruff` (gate 13 legs `13f`/`13e`) because `bash scripts/typecheck.sh` does not reach them
- **cost this run:** 3 fix units (2 code-review items, 1 test-fix item) and 1 extra Run gates round (round 2)
