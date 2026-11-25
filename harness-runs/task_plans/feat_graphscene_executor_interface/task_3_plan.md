### Task 3 — Add the scriptable `StubExecutor` with outcomes, delays, failures and stalls

**Goal:** Ship GraphScene's built-in test executor. `StubExecutor` satisfies `Executor` and runs each node from a script the test writes: an outcome, a failure of any class or a stall, each after an optional delay. It also keeps a record of what it was asked to run, so the engine's tests from #422 and #484 onward can assert joins, retries and the deadline without a real agent.

**Depends on:** Task 1, which declares, in `graphscene/src/graphscene/model/execution.py`:

```python
FailureClass: TypeAlias = Literal["infra", "agent", "undelivered"]
Completed(outcome: str, detail: str | None = None)   # kind "completed"
Failed(failure: FailureClass, reason: str)            # kind "failed"
NodeResult: TypeAlias = Completed | Failed
class Executor(Protocol):
    async def run(self, dispatch: Dispatch) -> NodeResult: ...
```

`Dispatch` is `graphscene.model.walk_actions.Dispatch`. This task implements that protocol structurally, with no subclassing, and imports each name from its defining module. It must honour the cancellation rule Task 1's docstring states: on `asyncio.CancelledError`, release what is held and re-raise, never return a result.

**Where this task stops.** It drives no walk and imports nothing from `graphscene.engine`, as the `graphscene-layers` contract forbids. Exporting the stub and its script types from `graphscene`, and the README rows, are **Task 4's**. Validating a structured return is Task 2's and not used here: the stub's script already holds results, not documents.

### Targets

- `graphscene/src/graphscene/adapters/stub_executor.py` (new): the script types and `StubExecutor`.
- `graphscene/src/graphscene/adapters/__init__.py`: its docstring lists what the layer touches, and now also holds an executor.
- `graphscene/tests/adapters/test_stub_executor.py` (new): this module's own suite.

**The contract this task defines.** Task 4 exports these names:

```python
@dataclass(frozen=True)
class ScriptedOutcome:   outcome: str; detail: str | None = None; delay: float = 0.0
@dataclass(frozen=True)
class ScriptedFailure:   failure: FailureClass; reason: str; delay: float = 0.0
@dataclass(frozen=True)
class ScriptedStall:     pass
Scripted: TypeAlias = ScriptedOutcome | ScriptedFailure | ScriptedStall

class StubExecutor:
    def __init__(self, script: Mapping[str, Sequence[Scripted]]) -> None: ...
    async def run(self, dispatch: Dispatch) -> NodeResult: ...
    @property
    def started(self) -> tuple[str, ...]: ...    # node ids, in the order run was called
    @property
    def finished(self) -> tuple[str, ...]: ...   # node ids, in the order a run returned
    @property
    def cancelled(self) -> tuple[str, ...]: ...  # node ids whose run was cancelled
```

**Work:**

- [ ] **`stub_executor.py`, the script types.**
  - Declare the three frozen dataclasses and the `Scripted` alias as above.
  - A negative `delay` raises `ValueError("<class name>: delay must be >= 0, got <delay>")` in `__post_init__`.
- [ ] **`stub_executor.py`, `StubExecutor.run`.**
  - The constructor copies `script` into one fresh `collections.deque` per node id, so a later change to the caller's mapping or sequences changes nothing.
  - Each `run(dispatch)` records `dispatch.node` in `started`, then pops the next entry from that node's queue, so a repeated dispatch (a retry, a resume) takes the next entry. With no entry left, it raises `LookupError("<node>: the stub has no scripted run left")`: that is a mistake in the test's script, not a node failure.
  - A `ScriptedOutcome` or `ScriptedFailure` awaits `asyncio.sleep(delay)`, then returns `Completed(outcome, detail)` or `Failed(failure, reason)` and records the node in `finished`.
  - A `ScriptedStall` awaits an `asyncio.Event` that is never set, so only cancellation ends it.
- [ ] **`stub_executor.py`, cancellation and the docstring.**
  - On `asyncio.CancelledError`, during a delay or a stall, record the node in `cancelled` and re-raise.
  - Concurrent runs on one event loop are supported, with one shared record and no lock: a single event loop runs one coroutine at a time between awaits.
  - The module docstring states what the module owns.
  - A *"The rule:"* paragraph covers: one queue per node, the record properties, re-raising on cancellation, and that a stall ends only by cancellation. It cites Task 1's `graphscene.model.execution` for the deadline being the caller's.
  - A *"Deliberately not covered:"* list names the stub's limits: no wall-clock assertion of a delay, no structured return documents, and no thread or process.
- [ ] **`adapters/__init__.py`.** Extend the docstring's list of what the layer touches with a built-in executor for tests and checking an executor's return against a JSON Schema. The second item is Task 2's module, listed here so that one task owns this file. The *"The rule:"* paragraph is unchanged.
- [ ] **`tests/adapters/test_stub_executor.py`.**
  - The module docstring opens *"The rule this file exists to enforce"*. Use plain `-> None` test functions, and drive each with `asyncio.run(…)`. Write every expected value by hand.
  - Build each `Dispatch` by hand.
  - Assert no duration. Order is asserted only through the record, never by timing a run, per `harness-runs/lessons.md` → *"A plan never makes repeated in-run timing runs its acceptance evidence"*.
  - Cases:
    - A scripted outcome returns `Completed("done", "notes.md")`.
    - Each failure class returns its `Failed`.
    - A node scripted twice returns its two entries in order on two runs.
    - An exhausted node raises the exact `LookupError` text.
    - A negative delay raises the exact `ValueError` text.
    - Mutating the caller's script after construction changes nothing.
    - `asyncio.gather` over three gates of one round on one stub returns every result, and `finished` follows the scripted delays (`0.0` before `0.05`), not the call order.
    - A stall under `asyncio.wait_for(…, timeout=0.01)` raises `TimeoutError`, `cancelled` holds the node, and `finished` does not.
    - `StubExecutor` is assigned to an `executor: Executor` local, which `mypy` grades.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_stub_executor.py` passes.
- `commands.typecheck` passes, and that includes the `Executor` assignment.
- The stall case proves cancellation propagates out of the stub. This guards the story index's second `Top risks:` entry: #484's engine-owned deadline is testable only if the stub never swallows cancellation.
- `stub_executor.py` imports only the standard library and `graphscene.model`.
