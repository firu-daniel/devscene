# Story: GraphScene run mode — the engine drives a walk end to end through an executor

## Context

This branch adds GraphScene's second way for a host to use it. In **step mode**, which stays as it is, the host calls `Walker.start` / `Walker.next` / `Walker.current` synchronously and runs each action itself. The `graphscene` command line (#452) is unchanged. In **run mode**, the host hands the engine an `Executor` and the engine runs the loop. It starts or continues a walk, dispatches each action through `execute_set`, records each `SetResult.records` entry through the walker in order, and stops at a terminal (`End`), a park (`Stop`), a graph interrupt (`Interrupt`), a walk refusal (`Refused`) or a run-level `Halt`. A `Halt` is STOP, PAUSE, the dispatch cap or the undelivered breaker. All the work is in the `graphscene` layer. The decisions dated 2026-11-25 and 2026-11-26 in the task prompt are binding.

Settled here and stated once, so every task file agrees:

- **Concurrency is a sliding window owned by `execute_set`.** The limit is the new field `ExecutionLimits.max_concurrent_dispatches: int = 10`, which must be `>= 1`. 10 is GraphScene's default, and a host passes its own value through the `ExecutionLimits` it already hands over. With a limit of 5, a set of 8 starts its 6th dispatch as soon as any of the first 5 finishes. Each dispatch takes its `Launch.seq` and its attempt when it **starts**, in set order. `run_timeout_seconds` runs from the start of the run, so time spent waiting for a slot never counts against it. The whole pass is still cleared once by `clear_set` and counted against the cap once. All of it goes out, and a STOP raised mid-pass is honoured at the next pass. The graph format stays unlimited. Task 1 adds the field and Task 2 applies it.
- **The run loop is `graphscene.engine.run_loop`, and it has two public coroutines.** `start_run` begins through `Walker.start(entry, resume=…)`. `continue_run` begins through `Walker.current()`, or through `Walker.next(outcome)` when the host gives `outcome`. That is how a graph `Interrupt` is resumed with its `resume_outcome`. Both return `RunExit = End | Stop | Interrupt | Halt | Refused`, an alias Task 1 adds to `graphscene.model.run_control`. The loop is Task 3. Task 4 makes it public and documents it.
- **State lives for one loop call.** Each call constructs its own `AttemptBook()` and `UndeliveredBreaker(undelivered_limit)`, with `undelivered_limit: int = 3`. What must survive a pause, a stop or a crash is the host's to keep and pass back in: the walk through its `StateStore`, and the dispatch total through its `DispatchCounter`.
- **One execution path.** A lone `Dispatch` runs through `execute_set` as a set of one. Its record goes to `Walker.next(outcome, node)` **without** `detail`, because the walker records a detail only for a gate of an open round (`graphscene/src/graphscene/engine/walker.py` → `_step`, *"detail is recorded only for a gate of an open round"*). That detail is not lost: the host's `LaunchSink` already received it in the `Launch` row's `result`. A gate of a `DispatchSet` is recorded with `Walker.next(outcome, node, detail)`.
- **Blocking calls stay off the event loop.** Every `Walker` call the loop makes goes through `await asyncio.to_thread(…)`, because `FileStateStore` takes an `fcntl` lock and writes a file (`graphscene/src/graphscene/adapters/state_file.py`). No helper is added for a synchronous executor: #420 decided against one, and `graphscene/src/graphscene/model/execution.py` → *"A helper for a synchronous executor: none is offered"* stays. The host protocols `RunSignals`, `DispatchCounter` and `LaunchSink` are synchronous and called on the loop thread by `clear_set` / `execute_set`. Keeping them fast is the host's job.
- **The loop sets no deadline of its own.** The engine's only time limit is `ExecutionLimits.run_timeout_seconds`, applied inside `execute_set`. Detecting a stall is the executor's (#421).

No new runtime dependency, no schema change and no wire-form change. `ExecutionLimits` is never serialized.

**Top risks:**
- **Wrong recording order or a dropped record after a mid-set `Halt`.** Either leaves the saved walk unable to continue. Task 3 records every record before acting on the halt, and its suite resumes a half-recorded round with `continue_run`. Task 4 repeats that over a real `FileStateStore`.
- **A window that changes what the existing rules promise.** For example, the seq taken at clear time, a queued dispatch charged against the run timeout, or a queued dispatch dropped by a mid-pass STOP. Task 2 pins each of these with its own case and keeps every existing `test_set_execution.py` case passing unchanged.
- **The `Walker`'s blocking file I/O run on the event loop thread.** That would serialise every concurrent run behind a lock wait. Task 3 asserts that the store is called from a thread other than the loop's.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker:** the commit step, `commit-on-branch.sh --unit`, in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. An implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_graphscene_run_mode/task_<K>_plan.md`. They are ordered bottom-up by ship sequence: `model`, then `engine`, then `facade` within the one `graphscene` layer.

1. [x] **Task 1** — Add `ExecutionLimits.max_concurrent_dispatches` and the `RunExit` alias to the run-control model _(layer: graphscene)_ _(points: 10)_
2. [x] **Task 2** — Run each `execute_set` pass through a sliding window of `max_concurrent_dispatches` _(layer: graphscene)_ _(points: 20)_
3. [ ] **Task 3** — Add the run loop `start_run` / `continue_run` in `graphscene.engine.run_loop` _(layer: graphscene)_ _(points: 20)_
4. [ ] **Task 4** — Make run mode public, document it in the README and drive it end to end as a caller _(layer: graphscene)_ _(points: 20)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"`feat_graphscene_run_mode` completes GraphScene's execution flow: the engine drives a walk end to end with an executor, applying #422's rules."* The corpus sites in scope are those that state or describe GraphScene's run loop or its absence.

**Derivation entry — corpus files (command).** Re-run verbatim from the repository root: `git grep -l -E '#484|run loop|[Ss]tep mode|not yet built' -- '*.md' ':!harness-runs/**' ':!examples/**'`

**Derivation entry — sites inside `graphscene/README.md` (procedure).** **Artifact:** `graphscene/README.md`. **Traversal:** in file order, the `## What it is` prose paragraph, then that section's table rows `src/graphscene/model/` and `src/graphscene/engine/`, then the `## The layers` table rows and bullets. **Decision rule:** a sentence or row is reached when it lists the names or modules of `graphscene/src/graphscene/model/run_control.py` or `graphscene/src/graphscene/engine/`, or states what the `engine` layer holds.

**Closure invariant:** every site that either entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `graphscene/README.md` → `## What it is` prose ("The run loop that applies the rules is not yet built (#484).") | — | command entry, `#484` / `run loop` / `not yet built`; procedure entry | `change` | Task 4 |
| 2 | `graphscene/README.md` → `## What it is` table, `src/graphscene/model/` row (`run_control.py`'s name list) | — | procedure entry, lists `run_control.py`'s names | `change` | Task 4 (adds `RunExit`) |
| 3 | `graphscene/README.md` → `## What it is` table, `src/graphscene/engine/` row (`set_execution.py: execute_set, …`) | — | procedure entry, lists the engine modules | `change` | Task 4 (adds `run_loop.py`, and the window on `execute_set`) |
| 4 | `graphscene/README.md` → `## The layers` table, `engine` row ("… the review-loop pattern, and the execution rules.") | — | procedure entry, states what `engine` holds | `change` | Task 4 (adds "and the run loop") |
| 5 | `graphscene/README.md` → `## The layers` bullet "A `typing.Protocol` that an adapter implements … Six exist: …" | — | procedure entry, `## The layers` bullet | `no-change` | the branch adds no protocol; the six are unchanged |
| 6 | `cli/templates/state-dir/autonomous_inbox/README.md` ("The unattended run loop's drop point") | — | command entry, `run loop` | `no-change` | names the watcher's unattended run loop, not GraphScene's |
| 7 | `docs/paid-team-layer-research.md` ("The whole run loop, sandbox and guards") | — | command entry, `run loop` | `no-change` | names the harness's run loop, not GraphScene's |
| 8 | `plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md` ("a new contributor being handed the run loop") | — | command entry, `run loop` | `no-change` | names the harness's run loop, not GraphScene's |
