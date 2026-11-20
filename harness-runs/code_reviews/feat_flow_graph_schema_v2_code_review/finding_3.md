### 3. `docs/flow-graph-walker.md` still calls a cap change an edit to "the graph", which is now a generated file

**File:** `docs/flow-graph-walker.md`, the **Cost, and how it is guarded.** paragraph above `### Format 4 — the graph declares its vocabulary, and format 3 is generated from it`: "Changing the cap is still a three-place edit (the graph and both core sentences)"
**Class:** Wrong action from operative text
**Failure:** If a maintainer follows "Changing the cap is still a three-place edit (the graph and both core sentences)" and edits `counters.iteration.cap` in `cli/templates/scripts/flows/task_plan_writing.graph.json`, then gate 3i fails with "differs from the graph generated from …; run node scripts/generate-flow-graph-v3.mjs --write", and running that remedy regenerates the file from the unedited format-4 source, reverting the cap edit.

This branch made `cli/templates/scripts/flows/task_plan_writing.graph.json` a generated file. Its source is `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, and gate 3i fails on any hand edit to either format-3 copy. The cap paragraph two sections earlier still tells a maintainer that changing the cap means editing "the graph". The walker reads the format-3 file, so a maintainer following that sentence edits it. Gate 3i then reports the copy as different and prints the remedy `run node scripts/generate-flow-graph-v3.mjs --write`. Running that remedy regenerates both copies from the unedited format-4 source and silently reverts the cap edit. The scope register's row 4 changed this document only to add the new decision section and extend the schema pointer, so this sentence was missed.

**Fix:** replace that sentence with:

> Changing the cap is still a three-place edit: the `counters.iteration.cap` of the format-4 source `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, regenerated into both format-3 copies with `node scripts/generate-flow-graph-v3.mjs --write`, and both core sentences. It also needs a re-sizing of `MAX_TOTAL_DISPATCHES`, which no check derives.

The fix edits no test file and runs none.
