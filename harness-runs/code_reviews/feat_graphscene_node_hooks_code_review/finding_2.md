### 2. The shipped `flow-walker.sh` header and the walker test helper still describe the planning graph as format 4

**File:** `cli/templates/scripts/flow-walker.sh` (the usage header comment) — "The graph is `<this script's dir>/flows/<flow>.graph.json`, formatVersion" followed on the next comment line by "#   4; the root is a bare `git rev-parse --show-toplevel`"
**File:** `cli/test/helpers/walker.mjs` (the doc comment above `WALKER_GRAPH_PATH`) — "The fixture's own copy of the format-4 graph the walker loads"

This branch raises the planning graph that `flow-walker.sh` hands to `devscene-flow-walker` to format 5: `cli/templates/scripts/flows/task_plan_writing.graph.json` → `"formatVersion": 5`, and GraphScene's builder now refuses anything else (`graphscene/src/graphscene/adapters/builder.py` → `build_flow_graph`, `"formatVersion: expected 5"`). Two comments in the `cli` layer still say format 4:

- **`cli/templates/scripts/flow-walker.sh`.** This is a template `init` copies byte for byte into every adopter's `scriptsDir`, so the stale header ships to adopters. The scope register's derivation entry for format statements missed it because its regex matches `formatVersion` and `4` only on one line, and here they are split across two comment lines.
- **`cli/test/helpers/walker.mjs`.** The `WALKER_GRAPH_PATH` doc comment calls the fixture's graph "the format-4 graph", but that fixture is `init`'s copy of the format-5 template.

The self-adopted `scripts/flow-walker.sh` is deliberately out of scope: it is re-rendered after merge, per the story index's `Manual setup required:`. Leave it alone.

Graded Should Fix: both are comments, which are never a Must Fix on their own, and neither gives a step that now fails.

**Fix:**

1. In `cli/templates/scripts/flow-walker.sh`, change the `4;` that continues the `formatVersion` sentence to `5;`, so the two comment lines read:

   ```bash
   #   The graph is `<this script's dir>/flows/<flow>.graph.json`, formatVersion
   #   5; the root is a bare `git rev-parse --show-toplevel` in the working
   ```

2. In `cli/test/helpers/walker.mjs`, change the doc comment above `WALKER_GRAPH_PATH` to:

   ```js
   /**
    * The fixture's own copy of the format-5 graph the walker loads — the one a mutation check edits,
    * never the template.
    */
   ```

Change nothing else in either file. Neither edit is to a test case: `walker.mjs` is a helper, and no test file is created or edited, so this fix runs no test. `cli/test/outer-loop-scripts.test.mjs` compares the written copy with the template's own bytes, so editing the template keeps that comparison intact. The full suite runs in the Run gates phase.
