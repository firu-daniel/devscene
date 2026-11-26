### Task 6 — Run the declared node, round and terminal hooks from `start_run` and `continue_run`

**Goal:** Make GraphScene's run mode run every hook a graph declares, at fixed points, through the host's `HookHost`. It refuses up front a graph whose hooks the host cannot run. This replaces the run loop's *"Deliberately not covered: Hooks (#423)."*

**Depends on:**

- **Task 2**, which built the declarations: `DispatchNode.before` / `.after`, `RoundNode.before` / `.after` and `TerminalNode.before`, each `tuple[str, ...] | None`.
- **Task 4**, which declares the calls and the protocol: `BeforeDispatch(dispatch, seq, attempt)`, `AfterDispatch(record, step)`, `BeforeRound(dispatch_set)`, `AfterRound(passage, step)`, `BeforeEnd(end)`, and `HookHost` with `provides(hook) -> bool` and `async run(hook, call) -> None`.
- **Task 5**, which made `execute_set` take `before_dispatch: Callable[[BeforeDispatch], Awaitable[None]] | None`. It awaits that once per attempt, inside each dispatch's task.

### Targets

- `graphscene/src/graphscene/engine/run_loop.py`
- `graphscene/tests/engine/test_run_loop.py`

**The contract this task produces.** Task 7 documents and exports it. `devscene-flow-host` Task 13 relies on it.

- **The new keyword.** `start_run(…, hooks: HookHost | None = None, …)` and `continue_run(…, hooks: HookHost | None = None, …)` each gain a keyword-only `hooks`.
- **The refusal.** After constructing `AttemptBook` and the breaker, and before any walker call, each call walks `walker.graph.nodes` in key order, and within a node its `before` names, then its `after` names. It raises `ValueError` with the store unread and unwritten:
  - with `hooks` `None`, for the first name: `the graph names hook '<name>' and no hook host was given`;
  - when `hooks.provides(name)` is false, for the first such name: `the graph names hook '<name>', which the hook host does not provide`.

  A graph naming no hook runs exactly as today, whatever `hooks` is.
- **A taken step.** The loop *takes* each of these steps:
  - the first step of the call (from `start`, from `next(outcome)` or from `current`);
  - the `current` step it takes in place of a `Wait`;
  - the last record's step, when that step becomes the next step: no record was refused and the `SetResult` has no halt.

  A `Wait` and a `Refused` are never taken.
- **What happens when a step is taken**, in this order and before the loop acts on it:
  1. For each `RoundPassage` in the step's `passed`, in order, the after-hooks of that passage's round node run in declared order, each with `AfterRound(passage, step)`.
  2. If the step is a `DispatchSet`, the before-hooks of its round node (`dispatch_set.round`) run, each with `BeforeRound(dispatch_set)`.
  3. If the step is an `End`, the before-hooks of its terminal node (`end.node`) run, each with `BeforeEnd(end)`.

  After that the loop acts as today: dispatch, or return `End`, `Stop` or `Interrupt`.
- **Before each attempt.** `execute_set` is given `before_dispatch`, which runs the dispatched node's `before` names in declared order with the `BeforeDispatch` it receives. When no node of the graph declares `before`, it is given `None`.
- **After each record.** After each record of a `SetResult` is recorded through `Walker.next`, if the step returned is not `Refused`, the recorded node's after-hooks run in declared order, each with `AfterDispatch(record, step)`. They run before the next record is recorded. A refused record runs none, and the remaining records are still recorded, as today.
- **The run order.** Hooks are awaited on the loop's thread, one at a time, in the order above. Walker calls stay in `asyncio.to_thread`.
- **A hook that raises.** Its exception propagates unchanged out of `start_run` / `continue_run`. Whatever the walker had saved stays saved:
  - a later `continue_run` takes `current` again, and so re-runs that step's round after-hooks and before-hooks;
  - a dispatch's after-hooks for a record already saved are not re-run.

**Work:**

- [ ] **`run_loop.py` — the parameter and the refusal.** Add `hooks` to both entry points and to `_drive`, and the up-front refusal with the two messages above, verbatim.
- [ ] **`run_loop.py` — the firing points.** Add a `_take(step)` helper covering the three hook kinds of a taken step. Call it at the three take points. Add the per-record after-hooks in the recording loop, and build `before_dispatch` from the graph and the host for `execute_set`.
- [ ] **`run_loop.py` — the docstring.** Extend *"The rule:"* with the refusal, the take points, the firing order and the exception rule as spelled above. Replace *"Hooks (#423)."* under *"Deliberately not covered"* with three items: what a hook does (the host's), hooks in step mode (`Walker` runs none), and re-running a dispatch after-hook lost to a crash after its record was saved (a host that must not lose one makes it re-derivable from what `current` returns, as the harness's round and ledger hooks are).
- [ ] **`test_run_loop.py` — the refusal and the walk.** Plant a variant of the file's `_graph` that declares `vocabulary.hooks` and uses `before` / `after` on a dispatch node and on the round node, and `before` on the terminal node. Add a recording `HookHost` that keeps `(hook, call.kind, node-or-round)` tuples. Then add these cases:
  - **a whole walk:** the exact call sequence, hand-written from the planted graph. It covers the before-dispatch calls with their attempts, the after-dispatch calls with their records, before-round, after-round and before-end;
  - **an infrastructure retry** gives a second `before_dispatch` call with attempt 2;
  - **both refusals**, each with its exact message, and with a `MemoryStore` that was never read;
  - **a graph with no hooks** runs with `hooks=None`.
- [ ] **`test_run_loop.py` — failure and resume.** Add these cases:
  - **a hook that raises after a round closes** propagates its exception. A following `continue_run(…, hooks=…)` re-runs that round's after-hooks for the step `current` returns, and finishes;
  - **a resumed round** entered through `start_run(…, resume=RoundResume(...))` with one gate already recorded runs the round's before-hooks once, with a `DispatchSet` holding only the due gate;
  - **a `Stop` reached by a cap** first runs the closed round's after-hooks.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_run_loop.py` passes, every existing case included without edit.
- The run loop still imports only `graphscene.engine` and `graphscene.model` modules. The layer contracts in `graphscene/pyproject.toml` would refuse anything else.
