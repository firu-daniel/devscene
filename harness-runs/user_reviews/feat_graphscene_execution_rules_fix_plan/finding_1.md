### 1. `ExecutionLimits.stall_seconds` is a total run timeout, not a stall timeout

**File:** `graphscene/src/graphscene/engine/set_execution.py` (`_run`) — "deadline = asyncio.timeout(stall_seconds)"; also `graphscene/src/graphscene/model/run_control.py` (`ExecutionLimits`) — "stall_seconds: float | None = None"

**The problem.** Verified in the current tree. `_run` wraps the whole `await executor.run(dispatch)` in `asyncio.timeout(stall_seconds)`. On expiry it returns `Failed("infra", f"stalled: no result within {stall_seconds}s")`. The value therefore bounds a node's **total** run time. A stall in the pilot sense is something else. `PD_NODE_STALL_SECS` is an **inactivity** limit: `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_run_set` kills a session only when its stream file has been silent that long ("its stream has been silent ${age}s; killing the session"). GraphScene cannot see a session's stream, and only the executor can. So an inactivity stall is detected by the executor and returned as `Failed("infra", …)`. `graphscene/src/graphscene/model/execution.py` already says so ("a stall the executor detected itself"). Calling the engine's deadline a stall invites a host to map its stall setting onto it. A host that did so would cancel long but healthy sessions.

**Grade: Should Fix.** The defect is real, but no host passes this value yet: the run loop is #484 and `devscene-flow-host` does not name `ExecutionLimits`. No consumer step that fails today can be named, so `finding_grades.md` does not allow a Must Fix.

**Fix.** Rename the field and every place that calls this value a stall, in one unit:

- [ ] `graphscene/src/graphscene/model/run_control.py` → `ExecutionLimits`: rename `stall_seconds` to `run_timeout_seconds`. Keep its default `None` (no limit) and its position as the last field. Make the `__post_init__` check `self.run_timeout_seconds` and call `_refuse("run_timeout_seconds", "> 0", self.run_timeout_seconds)`, so the message reads `ExecutionLimits: run_timeout_seconds must be > 0, got <value>`.
- [ ] `graphscene/src/graphscene/engine/set_execution.py`:
  - `_run`: rename the parameter to `run_timeout_seconds`. Change the expiry result to `Failed("infra", f"timed out: no result within {run_timeout_seconds}s")`.
  - `_run_pass`: pass `limits.run_timeout_seconds`.
  - Module docstring, the bullet "With `ExecutionLimits.stall_seconds` set, …": rewrite it to say that with `ExecutionLimits.run_timeout_seconds` set, each run's total time is under that deadline. A run that passes the deadline is cancelled and becomes `Failed("infra", "timed out: no result within <run_timeout_seconds>s")`. A timeout is an `infra` failure.
  - Under *"Deliberately not covered:"*, add one bullet: detecting a stalled (inactive) session is the executor's, since only the executor sees the session's activity, and it returns that stall as `Failed("infra", …)` (#421).
- [ ] `graphscene/src/graphscene/model/execution.py`, module docstring, the `run` is cancellable bullet ("The deadline around a node's run is `ExecutionLimits.stall_seconds`, …"):
  - Name `ExecutionLimits.run_timeout_seconds` as the limit on a run's **total** time, set by the host and applied by `graphscene.engine.set_execution`, which settles an expiry as an `infra` failure.
  - State that this limit is not an inactivity timeout: a stall (a session gone silent) is the executor's to detect and return as `Failed("infra", …)`.
  - Keep the `infra` class bullet's "a stall the executor detected itself" as it is.
- [ ] `graphscene/README.md` → `## What it is`, the paragraph that reads "The limits, `ExecutionLimits`, and the three host protocols, …": add one sentence. `ExecutionLimits.run_timeout_seconds` bounds a node's total run time and is no inactivity timeout. Detecting a stalled session is the executor's, which returns it as an `infra` `Failed`. No other README passage names the value, and the `adapters/` row's `ScriptedStall` stays as it is.
- [ ] `graphscene/tests/model/test_run_control.py`:
  - `test_the_limits_default_to_graphscenes_own_values`: use `run_timeout_seconds=None`, and make the field-name list end in `"run_timeout_seconds"`.
  - `test_an_out_of_range_limit_is_refused`: the case becomes `({"run_timeout_seconds": 0.0}, "ExecutionLimits: run_timeout_seconds must be > 0, got 0.0")`, with its id `"run_timeout_seconds"`.
- [ ] `graphscene/tests/engine/test_set_execution.py`:
  - Module docstring: "under the optional stall deadline" becomes "under the optional run timeout".
  - The `_execute` helper: rename its `stall_seconds` parameter and keyword to `run_timeout_seconds`.
  - Rename `test_a_stall_is_cancelled_and_retried_alone_while_its_siblings_run_once` to `test_a_run_past_its_timeout_is_cancelled_and_retried_alone_while_its_siblings_run_once`. Pass `run_timeout_seconds=0.05`, and expect `Failed("infra", "timed out: no result within 0.05s")`.
  - `ScriptedStall` stays: it scripts a run that never returns, and it does not name the limit.
- [ ] `graphscene/tests/facade/test_execution_rules.py`, `test_a_gate_stalled_once_is_re_dispatched_alone_and_passes_its_siblings_run_once`. This case is named after the pilot case of the same name (`cli/test/planning-driver-control.test.mjs`), whose stall is an inactivity stall. Under the rule above, that stall reaches the engine as the executor's own `infra` failure, not through the engine's timeout. Reproduce it that way and keep the pilot name:
  - Script `architecture_review` as `[ScriptedFailure("infra", "stalled: its stream was silent", delay=0.01), ScriptedOutcome("approved")]`. The delay keeps it finishing after its zero-delay siblings, so the row order the case asserts is unchanged.
  - Build `Run(_stub(script))` with no limit.
  - Assert `run.stub.cancelled == ()`, since nothing is cancelled now.
  - Expect `rows[2]` to carry `Failed("infra", "stalled: its stream was silent")`. Keep `rows[2]`'s `seq` 2 and attempt 1 of 3, and `rows[3]` as it is.
  - Drop the now-unused `stall_seconds` parameter from `Run.__init__` and the `ScriptedStall` import if nothing else in the file uses it. Ruff flags an unused import.
  - The module docstring's "(a stall or a return failing its schema among them)" stays true.
- [ ] Leave `ScriptedStall`, `graphscene/tests/adapters/test_stub_executor.py` → `test_a_stall_is_cancelled_by_the_callers_deadline`, and the `stalled` outcome names in `graphscene/tests/engine/test_vocabulary.py` alone. They are a scripted hang and an outcome name, not this limit.

The suites edited above are this unit's own test files; run them per the layer's single-file test command (`.claude/context/graphscene.md` → `## Tests`).
