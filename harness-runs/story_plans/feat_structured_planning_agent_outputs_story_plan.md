# Story: A declared, validated return for the six planning agents, read the same way by both drivers

## Context

This branch gives the six agents the planning graph dispatches — `task-plan-writer`, `task-plan-reviewer`, `architecture-reviewer`, `business-parity-reviewer`, `ui-tests-plan-writer` and `ui-tests-plan-reviewer` — one declared return schema each, and makes every caller of those returns read and check the same return: the orchestrating session's `Agent` dispatches, in every mode and every flow each agent runs in, and the planning driver's headless node sessions. It is the first half of `ROADMAP.md` → the `Structured agent outputs` row; `feat_structured_outputs_remaining_agents` (#380) applies the same mechanism to the other 17 agents afterwards, so the mechanism is settled here and documented where that branch will read it. No other agent's return changes.

**Why the driver needs it.** The task prompt's `## Measured, 2026-11-16, Claude Code 2.1.325` section records that a session launched with `--agent` ignores `--json-schema`: its `result` event carries no `structured_output`, and `result` is the agent's own prose reply, ending, for `task-plan-writer`, in its fenced `story_file:` … block. Today `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ` (rule 5) reads `structured_output`, else `result` parsed whole as JSON, so every real node would be an infrastructure `error`, retried three times and parked.

**The settled design.** The prompt's proposals are settled as follows; Task 14 records each decision with its reason and cost in `docs/structured-agent-returns.md`.

1. **Return shape — one fenced JSON block, last.** An agent's reply ends with its **return object**: one fenced code block whose info string is `json`, holding one JSON object, with nothing but whitespace after its closing fence. Prose may sit above it. Chosen over "the whole reply is JSON" because the measured `result` text of a node session is the agent's final reply verbatim, fences included (the prompt's fourth table row), so jq 1.5 can take the block with `split` alone (no regex), and an orchestrating session reads a fenced block at the end of an `Agent` result as plainly as it reads today's fenced `key: value` block.
2. **Everything a caller routes or records on moves into the object.** `## Questions`, `## Corpus staleness`, `## Parity exclusions / deferrals` and `## Manual setup required` become fields (table below), so no caller parses a prose heading of these six returns. One section deliberately stays prose above the block: `## Unsolicited dispatch guidance`, whose wording and record are owned by `plugin/instructions/dispatch_discipline_instructions.md` across every graded agent, and whose "above the fenced block" placement stays true. The `verdict:` lines inside a round file or a review index are file content, not a return, and do not change.
3. **Where the schema lives — a `## Return schema` section of the agent's own definition.** One fenced `json` block, a JSON Schema (draft-07) restricted to a small dialect. Chosen over `schemas/<agent>.json` because the installed plugin carries only `plugin/`, so the driver can read the schema from the pinned plugin at run time; because the model sees its own schema in its own definition; and because the definition stays the one owner. The agent's `## Output contract` describes the schema in a `### Return fields` subsection (one bullet per field) and never restates it in another form.
4. **One discriminator: `outcome`.** Every variant carries `outcome` as a `const`. For these six agents the `outcome` values are exactly their planning-graph node's outcome keys minus `error`, which is never an agent's outcome: it is what a caller records for a return that keeps failing its check. So the graph stays the one owner of which outcomes a node may have, and a static check holds each schema to it.
5. **Validation on each path.** The driver validates the whole object against the agent's schema at reap time, in jq (Task 10). The orchestrating session cannot run a validator for free — a validator script would need a write per dispatch and an agent-invocable row with the permission entries that implies, and the prompt allows no new permission — so it applies the **routing check** `plugin/instructions/agent_return_contract.md` → `## Reading a return` defines: the block exists and is one object, its `outcome` is one the dispatching section routes on, and every field that section reads for that outcome is present and not empty. A caller names a field it reads in the citation form `` `<agent>.<field>` ``, which Task 13's suite holds to the agent's schema, so a renamed field fails a test rather than a run.
6. **A return that fails its check.** On the driver it is the existing infrastructure class: the node alone is re-dispatched, at most `PD_MAX_ATTEMPTS` (3) attempts, and only the last is recorded `error`. On the orchestrator path it is treated as a dispatch that did not return — nothing is recorded, the same dispatch goes out again through the safety contract — and the third consecutive failure takes the section's `error` route: `--outcome error` where the section passes outcomes to `flow-walker.sh`, `<escalate>` elsewhere. Same bound on both paths, never a guess, and every retry counts against `MAX_TOTAL_DISPATCHES`.
7. **`--json-schema` is dropped, with `pnl_schema`, `structured_output` reading and `harness_friction`.** A flag measured as not applied under `--agent` would be a second schema owner built from the graph; if a later Claude Code applied it, it would force the graph's decision shape over the agent's own. `harness_friction` existed only as that flag's schema description, which no agent session ever received and no agent contract asks for, so its observation path is removed rather than kept as dead code. The remote mention control (`cli/templates/scripts/remote-run.sh` → `control_mention_session`) runs without `--agent` and is untouched.

**The return contract — every field, per agent and outcome.** Producers (Tasks 2–5) declare exactly this; consumers (Tasks 6–13) read exactly this. Strings are non-empty; counts are integers.

| Agent | `outcome` | Required fields | Optional fields |
|---|---|---|---|
| `task-plan-writer` | `returned` | `story_file`, `task_files_dir`, `tasks_count` (≥ 1), `story_points_total` (≥ 0) | `parity_exclusions`, `corpus_staleness`, `manual_setup` — each an array of strings, one entry per item, a `corpus_staleness` entry opening with its type `stale-rule` or `undescribed-layer` |
| | `questions` | `questions` — an array of at least one string, one self-contained question per item, verbatim | — |
| | `blocker` | `blocker` — one line | — |
| `ui-tests-plan-writer` | `returned` | `ui_test_index`, `ui_test_files_dir`, `tests_count` (≥ 0) | — |
| | `no_ui` | `reason` — one line | — |
| | `questions` | `questions` | `ui_test_index`, `ui_test_files_dir`, `tests_count` — present when an augment wrote files before asking |
| | `blocker` | `blocker` | — |
| `task-plan-reviewer` | `PASS` | `findings_file` | — |
| | `FAIL` | `findings_file`, `must_fix_count` (≥ 1) | — |
| | `blocker` | `blocker` | — |
| `architecture-reviewer` | `PASS` | — | `findings_file` — present in plan-review sub-cases (a) and (b) |
| | `FAIL` | `findings_file`, `must_fix_count` (≥ 1) | — |
| | `blocker` | `blocker` | — |
| `business-parity-reviewer` | `PASS` | — | `findings_file` — present in plan-review mode; `reason` — the disabled-phase no-op only |
| | `FAIL` | `findings_file`, `must_fix_count` (≥ 1) | — |
| | `blocker` | `blocker` | — |
| `ui-tests-plan-reviewer` | `PASS` | — | — |
| | `FAIL` | `findings_file`, `must_fix_count` (≥ 1) | — |
| | `blocker` | `blocker` | — |

`findings_file` is the flat round file in plan-review mode and the review **index** in implemented-solution mode, as today. Every variant sets `additionalProperties: false`.

**Ship order is contract before consumer** (`.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent`). The schemas are a `plugin`-layer contract the `cli` driver reads at run time, and no single capability here is split across the two layers in the other direction, so the `plugin` tasks ship first (Task 1 the shared module; Tasks 2–5 the six agents; Tasks 6–9 every orchestrator-path caller), then the `cli` tasks (Tasks 10–13), then the catch-all `general` tasks last (Tasks 14–15), which document and register what the others built. Tasks 10–12 are one driver switch split for size: `planning-node-lib.sh` changes the keys `pnl_reap` prints in Task 10, and the driver suites `cli/test/planning-driver-walk.test.mjs`, `cli/test/planning-driver-control.test.mjs` and `cli/test/watcher-planning-driver.test.mjs`, whose stubs stand in for the agent sessions, are brought to the new return in Tasks 11 and 12; between those commits they are expected to fail, and the Run gates round grades the whole tree after Task 15.

**Constraints every task carries.** No new permission entry in any profile. Bash 3.2 and jq 1.5 floors for shell (no regex in jq, every jq `if` has an `else`), and no new runtime dependency for the outer loop. `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass — the Run gates round's to run, not a unit's. **No measured result is invented:** the prompt's table is the record for `--json-schema` under `--agent`, and anything else this change relies on about how Claude Code returns an `Agent` result or a `result` event is recorded as unmeasured with its hand step (Task 14). Every return-field and heading rename is a multi-file edit (`.claude/context/plugin.md` → `## Wires: dispatch in, return out`), so each plugin task closes on the grep that re-derives its readers.

**Top risks:** The first is a caller left reading a retired form — a `verdict: PASS` line, a `## Questions` heading, `no_ui: true` — of one of these six returns, in a mode nobody runs during the branch, which would strand that flow silently; Tasks 6–9 each close on a re-derivation grep, the `## Scope register` below enumerates every candidate file, and Task 13's suite fails on any `` `<agent>.<field>` `` citation the schema does not declare. The second is the driver and the orchestrator diverging on what a valid return is, or on what a failed one does; Task 1 states the rule once, Task 10 implements the driver's half against the same dialect, and Task 13 holds every schema to the dialect and to the planning graph's outcomes. The third is a stub that still emits the retired `structured_output`, so the driver suites pass against a return no real session produces (`<state_dir>/lessons.md` → *"When a check moves to reading a field one producer writes, the same change makes every path that stands in for that producer … write the field too."*); Tasks 11 and 12 rewrite every stub to emit only `result` text ending in the return block, built from the real agents' schemas where the stub copies the real agents.

**Manual setup required:** after this branch merges, this repository's self-adopted copies `scripts/lib/planning-node-lib.sh`, `scripts/lib/planning-driver-lib.sh` and `scripts/autonomous-watcher.sh` stay at the old bytes until a maintainer runs the forced self-adopt render `docs/development.md` describes (**Regenerating this repository's adoption after a `cli/templates/` change is one forced self-adopt run, read as a dry run first.**), the separate chore #377 and #382 set as precedent. No task in this plan depends on it, and an adopter's copies follow `init --force` as usual.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker to `[x]`**: the `committer` agent in every flow that dispatches one, and the orchestrator itself in the supervised flow, which dispatches none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside per-task files, are informational progress markers only. They are never the iteration source, and the committer never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_structured_planning_agent_outputs/task_<K>_plan.md`. The entries are ordered contract before consumer, as `## Context` states, with the catch-all layer last.

1. [x] **Task 1** — Add `plugin/instructions/agent_return_contract.md`, the one owner of the return block, the schema dialect, the field citation form and the routing check _(layer: plugin)_ _(points: 15)_
2. [x] **Task 2** — Give `task-plan-writer` a `## Return schema` and rewrite its `## Output contract` around it _(layer: plugin)_ _(points: 15)_
3. [x] **Task 3** — Give `ui-tests-plan-writer` a `## Return schema`, rewrite its `## Output contract`, and move the two planning writers' untrusted-input report into `questions` _(layer: plugin)_ _(points: 15)_
4. [x] **Task 4** — Give `task-plan-reviewer` and `ui-tests-plan-reviewer` a `## Return schema`, and restate the plan gates' return in `plan_review_rounds.md` _(layer: plugin)_ _(points: 15)_
5. [x] **Task 5** — Give `architecture-reviewer` and `business-parity-reviewer` a `## Return schema` covering every mode _(layer: plugin)_ _(points: 20)_
6. [x] **Task 6** — Read the six returns through the routing check in `task_plan_writing_instructions_core.md` _(layer: plugin)_ _(points: 15)_
7. [x] **Task 7** — Read the planning writers' return fields in the semi-autonomous and autonomous planning forks _(layer: plugin)_ _(points: 10)_
8. [ ] **Task 8** — Read the parity, architecture and plan-writer returns in the implementation core and its autonomous fork _(layer: plugin)_ _(points: 15)_
9. [ ] **Task 9** — Read the reviewers' and the UI-test writer's returns in the user-review fix-plan, user-review fix and QA flows _(layer: plugin)_ _(points: 15)_
10. [ ] **Task 10** — Drop `--json-schema` from `planning-node-lib.sh` and decide a node's outcome from its return block validated against the agent's `## Return schema` _(layer: cli)_ _(points: 20)_
11. [ ] **Task 11** — Read the validated return object in `planning-driver-lib.sh`, and bring the driver fixture's stub and suites to the return block _(layer: cli)_ _(points: 20)_
12. [ ] **Task 12** — Bring the watcher planning-driver suite's stub and the watcher's REPRO note to the return block _(layer: cli)_ _(points: 10)_
13. [ ] **Task 13** — Add `cli/test/agent-return-schemas.test.mjs`, the static check that holds every return schema to its contract, its dialect, the planning graph and every citation of its fields _(layer: cli)_ _(points: 20)_
14. [ ] **Task 14** — Record the mechanism in `docs/structured-agent-returns.md` and correct `docs/flow-graph-walker.md` → `## 5. The two drivers` _(layer: general)_ _(points: 15)_
15. [ ] **Task 15** — Update `docs/watcher.md`, `ARCHITECTURE.md` and `docs/analyze.md`, and register the new suite in `devscene.config.json` → `treeGuards` _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`## Scope: the planning agents, in every mode they run in`): *"An agent has one return contract, so each of the six changes in **all** its modes, and **every** caller that reads any of their returns changes with it, in this branch, wherever that caller sits. No other agent's return changes here."* The register also covers every corpus sentence that states how the planning driver reads a node's decision, because Task 10 changes it. The plan's other targets (`cli/templates/scripts/**`, `cli/test/**`, `devscene.config.json`) are source and configuration and owe no rows.

**Derivation entry A — plugin files naming one of the six agents (command).** Re-run verbatim from the checkout root:

```
git grep -lE '(task-plan-writer|task-plan-reviewer|architecture-reviewer|business-parity-reviewer|ui-tests-plan-writer|ui-tests-plan-reviewer)' -- plugin
```

**Derivation entry B — repository documents stating one of the six returns or the driver's read (command).** Re-run verbatim from the checkout root. It excludes `docs/work-report-research` and `docs/rag-extraction-research`, which are dated research records that describe the corpus as it stood when they were written and are read by no flow:

```
git grep -lE --all-match -e '(task-plan-writer|task-plan-reviewer|architecture-reviewer|business-parity-reviewer|ui-tests-plan-writer|ui-tests-plan-reviewer|planning-node-lib|planning driver)' -e '(verdict: (PASS|FAIL)|findings_file|must_fix_count|story_file|tasks_count|story_points_total|ui_test_index|ui_test_files_dir|tests_count|no_ui|## Questions|Corpus staleness|Parity exclusions|blocker:|structured_output|json-schema|decision object)' -- docs README.md ARCHITECTURE.md ROADMAP.md ':(exclude)docs/work-report-research' ':(exclude)docs/rag-extraction-research'
```

**Derivation entry C — conventions documents and adopter context templates stating the return wire (command).** Re-run verbatim from the checkout root:

```
git grep -lE '(key: value|verdict: (PASS|FAIL)|findings_file|structured_output|json-schema|## Questions)' -- .claude/context cli/templates/claude
```

**Derivation entry D — corpus files this plan creates (procedure).** **Artifact:** this plan's per-task files `task_1_plan.md` … `task_15_plan.md`. **Traversal:** each file's `### Targets` list, in task order, top to bottom. **Decision rule:** a target marked `(new)` whose path sits under `plugin/` or `docs/` is a row.

**Derivation entry E — standing-artifact rows (command).** Re-run verbatim from the checkout root: `grep -nE '^- .*(driver|producer|return)' harness-runs/lessons.md`. Each line it prints is one rule of the standing lessons ledger and one row. No other standing tracked matrix under `<state_dir>` covers any corpus target of this plan.

**Closure invariant:** every site each derivation entry reaches appears as a row below, and every row's site is reached by one of them.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/agents/README.txt` | — | A | `no-change` | Lists the agent files and their history; states no return field of any agent. |
| 2 | `plugin/agents/architecture-reviewer.md` → `## Invocation contract` (**Your return is parsed, not read.**), `## Read first` (**A cited path you cannot read…**), `## Output contract` | — | A | `change` | Task 5 |
| 3 | `plugin/agents/business-parity-reviewer.md` → the disabled-phase paragraph under the opening, `## Invocation contract`, `## Read first`, `## Output contract` | — | A | `change` | Task 5 |
| 4 | `plugin/agents/conventions-writer.md` → its citation of `task-plan-writer.md`'s conventions-document prohibition | — | A | `no-change` | Cites a `## Process` rule of the writer, not its return. |
| 5 | `plugin/agents/skeptic-reviewer.md` | — | A | `no-change` | Names the six only as sibling reviewers; its own `verdict:` return is not one of the six and is #380's. |
| 6 | `plugin/agents/task-plan-reviewer.md` → `## Invocation contract` (**Your return is parsed, not read.**), `## Read first`, `## What to check` → `### Architecture (Must Fix)` → **No task targets a conventions document**, `## Output contract` | — | A | `change` | Task 4 |
| 7 | `plugin/agents/task-plan-writer.md` → `## Invocation contract` (**How the caller consumes your return.**), `## Read first (everything — the plan spans every layer)`, `## Process` steps 5 and 7, `## Clarification questions`, `## Output contract` | — | A | `change` | Task 2 |
| 8 | `plugin/agents/ui-tests-plan-reviewer.md` → `## Invocation contract`, `## Read first`, `## Process` step 0, `## Output contract` | — | A | `change` | Task 4 |
| 9 | `plugin/agents/ui-tests-plan-writer.md` → the phase-gate paragraph under the opening, `## Invocation contract`, `## Read first`, `## No-UI determination (do this FIRST, before enumerating tests)`, `## Process`, `## Quality checks before saving`, `## Clarification questions`, `## Output contract` | — | A | `change` | Task 3 |
| 10 | `plugin/commands/branch-implement-plan-semi-autonomous.md` | — | A | `no-change` | Describes Phases A1.5 and A2 and routes on no return field; the parse is `plan_orchestration_instructions_core.md`'s (row 23). |
| 11 | `plugin/commands/branch-implement-user-review-semi-autonomous.md` | — | A | `no-change` | Describes the phases; routes on no return field. |
| 12 | `plugin/commands/branch-qa-test.md` → step 4 ("after the `no_ui` gate") | — | A | `no-change` | `no_ui` stays the outcome's name, as the `outcome` value; the parse is `qa_test_instructions.md`'s (row 25). |
| 13 | `plugin/commands/branch-start-docs-autonomous.md` | — | A | `no-change` | Names the six only as agents the docs flow does not run. |
| 14 | `plugin/commands/branch-start-plan-semi-autonomous.md` | — | A | `no-change` | Describes the flow; the parse is the planning core's (row 28). |
| 15 | `plugin/commands/branch-start-plan.md` → step 9 | — | A | `no-change` | Dispatches `ui-tests-plan-writer` on explicit request and routes on no field of its return; the routing check binds a caller that routes. |
| 16 | `plugin/commands/branch-start-user-review-fix-plan.md` | — | A | `no-change` | Points at the fix-plan fork and core; its "live `## Questions` surface" is `user-review-fix-plan-writer`'s, outside this branch. |
| 17 | `plugin/docs/AUTONOMOUS_FLOW.md` → `## The wiring table` | — | A | `change` | Task 1 |
| 18 | `plugin/docs/AUTONOMOUS_FLOW_WHITEBOARD.md` | — | A | `no-change` | Draws `PASS`/`FAIL` edges, which keep those names as `outcome` values. |
| 19 | `plugin/instructions/README.md` | — | A | `no-change` | Describes the directory; lists no module and no return. |
| 20 | `plugin/instructions/autonomous_pause_and_ledger.md` → the `P2` / `E` / `R4` template lines | — | A | `no-change` | Names the `no_ui` and reviewer-`PASS` outcomes, which keep those names. |
| 21 | `plugin/instructions/dispatch_discipline_instructions.md` | — | A | `no-change` | Owns `## Unsolicited dispatch guidance`, which stays prose above the return block (`## Context` decision 2); "above the fenced block" stays true. |
| 22 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` → the `*g` flip, **Zero-finding rounds**, **The plan's corpus staleness is one of the observations.** | — | A | `change` | Task 8 |
| 23 | `plugin/instructions/plan_orchestration_instructions_core.md` → `### A1.5.1 Generate the parity review`, `### A2.1 Generate the architecture review`, `### G.2 Write and review the test fix plan` (**The architecture gate.**), `### D.2 Done summary` | — | A | `change` | Task 8 |
| 24 | `plugin/instructions/plan_review_rounds.md` → `## The round file` (the return lines) | — | A | `change` | Task 4 |
| 25 | `plugin/instructions/qa_test_instructions.md` → `### 1. Ensure a UI-test plan exists` step 4 | — | A | `change` | Task 9 |
| 26 | `plugin/instructions/run_mode_instructions.md` | — | A | `no-change` | Names the reviewers in its rosters and reads no return. |
| 27 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` → the `<ask>` row, `### \`<escalate>\` / \`<ask>\``, `### \`<terminal_handoff>\` — no approval gate`, the UI-test-plan commit override | — | A | `change` | Task 7 |
| 28 | `plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker`, `## Loop`, `## UI-test-plan write loop`, `## Convergence`, `## Stop conditions` | — | A | `change` | Task 6 |
| 29 | `plugin/instructions/task_plan_writing_instructions_semi_autonomous.md` → the `<escalate>` and `<ask>` rows, `### \`<terminal_handoff>\` — Present to user` | — | A | `change` | Task 7 |
| 30 | `plugin/instructions/unit_loop_core.md` | — | A | `no-change` | Names the six only in `## The test-run rule`'s roster; the `verdict:` / `findings_file:` lines it parses are `layer-reviewer`'s, #380's. |
| 31 | `plugin/instructions/untrusted_input.md` → `## Where a report goes`, the writers' row | — | A | `change` | Task 3 |
| 32 | `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` | — | A | `no-change` | Its `## Questions` triggers are `user-review-fix-plan-writer`'s; the gates' parse is the core's (row 33). |
| 33 | `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` → `## Flow` steps 7 and 8, and the round close | — | A | `change` | Task 9 |
| 34 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` → the `<ask>` row, `## Override L — commit the QA.0 UI-test plan augment (autonomous fork only)` → **Trigger.** | — | A | `change` | Task 9 |
| 35 | `plugin/instructions/user_review_fixes_instructions_core.md` → `### QA.0` step 2 | — | A | `change` | Task 9 |
| 36 | `plugin/instructions/user_review_fixes_instructions_semi_autonomous.md` → the `<ask>` row | — | A | `change` | Task 9 |
| 37 | `plugin/samples/sample_story/task_1_plan.md` | — | A | `no-change` | Names the writer and reviewer as the format's readers; carries no return. |
| 38 | `plugin/samples/sample_story/task_2_plan.md` | — | A | `no-change` | As row 37. |
| 39 | `plugin/samples/sample_story/task_3_plan.md` | — | A | `no-change` | As row 37. |
| 40 | `plugin/samples/sample_story_plan.md` | — | A | `no-change` | As row 37; its `## Scope register` cites the writer's `## Process`, not its return. |
| 41 | `plugin/samples/sample_task_plan.md` | — | A | `no-change` | As row 37. |
| 42 | `ARCHITECTURE.md` → the `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`, `pnl_launch` and `pnl_reap` row | — | B | `change` | Task 15 |
| 43 | `docs/analyze.md` → the **Any write under a repository's own `.claude/` tree is a supervised action** paragraph, its sentence naming the planner's `## Corpus staleness` return section | — | B | `change` | Task 15 |
| 44 | `docs/development.md` | — | B | `no-change` | Its `structured_output` / `--json-schema` hits are the remote mention session's, which runs without `--agent` and is unaffected. |
| 45 | `docs/flow-graph-walker.md` → `## 5. The two drivers` → `### How each runs a parallel round`, `### The schema-from-graph rule, and the \`init\` check`, `### Not yet measured, and the hand step that measures it` | — | B | `change` | Task 14 |
| 46 | `docs/sandbox-verification.md` → the `AP3` row | — | B | `no-change` | A dated run record of what a planner returned then; editing it falsifies the record. |
| 47 | `docs/second-runtime-port-decision.md` | — | B | `no-change` | A decision record of the flow's routing as it stood; the `FAIL` and questions edges it maps keep their names. |
| 48 | `docs/watcher.md` → **What parks or pauses the driver, and what it retries.**, **The planning driver's unmeasured facts** | — | B | `change` | Task 15 |
| 49 | `.claude/context/plugin.md` → `## Wires: dispatch in, return out`, the bullet "A return is a fenced block of `key: value` lines …" | — | C | `no-change` | A conventions document is never a plannable target. This branch falsifies the bullet for the six agents, so it is raised as a `stale-rule` entry in the writer's `## Corpus staleness` return. |
| 50 | `plugin/instructions/agent_return_contract.md` (new) | — | D | `change` | Task 1 |
| 51 | `docs/structured-agent-returns.md` (new) | — | D | `change` | Task 14 |
| 52 | `harness-runs/lessons.md` → *"When a check moves to reading a field one producer writes, …"* | — | E | `no-change` | The ledger is append-only and only the fix-plan writer appends; the rule binds Tasks 11 and 12 and holds as written. |
| 53 | `harness-runs/lessons.md` → *"An unattended driver retries a unit's infrastructure-class failure …"* | — | E | `no-change` | Append-only, as row 52; Task 10 classes a failed return as infrastructure, which the rule already covers. |
