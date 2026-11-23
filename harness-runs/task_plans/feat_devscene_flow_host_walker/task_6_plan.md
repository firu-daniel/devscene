### Task 6 — Compose the walker with `open_walker` and walk the harness's format-4 graph end to end

**Goal:** Compose the host's parts into GraphScene's `Walker` in one call, and prove the whole on the real graph. The suite loads `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` through `graphscene.load_graph_file`, which runs the schema, vocabulary and static checks (`.claude/context/graphscene.md` → `## Errors and the loading order`). It then walks the graph through `open_walker` on fixture configurations and ledgers planted under `tmp_path`. This is the branch's evidence that the harness side can load and walk its own graph: the task prompt's lead says the graph *"breaks none of [#415's rules]"* but was *"not yet run"*.

**Depends on:** Tasks 2, 4 and 5. It calls exactly these contracts:

- `devscene_flow_host.records.config.read_config(repo_root: Path) -> HarnessConfig`, whose `state_dir: str` is repo-relative (Task 2)
- `devscene_flow_host.host.predicates.HarnessPredicateHost(repo_root: Path, branch: str, *, skipped: str | None = None)`, with `answer(predicate, node) -> bool | None` and `refusal_reason(predicate) -> str | None` (Task 4)
- `devscene_flow_host.host.store.walk_store(repo_root: Path, state_dir: str, branch: str, *, lock_timeout: float = 120.0) -> FileStateStore`, at `<repo_root>/<state_dir>/.flow_walker_state/<quote(branch, safe="")>.json` (Task 5)

**Where this layer stops.** `open_walker` takes a graph that is already loaded. Where the graph file lives for a caller, the command line and rendering a `Step` belong to the `commands` layer, which has no module on this branch. Resuming a round from its files is not here either.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/walking.py` (new)
- `devscene-flow-host/tests/test_walking.py` (new)

**Work:**

- [ ] **`host/walking.py`**: `open_walker(repo_root: Path, branch: str, graph: FlowGraph, *, skipped: str | None = None) -> Walker`. It calls `read_config(repo_root)` once for `state_dir`, then returns `Walker(graph, walk_store(repo_root, config.state_dir, branch), HarnessPredicateHost(repo_root, branch, skipped=skipped))`. It imports `FlowGraph` and `Walker` with `from graphscene import …`. The docstring's *"The rule:"* says the walker it returns reads the branch's own store and asks a host that re-reads the records on every arrival. A `RecordError` from reading the configuration propagates.
- [ ] **`tests/test_walking.py` — header and fixtures.** The docstring opens *"The rule this file exists to enforce"*: the harness's own format-4 graph loads through every library check and walks through `open_walker` on planted records. It also states that every expected value is hand-written from reading the graph file, never taken from the walker's output, and lists as *"Deliberately not covered"* the refusal texts and the codec, which are GraphScene's suites. `_GRAPH` is `Path(__file__).resolve().parents[2] / "cli" / "templates" / "scripts" / "flows" / "task_plan_writing.v4.graph.json"`, the way `tests/test_graphscene_dependency.py` builds `_CHECKOUT`. A helper plants `devscene.config.json` with `"stateDir": "state"` and the case's `phases`, and optionally a ledger at `state/flow_progress/<branch>_progress.md`, under `tmp_path`. One case asserts that `load_graph_file(_GRAPH)` returns a graph whose `flow` is `"task_plan_writing"`.
- [ ] **Walk 1 — phases off, no run mode.** `phases` `{"parity": false, "qa": false}`, no ledger, `skipped="none"`, branch `feat_x`. Read each step off the graph file:
  - `start()` → a `Dispatch` at `plan_writer`, agent `task-plan-writer`, prompt `initial`
  - `next("returned")` → a `DispatchSet` for round `plan_round`, number `0`, whose dispatches are `architecture_review` then `plan_review`, and whose `passed` carries `SkipPassage("business_parity_review", "skipped")`
  - `next("PASS", node="architecture_review")` → a `Wait`
  - `next("PASS", node="plan_review")` → an `End` at `convergence`, binding `<terminal_handoff>`. Its `passed` carries the round's PASS, `LedgerPassage("P1")` and `SkipPassage("ui_writer", "skipped")`. Its `reports` hold `business_parity_review` `skipped`, `architecture_review` `passed`, `plan_review` `passed` and `ui_test` `qa-phase-off`

  Assert each step's fields that are named here. Read the order of `passed` and of `reports` off the graph and the engine's rules before writing the literal.
- [ ] **Walk 2 — the run mode from the ledger, phases on.** `phases` `{"parity": true, "qa": true}`, a ledger whose `## Run mode` block reads `- skipped: parity, qa`, and `skipped="none"` given (the ledger wins). The round's `DispatchSet` carries `SkipPassage("business_parity_review", "passed-by-exclusion")`. After both gates `PASS`, the `End` carries `SkipPassage("ui_writer", "passed-by-exclusion")`, `business_parity_review` `passed-by-exclusion` and `ui_test` `run-mode-skipped`.
- [ ] **Unanswerable, and two branches.**
  - With `phases.parity` `true` and a ledger whose `## Run mode` block has no `- skipped:` line, `start()` dispatches `plan_writer`, and `next("returned")` is exactly `Refused("the host cannot answer predicate 'run_mode_skips_parity' for node 'business_parity_review'")`. A fresh `open_walker(...).current()` still returns the `plan_writer` `Dispatch`, so the refusal wrote nothing. `HarnessPredicateHost(tmp_path, "feat_x").refusal_reason("run_mode_skips_parity")` is that ledger's exact reason.
  - Start a walk on `feat/a`. `open_walker(tmp_path, "feat/b", graph, skipped="none").current()` is `Refused("no walk has started")`, `feat/a`'s `current()` is its `plan_writer` `Dispatch`, and the only state file is `state/.flow_walker_state/feat%2Fa.json`.

**Verification:**

- Run this task's own test file from the repository root, as one foreground command: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_walking.py`. Every case passes.
- `commands.typecheck` exits zero.
- `git status --porcelain --ignored` shows nothing new outside `tmp_path`: no state directory in the checkout, and the graph file unchanged.
- If `load_graph_file(_GRAPH)` raises `GraphError`, stop and report the violations it names. The graph is the `cli` layer's file and is not edited here.

**Deviations from plan:**

- Plan specified `start()` → a `Dispatch` with prompt `initial`; the engine sets `Dispatch.prompt` only from an arriving edge's `prompt` (`graphscene/src/graphscene/engine/transitions.py` → `draft.prompts[edge.to] = edge.prompt`, read back by `prompt=draft.prompts.get(node.id)`), and `start` arrives by no edge, so the first `plan_writer` dispatch carries `prompt=None` (observed: `Dispatch(node='plan_writer', agent='task-plan-writer', prompt=None, …)`). Implemented as `None` in `tests/test_walking.py` → `_assert_plan_writer`, the reason in its docstring. Every other hand-written expectation held as planned.
- The `git status --porcelain --ignored` check shows `harness-runs/.flow_walker_state` and `harness-runs/.dispatch_counter`: flat files the run's own bash walker wrote (18:30 / 18:39), not this suite's output, which writes only under `tmp_path`. The graph file is unchanged.
