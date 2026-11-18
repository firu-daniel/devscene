## The plan loop's cap has no recorded outcome for an operator who proceeds anyway
- **category:** agent-contract
- **evidence:** `harness-runs/flow_progress/feat_init_upgrade_progress.md` keeps `P1` at `[ ]`. `scripts/flow-walker.sh` printed `binding: <escalate>`, `reason: cap` after plan round 4, with `plan_review` open. Asked at that escalation, the operator chose to implement the current plan. No ledger marker or walker outcome records that choice, so the Phase D completion check halts on `P1` after every other phase has passed.
- **cost this run:** the run stopped before the `D` flip and the Done summary until the operator directed that `P1` be marked `[x]` with a note recording the accepted cap
- **hypothesis:** a guess only: the check is doing what it was written to do, and this case was not anticipated

## A layer-implementer finished its work and returned no return object, twice
- **category:** silent-failure
- **evidence:** dispatches #3 (Task 3) and #12 (Task 11) of the implementation half ended with a full report and no fenced `json` block, so each failed `plugin/instructions/agent_return_contract.md` (main checkout) → `## Reading a return`. Dispatches #4 and #13 repeated them, edited no file and returned `{"outcome": "implemented"}`.
- **cost this run:** 2 extra implementer dispatches, 144k subagent tokens across the two repeats

## The configured default branch has no local ref in a run copy, so `dev..HEAD` fails
- **category:** tooling-gap
- **evidence:** `architecture-reviewer` (#20), `branch-reviewer` (#26), `review-plan-reviewer` (#29, #42), `skeptic-reviewer` (#39) and `statistics-plan-writer` (#50) each reported that `dev` does not exist in this checkout and used `origin/dev` instead. Phase A2 passes `diff_base: dev`, as `defaultBranch` resolves.
- **cost this run:** none measured; each agent worked around it on its own

## Agent dispatches ran in the background although the flow requires foreground calls
- **category:** tooling-gap
- **evidence:** `plugin/instructions/task_plan_writing_instructions_core.md` (main checkout) → `## Safety contract` → **A set.** requires foreground `Agent` calls. Every `Agent` call of this run, with no background option set, returned `Async agent launched successfully`, and the returns arrived as later messages.
- **cost this run:** none measured; both gates of each plan round still ran concurrently and every return was recorded

## The plan needs a restatement of a conventions rule this branch falsified
- **category:** tooling-gap
- **evidence:** `task-plan-writer.corpus_staleness` carried one `stale-rule` entry: `.claude/context/cli.md` → `## Naming and file layout` does not name the new `cli/src/upgrade/` area that Tasks 8 to 10 add.
- **cost this run:** owes a follow-up restatement, by a supervised `/devscene:analyze cli` re-run or a hand edit

## The plan needed 5 review rounds and stopped at the revision cap
- **category:** optimization
- **evidence:** 5 distinct round indices (0 to 4) under `harness-runs/task_plan_reviews/feat_init_upgrade/` and `harness-runs/architecture_reviews/feat_init_upgrade/`. Must Fix headings per round, `task-plan-reviewer`: 12, 5, 2, 2, 3; `architecture-reviewer`: 6, 1, 1, 0, 0. Compared by heading against each reviewer's previous round, rounds 1 to 4 were all net-new with 0 re-raised (`task-plan-reviewer` 5, 2, 2, 3; `architecture-reviewer` 1, 1, 0, 0). The heading of round 4's finding 2 says it continues round 3's finding 1, which an exact-heading comparison counts as net-new.
- **cost this run:** 15 planning dispatches, and a stop for an operator decision

## Two plan reviewers raised the same `--force` wording gaps
- **category:** optimization
- **evidence:** `architecture-reviewer` listed as non-gating incidental findings the two gaps `task-plan-reviewer` graded Must Fix on the same plan: the `--force`-only statements in `cli/src/generators/permissionProfile.ts` (architecture round 3, task-plan round 3 finding 2) and the `--force left them in place` note (architecture round 4, task-plan round 4 finding 3).
- **cost this run:** none measured; one gate held each gap as non-gating while the other failed the round on it
