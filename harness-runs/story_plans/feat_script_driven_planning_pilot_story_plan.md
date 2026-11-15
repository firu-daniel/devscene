# Story: Script-driven planning pilot

## Context

This branch moves the autonomous planning walk out of the orchestrator session. A planning driver walks `cli/templates/scripts/flows/task_plan_writing.graph.json` through the existing `cli/templates/scripts/flow-walker.sh` and runs every node as its own headless session, launched concurrently when the walker prints a round's set. The pilot is opt-in and off by default; with it off nothing the orchestrated path runs changes. Comparing its cost with the orchestrated path, which decides whether the unit loop follows, is the follow-up named by `ROADMAP.md` → the `Script-driven planning pilot` row (#159), not this branch.

**#370 has landed.** `git log` carries `e8ba4c28 feat: parallel plan reviews (#371)`. The graph is format 3 with `plan_round` carrying `"parallel": true`, and `docs/flow-graph-walker.md` → `### Item 8 — a round's gates fan out, and the round node joins` carries the parallel-round contract, including its closing **What a second driver must do.** paragraph. This branch's driver follows that paragraph and the walker header's `ROUNDS`, `OUTPUT`, `STATE`, `CONCURRENCY` and `EXIT CODES` blocks. It restates none of them.

**Verified: a session that never dispatched a planner arrives holding the run mode.** `plugin/instructions/plan_orchestration_instructions_core.md` → `## Setup` step 6 reads the run mode from the ledger's `## Run mode` block and says *"which is exactly how a session that never dispatched a planner arrives holding the run mode"*. So the engine session that runs after the driver needs no change.

**The shape: a watcher mode built from three sourced libraries.** The driver is not a standalone script. It is three libraries under `cli/templates/scripts/lib/`, sourced by `autonomous-watcher.sh` and called from `spawn_engine`'s launch subshell:
- `planning-node-lib.sh` (`pnl_*`, Task 1): one node session. It composes the prompt, builds the schema, launches the session, and reads and validates the result.
- `planning-record-lib.sh` (`prl_*`, Task 2): every durable write the orchestrator's autonomous fork makes today. That covers the commits of Overrides 3, 4 and 6, the ledger flips, the park question file, the pause files and the improvement observations.
- `planning-driver-lib.sh` (`pd_*`, Task 3): the walk itself, plus the safety contract applied per set.

The clarification channel's two index answers, the highest question index and the top-level answered pairs, keep one definition each. Task 10 ships first and moves them out of `autonomous-watcher.sh` into `lib/harness-run-lib.sh` as `hr_max_question_index` and `hr_top_level_answered_pairs`. `prl_park`, `pd_entry` and the watcher all call those, and the watcher archives at hand-off only the pairs the driver consumed (`PD_CONSUMED_SET`).

The driver's improvement-observation blocks are bracketed: an opening `# Script-driven planning — <time>` label and a closing `# Task run (Phase D)` label. So the task run's unlabelled Phase D entries, appended later, land under the closing label and never read as the driver's (Tasks 2, 4 and 7).

There are three reasons for this shape:
1. **One producer of the launch vector.** A node session must carry the watcher's own binary seam, `--settings` per-run profile, `--permission-mode`, `--model`, `--effort`, `--add-dir` list, scrubbed environment and main-checkout anchor. A watcher function, `session_exec` (Task 6), is the one producer of those flags for the engine session and every node session alike. A separate script would need all of them passed in and would become a second producer.
2. **No new reach for an agent.** The watcher is already withheld by the script-allowlist guard. A sourced library run directly only defines functions, as `lib/harness-run-lib.sh` does, so no new `DENY_SCRIPT_BASENAMES` entry is needed.
3. **The driver keeps the watcher's full environment.** It commits and pushes through the main checkout's `commit-on-branch.sh` and `push-branch.sh`, while each node session gets the scrubbed one.

**The switch is one watcher setting, `PLANNING_DRIVER_PLUGIN_DIR`.** It is an environment variable or a `watcher.env` line. Empty or unset means the pilot is off, which is the default. Set, it is both the switch and the plugin pin: every node session gets `--plugin-dir` set to that directory and names its agent with the scoped name `<plugin name>:<agent>`, the plugin name being read from that directory's `.claude-plugin/plugin.json`. A watcher setting rather than a configuration key, for two reasons:
- the lessons ledger requires a not-yet-measured seam to ship *"opt-in, off by default, behind an environment variable rather than a configuration key"*;
- the value is a path on one machine, which a committed `devscene.config.json` must never carry.

So the four-place configuration contract is not touched.

**The launch sequence when the pilot is on.** The pilot runs only in a local run of the task engine whose planning is not finished.
1. **Setup session.** The watcher first launches the task engine session as it does today, with one added launch-prompt clause carrying the literal `PLANNING IS SCRIPT-DRIVEN ON THIS LAUNCH`. On that clause, `/devscene:branch-start-plan-autonomous` (Task 7) does three things and then ends the session: it runs its steps 1–4 (kill switch, branch, task prompt, prompt-injection screen and run mode), creates or updates the flow-progress ledger with the run mode and the screened pairs, and emits `PLANNING HANDED TO SCRIPT: <branch>`. That keeps both judgement steps, reading a run mode and running the prompt-injection screen, in an agent session, and keeps the screen ahead of every reader of task data on every launch, resumes included.
2. **The driver.** The watcher then runs `pd_drive`.
3. **The engine session.** On the driver's hand-off, the watcher launches the task engine session again with no clause. It reads `P0`–`P3` resolved and falls straight through to implementation.

**The prompts come from the pinned plugin's own planning core.** The driver reads the dispatch blocks of `## Loop` and `## UI-test-plan write loop` out of `<PLANNING_DRIVER_PLUGIN_DIR>/instructions/task_plan_writing_instructions_core.md` at run time, as data. It reads `MAX_TOTAL_DISPATCHES = <n>` from the same file's `## Setup` step 4. A node's prompt is its dispatch block and nothing else: no `context_notes:` line and no `dispatch_additions/` record. Task 1 extracts the blocks, Task 5 holds the extraction against the real core, and Task 7 writes the one sentence in the core that says so.

**Outcomes come back structured, and the walker stays the only router.**
- **The schema.** Each node session runs with `--json-schema`, built by `jq` from that node's declared `outcomes` in the graph. It carries four keys: `outcome`, `findings_file`, `return` (the agent's return text, as its own `## Output contract` states it) and `harness_friction`.
- **Validation.** Only the driver's own `jq` check decides whether a result is valid. An outcome the node does not declare is `error`. So is a session with no `init` event, or one whose `init` tools do not match the agent file's `tools:` line.
- **Recording.** Outcomes are recorded with `flow-walker.sh next --node <node>` in the order sessions finish.

> Assumption: the closing `result` event of a `--output-format stream-json --verbose` session launched with `--json-schema` carries `structured_output` (with `.result | fromjson?` as the fallback, as `remote-run.sh` → `control_mention_session` reads it). The `init` event's `tools` under `--json-schema` is the agent's allowlist and nothing more. An installed copy of the plugin does not shadow the `--plugin-dir` copy when the agent is named by its scoped name. None of the three is measured on a real session. Tasks 1 and 5 pin the stub's shape. Task 8 records the three as not measured, beside the one by-hand session that measures them, listed under `Manual setup required:` below.

> Assumption: the remote job always runs the orchestrated path. `PLANNING_DRIVER_PLUGIN_DIR` is a local watcher setting that no `devscene-run.yml` `env:` block maps (`docs/remote-execution.md` → *"a tunable the watcher reads and that block does not map is not reachable from a repository variable"*). The watcher also ignores it in job mode. Task 8 states this per execution mode in `docs/watcher.md`.

> Assumption: `<escalate>` on this path is the headless park the autonomous fork's binding table gives it. The driver always writes the question file, because it has no judgement with which to apply `## Ask-vs-assume policy`. That is what "halts the run the way it does today" resolves to for a script.

> Assumption: the task prompt names the agent seam `HARNESS_AGENT_CLI`. The seam this tree ships is `${DEVSCENE_AGENT_CLI:-claude}` (`autonomous-watcher.sh` → `AGENT_CLI`), so every task uses that variable.

**Top risks:**
- **A node result read wrongly.** A missing init check, a guessed outcome, or a wrong `--findings` rule silently mis-routes the walk. Tasks 1 and 5 guard it with fixture cases, one per rejection rule.
- **Concurrency handled wrongly.** The danger is a set launched in part under the cap, a failed session cancelling its siblings, or one stalled session reading as the whole driver stalling. Task 3 owns these rules and Task 5's set cases assert them on the stub's recorded start and end times.
- **A resume that re-plans or repeats a commit.** Tasks 2, 3 and 6 keep the ledger the only durable record. Every commit goes through the wrapper's exit 3, and the answered pairs the driver consumed are archived before the second engine launch.

**Manual setup required:**
- To try the pilot, an operator sets `PLANNING_DRIVER_PLUGIN_DIR` to the plugin root in the machine-local `watcher.env` and bounces the daemon with `restart-watcher.sh`. Nothing in this branch needs it; with it unset every test and every run takes the orchestrated path.
- One real planning run with the switch on, from a terminal outside any agent session. It produces the three facts the first assumption above leaves unmeasured: where `structured_output` sits in the stream, the `init` tools under `--json-schema`, and whether an installed plugin copy shadows `--plugin-dir`. Task 8 writes the exact steps and records the facts as not measured until that run is taken. No task waits on it.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker to `[x]`**: the `committer` agent in every flow that dispatches one, and the orchestrator itself in the supervised flow, which dispatches none. No implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as the sub-step bullets inside the per-task files, are informational progress markers for the implementer. They are never the iteration source, and the committer never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_script_driven_planning_pilot/task_<K>_plan.md`, keyed by its **Task K**, not by its position: Task 10 was added in revision round 1 and ships first. The list is ordered bottom-up by ship sequence in the configured layer order (`cli`, `plugin`, then the catch-all `general`).

1. [x] **Task 10** — Move the clarification channel's two index scans into `lib/harness-run-lib.sh` as `hr_max_question_index` and `hr_top_level_answered_pairs` _(layer: cli)_ _(points: 15)_
2. [x] **Task 1** — Add `lib/planning-node-lib.sh`: one node session's prompt, schema, launch and validated result _(layer: cli)_ _(points: 20)_
3. [x] **Task 2** — Add `lib/planning-record-lib.sh`: the planning commits, ledger flips, park and pause files and improvement observations _(layer: cli)_ _(points: 20)_
4. [x] **Task 3** — Add `lib/planning-driver-lib.sh`: `pd_drive` walks the planning graph, runs each set concurrently and applies the safety contract per set _(layer: cli)_ _(points: 20)_
5. [x] **Task 4** — Ship the three planning libraries through `OUTER_LOOP_SCRIPTS`, name them in the two CLI READMEs, and name the driver as an intake writer in the two state-directory templates _(layer: cli)_ _(points: 15)_
6. [x] **Task 5** — Test the driver end to end with a stub agent CLI: walk, sets, held binding, park, STOP, PAUSE, cap and observations _(layer: cli)_ _(points: 20)_
7. [ ] **Task 6** — Wire the pilot into `autonomous-watcher.sh`: `PLANNING_DRIVER_PLUGIN_DIR`, `session_exec`, and the setup → driver → engine sequence _(layer: cli)_ _(points: 20)_
8. [ ] **Task 7** — Plugin side: the setup-only clause in the task engine command, the core's one-place note, and the observation intake's second writer _(layer: plugin)_ _(points: 15)_
9. [ ] **Task 8** — Document the two drivers in `docs/flow-graph-walker.md` and the pilot in `docs/watcher.md` _(layer: general)_ _(points: 15)_
10. [ ] **Task 9** — Add the node-session launch site to `ARCHITECTURE.md` §5 and the libraries to `docs/cli.md`'s outer-loop list _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt's `## Docs` section: *"`docs/flow-graph-walker.md`: the walker now has two drivers, which one runs when, and how each runs a parallel round. Each one follows the contract #370 wrote there."* / *"`docs/watcher.md` → `## 2. The scripts`: the new script."* / *"The planning core: say in one place that on the script-driven path it is not read, and that its dispatch blocks are the prompts' source."* This register applies those sentences to every durable corpus file whose statement the branch's work changes. That means every file that names who runs the planning walk, which outer-loop files ship, who writes the improvement-observations intake, which tunables the watcher reads, or how the engine session is launched.

**Derivation entry 1 — who runs the planning walk (command).** Re-run verbatim: `git grep -lE 'flow-walker\.sh' -- plugin docs ARCHITECTURE.md README.md ROADMAP.md cli/README.md cli/templates/scripts/README.md`

**Derivation entry 2 — the outer-loop file set (command).** Re-run verbatim: `git grep -lE 'lib/flow-walker-gates\.sh|flow walker with its gate library' -- plugin docs ARCHITECTURE.md README.md cli/README.md cli/templates/scripts/README.md`

**Derivation entry 3 — who writes the observations intake (command).** Re-run verbatim: `git grep -lE 'improvement_observations/<branch>' -- plugin docs ARCHITECTURE.md README.md cli/README.md cli/templates/state-dir`

**Derivation entry 4 — the watcher's tunables (command).** Re-run verbatim: `git grep -lE 'PARK_LOOP_MAX_CYCLES' -- plugin docs ARCHITECTURE.md README.md cli/README.md`

**Derivation entry 5 — how the engine session is launched (command).** Re-run verbatim: `git grep -lE 'spawn_engine' -- plugin docs ARCHITECTURE.md README.md`

No standing tracked artifact under `harness-runs/` carries rows that these targets fall under, so no procedure entry is owed.

**Closure invariant:** every file any of the five entries reaches appears as a row below. That is the property; there is no expected count.

| # | Site (path + symbol or quoted anchor) | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `docs/flow-graph-walker.md` → `### Item 4 — STOP, the counter and PAUSE stay orchestrator steps` and `### Item 8 …` → **What a second driver must do.** | — | entries 1, 2 | `change` | Task 8 |
| 2 | `docs/watcher.md` → `## 2. The scripts` table, and `## 4. Pausing, parking and the usage gate` → *"Its policy knobs, by name"* | — | entries 1, 2, 4, 5 | `change` | Task 8 |
| 3 | `cli/README.md` → the outer-loop shell-asset sentence (*"the flow walker (`flow-walker.sh`) and its gate library"*) | — | entries 1, 2 | `change` | Task 4 |
| 4 | `cli/templates/scripts/README.md` → *"The other family in this directory is not generated."* | — | entries 1, 2 | `change` | Task 4 |
| 5 | `docs/cli.md` → *"Two families land in `scriptsDir`, and only one of them is generated."* | — | entries 1, 2 | `change` | Task 9 |
| 6 | `ARCHITECTURE.md` → `## 5. Where the engine is reached — the launch path` (its derivation command reaches the node-session launch the driver adds) | — | entry 5 | `change` | Task 9 |
| 7 | `plugin/instructions/task_plan_writing_instructions_core.md` → its opening paragraphs | — | entry 1 | `change` | Task 7 |
| 8 | `plugin/commands/branch-start-plan-autonomous.md` → `## Steps` | — | entry 1 | `change` | Task 7 |
| 9 | `plugin/docs/AUTONOMOUS_FLOW.md` → the *"Routing of the planning loop"* table row, and *"Per-branch intake, human triage."* | — | entries 1, 3 | `change` | Task 7 |
| 10 | `plugin/instructions/improvement_observations_instructions.md` → `## Where it is written` (*"the file's first, unlabelled block is always the task run's"*) and `## Where it runs & the non-blocking rule` (*"When the branch's intake file **is** already tracked"*) | — | entry 3 | `change` | Task 7 |
| 11 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` → Overrides 2–6 | — | entry 1 | `no-change` | It stays the orchestrated path's text. The driver carries out the same overrides as code, and the engine command cites Override 5's two creation paragraphs by name without changing them. |
| 12 | `plugin/commands/branch-start-plan-semi-autonomous.md` → its `<scripts_dir>` row and step 3 | — | entry 1 | `no-change` | The semi-autonomous flow never takes the driver: the watcher launches only the autonomous task engine. |
| 13 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` → `Override I` | — | entry 3 | `no-change` | The orchestrator's own Phase D write is unchanged, as the task prompt requires. |
| 14 | `README.md` → *"The improvement ledger counts the harness's own defects"* | — | entry 3 | `no-change` | It says only that a run records its problems in one intake per branch, which still holds. |
| 15 | `docs/remote-execution.md` → the repository-variables table, and its `spawn_engine` mentions | — | entries 4, 5 | `no-change` | Its closing rule already makes an unmapped watcher tunable unreachable from a job, and the job's launch is unchanged. Task 8 states the per-mode answer in `docs/watcher.md`. |
| 16 | `docs/development.md` → its walker and `spawn_engine` mentions | — | entries 1, 5 | `no-change` | Measured records and gate history, true of what they measured. |
| 17 | `docs/sandbox-verification.md` → its walker, intake and `spawn_engine` mentions | — | entries 1, 3, 5 | `no-change` | Measured probe rows, true of the runs they record. |
| 18 | `docs/converging-plan-reviews.md` → its walker `STATE` citation | — | entry 1 | `no-change` | A decision record about counters, which the driver reads and does not change. |
| 19 | `docs/work-report-research/review-plan-reviewer.md` | — | entries 1, 2 | `no-change` | A research record of the corpus as it stood when it was taken. |
| 20 | `docs/work-report-research/reviews/review-plan-reviewer.md` | — | entries 1, 2 | `no-change` | A research record, as row 19. |
| 21 | `docs/work-report-research/reviews/task-plan-reviewer.md` | — | entry 1 | `no-change` | A research record, as row 19. |
| 22 | `docs/work-report-research/task-plan-reviewer.md` | — | entries 1, 2 | `no-change` | A research record, as row 19. |
| 23 | `docs/work-report-research/reviews/task-plan-writer.md` | — | entry 2 | `no-change` | A research record, as row 19. |
| 24 | `docs/work-report-research/reviews/ui-tests-plan-reviewer.md` | — | entry 2 | `no-change` | A research record, as row 19. |
| 25 | `docs/work-report-research/task-plan-writer.md` | — | entry 2 | `no-change` | A research record, as row 19. |
| 26 | `docs/work-report-research/ui-tests-plan-reviewer.md` | — | entry 2 | `no-change` | A research record, as row 19. |
| 27 | `cli/templates/state-dir/improvement_observations/README.md` → *"The first, unlabelled block is always the delivery run's."*, and the paragraphs opening *"Each block is written by the run's own orchestrator"* and *"The file is committed and pushed by the run itself"* | — | entry 3 | `change` | Task 4 |
| 28 | `cli/templates/state-dir/improvement_suggestions.md` → **How entries arrive.** (*"Each run writes exactly one intake file at `improvement_observations/<branch>.md`, once, at the end of the run"*) | — | entry 3 | `change` | Task 4 |
