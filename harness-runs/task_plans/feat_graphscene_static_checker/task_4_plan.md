### Task 4 — Export `static_violations` and hold loading to the static negatives

**Goal:** Make the static checker public as `graphscene.static_violations`, and prove the whole loading path end to end. Every `static_negative_*.json` fixture must be rejected by `load_graph` at stage `"static"`, naming its one path, and a vocabulary failure must never reach the static stage.

**Depends on:** Task 3. It makes `load_graph` run schema → build → vocabulary → static and raise `GraphError("static", found)`, with `Stage` = `Literal["parse", "schema", "vocabulary", "static"]`. Task 2 defines `static_violations(graph: FlowGraph) -> list[Violation]` in `graphscene/src/graphscene/engine/static_check.py`, and Tasks 1 and 2 commit the six fixtures named below. This task changes none of those files.

**Where this task stops.** `reference_violations` (`graphscene/src/graphscene/engine/references.py`) stays unexported: only `static_violations` becomes public. The README is Task 5's. Listing the fixtures in the root `validate:graphscene-schema` script is Task 6's.

### Targets

- `graphscene/src/graphscene/facade/__init__.py`
- `graphscene/src/graphscene/__init__.py`
- `graphscene/tests/test_public_surface.py`
- `graphscene/tests/facade/test_loading.py`

**Work:**

- [ ] `facade/__init__.py`: add `from graphscene.engine.static_check import static_violations`, and insert `"static_violations"` into `__all__` directly after `"vocabulary_violations"`.
- [ ] `graphscene/__init__.py`: import `static_violations` from `graphscene.facade`, and insert `"static_violations"` into `__all__` at the same place, so both lists stay equal and in the same order (`.claude/context/graphscene.md` → `## The public surface`). In the docstring, say the surface also exposes the static checker, `static_violations`, alongside loading.
- [ ] `test_public_surface.py`:
  - add `import graphscene.engine.static_check`;
  - insert `"static_violations"` into `_EXPECTED` after `"vocabulary_violations"`;
  - add `"static_violations": graphscene.engine.static_check` to `_DEFINED_IN`;
  - move the slice that maps the model names from `_EXPECTED[6:]` to `_EXPECTED[7:]`, so `FlowGraph` onward still maps to `graphscene.model.flow_graph`.

  The header's *"graph-model surface"* becomes the graph-model and checker surface.
- [ ] `test_loading.py`: add `_STATIC_NEGATIVES: list[tuple[str, str]]`, each fixture with the one path hand-read from its single change:
  - `("static_negative_node_known.json", "nodes.draft.outcomes.done.to")`
  - `("static_negative_reachable_from_start.json", "nodes.orphan")`
  - `("static_negative_reaches_terminal.json", "nodes.published")`
  - `("static_negative_fail_cycle_capped.json", "nodes.review_round.outcomes.rejected")`
  - `("static_negative_gate_in_round.json", "nodes.review_round.gates[1]")`
  - `("static_negative_round_fan_out.json", "nodes.edit_check.outcomes.approved")`

  Add `test_a_static_negative_is_rejected_at_the_static_stage`, parametrized over that list, asserting `stage == "static"` and that the violation paths equal `[path]`. This also proves each fixture passes the schema and the vocabulary check first. Add `test_a_vocabulary_failure_never_reaches_the_static_stage`: copy `valid_generic.json`, add `nodes.edit_check.outcomes.finished = {"to": "nowhere"}`, and assert `stage == "vocabulary"` with exactly `(Violation("nodes.edit_check.outcomes.finished", "outcome 'finished' is not declared in vocabulary.outcomes"),)`. The `nowhere` reference is never reported. Update the header's rule to name the static negatives and the stage order.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py tests/facade/test_loading.py` passes.
- `bash scripts/typecheck.sh` passes.
- `grep -n "static_violations\|reference_violations" graphscene/src/graphscene/__init__.py graphscene/src/graphscene/facade/__init__.py` shows `static_violations` in each file's import and `__all__`, and `reference_violations` in neither.
