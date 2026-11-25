### Task 1 — Ship the format-4 planning graph as `flows/task_plan_writing.graph.json` and retire the format-3 template

**Goal:** Make the format-4 planning graph the one file `init` ships under `flows/`, under the shipped name `task_plan_writing.graph.json`. The format-3 template there is retired, and everything in the `cli` layer that spells `.v4.graph.json` now spells the shipped name.

**Where this layer stops.** This task moves the template and updates this layer's readers of its name. It does **not** change what `devscene-flow-walker` looks for. That is `devscene_flow_host.commands.flow_walker.GRAPH_SUFFIX`, **Task 5's**, which moves it from `".v4.graph.json"` to `".graph.json"`. Until Task 5 lands, the flow host's suites and the `cli/test/flow-walker*` suites fail. That is the expected red window the story index's `## Context` states, and this task neither runs nor edits those suites. It also does not touch the self-adopted copies under `scripts/`, which are re-rendered after merge (story index → **Manual setup required**). The root `package.json` script `validate:graphscene-schema`, which names the old path, is **Task 7's**.

**What needs no edit here, and why.** The planning driver's libraries read the graph by the shipped name: `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_GRAPH` and its header's `cp` line, `cli/templates/scripts/lib/planning-driver-lib.sh` → `PD_ROUND_GATES`, and the comment above `hr_remote_planning_paths` in `cli/templates/scripts/lib/harness-run-lib.sh`. So do `cli/test/agent-return-schemas.test.mjs` → `GRAPH`, `cli/test/planning-node-lib.test.mjs`, `cli/test/watcher-planning-driver.test.mjs`, `cli/test/outer-loop-upgrade.test.mjs` and `cli/test/upgrade-report.test.mjs`. After this task they read the format-4 graph under that same name. Every key they read — dispatch nodes' `kind`, `agent` and `outcomes` keys, and round nodes' `gates` — has the same shape in both formats. Do not edit them.

### Targets

- `cli/templates/scripts/flows/task_plan_writing.graph.json` — replaced: the format-3 file is removed, and the format-4 file is moved onto this name.
- `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` — removed by that move.
- `cli/src/generators/outerLoopScripts.ts` — the `flows` rows of `OUTER_LOOP_SCRIPTS`.
- `cli/templates/scripts/flow-walker.sh` — its header's two mentions of the graph's name.
- `cli/test/helpers/walker.mjs` — `WALKER_GRAPH_PATH`.
- `cli/test/outer-loop-scripts.test.mjs` — `WALKER_FILES` and the test that iterates it.

**Work:**

- [ ] **The graph.** Delete the format-3 file `cli/templates/scripts/flows/task_plan_writing.graph.json`, then move `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` onto that name, its bytes unchanged. In the moved file, change only the top-level `description` string. Drop its last sentence, which names `scripts/generate-flow-graph-v3.mjs`, the format-3 graph and the claim that `init` does not copy the file. In its place, say that this is the graph `flow-walker.sh` hands `devscene-flow-walker` to walk, and that the planning driver's libraries read for its node list. Every other byte of the graph stays as it was.
- [ ] **`outerLoopScripts.ts`.** In `OUTER_LOOP_SCRIPTS`, remove the format-3 row and its comment (*"The format-3 graph: no walker reads it … Its retirement is #459's."*). Rename the `task_plan_writing.v4.graph.json` row to `file: 'task_plan_writing.graph.json'`, keeping `subdir: 'flows'`, `mode: 0o644` and `agentInvocable: false`. Its comment says that `devscene-flow-walker` walks it, that `flow-walker.sh` passes this directory as `--flows`, and that `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read its node list. Add no pruning, migration or upgrade handling for the file this table no longer ships: the task prompt's Decided section rules all three out.
- [ ] **`flow-walker.sh` header.** In the `start` / `next` / `current` usage block and in `EXIT CODES` → `1`, change `<this script's dir>/flows/<flow>.v4.graph.json` to `<this script's dir>/flows/<flow>.graph.json`. Change nothing else in the script.
- [ ] **`cli/test/helpers/walker.mjs`.** Set `WALKER_GRAPH_PATH` to `` `${INIT_SCRIPTS_DIR}/flows/${FLOW}.graph.json` ``.
- [ ] **`cli/test/outer-loop-scripts.test.mjs`.** `WALKER_FILES` becomes `flow-walker.sh` (`0o755`) and `flows/task_plan_writing.graph.json` (`0o644`). The comment above it and the test title it drives (*"the flow walker and its two graphs land verbatim …"*) now say the walker and its graph.

**Verification:**

- `npm test --workspace cli -- test/outer-loop-scripts.test.mjs` passes. It is the one test file this task edits.
- `git grep -n -e 'v4\.graph' -e 'format-3 graph' -- cli/src cli/templates/scripts/flow-walker.sh cli/templates/scripts/flows cli/test` prints nothing. The pathspec is this task's own reach. It deliberately leaves out `cli/templates/scripts/README.md`, which still names both graphs after this task: that README is **Task 2's**, and Task 2's own verification greps it.
- `git ls-files cli/templates/scripts/flows` lists `cli/templates/scripts/flows/task_plan_writing.graph.json` and no other path.
- `jq -r .formatVersion cli/templates/scripts/flows/task_plan_writing.graph.json` prints `4`.
- Compared with `git show HEAD:cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, the new `cli/templates/scripts/flows/task_plan_writing.graph.json` differs in the `description` line alone.
- `git grep -n 'task_plan_writing.graph.json' -- cli/templates/scripts/lib` still lists `PNL_GRAPH`, the header's `cp` line and the `hr_remote_planning_paths` comment, unedited. They are the readers that now get format 4 under the name they already use.
