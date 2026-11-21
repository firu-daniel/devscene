### Task 1 — Introduce `Violation` and `GraphError`, and return `Violation` values from `vocabulary_violations`

**Goal:** Give GraphScene one error type for every way a declared graph can be rejected. That is a structured `Violation(path, reason)` plus a `GraphError` exception carrying a stage and its violations. The existing vocabulary check moves onto it, so schema errors, vocabulary errors and a later static checker's findings share one shape instead of strings to parse back.

**Where this task stops.**

- This task produces the two types and changes `vocabulary_violations`'s element type. It loads nothing, validates nothing against the schema, and builds no model.
- The loader that raises `GraphError` is **Task 3's**. Task 3 also renders `jsonschema` errors into `Violation`s.
- Making `Violation` and `GraphError` importable from the package root (`graphscene.__all__`) is **Task 4's**. It owns `graphscene/src/graphscene/__init__.py`. This task does not edit that file, and its tests import from `graphscene.errors`.

### Targets

- `graphscene/src/graphscene/errors.py` (new) — `Violation`, `Stage`, `GraphError`.
- `graphscene/src/graphscene/vocabulary.py` — returns `list[Violation]`.
- `graphscene/tests/test_vocabulary.py` — expectations become `Violation` values.
- `graphscene/tests/test_errors.py` (new) — the new module's own suite.

**The contract this task defines.** Tasks 3 and 4 restate it, and each file restates exactly this:

```python
# graphscene/src/graphscene/errors.py
@dataclass(frozen=True)
class Violation:
    path: str    # dotted from the graph root: object keys joined with ".", array indices as "[i]";
                 # "" is the root
    reason: str
    def __str__(self) -> str: ...   # f"{path}: {reason}", with "" rendered as "(root)"

Stage: TypeAlias = Literal["parse", "schema", "vocabulary"]

class GraphError(ValueError):
    stage: Stage
    violations: tuple[Violation, ...]
    def __init__(self, stage: Stage, violations: Sequence[Violation]) -> None: ...
```

- `str(GraphError)` is the line `flow graph failed the <stage> check:` followed by one line per violation, each `str(violation)`, joined with `\n`.
- Constructing a `GraphError` with no violations raises `ValueError("a GraphError carries at least one violation")`. That is a programming error, never a rejection of a graph.

**Work:**

- [ ] **`errors.py` (new).**
  - It opens with a module docstring stating what it owns: the one error shape every stage of loading a graph reports in. It also states the rule: a path names the node and the field, in the dotted form above.
  - Implement the contract above exactly. Every function and attribute is fully annotated: `mypy` `strict` covers `src` and `tests`.
  - Imports stay inside the boundary: the standard library only (`.claude/context/graphscene.md` → `## What it may depend on`).
- [ ] **`vocabulary.py`.**
  - Every site that today builds the string `f"{path}: {reason}"` instead builds `Violation(path, reason)`. The path is everything before the first `": "` of the old string, and the reason is everything after it.
  - `str()` of each value must equal the old string byte for byte.
  - `vocabulary_violations(graph: Mapping[str, object]) -> list[Violation]`, still in document order. Import with `from graphscene.errors import Violation`.
  - Update the module docstring's sentence *"returns one `<path>: <reason>` string per violation"* to say it returns one `Violation` per violation, whose `str()` is that `<path>: <reason>` line. Keep its *"Deliberately not checked:"* list unchanged.
  - Update the function's own docstring the same way.
- [ ] **`test_vocabulary.py`.**
  - Convert every expected string into the `Violation` it splits into at its first `": "`. Every planted-case assertion and every `_NEGATIVES` entry compares `Violation` values: `_NEGATIVES` becomes `list[tuple[str, Violation]]`.
  - Keep each case's name, and keep the module docstring's rule, extended to say the check returns `Violation` values.
  - Example: `Violation("nodes.a.outcomes.stalled", "outcome 'stalled' is not declared in vocabulary.outcomes")`.
- [ ] **`test_errors.py` (new).**
  - It opens with the module docstring *"The rule this file exists to enforce"*: one error shape for every stage, rendered as `<path>: <reason>`.
  - Typed plain `pytest` functions `-> None`, one per clause, each asserting the exact text:
    - `str(Violation("nodes.draft.agent", "x"))` is `"nodes.draft.agent: x"`.
    - `str(Violation("", "x"))` is `"(root): x"`.
    - A `Violation` is frozen: assigning `path` raises `dataclasses.FrozenInstanceError`.
    - A `GraphError("schema", [v1, v2])` exposes `stage == "schema"` and `violations == (v1, v2)`, a tuple. Its `str()` is the exact three-line text.
    - It is an instance of `ValueError`.
    - `GraphError("vocabulary", [])` raises `ValueError` with the exact message above.
  - One case renders every violation `vocabulary_violations` returns for a planted graph back to the old strings. It is a case in **this** file, not in `test_vocabulary.py`. Use a graph with an undeclared outcome and an undeclared skip predicate, asserting `[str(v) for v in …]` equals `["nodes.a.outcomes.stalled: outcome 'stalled' is not declared in vocabulary.outcomes", "nodes.a.skip[0].when: predicate 'never' is not declared in vocabulary.predicates"]`. This is the story index's first `Top risks:` entry.

**Verification:**

- Run this task's two test files from the repository root, each as one plain foreground command:
  - `bash scripts/python-service.sh --package graphscene test tests/test_errors.py`
  - `bash scripts/python-service.sh --package graphscene test tests/test_vocabulary.py`

  Both pass.
- Every `_NEGATIVES` expectation and every planted-case expectation in `test_vocabulary.py` still renders, through `str()`, to the exact string it held before this task. Diff the old and new expectation text to confirm nothing was reworded.
- `grep -n 'def vocabulary_violations' graphscene/src/graphscene/vocabulary.py` prints a signature ending `-> list[Violation]:`.
- `mypy` `strict` and `ruff` are graded at the Run gates phase, by gate 13's legs `13f` and `13e`. Every new function and test carries full annotations so those legs have nothing to find.
