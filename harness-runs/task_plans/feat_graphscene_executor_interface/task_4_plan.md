### Task 4 — Export the executor surface from `graphscene` and document it in the README

**Goal:** Make the executor contract, the return check and the stub reachable the way every caller reaches GraphScene, `from graphscene import …`. Record them in `graphscene/README.md` as well. Per the task prompt's decisions, the public surface and the stub's tests are this branch's callers, so this task is what wires the earlier three.

**Depends on:** Tasks 1, 2 and 3, which define these names in these modules. This task imports each one from its defining module and changes none of them:

| Name | Defining module | Task |
|---|---|---|
| `Executor`, `NodeResult`, `Completed`, `Failed`, `FailureClass` | `graphscene.model.execution` | 1 |
| `return_violations` | `graphscene.adapters.return_schema` | 2 |
| `StubExecutor`, `Scripted`, `ScriptedOutcome`, `ScriptedFailure`, `ScriptedStall` | `graphscene.adapters.stub_executor` | 3 |

The contracts, as those tasks define them:

- `async def run(self, dispatch: Dispatch) -> NodeResult`.
- `NodeResult = Completed | Failed`.
- `Completed(outcome, detail=None)`.
- `Failed(failure, reason)`, where `FailureClass = Literal["infra", "agent", "undelivered"]`.
- `return_violations(document, schema) -> list[Violation]`.
- `StubExecutor(script)`, with `started`, `finished` and `cancelled`.

### Targets

- `graphscene/src/graphscene/facade/__init__.py`: imports and `__all__`.
- `graphscene/src/graphscene/__init__.py`: imports, `__all__` and the module docstring.
- `graphscene/tests/test_public_surface.py`: `_EXPECTED`, `_DEFINED_IN` and the new module imports. This is this task's own test file.
- `graphscene/README.md`: the five `change` sites of the story index's `## Scope register`, rows 1, 2, 3, 4 and 6.

**The order of the eleven new names.** They are appended to every list after `"LedgerPassage"`, in this order:

1. `"Executor"`
2. `"NodeResult"`
3. `"Completed"`
4. `"Failed"`
5. `"FailureClass"`
6. `"return_violations"`
7. `"StubExecutor"`
8. `"Scripted"`
9. `"ScriptedOutcome"`
10. `"ScriptedFailure"`
11. `"ScriptedStall"`

Appending keeps `_DEFINED_IN`'s existing `_EXPECTED[7:28]` slice pointing at the same `flow_graph` names.

**Work:**

- [ ] **`facade/__init__.py`.** Import the eleven names from their defining modules (table above) and append them to `__all__` in the order above. Its docstring's *"The rule:"* paragraph is unchanged.
- [ ] **`graphscene/__init__.py`.**
  - Import the eleven names from `graphscene.facade`, and append them to `__all__` (annotated `list[str]`) in the same order, per `.claude/context/graphscene.md` → `## The public surface`.
  - Add one sentence to the module docstring naming the executor protocol `Executor` with its `NodeResult`, the built-in `StubExecutor`, and `return_violations`. The boundary paragraph is unchanged.
- [ ] **`tests/test_public_surface.py`.**
  - Append the eleven names to `_EXPECTED` in the same order.
  - Add their `_DEFINED_IN` entries against `graphscene.model.execution`, `graphscene.adapters.return_schema` and `graphscene.adapters.stub_executor`, importing those three modules at the top as the file imports the others.
  - The existing test functions stay as they are.
- [ ] **`graphscene/README.md`, `## What it is`.**
  - **Opening paragraph (register row 1):** add one sentence. GraphScene declares how a node is run: an `asyncio` `Executor` protocol whose `run` takes a `Dispatch` and returns a `Completed` outcome or a `Failed` with an `infra`, `agent` or `undelivered` class. It also ships a scriptable `StubExecutor` for tests and `return_violations` for checking an executor's return against a JSON Schema it names. The engine does not yet drive an executor.
  - **`src/graphscene/model/` row (row 2):** add `execution.py` and its five names.
  - **`src/graphscene/adapters/` row (row 3):** add `return_schema.py` (`return_violations`) and `stub_executor.py` (`StubExecutor` and its script types). Neither gets a *"not public"* note, because both are exported.
- [ ] **`graphscene/README.md`, `## The layers`.**
  - **The `adapters` table row (register row 4):** add running a node from a script for tests, and checking a return against a JSON Schema, to what the layer holds.
  - **The protocol bullet (row 6):** *"Two exist: …"* becomes three, adding `Executor`, implemented by `StubExecutor` and by a host.
  - Rows 5 and 7 of the register stay unchanged, as the register states.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` passes. This is this task's own edited test file, and it proves both `__all__` lists match `_EXPECTED` and that each new name is the object its defining module defines.
- `commands.typecheck` passes.
- Re-run the story index's `## Scope register` derivation entries 1 and 2 against the edited README. Every line they print is a register row. The protocol bullet no longer says *"Two exist"*, and rows 5 and 7 still read as quoted there.
- Every name the README's new text cites is in `graphscene.__all__`, and the `adapters` row carries no *"not public"* note for the two new modules.
