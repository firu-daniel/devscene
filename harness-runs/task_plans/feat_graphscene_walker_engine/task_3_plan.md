### Task 3 — Build the walk's transitions in `engine/transitions.py`: arrival, skips, edges, caps, bindings, round open and close

**Goal:** Give the engine one module holding every transition that moves a walk from one node to the next: arriving at a node, following an edge, taking a binding, and opening and closing a round. These functions call one another recursively: arriving at a round opens it, an all-skipped round closes at once, and closing a round follows an edge that arrives somewhere. So they live in one module, over one engine-internal mutable draft. The walk routes on declared primitives only, never on a name.

**Depends on:** Task 1 and Task 2. This task consumes, from `graphscene.model.walk_actions`:

- `Dispatch(node, agent, prompt, counters, round_number, converging, closed_round, passed)`;
- `DispatchSet(round, number, dispatches, passed)`;
- `Interrupt(binding, node, agent, resume, resume_outcome, passed)`;
- `Stop(binding, node, agent, reason, summary, evidence, round_counts, held, closed_round, passed)`;
- `End(binding, node, reports, passed)`;
- `Refused(reason)`, `GateRecord`, `SkipPassage(node, status)`, `RoundPassage(round, number, verdict)`, `LedgerPassage(entry)`, `Passage` and `Step`.

From `graphscene.model.walk_state` it consumes:

- `WalkState(flow, node, awaiting, pending, counters, round_numbers, open_round, prompts, reports, skipped)`;
- `OpenRound(round, number, due, records)`;
- `PredicateHost.answer(predicate, node) -> bool | None`.

**Where this layer stops.** This task does not do these, and they are not to be added here:

- Recording a gate's outcome in an open set, `Wait`, and the held join are **Task 4's** (`engine/rounds.py`). Task 4 calls `close_round`, `follow_edge` and `take_binding` from here.
- Validating a caller's `next` (an undeclared outcome, a finished walk, the wrong node), `start`'s entry rules, the store's lock, and reading or writing state are **Task 5's** (`engine/walker.py`).
- Nothing here reads a file or configuration, and nothing raises: every refusal is a returned `Refused`.

### Targets

- `graphscene/src/graphscene/engine/transitions.py` (new)
- `graphscene/tests/engine/walk_support.py` (new) — the engine suites' shared support: `planted(nodes, **overrides) -> FlowGraph` built through `graphscene.adapters.builder.build_flow_graph` from a copy of `valid_generic.json`'s top level (as `graphscene/tests/engine/test_vocabulary.py` → `_graph` builds), and `AnswerTable(answers: dict[tuple[str, str], bool | None])`, a `PredicateHost` answering `False` for any pair not listed.
- `graphscene/tests/engine/test_transitions.py` (new)

**Work:**

- [ ] **Docstring and `WalkDraft`.** The module docstring has a *"The rule:"* paragraph that states the transitions below, and a *"Deliberately not covered:"* list: a graph that did not pass `load_graph` (its guarantees are relied on, never re-checked), path templates, heartbeats, round files and the review loop's rules. Then declare `WalkDraft`, a mutable (non-frozen) `@dataclass` with:
  - fields: `flow`, `node`, `awaiting`, `pending: Action | None`, `counters: dict[str, int]`, `round_numbers: dict[str, int]`, `open_round: OpenRound | None`, `prompts: dict[str, str]`, `reports: dict[str, str]`, `skipped: dict[str, str]` and `passed: list[Passage]`;
  - `WalkDraft.fresh(graph) -> WalkDraft`: every `graph.counters` key at 0, every round node's number at 0, `pending=None`, `awaiting="dispatch"`, `node=graph.start`;
  - `WalkDraft.from_state(state) -> WalkDraft`, with `passed=[]`;
  - `freeze(self) -> WalkState`, which wraps each `dict` in a `MappingProxyType` over a copy. A `pending` of `None` is a programming error, so assert on it.

  **Every transition function sets `draft.pending` and `draft.awaiting` and returns a `Step`.** On a `Refused` the caller discards the draft.
- [ ] **`arrive(graph, host, draft, node_id, *, closed_round=(), open_gates=()) -> Step`.** It loops over the nodes it reaches, keeping a visited set. Revisiting a node returns `Refused(f"skip entries loop through node '{node_id}'")`. At each node:
  - **`TerminalNode`:** the binding is an end, so return `End(binding, node, reports=tuple((slot, draft.reports[slot]) for slot in graph.reports if slot in draft.reports), passed=tuple(draft.passed))` with `awaiting="done"`.
  - **`RoundNode`:** `return open_round(...)`.
  - **`DispatchNode`:** evaluate `node.skip` entries in order, asking `host.answer(entry.when, node_id)` on every arrival and never caching the answer.
    - `None` returns `Refused(f"the host cannot answer predicate '{entry.when}' for node '{node_id}'")`.
    - `True` records `entry.report` into `draft.reports`, appends `SkipPassage(node_id, vocabulary.predicates[entry.when].records)`, sets `draft.skipped[node_id] = entry.when`, and continues at `entry.to` with no dispatch.
    - When no entry holds, return `Dispatch` with:
      - `prompt=draft.prompts.get(node_id)` and `counters` a read-only copy;
      - for a gate of a round `r` (in node-key order): `round_number=draft.round_numbers[r]` and `converging=draft.counters[r.counter] >= r.converging_from`;
      - for the writer of a round `r` (the first such round in key order): `round_number=draft.round_numbers[r]` and `converging=None`;
      - otherwise `None` for both;
      - `closed_round` and `passed` from the draft.

      Set `awaiting="dispatch"` and `node=node_id`.
- [ ] **`follow_edge(graph, host, draft, node_id, edge, *, advance=None, closed_round=(), open_gates=(), held=()) -> Step`** works in this exact order, the bash walker's `follow_edge` order:
  1. A `BindingEdge` goes to `take_binding`.
  2. `reset` sets that counter to 0.
  3. `increment` adds 1. When the new value is `>= graph.counters[name].cap`, take `edge.on_cap` through `take_binding` with `cap` set, and stop there.
  4. When `advance` names a round node, add 1 to its round number. This happens only on a routed edge, never at the cap.
  5. Record `edge.report` into `draft.reports`.
  6. `edge.ledger` appends `LedgerPassage`.
  7. Set `draft.prompts[edge.to] = edge.prompt` when it is given, and remove the key otherwise.
  8. `arrive(edge.to, closed_round=closed_round)`.

  **`take_binding(graph, draft, node_id, name, *, reason, resume, summary, round_counts, evidence, cap=None, open_gates=(), held=(), closed_round=()) -> Step`** routes on the declaration's class. `agent` is the node's agent, or `None` for a round node.
  - **`InterruptBinding`:** `Interrupt(name, node_id, agent, resume, binding.resume_outcome, passed)`, with `awaiting="interrupt"` and `node=node_id`.
  - **`StopBinding`:** `Stop(...)`, with `awaiting="done"`, built as follows:
    - `summary` has `{cap}` replaced by `str(cap)` when a cap fired, and `{open_gates}` by `", ".join(open_gates)`;
    - `round_counts` is the edge's list minus every node in `draft.skipped` whose predicate has `in_round_counts` false;
    - `evidence` is the `paths` key unchanged.
  - **`EndBinding`** on an edge returns `Refused(f"binding '{name}' is an end; only a terminal node takes one")`. A loaded graph never reaches this.
- [ ] **`open_round(graph, host, draft, round_id) -> Step` and `close_round(graph, host, draft, round_id) -> Step`.**
  - **`open_round`:**
    - Evaluate each gate's skip entries in `gates` order before building anything, as `arrive` does. A skipped gate records its report, passage and `skipped` entry, and its `to` is **not** followed.
    - The due gates are the unskipped ones, in `gates` order. With none due, `return close_round(...)` at once.
    - Otherwise set `draft.open_round = OpenRound(round_id, number, due, records={})`, `node=round_id` and `awaiting="set"`.
    - Return `DispatchSet(round_id, number, dispatches=<one Dispatch per due gate, built as arrive builds a gate's, with passed=()>, passed=tuple(draft.passed))`.
  - **`close_round`:**
    - The failing gates are those whose record's outcome declares `verdict == "fail"`, in `gates` order. A skipped gate counts as passed. The verdict is `"fail"` if any gate failed, else `"pass"`.
    - Append `RoundPassage(round_id, number, verdict)`.
    - `closed = tuple(records[g] for g in gates if g in records)`.
    - Clear `draft.open_round`.
    - Pick the round's outcome whose declared verdict matches, and `follow_edge` it with `advance=round_id` on fail only, `closed_round=closed` and `open_gates=failing`.
- [ ] **`test_transitions.py`.** Its module docstring opens *"The rule this file exists to enforce"*. Every case drives functions on a `WalkDraft.fresh(planted(...))` with an `AnswerTable`, and every expected value is hand-written from the planted graph. Cover these:
  - arrival at a dispatch node;
  - a skip chain, its report and passage;
  - a skip loop refused with the exact text;
  - `None` from the host refused with the exact text;
  - reset-before-increment;
  - the cap firing at `>= cap` and not one below;
  - the `{cap}` / `{open_gates}` summary;
  - `round_counts` dropping an `in_round_counts`-false skipped node;
  - an interrupt, a stop and a terminal's `End` reports in `reports` order;
  - `open_round` with one gate skipped and one due;
  - an all-skipped round closing `pass` at once;
  - `close_round` on fail advancing the round number and handing `closed_round` to the writer's `Dispatch`, with `round_number` the advanced number.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/engine/test_transitions.py` passes.
- [ ] `transitions.py` imports only `graphscene.model` modules and the standard library, never `graphscene.adapters` (the `graphscene-layers` contract).
- [ ] Grep `transitions.py` for any outcome, binding or predicate name used as a literal and find none: routing is on `verdict`, `held`, the binding class, `records` and `in_round_counts` only.
