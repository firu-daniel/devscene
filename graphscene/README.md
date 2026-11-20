# graphscene

**Who reads this:** a contributor changing this package, and whoever later extracts it from this repository. It owns what GraphScene is, the boundary between it and the harness, and how its toolchain is run here.

## What it is

GraphScene is a generic flow-graph navigation library. It has no engine code yet, and nothing runs a graph. It carries the generic flow-graph schema (format 4), the vocabulary check, and a loader that validates a parsed graph against both and returns it as typed objects. Its one runtime dependency, `jsonschema`, is what the loader validates with.

| Path | Holds |
|---|---|
| `src/graphscene/` | The typed package, `graphscene`. |
| `src/graphscene/schemas/flow-graph.schema.json` | The format-4 flow-graph schema, shipped as package data. |
| `src/graphscene/errors.py` | `Violation`, `Stage` and `GraphError`, the one error shape every loading stage rejects a graph with. |
| `src/graphscene/vocabulary.py` | `vocabulary_violations`, the used-against-declared names check JSON Schema cannot express, returning `Violation` values. |
| `src/graphscene/model.py` | `FlowGraph` and the typed objects it holds: `NodeKind`, `Primitive`, `Verdict`, `BindingDeclaration`, `Edge`, `Node`, `OutcomeDeclaration`, `InterruptBinding`, `StopBinding`, `EndBinding`, `PredicateDeclaration`, `Vocabulary`, `CounterDeclaration`, `OnCapEdge`, `RouteEdge`, `BindingEdge`, `SkipEntry`, `DispatchNode`, `RoundNode` and `TerminalNode`. |
| `src/graphscene/loader.py` | `load_graph` and `load_graph_file`, which validate a graph against the schema, then the vocabulary check, and return a `FlowGraph` or raise `GraphError`. |
| `tests/` | The `pytest` suite. |

## The boundary

- **The harness side lives outside this directory, and the dependency points one way.** Harness-specific code — reading the harness's configuration, executing its agents, its planning hooks — goes in its own distribution outside `graphscene/`, named with a `devscene` prefix, and that distribution depends on `graphscene`. `graphscene` never depends on it, so extracting the library means moving this one directory.
- **The library imports only the standard library, itself and its declared runtime dependencies.** It names no `devscene`-prefixed module, never reads the harness's configuration file, and declares no `devscene`-prefixed dependency.

`tests/test_boundary.py` enforces the boundary, so the rule travels with the library when it is extracted.

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
