# Code Review: feat_structured_outputs_branch_review

## Context

**Branch:** `feat_structured_outputs_branch_review`
**Date:** 2026-11-17
**Reviewed:** the whole branch diff against the default branch, `dev`. The checkout has no local `dev`, so the base is `origin/dev` at `82ad4406`. The diff is 25 files, +367 / −149, across Tasks 1–6:

- the five new schema files under `plugin/schemas/`, for `review-plan-reviewer`, `branch-reviewer`, `skeptic-reviewer`, `user-review-fix-plan-writer` and `statistics-plan-writer`;
- the `## Output contract` / `### Return fields` rewrite in each of those five agent definitions;
- every caller that moved onto the field-citation form: the orchestration core and its autonomous fork, the supervised code-review, code-review-fix and user-review-fix flows, the user-review-fix core and its autonomous fork, the user-review fix-plan writing core and both of its forks, `branch-start-user-review-fix-plan.md`, `untrusted_input.md` and `improvement_observations_instructions.md`;
- the `## A return that fails the check` amendment and the three new roster lines in `agent_return_contract.md`;
- the `not_written` decision recorded in `docs/structured-agent-returns.md`.

18 run-artifact files excluded from the reviewed diff.

**What was checked:**

- **Schemas against prose.** Each schema is in the closed dialect. Its properties match the agent's `### Return fields` bullet for bullet, and its non-string type annotations agree.
- **Return-block sentence.** All five definitions carry the canonical sentence verbatim in `## Output contract`. Finding 2 is about where `skeptic-reviewer` places it.
- **Callers.** Every `` `<agent>.<field>` `` citation resolves to a property of the named schema. Every plugin file that points at `agent_return_contract.md` is on its `## Who may cite this` roster.
- **Old literals.** A grep over `plugin/` and `cli/templates/scripts` finds no surviving reader of these five agents' old literals: `verdict:`, `index_path:`, `Pass 2 carried over`, `## Questions`, `fix_plan_file:`, `statistics_file:` and the `error:` return. The `verdict:` hits that remain belong to `qa-tester`, `docs-reviewer` and the round-file content, all out of this branch's scope.
- **Goal 3.** It holds: all five `statistics-plan-writer` dispatch sites name the `not_written` route as their own `error` route, and the amended module takes that route ahead of the `flow-walker.sh` and `<escalate>` fallbacks.
- **The `general` layer, against `.claude/context/conventions.md`.** `docs/structured-agent-returns.md` is the only changed path in the `general` layer (`path: "."`). It is clean against both rules that bind it:
  - **`### Where a new responsibility goes`.** The added paragraph under ``### An agent's own `error:` return becomes an outcome, never `error` `` records a decision of record: `statistics-plan-writer`'s `error:` became `not_written`. Its home is `docs/`, and the edit puts it there. No plugin file restates the decision. The schema and the dispatch sites carry the behaviour; the doc carries the decision and its reason.
  - **`## Documents of record`.** The paragraph states no measured fact, so the *"what was measured, the command and the exact message"* rule has nothing to bind. It introduces no deferral either: the sentence *"the outcome each such agent takes is decided by the branch that adopts it"* predates this branch, which only removed `statistics-plan-writer` from the *"among them"* list ahead of it. So the numbered-roadmap-item rule has no new deferral to grade. The paragraph's claims resolve. `plugin/schemas/statistics-plan-writer.return.json` carries `not_written` with `cause`. The Goal 3 check above confirms the five dispatch sites. The amended `## A return that fails the check` takes a named route ahead of the `flow-walker.sh` and blocker-route fallbacks, as the paragraph says.
- **`harness-runs/lessons.md` → `## Agent prose`, the three lessons the diff exhibits beyond Finding 1's.** All three are clean:
  - **Shared module carries only what its runtime reader acts on.** The `agent_return_contract.md` amendment is routing content. An orchestrating caller acts on it at the third failing return to choose its route, and the precedence is now *named `error` route*, then `--outcome error`, then the blocker route. It is not an authoring rule for maintainers. The three roster lines extend the pre-existing `## Who may cite this` list in its existing form, and add no new kind of content to the module.
  - **Agent growth is paid for by behaviour** (`.claude/context/plugin.md` → `## Writing agent prose`). Four definitions shrink or hold their line count: `review-plan-reviewer` +12/−17, `skeptic-reviewer` +17/−17, `statistics-plan-writer` +18/−22, `user-review-fix-plan-writer` +18/−19. `branch-reviewer` grows by +17/−8, and the net lines are its new `### Return fields` list: nine fields, each one a value the agent emits and the caller reads. The added lines carry no rationale, and nothing in them restates a rule another file owns. The canonical return-block sentence is required wording, and the `## Unsolicited dispatch guidance` placement line replaces the old prose-summary line rather than adding a second one. The clause *"Not written into any saved file"* now appears on each of the three Pass 2 count fields. That is a per-field edge case the agent acts on, not a rule another file owns, and this change adds behaviour. So neither the growth rule nor the give-back-words lesson binds it.
  - **A routed value is one token with no space.** Every outcome the five schemas introduce is one token: `PASS`, `FAIL`, `blocker`, `returned`, `questions`, `written`, `not_written`. So are the `status` enum values `pre-user-review` and `post-user-review`. The carried-over literals keep their words: `verdict: PASS` / `verdict: FAIL` became `PASS` / `FAIL`. The bare `error:` had no words to keep, and `docs/structured-agent-returns.md` records how `not_written` was named instead.

**Not checked here:**

- **Tests.** This review ran no test suite. Whether `cli/test/agent-return-schemas.test.mjs`, the tree guard covering every changed path, passes is the Run gates phase's to establish.
- **Parity.** `phases.parity` is `false`, so parity was not reviewed.

**Pass 2:** the per-unit findings root holds no per-unit review folder, so it carried nothing over.

**Result:** one Must Fix (a lessons-ledger restatement), one Should Fix and two Nice to Have.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below top to bottom, and the commit step flips each one to `[x]` as that fix's commit lands.

- **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself.
- `[ ]` markers anywhere else, such as sub-step bullets inside a per-finding file, are informational. They are never the iteration source, and the commit step does not touch them.

Each entry resolves to `harness-runs/code_reviews/feat_structured_outputs_branch_review_code_review/finding_<K>.md` through its `**Finding K**` reference. The list is sorted with the lowest blast radius first.

1. [x] **Finding 4** — Drop the redundant "returns its return object" from the two Override D trigger sentences _(layer: plugin)_
2. [x] **Finding 3** — Fix the singular pronoun in the autonomous fork's review-questions bullet _(layer: plugin)_
3. [x] **Finding 1** — Cut the restated `not_written` route cases from the core's `<escalate>` row and both autonomous Override D gates _(layer: plugin)_
4. [ ] **Finding 2** — Move `skeptic-reviewer`'s return-block sentence ahead of its per-outcome subsections _(layer: plugin)_

---

## Must Fix

### 1. The core's `<escalate>` row and both autonomous Override D `not_written` gates restate the cases the core's `### D.1` routes
→ [finding_1.md](feat_structured_outputs_branch_review_code_review/finding_1.md)

---

## Should Fix

### 2. `skeptic-reviewer`'s return-block sentence sits under the `FAIL` subsection, leaving the `PASS` path without a return instruction
→ [finding_2.md](feat_structured_outputs_branch_review_code_review/finding_2.md)

---

## Nice to Have

### 3. Plural subject with a singular pronoun in the autonomous fork's "A review's questions are not an observation" bullet
→ [finding_3.md](feat_structured_outputs_branch_review_code_review/finding_3.md)

### 4. "returns its return object" in the two Override D trigger sentences
→ [finding_4.md](feat_structured_outputs_branch_review_code_review/finding_4.md)

---

## Out of scope / verified-OK (intentional divergences / call-outs)

These are not fixes and do not appear in the readiness list. `phases.parity` is `false`, so there is no reference implementation to diverge from and no parity call-out.

- **Verified-OK: `review-plan-reviewer.must_fix_count` and four of `statistics-plan-writer`'s count fields are not read by any caller.** The four fields are `story_points_total`, `issue_cost_total`, `story_plan_tasks` and `user_review_issues`. All of them carry over from the old `key: value` contracts, which no caller read either. This branch neither added them nor removed a reader, so they are not newly dead.
- **Verified-OK: `plugin/instructions/mode_contract.md` → the `<ask>` row still mentions "a writer's `## Questions` section".** It is a rationale clause citing `task_plan_writing_instructions_core.md`, whose writer an earlier branch moved off that section. This branch's scope register (row 64) dispositions it `no-change`, and this diff did not make it stale.
