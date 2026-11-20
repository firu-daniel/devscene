### 1. Gate 6a: `review_1.md` names an absolute machine path

**Site:** `harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/review_1.md`, in Must Fix 2's body (starts "After Task 5, `bash scripts/test.sh` reaches `scripts/run-gates.sh`", near line 16) and Must Fix 3's body (starts "Task 5 wires `node scripts/generate-flow-graph-v3.mjs` into `scripts/run-gates.sh` as leg 3i", near line 24). Each carries the substring `/Work/devscene/plugin/instructions/unit_loop_core.md` prefixed by the running user's home directory.

**Failing test:** none — `run-gates.sh` leg `6a no machine paths` (`scripts/check-machine-paths.sh`)

**Class:** Broken contract

**Failure:** If a commit carries this tree, then gate 6a's self-containment check fails, printing `./harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/review_1.md:16:` and `:24:` lines that name `<home>/Work/devscene/plugin/instructions/unit_loop_core.md`.

**Failure as logged (machine paths rewritten):**

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/review_1.md:16:   After Task 5, `bash scripts/test.sh` reaches `scripts/run-gates.sh`, … `<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 4 forbids a Verification bullet that names a gate script. …
        ./harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/review_1.md:24:   Task 5 wires `node scripts/generate-flow-graph-v3.mjs` into `scripts/run-gates.sh` as leg 3i. … This is the same test-run-rule breach as Must Fix 2 (`<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 4). …
```

**Diagnosis:** The task plan reviewer resolved the plugin's `${CLAUDE_PLUGIN_ROOT}` to its absolute install location under the home directory and wrote that literal into the review, which is tracked (committed in "chore: Plan round 1 for feat_flow_graph_schema_v2"). `scripts/check-machine-paths.sh` greps the whole working tree for `$HOME`, and `harness-runs/task_plan_reviews/` is not among its exclusions, so the two lines are printed and the gate fails. In the current tree these are the only two hits under `harness-runs/task_plan_reviews/feat_flow_graph_schema_v2/` (`review_0.md` and `review_2.md` are clean), and the log names no other file.

**Fix:**

- [ ] In `review_1.md`, on both lines, replace the absolute prefix (the home directory followed by `/Work/devscene/plugin`) with `${CLAUDE_PLUGIN_ROOT}`, so each citation reads `` `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 4 ``. This is the form `finding_grades.md` and `unit_loop_core.md` themselves use for plugin paths.
- [ ] Change nothing else in the review: its findings, grades and wording stay as written.
- [ ] Do not add an exclusion to `scripts/check-machine-paths.sh`. The review is a committed file, and gate 6a exists to keep machine paths out of committed files.

**Deviations from plan:** The finding names no test file (`none — 6a no machine paths`), so the fix-site fallback applied: the fix site still carried the absolute prefix on lines 16 and 24, and the fix was implemented. Gate 6a (`scripts/check-machine-paths.sh`, reached through `scripts/run-gates.sh` from `commands.test`) was not run in this unit and is deferred to the Run gates phase. The after-state rests on `grep -c "$HOME"` over `review_1.md` returning `0`, and on the selected tree guard `test/no-container-home-paths.test.mjs` passing (`# pass 1`, `# fail 0`).
