# Story: Should Fix and Nice to Have are advisory in every plan-review loop

## Context

This branch makes Should Fix and Nice to Have findings advisory in every plan-review loop, on top of what #365 (`feat_converging_plan_reviews`) and #371 (`feat_parallel_plan_reviews`) shipped. Three rules come from the task prompt. **(1)** A plan review's verdict depends on Must Fix alone: a review with no Must Fix returns `verdict: PASS`. **(2)** A plan writer re-dispatched after a failing round acts on the round's Must Fix items only, whichever gate's file they sit in. **(3)** Should Fix and Nice to Have stay in the review file as a record for a human. No loop reads them, and no agent gets a new duty to read them.

**One owner, everyone else points.** `plugin/instructions/plan_review_rounds.md` is the shared contract. Task 2 states rules 1 and 3 there once, in a new `## The verdict` section. It also restates rule 2 once in `## The writer's revision`, in the place the old item 3 held: *"Each Should Fix of the round is applied, or recorded under `## Rejected findings` with its reason; …"*. After that the revision note and `## Rejected findings` carry Must Fix items only. Every other plan-review asset either points at those two sections or drops its own paraphrase of the old item 3:
- Task 3: the three writers.
- Task 4: `architecture-reviewer`, `business-parity-reviewer`, and the test-fix-plan gate's caller.
- Task 5: `ui-tests-plan-reviewer`, which joins the module's `## Who may cite this` roster (Task 2 adds the roster line).

This follows the ledger rule *"State a new behaviour once, in the section that decides it, and cite it from everywhere else"* and `.claude/context/plugin.md` → `## Writing agent prose`. Two reviewers previously had no defined Should-Fix-only case: `architecture-reviewer` sub-case (c) (the test fix plan, insertion point 4) and `ui-tests-plan-reviewer`. Under the new rule, each writes its review file when it has a Should Fix or Nice to Have but no Must Fix, and returns `verdict: PASS`. A review with no finding at all still writes nothing.

**Wire strings stay byte-identical.** No caller changes how it routes. The plan-review callers still match only `verdict: PASS` / `verdict: FAIL`. The UI-test gate and the test-fix-plan gate still receive a one-line `verdict: PASS`: the flow walker is never passed `--findings` with a `PASS` from `ui_review` (`plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker — routing is its, judgement is yours`), and G.2 routes `verdict: PASS` straight to G.3. So neither reviewer adds a `findings_file:` line on its new advisory `PASS`. `architecture-reviewer`'s implemented-solution literal *"Do not write any file when PASS"* is quoted by `plugin/instructions/plan_orchestration_instructions_autonomous.md` (the **Zero-finding rounds** paragraph), so Task 4 keeps it verbatim. The G.3 commit already picks up a non-empty `<test_fix_review_folder>` through its existence guard, so an advisory file there is committed with no routing change.

**The run-artifact READMEs that describe these folders.** They live twice: as adopter templates under `cli/templates/state-dir/`, and as this repository's own copies under `harness-runs/`. `init` writes them `create-if-absent`, so a template edit never reaches the live copy (`cli/src/generators/stateDir.ts`). #365 edited both copies in step. This branch does the same: Task 1 edits the templates, and Task 6 makes the live copies byte-identical to them. `harness-runs/` has no `ui_test_plan_reviews/` copy because `phases.qa` is `false` here.

**What deliberately does not change.**
- `task-plan-reviewer` → `## Output contract` already states rule 1 (*"Only **Must Fix** makes the round `FAIL`; …"*), and the prompt says to keep it.
- `ui-tests-plan-writer` already applies only Must Fix items, so its *"Same shape as the `task-plan-writer`'s revision mode"* becomes more true after Task 3, not less.
- `user-review-fix-plan-writer`'s own Must Fix / Should Fix / Nice to Have classification of the user's observations is a different thing, and Task 3 leaves it alone.
- The recorded-rejection blocks are shared, byte-identical, across five writers and four reviewers. They are left unchanged. They stay true (`call stands` is still unavailable for a Must Fix), and rule 2 simply stops feeding them anything but Must Fix items.
- Out of scope, and untouched: the implemented-solution mode of every reviewer, `review-plan-reviewer`, the end-of-branch reviewers, and `qa-tester`'s `verdict: FAIL` with `must_fix_count: 0`.

Every task here is a prose edit to a Markdown contract or README. None adds code or a test file.

**Top risks:**
- **A changed wire literal or return shape strands a caller silently.** Tasks 4 and 5 keep every return byte-identical and keep the quoted *"Do not write any file when PASS"*. Each verifies this with a grep over the literal's quoters.
- **The rule drifts.** It would drift if it were stated a second time in a reviewer or writer instead of being pointed at. Task 2 is the only task that states it, and Tasks 3–5 each verify that their file carries a pointer, not a restatement.
- **The two README copies drift apart.** Task 6 verifies byte-identity against Task 1's templates with `git diff --no-index --exit-code`.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`**: the `committer` agent in every flow that dispatches one, and the orchestrator itself in the supervised flow, which dispatches none. No implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational only. They are never the iteration source, and the committer never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_reviewers_should_fix_only_pass/task_<K>_plan.md`. The entries are in ship order: the configured layer order `cli`, `plugin`, then the catch-all `general` last.

1. [x] **Task 1** — State the advisory-PASS file and the Must-Fix-only revision note in the three adopter run-artifact README templates _(layer: cli)_ _(points: 10)_
2. [x] **Task 2** — Add `## The verdict` to `plan_review_rounds.md` and make `## The writer's revision` Must-Fix-only _(layer: plugin)_ _(points: 10)_
3. [x] **Task 3** — Drop the Should Fix / Nice to Have revision duties from the three plan writers _(layer: plugin)_ _(points: 10)_
4. [ ] **Task 4** — Point `architecture-reviewer` and `business-parity-reviewer` at `## The verdict`, and define sub-case (c)'s advisory PASS _(layer: plugin)_ _(points: 15)_
5. [ ] **Task 5** — Define `ui-tests-plan-reviewer`'s advisory PASS and point it at `## The verdict` _(layer: plugin)_ _(points: 10)_
6. [ ] **Task 6** — Bring this repository's live run-artifact README copies byte-identical to Task 1's templates _(layer: general)_ _(points: 5)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"**In scope:** `task-plan-reviewer`, `ui-tests-plan-reviewer`, and `architecture-reviewer` / `business-parity-reviewer` in plan-review mode, in every loop that dispatches them over a plan, plus the writers those loops re-dispatch."*

**Derivation entry A — plugin contract sites (command).** Re-run verbatim from the checkout root:
`git grep -nE "Should Fix of the round|apply or reject each Should Fix|Add no Nice to Have item|apply only the requested changes|apply only the Must Fix items|Only \*\*Must Fix\*\* (triggers|makes)|If everything is clean|Do not save a file when PASS|Do not write any file when PASS|must not touch disk|passed on iteration 0|One line per finding|Same shape as the .task-plan-writer" -- plugin`

**Derivation entry B — the shared recorded-rejection machinery (command).** Re-run verbatim from the checkout root:
`git grep -n "call stands" -- plugin`

**Derivation entry C — run-artifact READMEs, both copies (command).** Re-run verbatim from the checkout root:
`git grep -nE "per failed|PASS touches no disk|passed on the first gate|approved on the first pass|per finding of the round" -- cli/templates/state-dir 'harness-runs/*/README.md'`

**Derivation entry D — prose documentation (command).** Re-run verbatim from the checkout root:
`git grep -nE "Should Fix of the round|apply or reject each Should Fix|per failed plan review|PASS touches no disk|per finding of the round|Only \*\*Must Fix\*\* triggers" -- docs README.md ARCHITECTURE.md plugin/docs examples`
It reaches no site. The files under `docs/rag-extraction-research/` and `docs/work-report-research/` that use the words *Should Fix* or *Nice to Have* are dated research records. Under `.claude/context/conventions.md` → `## Documents of record`, they record what was true when they were written and are not contracts this branch could falsify.

**Derivation entry E — standing-artifact rows (procedure).** **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`. **Artifact:** the standing lessons ledger. **Traversal:** its topic headings in file order, then the one-line rules under each. **Decision rule:** a rule is reached when it states how a plan writer acts on a Should Fix or Nice to Have item, or what a plan review's verdict keys on. It reaches no row: the ledger line that taught the old item 3 was retired by #372.

**Closure invariant:** every site each derivation entry above reaches appears as a row below. Rows marked *plan addition* are targets the derivations do not reach by construction (a new section or roster line) and are listed so every target is accounted for.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/instructions/plan_review_rounds.md` → `## The writer's revision` ("Each Should Fix of the round is applied, or recorded under `## Rejected findings`") | — | entry A, `Should Fix of the round` | `change` | Task 2 |
| 2 | `plugin/instructions/plan_review_rounds.md` → `## The writer's revision` ("One line per finding.") | — | entry A, `One line per finding` | `change` | Task 2 |
| 3 | `plugin/instructions/plan_review_rounds.md` → new `## The verdict` section | — | plan addition | `change` | Task 2 |
| 4 | `plugin/instructions/plan_review_rounds.md` → `## Who may cite this` (the roster list) | — | plan addition | `change` | Task 2 — adds `ui-tests-plan-reviewer`, which Task 5 makes a citer |
| 5 | `plugin/agents/task-plan-writer.md` → `## Revision mode` ("Add no Nice to Have item unless the orchestrator explicitly told you to.") | — | entry A, `Add no Nice to Have item` | `change` | Task 3 |
| 6 | `plugin/agents/task-plan-writer.md` → `## Revision mode` ("apply or reject each Should Fix") | — | entry A, `apply or reject each Should Fix` | `change` | Task 3 |
| 7 | `plugin/agents/user-review-fix-plan-writer.md` → `## Revision mode` ("apply or reject each Should Fix") | — | entry A, `apply or reject each Should Fix` | `change` | Task 3 |
| 8 | `plugin/agents/user-review-fix-plan-writer.md` → `## Revision mode` ("open only the files they target, apply only the requested changes") | — | entry A, `apply only the requested changes` | `no-change` | The sentence covers both revision prompts, user feedback included. Its reviewer-findings half is bound by `## The writer's revision`, which the next sentence of the same section cites and which Task 2 makes Must-Fix-only. |
| 9 | `plugin/agents/test-fix-plan-writer.md` → `## Revision mode` ("apply only the requested changes") | — | entry A, `apply only the requested changes` | `change` | Task 3 — this writer cites no shared module, so its own sentence is its only statement of rule 2 |
| 10 | `plugin/agents/ui-tests-plan-writer.md` → `## Invocation contract` revision paragraph ("apply only the Must Fix items … Same shape as the `task-plan-writer`'s revision mode.") | — | entry A, `apply only the Must Fix items` / `Same shape as the .task-plan-writer` | `no-change` | It already applies only Must Fix items, and after Task 3 the `task-plan-writer` does the same, so the "same shape" claim stays true (task prompt, What changes item 5) |
| 11 | `plugin/agents/task-plan-reviewer.md` → `## Output contract` ("Only **Must Fix** makes the round `FAIL`") | — | entry A, `Only **Must Fix** makes` | `no-change` | It already states rule 1. The task prompt's *"What already holds — keep it"* names it. |
| 12 | `plugin/agents/architecture-reviewer.md` → `## Output contract` intro ("Both modes share the return lines") | — | plan addition | `change` | Task 4 — the plan-review-mode pointer to `## The verdict` |
| 13 | `plugin/agents/architecture-reviewer.md` → `### Clean review (both modes)` ("Do not write any file when PASS.") | — | entry A, `Do not write any file when PASS` | `change` | Task 4 — sub-case (c) narrowed to "no finding at all"; the quoted literal kept verbatim |
| 14 | `plugin/agents/architecture-reviewer.md` → `## Output contract` new sub-case (c) advisory-PASS section | — | plan addition | `change` | Task 4 |
| 15 | `plugin/agents/architecture-reviewer.md` → `### Return lines (both modes on FAIL)` ("Only **Must Fix** triggers another upstream iteration.") | — | entry A, `Only **Must Fix** triggers` | `change` | Task 4 |
| 16 | `plugin/agents/architecture-reviewer.md` → `## Invocation contract` ("the clean-review branch of `## Output contract` must not touch disk") | — | entry A, `must not touch disk` | `no-change` | It stays true. Sub-case (c) still creates the folder "only when you have findings to write", and an advisory PASS has findings. The clean-review branch remains the no-finding case. |
| 17 | `plugin/agents/business-parity-reviewer.md` → `## Output contract` intro ("Both modes share the return lines") | — | plan addition | `change` | Task 4 — the plan-review-mode pointer to `## The verdict` |
| 18 | `plugin/agents/business-parity-reviewer.md` → `### Return lines (both modes on FAIL)` ("Only **Must Fix** triggers another upstream iteration.") | — | entry A, `Only **Must Fix** triggers` | `change` | Task 4 |
| 19 | `plugin/agents/business-parity-reviewer.md` → `### Clean review (both modes)` ("Do not write any file when PASS. The one addition") | — | entry A, `Do not write any file when PASS` | `no-change` | It covers implemented-solution mode and the disabled-phase no-op only, both out of scope. Plan-review mode always writes its round file. |
| 20 | `plugin/agents/business-parity-reviewer.md` → `## Invocation contract` ("the clean-review branch of `## Output contract` must not touch disk") | — | entry A, `must not touch disk` | `no-change` | It applies to implemented-solution mode only, which is out of scope |
| 21 | `plugin/agents/ui-tests-plan-reviewer.md` → `## Invocation contract` ("The PASS branch of `## Output contract` must not touch disk.") | — | entry A, `must not touch disk` | `change` | Task 5 |
| 22 | `plugin/agents/ui-tests-plan-reviewer.md` → `## Output contract` ("**If everything is clean**, return exactly") | — | entry A, `If everything is clean` | `change` | Task 5 |
| 23 | `plugin/agents/ui-tests-plan-reviewer.md` → `## Output contract` ("Do not save a file when PASS.") | — | entry A, `Do not save a file when PASS` | `change` | Task 5 |
| 24 | `plugin/agents/ui-tests-plan-reviewer.md` → `## Output contract` ("Only **Must Fix** triggers another writer iteration.") | — | entry A, `Only **Must Fix** triggers` | `change` | Task 5 |
| 25 | `plugin/agents/review-plan-reviewer.md` → `## Invocation contract` ("The PASS branch of `## Output contract` must not touch disk.") | — | entry A, `must not touch disk` | `no-change` | It is the code-review meta-reviewer, outside the prompt's in-scope list. *"every other review keeps its current contract"*. |
| 26 | `plugin/agents/review-plan-reviewer.md` → `## Output contract` ("**If everything is clean**, return exactly") | — | entry A, `If everything is clean` | `no-change` | Out of scope, as row 25 |
| 27 | `plugin/agents/review-plan-reviewer.md` → `## Output contract` ("Do not save a file when PASS.") | — | entry A, `Do not save a file when PASS` | `no-change` | Out of scope, as row 25 |
| 28 | `plugin/agents/review-plan-reviewer.md` → `## Output contract` ("Only **Must Fix** triggers another iteration of the review's author.") | — | entry A, `Only **Must Fix** triggers` | `no-change` | Out of scope, as row 25 |
| 29 | `plugin/agents/skeptic-reviewer.md` → `## Invocation contract` ("The PASS branch of `## Output contract` must not touch disk.") | — | entry A, `must not touch disk` | `no-change` | It is an end-of-branch reviewer, which the prompt's out-of-scope list names |
| 30 | `plugin/instructions/plan_orchestration_instructions_core.md` → `### G.3 Commit the test fix plan` ("a gate that passed on iteration 0 created none") | — | entry A, `passed on iteration 0` | `change` | Task 4 — after sub-case (c)'s advisory PASS, only a pass with no finding at all creates none |
| 31 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` → **Zero-finding rounds** paragraph (quotes *"Do not write any file when PASS"*) | — | entry A, `Do not write any file when PASS` | `no-change` | It quotes the implemented-solution clean review, which Task 4 keeps byte-identical |
| 32 | `plugin/agents/architecture-reviewer.md` → `## Process` recorded-rejection paragraph ("rebutted round <j> — call stands") | — | entry B | `no-change` | The shared recorded-rejection machinery is not in the prompt's What changes. It stays true, and rule 2 only narrows what reaches it. |
| 33 | `plugin/agents/architecture-reviewer.md` → "A rejection recorded under precedence is tested as" | — | entry B | `no-change` | As row 32 |
| 34 | `plugin/agents/business-parity-reviewer.md` → `## Process` recorded-rejection paragraph ("rebutted round <j> — call stands") | — | entry B | `no-change` | As row 32 |
| 35 | `plugin/agents/business-parity-reviewer.md` → "A rejection recorded under precedence is tested as" | — | entry B | `no-change` | As row 32 |
| 36 | `plugin/agents/task-plan-reviewer.md` → "**A recorded rejection is an addressed finding only once you have tested it.**" | — | entry B | `no-change` | As row 32 |
| 37 | `plugin/agents/task-plan-reviewer.md` → "A rejection recorded under precedence is tested as" | — | entry B | `no-change` | As row 32 |
| 38 | `plugin/agents/ui-tests-plan-reviewer.md` → `### Index structure` ("**A recorded rejection is an addressed finding only once you have tested it.**") | — | entry B | `no-change` | As row 32 |
| 39 | `plugin/agents/task-plan-writer.md` → "**A reviewer finding you judge wrong is resolved or recorded**" | — | entry B | `no-change` | It is a byte-identical block shared by five writers. Under Task 2's `## The writer's revision`, only a Must Fix reaches it. |
| 40 | `plugin/agents/user-review-fix-plan-writer.md` → "**A reviewer finding you judge wrong is resolved or recorded**" | — | entry B | `no-change` | As row 39 |
| 41 | `plugin/agents/test-fix-plan-writer.md` → "**A reviewer finding you judge wrong is resolved or recorded**" | — | entry B | `no-change` | As row 39 |
| 42 | `plugin/agents/ui-tests-plan-writer.md` → "**A reviewer finding you judge wrong is resolved or recorded**" | — | entry B | `no-change` | As row 39 |
| 43 | `plugin/instructions/plan_review_rounds.md` → `## A rejection recorded under precedence` ("This is the one exception to *\"`call stands` is unavailable for a Must Fix\"*") | — | entry B | `no-change` | Precedence resolution is unchanged by rule 2 |
| 44 | `cli/templates/state-dir/plan_revisions/README.md` ("per finding of the round") | template | entry C, `per finding of the round` | `change` | Task 1 |
| 45 | `harness-runs/plan_revisions/README.md` ("per finding of the round") | live | entry C, `per finding of the round` | `change` | Task 6 |
| 46 | `cli/templates/state-dir/test_fix_plan_reviews/README.md` ("per failed plan review") | template | entry C, `per failed` | `change` | Task 1 |
| 47 | `cli/templates/state-dir/test_fix_plan_reviews/README.md` ("a plan approved on the first pass leaves no folder behind") | template | entry C, `approved on the first pass` | `change` | Task 1 |
| 48 | `cli/templates/state-dir/test_fix_plan_reviews/README.md` ("Files appear one per failed review") | template | entry C, `per failed` | `change` | Task 1 |
| 49 | `harness-runs/test_fix_plan_reviews/README.md` ("per failed plan review") | live | entry C, `per failed` | `change` | Task 6 |
| 50 | `harness-runs/test_fix_plan_reviews/README.md` ("a plan approved on the first pass leaves no folder behind") | live | entry C, `approved on the first pass` | `change` | Task 6 |
| 51 | `harness-runs/test_fix_plan_reviews/README.md` ("Files appear one per failed review") | live | entry C, `per failed` | `change` | Task 6 |
| 52 | `cli/templates/state-dir/ui_test_plan_reviews/README.md` ("A file appears only for a failed gate: a PASS touches no disk") | template | entry C, `PASS touches no disk` | `change` | Task 1. The live copy does not exist: `phases.qa` is `false` here, so `harness-runs/ui_test_plan_reviews/` was never created |
| 53 | `cli/templates/state-dir/ui_test_plan_reviews/README.md` ("a plan that passed on the first gate") | template | entry C, `passed on the first gate` | `change` | Task 1, as row 52 |
| 54 | `cli/templates/state-dir/test_fix_point_reviews/README.md` ("per failed unit review") | template | entry C, `per failed` | `no-change` | It is a `layer-reviewer` point review of an implemented fix, not a plan review. Out of scope. |
| 55 | `harness-runs/test_fix_point_reviews/README.md` ("per failed unit review") | live | entry C, `per failed` | `no-change` | As row 54 |
