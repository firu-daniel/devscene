# Task plan review — round 2

verdict: PASS
review_mode: converging

Round 1 raised no Must Fix. This round changed one file, `task_6_plan.md`, to answer architecture findings 1 and 2. I checked both changes and found no Must Fix.

- **The renamed-`iteration` graph-side case is sound.**
  - The mutant renames the `counters` key, `nodes.plan_round.counter` and every `increment` / `reset`. That keeps `graphscene`'s `counter-known` satisfied (`graphscene/src/graphscene/engine/references.py` → `_counter_known`).
  - The heartbeat's `{iteration}` placeholder stays. That is all the format-4 schema's `heartbeat` pattern requires (`graphscene/src/graphscene/schemas/flow-graph.schema.json`).
  - The claim *"anchors are only compared when there is a cap"* matches the bash checker it ports. In `scripts/check-flow-graph.sh` → `run_checks`, a graph with no cap returns before the `ANCHORS` loop.
- **The planted clean case is sound.**
  - It plants exactly the three documents the contract reads: `RUN_MODE_DOC`, `LEDGER_DOC` and `CORE_FOR_FLOW["task_plan_writing"]`.
  - Every changed-copy case now starts from that same plant.
- **Scope register.**
  - Re-running entry A verbatim reaches 16 files, and every one is a row.
  - Entry B's first step prints nothing.
  - Re-walking entry C reaches only documents that are already rows.
  - The revision note changes neither the register nor the target set, and this round's changes reach no corpus site.
- **No `## Rejected findings` section exists**, so there is nothing to test.

## Should Fix
1. **`task_6_plan.md` → the graph-side bullet still says each case asserts *"the exact single `Violation`"*.**
   - **Why that is wrong.** The case *"a `flow` absent from `CORE_FOR_FLOW`"* yields two violations under the file's own contract: one `findings-folder-in-core` and one `cap-matches-core`, both with path `flow`.
   - **Where it shows.** The bullet lists exceptions for the revision-note case and the cap-`6` case, but not this one. This round added the renamed-counter case to that list, so the list is within this round's reach. This was round 1 Should Fix 4.
   - **Fix.** Name the absent-flow case as asserting both findings.
2. **`task_6_plan.md` → document-side cases: *"Each changed-copy case asserts its 'refusing to pass' finding"* still leaves the step-2-table case's expected list open.**
   - **The question it leaves.** The contract does not say whether the revision-note clauses of check 6 still run when the table yields no backticked path.
   - **What the bash checker does.** In `scripts/check-flow-graph.sh` → `run_checks`, those clauses run outside the table's `if` / `else`. With the backticks stripped, that adds a `revision note '<dir>' is not in <core> ## Setup step 2 table` finding.
   - **Fix.** State whether those clauses run when the table is empty, and give that case's full expected list. This was round 1 Should Fix 2. This round rewrote the sentence without resolving it.
3. **`task_6_plan.md` → no document-side case deletes an owner document outright**, although the contract states *"A missing owner document or section reads as empty"*.
   - The new shared planting helper makes the missing case trivial: plant all three documents, then leave one out.
   - `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here` asks for *"one case per clause it enforces"*.
   - **Fix.** Add the case, or name its absence under the suite header's *"Deliberately not covered"*.
   - This round resolved the other half of round 1 Should Fix 3, the missing-`counters.iteration` clause.

## Incidental findings (not gating)
1. **The paragraph in round 1 Should Fix 1 is still unchanged and unreached.** `docs/watcher.md` → **Why only the `yes` rows carry a profile entry, and why that is not the reachability answer.** still says *"except the two graphs, which are read and never run"*.
   - Task 9 merges the two `flows/…` table rows, so after it the paragraph names two graphs where one ships.
   - The register's entry A does not reach this paragraph. It is a lead for the end-of-branch reviewers.
2. **Round 1 Nice to Have 1 is still open.** In `task_9_plan.md`, the Decision-record rule and the in-place edit to `### Item 2` → **Cost.** still disagree.
