### Task 4 — Declare the hook calls and the `HookHost` protocol in `model/hooks.py`

**Goal:** Give GraphScene the plain types a hook is called with and the protocol a host implements to run hooks. This is the seam an adopter of GraphScene alone uses, so it names nothing of the harness.

**Depends on:** Task 2, which declares the hooks on nodes (`before` / `after`) and in `vocabulary.hooks`. This module needs no graph type. It reads the walk's action types and `NodeRecord`, all of which already exist.

**Where this layer stops.** This task only declares the types:

- **Calling `HookHost`** is Task 5's (`BeforeDispatch`, inside `execute_set`) and Task 6's (every other call, from the run loop).
- **Exporting these names from `graphscene`** and **the README row for this module** are Task 7's. Task 7 owns `graphscene/README.md`, so this task leaves it alone.

### Targets

- `graphscene/src/graphscene/model/hooks.py` (new)
- `graphscene/tests/model/test_hooks.py` (new)

**The contract this task produces.** Tasks 5, 6 and 7 and `devscene-flow-host/src/devscene_flow_host/host/planning_hooks.py` (Task 13) read it.

```python
@dataclass(frozen=True)
class BeforeDispatch:
    kind: ClassVar[Literal["before_dispatch"]] = "before_dispatch"
    dispatch: Dispatch
    seq: int        # the Launch.seq this attempt took
    attempt: int    # the attempt number AttemptBook gave it

@dataclass(frozen=True)
class AfterDispatch:
    kind: ClassVar[Literal["after_dispatch"]] = "after_dispatch"
    record: NodeRecord
    step: Action    # what Walker.next returned for the record

@dataclass(frozen=True)
class BeforeRound:
    kind: ClassVar[Literal["before_round"]] = "before_round"
    dispatch_set: DispatchSet

@dataclass(frozen=True)
class AfterRound:
    kind: ClassVar[Literal["after_round"]] = "after_round"
    passage: RoundPassage
    step: Action    # the step whose passed carries the passage

@dataclass(frozen=True)
class BeforeEnd:
    kind: ClassVar[Literal["before_end"]] = "before_end"
    end: End

HookCall: TypeAlias = BeforeDispatch | AfterDispatch | BeforeRound | AfterRound | BeforeEnd

class HookHost(Protocol):
    """Runs the hooks a graph names, under this module's rule."""
    def provides(self, hook: str) -> bool: ...
    async def run(self, hook: str, call: HookCall) -> None: ...
```

`Dispatch`, `DispatchSet`, `End`, `RoundPassage` and `Action` come from `graphscene.model.walk_actions`. `NodeRecord` comes from `graphscene.model.run_control`. `model` imports only the standard library and `model` (`.claude/context/graphscene.md` → `## The internal layers`).

**Work:**

- [ ] **`model/hooks.py` — the docstring.** Open the module with a docstring stating what it owns. Its *"The rule:"* paragraph covers:
  - **which node kind takes which hook:** a dispatch node takes `before` (`BeforeDispatch`) and `after` (`AfterDispatch`); a round node takes `before` (`BeforeRound`) and `after` (`AfterRound`); a terminal node takes `before` (`BeforeEnd`);
  - **who calls them:** the hooks are run mode's (`graphscene.engine.set_execution`, `graphscene.engine.run_loop`), and `Walker` runs none;
  - **the host's obligations:** a hook may run more than once for the same node, round or end (a retry, a `current` that returns the same step again), so its side effects must be repeatable, as an executor's are. An exception from `run` propagates out of run mode unchanged. `provides` is asked once per declared name before the walk is touched;
  - **the discriminator:** each variant carries a `kind` `ClassVar`, as `graphscene.model.walk_actions` does.

  Its *"Deliberately not covered"* list names three things: what a hook does (the host's), offloading a blocking hook (the host wraps its work in `asyncio.to_thread`, as for an executor), and any hook outside run mode.
- [ ] **`model/hooks.py` — the types.** Declare the five call types, `HookCall` and `HookHost` exactly as the contract above spells them, with no other public name.
- [ ] **`tests/model/test_hooks.py`.** Open with the header *"The rule this file exists to enforce"*. Cover three things:
  - each variant's `kind` is its `ClassVar` value, not a field, which `dataclasses.fields` shows;
  - each variant is frozen: assigning to a field raises `FrozenInstanceError`;
  - an in-test class with `provides` and an `async def run` satisfies `HookHost` structurally, without subclassing. A function typed to take a `HookHost` accepts it under `mypy` strict, and an `asyncio.run` of its `run` records the call it was given.

  Build the actions from `graphscene.model.walk_actions` by hand, as `tests/model/test_walk_actions.py` does.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/model/test_hooks.py` passes.
- `model/hooks.py` imports nothing from `graphscene.engine`, `graphscene.adapters` or `graphscene.facade`. The `graphscene-layers` contract would refuse it.
