# Story: One strict definition of a Must Fix

## Context

This branch gives every agent that grades a finding one definition of a Must Fix: four closed classes, plus a failure sentence the grader must be able to complete. `plugin/instructions/finding_grades.md` becomes the only statement of the three grades. Each grading agent points at it from its reading list, keeps its own lens and checklist, and maps each of its Must Fix triggers to a class in a `### Must Fix triggers` table. Every Must Fix entry records `**Class:**` and `**Failure:**`. Should Fix and Nice to Have stay, and a planning-round Should Fix is handled exactly as it is today.

Two enforcement paths carry the new fields. `review-plan-reviewer` checks them on code and skeptic reviews, and sends an entry that does not hold up back to `## Should Fix`. No agent meta-reviews a plan round, so plan rounds get a scripted check, `fw_round_file_check` in `lib/flow-walker-gates.sh`.

**The round-file contract the check enforces.** A round file is valid when it carries exactly one `verdict:` line and:

- on `verdict: FAIL`, at least one numbered entry at column 0 under `## Must Fix`, each with a non-empty `**Class:**` line and a non-empty `**Failure:**` line;
- on `verdict: PASS`, no numbered entry under `## Must Fix`.

The check proves the fields are present, not that the reasoning is right.

**How a refused reviewer is sent back.** The walker runs the check when a round gate's `PASS` or `FAIL` is recorded. A refused file records no verdict. The set's other gates finish first, then the refused gates are dispatched again as one set in the same round, and each reviewer replaces its own `review_<n>.md`. The round number and the loop counter do not move, so the five-round cap is unchanged, and each re-dispatch counts against `MAX_TOTAL_DISPATCHES`. A gate's third refusal in a round is held as `error`, and the join escalates it. `bash <scripts_dir>/flow-walker.sh check-round-file --findings <path>` exposes the same check to the prose-routed user-review fix-plan rounds. Its exit 3 means the walker read the file and found it invalid, and only that status counts as a return that fails the check; any other non-zero exit, including an older walker's refusal of the unknown subcommand, is a held binding at once, with no reviewer re-dispatch. The check covers round gates only: `ui_review` and the test-fix plan's architecture review are not rounds, so their entries carry the fields by contract alone.

The work ships bottom-up: the walker and its tests (`cli`), then the grades file, the agents and the flow cores (`plugin`), then the decision record, the roadmap and this repository's self-adopted copies (`general`).

**Top risks:** a new walker running beside an older plugin would refuse every `FAIL` round file, because older reviewers write neither field; Task 13 records that an adopter updates both together, and Task 15 syncs this repository's copies last. A trigger table that silently lowers a real check would weaken review, so Tasks 5–10 change a grade only where this plan names the regrade. Resuming a round whose files predate the fields reads them as `unreadable` and re-opens the whole set; Task 1 tests that this never sends such a file to the writer.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** Only the committing role flips a marker to `[x]`: the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, and the orchestrator itself in the supervised flow, which runs none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers elsewhere, such as sub-step bullets in per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_must_fix_definition/task_<K>_plan.md`. Entries follow the configured layer order, with the catch-all layer last.

1. [x] **Task 1** — Add the round-file check to the walker's gate library _(layer: cli)_ _(points: 20)_
2. [x] **Task 2** — Refuse an invalid round file in the walker and expose the check _(layer: cli)_ _(points: 20)_
3. [x] **Task 3** — Prove the driver re-dispatches a refused gate and correct the state-dir READMEs _(layer: cli)_ _(points: 10)_
4. [x] **Task 4** — Create `finding_grades.md` and extend the Must Fix entry _(layer: plugin)_ _(points: 15)_
5. [x] **Task 5** — Move `task-plan-reviewer` and its register gaps onto the definition _(layer: plugin)_ _(points: 20)_
6. [ ] **Task 6** — Make `review-plan-reviewer` check and regrade Must Fix entries _(layer: plugin)_ _(points: 15)_
7. [ ] **Task 7** — Move `branch-reviewer` and `skeptic-reviewer` onto the definition _(layer: plugin)_ _(points: 20)_
8. [ ] **Task 8** — Move `layer-reviewer` and `ui-tests-plan-reviewer` onto the definition _(layer: plugin)_ _(points: 20)_
9. [ ] **Task 9** — Move `architecture-reviewer` and `business-parity-reviewer` onto the definition _(layer: plugin)_ _(points: 15)_
10. [ ] **Task 10** — Move the fix-plan writers and `qa-tester` onto the definition _(layer: plugin)_ _(points: 15)_
11. [ ] **Task 11** — Update the samples, dispatch discipline and the flow map _(layer: plugin)_ _(points: 10)_
12. [ ] **Task 12** — Route refused round files through both planning cores _(layer: plugin)_ _(points: 15)_
13. [ ] **Task 13** — Record the round-file check decision _(layer: general)_ _(points: 8)_
14. [ ] **Task 14** — Mark `Review severity markers` done in the roadmap _(layer: general)_ _(points: 5)_
15. [ ] **Task 15** — Sync the self-adopted copies and run the closure checks _(layer: general)_ _(points: 8)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"`plugin/instructions/finding_grades.md` is the only statement of the grades. Every agent that grades a finding points at it, and no competing definition or restatement remains under `plugin/`."*

The register also covers the durable text this branch's round-file behaviour and roadmap change would otherwise leave false.

**E1 — competing grade statements (command).** `git grep -lE 'Grade every finding by consequence|Must Fix is reserved for|real and impactful|would do the wrong thing|is a \*\*Must Fix\*\* unless noted|every fixable failure|severity rubric|[Tt]he rubric|dressed up as Must Fix|ladder above' -- plugin`

**E2 — assets that write or read Must Fix findings (command).** `git grep -lE '## Must Fix|must_fix_count|valid_must_fix' -- plugin/agents plugin/commands plugin/instructions plugin/samples`

**E3 — statements of the round-file contract (command).** `git grep -lE 'The Must Fix entry|Raised against|`verdict: (PASS|FAIL)`|round file|replaced only by its own reviewer' -- plugin docs cli/templates/state-dir cli/templates/scripts/README.md 'harness-runs/*/README.md' ':!docs/work-report-research' ':!docs/rag-extraction-research'`

**E4 — prose naming the walker (command).** `git grep -lE 'flow-walker\.sh|fw_review_verdict' -- plugin docs cli/templates/scripts/README.md ':!docs/work-report-research' ':!docs/rag-extraction-research'`

**E5 — the roadmap item (command).** `git grep -l 'Review severity markers' -- . ':!harness-runs'`

**E6 — sample Must Fix findings (procedure).** **Artifact:** `plugin/samples/sample_code_review.md` and `plugin/samples/sample_user_review_fix_plan.md`. **Traversal:** in each, the `### N. Title` pointers under `## Must Fix`, in file order. **Decision rule:** the `finding_<N>.md` each pointer names is reached, because a Must Fix finding file carries the two new fields.

**E7 — standing ledger rows (procedure).** **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`. **Artifact:** that ledger. **Traversal:** its topic headings in file order, then the rules under each. **Decision rule:** a rule is reached when it states what grade a finding takes. No rule meets it today, so this entry adds no row.

**Closure invariant:** every site any derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/agents/task-plan-reviewer.md` → `## What to check` | — | E2, E3 | `change` | Task 5 |
| 2 | `plugin/agents/review-plan-reviewer.md` → `### False positives (Must Fix)` | — | E1, E2 | `change` | Task 6 |
| 3 | `plugin/agents/branch-reviewer.md` → "Grade every finding by consequence" | — | E1, E2 | `change` | Task 7 |
| 4 | `plugin/agents/skeptic-reviewer.md` → "Grade every finding by consequence" | — | E1, E2 | `change` | Task 7 |
| 5 | `plugin/agents/layer-reviewer.md` → `## Checklist` | — | E1, E2 | `change` | Task 8 |
| 6 | `plugin/agents/ui-tests-plan-reviewer.md` → `## What to check` | — | E1, E2 | `change` | Task 8 |
| 7 | `plugin/agents/architecture-reviewer.md` → "A violation is a **Must Fix** unless noted" | — | E1, E2, E3 | `change` | Task 9 |
| 8 | `plugin/agents/business-parity-reviewer.md` → "A violation is a **Must Fix** unless noted" | — | E1, E2, E3 | `change` | Task 9 |
| 9 | `plugin/agents/user-review-fix-plan-writer.md` → "real and impactful" | — | E1, E2 | `change` | Task 10 |
| 10 | `plugin/agents/test-fix-plan-writer.md` → "every fixable failure" | — | E1, E2 | `change` | Task 10 |
| 11 | `plugin/agents/qa-tester.md` → `### 2. Some tests fail` | — | E2 | `change` | Task 10 |
| 12 | `plugin/agents/layer-implementer.md` → "would do the wrong thing, or fail to do a required thing" | — | E1 | `no-change` | A test for keeping a comment line; it grades no finding |
| 13 | `plugin/agents/ui-tests-plan-writer.md` → "no `## Must Fix` etc." | — | E2 | `no-change` | States that a plan index has no findings sections |
| 14 | `plugin/commands/branch-status.md` → "Must Fix (open)" | — | E2 | `no-change` | Reports existing sections and defines no grade |
| 15 | `plugin/commands/branch-start-plan-autonomous.md` (walker citation) | — | E4 | `no-change` | Names the walker; its commands do not change |
| 16 | `plugin/commands/branch-start-plan-semi-autonomous.md` (walker citation) | — | E4 | `no-change` | Names the walker; its commands do not change |
| 17 | `plugin/instructions/plan_review_rounds.md` → `## The Must Fix entry` | — | E2, E3 | `change` | Task 4 |
| 18 | `plugin/instructions/dispatch_discipline_instructions.md` → "**Case 2 —" | — | E1 | `change` | Task 11 |
| 19 | `plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker` | — | E3, E4 | `change` | Task 12 |
| 20 | `plugin/instructions/user_review_fix_plan_writing_instructions_core.md` → `## Flow` step 7 | — | E2, E3 | `change` | Task 12 |
| 21 | `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md` → "24 still holds" | — | E2, E3 | `change` | Task 12 |
| 22 | `plugin/instructions/user_review_fix_plan_writing_instructions.md` → "this flow invokes no wrapper script" | — | E2 | `change` | Task 12 |
| 23 | `plugin/instructions/task_plan_writing_instructions_autonomous.md` (round commits) | — | E3, E4 | `no-change` | A refused file prints no `round:` line, so its commit points do not change |
| 24 | `plugin/instructions/plan_orchestration_instructions_core.md` → `must_fix_count` routing | — | E2 | `no-change` | Routes on a count whose meaning holds |
| 25 | `plugin/instructions/plan_orchestration_instructions_autonomous.md` → "carry a `verdict: FAIL` line" | — | E3 | `no-change` | Counts failed rounds, which is still true |
| 26 | `plugin/instructions/user_review_fixes_instructions_autonomous.md` → "carry a `verdict: FAIL` line" | — | E3 | `no-change` | Counts failed rounds, which is still true |
| 27 | `plugin/instructions/autonomous_pause_and_ledger.md` → "each gate replacing its own round file" | — | E3 | `no-change` | Its resume rule still holds |
| 28 | `plugin/instructions/unit_loop_core.md` → `## Must Fix` prefix mapping | — | E2 | `no-change` | Reads section names; each reviewer's table carries the class for its test-run triggers |
| 29 | `plugin/instructions/agent_return_contract.md` (walker fallback) | — | E4 | `no-change` | The core applies this route to a refused file without changing it |
| 30 | `plugin/docs/AUTONOMOUS_FLOW.md` → canonical file table | — | E4 | `change` | Task 11 |
| 31 | `plugin/samples/sample_code_review.md` → `## Must Fix` | — | E2 | `no-change` | The index keeps pointers only |
| 32 | `plugin/samples/sample_user_review_fix_plan.md` → `## Must Fix` | — | E2 | `no-change` | The index keeps pointers only |
| 33 | `plugin/samples/sample_code_review/finding_1.md` | — | E6 | `change` | Task 11 |
| 34 | `plugin/samples/sample_user_review_fix_plan/finding_2.md` | — | E6 | `change` | Task 11 |
| 35 | `plugin/schemas/task-plan-reviewer.return.json` ("round file") | — | E3 | `no-change` | The return shape does not change |
| 36 | `plugin/schemas/architecture-reviewer.return.json` ("round file") | — | E3 | `no-change` | The return shape does not change |
| 37 | `plugin/schemas/business-parity-reviewer.return.json` ("round file") | — | E3 | `no-change` | The return shape does not change |
| 38 | `cli/templates/state-dir/task_plan_reviews/README.md` → "replaced only by its own reviewer" | template | E3 | `change` | Task 3 |
| 39 | `harness-runs/task_plan_reviews/README.md` → same sentence | self-adopted | E3 | `change` | Task 15 |
| 40 | `cli/templates/state-dir/architecture_reviews/README.md` → same sentence | template | E3 | `change` | Task 3 |
| 41 | `harness-runs/architecture_reviews/README.md` → same sentence | self-adopted | E3 | `change` | Task 15 |
| 42 | `cli/templates/state-dir/architecture_user_review_reviews/README.md` → same sentence | template | E3 | `change` | Task 3 |
| 43 | `harness-runs/architecture_user_review_reviews/README.md` → same sentence | self-adopted | E3 | `change` | Task 15 |
| 44 | `cli/templates/state-dir/business_parity_reviews/README.md` → same sentence | template | E3 | `change` | Task 3 |
| 45 | `cli/templates/state-dir/business_parity_user_review_reviews/README.md` → same sentence | template | E3 | `change` | Task 3 |
| 46 | `cli/templates/state-dir/plan_revisions/README.md` → "per Must Fix of the round" | template | E3 | `no-change` | The note's contract does not change |
| 47 | `harness-runs/plan_revisions/README.md` → same sentence | self-adopted | E3 | `no-change` | The note's contract does not change |
| 48 | `cli/templates/scripts/README.md` (walker row) | — | E4 | `no-change` | Names the script family; no new file ships |
| 49 | `docs/flow-graph-walker.md` → `### Item 8` | — | E3, E4 | `change` | Task 13 |
| 50 | `docs/converging-plan-reviews.md` → "the Must Fix entry" | — | E3, E4 | `no-change` | It points at the owning file and restates no field |
| 51 | `docs/structured-agent-returns.md` → "`verdict:` lines inside a round file" | — | E3, E4 | `no-change` | Still true: those lines are file content |
| 52 | `docs/development.md` (round-file and walker mentions) | — | E3, E4 | `no-change` | Neither mention states what the walker reads from a round file |
| 53 | `docs/github-integration-research.md` → "round file's file-and-line list" | — | E3 | `no-change` | Means a user-review round, not a plan round |
| 54 | `docs/github-run-control.md` → "newest round file" | — | E3 | `no-change` | Means a user-review round, not a plan round |
| 55 | `docs/second-runtime-port-decision.md` → "`verdict: FAIL` sends the plan back" | — | E3 | `no-change` | A dated decision record of the routing it compared |
| 56 | `docs/cli.md` (walker mention) | — | E4 | `no-change` | No command or written file changes |
| 57 | `docs/sandbox-verification.md` (walker mention) | — | E4 | `no-change` | A record of past measurements |
| 58 | `docs/watcher.md` (walker mention) | — | E4 | `no-change` | The driver's behaviour it describes does not change |
| 59 | `ROADMAP.md` → `Review severity markers` | — | E5 | `change` | Task 14 |
| 60 | `plugin/instructions/finding_grades.md` → `## Must Fix` | — | E2 (reached once Task 4 lands) | `change` | Task 4 |
