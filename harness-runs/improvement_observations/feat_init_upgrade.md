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

# User-review fix round 1 — plugin and CLI version mismatch handling, and the local-file advice for refused entries

## The fix plan needed 3 review rounds to converge
- **category:** optimization
- **evidence:** 3 distinct round indices (0 to 2) under `harness-runs/architecture_user_review_reviews/feat_init_upgrade/user_review_1/`, with verdicts FAIL, FAIL, PASS; `phases.parity` is `false`, so no parity round exists. Finding headings per round: 3, 3, 0. Compared by exact heading against the previous round, round 1 was 3 net-new and 0 re-raised, and round 2 raised none. Round 1's Should Fix 2 on `cli/src/machine/` placement covers the same subject as round 0's Should Fix 1 under a reworded heading, which an exact-heading comparison counts as net-new.
- **cost this run:** 2 writer revisions, `harness-runs/plan_revisions/feat_init_upgrade/fix_plan_1_revision_1.md` and `fix_plan_1_revision_2.md`

## The Phase D disposition command fails in a run copy with no local default branch
- **category:** tooling-gap
- **evidence:** `git log --format='%h %s%n%b' --name-only dev..HEAD`, the form `plugin/instructions/improvement_observations_instructions.md` (main checkout) → `## Dispositioned units` gives for `defaultBranch` `dev`, exited 128 with `fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree.` This session ran the disposition and index-only search over `origin/dev..HEAD` instead and matched no commit. `statistics-plan-writer` (#1) reported the same missing ref and made the same substitution.
- **cost this run:** one failed command; the search ran over a base the instruction does not name
