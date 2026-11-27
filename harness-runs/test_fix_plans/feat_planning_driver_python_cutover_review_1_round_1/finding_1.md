### 1. Replace the machine path in the user-review fix plan's `## Source observations` lead

**Site:** `harness-runs/user_reviews/feat_planning_driver_python_cutover_fix_plan.md`, under `## Source observations`, in the lead sentence containing `placed between the markers that` and `untrusted_input.md`. The navigation hint is line 62.

**Failing test:** none — test (gate 6a, `scripts/check-machine-paths.sh`, run by `scripts/run-gates.sh`)

**Class:** Broken contract

**Failure:** If the test gate runs gate 6a (`6a no machine paths`) over this tree, then it prints `./harness-runs/user_reviews/feat_planning_driver_python_cutover_fix_plan.md:62:… placed between the markers that `<home>/Work/devscene/plugin/instructions/untrusted_input.md` → `## The markers` names. …` and the gate fails. The tracked file names a location on the machine that wrote it, which breaks the self-containment gate that `.claude/context/conventions.md` says binds every commit.

**Quoted failure (log, home path rewritten):**

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/user_reviews/feat_planning_driver_python_cutover_fix_plan.md:62:This is a verbatim copy of the source user review, `harness-runs/user_reviews/feat_planning_driver_python_cutover_review.md`, placed between the markers that `<home>/Work/devscene/plugin/instructions/untrusted_input.md` → `## The markers` names. It keeps this fix plan self-contained: the implement flow does NOT re-read the user-review file.
```

**Diagnosis:** New this round. `scripts/check-machine-paths.sh` runs `grep -rn "$HOME"` over the checkout and fails the gate on any output. The user-review fix plan is tracked (`git ls-files` lists it). When the plan writer resolved the `${CLAUDE_PLUGIN_ROOT}` citation, it wrote the plugin root as an absolute path under the home directory. The current tree still has that text. A repo-wide search for the home directory, using the same exclusions as the gate, finds no other file. That makes this sentence the only hit. Other fix plans under `harness-runs/user_reviews/` cite the same document as `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md`.

**Fix:**

- [ ] In `harness-runs/user_reviews/feat_planning_driver_python_cutover_fix_plan.md`, in the `## Source observations` lead sentence, replace the absolute path (`<home>/Work/devscene/plugin/instructions/untrusted_input.md`, with the home directory spelled out literally) with `${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md`. Keep the backticks and the trailing ` → `## The markers` names.` unchanged.
- [ ] Change nothing between the `=== BEGIN UNTRUSTED DATA` and `=== END UNTRUSTED DATA` markers. That block is a verbatim copy and holds no machine path.
- [ ] Do not edit `scripts/check-machine-paths.sh` and do not add an exclusion for `harness-runs/user_reviews/`. The gate is correct. The artifact is wrong.
