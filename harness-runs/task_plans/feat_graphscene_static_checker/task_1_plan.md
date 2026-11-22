### Task 1 — Add the reference check `reference_violations` over `FlowGraph` in `engine/references.py`

**Goal:** Add the check the builder left to "a later static checker": every node, counter, path, report-slot and prompt name a built `FlowGraph` uses must exist. It is `reference_violations(graph: FlowGraph) -> list[Violation]` in a new `engine` module, with its own suite and one committed fixture.

**Where this task stops.** This module is **not public** and is **not wired into loading**. Task 2 calls it from `static_violations` (`graphscene/src/graphscene/engine/static_check.py`), which returns these violations alone when there are any. Task 3 makes `load_graph` run `static_violations`, and Task 4 exports `static_violations`, not this function. Binding, outcome and predicate names are the vocabulary check's (`graphscene/src/graphscene/engine/vocabulary.py`) and are not re-checked here. Reachability, termination, caps and round shape are Task 2's.

### Targets

- `graphscene/src/graphscene/engine/references.py` (new)
- `graphscene/tests/engine/test_references.py` (new), the module's own suite (`.claude/context/graphscene.md` → `## What accompanies a new module`)
- `graphscene/tests/fixtures/flow_graph/static_negative_node_known.json` (new)

**Work:**

- [ ] `references.py` imports only `graphscene.model.errors` (`Violation`), `graphscene.model.flow_graph` and the standard library (`engine` may import `model` only, `graphscene/pyproject.toml` → contract `graphscene-layers`). It opens with a module docstring stating what it owns and a *"The rule:"* paragraph: every node, counter, path, report-slot and prompt name the graph uses exists, `start` is listed in `entries`, and each violation's reason opens with its check id. Add a *"Deliberately not checked:"* list:
  - binding, outcome and predicate names: the vocabulary check's;
  - reachability, termination, caps and round shape: `graphscene.engine.static_check`'s;
  - what runs a node (an agent's existence, its return schema): a harness check, outside this package;
  - reading a file or a mapping: the graph arrives built.
- [ ] `reference_violations(graph: FlowGraph) -> list[Violation]` returns, in **document order**, one violation per unresolved name. The order is `start`, then each `entries[i]`, then the `start-in-entries` violation, then nodes in key order. Within a round node, report `gates[i]`, `writer`, `counter`, `plan[i]`, `revisionNote`, then its outcomes. Within a dispatch node, report its outcomes in key order, then its `skip` entries. A terminal node has nothing here.
  - Within a `RouteEdge`, report in this order: `to`, `increment`, `reset`, `prompt`, `report.<slot>` in key order, `onCap.roundCounts[i]`, `onCap.evidence`.
  - Within a `BindingEdge`, report `resume` (when not `None`), `roundCounts[i]`, `evidence`.
  - Within a `SkipEntry`, report `to`, then `report.<slot>`.
  - Paths are dotted from the graph root **in the serialized spelling** (`onCap`, `roundCounts`, `revisionNote`), written literally, never derived from the attribute names.
- [ ] The exact reasons. Each opens with its check id:
  - `node-known: '<id>' is not a node` (a node id in `start`, `entries[i]`, `gates[i]`, `writer`, a route `to`, an interrupt `resume`, a skip `to`, or an edge's or `onCap`'s `roundCounts[i]`).
  - `counter-known: '<name>' is not declared in counters` (`increment`, `reset`, a round's `counter`).
  - `path-known: '<name>' is not declared in paths` (`plan[i]`, `revisionNote`, an edge's or `onCap`'s `evidence`).
  - `report-slot-known: '<slot>' is not declared in reports` (each key of an edge's or a skip entry's `report`, at path `….report.<slot>`).
  - `prompt-known: '<prompt>' is not a prompt node '<to>' declares` (a route edge's `prompt`, when its `to` names a node that is not a dispatch node, or a dispatch node whose `prompts` is `None` or lacks it). When `to` names no node, only the `node-known` violation is reported for that edge, never also `prompt-known`.
  - `start-in-entries: start '<start>' is not listed in entries` at path `entries`. This is reported only when `start` names a node, so an unknown `start` is reported once, as `node-known`.
- [ ] `static_negative_node_known.json`: a copy of `graphscene/tests/fixtures/flow_graph/valid_generic.json` whose one change is `nodes.draft.outcomes.done.to` = `"review"`. It stays schema-valid (the id matches `^[a-z][a-z0-9_]*$`) and vocabulary-valid. Its one expected violation is `Violation("nodes.draft.outcomes.done.to", "node-known: 'review' is not a node")`. Task 6 lists it in `validate:graphscene-schema`, and Task 4 lists it in `_STATIC_NEGATIVES` in `graphscene/tests/facade/test_loading.py`.
- [ ] `test_references.py` opens with a docstring stating *"The rule this file exists to enforce"*, plus a *"Deliberately not covered:"* list naming the vocabulary check's names and the graph checks. Its planted graphs are complete format-4 mappings built with `graphscene.adapters.builder.build_flow_graph`, so the check reads what the builder produces (see the lessons-ledger rule about fixture helpers standing in for a producer). Keep the helpers in this file. Cases, each asserting the exact `list[Violation]`:
  - one planted case per id position listed above, per check id;
  - `prompt-known` for a target lacking the prompt, a target dispatch node with no `prompts`, and a target that is a round node;
  - an unknown `to` carrying a `prompt` reports `node-known` alone;
  - an unknown `start` reports `node-known` alone;
  - a document-order case mixing two nodes and several positions;
  - `valid_generic.json` built returns `[]`;
  - a `_NEGATIVES` list holding `static_negative_node_known.json` with its one `Violation`, asserted equal to the built fixture's result.

  Expected values are hand-written from reading each planted graph, never taken from the check's output.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_references.py` passes.
- `bash scripts/typecheck.sh` passes (strict `mypy` and `ruff` over `src` and `tests`).
- `grep -n "^from\|^import" graphscene/src/graphscene/engine/references.py` shows only `graphscene.model.*` and standard-library imports.
- `grep -n "references" graphscene/src/graphscene/__init__.py graphscene/src/graphscene/facade/__init__.py` finds nothing: the module stays unexported.
