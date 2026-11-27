### Task 5 — Run a dispatch's before-hooks on every attempt inside `execute_set`

**Goal:** Give `execute_set` a seam that runs before each attempt of each dispatch, so a node's before-hooks run again on an infrastructure retry. This is the gap the task prompt names: *"execute_set (#422) launches and retries a set's nodes inside one call, so an infrastructure retry would not run the hook again."* Planning settles it as **once per attempt**.

**Depends on:** Task 4, which declares the hook call this seam passes:

```python
@dataclass(frozen=True)
class BeforeDispatch:
    kind: ClassVar[Literal["before_dispatch"]] = "before_dispatch"
    dispatch: Dispatch
    seq: int
    attempt: int
```

**Where this layer stops.** `execute_set` knows no graph and no hook names. It calls one callable the caller passes. Task 6's run loop builds that callable from the dispatched node's `before` names and the host's `HookHost`.

### Targets

- `graphscene/src/graphscene/engine/set_execution.py`
- `graphscene/tests/engine/test_set_execution.py`

**The contract this task produces.** Task 6 calls it, and Task 7 documents it.

- `execute_set(…, before_dispatch: Callable[[BeforeDispatch], Awaitable[None]] | None = None)` gains a new keyword-only argument, defaulting to `None`. With `None`, its behaviour is byte-for-byte today's.
- **When it is awaited.** For each dispatch it starts, after that dispatch takes its `seq` from `DispatchCounter.increment` and its attempt from `AttemptBook.attempt`, `execute_set` awaits `before_dispatch(BeforeDispatch(dispatch, seq, attempt))`. It does so inside that dispatch's own task, before `Executor.run`, and outside the `run_timeout_seconds` deadline. The deadline covers `Executor.run` alone, so time a hook takes never counts against the run.
- **What an exception does.** An exception from `before_dispatch` is handled exactly as an exception out of `Executor.run`: the outstanding runs are cancelled and awaited, then it propagates. The dispatch whose hook raised runs no `Executor.run` and writes no `Launch` row, though it has taken its `seq`. That is the same as the module's existing *"Deliberately not covered"* case for a cancelled run.

**Work:**

- [ ] **`set_execution.py` — the parameter and the call.** Add the parameter and thread it to `_run_pass` and `_run`. In `_run`, await the hook with `BeforeDispatch(dispatch, seq, attempt)` before entering `asyncio.timeout`. This means `_run` takes `seq` and `attempt`, which `_run_pass` already has at task creation.
- [ ] **`set_execution.py` — the docstring.** Add a *"The rule:"* bullet stating the call point, the once-per-attempt rule and the exception handling as the contract above spells them. Add to *"Deliberately not covered"*: which hooks a node runs, and every other hook, belong to the caller (`graphscene.engine.run_loop`).
- [ ] **`test_set_execution.py`.** Add these cases, each with a recording `before_dispatch` and `StubExecutor`, and each expected value hand-written:
  - a set of two runs the hook once per dispatch, with each dispatch's own `seq` and attempt 1;
  - a node retried after `ScriptedFailure("infra", …)` runs the hook again, with attempt 2 and a new `seq`;
  - the hook is awaited before the node's run starts: the stub's `started` list has not gained the node when the hook records it;
  - a hook that raises propagates the exception, and the dispatch writes no `Launch` row;
  - with `run_timeout_seconds` set, a hook delayed by `asyncio.sleep` does not time the run out;
  - with no `before_dispatch`, an existing case passes unchanged.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_set_execution.py` passes.
- Every existing case in that file passes without edit. The new argument changes nothing when it is absent.
