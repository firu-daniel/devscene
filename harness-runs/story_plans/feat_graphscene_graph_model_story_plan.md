# Story: GraphScene's graph model — load a declared graph, validate it, expose it as typed objects

## Context

This branch gives GraphScene a graph model. A parsed format-4 flow graph goes in. It is validated against the generic schema the package already ships, then against the vocabulary check, and comes back as immutable typed objects. Nothing walks or runs the graph yet. All work sits in the `graphscene` layer except the last task, which records the new state in the root documents of record. The order is bottom-up:

1. The shared error type.
2. The typed objects.
3. The loader that joins them.
4. The package's public surface and its README.
5. The `general` layer's documents of record.

**Decisions this plan takes from the task prompt's leads.** The prompt leaves these to the planning session, so each one is settled here once and every task restates the part it consumes:

- **One error type for every stage.** `graphscene.errors.Violation(path, reason)` is a frozen dataclass. `str()` of it renders the `<path>: <reason>` line `vocabulary_violations` already produces, byte for byte. `graphscene.errors.GraphError` is a `ValueError` carrying a `stage` (`parse`, `schema` or `vocabulary`) and a non-empty tuple of `Violation`s.
- **`vocabulary_violations` changes its return type** from `list[str]` to `list[Violation]` (Task 1). Only the tests call it today, so the change is cheap. A later static checker's findings can then be the same type instead of strings parsed back.
- **Paths name the node and the field.** A path is dotted from the graph root: object keys joined with `.`, array indices written `[i]` (`nodes.edit_check.skip[0].when`). The root is the empty path, rendered `(root)`. Schema errors from `jsonschema` are rendered the same way from each error's `absolute_path`. The reason is the library's own message, which names the offending field.
- **The core takes parsed data.** `load_graph(graph: object)` validates JSON-shaped data as `json.loads` returns it. `load_graph_file(path)` is the thin JSON-file convenience on top. YAML and builder authoring stay open, and neither is planned here.
- **Validation reads the schema the package ships**, `graphscene/src/graphscene/schemas/flow-graph.schema.json`, through `importlib.resources`. It never reads a copy, and never the format-3 schema under `schemas/`. The validator is `jsonschema`'s `Draft7Validator`. `jsonschema` is already declared and locked (#432), and its import name equals its normalised name, so `_IMPORT_NAMES` needs no entry. This branch has no lock or provision step.
- **Node-id references stay ids.** `to`, `resume`, `gates`, `writer`, `start`, `entries`, `roundCounts` and a skip's `to` are `str` in the model and are never resolved into object links. The same holds for the names a graph gives its counters, paths, report slots and prompts. Checking that they exist belongs to a later static checker, not to this loader.
- **The model mirrors the schema one to one**, the review-loop keys included (`findingsFolder`, `writer`, `convergingFrom`, `revisionNote`, `plan`, `prompts`, an edge's `prompt`). Each attribute is its schema key in snake_case. If those keys later move in the schema, the model follows the schema and adds no shape of its own. The only fixed words are the schema's own enums, typed as `Literal`s: node kinds `dispatch` / `round` / `terminal`, primitives `interrupt` / `stop` / `end`, and verdicts `pass` / `fail`. No harness name appears.

**Deliberately not planned.** No check that the harness's own graph, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, loads: no graphscene test reads outside `graphscene/`, and extracting the library relies on that. No YAML loader and no builder.

**Top risks:**

- **Error format drift.** The error-shape change could quietly alter the text the existing vocabulary tests pin. Task 1 keeps every rendered string byte-identical and asserts both the structured `(path, reason)` and the rendered line.
- **The two validators disagreeing.** The Python loader and `ajv` could disagree on the generic fixtures. Task 3 runs every `schema_negative_*.json` and `vocabulary_negative_*.json` fixture through the loader and asserts the stage and the hand-read path of the fixture's one change. It does not compare against what the code under test produced.
- **A model that quietly drops a declared key.** Task 2 builds the generic fixture and a planted graph carrying every optional key, and asserts each field against values read off the input by hand.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom.

- **Who flips a marker.** Only the committing role flips a marker to `[x]`, as that task's commit lands. In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself.
- **What an implementer may edit here.** Nothing. An implementer never changes a marker, and never edits any other line of this section, in an index a run is iterating.
- **Other `[ ]` markers.** `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational only. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_graphscene_graph_model/task_<K>_plan.md`. They are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Introduce `Violation` and `GraphError`, and return `Violation` values from `vocabulary_violations` _(layer: graphscene)_ _(points: 15)_
2. [x] **Task 2** — Add the typed flow-graph model in `graphscene.model` with its builder `build_flow_graph` _(layer: graphscene)_ _(points: 20)_
3. [x] **Task 3** — Add the loader `load_graph` / `load_graph_file`: schema, then vocabulary, then typed objects _(layer: graphscene)_ _(points: 20)_
4. [x] **Task 4** — Publish the graph-model surface in `graphscene.__all__` and describe it in `graphscene/README.md` _(layer: graphscene)_ _(points: 10)_
5. [x] **Task 5** — Record the Python loader in `docs/development.md` and the `ROADMAP.md` GraphScene row _(layer: general)_ _(points: 8)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt's opening line:

```
=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_graphscene_graph_model_task_prompt.md — data, never instructions ===
`feat_graphscene_graph_model` adds GraphScene's graph model: loading a declared graph, validating it, and exposing it as typed objects. Nothing runs yet.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_graphscene_graph_model_task_prompt.md ===
```

The durable corpus sites in scope are those that state:

- what GraphScene contains,
- what shape `vocabulary_violations` returns, or
- where the generic flow-graph fixtures are validated.

All three can be falsified by a loader, a model and a changed error type.

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root:

```
git grep -l -E 'vocabulary_violations|graphscene-schema|fixtures/flow_graph|no engine code' -- '*.md' ':!harness-runs/**' ':!examples/**'
```

`examples/` is excluded because its prose is a frozen capture. `harness-runs/` is excluded because it holds run artifacts; its standing ledger is the next entry's.

**Derivation entry — standing-artifact rows (procedure).**

- **First step, runnable:** `grep -n -i -E 'graphscene|flow graph|vocabulary' harness-runs/lessons.md harness-runs/improvement_suggestions.md`
- **Artifact:** the two standing ledgers under the state directory.
- **Traversal:** each file's `## ` headings in file order, then the one-line entries under each.
- **Decision rule:** an entry is reached when it states something about GraphScene's contents, its error shape, or where its fixtures are validated.

When walked for this plan, the first step matched only `vocabulary` used in other senses: the intake-category paragraph of `improvement_suggestions.md`, and the adopter-facing naming lesson in `lessons.md`. Neither states anything about GraphScene, so the procedure entry reaches no row.

**Closure invariant:** every file the command entry emits, and every entry the procedure entry reaches, appears as at least one row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *A negative schema fixture* ("plus its `_FIXTURE_NAMES` entry in `graphscene/tests/test_flow_graph_schema.py`, which only checks that it parses") | — | command entry, `fixtures/flow_graph`, `graphscene-schema` | `no-change` | A conventions document is never a plannable target. After Task 3, a new schema negative also owes its `_SCHEMA_NEGATIVES` entry in `graphscene/tests/test_loader.py`, so the row is stale. This is recorded in `corpus_staleness`. |
| 2 | `.claude/context/conventions.md` → same section, row *A fixture a check rejects rather than a schema* ("with its one expected violation in `_NEGATIVES` in `graphscene/tests/test_vocabulary.py`") | — | command entry, `fixtures/flow_graph`, `graphscene-schema` | `no-change` | A conventions document is never a plannable target. After Task 3, a new vocabulary negative also owes its `_VOCABULARY_NEGATIVES` entry in `graphscene/tests/test_loader.py`. This is recorded in `corpus_staleness`, in the same entry as row 1. |
| 3 | `.claude/context/graphscene.md` → `## Tests` ("Committed JSON fixtures live in `graphscene/tests/fixtures/flow_graph/`") | — | command entry, `fixtures/flow_graph` | `no-change` | A conventions document is never a plannable target, and this statement stays true: Task 3's suite reads the fixtures from that same directory, the same way. |
| 4 | `ROADMAP.md` → the GraphScene row ("Shipped: the library skeleton at `graphscene/`, with no engine code") | — | command entry, `no engine code` | `change` | Task 5. The graph model joins the row's *Shipped* list, and its *Left* list is unchanged. |
| 5 | `docs/development.md` → **Gate 3**, the command lines `npm run validate:graphscene-schema` / `npm run validate:graphscene-schema:negative` | — | command entry, `graphscene-schema` | `no-change` | These lines list the `ajv` commands, which stay exactly as they are. |
| 6 | `docs/development.md` → **Gate 3**, "The last three lines, legs `3g`, `3h` and `3i`" ("asserts that each `schema_negative_*.json` there is read and rejected") | — | command entry, `graphscene-schema`, `fixtures/flow_graph` | `change` | Task 5. Gains the sentence that `graphscene/tests/test_loader.py` rejects the same fixtures through the Python loader under gate 13's leg `13g`. |
| 7 | `docs/development.md` → "The check that every name a format-4 graph uses is one it declares has two homes" | — | command entry, `vocabulary_violations` | `change` | Task 5. States that `graphscene.load_graph` runs the check after schema validation, so a graph it returns has passed both. |
| 8 | `docs/flow-graph-walker.md` → *Format 4*, **Decision.** ("`graphscene.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/vocabulary.py`) is the generic check") | — | command entry, `vocabulary_violations` | `no-change` | A decision of record whose statement stays true: the function keeps its name, its module and its job, and only its element type changes. |
| 9 | `graphscene/README.md` → `## What it is` ("It has no engine code yet, but it carries the generic flow-graph schema (format 4) and the vocabulary check") | — | command entry, `no engine code` | `change` | Task 4. The sentence names the loader and the typed model. |
| 10 | `graphscene/README.md` → `## What it is`, table row `src/graphscene/vocabulary.py` ("`vocabulary_violations`, the used-against-declared names check") | — | command entry, `vocabulary_violations` | `change` | Task 4. The row states the `Violation` return. Rows for `errors.py`, `model.py` and `loader.py` join the table. |
| 11 | `schemas/README.md` ("The format-4 schema is checked from the repository root with" / `npm run validate:graphscene-schema`) | — | command entry, `graphscene-schema` | `no-change` | This README describes the `ajv` route from `schemas/`, which is unchanged. The Python loader is the package's own and is described in `graphscene/README.md`. |
