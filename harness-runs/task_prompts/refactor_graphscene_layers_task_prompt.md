`refactor_graphscene_layers` gives GraphScene an internal architecture: layers inside `graphscene/src/graphscene/`, with the direction of imports between them enforced by a test, before more features land in it. Part of #376.

## Why

Every module sits flat in `graphscene/src/graphscene/` today: `model.py`, `errors.py`, `vocabulary.py`, `loader.py`. The static checker (#415), the walker and its state store (#416), the review-loop pattern (#417), the CLI (#418) and the executors (#420, #421) would all land beside them with no hierarchy, and the library extracted later would have no structure to show for it. With four modules the move is cheap now, and it gets more expensive with each branch.

## Decided (2026-11-21)

- **Four layers, imports pointing down only**, as in a sibling Python project of ours that settled this recently. The shape is not a chain: `facade` on top; `engine` and `adapters` side by side beneath it, **independent of each other**; `model` at the bottom. `adapters` never imports `engine` and `engine` never imports `adapters`; only `facade` combines the two. An `import-linter` `layers` contract lets a higher layer import any lower one, so the two middle layers go in one entry as independent siblings, e.g. `layers = ["graphscene.facade", "graphscene.adapters | graphscene.engine", "graphscene.model"]`, never as two stacked entries.
- **The top layer is `graphscene.facade`.** Callers never import it by name: they import from `graphscene`, whose `__init__.py` re-exports from it. Not `api`, which would read as a second import path beside the package root, and not `app`, which in the sibling project is the use-case layer beneath the composing one.
- **The layer contracts are `import-linter` contracts in `graphscene/pyproject.toml`, run from a test**, so they travel with the library when it is extracted. `import-linter` is already in the `dev` group and pinned in `graphscene/uv.lock` on `dev` (#436), so the run needs no `lock` or `provision` step.
- **The vocabulary check does not move onto the typed `FlowGraph`.** It keeps reading the parsed mapping, and `vocabulary_violations` keeps its signature and its place in `__all__`; the order stays schema → vocabulary → build. Whether it moves onto the model is #415's question, not this branch's.
- **It lands before #415**, so the checker and everything after it start in their layer.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- **What each layer holds, now and later:**

  | Layer | May import | Now | Later |
  |---|---|---|---|
  | `model` | standard library only | the typed `FlowGraph` and its objects (`model.py`), `Violation` / `GraphError` (`errors.py`) | walk state, checker findings |
  | `engine` | `model` | the vocabulary check | the static checker (#415), the walker and rounds (#416), the review-loop pattern (#417) |
  | `adapters` | `model`, `jsonschema` | reading a JSON file, schema validation with `jsonschema` (with the ECMA-262 pattern translator, `_ecma_pattern` / `_ecma_patterns`, that builds the validator), building the model from parsed data (`build_flow_graph`, out of `model.py` today) | the file state store (#416), the headless `claude` executor (#421) |
  | `facade` | everything | `load_graph` / `load_graph_file`, composing the adapter and the engine | the thin CLI (#418) |

- **The public API is the package root, re-exporting from `facade`.** GraphScene is a library first. Today `loader.py` reads, validates and builds in one module; split, the adapter validates against the schema, the engine runs the vocabulary check, the adapter builds the `FlowGraph`, and the facade calls them in that order, so a graph `load_graph` returns still passed both checks. `tests/test_public_surface.py` pins today's `__all__`; a refactor that keeps it unchanged is the easy proof nothing broke for a caller. Its `_DEFINED_IN` map and `test_the_named_examples_resolve_to_their_modules` name the defining modules (`graphscene.loader`, `graphscene.vocabulary`, …) and move with them; `test_the_unvalidated_builder_is_not_exported` keeps holding for `build_flow_graph` in its new place.
- **`jsonschema` forbidden in `model` and `engine`**, as a `forbidden` contract, so the format library stays in `adapters`. A `forbidden` contract naming an outside package needs `include_external_packages = true` under `[tool.importlinter]` (checked against the sibling project's configuration; confirm against `import-linter` 2.17).
- **`import-linter` writes a cache directory (`.import_linter_cache`) in the working directory by default**, and `.gitignore` does not list it; run from a test inside a run copy it would leave an untracked directory. Running it without a cache avoids that; how 2.17 spells that (a `lint_imports` argument, a CLI flag or a config key) is for planning to confirm.
- **The schema stays readable from a subpackage**: `files("graphscene") / "schemas" / "flow-graph.schema.json"` resolves against the package root wherever the validator lives.
- **Interfaces for what the walker drives (state store, executor, host-answered predicates) are not built here.** #416 and #420 add them; this branch only decides where a `Protocol` lives (in `model` or `engine`) so adapters can implement it without importing the engine. Say so in the conventions this branch leaves behind.
- **Tests mirror the layers:** `tests/model/`, `tests/engine/`, `tests/adapters/`, and the facade's tests beside them. Each test subdirectory likely needs an `__init__.py`: without it, two test files with the same basename in different directories collide under `pytest`'s default import mode, and `mypy` (`files = ["src", "tests"]`) reports a duplicate module. The fixtures in `tests/fixtures/flow_graph/` are named by path in `package.json` (`validate:graphscene-schema*`) and `docs/development.md`; moving them means updating both.
- **The schema stays package data** at `src/graphscene/schemas/flow-graph.schema.json` unless planning finds a reason to move it; `package.json`, `docs/development.md`, `schemas/README.md` and `docs/flow-graph-walker.md` name that path.
- **Prose that names a module path**: `docs/development.md` (the paragraph on the vocabulary check's two homes names `graphscene.vocabulary.vocabulary_violations`) and the layout table in `graphscene/README.md`. The harness-runs artifacts of earlier branches also name the old paths; they are records and stay as they are.
- **`tests/test_boundary.py` stays.** It enforces the harness boundary (no `devscene`-prefixed module, never `devscene.config.json`), which `import-linter` contracts can sit beside but do not replace. It walks `src/graphscene/` with `rglob`, so it already sees new subpackages; its real-tree case should keep passing unchanged.
- `graphscene/README.md` gets a layout table: layer, path, what it holds, what it may import.
- `devscene.config.json` keeps `graphscene` as one layer.

## Owed after merge (user steps, not this run's)

The run states these in its hand-off as owed after merge, and does not edit them:

- `.claude/context/graphscene.md` describes the package as flat; refilling it from the new layout is a `/devscene:analyze` step.
- `.claude/CLAUDE.md` → `## File naming conventions`: the *Python source module* row (`<package>/src/<import_name>/<snake_case>.py`) and the *Python test suite* row (`<package>/tests/test_<snake_case>.py`) allow no subpackage or test subdirectory. Both are updated after merge to admit `src/<import_name>/<layer>/` and `tests/<layer>/`. Until then a new file under a layer directory follows this issue, not those two rows.

## Depends on

#414, #435 (ordering only: agents check Python lint and types per unit)
