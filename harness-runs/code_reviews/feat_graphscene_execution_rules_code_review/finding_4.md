### 4. A run cancelled by `execute_set`'s own cancellation or by a sibling's defect takes a `seq` but writes no `Launch` row, and nothing says so

**File:** `graphscene/src/graphscene/engine/set_execution.py` (`_run_pass`): "except BaseException:"

`_run_pass` takes `counter.increment()` as each dispatch's `seq` before launching it. It writes that dispatch's `Launch` row only when the run's result is collected. When `execute_set` is cancelled, or another run raises, the `except BaseException:` arm cancels the outstanding runs and re-raises, so those runs return no `NodeResult` and write no row. The branch exercises both paths: `graphscene/tests/engine/test_set_execution.py` → `test_cancelling_execute_set_cancels_its_runs_and_re_raises` and `test_a_defect_out_of_run_cancels_the_outstanding_runs_and_propagates`. Yet `graphscene/src/graphscene/model/run_control.py` → `LaunchSink` says it *"Receives one `Launch` row per session launched"*, and `set_execution.py`'s `Deliberately not covered:` list does not name the exception.

The reader who gets this wrong is the host implementer under #484. Such a host keeps a persistent dispatch counter (the harness's `.dispatch_counter`) and an observation table built from `LaunchSink`. After a cancelled set, the counter is ahead of the rows. Trusting the documented one-row-per-launch rule, the host reports a missing observation as lost data rather than as a cancelled launch. A `Launch` needs a `NodeResult` and a cancelled run has none, so writing a row is not the fix here. Documenting the gap is.

**Fix.** In `graphscene/src/graphscene/engine/set_execution.py`'s module docstring, append to the `Deliberately not covered:` list, after "- Usage: the host's, through its executor's usage sink.":

```
- A `Launch` row for a run cancelled because `execute_set` was cancelled or another run raised:
  such a run has taken its `seq` from `DispatchCounter.increment` but returns no `NodeResult`,
  so it writes no row.
```

In `graphscene/src/graphscene/model/run_control.py`, change the `LaunchSink` docstring from

```python
    """Receives one `Launch` row per session launched."""
```

to

```python
    """Receives one `Launch` row per session launched whose run returned a result."""
```

The change is docstring-only and edits no test file, so it needs no test run of its own.
