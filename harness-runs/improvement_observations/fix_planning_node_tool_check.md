## A layer implementer blocked on a multi-layer unit, asking for the per-layer split the unit loop already performs
- **category:** agent-contract
- **evidence:** Phase C, code-review Finding 1, readiness tag `_(layer: cli, general)_` (`harness-runs/code_reviews/fix_planning_node_tool_check_code_review.md`). Dispatch #11 (`layer-implementer`, layer `cli`) returned `blocker: finding 1 needs an edit outside the `cli` layer's path scope (`docs/flow-graph-walker.md` belongs to the `general` catch-all layer), so the unit needs splitting before it is dispatched` and made no edit. Re-dispatched as #12 with a `context_notes:` line naming the per-layer split, recorded in `harness-runs/dispatch_additions/fix_planning_node_tool_check.md`; #12 and the `general` dispatch #13 then completed the unit.
- **cost this run:** one extra `layer-implementer` dispatch and one dispatch-additions record; strictly read, an unmarked blocker is an `<escalate>` that would have parked the run.
- **hypothesis:** the implementer's dispatch block does not tell it that a multi-layer finding is dispatched once per layer.

## `printenv HOME` refused for two agents whose instructions named it
- **category:** tooling-gap
- **evidence:** Phase G round 1: `test-fix-plan-writer` (#16) reported "I was not allowed to run `printenv HOME`" and took the home directory from the checkout root; `layer-implementer` (#19) on `harness-runs/test_fix_plans/fix_planning_node_tool_check_task_round_1/finding_1.md` reported the finding asked for a bare `printenv HOME`, "but the tool layer refused that command", and recorded a deviation note in that finding file.
- **cost this run:** two agents fell back to deriving the home directory indirectly; one plan deviation recorded.

## A layer implementer piped its tree-guard runs through `tail`
- **category:** agent-contract
- **evidence:** Phase A, Task 1, dispatch #1 (`layer-implementer`, layer `cli`) reported running `test/main-anchor-isolation.test.mjs`, `test/shipped-scripts-mktemp.test.mjs` and `test/watcher-main-anchor.test.mjs` "through `| tail -9`, which the test-run rule forbids", reading the counts from the TAP summary.
- **cost this run:** the tree-guard evidence for Task 1 is a truncated tail rather than the foreground output the test-run rule requires.

## The configured default branch has no local ref in the run checkout
- **category:** tooling-gap
- **evidence:** `devscene.config.json` `defaultBranch` is `dev`. `branch-reviewer` (#8) reported "There is no local `dev` branch in this checkout, so I diffed against `origin/dev`"; `statistics-plan-writer` (#21) reported "`git log dev..HEAD` failed. I used `origin/dev..HEAD` instead" and recorded the substitution in `harness-runs/branch_statistics/fix_planning_node_tool_check/statistics.md`.
- **cost this run:** two agents had to recover from a failed `<default_branch>..HEAD` range and each improvised the same fallback.

## Gate 13 reported BLOCKED in a round counted as one failure among 24
- **category:** silent-failure
- **evidence:** Phase G round 1 log `harness-runs/test_run_logs/fix_planning_node_tool_check/task_round_1.log` (untracked), as summarised by `test-fix-plan-writer` (#16): gate 13 (13a–13c) "was blocked until `bash scripts/python-service.sh sync` is run, and 13d and 14d were skipped. The run did not count any of these as failures (`run-gates: 1 failed, 23 passed`)". Round 2 printed `pass` with no fix landed for gate 13.
- **cost this run:** the branch's Run gates `pass` does not cover gates 13a–13d and 14d.
