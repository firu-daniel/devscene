### Task 3 — Give `Walker.start` a keyword-only `resume` and its refusals

**Goal:** Let a host start a walk inside a round with `Walker.start(entry=None, *, resume: RoundResume | None = None) -> Step`. With `resume=None` nothing changes. With a resume, `start` checks the resume and refuses what it cannot place. It then sets that round's number on a fresh draft and either enters the round with its records or arrives at the entry as today. Every counter stays at 0.

**Depends on:**

- **Task 1:** `RoundResume(round: str, number: int, records: tuple[GateRecord, ...] = ())` in `graphscene.model.walk_state`.
- **Task 2:** `enter_round(graph, host, draft, round_id, records: tuple[GateRecord, ...]) -> Step` in `graphscene.engine.rounds`. It assumes `round_id` is a round node, every record's gate is in its `gates`, no gate repeats, and `draft.round_numbers[round_id]` is already set. It refuses a skipped gate's record and an outcome `record_gate` refuses, and returns the set still out or the join's step.

This task makes `enter_round`'s preconditions true and owns the refusal texts for them.

**Where this layer stops.** The name becomes public, and the end-to-end walk through `FileStateStore` runs, in **Task 4**. This task's suite drives `graphscene.engine.walker.Walker` over its in-test `MemoryStore`.

### Targets

- `graphscene/src/graphscene/engine/walker.py`: `start`'s signature, its checks and the module docstring.
- `graphscene/tests/engine/test_walker.py`: the cases below.

**Work:**

- [ ] `walker.py` `start`: add the keyword-only `resume: RoundResume | None = None`, imported from `graphscene.model.walk_state`, and `enter_round` from `graphscene.engine.rounds`. Inside the existing lock, after the two existing entry refusals and before any draft is built, refuse in this order, each as a returned `Refused` with exactly this text. `e` is the resolved entry and `r`, `n` are `resume.round`, `resume.number`:
  1. `r` is not a `RoundNode` in `graph.nodes`: `'{r}' is not a round of flow '{graph.flow}'`.
  2. `n < 0`: `round number {n} of round '{r}' is below 0`.
  3. `resume.records` is non-empty and `e != r`: `records of round '{r}' are given, but the walk enters at '{e}'`.
  4. For each record in the given order, a gate not in that round's `gates`: `'{gate}' is not a gate of round '{r}'`.
  5. For each record in the given order, a gate already seen earlier in `records`: `a second record for '{gate}' in round '{r}'`.
- [ ] `walker.py` `start`: build the draft with `WalkDraft.fresh(graph)` as today, then set `draft.round_numbers[r] = n`. Set no counter: they stay at 0, matching bash `start`. If `e == r`, take the step from `enter_round(graph, self.host, draft, e, resume.records)`. Otherwise take it from `arrive(...)` as today. That second branch covers bash's writer entry, where the writer's `Dispatch.round_number` reads the resumed number. Write only a step that is not `Refused`, as today.
- [ ] `walker.py` module docstring, *"The rule:"*: replace *"Only `start` replaces a saved walk, and it sets every counter and round number to 0."* with a sentence saying only `start` replaces a saved walk. It sets every counter to 0 and every round number to 0 except the round a `RoundResume` names, which takes its `number`. Entering that round with records records them as `next` would. Add the refusal of a resume it cannot place. Keep *"Reading round evidence at `start`: the host's."* under *Deliberately not covered*, and widen it to *"which round to resume and whether its records are consistent"*.
- [ ] `test_walker.py`: add cases over the module's `_graph()` (writer `draft`, round `review_round` of `g1` then `g2`). Override `entries` where an entry is needed. Each expected value is hand-written:
  - **Partial resume:** `start("review_round", resume=RoundResume("review_round", 2, (GateRecord("g1", "approved", "f/review_2.md"),)))` returns a `DispatchSet` of `g2` alone at number 2. `current()` re-returns it, and a following `next("approved", node="g2")` closes the round pass.
  - **Resume with every gate recorded, one `rejected`:** closes fail at once and returns the writer's `rework` dispatch with `round_number` 3 and the counter `attempt` at 1.
  - **Resume at the writer entry** with `RoundResume("review_round", 4)`: the `draft` dispatch carries `round_number=4` and `attempt` 0.
  - **A resume that replaces a saved walk mid-loop:** the counter is back at 0 and the round number is the resumed one.
  - **The five refusals above**, each with its exact text and with `store.writes` unchanged afterwards.
  - **A skipped-gate record** (an `AnswerTable` answering the gate's skip `True`, `_graph(skip=True)`): Task 2's exact text, with nothing written.
- [ ] `test_walker.py` module docstring: replace *"with every counter and round number at 0"* with the new rule: every counter at 0, and every round number at 0 except a resumed round's. Name the resume refusals among what `start` refuses with exact text.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_walker.py` passes, the one test file this task edits. Every existing case still passes unchanged, which shows the `resume=None` path behaves as before.
- Every refusal case asserts `store.writes` is the same before and after the call: the story index's third `Top risks:` entry.
- `walker.py` still imports only `graphscene.engine.*`, `graphscene.model.*` and the standard library.
