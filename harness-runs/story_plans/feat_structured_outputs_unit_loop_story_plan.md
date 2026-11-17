# Story: Structured returns for the unit loop and Run gates agents

## Context

This branch is the second of five that give every plugin agent a declared, schema-validated return. It does this for the three agents of the unit loop and the Run gates phase: `layer-implementer`, `layer-reviewer` and `test-fix-plan-writer`. Each one gets a schema file `plugin/schemas/<agent>.return.json`, a `### Return fields` subsection and the canonical return-block sentence in its `## Output contract`. Every caller that routes on the return is moved onto the field-citation form `` `<agent>.<field>` `` and points at `plugin/instructions/agent_return_contract.md` → `## Reading a return` / `## A return that fails the check`. The mechanism is not re-decided here. The precondition holds: `docs/structured-agent-returns.md` records all three of `feat_structured_outputs_mechanism`'s decisions — `## Reading a return` step 1 on the measured `Agent` result shape (§3, the 2026-11-17 measurement), `### A list of structured items is an array of objects, one level deep`, and the heading *An agent's own `error:` return becomes an outcome, never `error`*. This plan found no point where the record and the task prompt disagree. `cli/test/agent-return-schemas.test.mjs` picks up each new schema file with no change to the suite.

**The outcomes, as the decision record fixes them.** No agent here is dispatched by the planning graph, so none is held to graph outcome keys.

- `layer-reviewer`: `PASS`, `FAIL` and `blocker`.
- `test-fix-plan-writer`: `returned`, `questions` and `blocker`. `questions` follows the `task-plan-writer` precedent: the former `## Questions` heading becomes a `questions` field.
- `layer-implementer`: `implemented`, `blocker`, `prohibited` and `already passing`. A transient stop halts the caller, so it becomes `blocker`. The two marked forms are non-halting. Under the record's rule *"The literal a caller matched before becomes the outcome value it routes on"*, they become the outcomes `prohibited` and `already passing`, with the cause in a `cause` field.

**Which of the implementer's seven report parts become fields.** The record's rule is *"Everything a caller routes or records on is a field."*

- Only part 7, *anything the orchestrator should flag to the user*, is read by a caller: the unit loop's step 6 appends each such line to the progress line. It becomes the array-of-strings field `flags`.
- Parts 1–6 stay as the numbered prose report above the block. That covers files, renames, the conventions evidence, the parity confirmations, the verification results and the plan deviations.
- No caller routes or records on parts 1–6. The orchestrator reads them and opens nothing (the two orchestration cores' context-discipline bullets). The commit wrapper derives the staged set itself, and the Done summary reads the commit record.
- So the object-item list form is not needed by this branch. The per-test verification results stay prose.

**The cause still matches the commit body.** The commit body's `record disposition of <token> — <cause>` / `mark <token> already passing — <cause>` line comes from the detail file's `**Cause:** ` line, which `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_record_cause` reads. `layer-implementer.md` already requires that line to be *the same text as* the cause in its return, and Task 2 moves that requirement onto `` `layer-implementer.cause` ``. No script reads an agent return, so no script changes. The `verdict:` lines, readiness lists and `**Cause:**` lines inside files an agent writes are file content and stay unchanged.

**Why an agent and its callers land in one task, and how the shared files are split.** The task prompt's constraint *"No caller is left reading a field its agent no longer returns, at the end of any task"* means each agent's schema, its definition and every caller of it must change together.

- Callers of different agents share five files: `plugin/instructions/unit_loop_core.md`, `plugin/instructions/plan_orchestration_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_core.md`, `plugin/instructions/user_review_fixes_instructions_autonomous.md` and `plugin/instructions/untrusted_input.md`.
- So each of those files is edited by more than one task. Each task owns named sections or named sentences in it, listed in its own file, and each later task `**Depends on:**` the earlier one: Task 1 → Task 2 → Task 3.
- No task edits a sentence another task owns.
- `plugin/instructions/agent_return_contract.md` is Task 1's alone. Task 1 adds `unit_loop_core.md` to its `## Who may cite this` roster, the only new citing document this branch creates. The other citing cores are already listed.

**What stays as it is.**

- The park name *"the `fixable: 0` park"* is kept wherever it names a kind of park rather than a parsed line: `### G.0 Resolve the round`, `### G.5 Re-run, and the round cap`, `cli/test/run-gates-park-answer.test.mjs` case (e), and the docs of record that measured it. Task 3 binds that name to the new field and leaves G.5 untouched.
- `## Unsolicited dispatch guidance` in `layer-reviewer.md` is the byte-identical block `plugin/instructions/dispatch_discipline_instructions.md` owns, and no task edits it.
- No permission, script, configuration key or measured fact is added. Everything the change relies on about the `Agent` result is already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured`.

**Top risks:**

- **A caller left reading the old prose form.** The literals are quoted across the corpus, so a missed sentence is a silent break. Each task's `Verification:` re-derives that agent's old return literals by grep across `plugin/`, and the `## Scope register` below closes the site set.
- **The returned `cause` drifting from the detail file's `**Cause:**` line,** which would break goal 3 for the commit body. Task 2 owns both sentences in `layer-implementer.md` and verifies they name the same field.
- **`cli/test/run-gates-park-answer.test.mjs` pins exact text.** It pins G.2's two prompt forms, the `Phase G test-fix-plan-writer` origin, the two prompt-form lines in the agent's `## Invocation contract`, and the `fixable: 0` literal in G.5's cap paragraph. Task 3 rewrites G.2's return parse and leaves every one of those strings byte-identical.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom, and the commit step flips each to `[x]` as that task's commit lands.

- **Only the committing role flips a marker.** That is the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker here, or edits any other line of this section, while a run is iterating this index.
- `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational only. The commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_structured_outputs_unit_loop/task_<K>_plan.md`.

1. [x] **Task 1** — Give `layer-reviewer` a schema-validated return and move the per-unit review step onto it _(layer: plugin)_ _(points: 20)_
2. [x] **Task 2** — Give `layer-implementer` a schema-validated return and move the unit loop and stop conditions onto it _(layer: plugin)_ _(points: 20)_
3. [x] **Task 3** — Give `test-fix-plan-writer` a schema-validated return and move Phase G onto it _(layer: plugin)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_structured_outputs_unit_loop_task_prompt.md` → `## The goal`, item 2): *"No caller parses these three agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`."*

**Derivation entry C1 — corpus files naming one of the three agents (command).** Re-run verbatim from the checkout root:
`git grep -lE 'layer-implementer|layer-reviewer|test-fix-plan-writer' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md'`

**Derivation entry C2 — corpus files carrying one of the three agents' old return literals (command).** Re-run verbatim from the checkout root:
`git grep -lE 'verdict: (PASS|FAIL)|must_fix_count|blocker: (prohibited|already passing)|(prohibited|already passing) — |fix_plan_file|fix_plan_dir|not_fixable|fixable: 0|pending — questions for user|item-7|Output contract. item 7' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md'`

Both pathspecs cover the plugin's Markdown and text, the adopter-facing templates, this repository's self-adopted copies of the state-directory READMEs, and the conventions documents. They leave out shell and TypeScript source and its comments, which are not corpus text.

**Derivation entry P1 — the files the task prompt names (procedure).**

- **Artifact:** the task prompt `harness-runs/task_prompts/feat_structured_outputs_unit_loop_task_prompt.md`.
- **Traversal:** its sections in file order (`## Why`, `## Scope: the agents and their current returns`, `## The goal`, `## Constraints`), and within each, every backticked repository path in order of appearance. The pattern `plugin/schemas/<agent>.return.json` is expanded once for each of the three agents `## Scope` names.
- **Decision rule:** a path is reached when it names durable corpus text: a plugin file, a document under `docs/`, a root prose document, or a schema file. A path to shell or TypeScript source, or to a test, is not reached.

**Derivation entry P2 — standing-artifact rows (procedure).**

- **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Artifact:** the lessons ledger.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when it sits under `## Agent prose`, or names an agent's return, a return schema or a shared instruction module.

**Closure invariant:** every site any of the four entries reaches appears as a row below. A site two entries reach is one row, and its `Evidence` cell names every entry that reached it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/schemas/layer-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 1 |
| 2 | `plugin/agents/layer-reviewer.md` | — | C1, C2 (`verdict: PASS`, `must_fix_count`) | `change` | Task 1 |
| 3 | `plugin/instructions/agent_return_contract.md` → `## Who may cite this` | — | P1, `## Why` | `change` | Task 1 — adds `unit_loop_core.md` |
| 4 | `plugin/instructions/unit_loop_core.md` | — | C1, C2 (`verdict: PASS`, `prohibited — `, `item 7`) | `change` | Task 1 (the per-unit review sections), Task 2 (the implementer sections) |
| 5 | `plugin/instructions/plan_orchestration_instructions_core.md` | — | C1, C2 (`must_fix_count`, `fixable: 0`, `pending — questions for user`) | `change` | Task 1 (the reviewers bullet and the review-loop stop bullet), Task 2 (the implementers bullet and the implementer stop bullet), Task 3 (G.0, G.2, G.3 and the `test-fix-plan-writer` stop bullets) |
| 6 | `plugin/instructions/user_review_fixes_instructions_core.md` | — | C1, C2 (`must_fix_count`, `already passing — `) | `change` | Task 1 (the reviewers bullet, the reviewer clause of the `<escalate>` row, the review-loop stop bullet), Task 2 (the implementers bullet, the implementer clause of the `<escalate>` row, the implementer stop bullet) |
| 7 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` → ``### `<escalate>` / `<ask>` — the park-and-yield clarification reroute`` | — | C1, C2 (`fixable: 0`) | `change` | Task 1 (the reviewer path), Task 2 (the implementer path), Task 3 (the G.2 planner path) |
| 8 | `plugin/instructions/untrusted_input.md` → `## Where a report goes` | — | C1, C2 (`item-7`, `item 7`) | `change` | Task 2 (the `layer-implementer` row), Task 3 (the `test-fix-plan-writer` placement) |
| 9 | `plugin/schemas/layer-implementer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 2 |
| 10 | `plugin/agents/layer-implementer.md` | — | C1, C2 (`blocker: prohibited`), P1 (`## Scope`) | `change` | Task 2 |
| 11 | `plugin/schemas/test-fix-plan-writer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 3 |
| 12 | `plugin/agents/test-fix-plan-writer.md` | — | C1, C2 (`fix_plan_file`, `not_fixable`) | `change` | Task 3 |
| 13 | `docs/structured-agent-returns.md` | — | P1, `## Why` | `no-change` | It already records the three decisions this branch adopts. The change relies on nothing it does not record as measured, so no `## 3.` entry is owed. |
| 14 | `ROADMAP.md` → the `Structured agent outputs` row | — | P1, `## Why` | `no-change` | The row stays open until the fifth branch of the series lands; this branch adopts the mechanism for three agents only |
| 15 | `.claude/context/plugin.md` → `## Wires: dispatch in, return out` | — | C1, C2 (`verdict: PASS`) | `no-change` | A conventions document, never a plannable target. This branch falsifies its *"A return is a fenced block of `key: value` lines"* rule, which cites exactly `layer-reviewer.md` and `layer-implementer.md`; that is recorded as a `stale-rule` entry in `corpus_staleness`. |
| 16 | `.claude/context/conventions.md` → `## Commit-message policy` | — | C2 (`already passing — `) | `no-change` | A conventions document; it states the commit-body record lines, which are unchanged |
| 17 | `cli/templates/claude/context/conventions.md` | — | C2 (`already passing — `) | `no-change` | It tells `/devscene:analyze` what to ask about commit-body record lines, which are file content of a commit, not a return |
| 18 | `cli/templates/state-dir/architecture_branch_review_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | It describes a folder the layer reviewer writes files into, not its return |
| 19 | `harness-runs/architecture_branch_review_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 20 | `cli/templates/state-dir/business_parity_branch_review_point_reviews/README.md` | `cli/templates` (no self-adopted copy: `phases.parity` is `false` here) | C1 | `no-change` | as row 18 |
| 21 | `cli/templates/state-dir/qa_review_point_reviews/README.md` | `cli/templates` (no self-adopted copy: `phases.qa` is `false` here) | C1 | `no-change` | as row 18 |
| 22 | `cli/templates/state-dir/review_plan_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | as row 18 |
| 23 | `harness-runs/review_plan_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 24 | `cli/templates/state-dir/skeptic_review_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | as row 18 |
| 25 | `harness-runs/skeptic_review_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 26 | `cli/templates/state-dir/task_plan_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | as row 18 |
| 27 | `harness-runs/task_plan_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 28 | `cli/templates/state-dir/test_fix_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | as row 18 |
| 29 | `harness-runs/test_fix_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 30 | `cli/templates/state-dir/user_review_fix_plan_point_reviews/README.md` | `cli/templates` | C1 | `no-change` | as row 18 |
| 31 | `harness-runs/user_review_fix_plan_point_reviews/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 18 |
| 32 | `cli/templates/state-dir/architecture_reviews/README.md` | `cli/templates` | C2 (`verdict: PASS`) | `no-change` | The `verdict:` line of another agent's round file — file content |
| 33 | `harness-runs/architecture_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 32 |
| 34 | `cli/templates/state-dir/architecture_user_review_reviews/README.md` | `cli/templates` | C2 | `no-change` | as row 32 |
| 35 | `harness-runs/architecture_user_review_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 32 |
| 36 | `cli/templates/state-dir/business_parity_reviews/README.md` | `cli/templates` (no self-adopted copy) | C2 | `no-change` | as row 32 |
| 37 | `cli/templates/state-dir/business_parity_user_review_reviews/README.md` | `cli/templates` (no self-adopted copy) | C2 | `no-change` | as row 32 |
| 38 | `cli/templates/state-dir/task_plan_reviews/README.md` | `cli/templates` | C2 | `no-change` | as row 32 |
| 39 | `harness-runs/task_plan_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 32 |
| 40 | `plugin/agents/README.txt` | — | C1 | `no-change` | A directory listing; it names `test-fix-plan-writer.md` as a file |
| 41 | `plugin/agents/architecture-reviewer.md` | — | C1, C2 | `no-change` | It names `test-fix-plan-writer` as the writer its sub-case (c) re-dispatches; its own return is already adopted |
| 42 | `plugin/agents/branch-reviewer.md` | — | C1 | `no-change` | It reads the layer reviewers' findings **files** in the per-unit folders, which is file content |
| 43 | `plugin/agents/business-parity-reviewer.md` | — | C1, C2 | `no-change` | Its own return is already adopted; it names the three agents only in roster or file-content contexts |
| 44 | `plugin/agents/docs-reviewer.md` | — | C2 | `no-change` | Its own `verdict:` return, adopted by `feat_structured_outputs_docs_qa` |
| 45 | `plugin/agents/qa-tester.md` | — | C1, C2 | `no-change` | Its own `verdict:` return, a later branch's; it names `layer-reviewer` only for a file-naming convention |
| 46 | `plugin/agents/review-plan-reviewer.md` | — | C2 | `no-change` | Its own return, adopted by `feat_structured_outputs_branch_review` |
| 47 | `plugin/agents/skeptic-reviewer.md` | — | C2 | `no-change` | as row 46 |
| 48 | `plugin/agents/task-plan-reviewer.md` | — | C2 | `no-change` | `verdict: FAIL` is its round-file content; its return is already adopted |
| 49 | `plugin/agents/ui-tests-plan-reviewer.md` | — | C2 | `no-change` | as row 48 |
| 50 | `plugin/agents/user-review-fix-plan-writer.md` | — | C2 | `no-change` | Its own `fix_plan_file:` / `## Questions` return, a later branch's |
| 51 | `plugin/commands/branch-implement-plan-semi-autonomous.md` | — | C1 | `no-change` | A summary (*"until the reviewer returns `PASS`"*) that names an outcome value and routes nothing; the routing is the cited `unit_loop_core.md`'s |
| 52 | `plugin/commands/branch-implement-user-review-semi-autonomous.md` | — | C1 | `no-change` | as row 51 |
| 53 | `plugin/commands/branch-start-docs-autonomous.md` | — | C1 | `no-change` | It states that `layer-reviewer` does not run in the docs flow |
| 54 | `plugin/docs/AUTONOMOUS_FLOW.md` | — | C1 | `no-change` | It names the agent files in its roster table and a heartbeat example; it parses no return |
| 55 | `plugin/instructions/README.md` | — | C1 | `no-change` | A directory description |
| 56 | `plugin/instructions/dispatch_discipline_instructions.md` | — | C1 | `no-change` | It lists `layer-reviewer` on the `## Unsolicited dispatch guidance` roster; *"above the fenced block"* stays true |
| 57 | `plugin/instructions/docs_orchestration_instructions_autonomous.md` | — | C1 | `no-change` | It names the agents as not run in the docs flow |
| 58 | `plugin/instructions/improvement_observations_instructions.md` | — | C1 | `no-change` | It reads the commit-body record lines, which are unchanged (the Context's goal 3 paragraph) |
| 59 | `plugin/instructions/mode_contract.md` | — | C1 | `no-change` | The `<per_unit_review>` binding's meaning, which is unchanged |
| 60 | `plugin/instructions/plan_orchestration_instructions.md` | — | C1 | `no-change` | The supervised flow dispatches `layer-implementer` and checks its output by reading it; it routes on no field of the return |
| 61 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` | — | C1, C2 | `no-change` | Its `verdict:` mentions are `review-plan-reviewer`'s and `skeptic-reviewer`'s; for `layer-reviewer` it binds `<per_unit_review>` `off` and names *"the verdict parse"* as a section of the cited loop, not a line |
| 62 | `plugin/instructions/plan_orchestration_instructions_semi_autonomous.md` | — | C1 | `no-change` | A `<per_unit_review>` binding only |
| 63 | `plugin/instructions/plan_review_rounds.md` | — | C2 | `no-change` | `verdict:` lines in a round file are file content |
| 64 | `plugin/instructions/qa_test_instructions.md` | — | C2 | `no-change` | `qa-tester`'s returns, a later branch's |
| 65 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` | — | C1 | `no-change` | It names the `Phase G test-fix-plan-writer` park origin, which is unchanged and pinned by `cli/test/run-gates-park-answer.test.mjs` case (c) |
| 66 | `plugin/instructions/user_review_fix_plan_writing_instructions.md` | — | C2 | `no-change` | `user-review-fix-plan-writer`'s return, a later branch's |
| 67 | `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` | — | C1, C2 | `no-change` | as row 66; its `test-fix-plan-writer` mention is the park origin, as row 65 |
| 68 | `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` | — | C2 | `no-change` | as row 66 |
| 69 | `plugin/instructions/user_review_fixes_instructions_semi_autonomous.md` | — | C1 | `no-change` | A `<per_unit_review>` binding only |
| 70 | `plugin/samples/sample_story_plan.md` | — | C1 | `no-change` | It cites `layer-implementer.md` → `## Working modes` for the readiness licence, which is unchanged |
| 71 | `plugin/samples/sample_task_plan.md` | — | C1 | `no-change` | as row 70 |
| 72 | `harness-runs/lessons.md` → *"State a new behaviour once, in the section that decides it, and cite it from everywhere else …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan. Each new route is stated once, in the unit loop or G.2, and the stop-condition lists and the closed reroute list name the case without restating its handling. |
| 73 | `harness-runs/lessons.md` → *"When an agent definition has to give back words to hold its word count, cut restatement or rationale …"* | — | P2, `## Agent prose` | `no-change` | It binds Tasks 1–3's agent edits, and no definition or edge case is dropped |
| 74 | `harness-runs/lessons.md` → *"Keep a machine-read contract the model never acts on, such as a JSON schema … in a plugin file outside the agent definition …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan: each schema lives in `plugin/schemas/`, never in the definition |
| 75 | `harness-runs/lessons.md` → *"A shared instruction module carries only what its runtime reader acts on …"* | — | P2, `## Agent prose` | `no-change` | It binds Task 1, which adds only a roster line to `agent_return_contract.md` |
