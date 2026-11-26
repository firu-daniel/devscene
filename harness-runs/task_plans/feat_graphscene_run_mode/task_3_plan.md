### Task 3 — Add the run loop `start_run` / `continue_run` in `graphscene.engine.run_loop`

**Goal:** Add run mode's engine. Two coroutines start or continue a walk, then repeat three steps: run the walker's next action through `execute_set`, record its `SetResult.records` in order through the walker, and advance. They return a `RunExit` at a terminal, a park, a graph interrupt, a walk refusal or a run-level `Halt`.

**Depends on:**
- Task 1: `graphscene.model.run_control.RunExit: TypeAlias = End | Stop | Interrupt | Halt | Refused`, and `ExecutionLimits.max_concurrent_dispatches: int = 10`.
- Task 2: `graphscene.engine.set_execution.execute_set(dispatches, executor, *, signals, counter, sink, book, breaker, limits, failure_outcome) -> SetResult`. It runs each pass through the sliding window and returns `SetResult(records, halt)`, where the records are the outcomes and then the held failures, each in finish order. This task calls it exactly so and never re-implements a window, a retry or a safety check.

**Where this task stops.** The module is engine-internal until **Task 4**. Task 4 adds `start_run`, `continue_run` and `RunExit` to both `__all__` lists and `test_public_surface.py`, writes the README rows, and drives run mode as a caller over `FileStateStore`. This task edits none of those files. Step mode (`Walker`) and the command line are not touched.

### Targets

- `graphscene/src/graphscene/engine/run_loop.py` (new): `start_run`, `continue_run` and the private drive loop.
- `graphscene/tests/engine/test_run_loop.py` (new): the module's suite, the accompanying test `.claude/context/graphscene.md` → `## What accompanies a new module` requires.

**Work:**

- [ ] `run_loop.py`, the opening docstring. State the module's ownership, then *"The rule:"* as bullets matching the behaviour below, then *"Deliberately not covered:"*:
  - keeping the walk, the dispatch total and anything else across a pause, a stop or a crash, which is the host's, through its `StateStore` and `DispatchCounter`;
  - a helper for a synchronous executor, for which `graphscene.model.execution` is the guidance;
  - offloading the synchronous host protocols `RunSignals`, `DispatchCounter` and `LaunchSink`, which are called on the loop thread and which the host keeps fast;
  - an inactivity timeout, which is the executor's (#421);
  - the loop's own deadline, which it has none of: the only time limit is `run_timeout_seconds`, applied by `execute_set`;
  - hooks (#423).

  Imports: `graphscene.engine.walker`, `graphscene.engine.set_execution`, `graphscene.engine.attempts`, `graphscene.engine.breaker`, `graphscene.model.*` and `asyncio`. Never `graphscene.adapters`.
- [ ] `run_loop.py`, the two entry points. The shared keywords are `signals: RunSignals`, `counter: DispatchCounter`, `sink: LaunchSink`, `limits: ExecutionLimits`, `failure_outcome: str` and `undelivered_limit: int = 3`.
  - `async def start_run(walker: Walker, executor: Executor, *, <shared>, entry: str | None = None, resume: RoundResume | None = None) -> RunExit` takes its first step from `await asyncio.to_thread(walker.start, entry, resume=resume)`.
  - `async def continue_run(walker: Walker, executor: Executor, *, <shared>, outcome: str | None = None) -> RunExit` takes it from `await asyncio.to_thread(walker.current)`, or from `await asyncio.to_thread(walker.next, outcome)` when `outcome` is given. That is how a host resumes a graph `Interrupt` with its `resume_outcome`, or continues after a `Halt` or a crash.
  - Each call constructs its own `AttemptBook()` and `UndeliveredBreaker(undelivered_limit)` **before** touching the walker. A limit below 1 therefore raises the breaker's `ValueError` and leaves the store unread and unwritten.
- [ ] `run_loop.py`, the drive loop. On each step:
  - `Dispatch`: run `(step,)`, a set of one.
  - `DispatchSet`: run `step.dispatches`.
  - `Wait`: never dispatched; take `await asyncio.to_thread(walker.current)`, the set of gates still out, in its place.
  - `End`, `Stop`, `Interrupt` or `Refused`: return it.

  After `execute_set`, record **every** record of the result, in order, each through `await asyncio.to_thread(walker.next, …)`. A gate of a set is recorded as `(r.outcome, r.node, r.detail)`. A lone dispatch is recorded as `(r.outcome, r.node)` with no detail, because the walker records a detail only for a gate (`graphscene/src/graphscene/engine/walker.py` → `_step`), and the host already has that detail in the `Launch` row its sink received. A refusal does not stop the remaining records from being recorded. Then:
  - if any record was refused, return the first `Refused`;
  - otherwise, if `result.halt` is set, return that `Halt`;
  - otherwise the last record's step is the next step: the join's step for a set, the next action for a dispatch.
- [ ] `run_loop.py`, errors and cancellation. A `StateStore` error (`ValueError`, `TimeoutError`, `OSError`) and an exception out of `Executor.run` propagate unchanged. On `asyncio.CancelledError` during `execute_set`, that call cancels and awaits its runs, the loop re-raises, and nothing of that set is recorded. During a `to_thread` walker call, the thread finishes its call and the loop re-raises: the saved walk is what a later `continue_run` reads.
- [ ] `test_run_loop.py`. The header opens with *"The rule this file exists to enforce"*. Use planted graphs from `graphscene/tests/engine/walk_support.py` → `planted`, plus an in-test `MemoryStore` satisfying `StateStore` that records `threading.get_ident()` on each `read`, `write` and `lock`, alongside in-test `Signals`, `Counter` and `Sink`. Drive `StubExecutor` with `backoff_seconds=0` through `asyncio.run`. Every expected value is hand-written from the planted graph and the script, never from the code's output. Cases:
  - A lone dispatch, a round set and a terminal end on `End`. The stub's `started` order is the walk order.
  - A lone dispatch's `Completed` detail does not make the walk refuse, and the `Launch` row carries it.
  - An agent failure is recorded under `failure_outcome`, and the node's binding returns the graph's `Stop`, with no retry.
  - Three `ScriptedStall` runs under `run_timeout_seconds` are recorded under `failure_outcome` and end on `Stop`, and `stub.cancelled` lists the three.
  - STOP before a set returns `Halt("stop", …)`, launches nothing, and leaves `walker.current()` returning the same action.
  - In a two-gate round, one gate retries and is halted by STOP on its retry pass. The recorded gate is saved, and `current()` returns a `DispatchSet` of the other gate alone. `continue_run` then finishes the walk, its relaunch taking `Launch.attempt == 1` because the book is per call.
  - `undelivered_limit=1` halts with `Halt("undelivered", "1 consecutive sets had an undelivered result")`.
  - An `Interrupt` binding returns the `Interrupt`, and `continue_run(outcome=<its resume_outcome>)` continues to `End`.
  - An undeclared outcome returns `Refused("outcome '<o>' is not declared by node '<n>'")` with the store unwritten for it.
  - `continue_run` with no saved walk returns `Refused("no walk has started")`.
  - `undelivered_limit=0` raises `ValueError` with the store untouched.
  - Every store call's thread id differs from the event loop's.
  - Cancelling a `start_run` task whose run stalls re-raises `CancelledError`, `stub.cancelled` names the node, and `current()` still returns the dispatch.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_run_loop.py` passes, with every case listed above present.
- `bash scripts/python-service.sh --package graphscene lint` and `… typecheck` pass. `mypy` `strict` covers both new files.
- `git grep -n "graphscene.adapters" -- graphscene/src/graphscene/engine/run_loop.py` prints nothing. The engine never imports adapters (`.claude/context/graphscene.md` → `## The internal layers`).
- Reading `run_loop.py` finds no `asyncio.timeout`, `wait_for` or `sleep` of its own, because the loop sets no deadline, and no retry or safety check re-implemented outside `execute_set`.
