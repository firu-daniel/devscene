### 2. Two documents say `graphscene.vocabulary` checks the harness's format-4 graph, but it runs only on generic fixtures

**File:** `docs/development.md` → **Gate 3 — configuration and flow-graph schemas.**: "The check that every name a format-4 graph uses is one it declares is not a gate 3 leg"; and `docs/flow-graph-walker.md` → `### Format 4 — the graph declares its vocabulary, and format 3 is generated from it`: "checks that every name the graph uses is one it declares"

`docs/development.md` says the used-against-declared check "is `graphscene/tests/test_vocabulary.py`'s, run by gate 13's leg `13g`". The `docs/flow-graph-walker.md` decision paragraph is about the planning graph, and in that context it says `vocabulary_violations` "checks that every name the graph uses is one it declares". Both sentences tell a maintainer that the harness's own format-4 source, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, goes through that check. It does not. `graphscene/tests/test_vocabulary.py` calls `vocabulary_violations` only on planted graphs and on `graphscene/tests/fixtures/flow_graph/*.json`. For the harness's source, the only check of used names against declared ones is `scripts/generate-flow-graph-v3.mjs` (gate 3i): its `checkVocabulary` and the per-node checks in `generate`. A maintainer who relies on 13g to catch an undeclared name in the harness graph is relying on a check that never reads that file.

**Fix:**

In `docs/development.md`, replace the sentence that begins "The check that every name a format-4 graph uses is one it declares is not a gate 3 leg" with:

> The check that every name a format-4 graph uses is one it declares has two homes. For a generic graph it is `graphscene.vocabulary.vocabulary_violations`, tested by `graphscene/tests/test_vocabulary.py` on the generic fixtures and run by gate 13's leg `13g`. For the harness's own source, `scripts/generate-flow-graph-v3.mjs` (`3i`) refuses an outcome, binding, predicate or stop reason the vocabulary does not declare, before it generates anything.

In `docs/flow-graph-walker.md`, `### Format 4 — …` → **Decision.**, replace "`graphscene.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/vocabulary.py`) checks that every name the graph uses is one it declares." with:

> `graphscene.vocabulary.vocabulary_violations` (`graphscene/src/graphscene/vocabulary.py`) is the generic check that every name a format-4 graph uses is one it declares. For this graph, `scripts/generate-flow-graph-v3.mjs` makes the same refusal before it generates the format-3 copies.

The "stop reason" wording is true only once Finding 1 has landed, so apply this finding after Finding 1. The fix edits no test file and runs none.
