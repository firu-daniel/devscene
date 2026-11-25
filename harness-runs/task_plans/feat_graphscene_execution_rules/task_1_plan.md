### Task 1 — Add the execution-rule types and host protocols in `model/run_control.py`

**Goal:** Give the `model` layer the plain types and protocols that the execution rules in Tasks 2–4 compute over: the host-supplied limits with GraphScene defaults, the three host protocols (signals, dispatch counter, launch sink), the observation row, the run-level halt, a node's record, a node's settlement, and the result of one executed set.

**Where this layer stops.** This module declares types and protocols only. It decides nothing, holds no counter and runs nothing. `clear_set` and `UndeliveredBreaker` are Task 2's, `AttemptBook` is Task 3's and `execute_set` is Task 4's. Making these names public and adding their README rows is Task 5's, because `graphscene/src/graphscene/__init__.py`, `graphscene/src/graphscene/facade/__init__.py`, `graphscene/tests/test_public_surface.py` and `graphscene/README.md` are shared files that only Task 5 edits. Rules from `.claude/context/graphscene.md` that bind this task: every class is a `@dataclass(frozen=True)`, each variant carries its discriminator as a `ClassVar[Literal[...]]` named `kind`, and the `model` layer imports only the standard library and `graphscene.model` (`## The model and its wire forms`, `## The internal layers`). A protocol that a host implements and the engine drives is declared in `model` (*"A `typing.Protocol` that an adapter implements and the engine drives is declared in `model`"*).

### Targets

- `graphscene/src/graphscene/model/run_control.py` (new)
- `graphscene/tests/model/test_run_control.py` (new)

**Work:**

- [ ] Write the module docstring in the form `.claude/context/graphscene.md` → `## Naming and layout` requires. It opens by stating what the module owns. Its *"The rule:"* paragraph states: the limits are the host's to pass and the defaults are GraphScene's, not any host's constants; `undelivered` re-dispatches use up no attempt; a halt is returned, never raised; `NodeResult` carries no usage, and a host joins usage to a `Launch` from its own executor's usage sink. Its *"Deliberately not covered:"* list names where STOP and PAUSE live, what the counter counts and where a row is written (the host's), and the run loop (#484).
- [ ] Declare, in this order:
  - `HaltReason: TypeAlias = Literal["stop", "pause", "cap", "undelivered"]`.
  - `ExecutionLimits`, frozen, with fields and defaults `max_attempts: int = 3`, `backoff_seconds: float = 60.0`, `dispatch_cap: int | None = None`, `undelivered_sets: int = 3`, `stall_seconds: float | None = None`. Its `__post_init__` raises `ValueError` with exactly `ExecutionLimits: <field> must be <condition>, got <value>`, where `<condition>` is `>= 1` for `max_attempts`, `undelivered_sets` and a set `dispatch_cap`, `>= 0` for `backoff_seconds`, and `> 0` for a set `stall_seconds`. Each comparison is written as `not value >= bound` (or `not value > 0`) so that a NaN is refused, as `graphscene/src/graphscene/adapters/stub_executor.py` → `_check_delay` does.
- [ ] Declare the three host protocols as `typing.Protocol`:
  - `RunSignals`, with `stop_requested(self) -> bool` and `pause_requested(self) -> bool`.
  - `DispatchCounter`, with `total(self) -> int` (sessions launched so far) and `increment(self) -> int` (counts one launch and returns the new total).
  - `LaunchSink`, with `record(self, launch: Launch) -> None`.
- [ ] Declare the frozen value types:
  - `Launch(seq: int, node: str, agent: str, attempt: int, max_attempts: int, result: NodeResult)`, with `NodeResult` imported from `graphscene.model.execution`.
  - `Halt(reason: HaltReason, detail: str)`, with `kind = "halt"`.
  - `NodeRecord(node: str, outcome: str, detail: str | None)`: exactly the arguments a caller passes to `Walker.next(outcome, node, detail)`.
  - The settlement variants `Recorded(record: NodeRecord)`, `kind = "recorded"`; `Retry(node: str, attempt: int, reason: str)`, `kind = "retry"`, where `attempt` is the attempt number the re-dispatch will be; and `Redispatch(node: str, reason: str)`, `kind = "redispatch"`. Then `Settlement: TypeAlias = Recorded | Retry | Redispatch`.
  - `SetResult(records: tuple[NodeRecord, ...], halt: Halt | None)`.
- [ ] `graphscene/tests/model/test_run_control.py`. Its module docstring opens with *"The rule this file exists to enforce"* (`.claude/context/conventions.md` → `## The testing bar`). Cases, as plain `-> None` functions:
  - every class is frozen;
  - each `kind` is the literal above;
  - `ExecutionLimits()` equals the hand-written defaults `3`, `60.0`, `None`, `3`, `None`;
  - one parametrized refusal per field, plus a NaN case, asserting the exact `ValueError` text;
  - in-test classes satisfying `RunSignals`, `DispatchCounter` and `LaunchSink` structurally, assigned to annotated locals so that `mypy` grades them, as `graphscene/tests/model/test_execution.py` does.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/model/test_run_control.py` passes.
- `bash scripts/typecheck.sh` reports no failure in either new file.
- The module imports only the standard library, `graphscene.model.execution` and `graphscene.model.walk_actions` if needed, and nothing from `engine` or `adapters`.
