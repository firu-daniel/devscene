### 3. Compose the main checkout's commit-wrapper path in one place, not in `commands` and `host` both

**Sites:**
- `devscene-flow-host/src/devscene_flow_host/commands/planning_driver.py` → `_run`, the substring `wrapper = main_repo / read_config(main_repo).scripts_dir / COMMIT_WRAPPER`.
- `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` → `run_planning`, the substring `wrapper = request.main_repo / read_config(request.main_repo).scripts_dir / COMMIT_WRAPPER`.

**The problem.**

`.claude/context/conventions.md` → `### Where a new responsibility goes` says *"A responsibility that already has a home does not get a second one"* and *"Before adding a copy of anything, grep for it"*. Resolving the main checkout's `<scriptsDir>/commit-on-branch.sh` is composed twice:

- once in `commands`, for `act_on_exit` and `Observations.flush`;
- once in `host`, for `PlanningHooks`.

Each copy re-reads `devscene.config.json`. The `commands` layer even imports `COMMIT_WRAPPER` from `host/planning_run.py` to do it.

If the two copies drift (a changed wrapper name or directory rule in one), the round commits and the partial and observation commits would go through different wrappers. No test pins that the two are equal.

`.claude/context/devscene-flow-host.md` → `## The internal layers` gives the commit points to `host` (`host/commit_points.py`). `commands` owns only the command line, the graph file and the exit status.

**The fix.** Give the path one owner in `host`:

1. Add `commit_wrapper_path(main_repo: Path) -> Path` to `devscene-flow-host/src/devscene_flow_host/host/commit_points.py`, beside `commit_artifact`, and move `COMMIT_WRAPPER` there as a `Final`.
2. Call it from `host/planning_run.py` → `run_planning`.
3. Either expose the resolved path on `PlanningOutcome` for `commands/planning_driver.py` to pass on, or have `commands/planning_driver.py` → `_run` call the same function. Delete the inline composition in `_run`.
4. Update the `COMMIT_WRAPPER` import in `commands/planning_driver.py` and in any test that imports it from `host/planning_run.py`.
