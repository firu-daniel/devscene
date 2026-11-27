### 1. `NodeSessions` never pairs a session whose `Completed` result `PlanningExecutor` turned into `Failed("infra")`, so its row is blanked and the log claims a total-run timeout

**File:** `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py` (`NodeSessions._pair`) — "if usage.result == launch.result:"
**Class:** Wrong behaviour
**Failure:** If a round gate's session returns `PASS` without a `findings_file`, `PlanningExecutor._check` returns `Failed("infra", "PASS carries no findings_file")`, but the usage record `ClaudeExecutor.run` handed the sink carries the original `Completed`. `NodeSessions._record_launch` then finds no pending usage with an equal result. The run log gets `[plan-drive] no usage record for architecture_review (total-run timeout)` although the planning run sets no total-run timeout (`host/run_control.py` → `planning_limits`, `run_timeout_seconds=None`), and the session-table row in the observations file reads `- architecture_review architecture-reviewer 1/3 failed - -`, with no seq, duration or cost.

**The problem.** `host/planning_run.py` → `run_planning` composes the executor as `_RoundRecorder(PlanningExecutor(ClaudeExecutor(…, usage_sink=sessions)))`, and `sessions` is also GraphScene's `LaunchSink`. The order is:

1. `ClaudeExecutor.run` calls `self._usage_sink.record(usage)` with `usage.result` set to the result it judged (`host/claude_executor.py` → `self._usage_sink.record(usage)`).
2. `PlanningExecutor.run` (`host/planning_executor.py` → `_check`) may then replace a verdict `Completed` with `Failed("infra", "<outcome> carries no findings_file")` or `Failed("infra", "the round file was refused: <problem>")`.
3. GraphScene writes its `Launch` row with that replaced result.

`NodeSessions._pair` accepts only a pending usage of the node whose `result` equals `launch.result`. A `Completed` never equals a `Failed`, so the pairing fails whenever `PlanningExecutor` intervenes. These are the held cases `tests/test_planning_driver_walk.py` → `test_a_session_the_driver_cannot_take_is_held_while_its_siblings_finish_then_parks` drives (`no-findings-file`, `no-verdict-line`). That suite asserts on the park, not on the log or the rows, so it does not see the defect. Three wrong outputs follow:

- **The log.** The `no usage record for <node> (total-run timeout)` line names a cause that did not happen.
- **The session table and its observations.** The row carries `-` for seq, duration and cost, and the evidence reads `#- <node> (<agent>)`. The session's permission-denial observation is never added, because `paired` is `None`.
- **The pending list.** The unmatched usage stays in `self._pending[node]`. A later attempt that is accepted, with a `Completed` equal to the leaked one, pairs with the oldest of them. Its row then carries the earlier attempt's seq, duration and cost, and its own usage leaks in turn.

**Probe (executed).** `bash scripts/python-service.sh --package devscene-flow-host probe harness-runs/scratch/branch_review_pairing.py` built one `NodeSessions`, recorded a `SessionUsage` for `architecture_review` carrying `Completed("PASS", None)`, then recorded `Launch(1, "architecture_review", "architecture-reviewer", 1, 3, Failed("infra", "PASS carries no findings_file"))`. It printed:

```text
rows: ('- architecture_review architecture-reviewer 1/3 failed - -',)
narrated: ['no usage record for architecture_review (total-run timeout)']
```

**Fix.** `PlanningExecutor` makes exactly one transformation, a `Completed` into a `Failed` whose `failure` is `"infra"`, so pair that case too. A genuine mismatch between two different `Completed` results must stay unpaired, as `tests/test_node_sessions.py` → `test_a_mismatched_result_is_not_paired` pins.

1. In `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py`, replace `_pair` with:

   ```python
   def _pair(self, launch: Launch) -> tuple[int, SessionUsage] | None:
       pending = self._pending.get(launch.node, [])
       for index, (_, usage) in enumerate(pending):
           if usage.result == launch.result:
               return pending.pop(index)
       if isinstance(launch.result, Failed) and launch.result.failure == "infra":
           for index, (_, usage) in enumerate(pending):
               if isinstance(usage.result, Completed):
                   return pending.pop(index)
       return None
   ```

2. In the same module's docstring, replace the sentence that opens *"`record(launch)` pairs the `Launch` with the oldest pending usage of `launch.node` whose `result` equals `launch.result`, and appends one row"* so that it reads:

   > `record(launch)` pairs the `Launch` with the oldest pending usage of `launch.node` whose `result` equals `launch.result`; failing that, a `Launch` whose result is `Failed("infra", …)` pairs with the oldest pending usage of that node whose result is a `Completed`, the one transformation `host/planning_executor.py` → `PlanningExecutor` makes after the usage was recorded. It then appends one row

   Keep the rest of that sentence (the row's shape) unchanged.

3. In `devscene-flow-host/tests/test_node_sessions.py`, add this case directly after `test_a_mismatched_result_is_not_paired`. The fifth word of the row is `result.kind` for a `Failed`, which the suite's existing timeout case writes as `failed` (`test_a_timeout_launch_without_usage_gives_its_row_and_no_exception`):

   ```python
   def test_a_completed_usage_pairs_with_the_infra_failure_the_planning_executor_made(
       tmp_path: Path,
   ) -> None:
       sessions, _, narrated = _sessions(tmp_path)
       sessions.record(_usage("plan_review", Completed("PASS")))
       refused = Failed("infra", "PASS carries no findings_file")
       sessions.record(Launch(1, "plan_review", "plan_review-agent", 1, 3, refused))
       assert sessions.rows == ("1 plan_review plan_review-agent 1/3 failed 12s 0.5",)
       assert narrated == []
   ```

   In the same file's module docstring, change *"pairs a `Launch` only with a pending usage of its node carrying an equal `result`"* to *"pairs a `Launch` with a pending usage of its node carrying an equal `result`, or, for a `Launch` whose result is `Failed("infra", …)`, with one carrying a `Completed`"*.

This fix edits one test file, `devscene-flow-host/tests/test_node_sessions.py`, and that is the only test file it runs: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_node_sessions.py`.
