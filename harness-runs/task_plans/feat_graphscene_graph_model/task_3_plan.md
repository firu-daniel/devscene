### Task 3 — Add the loader `load_graph` / `load_graph_file`: schema, then vocabulary, then typed objects

**Goal:** Load a declared flow graph. Validate parsed data against the format-4 schema the package ships, then against the vocabulary check, and return the typed model. Any rejection is a `GraphError` whose violations name the node and the field. A thin convenience reads a JSON file. The Python loader and `ajv` are then held to the same generic fixtures.

**Depends on:** Task 1 and Task 2. Each contract is restated exactly as consumed.

- **From Task 1 — `graphscene/src/graphscene/errors.py`:**
  - `Violation(path: str, reason: str)` is a frozen dataclass. The path is dotted from the graph root: object keys joined with `.`, array indices as `[i]`, and `""` for the root. `str()` renders `"<path>: <reason>"`, with `""` rendered as `(root)`.
  - `Stage = Literal["parse", "schema", "vocabulary"]`.
  - `GraphError(stage: Stage, violations: Sequence[Violation])` is a `ValueError` exposing `.stage` and `.violations: tuple[Violation, ...]`. It refuses an empty sequence.
  - `graphscene.vocabulary.vocabulary_violations(graph: Mapping[str, object]) -> list[Violation]` returns violations in document order. It expects a schema-valid graph.
- **From Task 2 — `graphscene/src/graphscene/model.py`:**
  - `build_flow_graph(graph: Mapping[str, object]) -> FlowGraph` builds the frozen typed model from a graph that has passed both checks.
  - It validates nothing. It raises `TypeError` only on a shape the schema refuses, which this loader never passes it.

**Where this task stops.**

- Node-id and other name references are **not** checked. A loaded graph may name a node, counter, path, report slot or prompt that does not exist. That is a later static checker's job, and the module docstring says so.
- No YAML and no builder authoring.
- No test reads outside `graphscene/`: the harness's own graph stays out of this suite.
- Exporting `load_graph`, `load_graph_file` and the types from the package root is **Task 4's**, which owns `graphscene/src/graphscene/__init__.py`. This task's tests import from `graphscene.loader` and `graphscene.errors`.

### Targets

- `graphscene/src/graphscene/loader.py` (new) — `load_graph`, `load_graph_file`.
- `graphscene/tests/test_loader.py` (new) — the module's own suite, which runs every generic fixture through the loader.
- `graphscene/tests/test_flow_graph_schema.py` — module docstring only. Its *"Deliberately not covered"* sentence about schema validation is no longer true.

**The contract this task defines.** Tasks 4 and 5 restate it.

```python
# graphscene/src/graphscene/loader.py
def load_graph(graph: object) -> FlowGraph: ...
def load_graph_file(path: str | os.PathLike[str]) -> FlowGraph: ...
```

**`load_graph`.** It takes JSON-shaped data as `json.loads` returns it, and runs three steps in this order:

1. **The schema step.** Validate with `jsonschema.Draft7Validator` against `files("graphscene") / "schemas" / "flow-graph.schema.json`, read through `importlib.resources`. Parse the schema once, then cache the validator.
   - Every error from `iter_errors` becomes `Violation(<rendered absolute_path>, error.message)`. The path renders keys joined with `.` and indices as `[i]`, and the empty path is `""`.
   - Sort the violations by `(path, reason)`.
   - If any exist, raise `GraphError("schema", …)`.
2. **The vocabulary step.** Otherwise run `vocabulary_violations`. If it returns any, raise `GraphError("vocabulary", …)`, kept in its document order.
3. **The build.** Otherwise return `build_flow_graph(graph)`.

A graph failing the schema never reaches the vocabulary step.

**`load_graph_file`.**

- It reads the file as UTF-8 and parses it with `json.loads`.
- On a `json.JSONDecodeError` it raises `GraphError("parse", [Violation("", f"not valid JSON: {error.msg} (line {error.lineno}, column {error.colno})")])`.
- An `OSError` propagates unchanged.
- It then returns `load_graph(parsed)`.

**Work:**

- [ ] **`loader.py` (new): `load_graph`.**
  - It opens with a module docstring stating what it owns: turning a declared graph into the typed model or a `GraphError`. It also states the rule: a returned graph has passed the shipped schema and the vocabulary check, in that order.
  - The docstring's *"Deliberately not checked:"* list names:
    - node-id references (`to`, `resume`, `gates`, `writer`, `start`, `entries`, `roundCounts`, a skip's `to`);
    - the names a graph gives its counters, paths, report slots and prompts;
    - reachability and counter caps;
    - duplicate JSON keys, which `json.loads` collapses to the last.
  - `import jsonschema` (or `from jsonschema import Draft7Validator`) is inside the boundary. It is declared in `graphscene/pyproject.toml` → `[project] dependencies`, and its import name equals its normalised name, so it needs no `_IMPORT_NAMES` entry (`.claude/context/graphscene.md` → `## What it may depend on`). Every other import is from the standard library or `graphscene` itself.
  - After the schema step passes, narrow `graph` to `dict` for `mypy` before the vocabulary step. A failed narrowing is unreachable, so assert it.
- [ ] **`loader.py`: `load_graph_file`**, exactly as specified above.
- [ ] **`test_loader.py` (new).**
  - It opens with the module docstring *"The rule this file exists to enforce"*: the loader rejects every fixture `ajv` rejects, at the schema stage, and every vocabulary negative, at the vocabulary stage. Each rejection names the node and the field where the fixture's one change sits, and `valid_generic.json` loads.
  - Read fixtures from `Path(__file__).parent / "fixtures" / "flow_graph"` through two explicit lists. Each path is hand-read from the fixture's one change against `valid_generic.json`, never taken from the loader's output.
    - `_SCHEMA_NEGATIVES: list[tuple[str, str]]`:
      - `schema_negative_format_version_3.json` → `formatVersion`
      - `schema_negative_no_vocabulary.json` → `""`
      - `schema_negative_unknown_primitive.json` → `vocabulary.bindings.<finish>.primitive`
      - `schema_negative_interrupt_without_resume_outcome.json` → `vocabulary.bindings.<pause>`
      - `schema_negative_outcome_verdict_and_held.json` → `vocabulary.outcomes.approved`
      - `schema_negative_skip_construct.json` → `nodes.edit_check.skip[0]`
      - `schema_negative_round_three_outcomes.json` → `nodes.review_round.outcomes`

      Each fixture raises `GraphError` with `stage == "schema"`, and its expected path is among the violations' paths.
    - `_VOCABULARY_NEGATIVES: list[tuple[str, str]]`:
      - `vocabulary_negative_unknown_outcome.json` → `nodes.draft.outcomes.finished`
      - `vocabulary_negative_unknown_binding.json` → `nodes.draft.outcomes.crashed.binding`
      - `vocabulary_negative_interrupt_without_resume.json` → `nodes.draft.outcomes.crashed`
      - `vocabulary_negative_undeclared_reason.json` → `nodes.draft.outcomes.crashed.reason`
      - `vocabulary_negative_round_without_fail_verdict.json` → `nodes.review_round.outcomes`
      - `vocabulary_negative_end_on_an_edge.json` → `nodes.draft.outcomes.crashed.binding`
      - `vocabulary_negative_unknown_predicate.json` → `nodes.edit_check.skip[0].when`

      Each fixture raises `GraphError` with `stage == "vocabulary"` and exactly one violation, at that path.
- [ ] **`test_loader.py`: planted and file cases.** Typed `-> None`, each asserting exact values:
  - `valid_generic.json` loads to a `FlowGraph` with `flow == "article_review"`.
  - `load_graph([])` raises stage `schema` with one violation at path `""`.
  - Removing `agent` from `nodes.draft` of a parsed copy of `valid_generic.json` raises stage `schema` with exactly `(Violation("nodes.draft", "'agent' is a required property"),)`. That is the node and the field.
  - Two planted schema errors in different nodes come back sorted by path.
  - A graph with both a schema error and an undeclared outcome raises stage `schema` only.
  - `load_graph_file` on `valid_generic.json` equals `load_graph` of the same parsed data.
  - A file under `tmp_path` holding `{` raises stage `parse` with exactly `(Violation("", "not valid JSON: Expecting property name enclosed in double quotes (line 1, column 2)"),)`.
  - A missing file under `tmp_path` raises `FileNotFoundError`.
  - `Draft7Validator.check_schema` accepts the shipped schema, read through `importlib.resources`.
- [ ] **`test_flow_graph_schema.py` (docstring only).**
  - Replace the *"Deliberately not covered"* item *"Schema validation itself: it runs through `ajv` from the repository root. This file only checks that each fixture parses."* with: schema validation runs in `tests/test_loader.py` through `graphscene.loader`, and through `ajv` from the repository root; this file only checks that each fixture parses.
  - Change no case and no list.

**Verification:**

- Run this task's two test files from the repository root, each as one plain foreground command:
  - `bash scripts/python-service.sh --package graphscene test tests/test_loader.py`
  - `bash scripts/python-service.sh --package graphscene test tests/test_flow_graph_schema.py`

  Both pass.
- **Every fixture is listed.** `ls graphscene/tests/fixtures/flow_graph` lists, besides `valid_generic.json`, exactly the names in `_SCHEMA_NEGATIVES` ∪ `_VOCABULARY_NEGATIVES`. No fixture is left unrun by the loader: the story index's second `Top risks:` entry.
- `grep -n -E '^(import|from) ' graphscene/src/graphscene/loader.py` shows only standard-library modules, `graphscene` and `jsonschema`.
- No file this task adds reads a path outside `graphscene/`: `grep -n -E '\.\./|cli/|templates' graphscene/tests/test_loader.py` has no hits.
- `mypy` `strict` and `ruff` are graded at the Run gates phase, by gate 13's legs `13f` and `13e`.
