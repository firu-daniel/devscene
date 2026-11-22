### 2. `arrive` declares an `open_gates` keyword no caller passes, and its comment says the walker uses it

**File:** `graphscene/src/graphscene/engine/transitions.py` (`arrive`) — "# `open_gates` is unused here; it is kept in the call shape `graphscene.engine.walker` uses."

`arrive` takes a keyword-only `open_gates: tuple[str, ...] = ()` and never reads it. The comment above its body says the keyword is *"kept in the call shape `graphscene.engine.walker` uses"*, and that is not true. `git grep -n 'arrive(' -- graphscene/` finds every call site, and none of them passes `open_gates`:

- `engine/walker.py` → `start` calls `arrive(graph, self.host, draft, e)`.
- `engine/walker.py` → `_step` calls `arrive(graph, host, draft, pending.resume)`.
- `engine/transitions.py` → `follow_edge` calls `arrive(graph, host, draft, edge.to, closed_round=closed_round)`.
- None of the five calls in `graphscene/tests/engine/test_transitions.py` passes it either.

`{open_gates}` is filled only inside `take_binding`, which gets it from `follow_edge` and `close_round`. A maintainer who follows the comment and passes `open_gates` to `arrive` would expect it to reach a stop summary, but `arrive` drops it.

**Fix:** remove the keyword and the comment from `arrive`:

```python
def arrive(
    graph: FlowGraph,
    host: PredicateHost,
    draft: WalkDraft,
    node_id: str,
    *,
    closed_round: tuple[GateRecord, ...] = (),
) -> Step:
    visited: set[str] = set()
    while True:
        ...
```

Change nothing else: no caller passes the keyword, so no call site changes. The fix edits no test file, so it runs none. The whole-tree typecheck and the suite run in the Run gates phase.
