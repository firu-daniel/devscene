# Story: Structured returns for the docs and interactive-test agents, and every agent held to a schema

## Context

This branch is the last of five that give every plugin agent a declared, schema-validated return. It covers five agents: `qa-tester`, its two declared-but-unimplemented variants `qa-tester-mobile-maestro` and `qa-tester-mobile-mcp`, `docs-writer` and `docs-reviewer`. Each one gets three things:

- a schema file `plugin/schemas/<agent>.return.json` in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists;
- a `### Return fields` subsection;
- the canonical return-block sentence in its `## Output contract`.

Every caller that reads one of these returns moves onto the field-citation form `` `<agent>.<field>` `` and the outcome form "an `outcome` of `PASS`". Each caller that routes on a return points at `plugin/instructions/agent_return_contract.md` → `## Reading a return` and `## A return that fails the check`. Then `cli/test/agent-return-schemas.test.mjs` is changed to fail any agent definition with no schema file, and the decision record and `ROADMAP.md` close the work. The mechanism is not re-decided here.

**The precondition holds.** `plugin/agents/` holds 22 definitions and `plugin/schemas/` 17 schema files; the five agents without one are exactly this branch's five. `docs/structured-agent-returns.md` records all three of `feat_structured_outputs_mechanism`'s decisions, and `agent_return_contract.md` → `## A return that fails the check` already takes a route the dispatching section names as its own `error` route ahead of the fallbacks.

**Where the plan and the task prompt differ, and why.** The plan found no point where the decision record and the task prompt disagree. It differs from the prompt in two places, both read off the corpus:

- **The two mobile stubs have no dispatching caller today.** The prompt says *"the same callers dispatch whichever variant `qa.driver` names"*. `plugin/agents/README.txt` says otherwise — *"Flows dispatch `qa-tester` by name, so a dispatch always reaches `qa-tester.md`"* — and no instruction file names either stub as a dispatch target. So the stubs' schema is the `blocker` subset of `qa-tester`'s, with the same field name, and the callers Task 1 moves already route that outcome. Task 2 changes no caller of the stubs. It also rewrites the two semi-autonomous implement commands' *"1-3 line contract"* clause, which names no single agent.
- **The docs pair's disabled-phase return becomes its own outcome, `phase_disabled`.** The prompt describes `docs-reviewer`'s as *"`verdict: PASS` plus a one-line reason and no `findings_file:`"*. A schema's `outcome` consts must be distinct across variants, and `PASS` carries a required `findings_file`, so a disabled `PASS` cannot be a second variant. `docs-writer`'s disabled-phase `notes:`-only return takes the same outcome. Task 6 records the choice.

**The outcomes and fields.** None of these agents is dispatched by the planning graph, so none is held to graph outcome keys. Every name below is one token (`harness-runs/lessons.md` → `## Agent prose`).

- **`qa-tester`:**
  - `PASS`, with no other field;
  - `FAIL`, with `findings_file` and `must_fix_count` (integer, at least 0 — a Should Fix alone makes a FAIL);
  - `blocked`, with `blocked_tests` (array of objects, at least 1): each item `test_id` (integer, at least 1) and `cause`. This is the former `error: blocked — ` return, which every caller treats as non-halting. Per `docs/structured-agent-returns.md` → *An agent's own `error:` return becomes an outcome, never `error`*, *"The literal a caller matched before becomes the outcome value it routes on"*: `blocked`. An item list carries both the per-test mode (one item) and the full-run mode's *"tests <ids>: <causes>"* (one item per blocked test);
  - `blocker`, with `blocker`. This is the former unmarked `error:` return — the run cannot proceed and the caller halts.
- **`qa-tester-mobile-maestro`, `qa-tester-mobile-mcp`:** `blocker`, with `blocker`, and no other variant.
- **`docs-writer`:**
  - `written` (catalog and update modes), with `doc_path` and the optional `unverified`, `parity_gaps` and `notes` (arrays of strings, at least 1, omitted when empty);
  - `targets` (survey), with `targets` (array of objects, at least 1): each item `action` (`enum` `new` / `update`), `slug`, `output_path`, `reason` and `entry_hints`; plus the optional `notes`;
  - `targets_none` (survey, the former `targets: none`), with `reason` and the optional `notes`;
  - `phase_disabled`, with `reason`;
  - `blocker`, with `blocker`.
- **`docs-reviewer`:**
  - `PASS` and `FAIL`, each with `findings_file`, `summary` and the optional `missed_docs` (array of strings, at least 1; update mode only);
  - `phase_disabled`, with `reason`;
  - `blocker`, with `blocker`.

**How the callers route.** Each routing caller states its routes at its dispatch site and names its own `error` route, which `## A return that fails the check` takes after a third failing return:

- **QA (plan-orchestration Phase E, the user-review-fix flow's Phase QA, the supervised QA flow):** `blocked` is the per-test blocked arm (record each item, leave the test `[ ]`, continue); `blocker` and a third failing return halt — the old unmarked-`error:` arm. A blocked test is never a pass.
- **The docs phase (best-effort, never blocks):** a survey's `blocker`, `phase_disabled` or third failing return logs and ends the phase; a write's logs and skips that target; a review's commits the doc as-is and appends the slug to `needs_review.md`, as the fix cap does.
- **The docs catalog:** a writer's `blocker`, `phase_disabled` or third failing return halts the session with the entry's box left `[ ]`; a reviewer's records the slug in `needs_review.md` and commits the doc as-is, as the fix cap does.

**Why each agent and its callers land in one task, and how the shared files are split.** The constraint *"No caller is left reading a field its agent no longer returns, at the end of any task"* means each agent's schema, its definition and every caller of it change together. Tasks 3 and 4 share their callers, as the third branch's tasks did; each task owns named sentences in each shared file, listed in its own file, and no task edits a sentence another task owns:

- `plugin/instructions/docs_phase_instructions.md` and `plugin/instructions/docs_orchestration_instructions_autonomous.md` — Task 3 owns every `docs-writer` dispatch's return sentence, Task 4 every `docs-reviewer` one.
- `plugin/instructions/untrusted_input.md` → `## Where a report goes` — Task 3 owns the `docs-writer` row, Task 4 the `docs-reviewer` row.
- `plugin/instructions/agent_return_contract.md` → `## Who may cite this` — Task 3 alone adds both docs files.

Tasks 1 and 2 share no file. The opening *"Reviewers … return …"* bullet of both orchestration cores is Task 1's: after it, no agent any section dispatches returns `verdict:` lines.

**Why the `cli` task ships after the `plugin` tasks.** The configured layer order is `cli`, `plugin`, `general`. Task 5's new rule — every agent definition has a schema file — holds only once Tasks 1–4 have added the five, so a `cli` task shipped first would fail its own test. A task never depends on a later one, so the order here is plugin, cli, then the catch-all.

**New citers of the module.** `docs_phase_instructions.md` and `docs_orchestration_instructions_autonomous.md` (Task 3). The QA callers — `plan_orchestration_instructions_core.md`, `user_review_fixes_instructions_core.md` and `qa_test_instructions.md` — are already on the roster. The user-review-fix autonomous fork cites fields but does not point at the module: the core it runs does the check.

**What stays as it is.**

- The QA review index, its readiness list, the per-finding files `qa-tester` writes, the documentation `docs-writer` writes and the findings files `docs-reviewer` writes are file content and unchanged.
- The `## Output contract` → `### 3. A test blocked` and `### 4. The run cannot proceed` headings of `qa-tester.md` are cited by name and keep their text.
- No script reads any of these returns, so no script changes. No permission, configuration key or measured fact is added: everything the change relies on about the `Agent` result is already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured`.
- Per the ledger's breaking-rename rule, no caller keeps a fallback that reads the old `verdict:` / `error:` / `key: value` form.

**Top risks:**

- **A caller left reading the old prose form.** The literals are quoted across the corpus, so a missed sentence is a silent break. Each task's `Verification:` re-derives its agent's old literals by grep across `plugin/`, and the `## Scope register` below closes the site set.
- **`blocked` read as `blocker`.** The two outcomes differ by one letter and route opposite ways — continue versus halt. Task 1 states each route once, at each site, and its verification checks every site names both and that no site halts on `blocked`.
- **A shared docs sentence edited twice.** Tasks 3 and 4 each list the exact sentences they own in the two docs instruction files, so Task 4's edits never touch what Task 3 left, and `docs_orchestration_instructions_autonomous.md` keeps exactly one copy of the report literal `Untrusted instruction not followed — `.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom, and the commit step flips each to `[x]` as that task's commit lands.

- **Only the committing role flips a marker.** That is the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker here, or edits any other line of this section, while a run is iterating this index.
- `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational only. The commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_structured_outputs_docs_qa/task_<K>_plan.md`. Ordered by ship sequence, with the catch-all layer last; the `cli` task follows the `plugin` tasks it depends on, as `## Context` states.

1. [x] **Task 1** — Give `qa-tester` a schema-validated return with a non-halting `blocked` outcome and move Phase E, Phase QA and the supervised QA flow onto it _(layer: plugin)_ _(points: 20)_
2. [x] **Task 2** — Give the two mobile `qa-tester` stubs a `blocker`-only schema and an `## Output contract`, and retire the semi-autonomous commands' "1-3 line contract" _(layer: plugin)_ _(points: 12)_
3. [x] **Task 3** — Give `docs-writer` a schema-validated return and move the docs phase and the docs catalog onto it _(layer: plugin)_ _(points: 20)_
4. [ ] **Task 4** — Give `docs-reviewer` a schema-validated return and move the docs phase and the docs catalog onto it _(layer: plugin)_ _(points: 15)_
5. [ ] **Task 5** — Make the schema suite fail an agent definition with no return schema _(layer: cli)_ _(points: 10)_
6. [ ] **Task 6** — Record the five agents' outcomes in the decision record, state the every-agent rule, and close the roadmap row _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_structured_outputs_docs_qa_task_prompt.md` → `## The goal`, item 2): *"No caller parses these agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`."*

**Derivation entry C1 — corpus files naming one of the five agents (command).** Re-run verbatim from the checkout root:
`git grep -lE 'docs-writer|docs-reviewer|qa-tester' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md' 'docs/*.md' 'README.md' 'ARCHITECTURE.md' 'ROADMAP.md' 'CONTRIBUTING.md' ':(exclude)docs/work-report-research/*' ':(exclude)docs/rag-extraction-research/*'`

**Derivation entry C2 — corpus files carrying one of the five agents' old return literals (command).** Re-run verbatim from the checkout root:
``git grep -lE 'error: blocked|unmarked [^.]*error|run-level [^.]*error|targets: none|`targets:`|doc_path:|missed_docs:|parity_gaps:`|`notes:`|`summary:`|`blocker:`|Reviewers return 1 line|reads `verdict:` lines|blocked `error:`|`error:` / blocker|1-3 line contract' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md' 'docs/*.md' 'README.md' 'ARCHITECTURE.md' 'ROADMAP.md' 'CONTRIBUTING.md' ':(exclude)docs/work-report-research/*' ':(exclude)docs/rag-extraction-research/*'``

**Derivation entry C3 — the closing work's wording (command).** Re-run verbatim from the checkout root:
`git grep -nE 'one at a time|outside every check until|#380|remaining_agents|Structured agent outputs' -- docs/structured-agent-returns.md ROADMAP.md`

**What the command entries cover.** The plugin's Markdown and text, the adopter-facing templates, this repository's self-adopted state-directory READMEs, the conventions documents, `docs/` and the root prose documents. They leave out shell and TypeScript source and the test suites, which are not corpus text: no script reads any of the five returns (`git grep -nE 'docs-writer|docs-reviewer|qa-tester' -- cli/templates/scripts` finds only two comments in `autonomous-watcher.sh` about the docs flow's missing clarification channel). They leave out `docs/work-report-research/` and `docs/rag-extraction-research/`, research records of past studies that name these agents as subjects and route nothing.

**Derivation entry P1 — the files the task prompt names (procedure).**

- **Artifact:** the task prompt `harness-runs/task_prompts/feat_structured_outputs_docs_qa_task_prompt.md`.
- **Traversal:** its sections in file order (`## Why`, `## Scope: the agents and their current returns`, `## Closing the work`, `## The goal`, `## Constraints`), and within each, every backticked repository path in order of appearance. The pattern `plugin/schemas/<agent>.return.json` is expanded once for each of the five agents the opening paragraph names.
- **Decision rule:** a path is reached when it names durable corpus text: a plugin file, a document under `docs/`, a root prose document or a schema file. A path to shell or TypeScript source, or to a test, is not reached.

**Derivation entry P2 — standing-artifact rows (procedure).**

- **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Artifact:** the lessons ledger.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when it sits under `## Agent prose`, or names a rename, an agent's return or an outcome.

**Closure invariant:** every site any of the five entries reaches appears as a row below. A site two entries reach is one row, and its `Evidence` cell names every entry that reached it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/schemas/qa-tester.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 1 |
| 2 | `plugin/agents/qa-tester.md` | — | C1, C2 (`error: blocked`, `run-level`) | `change` | Task 1 |
| 3 | `plugin/instructions/plan_orchestration_instructions_core.md` | — | C1, C2 (`reads `verdict:` lines`, `error: blocked`, `unmarked`) | `change` | Task 1 (the opening *"Reviewers end in a return object …"* bullet, the `<qa_review_path>` paragraph's *"per-dispatch `findings_file:` returns"* parenthesis, `### E.1`'s collect and mark-pass paragraphs and its credentials paragraph's blocked clause, `### E.2`'s four arms, `### D.2`'s **QA** bullet's blocked clause, the `## Stop conditions` `qa-tester` bullet) |
| 4 | `plugin/instructions/qa_test_instructions.md` | — | C1, C2 (`error: blocked`, `unmarked`) | `change` | Task 1 |
| 5 | `plugin/instructions/user_review_fixes_instructions_core.md` | — | C1, C2 (`Reviewers return 1 line`, `error: blocked`, `unmarked`) | `change` | Task 1 (the opening *"Reviewers return 1 line …"* bullet, the `<escalate>` binding row's *"an unmarked per-test `qa-tester` `error:`"* clause, the `## Phase QA` lead note's *"the `verdict: FAIL` → commit-the-QA-review-then-fix-loop sequence"*, `### QA.1+`'s mark-pass clause and round-PASS sentence, `### D.2`'s **QA** bullet's blocked clause, the `## Stop conditions` `qa-tester` bullet) |
| 6 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` | — | C1, C2 (`unmarked`) | `change` | Task 1 (the closed list's `qa-tester` clause) |
| 7 | `plugin/schemas/qa-tester-mobile-maestro.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 2 |
| 8 | `plugin/schemas/qa-tester-mobile-mcp.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 2 |
| 9 | `plugin/agents/qa-tester-mobile-maestro.md` | — | C1, C2 (`run-level`) | `change` | Task 2 |
| 10 | `plugin/agents/qa-tester-mobile-mcp.md` | — | C1, C2 (`run-level`) | `change` | Task 2 |
| 11 | `plugin/agents/README.txt` | — | C1, C2 (`blocked `error:``, `` `error:` / blocker ``) | `change` | Task 2 (the interactive-test paragraph's two return clauses, and the report-don't-substitute paragraph's return clause) |
| 12 | `plugin/schemas/docs-writer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 3 |
| 13 | `plugin/agents/docs-writer.md` | — | C1, C2 (`` `targets:` ``, `targets: none`, `doc_path:`, `` `notes:` ``, `parity_gaps:`) | `change` | Task 3 |
| 14 | `plugin/instructions/docs_phase_instructions.md` | — | C1, C2 (`` `targets:` ``, `missed_docs:`) | `change` | Task 3 (`## Loop` step 1, step 2's **Write** bullet, step 3), Task 4 (step 2's **Review**, **Fix loop** and **Missed-doc ripple** bullets) |
| 15 | `plugin/instructions/docs_orchestration_instructions_autonomous.md` | — | C1, C2 (`parity_gaps:`, `doc_path:`) | `change` | Task 3 (the `<parity_vocabulary>` row's clause, `## Per-entry loop` step 1's return sentences, step 4's two writer clauses, `## Final entry — INDEX`'s writer route), Task 4 (step 2's return sentence, step 3's opening clause, `## Final entry — INDEX`'s reviewer route) |
| 16 | `plugin/instructions/agent_return_contract.md` → `## Who may cite this` | — | P1, `## Why` | `change` | Task 3 (adds the two docs instruction files) |
| 17 | `plugin/instructions/untrusted_input.md` → `## Where a report goes` | — | C1, C2 (`` `notes:` ``, `` `summary:` ``) | `change` | Task 3 (the `docs-writer` row), Task 4 (the `docs-reviewer` row); its `qa-tester` row — *"whose return has no field a report can go in"* — stays true |
| 18 | `plugin/schemas/docs-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 4 |
| 19 | `plugin/agents/docs-reviewer.md` | — | C1, C2 (`missed_docs:`, `` `summary:` ``, `` `blocker:` ``) | `change` | Task 4 |
| 20 | `plugin/instructions/improvement_observations_instructions.md` → `## What the orchestrator may log — rules` item 6 | — | C2 (`` `notes:` `` / `` `summary:` ``) | `change` | Task 4 (the clause *"every sub-agent's `notes:` / `summary:` contract field"*) |
| 21 | `docs/structured-agent-returns.md` | — | C1, C2 (`error: blocked`), C3 (`#380`, `one at a time`, `outside every check until`), P1 (`## Why`, `## Closing the work`) | `change` | Task 6. It records every decision this change relies on as measured, so no `## 3.` entry is owed |
| 22 | `ROADMAP.md` → the `Structured agent outputs` row and its index row | — | C3, P1 (`## Closing the work`) | `change` | Task 6. Its *"one at a time"* in the `Parallel dispatch in waves` row is about dispatch, not adoption, and is unchanged |
| 23 | `.claude/context/plugin.md` → `## The sections an asset carries`; `## Wires: dispatch in, return out`; `## Not determined` | — | C1 | `no-change` | A conventions document, never a plannable target. Task 2 falsifies *"A declared-but-unimplemented variant carries neither"* and Task 5 leaves no agent the sentence *"An agent with no schema file yet still returns a fenced block of `key: value` lines"* describes; recorded as a `stale-rule` entry in `corpus_staleness` |
| 24 | `.claude/context/conventions.md` → `## Plugin asset authoring` | — | C2 (`` `error:` / blocker ``) | `no-change` | A conventions document. Task 1 removes the last agent `error:` return its *"through its own `error:` / blocker return"* describes; recorded as a `stale-rule` entry |
| 25 | `ARCHITECTURE.md` | — | C1, C2 (`unmarked [^.]*error`, a false match on its status-marker rule) | `no-change` | It names the three `qa-tester` files and the browser-tool grant; no return |
| 26 | `docs/analyze.md` | — | C1 | `no-change` | Why `/devscene:analyze` does not reuse the docs pair; *"returns a clean no-op"* stays true of `phase_disabled` |
| 27 | `docs/cli.md` | — | C1 | `no-change` | The `--qa` driver question; no return |
| 28 | `docs/copilot-foundry-research.md` | — | C1 | `no-change` | A research record of the tool closure |
| 29 | `docs/development.md` | — | C1 | `no-change` | A sanitization-sweep note naming a regular expression in `docs-reviewer.md` |
| 30 | `docs/orchestrator-cost-measurement.md` | — | C1 | `no-change` | A measured record of past runs |
| 31 | `docs/outer-loop-verification.md` | — | C1 | `no-change` | The docs flow's missing clarification channel; no return |
| 32 | `docs/retrieval-eval-results.md` | — | C1 | `no-change` | A measured record; it names a research document's path |
| 33 | `docs/retrieval.md` | — | C1 | `no-change` | Which agents query the docs index; no return |
| 34 | `docs/github-run-control.md` | — | C2 (`` `summary:` ``) | `no-change` | A `read-mention` measurement; not one of the five agents |
| 35 | `plugin/agents/ui-tests-plan-writer.md` | — | C1 | `no-change` | It names `qa-tester` as the consumer of the plan **file**; no return |
| 36 | `plugin/agents/ui-tests-plan-reviewer.md` | — | C1 | `no-change` | as row 35 |
| 37 | `plugin/commands/branch-implement-plan-semi-autonomous.md` | — | C1, C2 (`1-3 line contract`) | `change` | Task 2 (the orchestrator paragraph's *"beyond reading the 1-3 line contract each agent returns"*, which tells the session to read every dispatched agent's return, `qa-tester` included, in the old line form) |
| 38 | `plugin/commands/branch-implement-user-review-semi-autonomous.md` | — | C1, C2 (`1-3 line contract`) | `change` | Task 2 (the same clause of its orchestrator paragraph) |
| 39 | `plugin/commands/branch-qa-test.md` | — | C1 | `no-change` | Its driver statement and story-index check; it loads `qa_test_instructions.md`, which reads the return |
| 40 | `plugin/commands/branch-start-docs-autonomous.md` | — | C1 | `no-change` | It loads `docs_orchestration_instructions_autonomous.md`, which reads the returns |
| 41 | `plugin/docs/AUTONOMOUS_FLOW.md` | — | C1 | `no-change` | Its roster table and the Phase E summary; it parses no return and is already on the module's roster |
| 42 | `plugin/instructions/README.md` | — | C1 | `no-change` | A directory description |
| 43 | `plugin/instructions/autonomous_pause_and_ledger.md` | — | C1 | `no-change` | It names *"a `qa-tester` PASS"* as a verdict a unit carried, in prose; it routes nothing |
| 44 | `plugin/instructions/dispatch_discipline_instructions.md` | — | C1 | `no-change` | The receiving-side roster. *"above the fenced block, or above the prose summary"* stays true |
| 45 | `plugin/instructions/main_repo_resolution.md` | — | C1 | `no-change` | Its citer roster names `qa-tester.md` |
| 46 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` | — | C1 | `no-change` | The QA-user locks and Override H's docs-phase activation; it reads no return of the five |
| 47 | `plugin/instructions/unit_loop_core.md` | — | C1 | `no-change` | Row `E.3` names `qa-tester`'s per-dispatch **files**; no return |
| 48 | `plugin/instructions/task_plan_writing_instructions_semi_autonomous.md` | — | C2 (`` `summary:` ``) | `no-change` | The walker's `summary:` line, not one of the five agents |
| 49 | `plugin/samples/sample_task_plan.md` | — | C1 | `no-change` | The UI-test plan file family `qa-tester` consumes |
| 50 | `plugin/scripts/README.md` | — | C1 | `no-change` | The QA-user helper pair `qa-tester.md` invokes |
| 51 | `harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path …"* | — | P2, names a rename | `no-change` | It binds every task: no caller keeps a fallback reading the old `verdict:` / `error:` / `key: value` form |
| 52 | `harness-runs/lessons.md` → *"State a new behaviour once, in the section that decides it, and cite it from everywhere else …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan: each route is stated once, at its dispatch site |
| 53 | `harness-runs/lessons.md` → *"When an agent definition has to give back words to hold its word count …"* | — | P2, `## Agent prose` | `no-change` | It binds Tasks 1–4's agent edits: no definition or edge case is dropped |
| 54 | `harness-runs/lessons.md` → *"Keep a machine-read contract the model never acts on … in a plugin file outside the agent definition …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan: each schema lives in `plugin/schemas/`, never in a definition |
| 55 | `harness-runs/lessons.md` → *"A shared instruction module carries only what its runtime reader acts on …"* | — | P2, `## Agent prose` | `no-change` | It binds Task 3, which adds only roster lines to `agent_return_contract.md` |
| 56 | `harness-runs/lessons.md` → *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space …"* | — | P2, `## Agent prose`, names an outcome | `no-change` | It binds every outcome this plan names, and decides `blocked` (from `error: blocked — `) and `targets_none` (from `targets: none`) |
| 57 | `harness-runs/lessons.md` → *"Name an adopter-facing surface with the term adopters already arrive with …"* | — | P2, names a rename | `no-change` | This branch renames no adopter-facing surface: every return it changes is read by the plugin's own orchestrating sessions |
| 58 | `harness-runs/lessons.md` → *"A decision rule's outcome is a proposal to the maintainer, not a settled future …"* | — | P2, names an outcome | `no-change` | This branch makes no measurement and records no verdict; Task 6 records decisions of record the task prompt asks for |
| 59 | `harness-runs/lessons.md` → *"Grade a write probe on what reached the disk … is an outcome of its own …"* | — | P2, names an outcome | `no-change` | This branch grades no write probe |
