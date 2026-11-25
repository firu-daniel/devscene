### Task 1 — Declare the `Executor` protocol and its `Completed` / `Failed` results in `model`

**Goal:** Give GraphScene the contract for running a node: a structural `asyncio` protocol, `Executor`, and the result it returns, `NodeResult = Completed | Failed`, with the three failure classes as a `Literal` alias. These are declared in `model` so that an adapter implements them without importing the engine.

**Where this task stops.** This task declares types and nothing that runs them:

- **The scriptable stub** that satisfies `Executor` is **Task 3's** (`graphscene/src/graphscene/adapters/stub_executor.py`).
- **The JSON Schema check** an executor uses to decide `undelivered` is **Task 2's** (`graphscene/src/graphscene/adapters/return_schema.py`).
- **Exporting the names from `graphscene` and the README rows** for this module are **Task 4's**. This task does not edit `graphscene/src/graphscene/__init__.py`, `graphscene/src/graphscene/facade/__init__.py`, `graphscene/tests/test_public_surface.py` or `graphscene/README.md`.
- **The loop that calls `run`**, the deadline around it and what is done with each failure class belong to #484 and #422, not to this branch.

### Targets

- `graphscene/src/graphscene/model/execution.py` (new): the protocol, the two result classes and the two aliases.
- `graphscene/src/graphscene/model/__init__.py`: its docstring says *"the two protocols the engine drives"*, which becomes false when this module lands.
- `graphscene/tests/model/test_execution.py` (new): this module's own suite, the test that `.claude/context/graphscene.md` → `## What accompanies a new module` requires.

**The contract this task defines.** Tasks 2, 3 and 4 restate it exactly as written here:

```python
FailureClass: TypeAlias = Literal["infra", "agent", "undelivered"]

@dataclass(frozen=True)
class Completed:
    kind: ClassVar[Literal["completed"]] = "completed"
    outcome: str
    detail: str | None = None

@dataclass(frozen=True)
class Failed:
    kind: ClassVar[Literal["failed"]] = "failed"
    failure: FailureClass
    reason: str

NodeResult: TypeAlias = Completed | Failed

class Executor(Protocol):
    async def run(self, dispatch: Dispatch) -> NodeResult: ...
```

`Dispatch` is `graphscene.model.walk_actions.Dispatch`, imported from its defining module and never from the package root.

**Work:**

- [ ] **`execution.py`, the types.** Declare the five names above with exactly these spellings, fields and defaults. Follow the model rules of `.claude/context/graphscene.md` → `## The model and its wire forms`: every class is a `@dataclass(frozen=True)`, and the discriminator is a `ClassVar[Literal[...]]` named `kind`, as `graphscene/src/graphscene/model/walk_actions.py` does. Import only the standard library and `graphscene.model.walk_actions`.
- [ ] **`execution.py`, the module docstring and *"The rule:"*.** The module opens with a docstring stating what it owns. Then a *"The rule:"* paragraph, per `.claude/context/graphscene.md` → `## Naming and layout`, states:
  - `run` takes one `Dispatch`. A `DispatchSet` is fanned out by the caller, one `run` per gate, and the runs may be concurrent on one event loop.
  - `Completed.outcome` and `Completed.detail` are what the caller passes to `Walker.next(outcome, node, detail)`, with `node` being `dispatch.node`. Whether the outcome is one the node declares is the walk's to refuse, never the executor's to check.
  - An anticipated failure is returned as a `Failed`, never raised. An exception out of `run` is a defect and propagates.
  - The three classes, worded as the story index's `## Context` words them:
    - `infra`: the run did not finish for a reason outside the agent, such as a crash, an unresolved session or a stall the executor detected itself. Retryable.
    - `agent`: the agent finished and reported that it failed.
    - `undelivered`: the run finished but left no return the executor could read as a valid one, because it was absent, could not be parsed, or failed the schema the executor names.
  - `run` is cancellable. On `asyncio.CancelledError` it releases what it holds and re-raises, and never turns cancellation into a result. The deadline around a node's coroutine is the caller's to set and to report (#484).
  - A run may be repeated for the same dispatch (a retry, an interrupt's resume), so an executor's side effects must be repeatable.
- [ ] **`execution.py`, the *"Deliberately not covered:"* list.** It names:
  - Sandboxing, permission modes and allowed tools: the host passes them in when it constructs its executor, and `run` carries none.
  - A helper for a synchronous executor: none is offered. A blocking implementation wraps its work with `await asyncio.to_thread(…)`, and a cancelled `to_thread` call does not stop its thread.
  - What is done with each failure class (retry, park, breaker): #422.
  - The run loop and its deadline: #484.
- [ ] **`model/__init__.py`.** Reword the docstring's *"the two protocols the engine drives"* so it no longer gives a count. Mention the executor beside the walk's state and its actions. The *"The rule:"* paragraph is unchanged.
- [ ] **`tests/model/test_execution.py`.**
  - The module docstring opens *"The rule this file exists to enforce"*, per `.claude/context/conventions.md` → `## The testing bar`.
  - Use plain `-> None` test functions. Drive coroutines with `asyncio.run(…)` inside them, and add no async test plugin.
  - Write every expected value by hand.
  - Cases:
    - `Completed` and `Failed` are frozen.
    - `Completed.detail` defaults to `None`.
    - `Completed.kind == "completed"` and `Failed.kind == "failed"`.
    - `typing.get_args(FailureClass) == ("infra", "agent", "undelivered")`, in that order.
    - An in-test class with `async def run` that returns a `Completed` for one node and a `Failed` for another, assigned to an `executor: Executor` local. `mypy` grades it, as `graphscene/tests/model/test_walk_state.py` grades its protocols. The case runs it with `asyncio.run` on a hand-built `Dispatch`.
    - An in-test class wrapping a blocking function with `await asyncio.to_thread(…)`, assigned to an `Executor` local and run the same way. This shows the decided route for a synchronous adopter.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/model/test_execution.py` passes.
- `commands.typecheck` passes. `mypy` `strict` is what grades the two in-test classes against `Executor`, so a typecheck failure naming `test_execution.py` is this task's to fix.
- `execution.py` imports nothing outside the standard library and `graphscene.model`.
- The five names are spelled exactly as in the contract block above. Tasks 2–4 restate that block, so any drift breaks them.
