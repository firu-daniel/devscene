# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_1_plan.md` — the closing `git grep` covers a README that Task 2 owns, so it cannot pass at Task 1**
   Task 1's second **Verification:** bullet greps the whole of `cli/templates`. That includes `cli/templates/scripts/README.md`, which Task 2 edits. Today that README carries both patterns on the paragraph opening *"**The other family in this directory is not generated.**"*: *"its graph `flows/task_plan_writing.v4.graph.json` and the format-3 graph `flows/task_plan_writing.graph.json` the planning driver reads"*. Running `git grep -n -e 'v4\.graph' -e 'format-3 graph' -- cli/src cli/templates cli/test` against the tree prints `cli/templates/scripts/README.md:5` along with Task 1's own targets. Nothing in Task 1's Work removes that line, so the bullet still fails after Task 1 is done.
   **Raised against:** "`git grep -n -e 'v4\.graph' -e 'format-3 graph' -- cli/src cli/templates cli/test` prints nothing."
   **Must hold:** Every Task 1 verification step can pass using only Task 1's own Work. Its grep covers only files Task 1 owns, or it explicitly excludes the sites Task 2 changes later.
   **Class:** Wrong build
   **Failure:** If the Task 1 implementer runs its verification `git grep … -- cli/src cli/templates cli/test` after finishing every Work bullet, it prints `cli/templates/scripts/README.md:5`. The task then either fails its own check or edits a file that Task 2 owns.
   **Fix:** In `task_1_plan.md`, narrow the grep's pathspec to Task 1's targets: `cli/src`, `cli/templates/scripts/flow-walker.sh`, `cli/templates/scripts/flows` and `cli/test`. Alternatively, add `':!cli/templates/scripts/README.md'` and note that this file is Task 2's.

2. **`task_7_plan.md` — the closing `git grep` matches the format-4 schema path that stays, and a README that Task 8 owns**
   The pattern `schemas/flow-graph\.schema\.json` is a substring of the format-4 schema path `graphscene/src/graphscene/schemas/flow-graph.schema.json`. The story index's own register rows 4 and 20 already note this. After Task 7, the bullet's pathspec still hits:
   - `package.json` → `validate:graphscene-schema` and `validate:graphscene-schema:negative`, which Task 7 keeps as legs `3g`/`3h`;
   - `graphscene/README.md:13`, `graphscene/src/graphscene/adapters/schema.py:2`, `graphscene/src/graphscene/engine/vocabulary.py:13` and `graphscene/src/graphscene/facade/loading.py:5`;
   - `cli/test/python-packages-staged.test.mjs:127`.

   The `schemas` pathspec also covers `schemas/README.md`, whose paragraphs on `generate-flow-graph-v3`, `check-flow-graph`, `validate:flow-graph` and `flow-graph-check` are Task 8's to remove. The bullet's carve-out names only `docs/`, `ROADMAP.md` and `.claude/context/`.
   **Raised against:** "`git grep -n -E 'check-flow-graph|generate-flow-graph-v3|validate:flow-graph|flow-graph-check|flow-graph-schema-|schemas/flow-graph\.schema\.json' -- package.json scripts schemas cli devscene-flow-host graphscene plugin` prints nothing."
   **Must hold:** Task 7's absence check reaches only references to the retired format-3 artifacts. It never matches the format-4 schema path, which stays, and never matches a file a later task owns. It therefore passes once Task 7's own Work is done.
   **Class:** Wrong build
   **Failure:** If the Task 7 implementer runs this verification after its Work, the command prints the kept `validate:graphscene-schema` lines in `package.json`, four `graphscene/` files, `cli/test/python-packages-staged.test.mjs` and `schemas/README.md`. The implementer can then pass only by editing files outside Task 7's targets, including the leg-`3g`/`3h` scripts that must stay.
   **Fix:** In `task_7_plan.md`, anchor the schema alternative so it does not match a `…/schemas/` prefix, for example `(^|[^/])schemas/flow-graph\.schema\.json`. Also drop `graphscene` from the pathspec, or exclude the format-4 docstrings by path. Add `':!schemas/README.md'`, and extend the carve-out sentence to name it as Task 8's.

3. **`task_9_plan.md` — the entry-A verification states a result that the task's own Work leaves false**
   The first **Verification:** bullet says entry A, among Task 9's files, reaches only register rows 14 and 17 plus lines inside the new **Changed** paragraphs. But the same task's **Decision-record rule** keeps several matching passages verbatim:
   - Item 6 **Decision.** (*"`flows/task_plan_writing.v4.graph.json` ship from `cli/templates/scripts/`"*) and its existing `**Changed 2026-11-25 (#419).**` (*"format-3 graph"*);
   - the iteration cap's **Cost, and how it is guarded.** (`scripts/check-flow-graph.sh`), which gets a **Changed** paragraph and is not edited in place;
   - the *Format 4* heading (*"format 3 is generated from it"*), which stays as a cited anchor;
   - *Format 4* **Decision.** (`task_plan_writing.v4.graph.json`), **Cost.** (*"format-3 readers"*) and the existing #419 **Changed** paragraph.

   Each still matches entry A's pattern, and none is row 14, row 17 or a new **Changed** paragraph. The new **What it owns.** text that Work requires also names `graphscene/src/graphscene/schemas/flow-graph.schema.json`, which matches `schemas/flow-graph\.schema\.json`.
   **Raised against:** "Re-run the story index's `## Scope register` derivation entry A verbatim. Among this task's three files, it reaches only the sites that register marks `no-change` (rows 14 and 17), and lines inside the new **Changed** paragraphs, which name what they retired."
   **Must hold:** Task 9's verification states exactly the entry-A sites its own Work leaves in place: the kept **Decision.** / **Cost.** / earlier **Changed** paragraphs of rows 13, 15 and 16, the kept *Format 4* heading, rows 14 and 17, the new **Changed** paragraphs, and the format-4 schema path in **What it owns.** It must not ask for an outcome that requires editing text the Decision-record rule keeps.
   **Class:** Wrong build
   **Failure:** If the Task 9 implementer completes the Work and then runs this verification, entry A still reaches lines such as Item 6's kept **Decision.** naming `flows/task_plan_writing.v4.graph.json`. The bullet then fails, and the implementer either reports the task unfinished or edits a decision of record that the same file says must stay.
   **Fix:** In `task_9_plan.md`, restate the bullet as the full list of sites expected to remain: rows 14 and 17; the kept **Decision.**, **Cost.** and earlier **Changed** paragraphs of Item 6, the iteration cap and *Format 4*; the *Format 4* heading; the new **Changed** paragraphs; and the format-4 schema path in **What it owns.** Alternatively, replace it with a check scoped to the three live passages the Work edits in place.

## Should Fix
1. **Story index (`chore_retire_flow_graph_v3_story_plan.md`) → `## Scope register` — a stale site that no derivation entry reaches (disposition ii).** `docs/watcher.md` → the paragraph opening **Why only the `yes` rows carry a profile entry, and why that is not the reachability answer.** says *"except the two graphs, which are read and never run"*. After Task 9 the shipped-scripts table has one graph row, so the sentence becomes false. Entry A does not match it, because none of its alternatives spell the count. Sites newly reached: `docs/watcher.md` → that paragraph. The other hits of `two graphs`/`both graphs` are `cli/README.md`, `cli/templates/scripts/README.md`, `ROADMAP.md`, `docs/development.md`, `docs/flow-graph-walker.md` and `schemas/README.md`, all already rows. Corrected entry A, strictly wider: add `|two graphs|both graphs` to its `-E` alternatives. Then add the row: `change`, Task 9, which already targets `docs/watcher.md`. It is graded Should Fix because the sentence only describes the shipped set and gives no step that fails.
2. **`task_6_plan.md` — the contract leaves open whether the revision-note checks run when the step-2 table yields no backticked path.** In `scripts/check-flow-graph.sh` → `run_checks`, the revision-note checks run whatever the table yielded. Once backticks are stripped, the document-side case would also yield `findings-folder-in-core: revision note '<dir>' is not in <core> ## Setup step 2 table`. The contract says that case "asserts its *refusing to pass* finding" but never says whether that is the only finding. State the expected full list for that case, and say whether check 6's revision-note clauses still run.

## Nice to Have
1. **`task_9_plan.md`** — the Decision-record rule says *"Its **Decision**, **Reason** and **Cost** text stays as decided"*, while Work edits Item 2's **Cost.** in place as "live text". Say explicitly that Item 2's **Cost.** is the one exception, so the rule and the Work bullet read the same way.
