### Task 2 — Describe the one shipped planning graph in the CLI's READMEs and drop the bash checker from a suite header

**Goal:** The two `cli`-layer READMEs describe the shipped set as it stands after Task 1: **one** planning graph under `flows/`, `task_plan_writing.graph.json`. `devscene-flow-walker` walks it, and the planning driver's libraries read it for its node list. One suite header stops citing `scripts/check-flow-graph.sh`, which Task 7 deletes.

**Depends on:** Task 1, which ships the format-4 graph as `<scriptsDir>/flows/task_plan_writing.graph.json` and removes the `task_plan_writing.v4.graph.json` row from `OUTER_LOOP_SCRIPTS` (`cli/src/generators/outerLoopScripts.ts`). This task documents that set and changes no file Task 1 changed.

**Adopter-facing wording rule.** Both READMEs reach adopters: `cli/README.md` is the npm package's own, and `cli/templates/scripts/README.md` ships beside the scripts. Neither names the `.v4` file, says that a name changed, or tells an adopter what to do with a stale copy left by an earlier `init` (`harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path: … no sentence that names the old value or says a name changed; adopters migrate by hand."*).

### Targets

- `cli/README.md` — the paragraph opening *"TypeScript in `src/` compiles with `tsc` to `dist/`"*.
- `cli/templates/scripts/README.md` — the paragraph opening *"**The other family in this directory is not generated.**"*.
- `cli/test/run-gates-park-answer.test.mjs` — its header comment only.

**Work:**

- [ ] `cli/README.md`: replace *"with the planning flow's two graphs beside them under `flows/`: the format-4 `task_plan_writing.v4.graph.json` the walker walks and the format-3 `task_plan_writing.graph.json` the planning driver reads"* with one graph beside them under `flows/`, `task_plan_writing.graph.json`, which the walker walks and the planning driver's libraries read for its node list.
- [ ] `cli/templates/scripts/README.md`: in the list of copied files, *"its graph `flows/task_plan_writing.v4.graph.json` and the format-3 graph `flows/task_plan_writing.graph.json` the planning driver reads"* becomes its graph `flows/task_plan_writing.graph.json`, which the planning driver also reads. Then rewrite the sentence *"`flows/task_plan_writing.v4.graph.json` is the format-4 source this repository generates the format-3 graph from, and the graph `flow-walker.sh` passes `devscene-flow-walker` to walk."* so that it names `flows/task_plan_writing.graph.json` as the graph `flow-walker.sh` passes `devscene-flow-walker` to walk, with no mention of generation or of format 3.
- [ ] `cli/test/run-gates-park-answer.test.mjs`: in the header comment, *"no flow-graph fixture covers Phase G (`scripts/check-flow-graph.sh` checks the task plan-writing graph only)"* becomes a statement that the planning graph's checks cover the task-plan-writing graph only. It names no script. No test case changes.

**Verification:**

- `npm test --workspace cli -- test/run-gates-park-answer.test.mjs` passes, unchanged in what it asserts. It is the one test file this task edits.
- `git grep -n -e 'v4\.graph' -e 'format-3' -e 'check-flow-graph' -- cli/README.md cli/templates/scripts/README.md cli/test/run-gates-park-answer.test.mjs` prints nothing.
- Each of the two READMEs names `flows/task_plan_writing.graph.json` as the walker's graph, and as the one file the planning driver reads for its node list.
