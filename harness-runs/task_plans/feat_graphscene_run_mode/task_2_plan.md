### Task 2 — Run each `execute_set` pass through a sliding window of `max_concurrent_dispatches`

**Goal:** Make `execute_set` keep at most `limits.max_concurrent_dispatches` runs of a pass in flight. Under that limit, the next unstarted dispatch starts as soon as a slot frees: with a limit of 5, a set of 8 starts its 6th dispatch when any of the first 5 finishes. Every other rule in `graphscene/src/graphscene/engine/set_execution.py` keeps its meaning.

**Depends on:** Task 1, which adds `ExecutionLimits.max_concurrent_dispatches: int = 10` as the last field of `graphscene.model.run_control.ExecutionLimits`, refused below 1. This task reads that field and nothing else new. It does not write the run loop, which is **Task 3**'s. Task 3 calls `execute_set` with its signature unchanged: `execute_set(dispatches, executor, *, signals, counter, sink, book, breaker, limits, failure_outcome) -> SetResult`.

### Targets

- `graphscene/src/graphscene/engine/set_execution.py`: the window in `_run_pass` and the module docstring.
- `graphscene/tests/engine/test_set_execution.py`: the window's cases.

**Work:**

- [ ] `set_execution.py` → `_run_pass`: replace "launch every dispatch, then wait" with a window over the pass.
  - Keep the unstarted dispatches in a queue in set order, and start the first `limits.max_concurrent_dispatches`.
  - Inside the existing `asyncio.wait(..., FIRST_COMPLETED)` loop, first handle the results found finished together, in set order as now: `Launch` row, `book.settle`, outcomes, held and `again`. Then start the next unstarted dispatches from the queue, in set order, until the window is full again or the queue is empty.
  - A dispatch takes `counter.increment()` as its `seq` and `book.attempt(node)` as its attempt **when it starts**, never when the pass is cleared.
  - Its `_run(...)` task is created at that moment, so `run_timeout_seconds` measures the run alone and never the wait for a slot.
  - Write the window explicitly in the existing `asyncio.wait` loop rather than with an `asyncio.Semaphore`. Set-order starting is then a property of the code rather than of the semaphore's wake-up order.
- [ ] `set_execution.py` → the cancellation and defect path: on `BaseException`, cancel and await only the started tasks, as now. An unstarted dispatch never starts, never takes a `seq` and writes no `Launch` row. A STOP or PAUSE that becomes true while a pass runs does **not** hold back that pass's queued dispatches. The whole pass was cleared once by `clear_set`, all of it goes out, and the signal is honoured at the next `clear_set`.
- [ ] `set_execution.py`, module docstring. Rewrite the second rule bullet: each dispatch of a cleared pass starts in set order, at most `ExecutionLimits.max_concurrent_dispatches` at once, and the next one starts as soon as a running one finishes. It takes its `Launch.seq` and attempt when it starts. Add to the timeout bullet that the deadline runs from the run's start. Add a bullet that the whole pass goes out once cleared, and that a signal raised mid-pass is honoured at the next pass. Extend the cancellation bullet: a dispatch not yet started is never started and writes no row. Replace `- The run loop: #484.` under *Deliberately not covered* with `- Recording the records through the walker and driving the walk: graphscene.engine.run_loop.` That module lands in Task 3 of this branch.
- [ ] `test_set_execution.py`: extend `_execute` with a `max_concurrent_dispatches: int = 10` keyword passed into `ExecutionLimits`. Add an in-test class `Gated`, satisfying `Executor` structurally, with these parts:
  - one `asyncio.Event` per node that the test sets in a chosen order;
  - a single shared `events: list[tuple[str, str]]` logging `("start", node)` and `("end", node)`;
  - `in_flight` and `peak` counters.

  Every expected value is hand-written from the scenario.
- [ ] `test_set_execution.py`: add these cases:
  - `test_a_set_of_eight_under_a_limit_of_five_starts_the_sixth_when_one_finishes`: `peak == 5`; `("start", "n6")` is the entry right after the first `("end", …)`; the `Launch.seq` of `n1`–`n8` is `1`–`8` in set order.
  - `test_the_default_window_is_ten`: a set of 12 under the default limits has `peak == 10`.
  - `test_a_queued_dispatch_is_not_charged_the_wait_against_the_run_timeout`: limit 1, `run_timeout_seconds` set. The first run's scripted delay is under the timeout, and the second run's delay plus the first's exceeds it. Both are recorded `Completed`, with no `Failed("infra", "timed out: …")`.
  - `test_a_stop_raised_mid_pass_still_sends_the_queued_dispatches`: limit 1, a set of 3, `Signals(stop_after=3)`. All three start and are recorded, and the result's `halt` is `None`.
  - `test_cancelling_execute_set_never_starts_a_queued_dispatch`: limit 1, the first run a `ScriptedStall`. Cancel; `stub.started == ("n1",)`, `stub.cancelled == ("n1",)`, the counter total is `1` and the sink holds no row.
  - Every existing case passes unchanged.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_set_execution.py` passes. The existing cases pass with no edit to their bodies, which shows the window leaves the default behaviour of sets of up to 10 unchanged.
- `git grep -n "#484" -- graphscene/src/graphscene/engine/set_execution.py` prints nothing.
- No wall-clock assertion is added. Order is asserted only through the `Gated` log, the stub's records and the sink's rows (`graphscene/tests/engine/test_set_execution.py` → module docstring, *"never against the wall clock"*).
