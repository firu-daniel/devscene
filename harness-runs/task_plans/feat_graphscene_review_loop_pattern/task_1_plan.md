### Task 1 — Add the review-loop pattern module `engine/review_loop.py`

**Goal:** Give the engine one place that decides whether a round is a review loop, and that holds the pattern's own walk rule (`converging`). Every later reader of a round's `writer`, `counter` and `convergingFrom` calls this module instead of reading the fields.

**Where this task stops.** This task creates the module and its suite and changes no caller. Task 2 moves the walk's dispatch onto it (`engine/transitions.py`). Task 3 moves checks 8 and 9 onto it (`engine/static_check.py`). Task 4 makes the three fields optional in the schema, the model and the builder. The module must type-check under `mypy` `strict` **both before and after Task 4**, and Task 4 does not edit it. That is why the decision takes the three values typed `str | None` / `str | None` / `int | None`, never the `RoundNode` attributes' current non-optional types.

### Targets

- `graphscene/src/graphscene/engine/review_loop.py` (new)
- `graphscene/tests/engine/test_review_loop.py` (new) — the suite a new module lands with (`.claude/context/graphscene.md` → `## What accompanies a new module`)

**Work:**

- [ ] `review_loop.py`, module docstring (`.claude/context/graphscene.md` → `## Naming and layout`):
  - **"The rule:"** a round node is a review loop when it declares `writer`, `counter` and `convergingFrom`, which the schema requires together. A review loop's writer is dispatched with its round's number. Its gates are dispatched with `converging`, which is `counter >= convergingFrom`. Its shape is held by the review-loop clauses of checks 8 and 9 (`graphscene.engine.static_check`). A round that does not declare `writer` is a plain fan-out and join.
  - **"Deliberately not covered:"** the round itself, which is engine-generic for any round (`graphscene.engine.transitions`, `graphscene.engine.rounds`): fan-out, the join and the held join, the round number, and the closed round carried on an edge and on an interrupt. Also not covered: what a host does with `plan`, `revisionNote` and a dispatch node's `findingsFolder`.
- [ ] `review_loop.py`, the code. It imports only `graphscene.model.flow_graph` and the standard library (`.claude/context/graphscene.md` → `## The internal layers`, `engine` row):
  - `@dataclass(frozen=True) class ReviewLoop` with the fields `round: str` (the round node's id), `writer: str`, `counter: str` and `converging_from: int`.
  - `review_loop(node: RoundNode) -> ReviewLoop | None` delegates to a private `_loop(round_id: str, writer: str | None, counter: str | None, converging_from: int | None) -> ReviewLoop | None`. `_loop` returns `None` when any of the three is `None`, and the `ReviewLoop` otherwise.
  - `review_loops(graph: FlowGraph) -> tuple[ReviewLoop, ...]` returns every round node's review loop, in `nodes` key order.
  - `is_converging(loop: ReviewLoop, counters: Mapping[str, int]) -> bool` returns `counters[loop.counter] >= loop.converging_from`.
  - Nothing raises, and nothing here is made public: `graphscene/src/graphscene/__init__.py` and `graphscene/tests/test_public_surface.py` do not change.
- [ ] `test_review_loop.py`:
  - Open with the *"The rule this file exists to enforce"* docstring (`.claude/context/conventions.md` → `## The testing bar`).
  - Plain `-> None` test functions with no mocking. Graphs are built through `graphscene.adapters.builder.build_flow_graph`, from `graphscene/tests/fixtures/flow_graph/valid_generic.json` read off `__file__`, or from an in-test planted mapping.
  - Cases, each expected value hand-written from reading the graph:
    - `review_loop` of `valid_generic.json`'s `review_round` is `ReviewLoop("review_round", "draft", "attempt", 1)`;
    - `review_loops` of a planted two-round graph returns both loops in `nodes` key order;
    - `is_converging` is `False` one below `converging_from` and `True` at it;
    - `_loop` returns `None` when `writer`, `counter` or `converging_from` is `None`, with one case per argument. The absent case cannot be planted as a built graph until Task 4, so this case is how this task pins it.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_review_loop.py` passes.
- The module imports nothing outside `graphscene.model` and the standard library.
- No file other than the two targets is in the unit's diff.
