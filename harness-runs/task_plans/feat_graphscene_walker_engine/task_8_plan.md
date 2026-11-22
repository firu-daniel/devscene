### Task 8 — Make the walker public and drive whole walks, concurrent gates included, through `graphscene`

**Goal:** Expose the walker as a caller sees it, `from graphscene import Walker, FileStateStore, ...`, and prove the whole chain end to end: a graph loaded by `load_graph`, a `Walker` over a `FileStateStore`, and a host answering skips. That includes a round whose gates are recorded from concurrent threads, where exactly one call returns the join.

**Depends on:** Task 5 and Task 7.

- **Task 5's** `graphscene.engine.walker.Walker(graph: FlowGraph, store: StateStore, host: PredicateHost)` has three methods:
  - `start(entry: str | None = None) -> Step`;
  - `next(outcome: str, node: str | None = None, detail: str | None = None) -> Step`;
  - `current() -> Step`.

  A refusal is returned as `Refused(reason)` and writes nothing.
- **Task 7's** `graphscene.adapters.state_file.FileStateStore(path: Path, *, lock_timeout: float = 120.0)`.
- The model types it re-exports are Task 1's, from `graphscene.model.walk_actions`: `GateRecord`, `SkipPassage`, `RoundPassage`, `LedgerPassage`, `Passage`, `Dispatch`, `DispatchSet`, `Wait`, `Interrupt`, `Stop`, `End`, `Refused`, `Action` and `Step`.
- It also re-exports Task 2's, from `graphscene.model.walk_state`: `Awaiting`, `OpenRound`, `WalkState`, `StateStore` and `PredicateHost`.

**Where this layer stops.** No new behaviour lands here: only re-exports, docstrings and the composed suites. `WalkDraft`, the transition functions and the JSON codec stay private.

### Targets

- `graphscene/src/graphscene/facade/__init__.py`
- `graphscene/src/graphscene/__init__.py`
- `graphscene/tests/test_public_surface.py`
- `graphscene/tests/facade/test_walking.py` (new)

**Work:**

- [ ] **Both `__all__` lists.** In `facade/__init__.py` and `__init__.py`, import from each defining module (never from the package root) and append to **both** `__all__` lists, in this order after `"TerminalNode"`:

  `"Walker"`, `"FileStateStore"`, `"StateStore"`, `"PredicateHost"`, `"WalkState"`, `"OpenRound"`, `"Awaiting"`, `"Step"`, `"Action"`, `"Dispatch"`, `"DispatchSet"`, `"Wait"`, `"Interrupt"`, `"Stop"`, `"End"`, `"Refused"`, `"GateRecord"`, `"Passage"`, `"SkipPassage"`, `"RoundPassage"`, `"LedgerPassage"`

  Extend the package root's docstring with one sentence naming the walker and its file store (`.claude/context/graphscene.md` → `## What accompanies a new module`, the public-name row).
- [ ] **`test_public_surface.py`.** Append the same names to `_EXPECTED` in the same order. Bound the model slice in `_DEFINED_IN` to the flow-graph names only, from `_EXPECTED[7:]` to `_EXPECTED[7:28]`, the 21 names from `"FlowGraph"` to `"TerminalNode"`, and add one entry per new name against its defining module:
  - `graphscene.engine.walker` for `Walker`;
  - `graphscene.adapters.state_file` for `FileStateStore`;
  - `graphscene.model.walk_state` for `StateStore`, `PredicateHost`, `WalkState`, `OpenRound` and `Awaiting`;
  - `graphscene.model.walk_actions` for the rest.

  Import those modules at the top. Rename the docstring's "graph-model and checker surface" to "graph-model, checker and walker surface".
- [ ] **`tests/facade/test_walking.py`: whole walks.** Its module docstring opens *"The rule this file exists to enforce"*. It imports only from `graphscene`, as a caller does. It loads `graphscene/tests/fixtures/flow_graph/valid_generic.json` with `load_graph_file`, uses a `FileStateStore(tmp_path / "walk.json")` and an in-test host answering from a dict. Expected values are hand-written from reading the fixture:
  - **Draft, review, publish.** `start()` returns `Dispatch(node="draft", agent="article-writer", prompt=None, ...)` with `round_number=0`. `next("done")` returns a `DispatchSet` of `edit_check` alone, `number=0`, `converging=False`. `next("rejected", node="edit_check", detail="f0")` returns `Dispatch("draft", prompt="rework", round_number=1, counters={"attempt": 1})`, with `closed_round=(GateRecord("edit_check","rejected","f0"),)` and `passed` holding `RoundPassage("review_round", 0, "fail")`. Then `done` and `approved` lead to `End("<finish>", "published", reports=(("edit_check","approved"),))`.
  - **The cap.** Three rejected rounds give `Stop("<halt>", node="review_round", agent=None, reason="limit", summary="the article did not converge in 3 attempts; the gates open when it fired: edit_check", evidence="article", round_counts=("edit_check",))`.
  - **A held crash.** `crashed` at `edit_check` gives `Stop(reason="crash", node="edit_check", held=(GateRecord("edit_check","crashed",None),))`.
  - **A skipped gate.** The host answers `stage_disabled` `True`, so `passed` has `SkipPassage("edit_check","bypassed")`, the round closes `pass` at once, and `End.reports` is `(("edit_check","bypassed"),)`.
  - **`current` across instances.** It re-reads through a new `Walker` and `FileStateStore` on the same path.
- [ ] **`tests/facade/test_walking.py`: concurrency.** Load, through `load_graph`, an in-test copy of the fixture whose `review_round.gates` holds four gates. The extra three are copies of `edit_check` under new ids, and the copy passes every loading stage. Start the walk and `next("done")`. Then record all four gates from four threads at once, each with its own `Walker` and `FileStateStore` on the same path, released together by a `threading.Barrier`. Assert:
  - exactly one result is not a `Wait` (the join);
  - the three `Wait`s together name each gate once as `recorded`;
  - `current()` returns that one result.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` passes.
- [ ] `bash scripts/python-service.sh --package graphscene test tests/facade/test_walking.py` passes.
- [ ] `graphscene.__all__ == graphscene.facade.__all__`, and `build_flow_graph` is still absent from it.
