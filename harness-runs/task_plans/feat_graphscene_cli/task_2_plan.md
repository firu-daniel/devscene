### Task 2 — Add the check document's encoder in `adapters`

**Goal:** Add `graphscene/src/graphscene/adapters/check_json.py`, the one owner of the **check document**, the JSON form the command line prints for the result of loading a graph. Its single function maps a `GraphError` (or its absence) to `{"stage", "violations": [{"path", "check", "reason"}]}`, including the split of a static reason into its check id and its text. A format goes in `adapters` (`.claude/context/graphscene.md` → `## The internal layers`, *"A store, an executor or another format goes in `adapters`"*; `graphscene/src/graphscene/adapters/__init__.py` → *"what touches a format or the outside world"*), so the command module re-encodes nothing.

**Where this layer stops.** This task adds one module and its suite. It loads no graph, prints nothing, parses no argv and chooses no exit status: the command line, which calls the encoder and writes its result, is **Task 3's**. Task 3 calls exactly this signature:

- `check_document(error: GraphError | None) -> dict[str, object]`

It is not a walk form, so it does not go in `graphscene/src/graphscene/adapters/walk_json.py` (Task 1's). `graphscene/README.md`'s `src/graphscene/adapters/` row entry for this module is **Task 4's** to write. The function does not join the public surface (`__all__`), just as `state_to_json` stays out of it (`graphscene/tests/test_public_surface.py` → `_EXPECTED`).

### Targets

- `graphscene/src/graphscene/adapters/check_json.py` (new): `check_document` and its opening docstring.
- `graphscene/tests/adapters/test_check_json.py` (new): the module's own suite.

**Work:**

- [ ] `check_json.py` → `check_document(error: GraphError | None) -> dict[str, object]`.
  - `None` (the graph loaded) returns `{"stage": None, "violations": []}`.
  - A `GraphError` returns `{"stage": error.stage, "violations": [...]}`, one object per entry of `error.violations`, in that order. Each object is `{"path": v.path, "check": …, "reason": …}`, keys in that order.
  - `path` is `Violation.path` verbatim: `""` for the root, never the `(root)` that `Violation.__str__` renders (`graphscene/src/graphscene/model/errors.py`).
  - **Only for `error.stage == "static"`**, split `v.reason` at its first `": "` with `str.partition`: `check` is the text before it and `reason` the text after it. Every static reason opens with its check id (`graphscene/src/graphscene/engine/static_check.py` → *"Every reason opens with its check id"*; `graphscene/src/graphscene/engine/references.py` → `node-known: '…' is not a node`). A static reason with no `": "` (a `GraphError` built in code, not by `static_violations`) keeps `check` `None` and `reason` verbatim, so the encoder is total.
  - For every other stage (`parse`, `schema`, `vocabulary`), `check` is `None` and `reason` is `v.reason` verbatim — a vocabulary reason such as `binding 'x' is not declared …` carries no check id even where it contains `": "`.
  - Import `GraphError` from `graphscene.model.errors`: a `model` import, which `adapters` may make (`graphscene/pyproject.toml` → contract `graphscene-layers`). Import nothing from `engine` (`graphscene/src/graphscene/adapters/__init__.py` → *"never imports `graphscene.engine`"*).
- [ ] `check_json.py` opening docstring, in the shape `walk_json.py`'s has (`.claude/context/graphscene.md` → `## Naming and layout`): what the module owns, then *"The rule:"* — the document's exact shape and key order, `check` set only for stage `static` from the id before the reason's first `": "`, and `path` the library's own path with `""` for the root. Then *"Deliberately not covered:"*: serializing to text (the caller's, with `json.dumps`), and validating that a static check id is one `static_check` defines.
- [ ] `graphscene/tests/adapters/test_check_json.py`. Open with *"The rule this file exists to enforce"* (`.claude/context/conventions.md` → `## The testing bar`), stating that every expected document is hand-written from reading the planted `GraphError` and never taken from the encoder's output. Cases, each comparing `check_document(...)` with a hand-written `dict` and asserting its key order:
  - **The clean document:** `check_document(None) == {"stage": None, "violations": []}`.
  - **A static violation split:** `GraphError("static", [Violation("nodes.a.to", "node-known: 'b' is not a node")])` → `check` `"node-known"`, `reason` `"'b' is not a node"`.
  - **Two static violations keep their order**, each split.
  - **A schema violation:** `check` `None`, `reason` verbatim.
  - **A vocabulary violation whose reason contains `": "`** is not split.
  - **A parse-stage violation at the root:** `path` `""`, `check` `None`.
  - **A static reason with no `": "`:** `check` `None`, `reason` verbatim.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_check_json.py` passes.
- Every expected value in the suite is a hand-written literal, never taken from the function's output (`.claude/context/graphscene.md` → `## Tests`).
- `check_json.py` imports only `graphscene.model.errors` and the standard library; it prints nothing and calls no `json.dumps`.
- `check_document` is not in `graphscene/src/graphscene/__init__.py` or `graphscene/src/graphscene/facade/__init__.py`.
