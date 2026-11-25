`chore_retire_flow_graph_v3` retires the format-3 bridge that #413 added and the bash checks that still read it, now that #419 has moved the walker to Python. Part of #376.

## Why

Split out of #419 on 2026-11-23, so the walker cutover lands on its own. After #419 the bash walker is gone. The v3 copies of the planning graph are still read by their generator, the drift check, `scripts/check-flow-graph.sh` and the script-driven planning driver's two libraries (see **What #419 left for this branch** below).

## Decided (2026-11-25)

- **`init` does not remove files it no longer ships.** The v3 graph file this branch stops shipping stays in an adopter's `<scriptsDir>/flows/` after an upgrade, as `lib/flow-walker-gates.sh` stayed after #419. No pruning, no migration step, no `doctor` check for it. This repository's own self-adopted copies, `scripts/flows/task_plan_writing.graph.json` and any other v3 file the re-render no longer writes, are deleted by hand after merge, together with the re-render, which is a post-merge user step and not a run task.

## Leads

_The leads below are starting points from #376, #419 and the discussion that split them, not requirements. The planning session decides what holds when this branch is planned._

- **The v3 bridge from #413 retired:**
  - the planning graph's generated v3 copies (`cli/templates/scripts/flows/` and `scripts/flows/`), the harness-side v3 generator and its drift check;
  - the v3 schema `schemas/flow-graph.schema.json`, with its `schemas/negative/flow-graph-schema-*` and `schemas/flow-graph-check/` fixtures, and the `validate:flow-graph*` npm scripts;
  - gate legs `3c`–`3f` and `3i`. `3c`–`3d` run the v3 npm scripts; `3e`–`3f` run `check-flow-graph.sh`, whose checks 1–3, 8 and 9 #415 replaces and whose checks 4–7 move to `devscene-flow-host` first. `3g`–`3h` stay, for the format-4 schema;
  - the generator's own names check (the library's `vocabulary_violations` takes over);
  - the docs that describe the bridge: `docs/flow-graph-walker.md` → *Format 4*, `docs/development.md` → Gate 3, `schemas/README.md`, `cli/templates/README.md`, `cli/templates/scripts/README.md`, and the GraphScene row of `ROADMAP.md`.
- **The v4 graph becomes the shipped file under the shipped name.** `outerLoopScripts.ts` ships `task_plan_writing.v4.graph.json` beside `task_plan_writing.graph.json` since #419. Renaming the v4 file to the shipped name reaches further than `outerLoopScripts.ts` and `validate:graphscene-schema`:
  - `devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` → `GRAPH_SUFFIX = ".v4.graph.json"`, the suffix the command finds `<flows>/<flow><suffix>` by, and its module docstring;
  - `cli/templates/scripts/flow-walker.sh`'s header, which names `<this script's dir>/flows/<flow>.v4.graph.json`;
  - `cli/test/helpers/walker.mjs` → `WALKER_GRAPH_PATH`;
  - `devscene-flow-host/README.md`, and `cli/test/agent-return-schemas.test.mjs`, which reads the v3 copy today.
  
  A `devscene-flow-host` change reaches the main checkout's walker only after a re-provision (`bash scripts/flow-host-provision.sh`), because the walker's environment installs the packages as wheels (#478).
- **`check-flow-graph.sh` is only partly replaced by #415** _From #415 as merged (#444, 2026-11-22)._ #415 ported checks 1–3, 8 and 9, restated on declared primitives, plus a reference check the bash script never had. Checks 4–7 (`run-mode-id-known`, `ledger-id-known`, `findings-folder-in-core`, `cap-matches-core`) read plugin documents and stayed in bash. Retiring the script and `schemas/flow-graph-check/` means porting 4–7 to `devscene-flow-host` reading the format-4 graph first (settled 2026-11-22, when #418 was split; moved here from #419 on 2026-11-23). Until that port lands, gate legs `3e` / `3f` keep running checks 4–7 on the v3 copy.
- **Where the ported checks 4–7 run is open.** They read plugin documents: `task_plan_writing_instructions_core.md` and the run-mode and ledger ids. That is a dev-time gate over this repository, not something the walker does at run time in an adopter's repository. Which surface carries them is for planning: a new `devscene-flow-host` verb, a function a gate leg calls, or something else. So is whether reading `plugin/` documents sits inside `devscene-flow-host`'s boundary (`.claude/context/devscene-flow-host.md` → `## What it may depend on`).
- **Agreement between the two checkers is by meaning, not line for line.** Checks 8 and 9 were restated: check 8 picks gates by a fail verdict with no increment instead of `findingsFolder`, and check 9 accepts any writer route edge into the round instead of `returned`. A suite comparing them on the harness graph compares check ids, and the Python ids sit at the start of the reason text (`<check-id>: <detail>`).
- **How the comparison gets the check id is open** _From #452 as merged (#460, 2026-11-23)._ `graphscene check <graph>` prints `{"stage", "violations": [{"path", "check", "reason"}]}`. For stage `static`, `check` is the id split off the reason at its first `": "`, and `reason` is the rest; for every other stage `check` is `null`. The split is done once, by `check_document` in `graphscene/src/graphscene/adapters/check_json.py`. `Violation` still has no id field, and `check_document` is not public (not in `graphscene.__all__`), so `devscene-flow-host`, which reaches GraphScene only through its public surface, cannot call it as it stands. The routes to weigh: run `graphscene check` and read its `check` field; export the splitter through `graphscene.__all__` (a `graphscene`-layer change); or add a check-id field on `Violation`. Each reuses the one split rule instead of parsing the prefix a second time.
- **The two checkers differ on graphs without a review loop** _From #417 as merged (#448, 2026-11-22)._ The Python checker runs check 8's graph-wide clause and check 9's (ii), (iv) and (v) only where a round declares `writer`. Its check 3 also walks a round's fan-out for a fail edge that is not a gate's own (`graphscene/src/graphscene/engine/static_check.py`). The bash checker applies everything to every round. They agree on the harness's planning graph, whose `plan_round` opts in. A suite comparing them over plain-round fixtures will see differences that are intended.

## What #419 left for this branch

_From #419's branch, `feat_flow_walker_python_cutover` (2026-11-25)._

- **The v4 graph ships beside the v3 one**, because the script-driven planning driver still reads the v3 file. Removing the v3 file and renaming the v4 one are this branch's.
- **The planning driver's libraries read the v3 graph.** They are not in the bridge list above, and retiring the v3 file without re-pointing them breaks script-driven planning, which is on in this repository (`execution.scriptDrivenPlanning`):
  - `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_GRAPH` (`<worktree>/<scriptsDir>/flows/task_plan_writing.graph.json`), its dispatch-node and agent read, `PNL_REAP_JQ`'s `--slurpfile g`, and the header's `cp` line;
  - `cli/templates/scripts/lib/planning-driver-lib.sh` → `PD_ROUND_GATES`, which reads the round nodes' `gates` through `PNL_GRAPH`;
  - the comment mirror in `cli/templates/scripts/lib/harness-run-lib.sh` above `hr_remote_planning_paths`, which names `task_plan_writing.graph.json` → `findingsFolder`.
  
  Checked 2026-11-25: the v4 round nodes carry the same keys as v3 (`gates`, `kind`, `writer`, `plan`, `revisionNote`, `counter`, `outcomes`), and v4 dispatch nodes carry `kind` and `agent`. `PNL_REAP_JQ` reads `nodes[<node>].outcomes`' keys and the round nodes' `gates`, and every dispatch node declares the same outcome keys in the same order in both files. So re-pointing looks like a path change.
- **The planning driver runs the main checkout's walker** (#419's Task 6), with the run copy as its working directory, while `PNL_GRAPH` reads the run copy's graph. During this branch's own run, the walker reads the main checkout's graph and the libraries read the run copy's. Renaming or removing a graph file on the branch does not reach the walker until merge, re-render and re-provision.
- **What `init` leaves behind:** see **Decided (2026-11-25)** above. #419 already left `lib/flow-walker-gates.sh` in place for adopters and in this repository's `scripts/lib/`.

## Depends on

#419
