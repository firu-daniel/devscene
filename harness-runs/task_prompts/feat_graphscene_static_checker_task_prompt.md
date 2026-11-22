`feat_graphscene_static_checker` ports the flow-graph static checks (today `scripts/check-flow-graph.sh`) to GraphScene as a library call, and adds the check #414 left to it: that every id a graph names exists. Part of #376.

## Why

The schema checks shape and the vocabulary check checks names. The static checks catch unreachable nodes, outcomes with no route, loops with no cap and gates with no round. Every authoring route in #376 (builder, YAML, the conversational command) validates drafts through this checker, and a graph the walker (#416) takes must not name a node that does not exist.

## Decided (2026-11-22)

- **What the checker reads is decided on the checker's own evidence, and the vocabulary check follows that decision, never the reverse.** Whether the vocabulary check would have to move, and what moving it costs, is not a reason to pick either input. The plan states which input it chose and why, against the checker's own criteria (the lead *What the checker reads* below), and only then what that means for the vocabulary check.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

### What the checker is

- **A pure library call: a graph in, findings out.** It needs no walker, executor, state store or host, so every authoring route, the harness side (#418) and the CLI (#418) can call it the same way.
- **Its error shape already exists.** `Violation(path, reason)` with a dotted path, and `GraphError(stage, violations)`, raised only by the facade; the conventions say a new rejecting stage is a new `Stage` member, never a second error type (`.claude/context/graphscene.md`; `graphscene/src/graphscene/model/errors.py`). Open: whether a finding carries its check id, as the bash checker's `<check-id>: <detail>` lines do. `Violation` has no field for it today.
- **Where it runs is open.** Either `load_graph` runs it as a new stage after the build, so a graph it returns is safe to walk; or it is a separate public call; or both: id existence inside loading (a missing `to` would break a walk) and the graph checks as their own call.
- **What the checker reads: the typed `FlowGraph` or the parsed mapping.** The evidence to weigh, for the checker alone:
  - **How the checks read in each.** The ported checks walk one edge set: outcome `to` edges, an interrupt binding's `resume`, skip `to`s and a round's fan-out to its gates, plus lookups of a binding's primitive and an outcome's verdict (checks 2, 3, 9). The model already sorts edges into `RouteEdge` / `BindingEdge` and bindings into `InterruptBinding` / `StopBinding` / `EndBinding`; a mapping-reading checker sorts them again itself, as `vocabulary.py` does beside the builder today. Drafting one or two checks against both (for example `reaches-terminal` and `fail-cycle-capped`) shows the difference in code rather than in argument.
  - **Where it runs and who holds what there.** After the build, inside `load_graph`, the model is at hand; the walker (#416) holds a `FlowGraph`; a host building a graph in code may hold one too. Reading the mapping is only forced if the checker must run before the build, and the builder does not need it to: ids stay `str`.
  - **Violation paths.** The mapping gives JSON paths for free; from the model they are rebuilt in the JSON spelling (`roundCounts`, `onCap`, not `round_counts`, `on_cap`). A real cost of the model, to be weighed.
  - **Type checking.** Typed fields under strict `mypy`, against `object` values coerced back into dicts and lists (`vocabulary.py`'s `_mapping`, `_strings`).
- **What follows for the vocabulary check**, once the checker's input is chosen. #434 kept it on the mapping and left moving it to this branch.
  - **If the checker reads the model**, the vocabulary check moves onto it in this branch, so every engine check reads one input and loading becomes schema → build → vocabulary → static checks. The model holds everything it reads (verdicts, binding primitives and reasons, `resume` / `reason` / `onCap`, skip predicates, terminal bindings), and the builder already builds a graph with undeclared names. The work: `vocabulary_violations` taking a `FlowGraph` (only the tests call it), `graphscene/tests/engine/test_vocabulary.py`'s planted mappings going through the builder, and `build_flow_graph`'s docstring no longer promising a vocabulary-valid input. It removes the second edge-class decision in `vocabulary.py` and its defensive helpers.
  - **If the checker reads the mapping**, the vocabulary check stays as it is: same signature, same place in `__all__`, schema → vocabulary → build.
  - Either way, the document order of its violations holds: the model keeps the file's key order.
- It lands in the `engine` layer (#434), imports only `model` and the standard library, and is exported from the package root, with `graphscene/tests/test_public_surface.py` updated to match.

### Which checks

- **Id existence, which no bash check covers.** The builder leaves these as `str` ids for "a later static checker" (`graphscene/src/graphscene/adapters/builder.py` → *"Deliberately not covered"*): `to`, `resume`, `gates`, `writer`, `start`, `entries`, `roundCounts`, and the counter, path, report-slot, prompt and binding names.
- **The generic checks of `scripts/check-flow-graph.sh` → `THE CONTRACT`:** 1 `reachable-from-start`, 2 `reaches-terminal`, 3 `fail-cycle-capped`, 8 `gate-in-round`, 9 `round-fan-out`.
- **They need restating without harness names.** The bash checker is written against the harness's names; format 4 declares its own (`valid_generic.json` routes on `approved` / `rejected` / `done`). The engine routes on declared primitives, as #416 says, so for example:
  - check 2's `<escalate>` becomes a binding whose primitive is `stop`;
  - check 3's `FAIL` edge becomes an outcome declaring `verdict: fail`, and its `<ask>` resume exemption becomes the `interrupt` primitive's `resume`;
  - check 9's "writer's `returned` edge" needs a generic way to name the writer's edge into the round;
  - check 8 picks its gates by `findingsFolder`, one of the review-loop keys #417 may move: it can drop that key, or that part can wait for #417.
- **Checks 4 to 7 stay in bash:** `run-mode-id-known`, `ledger-id-known`, `findings-folder-in-core` and `cap-matches-core` read plugin documents, so they are harness checks. No harness-side package exists until #418, so they stay in `scripts/check-flow-graph.sh` for now.
- **Checks about what runs a node are the harness's too:** that a node's `agent` is a real plugin agent, or that the agent's return schema's `outcome` values equal the node's outcome keys (`cli/test/agent-return-schemas.test.mjs`). They depend on the executor (#420, #421), not on the graph.

### Tests

- **The bash fixtures cannot be loaded.** `schemas/flow-graph-check/` holds format-3 copies of the harness's graph; GraphScene loads only format 4, and no graphscene test reads outside `graphscene/` (#414). A format-4 fixture per ported check, under `graphscene/tests/fixtures/flow_graph/`, made from `valid_generic.json` with one change each like the bash ones, keeps the same rule: each fails with its own check and no other.
- **"Agreeing with the bash checker" means the same checks and meanings for now.** A test running both on the harness's graph needs the harness side (#418) and belongs to the cutover (#419). `scripts/check-flow-graph.sh` and its gate legs `3e` / `3f` stay as they are.
- A planted case per clause with its exact `Violation`, one clean case, and `valid_generic.json` passing (`.claude/context/graphscene.md` → the test rules).

## Depends on

#414, #434 (the checker lands in #434's `engine` layer)
