### Task 5 — Add the `Walker` with `start`, `next` and `current` in `engine/walker.py`

**Goal:** Give the engine its driver, `Walker(graph, store, host)`. `start` begins a walk (or replaces one), `next` records the outcome of the pending node and advances, and `current` re-returns the saved pending action, so a re-entry resumes through it. `start` and `next` hold the store's lock from before the read until after the write. A `Refused` writes nothing.

**Depends on:** Task 3 and Task 4. This task calls:

- from `graphscene.engine.transitions`: `WalkDraft.fresh(graph)`, `WalkDraft.from_state(state)`, `WalkDraft.freeze() -> WalkState`, `arrive(graph, host, draft, node_id, *, closed_round=(), open_gates=()) -> Step`, `open_round(graph, host, draft, round_id) -> Step` and `follow_edge(graph, host, draft, node_id, edge, *, advance=None, closed_round=(), open_gates=(), held=()) -> Step`;
- from `graphscene.engine.rounds`: `record_gate(graph, host, draft, gate, outcome, detail) -> Step`.

It drives `StateStore.read() -> WalkState | None`, `StateStore.write(state) -> None` and `StateStore.lock() -> AbstractContextManager[None]`, and passes `PredicateHost` through (`graphscene.model.walk_state`). A pending interrupt is the `Interrupt(binding, node, agent, resume, resume_outcome, passed)` stored as `WalkState.pending`.

**Where this layer stops.** The file-backed store is **Task 7's** `FileStateStore`. This task's tests use an in-memory store. Making `Walker` public is **Task 8's**. This module renders nothing and reads no file.

### Targets

- `graphscene/src/graphscene/engine/walker.py` (new)
- `graphscene/src/graphscene/engine/__init__.py`: the docstring's first line only, from "checks over a flow graph" to "checks over a flow graph, and the walk over one". *"The rule:"* is unchanged.
- `graphscene/tests/engine/test_walker.py` (new)

**Work:**

- [ ] **Docstring and `start`.** The module docstring has a *"The rule:"* paragraph:
  - only `start` replaces a saved walk, and it sets every counter and round number to 0;
  - `next` and `current` refuse a walk of another flow;
  - `current` takes no lock and changes nothing;
  - a `Refused` leaves the store unwritten.

  Add a *"Deliberately not covered:"* list: reading round evidence at `start` and the review loop's rules, both the host's.

  `start(self, entry: str | None = None) -> Step`, under `store.lock()`:
  - The entry is `entry or graph.start`.
  - Refuse `f"'{e}' is not an entry of flow '{graph.flow}'"` when it is not in `graph.entries`.
  - Refuse `f"'{e}' is a gate of round '{r}': enter at the round"` when the entry is a gate of a round.
  - Otherwise start from `WalkDraft.fresh(graph)` and `arrive` (a round entry opens its set). On a non-`Refused` step, `store.write(draft.freeze())`.
- [ ] **`next(self, outcome: str, node: str | None = None, detail: str | None = None) -> Step`, under `store.lock()`.** Refuse in this order, with these exact reasons:
  1. `"no walk has started"` when there is no saved state.
  2. `f"the saved walk is of flow '{s.flow}', not '{graph.flow}'"`.
  3. `"the walk has finished"` when `awaiting == "done"`.
  4. While a set is pending:
     - `f"a round's set is pending at '{s.node}': name the gate with node"` when `node` is `None`;
     - otherwise call `record_gate(..., node, outcome, detail)`.
  5. Otherwise:
     - `f"'{node}' is not the pending node '{s.node}'"` when `node` is given and differs;
     - `"detail is recorded only for a gate of an open round"` when `detail` is given.
  6. While an `Interrupt` is pending:
     - `f"the walk is interrupted at '{s.node}': resume with outcome '{ro}'"` unless `outcome == pending.resume_outcome`;
     - when it matches, `arrive(graph, host, draft, pending.resume)`.

     The resume outcome is never looked up under `vocabulary.outcomes`: the interrupt consumes it.
  7. At a pending dispatch node:
     - `f"outcome '{outcome}' is not declared by node '{s.node}'"` when the outcome is not a key of `node.outcomes`;
     - otherwise `follow_edge` that edge.

  Write the frozen draft on every non-`Refused` step.
- [ ] **`current(self) -> Step`.** It takes no lock. It returns `Refused("no walk has started")` for no saved state, the flow refusal above for another flow's walk, and otherwise `state.pending` unchanged. It makes no `write` call.
- [ ] **`test_walker.py`.** Its module docstring opens *"The rule this file exists to enforce"*. It uses an in-test `MemoryStore` (a `StateStore` holding one `WalkState | None`, with a `lock()` that records entry and exit and a `writes` counter) and planted graphs from `graphscene/tests/engine/walk_support.py`. Cover these:
  - every refusal's exact text, each asserting `writes` unchanged;
  - `start` at `graph.start` and at a round entry;
  - `start` replacing a saved walk mid-loop, with counters back to 0;
  - the lock held around `start` and `next` and not taken by `current`;
  - `current` after a `Wait` returning only the unrecorded gates' set;
  - an interrupt resumed with its `resume_outcome` re-dispatching the resume node with its stored prompt variant, while any other outcome is refused;
  - a `Stop` and an `End` followed by `next` refused as finished, and `current` still returning them.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/engine/test_walker.py` passes.
- [ ] `walker.py` imports only `graphscene.engine.transitions`, `graphscene.engine.rounds`, `graphscene.model` and the standard library.
