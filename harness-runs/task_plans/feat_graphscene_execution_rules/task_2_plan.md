### Task 2 — Add the per-set safety contract `clear_set` and the run-level `UndeliveredBreaker`

**Goal:** Add the two rules over counts that guard a dispatch set. `clear_set` is the safety contract checked before anything of a set goes out: STOP, PAUSE, and a cap over the whole set. `UndeliveredBreaker` is the separate run-level rule that trips after a number of consecutive sets that each had an `undelivered` result.

**Depends on:** Task 1, which declares these in `graphscene/src/graphscene/model/run_control.py`, used here exactly as follows:

- `ExecutionLimits`: `dispatch_cap: int | None` only, already validated, read by `clear_set`. `ExecutionLimits` carries no undelivered-set limit, and `UndeliveredBreaker` reads nothing from it: the breaker's limit is its own constructor argument;
- `RunSignals`: `stop_requested() -> bool` and `pause_requested() -> bool`;
- `DispatchCounter`: `total() -> int` and `increment() -> int`;
- `Halt(reason: HaltReason, detail: str)`, where `HaltReason` is `"stop" | "pause" | "cap" | "undelivered"`.

`Dispatch` is `graphscene.model.walk_actions.Dispatch`.

**Where this layer stops.** `clear_set` only checks: it never calls `DispatchCounter.increment()`. Counting each launch, and taking its number as the `Launch.seq`, is Task 4's `execute_set`. The breaker counts what it is told. Deciding whether a set had an `undelivered` result, and halting when the breaker trips, is also Task 4's. Persisting the breaker's count across processes is the host's. The public-surface entries and the README rows for both modules are Task 5's. Both modules sit in `engine` and import only `graphscene.model` and the standard library (`.claude/context/graphscene.md` → `## The internal layers`).

### Targets

- `graphscene/src/graphscene/engine/safety.py` (new)
- `graphscene/src/graphscene/engine/breaker.py` (new)
- `graphscene/tests/engine/test_safety.py` (new)
- `graphscene/tests/engine/test_breaker.py` (new)

**Work:**

- [ ] `safety.py` → `clear_set(dispatches: Sequence[Dispatch], signals: RunSignals, counter: DispatchCounter, limits: ExecutionLimits) -> Halt | None`. `None` means the set may go out. Its docstring's *"The rule:"* states the order, which follows the pilot's `### Item 4` → **On the script-driven path.** (`docs/flow-graph-walker.md`):
  1. Call `stop_requested()` once per dispatch, before anything else. If any call is true, return `Halt("stop", "stop requested before a set of <n>")`.
  2. Then call `pause_requested()` once. If true, return `Halt("pause", "pause requested before a set of <n>")`.
  3. Then, when `dispatch_cap` is set and `counter.total() + n > dispatch_cap`, return `Halt("cap", "<total> dispatched; a set of <n> (<node ids joined by ', '>) would pass the cap <cap>")`.

  No halt ever sends part of a set. An empty `dispatches` raises `ValueError("clear_set: a set holds at least one dispatch")`. The docstring adds that a STOP or PAUSE raised while a set is out is honoured by the next `clear_set`, so a running set is never cancelled, and that a retry pass is a set like any other.
- [ ] `breaker.py` → `class UndeliveredBreaker`:
  - `__init__(self, limit: int = 3)` raises `ValueError("UndeliveredBreaker: limit must be >= 1, got <limit>")` below 1 (written `not limit >= 1`). `3` is GraphScene's default, equal to the pilot's three undelivered sets; the host passes its own value here, and this argument is the limit's **only** source.
  - `observe(self, undelivered: bool) -> int`: an undelivered set adds one strike and a delivered set resets the strikes to 0; it returns the strikes.
  - `limit` property (read-only), `strikes` property, and `tripped` property (`strikes >= limit`).
  - `reset(self) -> None`.

  The docstring's *"The rule:"* states that the breaker counts consecutive sets, not sessions, that a delivered set resets it, that it is independent of every node's attempts, and that its limit is set at construction and nowhere else (`ExecutionLimits` carries none). *"Deliberately not covered:"* lists persisting the count, and what a host does once it trips.
- [ ] `test_safety.py`. Its header is the *"The rule this file exists to enforce"* docstring. In-test `RunSignals` and `DispatchCounter` classes record their calls. Cases:
  - STOP halts and asks `pause_requested` nothing;
  - STOP is asked once per dispatch;
  - PAUSE halts after STOP is clear;
  - a set that would pass the cap halts and `increment` is never called;
  - a set that exactly reaches the cap clears;
  - no cap means any total clears;
  - the empty-set refusal.

  Every `Halt` is asserted with its hand-written detail text.
- [ ] `test_breaker.py`. Same header rule. Cases:
  - `UndeliveredBreaker()` has `limit == 3`, and its third consecutive undelivered set trips it;
  - `UndeliveredBreaker(2)` trips on the second consecutive undelivered set, not the third;
  - a delivered set in between resets the strikes;
  - `reset` clears a tripped breaker;
  - the limit refusal, with its exact text.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_safety.py` passes.
- `bash scripts/python-service.sh --package graphscene test tests/engine/test_breaker.py` passes.
- Neither module imports from `graphscene.adapters` or `graphscene.facade`, and `clear_set` contains no call to `increment`.
