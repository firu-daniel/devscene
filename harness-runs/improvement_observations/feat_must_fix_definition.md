# Script-driven planning — 2026-11-18T11:57:18Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 784s 6.5315282; #2 architecture_review architecture-reviewer 1/3 PASS 296s 2.7979174; #3 plan_review task-plan-reviewer 1/3 FAIL 581s 5.159500599999999; #4 plan_writer task-plan-writer 1/3 returned 141s 1.03081; #5 architecture_review architecture-reviewer 1/3 PASS 243s 2.376761; #6 plan_review task-plan-reviewer 1/3 FAIL 601s 5.355733000000001; #7 plan_writer task-plan-writer 1/3 returned 65s 0.5363704000000001; #8 architecture_review architecture-reviewer 1/3 PASS 50s 0.8956229999999998; #9 plan_review task-plan-reviewer 1/3 PASS 82s 1.1806246
- **cost this run:** 9 node session(s)

# Task run (Phase D)

## The configured default branch has no local ref in this run copy
- **category:** agent-contract
- **evidence:** `git rev-parse --verify dev` printed `fatal: Needed a single revision`. The Phase A2 `architecture-reviewer`, Phase B `branch-reviewer`, Phase B.2 `review-plan-reviewer`, Phase C2 `skeptic-reviewer` and Phase D `statistics-plan-writer` each reported that `dev` does not exist here and that they used `origin/dev`. The A2 dispatch block carried `diff_base: dev` as `plan_orchestration_instructions_core.md` writes it (main checkout).
- **cost this run:** five agents each substituted the base on their own; the Phase-D `git log` over `dev..HEAD` was issued against `origin/dev` instead

## Implementer file-management commands were refused
- **category:** tooling-gap
- **evidence:** Task 1 and Task 2 implementers reported `rm` refused, leaving `harness-runs/scratch/stub-must-fix-probe.mjs` and `harness-runs/scratch/walker_repro.mjs` on disk. The Task 15 implementer reported both `cp` calls refused and wrote `scripts/flow-walker.sh` and `scripts/lib/flow-walker-gates.sh` with the file-edit tool, confirming them with `cmp`. The Task 7 implementer reported a compound byte comparison refused and compared two paragraphs by reading `grep` output.
- **cost this run:** two ignored scratch files left behind; one planned copy replaced by edits; one byte comparison replaced by reading

## The skeptic reviewer could not run a measurement it attempted
- **category:** tooling-gap
- **evidence:** the Phase C2 `skeptic-reviewer` return states it could not measure how past round files fit the column-0 entry format "because that command was denied".
- **cost this run:** that compatibility question was left unmeasured at Phase C2

## A Should Fix from a passing branch review exists only in the reviewer's reply
- **category:** silent-failure
- **evidence:** the Phase A2 `architecture-reviewer` returned `PASS` and reported a Should Fix against `plugin/agents/task-plan-reviewer.md` (it restates the grade test `plugin/instructions/finding_grades.md` owns), adding "Because no file is written on a pass, this finding exists only in this reply". `harness-runs/architecture_branch_reviews/feat_must_fix_definition_arch_review.md` does not exist.
- **cost this run:** the finding entered no fix loop; it reaches the branch only through this entry and the Done summary

## Reviews on this branch were graded under the main checkout's plugin, not the branch's
- **category:** shared-state
- **evidence:** the Phase B.2 `review-plan-reviewer` reported that `harness-runs/code_reviews/feat_must_fix_definition_code_review/finding_1.md` is a Must Fix with no `**Class:**` or `**Failure:**` line, and passed it because the run is graded against `plugin/samples/` (main checkout), while this branch's `plugin/agents/branch-reviewer.md` requires both fields.
- **cost this run:** the branch's own Must Fix contract was not applied to its own code review

## The plan needed three review rounds
- **category:** optimization
- **evidence:** rounds 0, 1 and 2 under `harness-runs/task_plan_reviews/feat_must_fix_definition/` and `harness-runs/architecture_reviews/feat_must_fix_definition/`. `task_plan_reviews`: round 0 `FAIL` with 7 entries; round 1 `FAIL` with 3 net-new, 0 re-raised; round 2 `PASS` with 0. `architecture_reviews`, all `PASS`: round 0 with 2 entries; round 1 with 2 net-new, 0 re-raised; round 2 with 1 net-new, 0 re-raised. Headings were compared exactly; the `grep` used also printed the full text of Should Fix entries written on one line.
- **cost this run:** 9 planning node sessions

## A plan-review Should Fix returned as a code-review finding
- **category:** optimization
- **evidence:** titles compared. `harness-runs/task_plan_reviews/feat_must_fix_definition/review_1.md` Should Fix 1, "A refused gate re-dispatched through `current` still counts as not running", matches code-review Finding 1, "`current` re-prints a refused gate the walker still counts as not out, so the gate is dispatched twice". Its Should Fix 2, on register row 58 and `docs/watcher.md`, matches code-review Finding 3, "`docs/watcher.md` omits `check-round-file` and the user-review fix-plan caller".
- **cost this run:** 2 of 4 code-review findings had been raised at planning; fixing them took 3 implementer dispatches

## Three end-of-branch reviews produced no change
- **category:** optimization
- **evidence:** Phase A2 `architecture-reviewer`, Phase B.2 `review-plan-reviewer` and Phase C2 `skeptic-reviewer` each ran once over the branch and returned `PASS`, with no findings file and no fix commit.
- **cost this run:** 3 dispatches, 1 pass each

# User-review fix round 1 — two-leg divergence row and the Must Fix triggers corpus test

## A per-unit Should Fix passes the unit and is summarised as Nice to Have
- **category:** agent-contract
- **evidence:** `layer-reviewer` returned `PASS` on Item 1 (`plugin`) and Item 2 (`cli`), each return reporting one Should Fix, in `harness-runs/user_review_fix_plan_point_reviews/feat_must_fix_definition_fix_plan/item_1/review_0.md` and `item_2/review_0.md`. `plugin/agents/layer-reviewer.md` (main checkout) case 2 returns `PASS` for Should Fix findings, while `plugin/instructions/user_review_fixes_instructions_core.md` (main checkout) → `### D.2 Done summary` says such files hold Nice to Have observations because "Must Fix / Should Fix would have triggered FAIL".
- **cost this run:** 2 Should Fix findings entered no fix iteration and remain open on the branch

## Agent probe and cleanup commands were refused
- **category:** tooling-gap
- **evidence:** the `user-review-fix-plan-writer` return states its scratch script was refused; the fix-plan `architecture-reviewer` return states its prototype of the planned audit was denied; the Item 2 `cli` and `general` `layer-reviewer` returns state their cleanup commands were denied, leaving `harness-runs/scratch/layer_review_triggers_probe.mjs` and `harness-runs/scratch/item2_general_audit_probe.mjs`.
- **cost this run:** the plan's matching lists were written and gated without being executed, and the first test run needed one added `NOT_A_GRADE` entry; two ignored scratch files left behind

## The ledger re-seed rule names no case for a task-engine ledger
- **category:** agent-contract
- **evidence:** `harness-runs/flow_progress/feat_must_fix_definition_progress.md` opened this round with the header `(engine: task)`, which carries no round. `plugin/instructions/autonomous_pause_and_ledger.md` (main checkout) § 1.4 decides by comparing header rounds: equal, older or absent. The run treated it as older and re-seeded in commit 51706719.
- **cost this run:** one decision taken by inference; no rework

## The configured default branch has no local ref in this run copy
- **category:** agent-contract
- **evidence:** the Phase D `statistics-plan-writer` return states `dev` has no local ref and that it read the range from `origin/dev`. This session's disposition and index-only history reads also used `origin/dev..HEAD`.
- **cost this run:** one agent substituted the base on its own

## The per-unit reviewer and the fix-plan gate produced no change
- **category:** optimization
- **evidence:** `layer-reviewer` ran 3 times across both fix items (Item 1 `plugin`, Item 2 `cli` and `general`), each returning `PASS` at iteration 0 with no fix dispatch. The fix-plan `architecture-reviewer` gate returned `PASS` on round 0 with no revision (`harness-runs/architecture_user_review_reviews/feat_must_fix_definition/user_review_1/review_0.md`).
- **cost this run:** 4 dispatches, none followed by a change
