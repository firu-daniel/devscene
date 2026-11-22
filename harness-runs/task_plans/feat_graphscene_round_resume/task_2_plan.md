### Task 2 — Enter a round with recorded gates through `enter_round` in `rounds.py`

**Goal:** Add the engine's half of starting inside a round. `enter_round(graph, host, draft, round_id, records) -> Step` opens the round and records the given gate outcomes as if `next` had recorded them one by one. It then returns either the set of gates still out or, when every due gate is recorded, the join's step.

**Depends on:** Task 1 for the shape only. This task's signature takes the records as `records: tuple[GateRecord, ...]`, which is exactly `RoundResume.records`, the third field of Task 1's `RoundResume(round: str, number: int, records: tuple[GateRecord, ...] = ())`. It does not import `RoundResume`: Task 3 unpacks it.

**Where this layer stops.** `enter_round` assumes its caller has already checked three things. The caller is Task 3's `Walker.start`. The checks are: `round_id` is a round node of `graph`; every record's gate is in that round's `gates`; and no gate appears twice in `records`. The caller has also set `draft.round_numbers[round_id]` to the resumed number. Those checks and their refusal texts are **Task 3's**. This task does not touch `walker.py`, `transitions.py` or `walk_json.py`.

### Targets

- `graphscene/src/graphscene/engine/rounds.py`: `enter_round` and the module docstring.
- `graphscene/tests/engine/test_rounds.py`: the cases below.

**Work:**

- [ ] `rounds.py`: add `enter_round(graph: FlowGraph, host: PredicateHost, draft: WalkDraft, round_id: str, records: tuple[GateRecord, ...]) -> Step`, in this order:
  1. Read `number = draft.round_numbers[round_id]`.
  2. Call `open_round(graph, host, draft, round_id)`, imported from `graphscene.engine.transitions` beside the names already imported there. Return its result unchanged when it is a `Refused` or when `records` is empty.
  3. Find the first record in the round's `gates` order whose gate is not in the opened round's `due`, where "opened" means `draft.open_round` is set and its `round == round_id`. When the round closed at once because no gate was due, treat every record as matching. Return `Refused(f"'{gate}' is skipped in round {number}: a skipped gate carries no record")` for that record.
  4. Call the existing `record_gate(graph, host, draft, r.gate, r.outcome, r.detail)` for each record in the round's `gates` order, returning the first `Refused` unchanged. This reuses its texts `outcome '<o>' is not declared by node '<g>'` and `outcome '<o>' of round gate '<g>' declares neither a verdict nor held`.
  5. If the last call returned a `Wait`, return `draft.pending`, which `record_gate` left as the `DispatchSet` trimmed to the gates still out (assert it is one). Otherwise return the last call's step, which is the join.
- [ ] `rounds.py`: write no second join and no second report recording. The held join (the first held gate's edge in `gates` order), the close and a verdict outcome's edge report all come from `record_gate` and `close_round`, so a resumed round and a stepped round cannot drift.
- [ ] `rounds.py` module docstring: add to *"The rule:"* that `enter_round` opens a round as `open_round` does. It refuses a record for a gate skipped on this arrival, then records each record through `record_gate` in `gates` order. It returns the set of gates still out, or the join's step once every due gate is recorded. Add to *"Deliberately not covered:"* that refusing a record for a gate outside the round, a repeated gate or a negative round number, and setting the round's number, are `graphscene.engine.walker`'s, and that deciding which round and which records is the host's.
- [ ] `test_rounds.py`: add cases over the module's existing two-gate planted graph (`_two_gates`), each starting from `WalkDraft.fresh` with `round_numbers["<round>"]` set to a hand-chosen number such as 2. Each expected value is hand-written from the planted graph:
  - **No records:** the whole set at that number, identical to `open_round`.
  - **One verdict record:** a `DispatchSet` of only the other gate, with `draft.open_round.due` holding both gates and `records` holding the given one.
  - **Both verdict records with one fail:** the round closes fail at once, and `draft.round_numbers` advances to 3.
  - **Both pass:** the round closes pass.
  - **One held record and one verdict record:** the walk takes the held gate's edge. Assert the exact `Stop`, carrying `held` with the held record.
  - **One held record alone:** the walk waits on the other gate.
  - **A record for an undeclared outcome:** the exact `record_gate` text.
  - **A record for a gate whose skip holds** (answered `True` by an `AnswerTable`): the exact skipped text. Also cover the variant where every gate is skipped and the round would close at once.
- [ ] `test_rounds.py` module docstring: extend the rule sentence with the `enter_round` clause. Note that refusals for a foreign or repeated gate are the walker's suite, and list that under *Deliberately not covered*.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_rounds.py` passes, the one test file this task edits, and every new case asserts the exact step or exact `Refused` text.
- `rounds.py` imports only `graphscene.engine.transitions`, `graphscene.model.*` and the standard library. No `graphscene.adapters` import, per `.claude/context/graphscene.md` → `## The internal layers`.
- Reading `enter_round`, no outcome lookup, report update or held-edge selection appears outside its calls to `open_round` and `record_gate`.
