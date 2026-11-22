### Task 2 — Add `static_violations` with the five generic graph checks and their fixtures in `engine/static_check.py`

**Goal:** Port the generic checks of `scripts/check-flow-graph.sh` → `THE CONTRACT` — 1 `reachable-from-start`, 2 `reaches-terminal`, 3 `fail-cycle-capped`, 8 `gate-in-round` and 9 `round-fan-out` — onto the typed `FlowGraph`, restated on declared primitives. Ship them behind one call, `static_violations(graph: FlowGraph) -> list[Violation]`, which runs Task 1's reference check first. Add one format-4 fixture per ported check.

**Depends on:** Task 1. That task produces `reference_violations(graph: FlowGraph) -> list[Violation]` in `graphscene/src/graphscene/engine/references.py`. Its violations' reasons open with `node-known`, `counter-known`, `path-known`, `report-slot-known`, `prompt-known` or `start-in-entries`, and it reports in document order. This task calls it and owns nothing in that module.

**Where this task stops.** `static_violations` is defined here. Task 3 makes `load_graph` run it as stage `"static"`, and Task 4 exports it from the package root and runs these fixtures through `load_graph`. Checks 4 to 7 of the bash contract read plugin documents and are **not** ported. `scripts/check-flow-graph.sh` is not touched.

### Targets

- `graphscene/src/graphscene/engine/static_check.py` (new)
- `graphscene/tests/engine/test_static_check.py` (new), the module's own suite
- `graphscene/tests/fixtures/flow_graph/static_negative_reachable_from_start.json`, `static_negative_reaches_terminal.json`, `static_negative_fail_cycle_capped.json`, `static_negative_gate_in_round.json`, `static_negative_round_fan_out.json` (all new)

**Work:**

- [ ] `static_check.py` imports only `graphscene.engine.references`, `graphscene.model.*` and the standard library. Its docstring states what it owns. Its *"The rule:"* paragraph says: `static_violations` returns the reference violations alone when there are any. Otherwise it returns the graph checks' violations, all of check 1, then 2, 3, 8 and 9. Each check reports nodes in key order, and every reason opens with its check id. The docstring also names **the walked edge set W**: a `RouteEdge`'s `to`, a `BindingEdge`'s `resume` when it is not `None`, each `SkipEntry`'s `to`, and a round node's fan-out to each of its `gates`. Add a *"Deliberately not checked:"* list:
  - schema validity and declared names: earlier loading stages;
  - checks 4–7 and what runs a node: harness checks, outside this package.

  The checks are total: they look targets, bindings and outcome declarations up with `.get`, so a graph built in code that an earlier stage would refuse never raises.
- [ ] Checks 1–3. Exact paths and reasons:
  - **1** — a node not reached from `start` over W gets `Violation("nodes.<id>", "reachable-from-start: node '<id>' is not reached from start '<start>'")`.
  - **2** — a **sink** is a terminal node, or a node with a `BindingEdge` whose binding is a `StopBinding`, or a `RouteEdge` whose `on_cap.binding` is a `StopBinding` (looked up in `graph.vocabulary.bindings`). A node from which no path over W reaches a sink gets `Violation("nodes.<id>", "reaches-terminal: node '<id>' reaches no terminal node and no stop binding")`.
  - **3** — let F be every `RouteEdge` whose `increment` is `None`, plus every skip edge. F excludes binding edges, which carry the interrupt-resume exemption, and fan-out edges. Check every `RouteEdge` u → v, outcomes in key order, whose outcome's declaration has `verdict == "fail"` and whose `increment` is `None`. When u is reachable from v over F, that edge gets `Violation("nodes.<u>.outcomes.<o>", "fail-cycle-capped: outcome '<o>' routes '<u>' -> '<v>' with no increment, and '<v>' reaches '<u>' again")`. Every counter has a cap in format 4, so "carries an increment" is the capped case.
- [ ] Checks 8–9. Exact paths and reasons, in node key order:
  - **8a** — a dispatch node with a fail-verdict `RouteEdge` whose `increment` is `None` must be in the `gates` of exactly one round node. Otherwise it gets `Violation("nodes.<id>", "gate-in-round: node '<id>' routes a fail verdict with no increment and is a gate of <c> round nodes, not exactly one")`. `findingsFolder` is not read.
  - **8b** — each round's `gates[i]` and then `writer` naming an existing node that is not a dispatch node gets `Violation("nodes.<r>.gates[<i>]", "gate-in-round: round '<r>' names '<x>' as a gate, which is not a dispatch node")` or `Violation("nodes.<r>.writer", "gate-in-round: round '<r>' names '<x>' as its writer, which is not a dispatch node")`.
  - **9** — per round, over its **dispatch** gates in gate order (a non-dispatch gate or writer is 8b's alone):
    - (i) every outcome of the gate declaring a verdict must be a `RouteEdge` to the round. Otherwise: `Violation("nodes.<g>.outcomes.<o>", "round-fan-out: gate '<g>' of round '<r>' does not route outcome '<o>' to the round")`.
    - (ii) the gate must have an outcome declaring `pass` and one declaring `fail`, wherever it routes them. Otherwise: `Violation("nodes.<g>.outcomes", "round-fan-out: gate '<g>' of round '<r>' routes no outcome declaring verdict <pass|fail>")`.
    - (iii) every `skip[i].to` must be the round. Otherwise: `Violation("nodes.<g>.skip[<i>].to", "round-fan-out: gate '<g>' of round '<r>' skips to '<t>', not to the round")`.
    - (iv) a dispatch writer must route at least one `RouteEdge` to the round. Otherwise: `Violation("nodes.<r>.writer", "round-fan-out: writer '<w>' of round '<r>' routes no outcome to the round")`.
    - (v) any other edge whose target is the round — a route `to` or a `resume` that is neither a gate's verdict `RouteEdge` nor a writer's `RouteEdge`, or a skip of a node that is not one of its gates — gets `Violation("nodes.<u>.outcomes.<o>", "round-fan-out: round '<r>' is targeted by '<u>' outcome '<o>', which is neither a verdict edge of one of its gates nor an edge of its writer")` or `Violation("nodes.<u>.skip[<i>]", "round-fan-out: round '<r>' is targeted by a skip of '<u>', which is not one of its gates")`.

    Report in the order (i)–(iii) per gate, then (iv), then (v) in node key order.
- [ ] Five fixtures, each a copy of `graphscene/tests/fixtures/flow_graph/valid_generic.json` with one change. Each stays schema-valid, vocabulary-valid and reference-valid, and returns exactly the one violation shown:
  - `static_negative_reachable_from_start.json`: adds node `orphan` = `{"kind": "dispatch", "agent": "article-archiver", "heartbeat": "[archive · attempt {iteration}] → article-archiver", "outcomes": {"done": {"to": "published"}}}`. Expected: `Violation("nodes.orphan", "reachable-from-start: node 'orphan' is not reached from start 'draft'")`.
  - `static_negative_reaches_terminal.json`: replaces `published` with `{"kind": "dispatch", "agent": "article-publisher", "heartbeat": "[publish · attempt {iteration}] → article-publisher", "outcomes": {"done": {"to": "published"}}}`. Expected: `Violation("nodes.published", "reaches-terminal: node 'published' reaches no terminal node and no stop binding")`.
  - `static_negative_fail_cycle_capped.json`: `nodes.review_round.outcomes.rejected` becomes `{"to": "draft", "prompt": "rework"}`. `increment` and `onCap` are dropped together, because the schema's `dependencies` ties them. Expected: `Violation("nodes.review_round.outcomes.rejected", "fail-cycle-capped: outcome 'rejected' routes 'review_round' -> 'draft' with no increment, and 'draft' reaches 'review_round' again")`.
  - `static_negative_gate_in_round.json`: `nodes.review_round.gates` becomes `["edit_check", "published"]`. Expected: `Violation("nodes.review_round.gates[1]", "gate-in-round: round 'review_round' names 'published' as a gate, which is not a dispatch node")`.
  - `static_negative_round_fan_out.json`: `nodes.edit_check.outcomes.approved.to` becomes `"published"`. Expected: `Violation("nodes.edit_check.outcomes.approved", "round-fan-out: gate 'edit_check' of round 'review_round' does not route outcome 'approved' to the round")`.

  Task 6 lists all five in `validate:graphscene-schema`, and Task 4 lists them in `_STATIC_NEGATIVES` in `graphscene/tests/facade/test_loading.py`.
- [ ] `test_static_check.py` opens with a docstring stating *"The rule this file exists to enforce"*, plus a *"Deliberately not covered:"* list naming checks 4–7, what runs a node, and agreement with the bash checker on the harness's graph, which needs the harness side and belongs to the cutover. Planted graphs are complete format-4 mappings built with `graphscene.adapters.builder.build_flow_graph`, with helpers kept in this file. Cases, each asserting the exact `list[Violation]`:
  - **check 1**: a node reached only by fan-out, only by an interrupt `resume`, or only by a skip is reached; an unreached node is named.
  - **check 2**: a stop-binding edge and an `onCap` stop each make a sink; an interrupt binding edge does not.
  - **check 3**: a fail edge carrying an increment is exempt; a cycle closed only through a `resume` or only through fan-out is not reported.
  - **check 8**: a gate in zero rounds and a gate in two rounds are each named; an incrementing fail edge is not selected; a non-dispatch gate and a non-dispatch writer are each named.
  - **check 9**: one case per clause (i)–(v), including a verdict outcome that is a binding edge for (i).
  - a reference violation is returned alone, even when the same graph also has an unreachable node.
  - two checks firing in one graph come back in check order.
  - `valid_generic.json` built returns `[]`.
  - a `_NEGATIVES` list of the five fixtures, each returning exactly its one `Violation`.

  Expected values are hand-written from reading each graph.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py` passes.
- `bash scripts/typecheck.sh` passes.
- `grep -n "^from\|^import" graphscene/src/graphscene/engine/static_check.py` shows only `graphscene.engine.references`, `graphscene.model.*` and standard-library imports, never `graphscene.adapters`.
- `grep -nE "PASS|FAIL|<escalate>|<ask>|returned|findingsFolder|findings_folder" graphscene/src/graphscene/engine/static_check.py` finds no harness name used as a routing key. The only hits allowed are prose in the docstring that names the bash checker's ids.
