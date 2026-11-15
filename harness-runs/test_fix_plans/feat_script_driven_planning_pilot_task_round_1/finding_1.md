### 1. Three tracked plan-round artifacts name machine paths under the home directory

**Site:** three tracked files under `harness-runs/`, each grep-verified in the current tree:

- `harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md` — three occurrences of `<home>/Work/devscene/plugin/instructions/unit_loop_core.md` (navigation hint: lines 6, 10, 16; each is followed by `` → `## The test-run rule` ``).
- `harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_2.md` — one occurrence of the same path, in the sentence beginning `So \`<home>/Work/devscene/plugin/instructions/unit_loop_core.md\`` (hint: line 8).
- `harness-runs/plan_revisions/feat_script_driven_planning_pilot/task_plan_revision_2.md` — three occurrences of `<home>/Work/devscene-feat_script_driven_planning_pilot/harness-runs/`, one inside the parenthesis of each of the `- architecture-reviewer 1 (`, `- architecture-reviewer 2 (` and `- task-plan-reviewer 1 (` bullets (hint: lines 2–4).

`<home>` here stands for the running user's home directory. This plan writes no literal home path, because gate 6a scans this file too.

**Failing test:** none — 6a no machine paths (`scripts/check-machine-paths.sh`)

**Failure (from the log, rewritten per step 5):**

```
FAIL  6a no machine paths (printed output, which is the finding, 2 s)
      ./harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md:6:Round 0's two Must Fix items are resolved. … The two Must Fix items below are new: both come from `<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule`, which binds every reviewer.
      ./harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md:10:1. **`task_3_plan.md` — a `**Verification:**` bullet names test files the unit neither creates nor edits** (`<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 4: …)
      ./harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md:16:2. **`task_10_plan.md` — its source guard reads a whole tree, and no task registers it in `treeGuards`** (`<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8: …)
      ./harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_2.md:8:1. **`task_3_plan.md` — "runs no test file" reads as a limit on the unit's test runs.** … So `<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 7 still has the unit run those guards. …
      ./harness-runs/plan_revisions/feat_script_driven_planning_pilot/task_plan_revision_2.md:2:- architecture-reviewer 1 (harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md) — files: harness-runs/task_plans/feat_script_driven_planning_pilot/task_3_plan.md — resolved
      ./harness-runs/plan_revisions/feat_script_driven_planning_pilot/task_plan_revision_2.md:3:- architecture-reviewer 2 (harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md) — files: harness-runs/task_plans/feat_script_driven_planning_pilot/task_10_plan.md — resolved
      ./harness-runs/plan_revisions/feat_script_driven_planning_pilot/task_plan_revision_2.md:4:- task-plan-reviewer 1 (harness-runs/task_plan_reviews/feat_script_driven_planning_pilot/review_1.md) — files: harness-runs/task_plans/feat_script_driven_planning_pilot/task_10_plan.md — resolved
```

(In the last three lines the log shows the absolute path of this checkout's root before `harness-runs/`. Step 5 rewrote it to the repo-relative form shown.)

**Diagnosis.** Gate 6a prints every line under the working tree that contains the running user's `$HOME`. It skips `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch` and `__pycache__`, and filters out `harness-runs/clarifications/*/` and `harness-runs/.flow_walker_state`. The gate fails on any output. All three files are tracked, and this branch committed them during its plan rounds (`chore: Plan round 1` / `chore: Plan round 2`). The architecture reviewer cited the plugin's instruction document by its absolute install path rather than as `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md`. The round-2 revision note recorded the findings files by absolute path, but the round-1 note (`task_plan_revision_1.md`) records them repo-relative (`harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_0.md`). A tree-wide search for the home prefix over the same scope finds exactly these three files and no others, so this finding clears 6a completely. The failure is in the run artifacts, not in shipped code.

**Fix.** Edit only the path text and keep every other byte of each line:

- [ ] In `review_1.md` (three places) and `review_2.md` (one place), replace `<home>/Work/devscene/plugin/instructions/unit_loop_core.md` with `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md`. That is the form the plugin corpus uses to cite its own instruction documents.
- [ ] In `task_plan_revision_2.md` (three places), delete the `<home>/Work/devscene-feat_script_driven_planning_pilot/` prefix inside each parenthesis. The parenthesis then reads `(harness-runs/architecture_reviews/feat_script_driven_planning_pilot/review_1.md)`, or `(harness-runs/task_plan_reviews/feat_script_driven_planning_pilot/review_1.md)` on the `task-plan-reviewer 1` bullet. That matches `task_plan_revision_1.md`.
- [ ] Confirm with a literal grep for the home-directory prefix over `harness-runs/architecture_reviews/feat_script_driven_planning_pilot/` and `harness-runs/plan_revisions/feat_script_driven_planning_pilot/` that nothing is left. This is a text search, not a gate run.

- **Deviations from plan:** Row-`G.4` check took the fix-site fallback, because the finding names no test file (`none — 6a no machine paths`) and a gate script is never run. Before the edit, the fix sites still held the home prefix: a `grep -rn "$HOME"` over the two directories listed all seven lines. So the fix was applied, not closed as already passing. Gate 6a (`scripts/check-machine-paths.sh`) was not run, and the close rests on two things instead. First, the same `grep -rn "$HOME"` over `harness-runs/architecture_reviews/feat_script_driven_planning_pilot/` and `harness-runs/plan_revisions/feat_script_driven_planning_pilot/` exits 1 after the edit, with no output. Second, the tree guard `test/no-container-home-paths.test.mjs` (selected by `covers: **/*.md`) passes through `npm test --workspace cli -- test/no-container-home-paths.test.mjs`. The Run gates phase verifies gate 6a.
