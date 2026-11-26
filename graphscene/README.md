# graphscene

**Who reads this:** a contributor changing this package, and whoever later extracts it from this repository. It owns what GraphScene is, the boundary between it and the harness, and how its toolchain is run here.

## What it is

GraphScene is a generic flow-graph navigation library. Its `engine` layer holds the vocabulary check, the static checker and the walker, `Walker`, which walks a loaded graph and says what runs next without launching anything. A walk's state is kept through a `StateStore` the caller supplies, such as `FileStateStore`. It carries the generic flow-graph schema (format 4), those two checks, and loading: the facade composes the schema adapter, the builder, the vocabulary check and the static checker, in that order, before returning the parsed graph as typed objects. Its runtime dependencies are `jsonschema`, which the schema adapter validates with, and `referencing`, which keeps `return_violations` from retrieving a `$ref` outside the schema it is handed. A round node dispatches its gates as one set and joins them; a round that declares `writer` is a review loop — write, parallel gates, round, revision with the closed round's records, capped by its counter — and its rules are checked and walked only where a graph declares one. GraphScene declares how a node is run: an `asyncio` `Executor` protocol whose `run` takes a `Dispatch` and returns a `NodeResult`, either a `Completed` outcome or a `Failed` with an `infra`, `agent` or `undelivered` `FailureClass`. It ships a scriptable `StubExecutor` for tests and `return_violations` for checking an executor's return against a JSON Schema the executor names. The engine holds the execution rules: the per-set safety contract, the per-node retry and failure settlement, the undelivered breaker, and `execute_set`, which runs one dispatch set through the caller's `Executor`. The limits, `ExecutionLimits`, and the three host protocols, `RunSignals`, `DispatchCounter` and `LaunchSink`, come from the caller. `ExecutionLimits.run_timeout_seconds` bounds a node's total run time and is no inactivity timeout: detecting a stalled session is the executor's, which returns it as an `infra` `Failed`. The run loop that applies the rules is not yet built (#484).

| Path | Holds |
|---|---|
| `src/graphscene/` | The typed package, `graphscene`. |
| `src/graphscene/__init__.py` | The public surface, re-exported from `graphscene.facade`. |
| `src/graphscene/schemas/flow-graph.schema.json` | The format-4 flow-graph schema, shipped as package data. |
| `src/graphscene/model/` | `errors.py`: `Violation`, `Stage` and `GraphError`, the one error shape every loading stage rejects a graph with. `flow_graph.py`: `FlowGraph` and the typed objects it holds: `NodeKind`, `Primitive`, `Verdict`, `BindingDeclaration`, `Edge`, `Node`, `OutcomeDeclaration`, `InterruptBinding`, `StopBinding`, `EndBinding`, `PredicateDeclaration`, `Vocabulary`, `CounterDeclaration`, `OnCapEdge`, `RouteEdge`, `BindingEdge`, `SkipEntry`, `DispatchNode`, `RoundNode` and `TerminalNode`. `walk_actions.py`: the steps a walk returns and the passages it records: `Step`, `Action`, `Dispatch`, `DispatchSet`, `Wait`, `Interrupt`, `Stop`, `End`, `Refused`, `GateRecord`, `Passage`, `SkipPassage`, `RoundPassage` and `LedgerPassage`. `walk_state.py`: `WalkState`, `OpenRound`, `RoundResume` and `Awaiting`, where a walk stands and the round a host resumes it in, and the `StateStore` and `PredicateHost` protocols. `execution.py`: the `Executor` protocol, how a node is run, and what its `run` returns: `NodeResult`, either `Completed` or `Failed`, with `FailureClass` naming why a run failed. `run_control.py`: the types and host protocols the execution rules compute over: `ExecutionLimits`, `HaltReason`, `Halt`, `NodeRecord`, `Recorded`, `Retry`, `Redispatch`, `Settlement`, `SetResult` and `Launch`, and the `RunSignals`, `DispatchCounter` and `LaunchSink` protocols. |
| `src/graphscene/engine/` | `vocabulary.py`: `vocabulary_violations`, the used-against-declared names check JSON Schema cannot express, reading the built `FlowGraph` and returning `Violation` values. `references.py`: `reference_violations`, that every node, counter, path, report-slot and prompt name the graph uses exists and `start` is listed in `entries`; not public. `static_check.py`: `static_violations`, the reference check, then the five graph checks (`reachable-from-start`, `reaches-terminal`, `fail-cycle-capped`, `gate-in-round`, `round-fan-out`), each reason opening with its check id; `gate-in-round` and `round-fan-out` hold round rules, run on every round, and review-loop rules, run only on a review loop. `review_loop.py`: whether a round is a review loop, and its writer's round number and its gates' convergence; not public. `transitions.py`: every move from one node to the next, including skips, binding edges and opening and closing a round; not public. `rounds.py`: recording a gate's outcome while its round's set is out, and the join once every gate is in, and entering a round with gates already recorded; not public. `walker.py`: `Walker`, whose `start`, `next` and `current` read the walk from its `StateStore`, step it and write it back; `start` takes an optional `RoundResume`, starting the walk at that round's number with the given gate outcomes recorded and every counter at 0, the host deciding which round and which records. `safety.py`: `clear_set`, the per-set safety contract checked before anything of a dispatch set goes out — STOP, PAUSE, then the dispatch cap — returning a `Halt` or `None`. `breaker.py`: `UndeliveredBreaker`, the run-level breaker tripped by consecutive sets that had an `undelivered` result. `attempts.py`: `AttemptBook`, the per-node attempt rule turning a node's `NodeResult` into its `Settlement`. `set_execution.py`: `execute_set`, running one dispatch set through the caller's `Executor` under those rules and returning a `SetResult`. |
| `src/graphscene/adapters/` | `json_file.py`: `read_json_file`, reading a UTF-8 JSON file or raising a parse-stage `GraphError`. `schema.py`: `schema_violations`, validating against the shipped schema with `jsonschema` and the ECMA-262 pattern translator. `builder.py`: `build_flow_graph`, building the typed `FlowGraph` from a validated mapping. `walk_json.py`: `state_to_json` and `state_from_json`, a `WalkState`'s JSON form; `step_document`, a walk step's JSON form; `resume_from_json`, reading the round-resume document into a `RoundResume`; not public. `check_json.py`: `check_document`, a `GraphError`'s JSON form, the check document the command line prints; not public. `state_file.py`: `FileStateStore`, the `StateStore` keeping a walk's state in one JSON file. `return_schema.py`: `return_violations`, checking an executor's return against a JSON Schema it names. `stub_executor.py`: `StubExecutor`, the `Executor` that runs a node from a script for tests, and its script types `Scripted`, `ScriptedOutcome`, `ScriptedFailure` and `ScriptedStall`. |
| `src/graphscene/facade/` | `loading.py`: `load_graph` and `load_graph_file`, which validate a graph against the schema, build it, then run the vocabulary check and the static checker, and return a `FlowGraph` or raise `GraphError`. `cli.py`: `main`, the `graphscene` command line (`check`, `start`, `next`, `current`); not public. `__init__.py`: the composed surface the package root re-exports. |
| `tests/` | The `pytest` suite. Its tests mirror the layers, in `tests/model/`, `tests/engine/`, `tests/adapters/` and `tests/facade/`; package-wide tests (`test_boundary.py`, `test_layers.py`, `test_public_surface.py`, `test_flow_graph_schema.py`) stay at `tests/`. A new module lands with its own suite, `tests/<layer>/test_<module>.py`. |

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `facade` | `src/graphscene/facade/` | Loading a graph, which composes the adapters and the engine, the composed surface the package root re-exports, and the `graphscene` command line, the one module that writes output. | `adapters`, `engine`, `model` and the standard library. |
| `engine` | `src/graphscene/engine/` | Checks and walks over the built model: the vocabulary check, the static checker, the walk with its rounds, the review-loop pattern, and the execution rules. | `model` and the standard library. |
| `adapters` | `src/graphscene/adapters/` | Reading a JSON file, validating against the schema with `jsonschema` and the ECMA-262 pattern translator, building the typed model, keeping a walk's state in a file, running a node from a script for tests, checking an executor's return against a JSON Schema. | `model`, `jsonschema`, `referencing` and the standard library. |
| `model` | `src/graphscene/model/` | The typed `FlowGraph` and its objects, `Violation`, `Stage` and `GraphError`, the walk state and its actions, the execution-rule types and limits, and the protocols the engine drives. | The standard library only. |

- **Imports point down only, and `engine` and `adapters` never import each other.** Only `facade` combines them.
- **Callers import from `graphscene` only and never name `graphscene.facade`.** No module inside the package imports from the package root; each imports the defining module of what it needs.
- **A `typing.Protocol` that an adapter implements and the engine drives is declared in `model`** — a state store, an executor, a host-answered predicate — so the adapter implements it without importing the engine. Six exist: `StateStore`, implemented by `FileStateStore`; `PredicateHost`, implemented by the caller; `Executor`, implemented by `StubExecutor` and by a host; and `RunSignals`, `DispatchCounter` and `LaunchSink`, each implemented by the caller.
- **New work goes by what it is.** A check or a walk over the model, and its rounds, goes in `engine`. A store, an executor or another format goes in `adapters`. A thin command-line entry point goes in `facade`. Walk state and checker findings, as plain types, go in `model`.
- **Every engine check reads the built `FlowGraph`, and loading runs schema → build → vocabulary → static.** A graph `load_graph` returns has passed all three checks, and a graph failing one stage never reaches the next.
- **The library never logs or prints.** It reports through return values and exceptions only. It has no user interface and keeps no state of its own: a walk's state is written only where the caller's `StateStore` puts it, and `FileStateStore` writes only the file it is given and its `<name>.lock` sibling. A command-line entry point in `facade` is the one place that may write output.
- **A walk refusal is a returned `Refused`, never an exception.** Loading raises `GraphError`; `FileStateStore` raises `ValueError` naming the file for a malformed state and `TimeoutError` naming the lock file when the lock is not acquired in time.

The direction and the confinement of `jsonschema` and `referencing` to `adapters` are `import-linter` contracts in `pyproject.toml` → `[tool.importlinter]`, ids `graphscene-layers` and `graphscene-jsonschema-in-adapters-only`, run by `tests/test_layers.py` with no cache. Run it alone:

```
bash scripts/python-service.sh --package graphscene test tests/test_layers.py
```

## The boundary

- **The harness side lives outside this directory, and the dependency points one way.** Harness-specific code — reading the harness's configuration, executing its agents, its planning hooks — goes in its own distribution outside `graphscene/`, named with a `devscene` prefix, and that distribution depends on `graphscene`. `graphscene` never depends on it, so extracting the library means moving this one directory.
- **The library imports only the standard library, itself and its declared runtime dependencies.** It names no `devscene`-prefixed module, never reads the harness's configuration file, and declares no `devscene`-prefixed dependency.
- **A new runtime dependency is a decision raised to the maintainer, never one an implementing run makes.** Adding a development tool to the `dev` dependency group is not restricted this way.

`tests/test_boundary.py` enforces the boundary and `tests/test_layers.py` the layer direction, so both rules travel with the library when it is extracted.

## The command line

`graphscene` is for a host not written in Python, or a shell script: it loads a graph and walks it one step at a time over a state file the caller names. It reads no configuration.

| Command | Arguments |
|---|---|
| `check` | `<graph>` |
| `start` | `<graph> <state> [--entry <node>] [--resume <file>] [--answer <predicate>=true\|false …]` |
| `next` | `<graph> <state> --outcome <outcome> [--node <node>] [--detail <text>] [--answer <predicate>=true\|false …]` |
| `current` | `<graph> <state>` |

`--resume` names a round-resume document, `{"round", "number", "records"}`, each record the walk-state document's `{"gate", "outcome", "detail"}`.

Every command loads the graph first and prints one JSON document on stdout as one ASCII-only line. Both documents are encoded in `adapters`, never by the command module:

- **The check document** (`adapters/check_json.py`), printed by `check` and by any command whose graph is rejected: `{"stage", "violations": [{"path", "check", "reason"}]}`. A graph that loaded is `{"stage": null, "violations": []}`. `path` is the dotted path, `""` for the root. `check` is set only for stage `static`, from the check id the reason opens with, and `reason` is then the text after it; otherwise `check` is `null` and `reason` is verbatim.
- **The step document** (`adapters/walk_json.py`), printed by `start`, `next` and `current`: the action as the walk-state document encodes `pending`, or `{"kind": "refused", "reason"}`.

**Predicate answers come only through repeated `--answer <predicate>=true|false`**, one per predicate. A predicate left unanswered is refused by the walk, never guessed.

| Exit | Meaning |
|---|---|
| `0` | The graph loaded (`check`), or the walk returned an action. |
| `1` | The graph was rejected; stdout holds the check document. |
| `2` | Usage; the usage text is on stderr. |
| `3` | The walk refused; stdout holds the step document with `"kind": "refused"`. |
| `4` | An input could not be read or used — an unreadable file, a malformed state or resume file, a state lock not acquired: one `graphscene: <message>` line on stderr and nothing on stdout. |

`--help`, on `graphscene` or on any command, is the one exception to the one-JSON-document rule: it prints the help text on stdout and exits `0`.

Install the console script into the package environment first, outside any sandbox (this provisions every package's environment):

```
bash scripts/python-service.sh provision
```

Then run the command from the repository root:

```
uv run --frozen --no-sync --project graphscene graphscene check graphscene/tests/fixtures/flow_graph/valid_generic.json
```

A walk over the same graph, its state in `walk.json`. `start` prints the `draft` dispatch:

```
uv run --frozen --no-sync --project graphscene graphscene start graphscene/tests/fixtures/flow_graph/valid_generic.json walk.json
```

Recording `draft`'s outcome enters `review_round`, whose gate `edit_check` asks the predicate `stage_disabled`; without its answer the walk refuses, exit `3`. With it, `next` prints the round's dispatch set:

```
uv run --frozen --no-sync --project graphscene graphscene next graphscene/tests/fixtures/flow_graph/valid_generic.json walk.json --outcome done --answer stage_disabled=false
```

`bash scripts/python-service.sh run` is not a route to the command: its `graphscene` row names no console script, and its exit mapping would collapse `1`–`4` into `1`.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package graphscene lint
```

Typecheck:

```
bash scripts/python-service.sh --package graphscene typecheck
```

Test:

```
bash scripts/python-service.sh --package graphscene test
```

`test` forwards paths to `pytest`, relative to `graphscene/`:

```
bash scripts/python-service.sh --package graphscene test tests/test_boundary.py
```

`typecheck` takes no argument (one is refused, exit 2): it runs `mypy` over the whole package, `src` and `tests`.

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13e–13g ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
