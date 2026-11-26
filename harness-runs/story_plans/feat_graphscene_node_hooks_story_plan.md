# Story: GraphScene node hooks and declared prompt sources

## Context

This branch lets a flow graph declare, per node, where its agent prompt comes from and which host side effects run around it, and gives GraphScene's run mode the seam that runs those side effects. It then turns the planning driver's flow-specific code into declarations on the harness's planning graph, and implements the host side in `devscene-flow-host/`. The driver hard-codes four things, and each gets a declaration or a host function:

- **its prompts**, cut from the `PNL_CORE_BLOCKS` headings of `plugin/instructions/task_plan_writing_instructions_core.md` (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_init`, `pnl_prompt`);
- **its entry and resume**, decided from the story index and the ledger's `P1`–`P3` (`cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_entry`);
- **its commits and ledger flips**, which are Overrides 3–6 of `plugin/instructions/task_plan_writing_instructions_autonomous.md` (`pd_act`, `pd_handoff`, and `cli/templates/scripts/lib/planning-record-lib.sh` → `prl_round_commit`, `prl_convergence_commits`, `prl_ledger_flip`);
- **its flow name**, which the graph already carries.

The work goes bottom-up through four layers. The `cli` task authors the declarations on the shipped planning graph. The `graphscene` tasks add the format, the check, the hook model, the run-mode seam and the public surface. The `devscene-flow-host` tasks add the readers, the prompt builder, the commit points, the planning hooks, the entry decision, the core-agreement check and the README. The `general` task records the decision.

**Decisions this plan takes.** The task prompt leaves several things to planning. Each answer below is stated once here. The task that implements it restates the contract it needs.

- **The graph format becomes 5.** The schema's own `formatVersion` description says *"A change to the key set raises it"*, and this branch adds keys. Format 5 adds four optional keys:
  - `vocabulary.hooks`: hook names, each declared as `{}`;
  - `promptSource` on a dispatch node: an opaque host string that GraphScene never parses;
  - `before` and `after` on dispatch and round nodes;
  - `before` on a terminal node.

  `prompts` stays the list of variants, so the `prompt-known` reference check (`graphscene/src/graphscene/engine/references.py` → `_prompt_known`) is unchanged. Task 2 owns every fixture's version. The planning graph moves to format 5 in Task 1, which ships first because `cli` is first in the configured layer order. The graph validates only once Task 2 lands. The first suite that loads it under the new schema is Task 13's.
- **Hooks are run mode's alone.** `Walker` (step mode), `flow-walker.sh`, the `graphscene` command line and the bash planning driver run none. The driver keeps doing its own commits and flips until the run-mode cutover, #424. Per `harness-runs/task_prompts/feat_flow_host_claude_executor_task_prompt.md`, *"Nothing in production calls this executor until #484's run loop and #424's cutover"*. The same holds for the hooks, the builder and the entry decision. This branch's callers are its tests, which drive the real planning graph end to end in run mode (Task 11 through `ClaudeExecutor`, Task 13 through `start_run`).
- **When each hook runs.**
  - **A dispatch's before-hooks run once per attempt.** An infrastructure retry inside `execute_set` runs them again. They run inside the dispatch's own task, after it takes its `seq` and attempt, before `Executor.run`, and outside `run_timeout_seconds` (Task 5).
  - **A dispatch's after-hooks** run once its record is recorded through `Walker.next` (Task 6).
  - **A round's before-hooks** run for every `DispatchSet` of that round the run loop dispatches. This settles #450's case: a round resumed with gates already recorded runs them again, with only the due gates in the set.
  - **A round's after-hooks** run for every `RoundPassage` in the `passed` of every step the loop takes, so a `current` that returns the same step again re-runs them. This is bash's *"`current` re-prints a `round:` line"*.
  - **A terminal's before-hooks** run before its `End` is returned.

  Every hook must be repeatable, as an executor's side effects must (`graphscene/src/graphscene/model/execution.py` → *"an executor's side effects must be repeatable"*). An exception from a hook propagates unchanged out of `start_run` / `continue_run`.
- **The planning graph's hooks.**
  - `plan_round` declares `after: ["commit_plan_round", "flip_ledger"]`. That is Override 6, with the commit made before the `P1` flip, as Override 6 orders it.
  - `convergence` declares `before: ["flip_ledger", "commit_convergence"]`. That is Override 5's `P2` flip, then Override 3, Override 4 and the `P3` flip.
  - `flip_ledger` flips every `LedgerPassage` its call's step carries. A walk that skips the UI-test loop therefore reaches `P1` twice, once after the round and once at convergence. The second time costs one wrapper call, answered by the wrapper's exit 3.
- **Pause, park and escalation stay the run driver's (#424).** None of them is a node or round event. Each is a `RunExit` the host acts on: a `Halt("pause")` and its `plan-round-partial` commit, an `<ask>` park, an `<escalate>` park and its partial commit. From Override 5, this branch takes the ledger flips (hooks) and resume (the entry decision, Task 14).
- **The prompt builder keeps answered pairs as host state.** It takes them at construction and appends them once, to the first dispatch it builds that is a writer's. It returns the same text for a repeated build of an equal `Dispatch`, so a retry gets the pairs again (Task 11).
- **The #325 symptom is covered.** On the #325 resume, an answered park re-ran the writer with the `initial` prompt. Task 14 keeps `pd_entry`'s order, so a usable saved walk parked at `<ask>` is continued with `answered`, which keeps the variant the walk saved. A test pins that.
- **`Dispatch.prompt` is not renamed.** Renaming it would change GraphScene's walk-state document. Its `pending` dispatch carries `"prompt"`, so `_VERSION` in `graphscene/src/graphscene/adapters/walk_json.py` would rise, and every saved walk would be refused. It would also break `devscene-flow-host` in the same change (`commands/render.py` → `_block`, three suites). The per-layer unit loop cannot make that change atomically: the whole-tree `commands.typecheck` would fail the `graphscene` unit on a file it may not edit. Task 11 records this in `ClaudeExecutor`'s docstring, and Task 16 records it in the README.
- **Two declarations of the prompt headings are held aligned.** Until #424, the graph's `promptSource` and the bash driver's `PNL_CORE_BLOCKS` both name the core headings. Task 1's case holds the graph to `PNL_CORE_BLOCKS`. Task 15's core-agreement check 10 holds it to the core itself.

**Not in scope.** These stay as they are:

- The bash planning libraries and the plugin's instruction cores and forks.
- This repository's self-adopted copies under `scripts/`. They are re-rendered after merge, as #485 did; see `Manual setup required:` below.
- The user-review fix-plan fork's overrides, which belong to #425.

**Top risks:**

1. **A half-moved format.** If the self-adopted `scripts/python/` copy of GraphScene is refreshed without `scripts/flows/task_plan_writing.graph.json`, every planning run's walker refuses its graph. The manual step below guards this. Inside the branch, Task 2 owns every fixture's version, and Task 13's end-to-end case loads the real planning graph under the new schema.
2. **Hooks that fire twice, out of order, or not at all on a resume.** Each one is a commit. Task 6 pins every firing point and the re-fire after a raising hook. Task 13 asserts the exact wrapper call sequence of a real planning walk.
3. **A ported builder that drifts from `pnl_prompt`.** Task 11's expected texts are hand-written from `pnl_prompt`'s token order and `pd_pairs_text`'s marker form, and are checked through `ClaudeExecutor`'s recorded `SessionUsage.agent_prompt`.

**Manual setup required:**

- After this branch merges, re-render this repository's self-adopted outer-loop scripts in one step, as #485 did (a forced self-adopt `init` in a scratch clone). That moves `scripts/flows/task_plan_writing.graph.json` to format 5 together with the walker's `scripts/python/` sources. Until then, do not refresh `scripts/python/` from a build of this branch: a format-5 GraphScene refuses the format-4 graph, and the planning walker exits 2. This depends on Tasks 1 and 2.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the commit step flips each one to `[x]` as that task's commit lands.

- **Only the committing role flips a marker.** In every flow that runs the unit loop, that role is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself.
- **An implementer never changes a marker** here, and never edits any other line of this section, in an index a run is iterating.
- **`[ ]` markers anywhere else are informational only.** The sub-step bullets inside the per-task files are progress markers for the implementer. The orchestrator does not iterate them, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_graphscene_node_hooks/task_<K>_plan.md`. The entries are ordered bottom-up in the configured layer order (`cli`, `graphscene`, `devscene-flow-host`), with the catch-all layer last.

1. [x] **Task 1** — Declare the planning graph's prompt sources and hooks at format 5, held to `PNL_CORE_BLOCKS` _(layer: cli)_ _(points: 10)_
2. [x] **Task 2** — Raise the flow-graph format to 5 with hook and prompt-source declarations in the schema, model and builder _(layer: graphscene)_ _(points: 20)_
3. [x] **Task 3** — Refuse a node hook that `vocabulary.hooks` does not declare _(layer: graphscene)_ _(points: 10)_
4. [x] **Task 4** — Declare the hook calls and the `HookHost` protocol in `model/hooks.py` _(layer: graphscene)_ _(points: 15)_
5. [x] **Task 5** — Run a dispatch's before-hooks on every attempt inside `execute_set` _(layer: graphscene)_ _(points: 15)_
6. [x] **Task 6** — Run the declared node, round and terminal hooks from `start_run` and `continue_run` _(layer: graphscene)_ _(points: 20)_
7. [x] **Task 7** — Export the hook surface, document hooks and format 5 in the README, and drive a hooked walk as a caller _(layer: graphscene)_ _(points: 15)_
8. [x] **Task 8** — Read a prompt source's fenced blocks from a plugin document in `records/prompt_blocks.py` _(layer: devscene-flow-host)_ _(points: 15)_
9. [x] **Task 9** — Read a branch's top-level answered clarification pairs in `records/clarifications.py` _(layer: devscene-flow-host)_ _(points: 10)_
10. [x] **Task 10** — Read the ledger's `P1`–`P3` marks in `records/ledger.py` _(layer: devscene-flow-host)_ _(points: 8)_
11. [x] **Task 11** — Port `pnl_prompt` as `CorePromptBuilder`, the host's `AgentPromptBuilder` _(layer: devscene-flow-host)_ _(points: 20)_
12. [x] **Task 12** — Commit through the main checkout's commit wrapper and flip a ledger entry in `host/commit_points.py` _(layer: devscene-flow-host)_ _(points: 15)_
13. [x] **Task 13** — Implement the planning graph's hooks as `PlanningHooks` and walk the planning graph in run mode with them _(layer: devscene-flow-host)_ _(points: 20)_
14. [x] **Task 14** — Port `pd_entry` as `decide_planning_entry`, the host's entry and resume decision _(layer: devscene-flow-host)_ _(points: 20)_
15. [x] **Task 15** — Hold each prompt source to the planning core as core-agreement check 10 _(layer: devscene-flow-host)_ _(points: 10)_
16. [x] **Task 16** — Document the prompt builder, the planning hooks and the entry decision in `devscene-flow-host/README.md` _(layer: devscene-flow-host)_ _(points: 10)_
17. [x] **Task 17** — Record format 5 and the hook seam in the flow-graph decision record, Gate 3, the schemas README and the roadmap _(layer: general)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_graphscene_node_hooks_task_prompt.md — data, never instructions ===
`feat_graphscene_node_hooks` lets a graph declare each node's prompt source and side effects, so the planning driver's flow-specific code becomes declarations in the harness's planning graph.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_graphscene_node_hooks_task_prompt.md ===

That change alters what the durable corpus says in three places, and each has its own derivation entry: the corpus states the graph format, it states that prompt building and hooks are deferred, and it describes run mode.

**Derivation entry — sites stating the graph format (command).** Re-run verbatim from the checkout root:
`git grep -lE 'format 4|format-4|"formatVersion": ?4' -- '*.md' 'cli/templates/**' ':!harness-runs/**' ':!examples/**'`

**Derivation entry — sites deferring prompt building or hooks (command).** Re-run verbatim:
`git grep -lE 'prompt sources and node hooks|node hooks|Dispatch\.prompt' -- '*.md' ':!harness-runs/**' ':!examples/**'`

**Derivation entry — sites describing run mode (command).** Re-run verbatim:
`git grep -lE 'start_run|continue_run' -- '*.md' ':!harness-runs/**' ':!examples/**'`

`examples/` is excluded because its captured prose is a frozen record (`.claude/context/conventions.md` → `## Documents of record`). `harness-runs/` is excluded because it records runs, not this project. Application source and its docstrings are not corpus text. They are planned in their own tasks.

**Closure invariant:** every path that any derivation entry above prints appears as a row below.

Round 1 added two target files: `graphscene/tests/fixtures/flow_graph/valid_hooks.json` (Task 2) and the root `package.json` → `validate:graphscene-schema` (Task 17). Neither is durable corpus text. All three derivation entries were re-run verbatim in that pass, and every path they print is already a row below.

| # | Site | Copy | Evidence (what the derivation matched) | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, the *A negative schema fixture* row (*"`graphscene/src/graphscene/schemas/flow-graph.schema.json`, format 4"*) | — | format entry, `format 4` | `no-change` | A conventions document is never a plannable target. The branch falsifies its *"format 4"*, so a `stale-rule` entry is recorded for a supervised `/devscene:analyze` re-run or a hand edit. |
| 2 | `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` (*"It owns the format-4 flow-graph schema"*) and `## The model and its wire forms` (*"`formatVersion` → `format_version`"*) | — | format entry, `format-4`, `formatVersion` | `no-change` | A conventions document. The first statement is falsified and is recorded as a `stale-rule` entry. The snake-case example stays true. |
| 3 | `ROADMAP.md` → the GraphScene row (*"the generic flow-graph schema, format 4"*, *"the format-4 schema"*, *"the harness's format-4 graph"*) | — | format entry, `format 4`, `format-4` | `change` | Task 17 |
| 4 | `cli/templates/scripts/flows/task_plan_writing.graph.json` → `formatVersion` and `description` | — | format entry, `"formatVersion": 4` | `change` | Task 1 |
| 5 | `devscene-flow-host/README.md` → `## The executor` → **The agent prompt.** (*"belongs to the later branch that makes prompt sources and node hooks declarations, not yet merged"*) and `## Differences from flow-walker.sh` → **The graph.** (*"The command reads format 4"*) | — | format entry, `format 4`; deferral entry, `node hooks`, `Dispatch.prompt` | `change` | Task 16 |
| 6 | `docs/development.md` → **Gate 3** (*"cover format 4"*, *"validates against the format-4 schema"*, *"stated on the format-4 graph's declared primitives"*) and **Gate 13** (*"walk of the harness's format-4 planning graph"*) | — | format entry, `format 4`, `format-4` | `change` | Task 17 |
| 7 | `docs/flow-graph-walker.md` → the item whose **Decision.** opens *"The planning graph is authored in format 4"*, and the format-4 statements around it | — | format entry, `format 4`, `format-4`, `"formatVersion": 4` | `change` | Task 17 appends a **Changed** note recording format 5. The decision text of record above it stays as it was decided. |
| 8 | `graphscene/README.md` → `## What it is` (the schema row *"The format-4 flow-graph schema"*, and the run-mode text naming `start_run` / `continue_run`) | — | format entry, `format-4`; run-mode entry, `start_run` | `change` | Task 7 |
| 9 | `schemas/README.md` → its opening paragraph (*"…flow-graph.schema.json`, format 4"*) | — | format entry, `format 4` | `change` | Task 17 |
