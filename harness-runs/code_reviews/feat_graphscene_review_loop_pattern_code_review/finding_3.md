### 3. The reflowed `references.py` docstring leaves a stub line, "key order; within"

**File:** `graphscene/src/graphscene/engine/references.py` (module docstring) — "key order; within"

Task 3 inserted "and `counter` when present" into the report-order sentence. It rewrapped only the edited line, so the paragraph now holds a three-word line in the middle:

```
`gates[i]`, `writer` and `counter` when present, `plan[i]`, `revisionNote`, then its outcomes in
key order; within
a dispatch node: its outcomes in key order, then its `skip` entries. Within a route edge: `to`,
```

This is wording and layout only. Nothing reads it as input.

**Fix:** rejoin the stub line with the next one, so the passage reads (each line within 100 characters, the `ruff` `line-length`):

```
`gates[i]`, `writer` and `counter` when present, `plan[i]`, `revisionNote`, then its outcomes in
key order; within a dispatch node: its outcomes in key order, then its `skip` entries. Within a
route edge: `to`, `increment`, `reset`, `prompt`, `report.<slot>` in key order,
`onCap.roundCounts[i]`, `onCap.evidence`; within a binding edge: `resume`, `roundCounts[i]`,
`evidence`; within a skip entry: `to`, then `report.<slot>`. Paths use the serialized spelling
(`onCap`, `roundCounts`, `revisionNote`). An unknown `start` is reported once, as `node-known`; an
unknown route `to` carrying a `prompt` is reported as `node-known` alone.
```

The fix creates and edits no test file, so it names no test run: the unit's whole-tree typecheck and the tree guards the loop selects are its verification.
