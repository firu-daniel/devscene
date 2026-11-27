### Task 3 — Refuse a node hook that `vocabulary.hooks` does not declare

**Goal:** Extend GraphScene's vocabulary check so that every hook name a node uses is one the graph declares under `vocabulary.hooks`. A graph that names an undeclared hook is refused at loading's vocabulary stage, as an undeclared predicate already is.

**Depends on:** Task 2, which built these model attributes:

- `Vocabulary.hooks: Mapping[str, HookDeclaration] | None`;
- `DispatchNode.before` and `DispatchNode.after`;
- `RoundNode.before` and `RoundNode.after`;
- `TerminalNode.before`, each `tuple[str, ...] | None`.

This task reads them and adds nothing to the model.

**Where this layer stops.** This check is static. Two things belong to Task 6, which raises its own `ValueError` before the walk is touched:

- whether the host *provides* a declared hook;
- what a hook does.

### Targets

- `graphscene/src/graphscene/engine/vocabulary.py`
- `graphscene/tests/engine/test_vocabulary.py`

**Work:**

- [ ] **`vocabulary.py`.** For each node, after everything the node already reports, report its `before` names in order and then its `after` names in order. A terminal node has only `before`.
  - **A name not in `graph.vocabulary.hooks`** is reported as `Violation(f"nodes.{node_id}.before[{i}]", f"hook '{name}' is not declared in vocabulary.hooks")`, and likewise with `.after[{i}]`.
  - **An absent `vocabulary.hooks`** (`None`) declares no hook.
  - **The module docstring:**
    - add this ordering to *"in document order"* (after a terminal's `binding`, the node's `before` then `after` hook names);
    - add *"every hook name a node uses is declared"* to the rule;
    - rename *"format-4"* to *"format-5"* in both places.
- [ ] **`test_vocabulary.py`.**
  - Add four planted cases, each through `_graph` and each asserting the exact `Violation` list: an undeclared `before` on a dispatch node, an undeclared `after` on a round node, an undeclared `before` on a terminal node, and a graph naming a hook with no `vocabulary.hooks` at all.
  - Add one clean case in which every named hook is declared and nothing is reported.
  - Bump the planted mapping's `formatVersion` to 5.

  Write each expected path and reason by hand from the planted graph.
  - **Deviations from plan:** `_graph`'s planted mapping already carried `"formatVersion": 5` at this task's base commit (Task 2 raised it), so the bump was a no-op and no edit was made for it.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_vocabulary.py` passes.
- `valid_hooks.json`, the fixture Task 2 created with declared hooks used on a dispatch, a round and a terminal node, produces no vocabulary violation. Add a case in `test_vocabulary.py` asserting that `vocabulary_violations` of the built `valid_hooks.json` is `[]`.
