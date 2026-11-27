### 5. The held-session cases never check the log for a false total-run-timeout line

**File:** `devscene-flow-host/tests/test_planning_driver_walk.py` (`test_a_session_the_driver_cannot_take_is_held_while_its_siblings_finish_then_parks`) — `assert not (drive.repo / "devscene/clarifications/feat_x/question_2.md").exists()`

**Problem.** `host/node_sessions.py` → `NodeSessions._pair` now pairs a `Launch` whose result is `Failed("infra", …)` with the node's oldest pending `Completed` usage. That is the transformation `PlanningExecutor` makes after the usage was recorded, for example `PASS carries no findings_file` or `the round file was refused: no single verdict line`. A `Launch` with no usage record is narrated as `no usage record for <node> (total-run timeout)`. `test_node_sessions.py` → `test_a_completed_usage_pairs_with_the_infra_failure_the_planning_executor_made` covers that pairing on its own. The end-to-end held-session case never reads `drive.log` for that line, though, so a regression in how the driver feeds `NodeSessions` would go unnoticed. That case is parametrized over `schema`, `no-findings-file`, `no-init` and `no-verdict-line`, and the last two of those are the refused and missing round-file paths.

The planning run sets `run_timeout_seconds=None` (`host/run_control.py` → `planning_limits`), so no case in this suite has a real total-run timeout. The line must never appear.

**Fix:**

- [ ] At the end of `test_a_session_the_driver_cannot_take_is_held_while_its_siblings_finish_then_parks`, after the existing `question_2.md` assertion, add an assertion that holds for every parametrized id:

  ```python
  timeouts = [line for line in drive.log if "no usage record for" in line]
  assert timeouts == [], _show(drive)
  ```

  `drive.log` is the run log's lines (`_drive` → `log=log.read_text(...).splitlines()`). Matching the substring `no usage record for`, rather than the whole `[plan-drive] no usage record for <node> (total-run timeout)` literal, keeps a prefix or node-name change from making the assertion pass vacuously.
- [ ] Add one sentence to the module docstring's rule paragraph: a held session's `Launch` is paired with its usage record, so the log carries no `no usage record for <node> (total-run timeout)` line.
- This test file is the unit's own edited test file. Run it under that rule.
