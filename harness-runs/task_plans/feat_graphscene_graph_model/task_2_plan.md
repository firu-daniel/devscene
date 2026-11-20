### Task 2 — Add the typed flow-graph model in `graphscene.model` with its builder `build_flow_graph`

**Goal:** Expose a declared format-4 flow graph as immutable typed objects. These are frozen dataclasses mirroring the schema one to one, plus the builder that turns an already-validated parsed graph into them. Callers then read `graph.nodes["draft"].outcomes["done"].to` instead of walking nested `dict[str, object]`.

**Depends on:** nothing in this branch. It imports nothing from Task 1's `graphscene.errors`: the builder never rejects a graph.

**Where this task stops.**

- `build_flow_graph` **does not validate**. It is called only by **Task 3's** loader, after the schema check and the vocabulary check have both passed.
- A shape the schema would have refused is a programming error here. The builder raises `TypeError` naming the dotted path, never a `GraphError`.
- **Node-id references stay ids.** `to`, `resume`, `gates`, `writer`, `start`, `entries`, `round_counts` and a skip entry's `to` are `str` values, never resolved into object links. The same holds for counter, path, report-slot, prompt and binding names. Checking that they exist belongs to a later static checker.
- Exporting these names from the package root is **Task 4's**, which owns `graphscene/src/graphscene/__init__.py`. This task's test imports from `graphscene.model`.

### Targets

- `graphscene/src/graphscene/model.py` (new) — the types and `build_flow_graph`.
- `graphscene/tests/test_model.py` (new) — the module's own suite.

**The contract this task defines.** Task 3 calls `build_flow_graph`, and Task 4 exports the names.

```python
# graphscene/src/graphscene/model.py — every class @dataclass(frozen=True)
NodeKind: TypeAlias = Literal["dispatch", "round", "terminal"]
Primitive: TypeAlias = Literal["interrupt", "stop", "end"]
Verdict: TypeAlias = Literal["pass", "fail"]

OutcomeDeclaration(verdict: Verdict | None, held: bool)
InterruptBinding(resume_outcome: str)        # primitive: ClassVar[Literal["interrupt"]]
StopBinding(reasons: tuple[str, ...])        # primitive: ClassVar[Literal["stop"]]
EndBinding()                                 # primitive: ClassVar[Literal["end"]]
BindingDeclaration: TypeAlias = InterruptBinding | StopBinding | EndBinding
PredicateDeclaration(records: str, in_round_counts: bool)
Vocabulary(outcomes: Mapping[str, OutcomeDeclaration],
           bindings: Mapping[str, BindingDeclaration],
           predicates: Mapping[str, PredicateDeclaration])
CounterDeclaration(cap: int)
OnCapEdge(binding: str, reason: str, summary: str | None,
          round_counts: tuple[str, ...] | None, evidence: str | None)
RouteEdge(to: str, increment: str | None, reset: str | None, prompt: str | None,
          ledger: str | None, report: Mapping[str, str] | None, on_cap: OnCapEdge | None)
BindingEdge(binding: str, resume: str | None, reason: str | None, summary: str | None,
            round_counts: tuple[str, ...] | None, evidence: str | None)
Edge: TypeAlias = RouteEdge | BindingEdge
SkipEntry(when: str, to: str, report: Mapping[str, str] | None)
DispatchNode(id: str, agent: str, heartbeat: str, outcomes: Mapping[str, Edge],
             prompts: tuple[str, ...] | None, findings_folder: str | None,
             skip: tuple[SkipEntry, ...] | None)                     # kind: ClassVar[Literal["dispatch"]]
RoundNode(id: str, parallel: bool, gates: tuple[str, ...], writer: str, counter: str,
          converging_from: int, plan: tuple[str, ...] | None, revision_note: str | None,
          outcomes: Mapping[str, Edge])                              # kind: ClassVar[Literal["round"]]
TerminalNode(id: str, binding: str)                                  # kind: ClassVar[Literal["terminal"]]
Node: TypeAlias = DispatchNode | RoundNode | TerminalNode
FlowGraph(format_version: Literal[4], flow: str, description: str, vocabulary: Vocabulary,
          start: str, entries: tuple[str, ...], counters: Mapping[str, CounterDeclaration],
          paths: Mapping[str, str], reports: tuple[str, ...], nodes: Mapping[str, Node])

def build_flow_graph(graph: Mapping[str, object]) -> FlowGraph: ...
```

**The mapping rules.** State all of them in the module docstring.

- **Attribute names.** Each attribute is its schema key in snake_case: `formatVersion`→`format_version`, `resumeOutcome`→`resume_outcome`, `inRoundCounts`→`in_round_counts`, `convergingFrom`→`converging_from`, `revisionNote`→`revision_note`, `findingsFolder`→`findings_folder`, `onCap`→`on_cap`, `roundCounts`→`round_counts`. Every other key keeps its own name. The one addition is `id` on a node, which is its key in `nodes`.
- **Containers.** A JSON array becomes a `tuple`. A JSON object becomes a read-only `types.MappingProxyType` that keeps the declaration's key order.
- **Absent keys.** An absent optional key is `None`. The single exception is `held`, which the schema allows only as `true`: it becomes `bool`, `False` when absent.
- **Which classes.** An edge carrying `binding` is a `BindingEdge`, and any other edge is a `RouteEdge`, as the schema's `edge` `if`/`then` decides. A node's class follows `kind`. A binding's class follows `primitive`.
- **Fixed words.** No harness name is fixed anywhere. The only fixed words are the schema's own enums, typed as the three `Literal` aliases.

**Work:**

- [ ] **`model.py` (new): the types.**
  - It opens with a module docstring stating:
    - what it owns: the typed, immutable form of a declared graph;
    - the mapping rules above;
    - a *"Deliberately not covered:"* list. It covers validation (the loader's), resolving node-id and other name references (a later static checker's), and any harness name.
  - Declare every type and alias in the contract above with full annotations. Imports are the standard library only.
- [ ] **`model.py`: `build_flow_graph`.**
  - Build each object from the parsed mapping through small private readers that narrow `object` to the expected type for `mypy` `strict`. Each reader raises `TypeError(f"{path}: expected <type>")` on a shape the schema would have refused, using the same dotted path form as `graphscene.errors.Violation.path`.
  - Wrap every object in `MappingProxyType` over a fresh `dict`, so the caller's input is never aliased.
- [ ] **`test_model.py` (new).**
  - It opens with the module docstring *"The rule this file exists to enforce"*: the model mirrors the declaration one to one, and keeps references as ids.
  - Typed plain `pytest` cases. Read `valid_generic.json` from `Path(__file__).parent / "fixtures" / "flow_graph"` with `json`. Every expected value is hand-written from reading that fixture:
    - `start == "draft"` and `entries == ("draft", "review_round")`.
    - `list(nodes) == ["draft", "edit_check", "review_round", "published"]`, so key order is kept.
    - `counters["attempt"].cap == 3`.
    - `vocabulary.bindings["<pause>"] == InterruptBinding(resume_outcome="resumed")`.
    - `vocabulary.bindings["<halt>"] == StopBinding(reasons=("limit", "crash"))`.
    - `vocabulary.outcomes["crashed"].held is True`, and `vocabulary.outcomes["done"] == OutcomeDeclaration(verdict=None, held=False)`.
    - `vocabulary.predicates["stage_disabled"] == PredicateDeclaration(records="bypassed", in_round_counts=False)`.
    - `nodes["draft"]` is a `DispatchNode` with `prompts == ("first", "rework")`, `findings_folder is None` and `skip is None`.
    - Its `outcomes["crashed"] == BindingEdge(binding="<halt>", resume=None, reason="crash", summary=None, round_counts=None, evidence=None)`.
    - `nodes["edit_check"].skip == (SkipEntry(when="stage_disabled", to="review_round", report={"edit_check": "bypassed"}),)`, and its `findings_folder == "{state_dir}/edit_checks/{branch}/"`.
    - `nodes["review_round"]` is a `RoundNode` with `gates == ("edit_check",)`, `writer == "draft"`, `converging_from == 1`, `plan == ("article",)` and `revision_note is None`.
    - Its `outcomes["rejected"]` is a `RouteEdge` with `increment == "attempt"` and `prompt == "rework"`. Its `on_cap` is `OnCapEdge(binding="<halt>", reason="limit", summary=<the fixture's sentence>, round_counts=("edit_check",), evidence="article")`.
    - `nodes["published"] == TerminalNode(id="published", binding="<finish>")`.
- [ ] **`test_model.py`: planted cases.**
  - **Every optional key present.** A planted in-test graph sets `ledger`, `reset`, `revisionNote`, `resume` and `summary` on a binding edge, `roundCounts` and `evidence`. Assert each lands on its snake_case attribute.
  - **References stay strings.** `nodes["draft"].outcomes["done"].to == "review_round"` and is a `str`, not a node.
  - **Immutability.** Assigning an attribute raises `dataclasses.FrozenInstanceError`, and item assignment on `graph.nodes` raises `TypeError`.
  - **No aliasing.** Mutating the input mapping after the build leaves the built graph unchanged.
  - **The builder's own refusal.** It raises `TypeError` with the exact text `"nodes.draft.agent: expected str"` when `agent` is an integer.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_model.py`, run from the repository root as one plain foreground command, passes.
- `grep -n -E 'import' graphscene/src/graphscene/model.py` shows standard-library imports only.
- Every key the schema declares under `definitions` appears as an attribute in the contract above, or as a class choice for `kind`, `primitive` or `binding`. This is the story index's third `Top risks:` entry. Walk `graphscene/src/graphscene/schemas/flow-graph.schema.json` → each `properties` block against the model's fields and find none unmapped.
- `mypy` `strict` and `ruff` are graded at the Run gates phase, by gate 13's legs `13f` and `13e`.
