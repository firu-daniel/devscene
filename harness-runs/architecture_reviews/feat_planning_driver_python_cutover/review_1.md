# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix
- **`task_1_plan.md` / `task_2_plan.md`: the watcher launches a flow-host console script without going through `flow-walker.sh`.** Carried over from round 0, unchanged. `.claude/context/conventions.md` → `## The layers` says *"Every caller launches it through `flow-walker.sh`"*, and `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` repeats it. The substance of the rule still holds: one `uv` launch, now `hr_flow_host_exec`, the provisioning refusal, and no bash fallback. The plan records the sentences it falsifies as `stale-rule` entries (scope register rows 2–3), which `plugin/agents/task-plan-writer.md` → the conventions-document prohibition requires. Make sure those entries actually reach a maintainer in this run's return.
- **`task_10_plan.md` / `task_12_plan.md`: `RecordError` is used for a host-side file condition.** `RecordError` is *"the one anticipated failure of reading a repository record"* (`.claude/context/devscene-flow-host.md` → `## Errors`). Two plan items use it anyway:
  - Task 10 raises it for a park path that is already occupied, which is a write collision.
  - Task 12 raises it for a corrupt `.dispatch_counter`.

  The host's existing stores raise `ValueError` naming the file instead (`host/refusals.py`, `host/revision_findings.py`). Either follow that, or state in each module docstring why `RecordError` is reused.
- **`task_16_plan.md`: the missing-ledger check builds its own `RecordError` in `host`.** It also hand-spells the path `'<stateDir>/flow_progress/<branch>_progress.md'`. `records/ledger.py` → `ledger_path` owns that path. After Task 10, `read_run_mode_entries` also owns a missing-ledger message: `the flow-progress ledger '{path}' does not exist`. That makes two spellings. Build the path with `ledger_path`, or move the check beside it.
- **`task_16_plan.md` / `task_18_plan.md`: the commit-wrapper path is built in two layers.** `host/planning_run.py` builds `main_repo / read_config(main_repo).scripts_dir / "commit-on-branch.sh"` for `PlanningHooks`. Task 18 has `commands/planning_driver.py` build *"the same"* path again for `act_on_exit`, so the literal `commit-on-branch.sh` exists in two modules, and `host/commit_points.py` owns no constant for it (`.claude/context/conventions.md` → *"A responsibility that already has a home does not get a second one"*). Either have `PlanningOutcome` carry the wrapper Task 16 built, or give the composition one function in `host`.
- **`task_3_plan.md`: *"Record where each behaviour goes, in the commit body's record line."*** This was moved here from Task 4 and is still not something the implementer can follow. `commit-on-branch.sh --unit` builds the body in one of three fixed forms from the `**Cause:**` line (`.claude/context/conventions.md` → `## Commit-message policy`). Put the behaviour-to-task map in the task file instead. This is outside the architecture lens and is noted in passing.

## Nice to Have
- `task_13_plan.md`: `NodeSessions.record` serves both `UsageSink.record(usage)` and `LaunchSink.record(launch)`. State that it takes `SessionUsage | Launch` and dispatches on type, so it visibly fits both protocols.
- `task_9_plan.md`: *"Extend the module docstring's rule"* for `max_question_index` should name `hr_max_question_index` as the bash reader it reads as. The record-reader row of `.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here` asks for that name, and the Goal gives it but the Work bullet does not.
