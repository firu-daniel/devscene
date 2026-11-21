### Task 3 — Document the layer layout, the import rules and the `Protocol` placement in `graphscene/README.md`

**Goal:** Make `graphscene/README.md` the library's own statement of its layers: which layer holds what, what each may import, where a `Protocol` lives, where future work goes, and what enforces the direction. The rules then travel with the library when it is extracted, and later branches have one place to read them from.

**Depends on:** Task 1 and Task 2. Task 1 creates the layered layout this file describes:

- `src/graphscene/model/` (`errors.py`, `flow_graph.py`)
- `src/graphscene/engine/` (`vocabulary.py`)
- `src/graphscene/adapters/` (`schema.py`, `builder.py`, `json_file.py`)
- `src/graphscene/facade/` (`loading.py`, and `__init__.py` as the composed surface)
- the root `__init__.py`, which re-exports from `graphscene.facade` only
- the tests under `tests/model/`, `tests/engine/`, `tests/adapters/` and `tests/facade/`

Task 2 creates the two contracts in `graphscene/pyproject.toml` → `[tool.importlinter]`, with ids `graphscene-layers` and `graphscene-jsonschema-in-adapters-only`, and the test that runs them, `tests/test_layers.py`. This task describes those artifacts and changes none of them.

**Where this task stops.** It edits `graphscene/README.md` only. It does not edit `.claude/context/graphscene.md` or `.claude/CLAUDE.md`: both describe the flat layout, and updating them is a user step after merge (see the story index's `## Context`). The documents at the repository root that name module paths belong to **Task 4**.

**One owner for each rule.** This README is where the layer rules are stated. `docs/development.md` (Task 4) cites this README for them and does not restate them (`harness-runs/lessons.md` → `## Agent prose`: *"State a new behaviour once, in the section that decides it, and cite it from everywhere else"*).

### Targets

- `graphscene/README.md`

**Work:**

- [ ] **`## What it is`**: keep the opening paragraph, reworded only where it says *"a loader"*: loading is now the facade's, composing a schema adapter, the vocabulary check and the builder. In the `Path | Holds` table, keep the `src/graphscene/`, `src/graphscene/schemas/flow-graph.schema.json` and `tests/` rows. Add a row for `src/graphscene/__init__.py`, the public surface, re-exported from `graphscene.facade`. Replace the four flat module rows (`errors.py`, `vocabulary.py`, `model.py`, `loader.py`) with one row per layer directory, naming the modules and public names each holds. Make the `tests/` row say that the tests mirror the layers, with `tests/model/`, `tests/engine/`, `tests/adapters/` and `tests/facade/`. Package-wide tests (`test_boundary.py`, `test_layers.py`, `test_public_surface.py`, `test_flow_graph_schema.py`) stay at `tests/`.
- [ ] **New `## The layers` section, between `## What it is` and `## The boundary`**, opening with a table: `Layer | Path | Holds | May import`.
  - `facade`, `src/graphscene/facade/`: loading a graph, which composes the adapters and the engine, and the composed surface the package root re-exports. May import every layer below.
  - `engine`, `src/graphscene/engine/`: checks over a flow graph (the vocabulary check). May import `model` and the standard library.
  - `adapters`, `src/graphscene/adapters/`: reading a JSON file, validating against the schema with `jsonschema` and the ECMA-262 pattern translator, building the typed model. May import `model`, `jsonschema` and the standard library.
  - `model`, `src/graphscene/model/`: the typed `FlowGraph` and its objects, and `Violation` / `Stage` / `GraphError`. May import the standard library only.
- [ ] **The rules under that table**, each stated once:
  - Imports point down only, and `engine` and `adapters` never import each other; only `facade` combines them.
  - Callers import from `graphscene` only and never name `graphscene.facade`. No module inside the package imports from the package root. Each imports the defining module of what it needs.
  - A `typing.Protocol` that an adapter implements and the engine drives (a state store, an executor, a host-answered predicate) is declared in `model`, so the adapter implements it without importing the engine. None exists yet.
  - Where new work goes, as placement rules rather than promised work. A check or a walk over the model, and its rounds, goes in `engine`. A store, an executor or another format goes in `adapters`. A thin command-line entry point goes in `facade`. Walk state and checker findings, as plain types, go in `model`.
  - The vocabulary check reads the parsed mapping and runs after the schema check and before the build. A graph `load_graph` returns has passed both.
- [ ] **What enforces it.** Close `## The layers` with: the direction and the `jsonschema` confinement are `import-linter` contracts in `pyproject.toml` → `[tool.importlinter]` (ids `graphscene-layers` and `graphscene-jsonschema-in-adapters-only`), run by `tests/test_layers.py` with no cache. Give the one command that runs it alone in a fenced block, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`, the fenced-command rule):

  ```
  bash scripts/python-service.sh --package graphscene test tests/test_layers.py
  ```

  In `## The boundary`, change the closing line to say that `tests/test_boundary.py` enforces the boundary and `tests/test_layers.py` the layer direction, so both rules travel with the library when it is extracted. The two bullets above that line stay unchanged.

**Verification:**

- Every path the README names exists after Tasks 1 and 2. Each `src/graphscene/…` and `tests/…` path in the edited sections resolves under `graphscene/` (`git ls-files graphscene` lists it). No row names `errors.py`, `vocabulary.py`, `model.py` or `loader.py` at the package top level: `git grep -nE 'src/graphscene/(errors|vocabulary|model|loader)\.py' -- graphscene/README.md` prints nothing.
- The layer table's `May import` column matches the contracts in `graphscene/pyproject.toml` → `[tool.importlinter]` cell for cell. The two contract ids the README names are the ones that file declares.
- The README states each rule once, and `## Running the toolchain` and `## Gating` are unchanged: `git diff -- graphscene/README.md` touches only `## What it is`, the new `## The layers` and the closing line of `## The boundary`.
