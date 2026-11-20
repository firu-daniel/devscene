### 4. `vocabulary.py`'s docstring names the schema by a path that is also the repository's format-3 schema

**File:** `graphscene/src/graphscene/vocabulary.py`, module docstring: "the caller validates the graph against `schemas/flow-graph.schema.json` first"

The module docstring's *Deliberately not checked* list tells a caller to validate the graph against `schemas/flow-graph.schema.json` before calling `vocabulary_violations`. Inside the package that path means the format-4 package data, `graphscene/src/graphscene/schemas/flow-graph.schema.json`. But this repository also has `schemas/flow-graph.schema.json` at its root, and that file is the format-3 schema, which rejects every format-4 graph (`"formatVersion": { "const": 3 }`). A harness-side caller reading the docstring from the repository root would resolve it to the wrong schema. This file is a module docstring, so this is a wording fix.

**Fix:** replace that list item with:

```python
- Schema validity: the caller validates the graph against the format-4 schema this package
  ships as data, `schemas/flow-graph.schema.json` inside the `graphscene` package
  (`graphscene/src/graphscene/schemas/` in this repository), first.
```

Every line stays within the 100-column `ruff` limit. The fix edits no test file and runs none.
