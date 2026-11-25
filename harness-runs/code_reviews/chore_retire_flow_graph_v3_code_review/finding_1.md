### 1. `docs/watcher.md` still says "the two graphs" after the shipped table went down to one graph row

**File:** `docs/watcher.md` → the paragraph **Why only the `yes` rows carry a profile entry, and why that is not the reachability answer.** — "except the two graphs, which are read and never run"

Task 9 merged the shipped-scripts table's two rows, `flows/task_plan_writing.graph.json` and `flows/task_plan_writing.v4.graph.json`, into one row, `flows/task_plan_writing.graph.json`. That matches `cli/src/generators/outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`, which now ships one graph. The paragraph directly under that table still accounts for the `no` rows with "— except the two graphs, which are read and never run —". Now only one graph row exists, so the paragraph's count disagrees with the table it explains.

This is a sentence that describes the project and gives no step to follow, so it is a Should Fix (`finding_grades.md` → `## Never a Must Fix on its own`, *"A sentence that only describes the project and has become false, including a stale count"*). It is the lead that `harness-runs/task_plan_reviews/chore_retire_flow_graph_v3/review_2.md` → `## Incidental findings (not gating)` item 1 recorded. The scope register's derivation entry A could not reach it, because the sentence names no retired file. It was confirmed by reading the table and the paragraph on the branch tip.

**Fix:** in that paragraph of `docs/watcher.md`, replace

```
— except the two graphs, which are read and never run —
```

with

```
— except the graph, which is read and never run —
```

Change nothing else in the paragraph. No test reads this sentence, so the fix runs no test.
