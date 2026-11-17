# Story: Structured returns for the end-of-branch reviewers, the user-review fix-plan writer and the statistics writer

## Context

This branch is the third of five that give every plugin agent a declared, schema-validated return. It covers five agents: `review-plan-reviewer`, `branch-reviewer`, `skeptic-reviewer`, `user-review-fix-plan-writer` and `statistics-plan-writer`. Each one gets three things:

- a schema file `plugin/schemas/<agent>.return.json` in the closed dialect `docs/structured-agent-returns.md` → `### The return schema` lists;
- a `### Return fields` subsection;
- the canonical return-block sentence in its `## Output contract`.

Every caller that reads one of these returns moves onto the field-citation form `` `<agent>.<field>` `` and the outcome form "an `outcome` of `PASS`". Each caller that routes on a return points at `plugin/instructions/agent_return_contract.md` → `## Reading a return` and `## A return that fails the check`. The mechanism is not re-decided here, and `cli/test/agent-return-schemas.test.mjs` picks up each new schema file with no change to the suite.

**The preconditions hold.**

- `docs/structured-agent-returns.md` records all three of `feat_structured_outputs_mechanism`'s decisions:
  - how a session reads an `Agent` result, in `## Reading a return` step 1 and the 2026-11-17 measurement in §3;
  - how a list of multi-part items is represented, in `### A list of structured items is an array of objects, one level deep`;
  - what an agent's `error:` return becomes, in *An agent's own `error:` return becomes an outcome, never `error`*.
- `agent_return_contract.md` → `## Reading a return` step 4 carries `feat_structured_outputs_unit_loop`'s optional-field rule.
- `harness-runs/lessons.md` carries that branch's rule that an outcome value is one token with no space.

The plan found no point where the record and the task prompt disagree. One sentence of the record needed reading in context. *"The literal a caller matched before becomes the outcome value it routes on"* cannot hold for `statistics-plan-writer`, because its old literal is the bare `error:`, which carries no other words. The record's own rule *"named for the result it reports and never `error` or `blocker`"* decides that case, and the record leaves the choice to the adopting branch (*"the outcome each such agent takes is decided by the branch that adopts it"*). Task 6 writes the choice into the record.

**The outcomes and fields.** None of these agents is dispatched by the planning graph, so none is held to graph outcome keys. Every name below is one token.

- **`review-plan-reviewer`:**
  - `PASS`, with no other field;
  - `FAIL`, with `findings_file` and `must_fix_count` (integer, at least 1);
  - `blocker`, with `blocker`.
- **`branch-reviewer`:**
  - `returned`, with `index_path`, `findings_dir` and `finding_count` (integer, at least 0);
  - in two-pass mode only, the reconciliation counts `carried_over`, `skipped_covered` and `skipped_stale` (integers, at least 0), which replace the prose line `Pass 2 carried over N items, skipped M (already covered) and K (stale).`;
  - the optional `questions` (array of strings);
  - `blocker`, with `blocker`.
- **`skeptic-reviewer`:**
  - `PASS`, with the optional `questions`;
  - `FAIL`, with `index_path`, `must_fix_count` (integer, at least 0 — a FAIL may carry only Should Fix findings) and the optional `questions`;
  - `blocker`, with `blocker`.
- **`user-review-fix-plan-writer`:**
  - `returned`, with `fix_plan_file`, `fix_plan_dir`, `valid_must_fix`, `valid_should_fix`, `valid_nice_to_have` and `invalid` (integers, at least 0);
  - `questions`, with `questions` (array of strings, at least 1), which replaces the `## Questions` section and the `fix_plan_file: (pending — questions for user)` sentinel;
  - `blocker`, with `blocker`.
- **`statistics-plan-writer`:**
  - `written`, with `statistics_file`, `story_points_total`, `issue_cost_total`, `story_plan_tasks`, `user_review_issues` (integers, at least 0), `success_rate` (a string: a percentage or `n/a`) and `status` (`enum` `pre-user-review` / `post-user-review`);
  - `not_written`, with `cause`. This is its former `error:` return, which every caller treated as non-halting.

**Two placements of `questions`, both the field the precedent made of `## Questions`.**

- For `user-review-fix-plan-writer`, a question stops the loop. So, as for `task-plan-writer`, it is an outcome of its own.
- For `branch-reviewer` and `skeptic-reviewer`, a question rides beside a finished review. The caller retains it and acts on nothing (`plan_orchestration_instructions_core.md` → `### B.1` and `### C2.1`). So it is an **optional** field on their non-blocker outcomes. `## Reading a return` step 4 leaves it out of the check: absent or empty means none.

`## Unsolicited dispatch guidance` stays prose above the block, and its byte-identical block in the three reviewers is not edited.

**A failed statistics write still never halts (goal 3).** As it stands, `agent_return_contract.md` → `## A return that fails the check` defines a third failing return's `error` route as `--outcome error` where the section passes outcomes to `flow-walker.sh`, otherwise the flow's blocker route. Neither orchestration core runs on `flow-walker.sh` and both bind `<escalate>`, so a sentence at the dispatch site alone would be overridden and the flow would halt. Task 5 therefore does two things:

- it amends that section so a dispatching section that names its own `error` route has that route taken, ahead of the `flow-walker.sh` and blocker-route fallbacks — runtime content the orchestrating session acts on, as the ledger's shared-module rule requires;
- it names, at every `statistics-plan-writer` dispatch site, that `error` route as the same non-halting route `not_written` takes: report, omit the statistics line, continue.

The non-halting outcome then follows from the module's own wording. Task 6 records that mechanism.

**Why each agent and its callers land in one task, and how the shared files are split.** The constraint *"No caller is left reading a field its agent no longer returns, at the end of any task"* means each agent's schema, its definition and every caller of it change together. Callers of different agents share files. Each task owns named sentences in them, listed in its own file, and no task edits a sentence another task owns. Each task `**Depends on:**` the one before it.

- `plugin/instructions/plan_orchestration_instructions_core.md` is shared by Tasks 1, 2, 3 and 5.
- `plugin/instructions/plan_orchestration_instructions_autonomous.md` is shared by Tasks 1–5.
- `plugin/instructions/code_review_instructions.md` and `plugin/instructions/agent_return_contract.md` are shared by Tasks 2 and 5.
- Two sentences are shared clause by clause: `### D.2 Done summary`'s **Review questions** bullet and the autonomous fork's *"A reviewer's `## Questions` section is not an observation"* bullet. Task 2 rewrites each into a two-clause form, with the `branch-reviewer` clause on the new form and the `skeptic-reviewer` clause unchanged. Task 3 rewrites only the `skeptic-reviewer` clause. Both task files spell out the intermediate and the final text.
- The orchestration core's opening *"Reviewers return 1 line …"* bullet is Task 1's alone. Task 1 rewrites it in a form that names no agent, so it stays true at every task boundary.
- `plugin/instructions/untrusted_input.md` → `## Where a report goes` is Task 4's alone. That covers both its `user-review-fix-plan-writer` row and its `statistics-plan-writer` row. The latter is reworded to *"whose return has no field a report can go in"*, which is true before and after Task 5.

**New citers of the module.** `agent_return_contract.md` → `## Who may cite this` gains three documents:

- `code_review_instructions.md` (Task 2), which presents `branch-reviewer`'s return and later reads `statistics-plan-writer`'s;
- `code_review_fixes_instructions.md` and `user_review_fixes_instructions.md` (Task 5), the two supervised statistics dispatch sites.

Every other routing caller is already on the roster. The autonomous and supervised forks over a core cite fields but do not point at the module: the core they run does the check.

**What stays as it is.**

- The review index, its `## Phase 2 Readiness — Ordered Fix List`, the per-finding files and the round files' `verdict:` lines are file content.
- So is the fix plan's `**Review comments:** ` line, which `cli/templates/scripts/remote-run.sh` → `deliver` reads.
- No script reads any of these five returns, so no script changes.
- No permission, configuration key or measured fact is added. Everything the change relies on about the `Agent` result is already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured`.
- Per the ledger's breaking-rename rule, no caller keeps a fallback that reads the old `verdict:` / `key: value` form.

**Top risks:**

- **A caller left reading the old prose form.** The literals are quoted across the corpus, so a missed sentence is a silent break. Each task's `Verification:` re-derives its agent's old literals by grep across `plugin/`, and the `## Scope register` below closes the site set.
- **A statistics failure that halts.** Under the module's current wording, a third failing `statistics-plan-writer` return would fall through to `<escalate>`. Task 5 amends `## A return that fails the check` so a section's own named `error` route is taken first, names that route at all five dispatch sites, and verifies the amended sentence by reading it and each site by grep.
- **A shared sentence edited twice into an incoherent state.** Tasks 2 and 3 each carry the exact intermediate and final wording of the two clause-shared sentences, so Task 3's edit replaces exactly what Task 2 left.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom, and the commit step flips each to `[x]` as that task's commit lands.

- **Only the committing role flips a marker.** That is the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker here, or edits any other line of this section, while a run is iterating this index.
- `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational only. The commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_structured_outputs_branch_review/task_<K>_plan.md`. Ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Give `review-plan-reviewer` a schema-validated return and move the B.2 and C2.2 meta-review loops onto it _(layer: plugin)_ _(points: 15)_
2. [x] **Task 2** — Give `branch-reviewer` a schema-validated return and move Phase B and the supervised code review onto it _(layer: plugin)_ _(points: 20)_
3. [x] **Task 3** — Give `skeptic-reviewer` a schema-validated return and move Phase C2 and its Done-summary lines onto it _(layer: plugin)_ _(points: 20)_
4. [ ] **Task 4** — Give `user-review-fix-plan-writer` a schema-validated return and move the user-review fix-plan flow onto it _(layer: plugin)_ _(points: 20)_
5. [ ] **Task 5** — Give `statistics-plan-writer` a schema-validated return with a non-halting `not_written` outcome and move every statistics dispatch onto it _(layer: plugin)_ _(points: 20)_
6. [ ] **Task 6** — Record `statistics-plan-writer`'s `not_written` outcome in the decision record _(layer: general)_ _(points: 8)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_structured_outputs_branch_review_task_prompt.md` → `## The goal`, item 2): *"No caller parses these agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`."*

**Derivation entry C1 — corpus files naming one of the five agents (command).** Re-run verbatim from the checkout root:
`git grep -lE 'branch-reviewer|skeptic-reviewer|review-plan-reviewer|user-review-fix-plan-writer|statistics-plan-writer' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md' 'docs/*.md' 'README.md' 'ARCHITECTURE.md' 'ROADMAP.md' 'CONTRIBUTING.md' ':(exclude)docs/work-report-research/*' ':(exclude)docs/rag-extraction-research/*'`

**Derivation entry C2 — corpus files carrying one of the five agents' old return literals (command).** Re-run verbatim from the checkout root:
``git grep -lE 'verdict: (PASS|FAIL)|must_fix_count|index_path:|Pass 2 carried over|pending — questions for user|`## Questions`|fix_plan_file|fix_plan_dir|valid_must_fix|valid_should_fix|valid_nice_to_have|statistics_file|story_plan_tasks|user_review_issues|success_rate|returns? `error:`|returned an `error:`|`error:` gate' -- 'plugin/*.md' 'plugin/*.txt' 'cli/templates/*.md' 'harness-runs/*/README.md' '.claude/*.md' 'docs/*.md' 'README.md' 'ARCHITECTURE.md' 'ROADMAP.md' 'CONTRIBUTING.md' ':(exclude)docs/work-report-research/*' ':(exclude)docs/rag-extraction-research/*'``

**What the two command entries cover.**

- They cover the plugin's Markdown and text, the adopter-facing templates, this repository's self-adopted state-directory READMEs, the conventions documents, `docs/` and the root prose documents.
- They leave out shell and TypeScript source and its comments, which are not corpus text. No script reads any of the five returns: `git grep` over `cli/templates/scripts` and `cli/src` finds only `cli/templates/scripts/remote-run.sh`'s header naming the fix plan's `**Review comments:**` file contract.
- They leave out `docs/work-report-research/` and `docs/rag-extraction-research/`. Those are research records of past studies, which name these agents as subjects and route nothing.

**Derivation entry P1 — the files the task prompt names (procedure).**

- **Artifact:** the task prompt `harness-runs/task_prompts/feat_structured_outputs_branch_review_task_prompt.md`.
- **Traversal:** its sections in file order (`## Why`, `## Scope: the agents and their current returns`, `## The goal`, `## Constraints`), and within each, every backticked repository path in order of appearance. The pattern `plugin/schemas/<agent>.return.json` is expanded once for each of the five agents the opening paragraph names.
- **Decision rule:** a path is reached when it names durable corpus text: a plugin file, a document under `docs/`, a root prose document or a schema file. A path to shell or TypeScript source, or to a test, is not reached.

**Derivation entry P2 — standing-artifact rows (procedure).**

- **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`.
- **Artifact:** the lessons ledger.
- **Traversal:** its topic headings in file order, then the one-line rules under each.
- **Decision rule:** a rule is reached when it sits under `## Agent prose`, or names a rename, an agent's return, an outcome or a shared instruction module.

**Closure invariant:** every site any of the four entries reaches appears as a row below. A site two entries reach is one row, and its `Evidence` cell names every entry that reached it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/schemas/review-plan-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 1 |
| 2 | `plugin/agents/review-plan-reviewer.md` | — | C1, C2 (`verdict: PASS`, `must_fix_count`) | `change` | Task 1 |
| 3 | `plugin/instructions/plan_orchestration_instructions_core.md` | — | C1, C2 (`verdict: PASS`, `index_path:`, `must_fix_count`, `` `## Questions` ``, `statistics_file`, ``returns `error:` ``) | `change` | Task 1 (the *"Reviewers return 1 line …"* bullet, `### B.2` step 2, `### C2.2` step 2), Task 2 (`### B.1`'s return paragraphs, the `branch-reviewer` clause of `### D.2`'s **Review questions** bullet), Task 3 (`### C2.1`'s parse and questions paragraphs, `### D.2`'s **Skeptic review** bullet, the `skeptic-reviewer` clause of **Review questions**), Task 5 (the `<escalate>` row's D.1 sentence, `### D.1`'s parse paragraph, `### D.2`'s **Branch statistics** bullet) |
| 4 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` | — | C1, C2 (`verdict: PASS`, `` `## Questions` ``, `statistics_file`, `` `error:` gate ``) | `change` | Task 1 (the `Bm` flip), Task 2 (the `branch-reviewer` clause of the *"is not an observation"* bullet), Task 3 (the `C2g` flip, the `skeptic-reviewer` clause of the `*g` paragraph, the `skeptic-reviewer` clause of the *"is not an observation"* bullet), Task 4 (the closed list's entry 13), Task 5 (Override D's trigger, gate and commit-mechanism paragraphs, Override I's *"mirrors Override D's `error:` gate"* clause, the closed list's entry 5 clause) |
| 5 | `plugin/schemas/branch-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 2 |
| 6 | `plugin/agents/branch-reviewer.md` | — | C1, C2 (`Pass 2 carried over`, `` `## Questions` ``) | `change` | Task 2 |
| 7 | `plugin/instructions/code_review_instructions.md` | — | C1, C2 (`statistics_file`, `success_rate`) | `change` | Task 2 (`## Flow` steps 3–4 and the module pointer), Task 5 (step 6.2) |
| 8 | `plugin/instructions/agent_return_contract.md` → `## A return that fails the check`; `## Who may cite this` | — | P1, `## Why` | `change` | Task 2 (adds `code_review_instructions.md` to the roster), Task 5 (amends the `error`-route sentence of `## A return that fails the check` so a dispatching section's own named `error` route is taken ahead of the fallbacks; adds `code_review_fixes_instructions.md` and `user_review_fixes_instructions.md` to the roster) |
| 9 | `plugin/schemas/skeptic-reviewer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 3 |
| 10 | `plugin/agents/skeptic-reviewer.md` | — | C1, C2 (`verdict: PASS`, `index_path:`, `` `## Questions` ``) | `change` | Task 3 |
| 11 | `plugin/schemas/user-review-fix-plan-writer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 4 |
| 12 | `plugin/agents/user-review-fix-plan-writer.md` | — | C1, C2 (`fix_plan_file`, `pending — questions for user`, `` `## Questions` ``) | `change` | Task 4 |
| 13 | `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` | — | C1, C2 (`` `## Questions` ``, `fix_plan_file`, `valid_must_fix`) | `change` | Task 4 |
| 14 | `plugin/instructions/user_review_fix_plan_writing_instructions.md` | — | C2 (`` `## Questions` ``, `fix_plan_file`) | `change` | Task 4 |
| 15 | `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` | — | C1, C2 (`` `## Questions` ``, `valid_must_fix`) | `change` | Task 4 |
| 16 | `plugin/commands/branch-start-user-review-fix-plan.md` | — | C1, C2 (`` `## Questions` ``) | `change` | Task 4 (step 4's *"the live `## Questions` surface"*) |
| 17 | `plugin/instructions/untrusted_input.md` → `## Where a report goes` | — | C1, C2 (`` `## Questions` ``) | `change` | Task 4 (the `user-review-fix-plan-writer` row and the `statistics-plan-writer` row) |
| 18 | `plugin/schemas/statistics-plan-writer.return.json` (new) | — | P1, `## The goal` item 1 | `change` | Task 5 |
| 19 | `plugin/agents/statistics-plan-writer.md` | — | C1, C2 (`statistics_file`, `success_rate`), P1 (`## Scope`) | `change` | Task 5 |
| 20 | `plugin/instructions/user_review_fixes_instructions_core.md` | — | C1, C2 (`statistics_file`, ``returns `error:` ``) | `change` | Task 5 (`### D.1`'s parse paragraph and `### D.2`'s **Branch statistics** bullet); its *"Reviewers return 1 line …"* bullet is unchanged, because no reviewer this flow dispatches is one of the five |
| 21 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` | — | C1, C2 (`statistics_file`, `` `error:` gate ``) | `change` | Task 5 (Override D's trigger, gate and commit-mechanism paragraphs; the *"mirrors Override D's `error:` gate"* clause) |
| 22 | `plugin/instructions/code_review_fixes_instructions.md` | — | C1, C2 (`statistics_file`, `success_rate`) | `change` | Task 5 |
| 23 | `plugin/instructions/user_review_fixes_instructions.md` | — | C1, C2 (`statistics_file`, `success_rate`) | `change` | Task 5 |
| 24 | `plugin/instructions/improvement_observations_instructions.md` | — | C2 (``returns `error:` ``, `` `error:` gate ``) | `change` | Task 5 (the two clauses that compare a skipped write with the statistics `error:` route) |
| 25 | `docs/structured-agent-returns.md` | — | C1, C2 (`` `## Questions` ``, ``returns `error:` ``), P1 (`## Why`) | `change` | Task 6 — the *An agent's own `error:` return …* decision. It already records the mechanism's three decisions, and the change relies on nothing it does not record as measured, so no `## 3.` entry is owed |
| 26 | `ROADMAP.md` → the `Structured agent outputs` row | — | C1, P1 (`## Why`) | `no-change` | The row stays open until the fifth branch of the series lands. Its other mention of `branch-reviewer` is a research item |
| 27 | `.claude/context/plugin.md` → `## Wires: dispatch in, return out` | — | C1, C2 (`verdict: PASS`) | `no-change` | A conventions document, never a plannable target. Task 3 falsifies its example *"`verdict: FAIL` with its path and count lines … (`plugin/agents/skeptic-reviewer.md` → `## Output contract`)"*; recorded as a `stale-rule` entry in `corpus_staleness` |
| 28 | `.claude/context/conventions.md` → `## Plugin asset authoring`; `## Commit-message policy` | — | C1 | `no-change` | A conventions document. Task 5 falsifies *"reports it through its own `error:` / blocker return"* for `statistics-plan-writer`; recorded as a `stale-rule` entry. Its commit-policy mention, that `statistics-plan-writer` reads commit-body record lines, is unchanged |
| 29 | `ARCHITECTURE.md` | — | C1 | `no-change` | The docs-retrieval tool roster; no return |
| 30 | `README.md` | — | C1 | `no-change` | It names the writer of `statistics.md`, a file, not a return |
| 31 | `cli/templates/state-dir/dispatch_additions/README.md` | `cli/templates` | C1 | `no-change` | A heartbeat example naming `skeptic-reviewer`; no return |
| 32 | `harness-runs/dispatch_additions/README.md` | `harness-runs` (self-adopted) | C1 | `no-change` | as row 31 |
| 33 | `docs/converging-plan-reviews.md` | — | C1, C2 (`verdict: FAIL`) | `no-change` | Round-file `verdict:` lines, which are file content; it names the end-of-branch reviewers as readers of incidental findings |
| 34 | `docs/github-run-control.md` | — | C1 | `no-change` | It describes the fix plan's `**Review comments:**` file contract, which is unchanged |
| 35 | `docs/orchestrator-cost-measurement.md` | — | C1 | `no-change` | A measured record of past runs |
| 36 | `docs/retrieval-eval-results.md` | — | C1 | `no-change` | A measured record; it names a research document's path |
| 37 | `docs/sandbox-verification.md` | — | C1, C2 (`` `## Questions` ``) | `no-change` | A measured record of past runs; its `## Questions` is `test-fix-plan-writer`'s at the time |
| 38 | `docs/flow-graph-walker.md` | — | C2 (`` `## Questions` ``, `verdict: PASS`) | `no-change` | A decision record about the planning agents, a prior branch's |
| 39 | `docs/second-runtime-port-decision.md` | — | C2 (`verdict: FAIL`, `` `## Questions` ``) | `no-change` | A decision record about the planning flow, a prior branch's |
| 40 | `cli/templates/state-dir/architecture_reviews/README.md` | `cli/templates` | C2 (`verdict: PASS`) | `no-change` | A round file's `verdict:` line — file content |
| 41 | `harness-runs/architecture_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 40 |
| 42 | `cli/templates/state-dir/architecture_user_review_reviews/README.md` | `cli/templates` | C2 | `no-change` | as row 40 |
| 43 | `harness-runs/architecture_user_review_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 40 |
| 44 | `cli/templates/state-dir/business_parity_reviews/README.md` | `cli/templates` (no self-adopted copy: `phases.parity` is `false` here) | C2 | `no-change` | as row 40 |
| 45 | `cli/templates/state-dir/business_parity_user_review_reviews/README.md` | `cli/templates` (no self-adopted copy) | C2 | `no-change` | as row 40 |
| 46 | `cli/templates/state-dir/task_plan_reviews/README.md` | `cli/templates` | C2 | `no-change` | as row 40 |
| 47 | `harness-runs/task_plan_reviews/README.md` | `harness-runs` (self-adopted) | C2 | `no-change` | as row 40 |
| 48 | `plugin/agents/README.txt` | — | C1 | `no-change` | The docs-retrieval roster and a directory listing; no return |
| 49 | `plugin/agents/architecture-reviewer.md` | — | C1, C2 | `no-change` | Its own return is already adopted. It names `branch-reviewer`'s split **file** shape and re-dispatches `user-review-fix-plan-writer` in revision mode, which reads no return |
| 50 | `plugin/agents/business-parity-reviewer.md` | — | C1, C2 | `no-change` | as row 49 |
| 51 | `plugin/agents/layer-reviewer.md` | — | C1, C2 | `no-change` | It states that `branch-reviewer`'s Pass 2 reads its **files**; its own return is adopted |
| 52 | `plugin/agents/qa-tester.md` | — | C1, C2 | `no-change` | Its own `verdict:` return, adopted by `feat_structured_outputs_docs_qa`; it names `branch-reviewer`'s split file format |
| 53 | `plugin/agents/docs-reviewer.md` | — | C2 (`verdict: PASS`) | `no-change` | Its own return, a later branch's |
| 54 | `plugin/agents/task-plan-reviewer.md` | — | C2 | `no-change` | `verdict:` round-file content; its return is adopted |
| 55 | `plugin/agents/test-fix-plan-writer.md` | — | C2 (`fix_plan_file`, `fix_plan_dir`) | `no-change` | Those are its own adopted fields, not `user-review-fix-plan-writer`'s |
| 56 | `plugin/agents/ui-tests-plan-reviewer.md` | — | C2 | `no-change` | as row 54 |
| 57 | `plugin/commands/branch-implement-plan-semi-autonomous.md` | — | C1 | `no-change` | A summary (*"loop up to 5 times until `PASS`"*) that names an outcome value and routes nothing |
| 58 | `plugin/commands/branch-start-docs-autonomous.md` | — | C1 | `no-change` | It names agents the docs flow does not run |
| 59 | `plugin/docs/AUTONOMOUS_FLOW.md` | — | C1 | `no-change` | Its roster table names the agent files; it parses no return and is already on the module's roster |
| 60 | `plugin/instructions/README.md` | — | C1 | `no-change` | A directory description |
| 61 | `plugin/instructions/dispatch_discipline_instructions.md` | — | C1 | `no-change` | The receiving-side roster. The `## Unsolicited dispatch guidance` block it owns says *"above the fenced block, or above the prose summary"*, which stays true |
| 62 | `plugin/instructions/docs_orchestration_instructions_autonomous.md` | — | C1 | `no-change` | It names `statistics-plan-writer` as not run in the docs flow |
| 63 | `plugin/instructions/docs_phase_instructions.md` | — | C1 | `no-change` | It places the docs phase before the D.1 dispatch; it reads no return |
| 64 | `plugin/instructions/mode_contract.md` → `## Binding vocabulary`, the `<ask>` row | — | C2 (`` `## Questions` ``) | `no-change` | A rationale clause citing `task_plan_writing_instructions_core.md`, whose writer an earlier branch moved to a `questions` outcome; it routes nothing |
| 65 | `plugin/instructions/plan_review_rounds.md` | — | C1, C2 | `no-change` | Its roster of agents citing it, and round-file `verdict:` lines — file content |
| 66 | `plugin/instructions/qa_test_instructions.md` | — | C2 | `no-change` | `qa-tester`'s returns, a later branch's |
| 67 | `plugin/instructions/run_mode_instructions.md` | — | C1 | `no-change` | It names `review-plan-reviewer` as a structural reviewer; no return |
| 68 | `plugin/instructions/unit_loop_core.md` → `## The test-run rule` | — | C1 | `no-change` | Its roster of citers names three of the five agent files |
| 69 | `plugin/samples/sample_code_review.md` | — | C1 | `no-change` | The review index file format, unchanged |
| 70 | `plugin/samples/sample_statistics.md` | — | C1, C2 (`success_rate`, `story_plan_tasks`) | `no-change` | `statistics.md` file content, whose headings name the same quantities; unchanged |
| 71 | `plugin/samples/sample_task_plan.md` | — | C1 | `no-change` | It names the statistics writer of a file family |
| 72 | `plugin/samples/sample_user_review.md` | — | C1 | `no-change` | The user-review file format |
| 73 | `plugin/samples/sample_user_review_fix_plan.md` | — | C1 | `no-change` | The fix-plan index file format, unchanged |
| 74 | `harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path …"* | — | P2, names a rename | `no-change` | It binds every task: no caller keeps a fallback reading the old `verdict:` / `key: value` / `error:` form |
| 75 | `harness-runs/lessons.md` → *"State a new behaviour once, in the section that decides it, and cite it from everywhere else …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan. Each route is stated once, at its dispatch site, and every other mention — the Done summary, the autonomous overrides, the forks — names the route without restating it |
| 76 | `harness-runs/lessons.md` → *"When an agent definition has to give back words to hold its word count, cut restatement or rationale …"* | — | P2, `## Agent prose` | `no-change` | It binds Tasks 1–5's agent edits: no definition or edge case is dropped |
| 77 | `harness-runs/lessons.md` → *"Keep a machine-read contract the model never acts on … in a plugin file outside the agent definition …"* | — | P2, `## Agent prose` | `no-change` | It binds this plan: each schema lives in `plugin/schemas/`, never in a definition |
| 78 | `harness-runs/lessons.md` → *"A shared instruction module carries only what its runtime reader acts on …"* | — | P2, `## Agent prose` | `no-change` | It binds Tasks 2 and 5. They add roster lines to `agent_return_contract.md`, and Task 5's amendment of `## A return that fails the check` is a routing rule the orchestrating session acts on at run time, never an authoring rule |
| 79 | `harness-runs/lessons.md` → *"A value a script or graph may route on (an outcome, a key, an id) is one token with no space …"* | — | P2, `## Agent prose`, names an outcome | `no-change` | It binds every outcome this plan names: `PASS`, `FAIL`, `blocker`, `returned`, `questions`, `written`, `not_written` |
| 80 | `harness-runs/lessons.md` → `## Adopter-facing documentation` → *"Name an adopter-facing surface with the term adopters already arrive with … never the configuration key, tool name, check id or any other wire identifier."* | — | P2, names a rename | `no-change` | It constrains renames of adopter-facing surfaces. This branch renames no adopter-facing surface: every return it changes is read by the plugin's own orchestrating sessions |
| 81 | `harness-runs/lessons.md` → `## Evidence and measurement` → *"A decision rule's outcome is a proposal to the maintainer, not a settled future …"* | — | P2, names an outcome | `no-change` | It constrains how a measurement verdict is recorded. This branch makes no measurement and records no verdict; Task 6 records a decision of record the task prompt asks for |
| 82 | `harness-runs/lessons.md` → `## Evidence and measurement` → *"Grade a write probe on what reached the disk, never on the call's exit status. "Call succeeded, nothing on disk" is an outcome of its own …"* | — | P2, names an outcome | `no-change` | It grades a write probe's result. This branch writes and grades no probe: its outcomes are agent returns validated against a schema, never a write's disk effect |
