# Story: Cut the flow walker over to GraphScene's Python walker and retire the bash walker

## Context

This branch makes `flow-walker.sh` a thin hand-off to `devscene-flow-host`'s compatibility command `devscene-flow-walker` (#465) for every caller: orchestrator sessions, the user-review fix flow's `check-round-file`, and the watcher's script-driven planning driver. The bash walker's body and its gate library `lib/flow-walker-gates.sh` are retired in the same branch, together with the suite that tested that library. Callers keep calling `bash <scripts_dir>/flow-walker.sh …` unchanged. The wire grammar is held where callers parse it: keys, their order, exit codes and actions. Every place the command answers differently is already listed in `devscene-flow-host/README.md` → `## Differences from flow-walker.sh`, and Task 7 moves exactly the suite cases it names.

**The hand-off (Task 1).** The launch line is fixed by #478: `UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv uv run --frozen --no-sync --no-cache --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker <verb> …`. It adds `--flows <scriptsDir>/flows` to `start`, `next` and `current` only. `--no-cache` is always passed: a `--no-sync` run needs no cache, and the sandbox refuses it (measured 2026-11-24, task prompt). The hand-off also does two things itself:
- **An unprovisioned checkout.** No `uv`, no environment, or no console script in it: exit 2 with one `flow-walker:` line naming `bash <scriptsDir>/flow-host-provision.sh`, to be run outside the sandbox.
- **A leftover bash state file.** For `start`, `next` and `current` it deletes a flat file at `<stateDir>/.flow_walker_state`. `current` then answers "no saved walk" (exit 1), and the orchestrator's `current` → exit 1 → `start` recovery (#464) starts fresh.

**What the hand-off executes is chosen by its own directory alone.** It reads no environment variable to choose the environment, the project or the sources (`<state_dir>/lessons.md` → `## Trust checks`), because the watcher's planning driver runs it outside the sandbox (Task 6). It reaches every layout name through one declared shell mirror, `HR_FLOW_HOST_*` in `lib/harness-run-lib.sh`. Task 3 declares those names there, `hr_flow_host_provision` reads them too, and Task 16 holds them equal to `cli/src/flowHost/layout.ts` and `provision.ts` → `ENV_MARKER_FILE`.

It sets `PYTHONPATH` on the launch to the shipped `devscene-flow-host` and `graphscene` sources beside it, replacing any inherited value. A run copy's environment is built from the main checkout's packages as wheels (#478), so this is what makes the code that runs the code `init` shipped. That is also how every `cli` suite runs the branch's own sources, as the task prompt's "after #478" decision requires:
- a fixture's shipped packages are copied from `cli/dist/python/`, which the build stages from this checkout;
- the test helper only links the fixture's `<scriptsDir>/python/.venv` to this checkout's provisioned environment (Task 2).

The format-4 graph now ships into `scriptsDir` beside the format-3 graph. The format-3 graph stays shipped, because `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read its node list. Retiring it is #459's.

**Settled here, as the task prompt leaves to this branch:**
- **`init` builds the walker's environment by default** in every run that is not `--dry-run` and not `--upgrade`, whether or not it can prompt. The question it used to ask is gone, because there is nothing left to ask. `--no-provision-python` opts out. `--provision-python` is still accepted as the explicit form of the default, so adopter scripts that pass it keep working. A run that cannot be prompted builds too: the walker is required, and an `init` that left no environment would leave a repository that cannot plan.
- **A test seam keeps the `cli` suite off the network.** `init` reads a probe variable owned by `cli/src/flowHost/provision.ts`, which the suite's isolated environment sets to `off`, following the `KEEP_AWAKE_LOCK_PROBE_ENV` precedent (Task 4).
- **`doctor`'s grades.** `uv` absent is a `fail`. An unprovisioned main-checkout environment stays a `warn`, because run copies build their own at `setup-worktree.sh` step 6. It becomes a `fail` where `execution.scriptDrivenPlanning` is on, because Task 6 makes the planning driver depend on the main checkout's environment (Task 5).
- **`hr_flow_host_provision` fails rather than skips.** No `uv` and no project both return 1 with `failed —` lines, so `setup-worktree.sh` step 6 fails the bootstrap (Task 3). Task 16 brings every suite that bootstraps or provisions to that outcome. Task 17 brings the bundle suites to the walker's directory.

**The trust rule behind Task 6.** The watcher's planning driver runs the walker outside the sandbox. Today it runs the run copy's `flow-walker.sh`, and after the cutover that would also execute the run copy's `<scriptsDir>/python/.venv`. `cli/src/generators/writeProtection.ts` leaves that environment writable *"since no unsandboxed step builds from it"*. Its rule is *"anything that runs outside the sandbox must not be writable from inside it"*. So Task 6 makes the driver run the **main checkout's** walker, whose script and environment that module already write-protects. Task 1's hand-off takes no environment variable that could point that call elsewhere.

**Not in this branch.** This repository's self-adopted copies under `scripts/` (`scripts/flow-walker.sh`, `scripts/lib/flow-walker-gates.sh`, `scripts/flows/`) are re-rendered by the user after merge (task prompt, *"a post-merge user step"*), so no task edits them. Gate 6a's filter (Task 12) matches both the flat file and the directory for that reason. No task changes a file under `.github/workflows/`, so the run never parks for a hand push. The per-call startup cost is measured **by hand, outside any headless session** (`<state_dir>/lessons.md` → *"A wall-clock figure in a document of record is never one a run measured inside its own session"*). Task 13 ships the measurement command and the slot, and the figure is a manual step.

Top risks:
- **A suite that still drives the bash walker, drives the Python one against main's code instead of the branch's, or still asserts a bootstrap or bundle outcome this branch changed.** Task 2 owns the one helper every walker-driving suite goes through, including the planning-driver, watcher and remote-run suites. Task 8 pins the hand-off's own contract. Tasks 16 and 17 move the provisioning, bootstrap and bundle suites.
- **A new unsandboxed execution path into a session-writable environment.** Task 6 guards it, and its verification shows the driver ignoring a run copy's own walker.
- **The `init` default turning every fixture `init` into a networked `uv sync`.** Task 4 guards it through the isolated-environment seam, and its suite asserts both the default and the seam.

Manual setup required:
- After merge, re-render this repository's self-adopted scripts (the self-adopt `init` re-render), so `scripts/flow-walker.sh` becomes the hand-off and `scripts/flows/task_plan_writing.v4.graph.json` lands. Depends on Tasks 1 and 3.
- After that re-render, on an idle machine and outside any headless session, run the measurement commands that `docs/flow-graph-walker.md` → the per-call startup section names, and record the figures, host and date in that section's slot. Depends on Task 13.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`.** In every flow that runs the unit loop, that role is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. So no implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_flow_walker_python_cutover/task_<K>_plan.md`. The entries are ordered bottom-up by ship sequence in the configured layer order, with the catch-all layer last. A task's number `K` is its identifier, not its position: the list's order is the ship order, and every `**Depends on:**` names a task listed above it.

1. [x] **Task 3** — Declare the flow host's layout names once in the gate library, carry one branch's walk files in the remote bundle, and fail provisioning without `uv` or a project _(layer: cli)_ _(points: 20)_
2. [x] **Task 4** — Make `init` build the walker's environment by default, with `--no-provision-python` to opt out _(layer: cli)_ _(points: 20)_
3. [x] **Task 1** — Hand `flow-walker.sh` to `devscene-flow-walker`, ship the format-4 graph and retire the gate library _(layer: cli)_ _(points: 20)_
4. [x] **Task 2** — Point the walker-driving test helpers at the Python walker over the branch's own sources _(layer: cli)_ _(points: 15)_
5. [x] **Task 16** — Bring the provisioning and bootstrap suites to failing provisioning, and hold the new layout mirror equal _(layer: cli)_ _(points: 20)_
6. [x] **Task 17** — Bring the bundle and shipped-set suites to the walker's directory and the new shipped set _(layer: cli)_ _(points: 20)_
7. [x] **Task 5** — Grade a missing `uv` as a `doctor` failure _(layer: cli)_ _(points: 15)_
8. [x] **Task 6** — Run the main checkout's walker from the unsandboxed planning driver _(layer: cli)_ _(points: 10)_
9. [x] **Task 7** — Move the `flow-walker*` cases that pinned the bash walker's behaviour _(layer: cli)_ _(points: 15)_
10. [x] **Task 8** — Add a suite for the hand-off's own contract _(layer: cli)_ _(points: 10)_
11. [x] **Task 9** — Describe the hand-off in the `cli` package's own READMEs _(layer: cli)_ _(points: 8)_
12. [x] **Task 10** — Name the format-4 graph as the planning loop's routing graph in the plugin _(layer: plugin)_ _(points: 8)_
13. [x] **Task 11** — Record the launch route and the retired bash walker in `devscene-flow-host` _(layer: devscene-flow-host)_ _(points: 10)_
14. [ ] **Task 12** — Widen gate 6a's walker-state filter to the per-branch directory _(layer: general)_ _(points: 8)_
15. [ ] **Task 13** — Rewrite the walker's decisions of record and ship the startup-cost measurement _(layer: general)_ _(points: 15)_
16. [ ] **Task 14** — Update the remote, sandbox and watcher documents for the walker's directory and shipped set _(layer: general)_ _(points: 10)_
17. [ ] **Task 15** — Document `init`'s default provisioning in `docs/cli.md` and the root README _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"The bash walker is retired in this branch once the `flow-walker*` suites pass against Python."* and *"The prose that describes the flat file goes with them: `docs/flow-graph-walker.md`'s state and lock *Decision.*s, `docs/remote-execution.md` → **The walker state.** and `cli/templates/scripts/README.md`."*

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root: `git grep -l -e 'flow-walker' -e 'flow_walker_state' -e 'provision-python' -e 'task_plan_writing\.graph\.json' -- '*.md' '*.txt' 'cli/templates/**' ':!cli/templates/**/*.sh' ':!harness-runs' ':!examples/notes-app/devscene'`

**Derivation entry — standing-artifact rows (procedure).** **Artifact:** `harness-runs/lessons.md`, the one standing ledger under `<state_dir>` that is graded against plans. **Traversal:** its `## ` topic headings in file order, then each one-line rule under each heading. **Decision rule:** a rule is reached when it names the flow walker, its state file, `init`'s provisioning flag or a file in this branch's target set. Walked for this plan: no rule is reached, so the entry contributes no row. No standing matrix under `<state_dir>` keys a check id to any target file here.

**Closure invariant:** every site either derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## Not determined` ("How a caller launches `devscene-flow-host` is decided but not built") and `## The layers` ("How a caller launches it is still open") | — | command entry, `flow-walker` | `no-change` | conventions document; this branch falsifies both sentences, recorded as `stale-rule` in `corpus_staleness` |
| 2 | `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` ("how a caller launches it is still its `## Not determined`") and `## Records, and which one is the truth` ("its docstring rule names that bash function") | — | command entry, `flow-walker` | `no-change` | conventions document; falsified by Tasks 1 and 11, recorded as `stale-rule` in `corpus_staleness` |
| 3 | `README.md` (`npx devscene init --provision-python`) | — | command entry, `provision-python` | `change` | Task 15 |
| 4 | `ROADMAP.md` (the #465 row: "`devscene-flow-walker`, `flow-walker.sh`'s compatibility command") | — | command entry, `flow-walker` | `no-change` | the record of a shipped item, which stays true of what #465 delivered |
| 5 | `cli/README.md` ("the flow walker (`flow-walker.sh`) and its gate library (`lib/flow-walker-gates.sh`)") | — | command entry, `flow-walker` | `change` | Task 9 |
| 6 | `cli/templates/claude/settings.autonomous.json` (comment: "the orchestrating session runs four of them, the flow walker `flow-walker.sh`") | — | command entry, `flow-walker` | `no-change` | still true: the session still runs `flow-walker.sh`, and its allow entry is unchanged |
| 7 | `cli/templates/scripts/README.md` (the walker, its gate library, `.flow_walker_state`, and "`flows/task_plan_writing.v4.graph.json` … is **not** written into `scriptsDir`") | — | command entry, `flow-walker` | `change` | Task 9 |
| 8 | `devscene-flow-host/README.md` → `## The command line` ("How an adopter launches it is #419's"), `## What it reads, answers and keeps` → **The walk.**, `## Differences from flow-walker.sh` | — | command entry, `flow-walker` | `change` | Task 11 |
| 9 | `docs/cli.md` (the `--provision-python` flag row, step 6, the post-plan provisioning paragraph) | — | command entry, `provision-python` | `change` | Task 15 |
| 10 | `docs/converging-plan-reviews.md` ("`cli/templates/scripts/flow-walker.sh` → the header's `STATE` paragraph") | — | command entry, `flow-walker` | `change` | Task 13, because Task 1 removes that header paragraph |
| 11 | `docs/development.md` → gate 6a paragraph ("drops `harness-runs/.flow_walker_state`, the flow walker's state file, which `scripts/flow-walker.sh`'s `STATE —` header calls …") | — | command entry, `flow_walker_state` | `change` | Task 12 |
| 12 | `docs/development.md` → **Gate 3** paragraphs (the format-3 graph `cli/templates/scripts/flows/task_plan_writing.graph.json` and its generation) | — | command entry, `task_plan_writing\.graph\.json` | `no-change` | the format-3 graph and its gate legs stay until #459 |
| 13 | `docs/flow-graph-walker.md` → Item 3a, Item 6, Item 8's lock sentence, Item 9, **The runtime — bash 3.2 and `jq` 1.5** | — | command entry, `flow-walker` | `change` | Task 13 |
| 14 | `docs/remote-execution.md` → **The walker state.** | — | command entry, `flow_walker_state` | `change` | Task 14 |
| 15 | `docs/sandbox-record.md` → residuals 4 and 5 (`.flow_walker_state` restored and copied as one file) | — | command entry, `flow_walker_state` | `change` | Task 14, because Task 3 changes what the restore and the write copy |
| 16 | `docs/sandbox-verification.md` (the script list measured: "…flow-walker.sh, …run-test-suite.sh") | — | command entry, `flow-walker` | `no-change` | a dated measurement record of what was run then |
| 17 | `docs/structured-agent-returns.md` (outcome keys "in `cli/templates/scripts/flows/task_plan_writing.graph.json`"; the `flow-walker.sh` error route) | — | command entry, `task_plan_writing\.graph\.json` | `no-change` | the format-3 graph is still generated from format 4 with the same outcome keys, and the error route is unchanged |
| 18 | `docs/watcher.md` (shipped-table rows `lib/flow-walker-gates.sh`, `flows/task_plan_writing.graph.json`, `flow-walker.sh`) | — | command entry, `flow-walker` | `change` | Task 14 |
| 19 | `docs/work-report-research/README.md` | — | command entry, `flow-walker` | `no-change` | research record ("Research only"); it describes what was true when it was written |
| 20 | `docs/work-report-research/_brief.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 21 | `docs/work-report-research/architecture-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 22 | `docs/work-report-research/business-parity-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 23 | `docs/work-report-research/review-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 24 | `docs/work-report-research/reviews/review-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 25 | `docs/work-report-research/reviews/task-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 26 | `docs/work-report-research/reviews/task-plan-writer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 27 | `docs/work-report-research/reviews/ui-tests-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 28 | `docs/work-report-research/reviews/ui-tests-plan-writer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 29 | `docs/work-report-research/task-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 30 | `docs/work-report-research/task-plan-writer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 31 | `docs/work-report-research/test-fix-plan-writer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 32 | `docs/work-report-research/ui-tests-plan-reviewer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 33 | `docs/work-report-research/ui-tests-plan-writer.md` | — | command entry, `flow-walker` | `no-change` | research record, as row 19 |
| 34 | `plugin/commands/branch-start-plan-autonomous.md` → `## Resolved values`, `<scripts_dir>` row ("`flow-walker.sh` with its graph `flows/task_plan_writing.graph.json`") | — | command entry, `task_plan_writing\.graph\.json` | `change` | Task 10 |
| 35 | `plugin/commands/branch-start-plan-semi-autonomous.md` → `## Resolved values`, `<scripts_dir>` row ("`flow-walker.sh` and `flows/task_plan_writing.graph.json` as the owners of the planning loop's routing and caps") | — | command entry, `task_plan_writing\.graph\.json` | `change` | Task 10 |
| 36 | `plugin/docs/AUTONOMOUS_FLOW.md` (the "Routing of the planning loop" row: "`flow-walker.sh` and `flows/task_plan_writing.graph.json` in `<scripts_dir>`") | — | command entry, `task_plan_writing\.graph\.json` | `change` | Task 10 |
| 37 | `plugin/instructions/agent_return_contract.md` ("`--outcome error` where that section passes outcomes to `flow-walker.sh`") | — | command entry, `flow-walker` | `no-change` | the call and its outcome are unchanged |
| 38 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` (the graph "walked by `<scripts_dir>/flow-walker.sh`"; the `current` re-issue) | — | command entry, `flow-walker` | `no-change` | the invocations and their meaning are unchanged |
| 39 | `plugin/instructions/task_plan_writing_instructions_core.md` (the three invocations; "A non-zero exit is a blocker"; "Do NOT edit `<state_dir>/.flow_walker_state`") | — | command entry, `flow-walker` | `no-change` | the invocations hold; the hand-off's unprovisioned refusal is an exit 2, which the existing blocker route covers; the state path is still the walker's |
| 40 | `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` (the `check-round-file` invocation) | — | command entry, `flow-walker` | `no-change` | the invocation and its exit 3 hold, and the hand-off passes no `--flows` to that verb |
| 41 | `schemas/README.md` (the format-3 graph, generated from format 4) | — | command entry, `task_plan_writing\.graph\.json` | `no-change` | the format-3 graph and its checker are #459's |
| 42 | `schemas/flow-graph-check/README.md` | — | command entry, `task_plan_writing\.graph\.json` | `no-change` | `scripts/check-flow-graph.sh` and the format-3 fixtures are #459's |
| 43 | `schemas/negative/README.md` | — | command entry, `task_plan_writing\.graph\.json` | `no-change` | the format-3 negatives are #459's |
