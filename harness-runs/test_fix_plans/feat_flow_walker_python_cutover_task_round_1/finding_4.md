### 4. Gate 6a: the round-0 architecture review names a machine path

**File:** `harness-runs/architecture_reviews/feat_flow_walker_python_cutover/review_0.md` — the Must Fix item beginning "3. **`task_12_plan.md` — the Verification runs gate 6a's script**", in its citation "/plugin/instructions/unit_loop_core.md` → `## The test-run rule`" (line 23, navigation hint only).

**Failing test:** none — 6a no machine paths (`scripts/check-machine-paths.sh`, run by `scripts/run-gates.sh` as gate 6a)

**Class:** Broken contract
**Failure:** If the running program runs gate 6a (`scripts/check-machine-paths.sh`), then it prints `./harness-runs/architecture_reviews/feat_flow_walker_python_cutover/review_0.md:23:3. **`task_12_plan.md` — the Verification runs gate 6a's script** (`<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → …` and the gate fails, because a committed file names a location under the home directory of the machine that wrote it.

**Failure as logged** (gate 6a, first round; the home directory rewritten to `<home>`):

```
FAIL  6a no machine paths (printed output, which is the finding, 2 s)
      ./harness-runs/architecture_reviews/feat_flow_walker_python_cutover/review_0.md:23:3. **`task_12_plan.md` — the Verification runs gate 6a's script** (`<home>/Work/devscene/plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 4: *"No `**Verification:**` bullet … names `<test_cmd>`, a gate script, or a test file the unit neither creates nor edits"*)
```

**Diagnosis.** Class: first round (no earlier log). `scripts/check-machine-paths.sh` greps the tree for the running user's `$HOME`, excluding only `node_modules`, `dist`, `.git`, `test_run_logs`, `scratch`, Python caches, `harness-runs/clarifications/*/` and the walker state — `harness-runs/architecture_reviews/` is in scope. The round-0 architecture review (committed in `1405ecc1`, "Plan round 0 for feat_flow_walker_python_cutover") cites `unit_loop_core.md` by the absolute path the plugin root resolved to on this machine, rather than by the `${CLAUDE_PLUGIN_ROOT}`-rooted form the plugin corpus uses. `.claude/context/conventions.md` → `## The testing bar` states: "The self-containment gate binds every commit: nothing in this tree may name a location on the machine that wrote it". A grep of `harness-runs/architecture_reviews/feat_flow_walker_python_cutover/` finds this one line and no other; gate 6a printed no other hit in the tree.

**Fix** (one-line text edit; no code change):

- [ ] In `harness-runs/architecture_reviews/feat_flow_walker_python_cutover/review_0.md`, in the Must Fix item 3 line, replace the absolute path prefix that precedes `/plugin/instructions/unit_loop_core.md` (the home directory followed by `/Work/devscene`) so the citation reads `` `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` ``. Change nothing else on the line or in the file — the review is a point-in-time record, and only the machine-local prefix is wrong.
- [ ] After the edit, `grep -n` for the home directory over `harness-runs/architecture_reviews/feat_flow_walker_python_cutover/` should print nothing (a plain grep, not the gate script).

**Deviations from plan:** Row-`G.4` fix-site fallback: the finding names no test file (`none — 6a no machine paths`), so gate 6a (`scripts/check-machine-paths.sh`) was not run; a gate script is never run by a unit, and the Run gates phase's `commands.test` run verifies it. Before the edit, the fix site still carried the home-directory prefix (`grep -n "$HOME"` printed line 23), so the fix was implemented. The after-evidence is `grep -rn "$HOME"` over `harness-runs/architecture_reviews/feat_flow_walker_python_cutover/`, which printed nothing (exit 1), and the whole-tree `bash scripts/typecheck.sh` ending `PASS: typecheck`.
