### Task 1 — Declare the walk's actions and passages in `model/walk_actions.py`

**Goal:** Give `model` the plain, immutable types a walk step returns. These are what the engine produces, what the state stores as its pending action, and what a host acts on. The module imports only the standard library and `graphscene.model.flow_graph`.

**Where this layer stops.** These are types only. No function here computes a value. Building them is Task 3's (`engine/transitions.py`) and Task 4's (`engine/rounds.py`). Storing one as the pending action is Task 2's `WalkState.pending`. Serializing them is Task 6's (`adapters/walk_json.py`). Making them public is Task 8's.

### Targets

- `graphscene/src/graphscene/model/walk_actions.py` (new)
- `graphscene/tests/model/test_walk_actions.py` (new)

**Work:**

- [ ] **Module and passage types.** Create `walk_actions.py` opening with a docstring that states what it owns: the steps a walk returns and the passages it records. Add a *"The rule:"* paragraph: every class is a `@dataclass(frozen=True)`, sequences are `tuple`s, mappings are `MappingProxyType` over a fresh `dict`, and each variant carries its discriminator as a `ClassVar[Literal[...]]` named `kind`, as `graphscene/src/graphscene/model/flow_graph.py` → `DispatchNode.kind` does. Declare these types:
  - `GateRecord(gate: str, outcome: str, detail: str | None)`: what one gate of a round returned, with the host's opaque detail, such as a findings path.
  - `SkipPassage(node: str, status: str)`, kind `"skip"`: `status` is the skipping predicate's `records`.
  - `RoundPassage(round: str, number: int, verdict: Verdict)`, kind `"round"`, with `Verdict` imported from `graphscene.model.flow_graph`.
  - `LedgerPassage(entry: str)`, kind `"ledger"`.
  - `Passage: TypeAlias = SkipPassage | RoundPassage | LedgerPassage`.
- [ ] **Action types.** Declare each with exactly these fields, in this order:
  - `Dispatch`, kind `"dispatch"`: `node: str`, `agent: str`, `prompt: str | None`, `counters: Mapping[str, int]`, `round_number: int | None`, `converging: bool | None`, `closed_round: tuple[GateRecord, ...]`, `passed: tuple[Passage, ...]`.
  - `DispatchSet`, kind `"set"`: `round: str`, `number: int`, `dispatches: tuple[Dispatch, ...]`, `passed: tuple[Passage, ...]`.
  - `Wait`, kind `"wait"`: `round: str`, `recorded: GateRecord`, `pending: tuple[str, ...]`.
  - `Interrupt`, kind `"interrupt"`: `binding: str`, `node: str`, `agent: str | None`, `resume: str`, `resume_outcome: str`, `passed: tuple[Passage, ...]`.
  - `Stop`, kind `"stop"`: `binding: str`, `node: str`, `agent: str | None`, `reason: str`, `summary: str | None`, `evidence: str | None`, `round_counts: tuple[str, ...]`, `held: tuple[GateRecord, ...]`, `closed_round: tuple[GateRecord, ...]`, `passed: tuple[Passage, ...]`.
  - `End`, kind `"end"`: `binding: str`, `node: str`, `reports: tuple[tuple[str, str], ...]`, `passed: tuple[Passage, ...]`.
  - `Refused`, kind `"refused"`: `reason: str`.
  - `Action: TypeAlias = Dispatch | DispatchSet | Wait | Interrupt | Stop | End` and `Step: TypeAlias = Action | Refused`.
- [ ] **Field meanings in the docstring**, so Task 3's and Task 4's implementers read one source:
  - `agent` is `None` when `node` is a round node.
  - `evidence` is a `paths` **key**, never a resolved path.
  - `round_counts` holds node ids, never counts: counting files is the host's.
  - `End.reports` is `(slot, status)` pairs in the graph's `reports` order.
  - A `Dispatch` inside a `DispatchSet` carries `passed=()`, and the set carries the passages.
  - Add a *"Deliberately not covered:"* list. Heartbeats and path templates are rendered by the host.
- [ ] **`test_walk_actions.py`.** Its module docstring opens *"The rule this file exists to enforce"*. Add plain `-> None` test functions with no mocking that assert:
  - every class is frozen: assigning a field raises `dataclasses.FrozenInstanceError`;
  - each `kind` value is the literal above and is a class attribute, not a field (`dataclasses.fields` does not list it);
  - `Dispatch.counters` given as a `MappingProxyType` stays read-only.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/model/test_walk_actions.py` passes.
- [ ] `walk_actions.py` imports nothing outside the standard library and `graphscene.model.flow_graph`.
