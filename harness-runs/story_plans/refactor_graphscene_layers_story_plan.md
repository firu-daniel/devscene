# Story: Layer GraphScene's package — `model`, `engine`, `adapters`, `facade` — with the import direction held by `import-linter` contracts run from a test

## Context

This branch gives the GraphScene library (`graphscene/`) an internal architecture before the static checker, the walker, the review-loop pattern, the CLI and the executors land in it. Today every module sits flat in `graphscene/src/graphscene/` (`errors.py`, `model.py`, `vocabulary.py`, `loader.py`). After this branch the package holds four layer subpackages, and imports point down only:

| Layer | Path | Holds after this branch | May import |
|---|---|---|---|
| `facade` | `graphscene/src/graphscene/facade/` | `load_graph`, `load_graph_file` (composing the adapters and the engine), and the composed public surface the package root re-exports | every layer below |
| `engine` | `graphscene/src/graphscene/engine/` | the vocabulary check, `vocabulary_violations` | `model`, the standard library |
| `adapters` | `graphscene/src/graphscene/adapters/` | schema validation with `jsonschema` and its ECMA-262 pattern translator, reading a JSON file, `build_flow_graph` | `model`, `jsonschema`, the standard library |
| `model` | `graphscene/src/graphscene/model/` | the typed `FlowGraph` and its objects, `Violation` / `Stage` / `GraphError` | the standard library only |

`engine` and `adapters` are **independent siblings**: neither imports the other, and only `facade` combines them. The shape is fixed by the task prompt's `## Decided (2026-11-21)` section and is not re-decided here. In particular, the vocabulary check keeps reading the parsed mapping, `vocabulary_violations` keeps its signature and its place in `__all__`, and the load order stays schema → vocabulary → build.

**Callers import from `graphscene` alone.** The root `__init__.py` re-exports from `graphscene.facade` only, and its `__all__` stays unchanged, name for name and in order. `tests/test_public_surface.py` pins that list, so an unchanged list is the proof that no caller broke. No module inside the package imports from the package root. Each module imports the defining module of what it needs (`from graphscene.model.errors import Violation`), and the three lower layer packages' `__init__.py` files hold a docstring and nothing else. **Where a `Protocol` lives:** in `model`. It is the only layer both `engine` and `adapters` may import, so an adapter can implement a `Protocol` the engine drives without importing the engine. No `Protocol` is built here. This branch only records the placement, in `graphscene/README.md` (Task 3) and the `model` package docstring (Task 1).

**Why the move is one task.** Every module that moves rewires its importers in the same change: the root `__init__.py`, the other source modules and the test files. If the move were split by layer, two tasks would edit the same files (the root `__init__.py`, `tests/test_public_surface.py`, the moved test files), or a commit would land a tree that does not import. So Task 1 moves the source and the tests together, verbatim except where a module splits. The work it leaves out, and leaves to Tasks 2–4, is the parts that need no rewiring: the contracts, the README and the root documents.

The schema stays package data at `graphscene/src/graphscene/schemas/flow-graph.schema.json`, read as `files("graphscene") / "schemas" / "flow-graph.schema.json"` from the schema adapter. The fixtures stay in `graphscene/tests/fixtures/flow_graph/`, so `package.json` (`validate:graphscene-schema*`) is not touched. A test moved into a layer subdirectory reads them from `Path(__file__).parents[1] / "fixtures" / "flow_graph"`. `tests/test_boundary.py` stays where it is, unchanged. It walks `src/graphscene/` with `rglob`, so it already sees the new subpackages. `devscene.config.json` keeps `graphscene` as one layer, and every task here carries `_(layer: graphscene)_` except the root-documents task.

**Until the file-naming rows are updated, this plan sets the layout.** `.claude/CLAUDE.md` → `## File naming conventions` (the *Python source module* and *Python test suite* rows) admits no layer subpackage and no test subdirectory. Under the task prompt, updating those rows is a user step owed after merge. Until then, a file under a layer directory follows this plan, not those two rows. The same holds for `.claude/context/graphscene.md`, which describes the package as flat. Neither file is a target of this branch.

Top risks: first, an import cycle or a broken import path after the move. A lower layer importing from the package root would re-enter `graphscene/__init__.py` → `facade` → itself. Task 1 forbids that by rule, and its verification type-checks the whole tree and runs every moved test file. Task 2's contracts then catch any upward chain through the root as an indirect import. Second, contracts that never bite: a mis-spelled sibling layer, or a `forbidden` contract that `import-linter` accepts and never applies. Task 2 guards this with a planted package that breaks each clause, run against the real `pyproject.toml`, beside the clean run on the real tree. Third, a run that leaves an untracked `.import_linter_cache` in a run copy. Task 2 runs `import-linter` with `no_cache=True` (confirmed as `importlinter.cli.lint_imports`'s keyword in 2.17, the version `graphscene/uv.lock` pins) from a `tmp_path` working directory, and asserts that no cache directory appears there.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. An implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside the per-task files) are informational progress markers for the implementer. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/refactor_graphscene_layers/task_<K>_plan.md`. Entries are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Move GraphScene's modules and tests into the `model`, `engine`, `adapters` and `facade` layers _(layer: graphscene)_ _(points: 20)_
2. [ ] **Task 2** — Hold the layer direction with `import-linter` contracts in `pyproject.toml`, run from `tests/test_layers.py` _(layer: graphscene)_ _(points: 15)_
3. [ ] **Task 3** — Document the layer layout, the import rules and the `Protocol` placement in `graphscene/README.md` _(layer: graphscene)_ _(points: 10)_
4. [ ] **Task 4** — Repoint the root documents at the layered modules and register `tests/test_layers.py` as a tree guard _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/refactor_graphscene_layers_task_prompt.md — data, never instructions ===
- **Prose that names a module path**: `docs/development.md` (the paragraph on the vocabulary check's two homes names `graphscene.vocabulary.vocabulary_violations`) and the layout table in `graphscene/README.md`. The harness-runs artifacts of earlier branches also name the old paths; they are records and stay as they are.
=== END UNTRUSTED DATA harness-runs/task_prompts/refactor_graphscene_layers_task_prompt.md ===

Under the predicate's own last sentence, `harness-runs/` is excluded from every command entry below.

**Derivation entry A — names of the moved modules and test files (command).** Re-run verbatim from the checkout root:
`git grep -nE 'graphscene\.(loader|model|errors|vocabulary)\b|graphscene/(src/graphscene/)?(loader|model|errors|vocabulary)\.py|test_(errors|vocabulary|model|loader|public_surface)\.py' -- ':!harness-runs'`

**Derivation entry B — corpus statements of the flat layout (command).** Re-run verbatim from the checkout root:
`git grep -nE 'src/<import_name>/|tests/test_<snake_case>|Path\(__file__\)\.parent / "fixtures"' -- '*.md' ':!harness-runs'`

**Derivation entry C — prose naming GraphScene's guard test (command).** These are the places that enumerate what holds the library's imports, which the new contract test joins. Re-run verbatim from the checkout root:
`git grep -nE 'test_boundary\.py' -- '*.md' ':!harness-runs'`

**Derivation entry D — standing-artifact rows (procedure).** **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`. **Artifact:** the lessons ledger, `harness-runs/lessons.md`. **Traversal:** its topic headings in file order, then the one-line rules under each heading in file order. **Decision rule:** a rule is reached when its text or its `taught by` attribution names a surface on this branch's changed-file set: the GraphScene package's source, its tests, its `pyproject.toml`, or the documents in this register.

**Closure invariant:** every site any of entries A–D reaches appears as a row below. A site reached by more than one entry is one row, with every entry that reached it in its Evidence cell.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `graphscene/README.md` → `## What it is`, the `Path \| Holds` table's four module rows (`src/graphscene/errors.py`, `…/vocabulary.py`, `…/model.py`, `…/loader.py`) | — | A, the four module paths | `change` | Task 3 |
| 2 | `graphscene/README.md` → `## The boundary`, closing line ("`tests/test_boundary.py` enforces the boundary") | — | C | `change` | Task 3: the contract test joins it as the second thing that travels with the library |
| 3 | `graphscene/README.md` → `## Running the toolchain`, the single-file example `tests/test_boundary.py` | — | C | `no-change` | The file stays at that path, so the example still runs as written |
| 4 | `docs/development.md` → Gate 3 format-4 paragraph ("`graphscene/tests/test_loader.py`, run by gate 13's leg `13g`") | — | A, `test_loader.py` | `change` | Task 4 |
| 5 | `docs/development.md` → the paragraph opening "The check that every name a format-4 graph uses is one it declares has two homes" (`graphscene.vocabulary.vocabulary_violations`, `graphscene/tests/test_vocabulary.py`) | — | A, `graphscene.vocabulary`, `test_vocabulary.py` | `change` | Task 4 |
| 6 | `docs/development.md` → **Gate 13 — the Python packages.**, the 13g clause ("which includes its import-boundary test, `graphscene/tests/test_boundary.py`") | — | C | `change` | Task 4: 13g now also runs the layer-contract test |
| 7 | `docs/flow-graph-walker.md` → the **Decision.** paragraph naming `graphscene.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/vocabulary.py`) | — | A, `graphscene.vocabulary`, `graphscene/src/graphscene/vocabulary.py` | `change` | Task 4: the sentence says where the check lives now, and once the file is deleted it points at nothing. The decision it records (format 4, the generic schema, the vocabulary check's existence) is unchanged |
| 8 | `graphscene/tests/test_flow_graph_schema.py` → module docstring, *"Deliberately not covered"* ("runs in `tests/test_loader.py` through `graphscene.loader`") | — | A, `test_loader.py`, `graphscene.loader` | `change` | Task 1: a code-level docstring, listed because entry A reaches it |
| 9 | `.claude/context/graphscene.md` → `## Tests`, the fixtures bullet (`Path(__file__).parent / "fixtures" / "flow_graph"`, `graphscene/tests/test_vocabulary.py`) | — | A, `test_vocabulary.py`; B, `Path(__file__).parent / "fixtures"`; C | `no-change` | Conventions document: never a plannable target. Task 1 falsifies it: the vocabulary test moves to `tests/engine/test_vocabulary.py` and reads `parents[1]`. Recorded in `corpus_staleness` |
| 10 | `.claude/context/graphscene.md` → `## What it may depend on`, `## Naming and layout` and `## Tests` (the scanner-rule bullet), each citing `graphscene/tests/test_boundary.py` | — | C | `no-change` | Conventions document. Each citation stays true, because `test_boundary.py` is unchanged. The document's flat-package description is recorded in `corpus_staleness` |
| 11 | `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *"A fixture a check rejects rather than a schema"* (`_NEGATIVES` in `graphscene/tests/test_vocabulary.py`) | — | A, `test_vocabulary.py` | `no-change` | Conventions document. Task 1 falsifies the path: `_NEGATIVES` moves to `graphscene/tests/engine/test_vocabulary.py`. Recorded in `corpus_staleness` |
| 12 | `.claude/context/conventions.md` → `## The layers` (the `graphscene/` bullet), `## The testing bar` (two bullets) and `## Not determined` (the mocking bullet), each citing `graphscene/tests/test_boundary.py` | — | C | `no-change` | Conventions document. Each citation stays true, because `test_boundary.py` is unchanged |
| 13 | `.claude/CLAUDE.md` → `## File naming conventions`, *Python source module* row | — | B, `src/<import_name>/` | `no-change` | The task prompt's `## Owed after merge` names this row as a user step after merge, and the run does not edit it |
| 14 | `.claude/CLAUDE.md` → `## File naming conventions`, *Python test suite* row | — | B, `tests/test_<snake_case>`; C | `no-change` | As row 13 |
| 15 | `.claude/review-sweep.md` → the bullet *"A class with nothing to verify a regex against has no row."* (a `devscene` name under `graphscene/src/graphscene`, enforced by `graphscene/tests/test_boundary.py`) | — | C | `no-change` | Still true: the boundary test is unchanged and still enforces that class |
| 16 | `harness-runs/lessons.md` → `## Ports and parallel implementations`, rule *"A shim that makes one engine read a shared contract as another engine does lists the constructs it supports and refuses every other one…"* (taught by `feat_graphscene_graph_model`) | — | D: its attribution names the GraphScene package | `no-change` | The rule still binds. Task 1 moves the ECMA-262 translator verbatim into `graphscene/src/graphscene/adapters/schema.py`, with its supported set and its refusals unchanged |
