### 4. No test-only backoff override, so the end-to-end suites sleep through real 60-second backoffs

**File:** `devscene-flow-host/src/devscene_flow_host/host/run_control.py` (`BACKOFF_SECONDS`, `planning_limits`) — `backoff_seconds=BACKOFF_SECONDS,`

**Problem.** `planning_limits` passes the fixed `BACKOFF_SECONDS` (60.0) into GraphScene's `ExecutionLimits.backoff_seconds`. `graphscene/src/graphscene/engine/set_execution.py` → `execute_set` then sleeps that long before every re-dispatch pass, whether the pass follows an infrastructure retry or an undelivered re-dispatch. The retired pilot read the optional `PD_BACKOFF_SECS`, with 60 as both default and ceiling. Its `pd_backoff` (`cli/templates/scripts/lib/planning-driver-lib.sh`, read at `613de204^`) did this:

```bash
PD_V="${PD_BACKOFF_SECS:-60}"
case "$PD_V" in '' | *[!0-9]*) PD_V=60 ;; esac
[ "$PD_V" -le 60 ] || PD_V=60
```

The Python host has no override. As a result, every retry case in `test_planning_driver_walk.py` and `test_planning_driver_control.py` sleeps through real 60-second backoffs. Both suites' docstrings say so: *"no case shortens them"*.

**Fix:**

- [ ] In `host/run_control.py`:
  - Keep `BACKOFF_SECONDS: Final = 60.0` as the default and ceiling.
  - Add `BACKOFF_ENV: Final = "PD_BACKOFF_SECS"`.
  - Add a function that reads the value **at call time**, never at import time, so a test's `monkeypatch.setenv` before `main` takes effect:

  ```python
  _DECIMAL: Final = re.compile("[0-9]+")

  def backoff_seconds(environ: Mapping[str, str] = os.environ) -> float:
      raw = environ.get(BACKOFF_ENV, "")
      if _DECIMAL.fullmatch(raw) is None:
          return BACKOFF_SECONDS
      return min(float(int(raw, 10)), BACKOFF_SECONDS)
  ```

  This mirrors `pd_backoff`. Unset, empty or non-decimal gives 60, a decimal above 60 is capped to 60, and `0` means no backoff. `planning_limits` passes `backoff_seconds=backoff_seconds()`. Real runs never set the variable, so they keep 60 s.
- [ ] Update the module docstring's rule: `planning_limits` reads the backoff from `PD_BACKOFF_SECS`, a test-only override with 60 as default and ceiling, read as `pd_backoff` read it. Also say why it is an environment value and not a `devscene.config.json` key: it exists only so test suites need not sleep.
- [ ] In `devscene-flow-host/tests/test_run_control.py`, add cases that pass an explicit mapping to `backoff_seconds`. Each expected value is a literal:
  - absent → `60.0`
  - `"0"` → `0.0`
  - `"5"` → `5.0`
  - `"61"` → `60.0`
  - `"-1"` → `60.0`
  - `"1.5"` → `60.0`
  - `""` → `60.0`

  Add one case asserting that `planning_limits(7).backoff_seconds == 0.0` under `monkeypatch.setenv("PD_BACKOFF_SECS", "0")`.
- [ ] In `devscene-flow-host/tests/test_planning_driver_walk.py` and `devscene-flow-host/tests/test_planning_driver_control.py`, set `PD_BACKOFF_SECS` to `"0"` for every case. Each suite already has an autouse fixture (`_isolated_git`) that calls `monkeypatch.setenv`. Add `monkeypatch.setenv("PD_BACKOFF_SECS", "0")` there, or add a sibling autouse fixture.
- [ ] Rewrite the docstring sentences that say no case shortens the backoffs:
  - `test_planning_driver_walk.py`: *"A held case spends GraphScene's two 60-second retry backoffs, as the run does: no case shortens them."*
  - `test_planning_driver_control.py`: *"The retried cases spend GraphScene's 60-second retry backoffs, as the run does: no case shortens them."*

  Each becomes a statement that the suite sets `PD_BACKOFF_SECS=0`, so the retries go out with no backoff, and that the 60-second default and ceiling are held by `tests/test_run_control.py`. Leave the control suite's *"the inactivity limit is `ClaudeExecutor`'s fixed constant, which this suite does not shorten"* bullet as it is. It is about the stall limit, not the backoff.
- [ ] `docs/watcher.md` → **What parks or pauses the driver, and what it retries.** says *"dispatches the node alone again after 60 seconds"*. That is still true of a real run, so leave it unchanged.
- The edited test files are the unit's own. Run them under that rule.
  - **Deviations from plan:** `test_run_control.py` → `test_planning_limits_fix_every_limit_but_the_cap` now calls `monkeypatch.delenv("PD_BACKOFF_SECS", raising=False)` first. Without it, an outer environment that sets the variable would break that test's literal `60.0`.
