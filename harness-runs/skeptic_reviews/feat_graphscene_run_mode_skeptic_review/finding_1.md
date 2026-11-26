### 1. `_drive` spins forever when the saved walk's `pending` is a `Wait`: `continue_run` never returns

**File:** `graphscene/src/graphscene/engine/run_loop.py` (`_drive`) — "if isinstance(step, Wait):"
**Class:** Wrong behaviour
**Failure:** If a host calls `continue_run` over a saved walk whose `pending` is a `Wait`, then `continue_run` never returns: `_drive` calls `walker.current()` through `asyncio.to_thread` in an endless loop (37,627 calls in 2 s in the probe below), and the run hangs instead of ending on a `RunExit`.

**The problem.** `_drive` handles a `Wait` by taking `Walker.current()` in its place and looping:

```python
        if isinstance(step, Wait):
            step = await asyncio.to_thread(walker.current)
            continue
```

The module docstring justifies this with "`Walker.current()`, the set of gates still out, is taken in its place". That holds only if the saved `pending` is never itself a `Wait`. Nothing guarantees it:

- `graphscene/src/graphscene/engine/walker.py` (`Walker.current`) — "return state.pending" returns the saved `pending` verbatim, and `graphscene/src/graphscene/model/walk_state.py` → *"`pending` is exactly what `current` returns"*.
- `WalkState.pending` is typed `Action`, and `graphscene/src/graphscene/model/walk_actions.py` → `Action: TypeAlias = Dispatch | DispatchSet | Wait | Interrupt | Stop | End` includes `Wait`.
- `graphscene/src/graphscene/adapters/walk_json.py` (`_action`) — `if kind == "wait":` decodes a `{"kind": "wait", …}` `pending` into a `Wait`. The module docstring, under *"Deliberately not checked"*, says a state the walk cannot reach "decodes as written". So `FileStateStore.read` hands such a document back, and `continue_run` → `Walker.current()` returns the `Wait`.

When `current()` returns a `Wait`, the branch above sees a `Wait` again, calls `current()` again, and gets the same `Wait`. The loop never reaches `execute_set` or a `return`. It yields to the event loop on each thread hop, so only an outside cancellation ends it.

The walker itself never saves a `Wait` as `pending`: `graphscene/src/graphscene/engine/rounds.py` (`record_gate`) stores a cut-down `DispatchSet` and only *returns* the `Wait`. So the input is a foreign or hand-edited state file, but it is one the library's own codec and model accept. In step mode the same state is harmless, because `current()` simply returns the `Wait` to the host. Run mode turns that same input into a hang where it should return an exit. Every other unusable input `_drive` meets ends the call with a returned `Refused`.

**Proof (probe, executed).** `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_wait_probe.py <repo_root>` ran these steps:

1. Load `graphscene/tests/fixtures/flow_graph/valid_plain_round.json` and `Walker.start("checks")` over a `FileStateStore` in a temporary directory.
2. Rewrite the saved state with `pending=Wait("checks", recorded=GateRecord("lint", "accepted", None), pending=("license",))`.
3. Call `continue_run` under `asyncio.wait_for(…, timeout=2)`, with `walker.current` wrapped in a call counter.

It printed:

```
start: DispatchSet
current: Wait(round='checks', recorded=GateRecord(gate='lint', outcome='accepted', detail=None), pending=('license',))
continue_run did not return within 2s; walker.current calls: 37627
```

**Fix:**

1. In `graphscene/src/graphscene/engine/run_loop.py` → `_drive`, replace the `Wait` branch with:

   ```python
           if isinstance(step, Wait):
               step = await asyncio.to_thread(walker.current)
               if isinstance(step, Wait):
                   return Refused("the saved walk's pending action is a wait, which names no dispatch")
               continue
   ```

   `Refused` is already imported there, and a `Refused` is already a `RunExit`.

2. In the same module's docstring, change the bullet ending "A `Wait` is never dispatched: `Walker.current()`, the set of gates still out, is taken in its place. An `End`, `Stop`, `Interrupt` or `Refused` is returned." to "A `Wait` is never dispatched: `Walker.current()`, the set of gates still out, is taken in its place, and if that is itself a `Wait` the call returns `Refused("the saved walk's pending action is a wait, which names no dispatch")`. An `End`, `Stop`, `Interrupt` or `Refused` is returned." Re-wrap the bullet to the file's line length.

3. In `graphscene/tests/engine/test_run_loop.py`:

   - Add `import dataclasses` beside `import contextlib`.
   - Add `Wait` to the `from graphscene.model.walk_actions import (...)` list, after `Stop`.
   - Append this case at the end of the file:

   ```python
   def test_a_saved_wait_pending_is_refused_instead_of_looping() -> None:
       store = MemoryStore()
       walker = _walker(store)
       assert isinstance(walker.start("review_round"), DispatchSet)
       assert store.state is not None
       store.state = dataclasses.replace(
           store.state,
           pending=Wait("review_round", recorded=GateRecord("g1", "approved", None), pending=("g2",)),
       )
       writes = store.writes
       assert _continue(walker, _stub({})) == Refused(
           "the saved walk's pending action is a wait, which names no dispatch"
       )
       assert store.writes == writes
   ```

   - In the module docstring, after "re-raises with nothing of the set recorded", add ", and a saved `Wait` pending is refused rather than looped on".

   `review_round` is an entry of `_graph()`, as `test_a_gates_detail_is_recorded_with_its_outcome` already relies on. Without the fix this case hangs, so it lands in the same change as step 1. This test file is the one the fix edits, so it is the only test the fix runs.
