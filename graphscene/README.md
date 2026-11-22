# graphscene

**Who reads this:** a contributor changing this package, and whoever later extracts it from this repository. It owns what GraphScene is, the boundary between it and the harness, and how its toolchain is run here.

## What it is

GraphScene is a generic flow-graph navigation library. Nothing walks a graph yet: its `engine` layer holds the vocabulary check and the static checker. It carries the generic flow-graph schema (format 4), those two checks, and loading: the facade composes the schema adapter, the builder, the vocabulary check and the static checker, in that order, before returning the parsed graph as typed objects. Its one runtime dependency, `jsonschema`, is what the schema adapter validates with.

| Path | Holds |
|---|---|
| `src/graphscene/` | The typed package, `graphscene`. |
| `src/graphscene/__init__.py` | The public surface, re-exported from `graphscene.facade`. |
| `src/graphscene/schemas/flow-graph.schema.json` | The format-4 flow-graph schema, shipped as package data. |
| `src/graphscene/model/` | `errors.py`: `Violation`, `Stage` and `GraphError`, the one error shape every loading stage rejects a graph with. `flow_graph.py`: `FlowGraph` and the typed objects it holds: `NodeKind`, `Primitive`, `Verdict`, `BindingDeclaration`, `Edge`, `Node`, `OutcomeDeclaration`, `InterruptBinding`, `StopBinding`, `EndBinding`, `PredicateDeclaration`, `Vocabulary`, `CounterDeclaration`, `OnCapEdge`, `RouteEdge`, `BindingEdge`, `SkipEntry`, `DispatchNode`, `RoundNode` and `TerminalNode`. |
| `src/graphscene/engine/` | `vocabulary.py`: `vocabulary_violations`, the used-against-declared names check JSON Schema cannot express, reading the built `FlowGraph` and returning `Violation` values. `references.py`: `reference_violations`, that every node, counter, path, report-slot and prompt name the graph uses exists and `start` is listed in `entries`; not public. `static_check.py`: `static_violations`, the reference check, then the five graph checks (`reachable-from-start`, `reaches-terminal`, `fail-cycle-capped`, `gate-in-round`, `round-fan-out`), each reason opening with its check id. |
| `src/graphscene/adapters/` | `json_file.py`: `read_json_file`, reading a UTF-8 JSON file or raising a parse-stage `GraphError`. `schema.py`: `schema_violations`, validating against the shipped schema with `jsonschema` and the ECMA-262 pattern translator. `builder.py`: `build_flow_graph`, building the typed `FlowGraph` from a validated mapping. |
| `src/graphscene/facade/` | `loading.py`: `load_graph` and `load_graph_file`, which validate a graph against the schema, build it, then run the vocabulary check and the static checker, and return a `FlowGraph` or raise `GraphError`. `__init__.py`: the composed surface the package root re-exports. |
| `tests/` | The `pytest` suite. Its tests mirror the layers, in `tests/model/`, `tests/engine/`, `tests/adapters/` and `tests/facade/`; package-wide tests (`test_boundary.py`, `test_layers.py`, `test_public_surface.py`, `test_flow_graph_schema.py`) stay at `tests/`. A new module lands with its own suite, `tests/<layer>/test_<module>.py`. |

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `facade` | `src/graphscene/facade/` | Loading a graph, which composes the adapters and the engine, and the composed surface the package root re-exports. | `adapters`, `engine`, `model` and the standard library. |
| `engine` | `src/graphscene/engine/` | Checks over the built model: the vocabulary check and the static checker. | `model` and the standard library. |
| `adapters` | `src/graphscene/adapters/` | Reading a JSON file, validating against the schema with `jsonschema` and the ECMA-262 pattern translator, building the typed model. | `model`, `jsonschema` and the standard library. |
| `model` | `src/graphscene/model/` | The typed `FlowGraph` and its objects, and `Violation`, `Stage` and `GraphError`. | The standard library only. |

- **Imports point down only, and `engine` and `adapters` never import each other.** Only `facade` combines them.
- **Callers import from `graphscene` only and never name `graphscene.facade`.** No module inside the package imports from the package root; each imports the defining module of what it needs.
- **A `typing.Protocol` that an adapter implements and the engine drives is declared in `model`** — a state store, an executor, a host-answered predicate — so the adapter implements it without importing the engine. None exists yet.
- **New work goes by what it is.** A check or a walk over the model, and its rounds, goes in `engine`. A store, an executor or another format goes in `adapters`. A thin command-line entry point goes in `facade`. Walk state and checker findings, as plain types, go in `model`.
- **Every engine check reads the built `FlowGraph`, and loading runs schema → build → vocabulary → static.** A graph `load_graph` returns has passed all three checks, and a graph failing one stage never reaches the next.
- **The library never logs or prints.** It reports through return values and `GraphError` only. It has no user interface and keeps no persisted or shared state. A command-line entry point in `facade` is the one place that may write output.

The direction and the `jsonschema` confinement are `import-linter` contracts in `pyproject.toml` → `[tool.importlinter]`, ids `graphscene-layers` and `graphscene-jsonschema-in-adapters-only`, run by `tests/test_layers.py` with no cache. Run it alone:

```
bash scripts/python-service.sh --package graphscene test tests/test_layers.py
```

## The boundary

- **The harness side lives outside this directory, and the dependency points one way.** Harness-specific code — reading the harness's configuration, executing its agents, its planning hooks — goes in its own distribution outside `graphscene/`, named with a `devscene` prefix, and that distribution depends on `graphscene`. `graphscene` never depends on it, so extracting the library means moving this one directory.
- **The library imports only the standard library, itself and its declared runtime dependencies.** It names no `devscene`-prefixed module, never reads the harness's configuration file, and declares no `devscene`-prefixed dependency.
- **A new runtime dependency is a decision raised to the maintainer, never one an implementing run makes.** Adding a development tool to the `dev` dependency group is not restricted this way.

`tests/test_boundary.py` enforces the boundary and `tests/test_layers.py` the layer direction, so both rules travel with the library when it is extracted.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package graphscene lint
```

Typecheck:

```
bash scripts/python-service.sh --package graphscene typecheck
```

Test:

```
bash scripts/python-service.sh --package graphscene test
```

`test` forwards paths to `pytest`, relative to `graphscene/`:

```
bash scripts/python-service.sh --package graphscene test tests/test_boundary.py
```

`typecheck` takes no argument (one is refused, exit 2): it runs `mypy` over the whole package, `src` and `tests`.

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13e–13g ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
