### 3. `execution.py` still says the run deadline is the caller's and #484's, though `execute_set` now applies it

**File:** `graphscene/src/graphscene/model/execution.py` (module docstring): "The deadline around a node's coroutine is the caller's" and "The run loop and its deadline: #484."

This branch moved the stall deadline into the engine. `graphscene/src/graphscene/engine/set_execution.py` → `_run` wraps each `executor.run` in `asyncio.timeout(stall_seconds)` and settles an expiry as `Failed("infra", "stalled: …")`. Two lines of the `execution.py` docstring still give that deadline to someone else:

- `The rule:`, the `run` is cancellable bullet: *"The deadline around a node's coroutine is the caller's to set and to report (#484)."*
- `Deliberately not covered:`: *"The run loop and its deadline: #484."*

The reader who gets this wrong is the implementer of #484's run loop. That person reads the `Executor` protocol's module to learn what is left to build, concludes the deadline is theirs, and wraps `execute_set`'s runs in a second timeout. The engine's own `stall_seconds` timeout then reports a different stall than the one #484 adds.

**Fix.** In `graphscene/src/graphscene/model/execution.py`'s module docstring, replace

```
  never turns cancellation into a result. The deadline around a node's coroutine is the caller's
  to set and to report (#484).
```

with

```
  never turns cancellation into a result. The deadline around a node's run is
  `ExecutionLimits.stall_seconds`, set by the host and applied by
  `graphscene.engine.set_execution`, which settles an expiry as an `infra` failure.
```

and replace

```
- The run loop and its deadline: #484. The stall deadline's result is recorded as `infra` by
  `graphscene.engine.set_execution`.
```

with

```
- The run loop: #484.
```

The change is docstring-only and edits no test file, so it needs no test run of its own.
