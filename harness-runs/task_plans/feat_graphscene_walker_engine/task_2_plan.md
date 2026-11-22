### Task 2 — Declare `WalkState` and the `StateStore` and `PredicateHost` protocols in `model/walk_state.py`

**Goal:** Give `model` the walk's persisted position as a plain type, and the two `typing.Protocol`s the engine drives and an adapter or host implements. `.claude/context/graphscene.md` → `## The internal layers` puts all three in `model`, so an adapter implements them without importing the engine.

**Depends on:** Task 1. This task imports, from `graphscene.model.walk_actions`:

- `Action`: `Dispatch | DispatchSet | Wait | Interrupt | Stop | End`;
- `GateRecord(gate: str, outcome: str, detail: str | None)`.

It defines no action type of its own.

**Where this layer stops.** These are types and protocols only. The engine that reads and replaces a `WalkState` is Tasks 3–5. The file-backed `StateStore` is Task 7's `FileStateStore`, and the JSON form of a `WalkState` is Task 6's. A `PredicateHost` is implemented by the caller; the tests' own hosts are Task 3's and Task 8's.

### Targets

- `graphscene/src/graphscene/model/walk_state.py` (new)
- `graphscene/tests/model/test_walk_state.py` (new)

**Work:**

- [ ] **`walk_state.py` module docstring.** State what it owns, with a *"The rule:"* paragraph:
  - `WalkState` is a position, never a history;
  - it is replaced whole and never mutated;
  - `pending` is exactly what `current` returns.
- [ ] **The state types.** Declare these, every class `@dataclass(frozen=True)`:
  - `Awaiting: TypeAlias = Literal["dispatch", "set", "interrupt", "done"]`.
  - `OpenRound(round: str, number: int, due: tuple[str, ...], records: Mapping[str, GateRecord])`. `due` is the gates dispatched in this set, in the round's `gates` order. `records` is keyed by gate and holds verdict and held outcomes alike.
  - `WalkState(flow: str, node: str, awaiting: Awaiting, pending: Action, counters: Mapping[str, int], round_numbers: Mapping[str, int], open_round: OpenRound | None, prompts: Mapping[str, str], reports: Mapping[str, str], skipped: Mapping[str, str])`. The fields mean:
    - `node`: the pending node; it is the round node while a set is pending.
    - `prompts`: the prompt variant last routed to each dispatch node. An interrupt's resume re-dispatches with it.
    - `reports`: slot → status recorded so far.
    - `skipped`: node → the predicate name that skipped it, kept so a cap's `round_counts` can drop a node whose predicate has `in_round_counts` false.
- [ ] **`StateStore` Protocol.** It has three methods: `read(self) -> WalkState | None` (`None` when no walk is saved), `write(self, state: WalkState) -> None` and `lock(self) -> contextlib.AbstractContextManager[None]`. The docstring states the contract the engine relies on: `write` replaces the whole state atomically, so a `read` without the lock is never torn; and `lock` is exclusive across processes and threads and released on every exit path.
- [ ] **`PredicateHost` Protocol.** It has one method, `answer(self, predicate: str, node: str) -> bool | None`. `True` skips, `False` does not, and `None` means "cannot answer", which the walk refuses rather than guesses. The docstring says the host decides what a predicate means and the engine never reads configuration (`graphscene/README.md` → `## The boundary`).
- [ ] **`test_walk_state.py`** (module docstring opening *"The rule this file exists to enforce"*):
  - `WalkState` and `OpenRound` are frozen;
  - a small in-test class with `read` / `write` / `lock`, and one with `answer`, are accepted by `mypy` where a `StateStore` / `PredicateHost` is annotated, by assigning each to an annotated local. A structural check is what `mypy` grades, so no `runtime_checkable` is needed.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/model/test_walk_state.py` passes.
- [ ] `walk_state.py` imports only the standard library and `graphscene.model`.
