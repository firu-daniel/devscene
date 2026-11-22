### Task 6 — Load and walk the plain-round fixture through the public surface

**Goal:** Show, as a caller of `graphscene` sees it, that a graph with no review loop loads and walks end to end, and that loading refuses a review loop missing part of its group at the schema stage.

**Depends on:**
- Task 4, which adds `graphscene/tests/fixtures/flow_graph/valid_plain_round.json` and `graphscene/tests/fixtures/flow_graph/schema_negative_writer_without_counter.json`. The second is `valid_generic.json` with `nodes.review_round.counter` removed, which the schema reports at `nodes.review_round`. Task 4 also makes `RoundNode.writer` / `.counter` / `.converging_from` `None` on a plain round.
- Task 4's description of `valid_plain_round.json`:
  - `intake` routes `accepted` → round `checks`, `rejected` → `discarded`, and `crashed` → `<halt>`/`crash`;
  - gates `lint` and `license` route `accepted` and `rejected` → `checks`;
  - `checks` routes `accepted` → terminal `published` and `rejected` → `{"binding": "<halt>", "reason": "failed"}`;
  - no counters, paths, reports or predicates.
- Tasks 2 and 3, which give a plain round's gates `converging` `None` and leave the review-loop clauses off it.

**Where this task stops.** This task changes no source module. Listing the new fixtures in the root `validate:graphscene-schema` scripts is Task 8's.

### Targets

- `graphscene/tests/facade/test_loading.py`
- `graphscene/tests/facade/test_walking.py`

**Work:**

- [ ] `test_loading.py`:
  - Add `("schema_negative_writer_without_counter.json", "nodes.review_round")` to `_SCHEMA_NEGATIVES`, the path hand-read from the fixture's one change.
  - Add a case: `load_graph` of `valid_plain_round.json` returns a `FlowGraph` whose `nodes["checks"]` is a `RoundNode` with `writer`, `counter` and `converging_from` `None`.
  - Restate the header docstring's list of what loads to include the plain-round fixture.
  - Names are imported from `graphscene`, as the file does today.
- [ ] `test_walking.py`: a case that walks `valid_plain_round.json` through `Walker` and a `FileStateStore` under `tmp_path`, importing from `graphscene` only. Expected values are hand-written from the fixture and the engine docstrings:
  - `start()` returns the `Dispatch` of `intake` with `round_number=None` and `converging=None`.
  - `next("accepted")` returns a `DispatchSet` for `checks` with `number=0`. It carries the `Dispatch`es of `lint` and then `license`, each with `round_number=0`, `converging=None`, `closed_round=()` and `passed=()`.
  - `next("accepted", node="lint")` returns a `Wait` whose `pending` is `("license",)`.
  - `next("rejected", node="license")` returns a `Stop` with:
    - `binding="<halt>"`, `node="checks"`, `agent=None` and `reason="failed"`;
    - `closed_round` equal to `(GateRecord("lint", "accepted", None), GateRecord("license", "rejected", None))`;
    - `round_counts=()` and `held=()`;
    - `passed=(RoundPassage("checks", 0, "fail"),)`.
- [ ] `test_walking.py`: restate its header docstring's rule to cover a walk with no review loop. No existing case changes.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/facade/test_loading.py` passes.
- `bash scripts/python-service.sh --package graphscene test tests/facade/test_walking.py` passes.
- The walk writes only the state file and its `<name>.lock` sibling under `tmp_path`, never inside the checkout.
