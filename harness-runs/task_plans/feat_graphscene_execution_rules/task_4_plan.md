### Task 4 — Add `execute_set`, running one dispatch set under the execution rules

**Goal:** Compose the rules into one `asyncio` component that runs a dispatch set through the caller's `Executor`. It clears every pass through `clear_set`, launches each node concurrently under the optional stall deadline, writes one `Launch` row per launched session, and settles each result as it finishes through `AttemptBook`. It never cancels a sibling. It re-dispatches only the retried and the undelivered nodes, after the backoff, as a new pass that clears the safety contract again. It feeds each pass to `UndeliveredBreaker` and returns every final record in join order, together with any run-level `Halt`.

**Depends on:** Tasks 1, 2 and 3, whose contracts are used here exactly as stated.

- **Task 1** (`graphscene/src/graphscene/model/run_control.py`):
  - `ExecutionLimits(max_attempts, backoff_seconds, dispatch_cap, stall_seconds)` — no undelivered-set limit;
  - `RunSignals`, `DispatchCounter` (`total()`, `increment() -> int`) and `LaunchSink` (`record(launch)`);
  - `Launch(seq, node, agent, attempt, max_attempts, result)`;
  - `Halt(reason, detail)`, `NodeRecord(node, outcome, detail)`, `Recorded(record)`, `Retry(node, attempt, reason)`, `Redispatch(node, reason)`;
  - `SetResult(records: tuple[NodeRecord, ...], halt: Halt | None)`.
- **Task 2:**
  - `graphscene/src/graphscene/engine/safety.py` → `clear_set(dispatches, signals, counter, limits) -> Halt | None`, which only checks and never increments;
  - `graphscene/src/graphscene/engine/breaker.py` → `UndeliveredBreaker(limit: int = 3)`, with `limit`, `strikes`, `observe(undelivered: bool) -> int` and `tripped` (`strikes >= limit`). The limit is the breaker's own constructor argument and its only source; `execute_set` reads no other breaker limit and decides the trip only through `breaker.tripped`.
- **Task 3:** `graphscene/src/graphscene/engine/attempts.py` → `AttemptBook`, with `attempt(node) -> int` and `settle(node, result, limits, failure_outcome) -> Settlement`.
- **#420 and #487:** `graphscene.model.execution` → `Executor.run(dispatch) -> NodeResult`, `Completed` and `Failed`.

**Where this layer stops.** `execute_set` runs one set and returns. It never calls `Walker`, renders nothing, and never logs or prints (`.claude/context/graphscene.md` → `## What this layer owns, and what it is not`, *"The library never logs or prints"*). Recording `SetResult.records` through `Walker.next` and acting on a `Halt` are the caller's: #484's loop, and in this branch Task 6's scenario suite. The public-surface entries and the README row are Task 5's. The module is in `engine`, so it imports only `graphscene.model`, `graphscene.engine` and the standard library. `StubExecutor` is used only by the tests.

### Targets

- `graphscene/src/graphscene/engine/set_execution.py` (new)
- `graphscene/tests/engine/test_set_execution.py` (new)

**Work:**

- [ ] Write the module docstring. Its *"The rule:"* paragraph states each rule this task implements, in the bullets that follow. Its *"Deliberately not covered:"* list names: recording through the walker, persisting the book, breaker and counter across processes, usage (the host's, through its executor's usage sink), and the run loop (#484).
- [ ] `async def execute_set(dispatches: Sequence[Dispatch], executor: Executor, *, signals: RunSignals, counter: DispatchCounter, sink: LaunchSink, book: AttemptBook, breaker: UndeliveredBreaker, limits: ExecutionLimits, failure_outcome: str) -> SetResult`. Each pass, starting with the whole set:
  1. Call `clear_set` on the pass. On a `Halt`, return `SetResult(<records so far>, halt)`.
  2. For each dispatch, in set order, take `seq = counter.increment()` and `attempt = book.attempt(node)`, and start one task running `executor.run(dispatch)`. When `stall_seconds` is set, the run is inside `asyncio.timeout(stall_seconds)`, and a `TimeoutError` becomes `Failed("infra", "stalled: no result within <stall_seconds>s")`. This is the branch's decision that **a timeout is `infra`**.
  3. Handle each task as it finishes, using `asyncio.wait(..., return_when=FIRST_COMPLETED)`:
     - write `sink.record(Launch(seq, node, dispatch.agent, attempt, limits.max_attempts, result))`;
     - settle the result;
     - append a `Recorded` from a `Completed` to the outcome list, in finish order;
     - append a `Recorded` from a failure to the held list, in finish order;
     - collect each `Retry` and `Redispatch` node.
- [ ] Join and next pass:
  - A failing node never cancels a sibling.
  - Once every task of the pass has finished, call `breaker.observe(<any Redispatch in this pass>)`. If it is then `tripped`, return `SetResult(<records>, Halt("undelivered", "<strikes> consecutive sets delivered nothing"))`.
  - Otherwise the next pass is the retried and redispatched nodes' original `Dispatch` objects, in set order. A set holding both kinds sends them out together, as the pilot does. Before that pass, `await asyncio.sleep(limits.backoff_seconds)` when it is above 0.
  - With no next pass, return `SetResult(<outcomes, then held failures>, None)`. `<records>` is always that same order: outcomes, then held failures.
- [ ] Cancellation and defects:
  - If `execute_set` itself is cancelled, it cancels its outstanding tasks, awaits them and re-raises.
  - An exception out of `executor.run` is a defect (`graphscene/src/graphscene/model/execution.py` → *"An exception out of `run` is a defect and propagates."*). The outstanding tasks are cancelled and awaited, then the exception propagates.

  Both rules go into the docstring.
- [ ] `test_set_execution.py`. Its header is the *"The rule this file exists to enforce"* docstring. It uses `StubExecutor`, `ScriptedOutcome`, `ScriptedFailure` and `ScriptedStall` from `graphscene.adapters.stub_executor`, plus in-test structural `RunSignals`, `DispatchCounter` and `LaunchSink` classes. Every async case runs through `asyncio.run(...)` inside a plain `-> None` test, with `backoff_seconds=0`. Order is asserted only through `StubExecutor.started`, `StubExecutor.finished`, `StubExecutor.cancelled` and the sink's rows, never against the wall clock. Cases:
  - outcomes are recorded in finish order, not set order, using scripted delays;
  - an agent failure on one gate waits for its siblings, is listed after the last outcome, and `StubExecutor.cancelled` stays `()`;
  - a stall with `stall_seconds` set is cancelled, retried alone and passes, while its siblings run once;
  - three infra failures produce the exhausted three-line `detail`;
  - an undelivered gate is re-dispatched with an unchanged `attempt` in its next `Launch` row;
  - with `breaker=UndeliveredBreaker()`, a third consecutive undelivered pass returns `Halt("undelivered", "3 consecutive sets delivered nothing")`, with the outcomes recorded so far;
  - with `breaker=UndeliveredBreaker(2)`, the second consecutive undelivered pass returns `Halt("undelivered", "2 consecutive sets delivered nothing")` — the host's limit takes effect;
  - a retry pass that would pass `dispatch_cap` returns the cap halt and launches nothing more;
  - a STOP raised by the in-test signals after the first pass lets that pass finish, and the retry pass halts with `"stop"`;
  - the sink holds one row per launched session, retries included, with `seq` taken from the counter and `attempt`/`max_attempts` correct.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_set_execution.py` passes.
- `bash scripts/typecheck.sh` reports no failure in either new file.
- The module imports nothing from `graphscene.adapters` or `graphscene.facade`, and nothing in it writes to stdout or stderr.
