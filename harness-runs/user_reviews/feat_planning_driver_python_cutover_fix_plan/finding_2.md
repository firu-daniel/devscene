### 2. The undelivered re-dispatch observation and its narration line were dropped

**File:** `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py` (`NodeSessions._observe`) — `if not isinstance(result, Failed) or result.failure == "undelivered":`. The GraphScene half is at `graphscene/src/graphscene/model/run_control.py` (`Launch`) — `max_attempts: int`, and at `graphscene/src/graphscene/engine/set_execution.py` (`_run_pass`) — `Launch(seq, dispatch.node, dispatch.agent, attempt, limits.max_attempts, result)`.

**Problem.** The retired pilot's `pd_undelivered` (`cli/templates/scripts/lib/planning-driver-lib.sh`, read at `613de204^`) added this observation on every undelivered set short of the third:

```bash
pd_observe flow-efficiency "An undelivered planning dispatch was re-dispatched" \
  "nodes: $PD_UNDELIV_NODES; consecutive undelivered sets: $PD_STRIKES; reason: $PD_UNDELIV_REASON" "one re-dispatch per node"
```

It also logged `undelivered: re-dispatching <nodes> at once`, or `undelivered again: backing off <n>s before the re-dispatch`. In `NodeSessions`, `_observe` returns early on `Failed("undelivered", …)`, and `_track_attempts` does the same. So a run records no trace of an undelivered re-dispatch until the third consecutive one self-pauses (`host/run_exits.py` → `UNDELIVERED_PROBLEM`).

**The consecutive-set count is not derivable from the `Launch` rows the host sees.** GraphScene's `UndeliveredBreaker` counts passes, not sessions:

- A pass with any `Redispatch` adds a strike.
- A pass whose every node was recorded resets the strikes to 0.
- A pass with only a `Retry` leaves the strikes unchanged.

These rules are in `set_execution.py` → `execute_set`. A `Launch` carries `seq, node, agent, attempt, max_attempts, result` and nothing that marks where a pass ends. For example, the last launch of a delivered pass and the first launch of the next set's pass arrive back to back with no boundary between them, so the host cannot tell whether a later undelivered launch extends a run of strikes or follows a reset. The breaker also lives inside `start_run` / `continue_run`, and the host never sees it.

**Smallest generic GraphScene addition: one defaulted field on `Launch`.** `undelivered_strikes: int = 0` is the strikes the run's `UndeliveredBreaker` held when this launch's pass was cleared, meaning the consecutive passes before it that had an undelivered result. Any host can use it, and it names nothing about planning. For an undelivered launch, `undelivered_strikes + 1` is the pilot's `PD_STRIKES`. The default keeps every existing positional `Launch(...)` construction valid in both packages' tests.

**Fix:**

GraphScene, `graphscene` layer:

- [ ] `graphscene/src/graphscene/model/run_control.py` → `Launch`: append the field `undelivered_strikes: int = 0` after `result`. Add a docstring: *"`undelivered_strikes` is the `UndeliveredBreaker`'s strikes when this launch's pass was cleared — the consecutive passes before it that had an `undelivered` result; 0 for a host that drives `execute_set` with a fresh breaker."*
- [ ] `graphscene/src/graphscene/engine/set_execution.py`:
  - `execute_set` passes `breaker.strikes` into `_run_pass` as a new parameter, read before the pass runs. That is after `clear_set` and before `_run_pass`, so every launch of one pass carries the same value.
  - `_run_pass` builds each row as `Launch(seq, dispatch.node, dispatch.agent, attempt, limits.max_attempts, result, strikes)`.
  - Add one bullet to the module docstring's rule: each `Launch` row carries the breaker's strikes as they stood when its pass was cleared.
- [ ] `graphscene/tests/engine/test_set_execution.py`: add a case on one breaker, scripted through `StubExecutor`. Node `a` returns `Failed("undelivered", "x")` on its first run and `Completed(...)` on its second, so the recorded `Launch` rows carry `undelivered_strikes` `0` then `1`. Then run a second `execute_set` with the same breaker, whose single pass delivers, and check that its row carries `0`. All expected values are literals. Reuse the file's existing fixtures for signals, counter, sink and limits, with `backoff_seconds=0`.
- No change to `graphscene/README.md` or `.claude/context/graphscene.md` is needed: neither lists `Launch`'s fields.

Flow host, `devscene-flow-host` layer:

- [ ] `host/node_sessions.py` → `NodeSessions.__init__`: add the keyword arguments `backoff_seconds: float` and `undelivered_limit: int`, and keep both.
- [ ] `host/planning_run.py`: compute `limits = planning_limits(read_max_total_dispatches(plugin_dir))` **before** `sessions = NodeSessions(...)`, then pass `backoff_seconds=limits.backoff_seconds` and `undelivered_limit=UNDELIVERED_LIMIT` (already imported there).
- [ ] `NodeSessions._observe`: keep the permission-denial check first. Then, for `Failed("undelivered", reason)`, replace the bare `return` with the following:

  ```python
  count = launch.undelivered_strikes + 1
  if count >= self._undelivered_limit:
      return  # the set halts; run_exits records the self-pause (UNDELIVERED_PROBLEM)
  self._observations.add(
      "flow-efficiency",
      "An undelivered planning dispatch was re-dispatched",
      f"nodes: {launch.node}; consecutive undelivered sets: {count}; reason: {result.reason}",
      "one re-dispatch per node",
  )
  if self._backoff_seconds > 0:
      self._narrate(
          f"undelivered: backing off {self._backoff_seconds:g}s before re-dispatching {launch.node}"
      )
  else:
      self._narrate(f"undelivered: re-dispatching {launch.node} at once")
  return
  ```

  The title, category, evidence fields and cost text are the pilot's. The rule for skipping the limit-reaching strike is also the pilot's: its `pd_undelivered` returned at `PD_STRIKES -ge 3` before observing. The narration goes through `narrate`, which adds the `[plan-drive] ` prefix (`commands/planning_driver.py` → `NARRATION_PREFIX`). One deliberate difference: the observation is written once per undelivered `Launch`, so a pass with two undelivered nodes gives two entries with one node each, where the pilot gave one entry naming both. GraphScene backs off before every re-dispatch pass, not only the second, so the narration states the backoff whenever it is above 0.
- [ ] `_track_attempts` keeps its early return for `undelivered`, because an undelivered launch must not touch the attempt log. Update the module docstring's per-session observations bullet to add the undelivered re-dispatch observation and its narration, and state that the count comes from `Launch.undelivered_strikes`.
- [ ] `devscene-flow-host/tests/test_node_sessions.py`:
  - Pass the two new keyword arguments in `_sessions`.
  - Add cases, all with literal expectations: an undelivered `Launch` with `undelivered_strikes=0` and backoff 60 gives the observation `("flow-efficiency", "An undelivered planning dispatch was re-dispatched", "nodes: plan_review; consecutive undelivered sets: 1; reason: no result event", "one re-dispatch per node")` and the narration `undelivered: backing off 60s before re-dispatching plan_review`.
  - The same `Launch` with backoff 0 narrates `undelivered: re-dispatching plan_review at once`.
  - `undelivered_strikes=2` with limit 3 gives no observation and no narration.
- [ ] `devscene-flow-host/tests/test_planning_driver_control.py`: add `test_an_undelivered_set_is_re_dispatched_and_observed`. `task-plan-reviewer`'s first call takes `{"drop_result": True}` and its second call returns normally, so the drive hands off with status `0`. Assert the following:
  - The observations file holds a block starting `An undelivered planning dispatch was re-dispatched\n` that carries `nodes: plan_review; consecutive undelivered sets: 1; reason: no result event` and the cost `one re-dispatch per node`.
  - `drive.log` contains `[plan-drive] undelivered: re-dispatching plan_review at once`. That holds because Finding 4 sets `PD_BACKOFF_SECS=0` for this suite.

  Shape it on `test_an_infrastructure_failure_is_re_dispatched_alone_and_observed`. Also update the module docstring's rule paragraph to name the observation.
- The edited test files are the unit's own. Run them under that rule.
