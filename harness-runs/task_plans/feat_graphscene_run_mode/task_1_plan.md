### Task 1 — Add `ExecutionLimits.max_concurrent_dispatches` and the `RunExit` alias to the run-control model

**Goal:** Give the `model` layer the two plain values the rest of the branch computes over. The first is the concurrency limit a host passes, `ExecutionLimits.max_concurrent_dispatches`. The second is the type the run loop returns, `RunExit`. The task also brings the two model docstrings that defer to "the run loop: #484" in line with the run loop this branch lands.

**Where this task stops.** This task declares the field and the alias and validates the field. It applies neither. **Task 2** makes `execute_set` honour `max_concurrent_dispatches`. **Task 3** writes `graphscene.engine.run_loop`, whose `start_run` and `continue_run` return `RunExit`. **Task 4** makes `RunExit` public. Until Task 2 lands, the field is declared and validated but read by nothing. That is the contract-before-consumer order (`.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent`).

### Targets

- `graphscene/src/graphscene/model/run_control.py`: the new field, its validation, the `RunExit` alias and the module docstring.
- `graphscene/src/graphscene/model/execution.py`: module docstring only.
- `graphscene/tests/model/test_run_control.py`: the suite's cases for the field and the alias.

**Work:**

- [ ] `run_control.py` → `ExecutionLimits`: append `max_concurrent_dispatches: int = 10` as the **last** field, after `run_timeout_seconds`, so every existing keyword call keeps its meaning. In `__post_init__`, refuse a value below 1 through the existing `_refuse` helper, which produces exactly `ExecutionLimits: max_concurrent_dispatches must be >= 1, got <value>`. In the module docstring's rule, add one bullet stating that `max_concurrent_dispatches` is how many runs of one set are in flight at once, applied by `graphscene.engine.set_execution`, and that the graph format sets no limit.
- [ ] `run_control.py` → `RunExit`: add `RunExit: TypeAlias = End | Stop | Interrupt | Halt | Refused`, in that order, below `SetResult`. Import `End`, `Interrupt`, `Refused` and `Stop` from `graphscene.model.walk_actions`, a model-internal import. In the opening summary line, name `RunExit` as "what a run of a walk ends on". Replace the docstring's `- The run loop: #484.` with `- Driving a walk with these: graphscene.engine.run_loop (start_run, continue_run).` That module lands in Task 3 of this branch.
- [ ] `execution.py`, module docstring only, with no code change. Rewrite the first rule bullet to say that `execute_set` fans out a `DispatchSet`, one `run` per gate, with at most `ExecutionLimits.max_concurrent_dispatches` runs concurrent on one event loop. Rewrite the second bullet to say that `Completed.detail` is passed to `Walker.next` only for a gate of a set, because the walk records no detail for a lone dispatch. Replace `- The run loop: #484.` with `- Driving a walk with an executor: graphscene.engine.run_loop.` Keep the *"A helper for a synchronous executor: none is offered"* bullet as it is.
- [ ] `test_run_control.py`. Extend `test_the_limits_default_to_graphscenes_own_values` with `max_concurrent_dispatches=10` in the equality and `"max_concurrent_dispatches"` as the last name in the field-order list. Add a parametrized refusal row `({"max_concurrent_dispatches": 0}, "ExecutionLimits: max_concurrent_dispatches must be >= 1, got 0")` with id `max_concurrent_dispatches`. Add `test_a_run_exit_is_one_of_the_five_ends`, asserting `typing.get_args(RunExit) == (End, Stop, Interrupt, Halt, Refused)`. Every expected literal is hand-written from this file, never taken from the code's output.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/model/test_run_control.py` passes, with the new refusal row and the alias case among its cases.
- Every existing `ExecutionLimits(...)` call in `graphscene/` passes keywords only. `git grep -n "ExecutionLimits(" -- graphscene` shows no positional call, so appending the field changes no existing call.
- `git grep -n "#484" -- graphscene/src/graphscene/model` prints nothing.
