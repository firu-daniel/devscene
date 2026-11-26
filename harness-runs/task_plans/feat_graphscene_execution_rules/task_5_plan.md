### Task 5 — Make the execution rules public and describe them in the README

**Goal:** Make the execution rules part of GraphScene's public surface, so that a host (`devscene-flow-host`, through `graphscene`'s public surface only) and #484's loop can reach them. Then bring `graphscene/README.md` and the two docstrings that defer this work up to date with what Tasks 1–4 built.

**Depends on:** Tasks 1–4, which define the names below in these modules:

- `graphscene.model.run_control` (Task 1): `ExecutionLimits`, `HaltReason`, `Halt`, `NodeRecord`, `Recorded`, `Retry`, `Redispatch`, `Settlement`, `SetResult`, `Launch`, `RunSignals`, `DispatchCounter`, `LaunchSink`.
- `graphscene.engine.safety` (Task 2): `clear_set`.
- `graphscene.engine.breaker` (Task 2): `UndeliveredBreaker`.
- `graphscene.engine.attempts` (Task 3): `AttemptBook`.
- `graphscene.engine.set_execution` (Task 4): `execute_set`.

This task changes no behaviour in those modules. It owns the shared files those four tasks deliberately left alone. That makes this task the one that carries their required accompanying items (`.claude/context/graphscene.md` → `## What accompanies a new module`, *"with its row entry in `graphscene/README.md` → `## What it is`"*, and *"A name made public lands with …"*).

### Targets

- `graphscene/src/graphscene/facade/__init__.py`
- `graphscene/src/graphscene/__init__.py`
- `graphscene/tests/test_public_surface.py`
- `graphscene/README.md`
- `graphscene/src/graphscene/model/execution.py` (docstring only)

**Work:**

- [ ] `graphscene/src/graphscene/facade/__init__.py`:
  - Import each name above from its defining module, beside the existing `from graphscene.engine.*` and `from graphscene.model.*` imports (`from graphscene.model.run_control import (...)`, `from graphscene.engine.safety import clear_set`, `from graphscene.engine.breaker import UndeliveredBreaker`, `from graphscene.engine.attempts import AttemptBook`, `from graphscene.engine.set_execution import execute_set`).
  - Append the names to its `__all__` after `"ScriptedStall"`, in exactly this order: `"ExecutionLimits"`, `"HaltReason"`, `"Halt"`, `"NodeRecord"`, `"Recorded"`, `"Retry"`, `"Redispatch"`, `"Settlement"`, `"SetResult"`, `"Launch"`, `"RunSignals"`, `"DispatchCounter"`, `"LaunchSink"`, `"clear_set"`, `"UndeliveredBreaker"`, `"AttemptBook"`, `"execute_set"`.
- [ ] `graphscene/src/graphscene/__init__.py` (the package root):
  - Add the same seventeen names to its existing `from graphscene.facade import (...)` block, the way it takes every existing public name. It imports **nothing** from `graphscene.model.*` or `graphscene.engine.*` directly: the root re-exports its whole surface from `graphscene.facade` (`.claude/context/graphscene.md` → `## The public surface`, *"re-exported from `graphscene.facade`"*; the root docstring says the same).
  - Append the names to its `__all__` after `"ScriptedStall"`, in the same order as the facade's. The two `__all__` lists stay identical (`.claude/context/graphscene.md` → `## The public surface`).
  - Extend the root module docstring's surface sentence with the execution rules, keeping its *"The surface is re-exported from `graphscene.facade`"* sentence true.
- [ ] `graphscene/tests/test_public_surface.py`: append the same seventeen names, in the same order, to `_EXPECTED`. Add each one's `_DEFINED_IN` entry against its defining module, and add the `import graphscene.model.run_control` and `import graphscene.engine.<module>` lines that those entries need.
- [ ] `graphscene/README.md`, in two sections.

  `## What it is`:
  - In the opening paragraph, replace *"the engine does not yet drive an executor"* with a sentence saying the engine now holds the execution rules: the per-set safety contract, the per-node retry and failure settlement, the undelivered breaker, and `execute_set` running one set through the caller's `Executor`. The limits and the three host protocols come from the caller, and the run loop that applies the rules is not yet built. Cite it as #484.
  - Add `run_control.py` to the `src/graphscene/model/` row, and add `safety.py`, `breaker.py`, `attempts.py` and `set_execution.py` to the `src/graphscene/engine/` row, each with the names it defines. All of them are public, so none carries *"not public"*.

  `## The layers`:
  - Add *"the execution rules"* to the `engine` row's **Holds** cell.
  - Add *"the execution-rule types and limits"* to the `model` row's **Holds** cell.
  - Rewrite the bullet *"A `typing.Protocol` … Three exist"* so it names six protocols: `RunSignals`, `DispatchCounter` and `LaunchSink` are added, each implemented by the caller.

  These are scope-register rows 1, 2, 3, 5, 6 and 7. Rows 4 and 8 stay unchanged.
- [ ] `graphscene/src/graphscene/model/execution.py`, docstring only. Replace the *"Deliberately not covered:"* line *"What is done with each failure class (retry, park, breaker): #422."* with a pointer to `graphscene.engine.attempts`, `graphscene.engine.breaker` and `graphscene.engine.set_execution`. Leave *"The run loop and its deadline: #484."* in place, and add that the stall deadline's result is recorded as `infra` by `graphscene.engine.set_execution`.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` passes. This is the file this task edits.
- `from graphscene import execute_set, AttemptBook, ExecutionLimits` resolves, and each name is the object its defining module defines, which `_DEFINED_IN` asserts.
- `grep -nE '^from graphscene\.(model|engine|adapters)' graphscene/src/graphscene/__init__.py`, run from the checkout root, prints nothing: the root still takes its whole surface from `graphscene.facade`.
- Re-run the story index's `## Scope register` command entry from the checkout root. `graphscene/README.md` no longer reports `does not yet drive an executor`, and every remaining hit is a register row.
