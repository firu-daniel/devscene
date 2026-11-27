### 3. The schema's top-level `description` lost the space after "format 5:"

**File:** `graphscene/src/graphscene/schemas/flow-graph.schema.json` (the top-level `"description"`) — "The routing of one flow as data, format 5:which agent each node dispatches"

Task 2 changed `format 4: which agent` to `format 5:which agent` and dropped the space after the colon. The text is prose that no check parses. `graphscene/tests/test_flow_graph_schema.py` → `harness_names` scans the schema for harness vocabulary only, and no test asserts this description. So this is wording only.

**Fix:** put the space back, so the description opens:

```json
  "description": "The routing of one flow as data, format 5: which agent each node dispatches, …",
```

Change nothing else in the string. The schema is package data and no test file is edited, so this fix runs no test. Gate 3's `validate:graphscene-schema` and gate 13's `graphscene` legs re-read the schema in the Run gates phase.
