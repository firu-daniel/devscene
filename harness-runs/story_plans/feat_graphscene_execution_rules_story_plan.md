# Story: GraphScene execution rules — the planning driver's rules as engine components

## Context

This branch moves the planning driver's execution rules out of the bash pilot (`cli/templates/scripts/lib/planning-driver-lib.sh`, described in `docs/flow-graph-walker.md` → `## 5. The two drivers` → `### How each runs a parallel round`) into GraphScene's `engine`, so every graph and every host gets them. The rules are: a safety contract per dispatch set (STOP, PAUSE, and a dispatch cap over the whole set), recording in finish order, a join in which a node's final failure waits for its siblings, a bounded per-node retry for `infra` failures while an `agent` failure is recorded at once, an `undelivered` re-dispatch that uses up no attempt plus a separate run-level breaker over consecutive undelivered sets, and one observation row per launched session. The branch ships the rules and their tests. Nothing runs them yet: #484's engine-driven run loop applies them, and until then the public surface and its tests are their only callers. The work is all in the `graphscene` layer and is tested against #420's `StubExecutor`, never a real executor. `devscene-flow-host/` gets no change here. It will later supply the harness's STOP and PAUSE markers, its `.dispatch_counter` and its observation file through the protocols below. The escalation-resume cases (a)–(d) of `cli/test/planning-driver-control.test.mjs` commit files and read the ledger, so they belong to the host or to #423 and are out of scope.

**Decisions this plan takes** (the task prompt leaves these to planning):

- **Failure classes** are #487's, as `graphscene/src/graphscene/model/execution.py` defines them: `infra` is retried for that node alone, `agent` is recorded at once, and `undelivered` is re-dispatched without counting as an attempt.
- **A stall is `infra`.** When `ExecutionLimits.stall_seconds` is set, a node's run that has not returned in time is cancelled and settled as `Failed("infra", "stalled: no result within <stall_seconds>s")`, so it is retried for that node like any other infrastructure failure. This settles the question #484 left to this branch.
- **The limits are the host's, with GraphScene defaults.** `ExecutionLimits(max_attempts=3, backoff_seconds=60.0, dispatch_cap=None, stall_seconds=None)`. The run-level breaker's limit is **not** an `ExecutionLimits` field: it is supplied once, at `UndeliveredBreaker(limit=3)` construction, and the breaker the host builds is the only place it lives, so `execute_set` can never run with a breaker limit other than the one the host passed. The defaults equal the pilot's values (`PD_MAX_ATTEMPTS` 3, `PD_BACKOFF_SECS` default 60, three undelivered sets), but no harness value is hard-coded: the cap defaults to none, and the harness passes its `MAX_TOTAL_DISPATCHES`.
- **A node's park is the graph's own binding.** A final failure (an `agent` failure, or an `infra` failure on its last attempt) becomes a `NodeRecord` carrying the host-named `failure_outcome`, for example the harness graph's `error`. The caller records it through `Walker.next`, and the walk's existing join and the graph's binding for that held outcome produce the park. The engine adds no second park mechanism. **Run-level halts** — STOP, PAUSE, the cap and the tripped breaker — come back as a returned `Halt` and are never raised. The caller then continues the saved walk on a later call, so the halt behaves as an interrupt.
- **Recording order.** A `SetResult.records` lists every `Completed` record in finish order, then every final-failure record in finish order. A sibling is never cancelled because another node failed.
- **Usage stays with the host.** The engine counts launches: each launch takes `DispatchCounter.increment()` as its `seq`, and exactly one `Launch(seq, node, agent, attempt, max_attempts, result)` is written to the host's `LaunchSink` per launched session, retries included. Usage figures are joined by the host from the usage sink its executor writes to. `NodeResult` carries no usage.

**Module ownership.** These modules are new. Each task owns its module and that module's suite, and no two tasks edit one file:

- `graphscene/src/graphscene/model/run_control.py` (Task 1): the plain types and protocols — `HaltReason`, `ExecutionLimits`, `RunSignals`, `DispatchCounter`, `Launch`, `LaunchSink`, `Halt`, `NodeRecord`, `Recorded`, `Retry`, `Redispatch`, `Settlement`, `SetResult`.
- `graphscene/src/graphscene/engine/safety.py` → `clear_set` and `graphscene/src/graphscene/engine/breaker.py` → `UndeliveredBreaker` (Task 2).
- `graphscene/src/graphscene/engine/attempts.py` → `AttemptBook` (Task 3).
- `graphscene/src/graphscene/engine/set_execution.py` → `execute_set`, the composition (Task 4).

Every new module's required accompanying items that sit in shared files — its `graphscene/README.md` → `## What it is` row, the `## The layers` cells, the import and `__all__` entries in both `__init__.py` files and the `_EXPECTED` / `_DEFINED_IN` entries in `graphscene/tests/test_public_surface.py` — are **Task 5's**, because those files are shared. Task 6 is the caller-side scenario suite, and it can only be written once the names are public.

**Top risks:** The likeliest defect is a retry that is not bounded or not isolated: an `infra` retry that re-runs the siblings, uses up an attempt on an `undelivered` re-dispatch, or skips the safety contract. Task 3 owns the per-node arithmetic, and Task 4 requires every retry pass to go through `clear_set` and count against the cap. The second risk is a sibling cancelled because another node failed, or a failure recorded ahead of the outcomes that finished after it. Task 4 asserts `StubExecutor.cancelled` stays empty and that held failures come after the last outcome. The third is rules that pass their unit tests but cannot be reached or composed by a caller. Task 6 drives them only through `graphscene`'s public surface, through to a real `Walker` join on `valid_generic.json`.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`**: in every flow that runs the unit loop that is the commit step, `commit-on-branch.sh --unit`, and in the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational progress markers only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_graphscene_execution_rules/task_<K>_plan.md`, in ship order: model before engine, the composition after its parts, the public surface and README after every module, and the caller-side suite last.

1. [ ] **Task 1** — Add the execution-rule types and host protocols in `model/run_control.py` _(layer: graphscene)_ _(points: 15)_
2. [ ] **Task 2** — Add the per-set safety contract `clear_set` and the run-level `UndeliveredBreaker` _(layer: graphscene)_ _(points: 15)_
3. [ ] **Task 3** — Add the per-node attempt rule `AttemptBook` in `engine/attempts.py` _(layer: graphscene)_ _(points: 15)_
4. [ ] **Task 4** — Add `execute_set`, running one dispatch set under the execution rules _(layer: graphscene)_ _(points: 20)_
5. [ ] **Task 5** — Make the execution rules public and describe them in the README _(layer: graphscene)_ _(points: 15)_
6. [ ] **Task 6** — Reproduce the pilot's engine-owned control cases through the public surface _(layer: graphscene)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_graphscene_execution_rules_task_prompt.md`, line 1): *"moves the planning driver's execution rules into the GraphScene engine so every graph gets them."*

**Derivation entry — corpus text stating where running a node or handling its failure lives (command).** Run bare from the checkout root:

```
git grep -n -o -i -e "does not yet drive an executor" -e "retry, park, breaker" -e "running a node" -e "an executor or another format" -e "is run, the" -- graphscene/README.md .claude/context docs devscene-flow-host/README.md README.md ARCHITECTURE.md
```

**Derivation entry — the README's layer inventories (procedure).** **Artifact:** `graphscene/README.md`. **Traversal:** the `## What it is` opening paragraph, then each row of its path table in order, then each row of the `## The layers` table in order, then each bullet under that table in order. **Decision rule:** a paragraph, row or bullet is reached when it names the modules, the protocols or the list of what the `model` or `engine` layer holds.

**Closure invariant:** every site either entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `graphscene/README.md` → `## What it is`, opening paragraph ("the engine does not yet drive an executor") | — | command entry, `does not yet drive an executor`; procedure entry | `change` | Task 5 |
| 2 | `graphscene/README.md` → `## What it is` table, the `src/graphscene/model/` row | — | procedure entry, lists `model`'s modules | `change` | Task 5 — gains `run_control.py` |
| 3 | `graphscene/README.md` → `## What it is` table, the `src/graphscene/engine/` row | — | procedure entry, lists `engine`'s modules | `change` | Task 5 — gains `safety.py`, `breaker.py`, `attempts.py`, `set_execution.py` |
| 4 | `graphscene/README.md` → `## The layers` table, the `adapters` row ("running a node from a script for tests") | — | command entry, `running a node` | `no-change` | describes `StubExecutor`, which this branch does not change |
| 5 | `graphscene/README.md` → `## The layers` table, the `engine` row | — | procedure entry, lists what `engine` holds | `change` | Task 5 — adds the execution rules |
| 6 | `graphscene/README.md` → `## The layers` table, the `model` row | — | procedure entry, lists what `model` holds | `change` | Task 5 — adds the execution-rule types and the host protocols |
| 7 | `graphscene/README.md` → `## The layers`, the bullet *"A `typing.Protocol` that an adapter implements … Three exist"* | — | procedure entry, names the protocols | `change` | Task 5 — names `RunSignals`, `DispatchCounter` and `LaunchSink`, implemented by the caller |
| 8 | `graphscene/README.md` → `## The layers`, the bullet *"New work goes by what it is."* ("A store, an executor or another format goes in `adapters`") | — | command entry, `an executor or another format`; procedure entry | `no-change` | still true: this branch adds no executor, and the rules are a walk-time rule over results and counts, which the bullet puts in `engine` |
| 9 | `.claude/context/graphscene.md` → `## What this layer owns, and what it is not`, *"The walker says what runs next and launches nothing: running a node, … are the host's"* | — | command entry, `running a node` | `no-change` | a conventions document, never a plannable target. `execute_set` now runs a dispatch set through the caller's `Executor`, which falsifies *"running a node … are the host's"*. Recorded as a `stale-rule` entry in `corpus_staleness` |
| 10 | `.claude/context/graphscene.md` → `## The internal layers`, *"A store, an executor or another format goes in `adapters`"* | — | command entry, `an executor or another format` | `no-change` | a conventions document, and still true, as row 8 |
