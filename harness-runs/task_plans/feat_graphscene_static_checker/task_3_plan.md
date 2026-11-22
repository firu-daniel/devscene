### Task 3 — Move the vocabulary check onto `FlowGraph` and load as schema, build, vocabulary, static

**Goal:** Make every engine check read one input, the built `FlowGraph`, and make loading run **schema → build → vocabulary → static**. `vocabulary_violations` takes a `FlowGraph` and reports exactly what it reports today. `load_graph` adds the static stage, a new `Stage` member `"static"`. The builder's docstring stops promising a vocabulary-valid input.

**Depends on:** Task 2. That task produces `static_violations(graph: FlowGraph) -> list[Violation]` in `graphscene/src/graphscene/engine/static_check.py`, which returns `[]` for `valid_generic.json`. When the reference check finds anything, it returns those violations alone; otherwise it returns the graph-check violations. This task calls it from `load_graph` and changes nothing in it. Why the input is the model is the story index's `## Context` decision. This task carries it out for the vocabulary check.

**Where this task stops.** The public surface is Task 4's: `static_violations` is not added to either `__all__` here, and `graphscene/tests/facade/test_loading.py` and `graphscene/tests/test_public_surface.py` are Task 4's files. `graphscene/README.md` is Task 5's.

### Targets

- `graphscene/src/graphscene/model/errors.py`
- `graphscene/src/graphscene/engine/vocabulary.py`
- `graphscene/tests/engine/test_vocabulary.py`
- `graphscene/src/graphscene/adapters/builder.py` (docstrings only)
- `graphscene/src/graphscene/facade/loading.py`

**Work:**

- [ ] `errors.py`: `Stage: TypeAlias = Literal["parse", "schema", "vocabulary", "static"]`. The model gets a new member, never a second error type (`.claude/context/graphscene.md` → `## Errors and the loading order`).
- [ ] `vocabulary.py`: `vocabulary_violations(graph: FlowGraph) -> list[Violation]`, importing `graphscene.model.flow_graph` and `graphscene.model.errors` only.
  - Read edge classes and binding classes off the model: `RouteEdge` / `BindingEdge`, `RouteEdge.on_cap`, `InterruptBinding` / `StopBinding` / `EndBinding`, `RoundNode`, `TerminalNode`, `SkipEntry.when`, and `OutcomeDeclaration.verdict`, where a `None` verdict is neither pass nor fail.
  - Delete `_mapping`, `_strings`, `_Binding` and `_bindings`.
  - Every path, reason and the document order stay **byte-identical**, including `onCap` in the serialized spelling and *"a binding that is not declared is reported as undeclared alone"*.
  - In the docstring, the graph now arrives as a built `FlowGraph`. *"Deliberately not checked:"* names schema validity and the build, both the caller's and both run first, and gives node-id references, reachability and caps to `graphscene.engine.static_check`.
- [ ] `test_vocabulary.py`: the planted graphs go through `graphscene.adapters.builder.build_flow_graph`. `_graph`, `_dispatch` and `_round` fill the keys the builder requires: `formatVersion`, `flow`, `description`, `start`, `entries`, `counters`, `paths` and `reports` at the root; `agent` and `heartbeat` on a dispatch node; `parallel`, `gates`, `writer`, `counter` and `convergingFrom` on a round node. `_load` builds each fixture.
  - Every existing expected `Violation` and every `str()` line stays **unchanged**, so the move is proven not to change what the check reports.
  - Update the header to say the check reads the built model. Its *"Deliberately not covered"* list names the static checker for node-id references.
- [ ] `builder.py`, docstrings only, no code change:
  - The module docstring's *"Deliberately not covered"* says validation is the facade's: the schema check runs before the build, and the vocabulary and static checks run on the model it returns. Checking that references exist is `graphscene.engine.static_check`'s.
  - Its opening sentence and `build_flow_graph`'s docstring say the input has passed the schema check, and no longer say it has passed the vocabulary check.
- [ ] `loading.py`: `load_graph` runs `schema_violations` and raises `GraphError("schema", …)`. It then runs `build_flow_graph`, then `vocabulary_violations(built)`, raising `GraphError("vocabulary", …)`, then `static_violations(built)`, raising `GraphError("static", …)`, and returns `built`.
  - The *"The rule:"* paragraph says a returned graph has passed the format-4 schema, been built, then passed the vocabulary check and the static checks, in that order. A graph failing one stage never reaches the next.
  - *"Deliberately not checked:"* drops node-id references, names and reachability, keeps duplicate JSON keys, and adds what runs a node (an agent's existence, its return schema), a harness check outside this package.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_vocabulary.py` passes, with every expected `Violation` in it unchanged from before this task: `git diff` on that file shows no edited `Violation(` literal or expected string.
- `bash scripts/typecheck.sh` passes. This is the check that `load_graph` no longer passes a mapping to `vocabulary_violations`.
- `grep -nE "_mapping|_strings|_Binding|_bindings" graphscene/src/graphscene/engine/vocabulary.py` finds nothing.
- `git diff graphscene/src/graphscene/adapters/builder.py` touches docstring lines only.
