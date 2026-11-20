### Task 4 — Publish the graph-model surface in `graphscene.__all__` and describe it in `graphscene/README.md`

**Goal:** Make the graph model the package's public surface. The loader, the typed objects and the error type become importable from `graphscene` and listed in `__all__`, and the package README says what the library now holds. A consumer writes `from graphscene import load_graph, FlowGraph, GraphError`.

**Depends on:** Tasks 1, 2 and 3. This task exports exactly the names they define, restated here:

- **Task 1** (`graphscene.errors`): `Violation`, `Stage` and `GraphError`. `graphscene.vocabulary.vocabulary_violations` now returns `list[Violation]`.
- **Task 2** (`graphscene.model`): the alias types `NodeKind`, `Primitive`, `Verdict`, `BindingDeclaration`, `Edge` and `Node`, and the classes `OutcomeDeclaration`, `InterruptBinding`, `StopBinding`, `EndBinding`, `PredicateDeclaration`, `Vocabulary`, `CounterDeclaration`, `OnCapEdge`, `RouteEdge`, `BindingEdge`, `SkipEntry`, `DispatchNode`, `RoundNode`, `TerminalNode` and `FlowGraph`.
  - `build_flow_graph` is **not** exported. It assumes a validated graph, and `load_graph` is the public way in.
- **Task 3** (`graphscene.loader`): `load_graph(graph: object) -> FlowGraph` and `load_graph_file(path: str | os.PathLike[str]) -> FlowGraph`. Both raise `GraphError` with stage `parse`, `schema` or `vocabulary`.

This task changes no behaviour in those modules. It owns `graphscene/src/graphscene/__init__.py` and `graphscene/README.md`, and no earlier task touches either.

### Targets

- `graphscene/src/graphscene/__init__.py` — imports and `__all__: list[str]`.
- `graphscene/README.md` — `## What it is`.
- `graphscene/tests/test_public_surface.py` (new) — pins the public surface.

**Work:**

- [ ] **`__init__.py`.**
  - Import every name listed under **Depends on** from its module with absolute `from graphscene.<module> import …` lines, keeping `vocabulary_violations`.
  - List them all in `__all__: list[str]`. Under `mypy` `strict`, an imported name missing from `__all__` is not re-exported (`.claude/context/graphscene.md` → `## Naming and layout`).
  - Extend the module docstring with one sentence on what the package exposes: loading a declared graph into the typed model, and the error type every rejection uses. Keep the boundary paragraph verbatim.
- [ ] **`graphscene/README.md` → `## What it is`.**
  - Rewrite the opening sentence *"It has no engine code yet, but it carries the generic flow-graph schema (format 4) and the vocabulary check, and declares one runtime dependency, `jsonschema`, for validating a graph against that schema."* It should say three things:
    - it still has no engine code, and nothing runs a graph;
    - it carries the format-4 schema, the vocabulary check, and a loader that validates a parsed graph against both and returns it as typed objects;
    - `jsonschema` is the dependency the loader validates with.
  - In the table, change the `src/graphscene/vocabulary.py` row so it states that `vocabulary_violations` returns `Violation` values. Add one row each for `src/graphscene/errors.py`, `src/graphscene/model.py` and `src/graphscene/loader.py`, naming the public names each holds.
  - Change nothing under `## The boundary`, `## Running the toolchain` or `## Gating`.
- [ ] **`test_public_surface.py` (new).**
  - It opens with the module docstring *"The rule this file exists to enforce"*: the package root exposes exactly the graph-model surface, and each name is the object its module defines.
  - **The exact list.** `graphscene.__all__` equals a hand-written list of the names above. Compare it as a list, so a reordering also shows up as a reviewed change.
  - **Each name resolves.** For each name, `getattr(graphscene, name)` is the same object as in its defining module: for example `graphscene.load_graph is graphscene.loader.load_graph` and `graphscene.Violation is graphscene.errors.Violation`.
  - **Not exported.** `"build_flow_graph" not in graphscene.__all__`.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py`, run from the repository root as one plain foreground command, passes.
- The README's table rows name only files that exist: each `src/graphscene/…` path in the table resolves under `graphscene/`.
- Re-run the story index's `## Scope register` command entry. Rows 9 and 10 (`graphscene/README.md`) now read as their `change` dispositions describe.
- `mypy` `strict` and `ruff` are graded at the Run gates phase, by gate 13's legs `13f` and `13e`.
