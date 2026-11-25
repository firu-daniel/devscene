"""Running one dispatch set under the execution rules: `execute_set`, which fans a set out through
the caller's `Executor`, settles each result through `AttemptBook` and re-dispatches what the
rules send back, returning a `SetResult`.

The rule:

- Every pass, the first being the whole set, is cleared by `clear_set` before anything of it goes
  out; a `Halt` from it is returned with the records settled so far, and nothing of that pass is
  launched.
- Each dispatch of a cleared pass, in set order, takes its `Launch.seq` from
  `DispatchCounter.increment` and its attempt from `AttemptBook.attempt`, then starts running
  concurrently with its siblings.
- With `ExecutionLimits.stall_seconds` set, each run is under that deadline; a run that passes it
  is cancelled and becomes `Failed("infra", "stalled: no result within <stall_seconds>s")`. A
  timeout is an `infra` failure.
- Results are handled in finish order; runs found finished together are taken in set order. Each
  writes one `Launch` row to the `LaunchSink` and is settled: a `Recorded` from a `Completed` joins
  the outcomes, a `Recorded` from a `Failed` joins the held failures, and a `Retry` or `Redispatch`
  sends its node to the next pass.
- A failing node never cancels a sibling; a pass ends when every run of it has finished.
- After each pass, `UndeliveredBreaker.observe` is told whether the pass had a `Redispatch`; once
  the breaker is tripped, `Halt("undelivered", "<strikes> consecutive sets delivered nothing")`
  is returned. Its limit is the breaker's own.
- The next pass is the retried and redispatched nodes' original `Dispatch` objects, together, in
  set order, after `ExecutionLimits.backoff_seconds` when it is above 0.
- `SetResult.records` is always the outcomes, then the held failures, each in finish order.
- If `execute_set` is cancelled, it cancels its outstanding runs, awaits them and re-raises.
- An exception out of `Executor.run` is a defect: the outstanding runs are cancelled and awaited,
  then it propagates.

Deliberately not covered:

- Recording the records through the walker, and acting on a `Halt`: the caller's.
- Persisting the book, the breaker and the counter across processes: the host's.
- Usage: the host's, through its executor's usage sink.
- The run loop: #484.
"""

import asyncio
from collections.abc import Sequence

from graphscene.engine.attempts import AttemptBook
from graphscene.engine.breaker import UndeliveredBreaker
from graphscene.engine.safety import clear_set
from graphscene.model.execution import Completed, Executor, Failed, NodeResult
from graphscene.model.run_control import (
    DispatchCounter,
    ExecutionLimits,
    Halt,
    Launch,
    LaunchSink,
    NodeRecord,
    Recorded,
    RunSignals,
    SetResult,
)
from graphscene.model.walk_actions import Dispatch


async def execute_set(
    dispatches: Sequence[Dispatch],
    executor: Executor,
    *,
    signals: RunSignals,
    counter: DispatchCounter,
    sink: LaunchSink,
    book: AttemptBook,
    breaker: UndeliveredBreaker,
    limits: ExecutionLimits,
    failure_outcome: str,
) -> SetResult:
    outcomes: list[NodeRecord] = []
    held: list[NodeRecord] = []
    current: tuple[Dispatch, ...] = tuple(dispatches)
    while True:
        halt = clear_set(current, signals, counter, limits)
        if halt is not None:
            return SetResult((*outcomes, *held), halt)
        again, undelivered = await _run_pass(
            current, executor, counter, sink, book, limits, failure_outcome, outcomes, held
        )
        breaker.observe(undelivered)
        if breaker.tripped:
            detail = f"{breaker.strikes} consecutive sets delivered nothing"
            return SetResult((*outcomes, *held), Halt("undelivered", detail))
        current = tuple(d for d in current if d.node in again)
        if not current:
            return SetResult((*outcomes, *held), None)
        if limits.backoff_seconds > 0:
            await asyncio.sleep(limits.backoff_seconds)


async def _run_pass(
    current: tuple[Dispatch, ...],
    executor: Executor,
    counter: DispatchCounter,
    sink: LaunchSink,
    book: AttemptBook,
    limits: ExecutionLimits,
    failure_outcome: str,
    outcomes: list[NodeRecord],
    held: list[NodeRecord],
) -> tuple[set[str], bool]:
    again: set[str] = set()
    undelivered = False
    launched: dict[asyncio.Task[NodeResult], tuple[Dispatch, int, int]] = {}
    try:
        for dispatch in current:
            seq = counter.increment()
            attempt = book.attempt(dispatch.node)
            task = asyncio.create_task(_run(executor, dispatch, limits.stall_seconds))
            launched[task] = (dispatch, seq, attempt)
        outstanding = set(launched)
        while outstanding:
            done, outstanding = await asyncio.wait(outstanding, return_when=asyncio.FIRST_COMPLETED)
            for task in [t for t in launched if t in done]:
                dispatch, seq, attempt = launched[task]
                result = task.result()
                sink.record(
                    Launch(seq, dispatch.node, dispatch.agent, attempt, limits.max_attempts, result)
                )
                settlement = book.settle(dispatch.node, result, limits, failure_outcome)
                if isinstance(settlement, Recorded):
                    (outcomes if isinstance(result, Completed) else held).append(settlement.record)
                else:
                    again.add(settlement.node)
                    if settlement.kind == "redispatch":
                        undelivered = True
    except BaseException:
        for task in launched:
            task.cancel()
        await asyncio.gather(*launched, return_exceptions=True)
        raise
    return again, undelivered


async def _run(executor: Executor, dispatch: Dispatch, stall_seconds: float | None) -> NodeResult:
    if stall_seconds is None:
        return await executor.run(dispatch)
    deadline = asyncio.timeout(stall_seconds)
    try:
        async with deadline:
            return await executor.run(dispatch)
    except TimeoutError:
        if not deadline.expired():
            raise
        return Failed("infra", f"stalled: no result within {stall_seconds}s")
