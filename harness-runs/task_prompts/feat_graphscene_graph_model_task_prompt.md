`feat_graphscene_graph_model` adds GraphScene's graph model: loading a declared graph, validating it, and exposing it as typed objects. Nothing runs yet. Part of #376.

## Decided (2026-11-20)

- **Schema validation uses `jsonschema`, GraphScene's first runtime dependency.** It is already declared in `graphscene/pyproject.toml` under `[project] dependencies` and pinned in `graphscene/uv.lock` on `dev` (#432), so this branch needs no `lock` or `provision` step. `jsonschema` ships no `py.typed`, so `types-jsonschema` is in the `dev` group beside it; a `Draft7Validator(...).iter_errors(...)` probe passed strict `mypy` with it. #413 kept the package dependency-free and ran its schema fixtures through `ajv` from the repository root; the loader is where Python validation starts.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- Validation against the generic schema in `graphscene/` (#413), the same file the harness's checks read, not a copy. `tests/test_flow_graph_schema.py` already reads it through `importlib.resources`. The v3 schema in `schemas/` belongs to the bash walker and is not this package's.
- Errors that name the node and the field.
- **The error shape is shared with #415.** `vocabulary_violations` returns `<path>: <reason>` strings and is exported in `__all__`; #415 wants structured findings rather than text. Only the tests call it today, so changing its return type here is cheap, and one error type for schema errors, names errors and #415's findings may be better than parsing the strings back.
- No vocabulary of its own, meaning no *harness* names: everything a graph routes on comes from its declaration (#413), including the behaviour each declared outcome and binding maps to. The engine's own words are not that: the node kinds `dispatch` / `round` / `terminal` and the primitives `interrupt` / `stop` / `end` are fixed by the schema's enums and can be typed as such.
- **Node-id references stay ids.** A graph that passed the loader may still name a node that does not exist (`to`, `resume`, `gates`, `writer`, `start`, `entries`); that check is #415's. Resolving ids into object links here would do half of it.
- **The review-loop keys are carried over, and #417 may move them:** `findingsFolder`, a round's `writer`, `convergingFrom`, `revisionNote`, `plan`, `prompts` and an edge's `prompt`. Typing them as first-class fields now may be undone by #417's opt-in pattern.
- **The core takes parsed data.** `vocabulary_violations` takes a parsed mapping, and #376 plans YAML and builder authoring later. A loader that validates a mapping, with a thin convenience for a JSON file, keeps those open.
- #413's fixtures as test cases: `graphscene/tests/fixtures/flow_graph/` holds `valid_generic.json`, the `schema_negative_*.json` the schema rejects and the `vocabulary_negative_*.json` that are schema-valid and rejected by the names check. Today the schema negatives are only run through `ajv` (`validate:graphscene-schema*` in `package.json`); a Python loader rejecting them too means the two validators agree on the same file.
- **The harness's own graph stays outside the package's tests.** `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` is harness code; no graphscene test reads outside `graphscene/` today, and extracting the library relies on that. A check that the harness graph loads belongs on the harness side, if anywhere.
- #413 built the names check JSON Schema cannot express, `graphscene.vocabulary.vocabulary_violations` (a parsed, schema-valid graph in, `<path>: <reason>` strings out). The loader may call it after schema validation, so a loaded graph has passed both; its docstring leaves node-id references, reachability and caps to #415.

## Depends on

#412, #413

