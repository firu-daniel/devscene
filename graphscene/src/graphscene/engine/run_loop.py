"""Run mode's engine: `start_run` and `continue_run`, which drive a walk through the caller's
`Executor` until it reaches a `RunExit`.

The rule:

- Each call constructs its own `AttemptBook` and `UndeliveredBreaker(undelivered_limit)` before
  touching the walker, so a limit below 1 raises the breaker's `ValueError` with the store unread
  and unwritten.
- `start_run` takes its first step from `Walker.start(entry, resume=resume)`; `continue_run` from
  `Walker.next(outcome)` when `outcome` is given (resuming a graph `Interrupt` with its
  `resume_outcome`), otherwise from `Walker.current()` (continuing after a `Halt` or a crash).
- Every walker call runs through `asyncio.to_thread`, so the `StateStore` is never called on the
  event loop's thread.
- A `Dispatch` runs as a set of one, a `DispatchSet` as its `dispatches`, each through
  `execute_set`. A `Wait` is never dispatched: `Walker.current()`, the set of gates still out, is
  taken in its place, and if that is itself a `Wait` the call returns `Refused("the saved walk's
  pending action is a wait, which names no dispatch")`. An `End`, `Stop`, `Interrupt` or
  `Refused` is returned.
- After `execute_set`, every record of its `SetResult` is recorded through `Walker.next`, in order:
  a gate of a set as `(outcome, node, detail)`, a lone dispatch as `(outcome, node)` with no
  detail, because the walk records a detail only for a gate and the host already has it in the
  `Launch` row. A refusal does not stop the remaining records from being recorded.
- Then the first `Refused` is returned if any record was refused; otherwise the `SetResult.halt`
  if set; otherwise the last record's step is the next step.
- A `StateStore` error and an exception out of `Executor.run` propagate unchanged.
- On `asyncio.CancelledError` during `execute_set`, that call cancels and awaits its runs and the
  loop re-raises, recording nothing of that set. During a walker call, the thread finishes its
  call and the loop re-raises: the saved walk is what a later `continue_run` reads.

Deliberately not covered:

- Keeping the walk, the dispatch total and anything else across a pause, a stop or a crash: the
  host's, through its `StateStore` and `DispatchCounter`.
- A helper for a synchronous executor: `graphscene.model.execution` is the guidance.
- Offloading the synchronous host protocols `RunSignals`, `DispatchCounter` and `LaunchSink`: they
  are called on the loop thread, and the host keeps them fast.
- An inactivity timeout: the executor's (#421).
- A deadline of the loop's own: it has none. The only time limit is `run_timeout_seconds`,
  applied by `execute_set`.
- Hooks (#423).
"""

import asyncio

from graphscene.engine.attempts import AttemptBook
from graphscene.engine.breaker import UndeliveredBreaker
from graphscene.engine.set_execution import execute_set
from graphscene.engine.walker import Walker
from graphscene.model.execution import Executor
from graphscene.model.run_control import (
    DispatchCounter,
    ExecutionLimits,
    LaunchSink,
    RunExit,
    RunSignals,
)
from graphscene.model.walk_actions import Dispatch, DispatchSet, Refused, Step, Wait
from graphscene.model.walk_state import RoundResume


async def start_run(
    walker: Walker,
    executor: Executor,
    *,
    signals: RunSignals,
    counter: DispatchCounter,
    sink: LaunchSink,
    limits: ExecutionLimits,
    failure_outcome: str,
    undelivered_limit: int = 3,
    entry: str | None = None,
    resume: RoundResume | None = None,
) -> RunExit:
    book = AttemptBook()
    breaker = UndeliveredBreaker(undelivered_limit)
    step = await asyncio.to_thread(walker.start, entry, resume=resume)
    return await _drive(
        walker, executor, step, signals, counter, sink, book, breaker, limits, failure_outcome
    )


async def continue_run(
    walker: Walker,
    executor: Executor,
    *,
    signals: RunSignals,
    counter: DispatchCounter,
    sink: LaunchSink,
    limits: ExecutionLimits,
    failure_outcome: str,
    undelivered_limit: int = 3,
    outcome: str | None = None,
) -> RunExit:
    book = AttemptBook()
    breaker = UndeliveredBreaker(undelivered_limit)
    if outcome is None:
        step = await asyncio.to_thread(walker.current)
    else:
        step = await asyncio.to_thread(walker.next, outcome)
    return await _drive(
        walker, executor, step, signals, counter, sink, book, breaker, limits, failure_outcome
    )


async def _drive(
    walker: Walker,
    executor: Executor,
    step: Step,
    signals: RunSignals,
    counter: DispatchCounter,
    sink: LaunchSink,
    book: AttemptBook,
    breaker: UndeliveredBreaker,
    limits: ExecutionLimits,
    failure_outcome: str,
) -> RunExit:
    while True:
        if isinstance(step, Wait):
            step = await asyncio.to_thread(walker.current)
            if isinstance(step, Wait):
                return Refused("the saved walk's pending action is a wait, which names no dispatch")
            continue
        if isinstance(step, Dispatch):
            dispatches: tuple[Dispatch, ...] = (step,)
            is_set = False
        elif isinstance(step, DispatchSet):
            dispatches = step.dispatches
            is_set = True
        else:
            return step
        result = await execute_set(
            dispatches,
            executor,
            signals=signals,
            counter=counter,
            sink=sink,
            book=book,
            breaker=breaker,
            limits=limits,
            failure_outcome=failure_outcome,
        )
        last: Step | None = None
        refused: Refused | None = None
        for record in result.records:
            detail = record.detail if is_set else None
            last = await asyncio.to_thread(walker.next, record.outcome, record.node, detail)
            if refused is None and isinstance(last, Refused):
                refused = last
        if refused is not None:
            return refused
        if result.halt is not None:
            return result.halt
        # execute_set returns no halt only once every dispatch is recorded, so `last` is set.
        assert last is not None
        step = last
