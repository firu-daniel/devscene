# Story: GraphScene executor interface and stub executor

## Context

This branch defines how GraphScene runs a node, and stops there. It ships an `asyncio`-based executor protocol with the result an executor returns, a helper an executor uses to check a structured return against a JSON Schema it names, and a scriptable stub executor for tests. The task prompt settles three things. Only the interface and the stub ship: the engine-driven run loop is #484, and the retry, join, breaker and park rules are #422. An executor runs a node as a coroutine. And the public surface and the stub's own tests are this branch's only callers. No engine module changes, so `Walker` still launches nothing (`graphscene/src/graphscene/engine/walker.py`). `devscene-flow-host` is not touched: the harness's `claude` executor is #421.

All four tasks are in the `graphscene` layer (`.claude/context/graphscene.md`), placed by that document's `## The internal layers` → *"New work goes by what it is"* rule:

- **Task 1 (`model`)** declares the protocol and the result types in `graphscene/src/graphscene/model/execution.py`. A `typing.Protocol` that an adapter implements and the engine drives is declared in `model`, as `StateStore` and `PredicateHost` are.
- **Task 2 (`adapters`)** adds `return_violations` in `graphscene/src/graphscene/adapters/return_schema.py`, the one place `jsonschema` may be imported. It reuses the shipped schema adapter's ECMA-262 pattern translator rather than writing a second one.
- **Task 3 (`adapters`)** adds `StubExecutor` in `graphscene/src/graphscene/adapters/stub_executor.py`.
- **Task 4** makes all of it public and documents it. It owns the two `__all__` lists, `graphscene/tests/test_public_surface.py` and `graphscene/README.md`, so no two tasks edit one file. Tasks 1–3 each say which of their accompanying entries Task 4 lands.

**The contract every task restates.** These names and spellings are fixed here and are not re-derived by any task:

- `Executor` is a `typing.Protocol` with one method, `async def run(self, dispatch: Dispatch) -> NodeResult`. Its argument is the walk's own `Dispatch` (`graphscene/src/graphscene/model/walk_actions.py`). Fanning a `DispatchSet` out into one `run` per gate is the engine's job (#484).
- `NodeResult = Completed | Failed`. `Completed(outcome: str, detail: str | None)` maps one-to-one onto `Walker.next(outcome, node, detail)`. `Failed(failure: FailureClass, reason: str)` uses `FailureClass = Literal["infra", "agent", "undelivered"]`.
- Each variant carries `kind` as a `ClassVar[Literal[...]]`: `"completed"` and `"failed"`.
- The three failure classes:
  - **`infra`**: the run did not finish for a reason outside the agent, such as a crash, an unresolved session or a stall the executor detected itself. Retryable.
  - **`agent`**: the agent finished and reported that it failed.
  - **`undelivered`**: the run finished but left no return the executor could read as a valid one. The return was absent, could not be parsed, or failed the schema the executor names.
- What the engine does with each class is #422's. The `infra` / `agent` split is the one `harness-runs/lessons.md` → *"An unattended driver retries a unit's infrastructure-class failure … alone and a bounded number of times before parking; only a failure the agent itself reported parks at once"* already relies on.

**Decisions this plan settles for the task prompt's open leads.** Each is written once, into Task 1's module docstring, and the other tasks cite it there:

- **The stall timeout belongs to the engine.** #484 sets a deadline around a node's coroutine and reports the timeout itself, as an HTTP client library does. An executor that detects a stall on its own may still return `Failed("infra", …)`. For this to work, an executor's `run` must be cancellable: on `asyncio.CancelledError` it releases what it holds and re-raises, and never turns cancellation into a result.
- **No helper for an adopter's synchronous executor.** The docstring shows wrapping blocking code with `asyncio.to_thread`, and states that a cancelled `to_thread` call does not stop its thread. Task 1's suite shows such a wrapper satisfies the protocol.
- **An executor chooses no sandbox, permission mode or tool set.** The host passes those in when it constructs the executor, so `run` carries none of them.
- **A run may be repeated for the same dispatch** (a retry, an interrupt's resume), so an executor's side effects must be repeatable. The stub supports this by keeping one script queue per node.
- **An anticipated failure is returned as a `Failed`, never raised.** An exception out of `run` is a defect and propagates.

**How the tests run async code.** The suites drive coroutines with `asyncio.run(…)` inside plain synchronous `-> None` test functions. This follows the precedent in `.claude/context/docs-retrieval.md` → *"Async code is driven with `asyncio.run(…)` inside synchronous test functions"*. No async test plugin is added, and no runtime dependency is added: `asyncio` is standard library, and `jsonschema` is already declared.

**Top risks:**

- **The three tasks drift apart on the contract.** The most likely failure is a mismatch in the protocol's names or the failure-class spellings. Task 1 owns them, and Tasks 2–4 restate the exact contract above rather than paraphrasing it.
- **A stub that swallows cancellation.** That would make #484's engine-owned deadline untestable. Task 3's suite cancels a stalled run through `asyncio.wait_for` and asserts both the timeout and the stub's cancellation record.
- **A public surface that does not match its modules.** Task 4 lands both `__all__` lists, `_EXPECTED` and `_DEFINED_IN` together, appended after `"LedgerPassage"`, so the existing `_EXPECTED[7:28]` slice keeps its meaning.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, only track progress: the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_graphscene_executor_interface/task_<K>_plan.md`. They are ordered by ship sequence: contract before consumer, then the public surface.

1. [x] **Task 1** — Declare the `Executor` protocol and its `Completed` / `Failed` results in `model` _(layer: graphscene)_ _(points: 15)_
2. [x] **Task 2** — Add `return_violations`, checking an executor's return against a JSON Schema it names _(layer: graphscene)_ _(points: 10)_
3. [x] **Task 3** — Add the scriptable `StubExecutor` with outcomes, delays, failures and stalls _(layer: graphscene)_ _(points: 20)_
4. [ ] **Task 4** — Export the executor surface from `graphscene` and document it in the README _(layer: graphscene)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"defines how GraphScene runs a node: an executor interface, plus a stub executor for tests."* The predicate is read as covering every durable corpus statement that lists GraphScene's protocols, its `model` or `adapters` modules, or its stance on executors and `asyncio`. The plan's one corpus target is `graphscene/README.md`. The module docstrings the tasks edit are code-level docs and fall outside the register.

**Derivation entry 1: corpus statements about executors, protocols and `asyncio` (command).** Re-run verbatim from the checkout root:

`git grep -nE 'Two exist|protocols the engine drives|[Ee]xecutor|asyncio' -- graphscene/README.md 'docs/*.md' ARCHITECTURE.md README.md devscene-flow-host/README.md '.claude/context/*.md'`

**Derivation entry 2: the README's own surface inventory (command).** Re-run verbatim from the checkout root:

`git grep -nE '^\| .(src/graphscene/)?(model|adapters)/?. \||^GraphScene is ' -- graphscene/README.md`

**Derivation entry 3: standing-artifact rows (procedure).**

- **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Artifact:** `harness-runs/lessons.md`, the one standing ledger under `harness-runs/` whose rules bind planning. No standing check matrix under `harness-runs/` covers `graphscene/`.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when it states how a failure is classified or retried, or when it was taught by a `graphscene` branch.

**Closure invariant:** every site each derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `graphscene/README.md` → `## What it is`, opening paragraph ("GraphScene is a generic flow-graph navigation library.") | — | entry 2, `^GraphScene is ` | `change` | Task 4: add the sentence naming the executor protocol, the stub and the return check |
| 2 | `graphscene/README.md` → `## What it is`, the `src/graphscene/model/` row | — | entry 2, model row | `change` | Task 4: add `execution.py` and its names |
| 3 | `graphscene/README.md` → `## What it is`, the `src/graphscene/adapters/` row | — | entry 2, adapters row | `change` | Task 4: add `return_schema.py` and `stub_executor.py` |
| 4 | `graphscene/README.md` → `## The layers`, the `adapters` table row ("Reading a JSON file, validating against the schema …") | — | entry 2, `adapters` layer row | `change` | Task 4: add the stub executor and return validation to what the layer holds |
| 5 | `graphscene/README.md` → `## The layers`, the `model` table row ("… and the protocols the engine drives.") | — | entry 1, `protocols the engine drives`; entry 2, `model` layer row | `no-change` | it already says "the protocols the engine drives" with no count, and that stays true with `Executor` added |
| 6 | `graphscene/README.md` → `## The layers`, the protocol bullet ("Two exist: `StateStore`, implemented by `FileStateStore`, and `PredicateHost`, implemented by the caller.") | — | entry 1, `Two exist` and `executor` | `change` | Task 4: three exist, the third being `Executor`, implemented by `StubExecutor` and by a host |
| 7 | `graphscene/README.md` → `## The layers`, the bullet *"New work goes by what it is. … A store, an executor or another format goes in `adapters`."* | — | entry 1, `executor` | `no-change` | already true of `stub_executor.py`, which Task 3 places in `adapters` |
| 8 | `.claude/context/graphscene.md` → `## The internal layers`, *"New work goes by what it is"* | — | entry 1, `executor` | `no-change` | conventions document, never a plannable target. Its statement still holds: the stub lands in `adapters` |
| 9 | `.claude/context/graphscene.md` → `## The internal layers`, *"A `typing.Protocol` that an adapter implements and the engine drives is declared in `model`"* | — | entry 1, `executor` | `no-change` | conventions document. It already names an executor among its examples, and Task 1 follows it |
| 10 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host` row ("… executor configuration and hooks …") | — | entry 1, `executor` | `no-change` | conventions document. `devscene-flow-host` is not touched, and its executor is #421's |
| 11 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet ("… executor configuration and hooks …") | — | entry 1, `executor` | `no-change` | conventions document, same reason as row 10 |
| 12 | `.claude/context/conventions.md` → `### Where a new responsibility goes`, the `devscene-flow-host/src/devscene_flow_host/` row ("… executor configuration or hooks …") | — | entry 1, `executor` | `no-change` | conventions document, same reason as row 10 |
| 13 | `.claude/context/docs-retrieval.md` → `## Testing — what "done" means here`, *"Async code is driven with `asyncio.run(…)` inside synchronous test functions"* | — | entry 1, `asyncio` | `no-change` | conventions document of another layer. Tasks 1 and 3 follow its precedent, and nothing contradicts it |
| 14 | `ARCHITECTURE.md` → the open-weights paragraph ("… rather than a different executor.") | — | entry 1, `executor` | `no-change` | it is about the harness's engine axis (which runtime runs a session), not GraphScene's node executor, and nothing here changes it |
| 15 | `devscene-flow-host/README.md` → `## What it is` ("… executor configuration and hooks …") | — | entry 1, `executor` | `no-change` | the host package is not touched. Its executor is #421's |
| 16 | `docs/development.md` → `## 6. The roadmap this tree defers to`, row 16 ("… no remote executor.") | — | entry 1, `executor` | `no-change` | it is about the run daemon's machine lane, not GraphScene |
| 17 | `docs/rag-extraction-research/01-current-mechanism.md` ("the Python side uses an `asyncio.Lock`") | — | entry 1, `asyncio` | `no-change` | a research record about docs retrieval, unrelated to GraphScene |
| 18 | `harness-runs/lessons.md` → `## Unattended control loops`, *"Every automatic retry in an unattended path is bounded by a count or a deadline."* | — | entry 3, retry rule | `no-change` | the ledger is append-only. Retries are #422's, and this branch ships no retry |
| 19 | `harness-runs/lessons.md` → `## Unattended control loops`, *"An unattended driver retries a unit's infrastructure-class failure … only a failure the agent itself reported parks at once."* | — | entry 3, failure-classification rule | `no-change` | the ledger is append-only. Task 1's `infra` / `agent` split is the classification this rule needs |
| 20 | `harness-runs/lessons.md` → `## Ports and parallel implementations`, *"A shim that makes one engine read a shared contract as another engine does lists the constructs it supports and refuses every other one …"* (taught by `feat_graphscene_graph_model`) | — | entry 3, taught by a `graphscene` branch | `no-change` | the ledger is append-only. Task 2 honours the rule by reusing `_ecma_patterns`, which refuses untranslatable constructs |
