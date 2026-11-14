## The task plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** Plan-review round files `harness-runs/task_plan_reviews/feat_parallel_plan_reviews/review_{0,1,2}.md` and `harness-runs/architecture_reviews/feat_parallel_plan_reviews/review_{0,1,2}.md` — 3 distinct round indices (rounds 0 and 1 FAIL, round 2 PASS; business-parity gate skipped, `phases.parity` false). Per root, finding titles diffed against the previous round in the same root: task-plan-reviewer — round 0: 4 findings; round 1: 4 net-new, 0 re-raised; round 2: 1 net-new, 0 re-raised. architecture-reviewer — round 0: 1 finding; round 1: 3 net-new, 0 re-raised; round 2: 0.
- **cost this run:** 2 extra writer revisions and 4 extra gate dispatches before the plan converged (9 planning dispatches in total).
- **hypothesis:** (guess) every finding being net-new rather than re-raised points at partial passes per round, not at fixes that failed to land.

## Implementers reported "no tree guard was selected" for changes that matched a configured guard
- **category:** agent-contract
- **evidence:** The `layer-implementer` returns for Task 14, Task 15, Task 18 and code-review Finding 2 each stated that no tree guard was selected. Each changed only `plugin/**/*.md` files (e.g. `plugin/commands/branch-start-plan-semi-autonomous.md`, `plugin/instructions/user_review_fix_plan_writing_instructions_core.md`, `plugin/docs/AUTONOMOUS_FLOW.md`), which `devscene.config.json` `treeGuards` covers through `plugin/**/*.md` (`test/main-repo-resolution-corpus.test.mjs`, `test/untrusted-input-corpus.test.mjs`) and `**/*.md` (`test/no-container-home-paths.test.mjs`). Implementers on other plugin tasks (11, 12, 13, 16, 17) ran those same three guards for the same file class.
- **cost this run:** 4 units committed without their unit-level tree-guard runs; the Phase G round-2 suite run passed, so nothing shipped broken.

## Implementers piped single-file test runs, breaching the foreground rule
- **category:** agent-contract
- **evidence:** The Task 1 implementer's return says it piped each tree-guard run's output through `tail`; the Task 11 implementer's return says it piped each guard run through `grep` to read counts. Both self-reported the breach against `unit_loop_core.md` → `## The test-run rule` point 6. Neither reran clean.
- **cost this run:** none observed; the counts reported were the real output and the Phase G suite passed.

## Sub-agents were refused commands they needed for verification or copying
- **category:** tooling-gap
- **evidence:** Task 20 implementer: `bash -n scripts/check-flow-graph.sh` refused, so the new jq program in the checker was first executed by the Phase G gates. Task 21 implementer and the code-review Finding 1 (general layer) implementer: `cp` refused, so `scripts/flow-walker.sh` and four other self-adopted copies were rewritten by hand with the file tools and confirmed with `cmp`. Round-1 `test-fix-plan-writer`: `printenv HOME` refused during its machine-path check. Task 2 implementer: an edit attempted through Bash refused in don't-ask mode, redone with the Edit tool.
- **cost this run:** hand-copied scripts instead of `cp`; the Task 20 checker logic went unexecuted until Phase G.

## The configured default branch has no local ref in the run copy
- **category:** tooling-gap
- **evidence:** `devscene.config.json` `defaultBranch` is `dev`. In this checkout `git rev-parse --verify --quiet dev` printed nothing while `origin/dev` resolved, and `git log --format='%h %s' -i --grep='record disposition of ' --grep=' done — ' dev..HEAD` failed with exit 128 (`ambiguous argument 'dev..HEAD'`). The Phase A2 architecture reviewer, the Phase B branch reviewer and the Phase C2 skeptic reviewer were dispatched with `diff_base: dev`; the branch and skeptic reviewers each reported falling back to `origin/dev`. The Phase-D derivation here was re-run against `origin/dev..HEAD`.
- **cost this run:** each reviewer and the Phase-D derivation had to choose a substitute base on its own.

## The branch reviewer's Pass 0 grep sweep had an empty regex list
- **category:** agent-contract
- **evidence:** The Phase B `branch-reviewer` return: "Pass 0 grep sweep: its regex list is still empty in this agent's definition, so that half of Pass 0 didn't run. That is a configuration gap." It substituted a hand sweep of added lines.
- **cost this run:** the automated half of Pass 0 did not run on this branch.
