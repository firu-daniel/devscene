### 1. Make the two plan-revision notes' review paths repo-relative

**Site:**
- `harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_1.md` — the line beginning `- task-plan-reviewer 1 (` (line 2, hint only), whose parenthesised path ends `harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_0.md)`.
- `harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_2.md` — the line beginning `- task-plan-reviewer 1 (` (line 2, hint only), whose parenthesised path ends `harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_1.md)`.

Both grep-verified in the current tree: these two files are the only files under `harness-runs/` (tracked or untracked) naming the home directory.

**Failing test:** none — test (gate check `6a no machine paths`, run by `scripts/run-gates.sh` through `scripts/check-machine-paths.sh`)

**Class:** Broken contract

**Failure:** If `scripts/run-gates.sh` runs gate check `6a no machine paths` over this tree, then it prints the two plan-revision lines naming the checkout's absolute path and fails the test gate — `FAIL  6a no machine paths (printed output, which is the finding, 2 s)`, `run-gates: 1 failed, 30 passed`.

**Failure quoted from the log** (machine paths rewritten repo-relative):

```
== gate 6 — self-containment
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_1.md:2:- task-plan-reviewer 1 (harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_0.md) — files: harness-runs/story_plans/feat_graphscene_execution_rules_story_plan.md, harness-runs/task_plans/feat_graphscene_execution_rules/task_1_plan.md, task_2_plan.md, task_4_plan.md, task_6_plan.md — resolved (…)
        ./harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_2.md:2:- task-plan-reviewer 1 (harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_1.md) — files: harness-runs/task_plans/feat_graphscene_execution_rules/task_5_plan.md — resolved (…)
run-gates: 1 failed, 30 passed
  - 6a no machine paths
FAIL: test (exit 1)
== run-test-suite.sh: gate test exited 1 ==
```

In the log (and in the files today) each parenthesised path carries the absolute checkout-root prefix — a directory under the home directory ending in `devscene-feat_graphscene_execution_rules/` — immediately before `harness-runs/task_plan_reviews/…`. The quote above shows them already rewritten, which is exactly the fix.

**Diagnosis:** New this round (no earlier logs). `scripts/check-machine-paths.sh` prints every line under the working directory containing `$HOME`, excluding only `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch`, the Python caches, `harness-runs/clarifications/<subdir>/` and `harness-runs/.flow_walker_state`; `harness-runs/plan_revisions/` is not excluded, and any printed line fails the gate. The general-layer conventions state the same bar (`.claude/context/conventions.md` → `## The testing bar`: *"nothing in this tree may name a location on the machine that wrote it"*). The two revision notes were written from the template in `plugin/instructions/plan_review_rounds.md` → `## The writer's revision` (`- <reviewer> <n> (<findings file path>) — …`), with the findings file path copied as the round's prompt handed it — absolute. Only line 2 of each file is affected; the `files:` lists and every other line are already repo-relative. These are run artifacts committed under the self-adopted `harness-runs/` tree, which falls under the catch-all `general` layer (`path: "."`).

**Fix:**

- [ ] In `harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_1.md`, line 2: delete the absolute checkout-root prefix inside the parentheses so it reads `(harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_0.md)`. Change nothing else on the line or in the file.
- [ ] In `harness-runs/plan_revisions/feat_graphscene_execution_rules/task_plan_revision_2.md`, line 2: the same edit, so it reads `(harness-runs/task_plan_reviews/feat_graphscene_execution_rules/review_1.md)`. Change nothing else.
- [ ] Confirm with a plain text search (not a gate run) that no file under `harness-runs/`, outside the excluded `test_run_logs/` folder, still contains the home directory: `git grep -n --untracked -l` of the home directory over `harness-runs` prints nothing.

Do not edit `scripts/check-machine-paths.sh` or add an exclusion for `harness-runs/plan_revisions/`: these notes are committed, and the gate is right to grade them.
