`feat_graphscene_run_mode` completes GraphScene's execution flow: the engine drives a walk end to end with an executor, applying #422's rules. Part of #376.

## Why

Split out of #420 on 2026-11-25. #420 ships the executor interface and a stub, and #422 the execution rules. Neither runs a walk. This branch adds the second way a host uses GraphScene. In step mode the host runs each action the walker returns, while in run mode the host hands the engine an executor and the engine runs the loop. #423's hooks and #424's planning cutover build on it.

## Decided (2026-11-25)

- **Run mode is `asyncio`-based**, as #420's interface is. A round's gates are dispatched concurrently as tasks on one event loop, not as one thread per gate. GraphScene puts no limit on how many gates a round declares.

## Decided (2026-11-26)

- **How many dispatches run at once.** A sliding window: `execute_set` takes an `asyncio.Semaphore`-style limit, so with a limit of 5 a set of 8 starts its 6th dispatch as soon as any of the first 5 finishes. GraphScene's default is 10, used when the host sets none; the host passes its own (5 for the harness). The graph format stays unlimited. The whole set is still cleared by the safety contract and counted against the cap once, and all of it goes out: a STOP raised mid-set is honoured at the next set.
- **State lives for one loop call.** The `AttemptBook` and `UndeliveredBreaker` a call uses are that call's. Whatever must survive a pause, a stop or a crash is the host's to keep and pass back in.
- **A single `Dispatch` runs as a set of one** through `execute_set`, so there is one execution path. The `Dispatch` type stays: `DispatchSet` is built from it.
- **The loop sets no deadline of its own.** The engine's only time limit is the optional total-run limit in `ExecutionLimits` (`run_timeout_seconds`, renamed from `stall_seconds` by #422's user review), default `None`, set by the host and applied by `execute_set`. Detecting an inactive session (a stall) is the executor's (#421), returned as `Failed("infra", …)`.

## Leads

_The leads below are starting points from #376, #420 and #422 and the discussion that split them, not requirements. The planning session decides what holds when this branch is planned._

- **The loop.** The loop starts or resumes a walk, then repeats: dispatch the walker's next action through the executor, record the outcome, and advance. It stops at a terminal, a park or an interrupt. Step mode (#416) stays as it is, synchronous, and the CLI (#452) is unchanged.
- **#422's rules applied in the loop.** The loop runs each set through #422's `execute_set` and records its `SetResult.records` in order through the walker. A node's final failure is recorded under the host-named failure outcome, and the graph's binding for it parks the walk; a returned `Halt` (STOP, PAUSE, the cap, the undelivered breaker) ends the call as an interrupt the host resumes later. #422's suites already drive the rules on the stub; this branch's tests are the loop's.
- **Blocking calls inside the event loop.** `FileStateStore` takes an `fcntl` lock and writes a file (`graphscene/src/graphscene/adapters/state_file.py`). An executor an adopter writes may be synchronous. Planning decides how these run without blocking the loop, for example with `asyncio.to_thread`. #420 offers no helper for a synchronous executor; its docstring shows wrapping one with `asyncio.to_thread` and notes that a cancelled `to_thread` call does not stop its thread.
- **Cancellation.** An executor's `run` is cancellable and re-raises on cancellation (`graphscene/src/graphscene/model/execution.py`). `StubExecutor`'s `ScriptedStall` and its `cancelled` record are there to test the loop's cancellation and the total-run limit.

## Depends on

#422
