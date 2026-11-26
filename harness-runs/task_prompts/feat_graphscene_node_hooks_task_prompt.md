`feat_graphscene_node_hooks` lets a graph declare each node's prompt source and side effects, so the planning driver's flow-specific code becomes declarations in the harness's planning graph. Part of #376.

## Why

The planning driver hard-codes its flow: `PD_FLOW`, prompts cut from fixed headings (`PNL_CORE_BLOCKS`), entry and resume from the story index and ledger `P1`–`P3`, commits as the planning fork's Overrides 3–6. A unit-loop driver built that way would be a second, larger copy.

## Decided (2026-11-26)

- **The scope is the task-plan fork.** Overrides 3–6 are those of `plugin/instructions/task_plan_writing_instructions_autonomous.md`: 3 commits the UI-test plan at convergence, 4 commits the task plan at convergence, 5 is pause/resume and the flow-progress ledger (planning half), and 6 commits each plan-review round. The user-review fix-plan fork's overrides go to #425.
- **GraphScene gets a per-node hook seam, before and after a node, both awaited by the engine.** A host-only seam is not enough: an adopter of GraphScene alone must be able to run hooks too. Planning decides whether a before-node hook runs once per node or once per attempt, since retries happen inside `execute_set`.
- **Commits and ledger flips stay out of the agents.** They are host hooks, run after a node or a round. Parallel gates committing would race, Override 6 commits a whole round rather than one node, and agents would need the commit wrapper in their allowlists.
- **The agent prompt is built by the host through `ClaudeExecutor`'s `AgentPromptBuilder`** _(from #421's branch, `feat_flow_host_claude_executor`)._ `Dispatch.prompt` is the prompt variant (`initial`, `revision`, or `None` for a node with no `prompts`), never the session's text. #421 added the seam: a builder the host passes at construction, a function from `Dispatch` to the agent prompt, called once per run before the launch, which must give the same text for a repeated run of the same dispatch. The executor records the built text on `SessionUsage.agent_prompt`. This branch ports the builder.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- Prompt sources and variants (`initial`, `revision`) declared per node.
- **Porting `pnl_prompt` as the flow host's `AgentPromptBuilder`** _(from #421's branch)._ `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_init` cuts the fenced blocks under the `PNL_CORE_BLOCKS` headings of `plugin/instructions/task_plan_writing_instructions_core.md`, and refuses a missing heading or a wrong block count before any session starts. `pnl_prompt` fills a block's `<prompt_path>`, `<state_dir>`, `<branch>`, `<iteration>`, `<review_mode>` and `<findings_file(s)>` tokens. The values come from the `Dispatch` the way `devscene-flow-host/src/devscene_flow_host/commands/render.py` → `_block` derives its `arg.*` lines: `round_number`, `converging`, the findings files of `closed_round`, and a non-round reviewer's iteration from the host's printed reads. `ClaudeExecutor`'s docstring leaves to this branch refusing a prompt source that cannot be built when the host constructs its builder.
- **Answered clarification pairs make the builder stateful.** `planning-driver-lib.sh` appends the answered pairs to the next writer prompt once (`PD_PAIR_NODE` / `PD_PAIR_TEXT`), and the builder must still return the same text for a repeated run of that dispatch. Planning decides whether the pairs reach the builder through the dispatch or through host state. Seen on the #325 resume (below): an answered park re-ran the writer with the `initial` prompt.
- **Renaming `Dispatch.prompt`** (to `prompt_variant`, say), so that it is not mistaken for the agent prompt again. It touches `graphscene/src/graphscene/engine/transitions.py`, `render.py`'s `_block` and the `prompt-known` reference check (below).
- **Round hooks, before and after a round**, are wanted too. Run mode already dispatches a round's gates as one set per call, so both fit around `execute_set`. The case to settle is a round resumed with gates already recorded (#450): whether its before-round hook runs again. Override 6 (commit each plan-review round) is an after-round hook.
- Hooks before and after a node, implemented by the host (commit these paths, flip a ledger entry, write an observation). A before-node hook has no seam yet: `execute_set` (#422) launches and retries a set's nodes inside one call, so an infrastructure retry would not run the hook again. An after-node hook fits after the set's records come back from it.
- Entry and resume decided by a host hook.
- Overrides 3–6 as hooks on the planning graph.
- Seen on the #325 resume: an answered park re-ran the writer with the `initial` prompt.
- **`prompt-known` ties prompts to the current declaration** _From #415 as merged (#444, 2026-11-22)._ an edge's `prompt` must be one of its target dispatch node's `prompts` (`graphscene/src/graphscene/engine/references.py`). If this branch changes how prompt sources and variants are declared, that reference check changes with it.
- **Where the host side lives** _Decided 2026-11-22 with #418._ GraphScene declares and calls the hooks. The harness's implementations go in `devscene-flow-host/`, DevScene's GraphScene host package (#451, renamed by #455): commits through the commit wrapper, ledger flips, observations, and prompt sources cut from plugin instruction documents (`PNL_CORE_BLOCKS`). A hook that is useful without DevScene belongs in GraphScene instead.
- **Entry and resume as a host hook build on #450's entry.** The hook decides where the walk stands from the story index and ledger `P1`–`P3`, and hands GraphScene the round, its number and the recorded gates.
- **A test ties the planning graph to the plugin core** _From #459's branch, `chore_retire_flow_graph_v3` (2026-11-25)._ Checks 4–7 of the retired `scripts/check-flow-graph.sh` are now `devscene-flow-host/tests/core_agreement.py`, run by `test_core_agreement.py` in gate leg `13j`. It holds the graph to `plugin/instructions/task_plan_writing_instructions_core.md` and two other plugin documents:
  - each dispatch node's `findingsFolder` and each round's revision note against the core's `## Setup` step 2 table and `## Loop`;
  - `counters.iteration.cap` against the core's cap phrases;
  - the run-mode skip ids and the route edges' ledger ids against the other two documents.

  The flow-to-core table is `CORE_FOR_FLOW`, kept in the test. If Overrides 3–6 become hooks, or prompt sources and paths move out of the core, the checker and its suite change with them.

## Depends on

#484
