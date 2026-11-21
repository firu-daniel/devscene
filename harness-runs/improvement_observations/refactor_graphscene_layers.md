# Script-driven planning — 2026-11-21T12:20:04Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 3 denial(s)
- **cost this run:** 3 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 651s 4.293573599999999; #2 architecture_review architecture-reviewer 1/3 FAIL 135s 1.3905016; #3 plan_review task-plan-reviewer 1/3 FAIL 820s 2.9080567999999998; #4 plan_writer task-plan-writer 1/3 returned 79s 0.5027662; #5 architecture_review architecture-reviewer 1/3 PASS 117s 1.3202437999999999; #6 plan_review task-plan-reviewer 1/3 PASS 361s 2.3646125999999996
- **cost this run:** 6 node session(s)

# Task run (Phase D)

## The configured `defaultBranch` has no local ref in this checkout, so `<default_branch>`-based diffs and logs error
- **category:** agent-contract
- **evidence:** `devscene.config.json` → `defaultBranch` is `dev`; `git branch -a --list '*dev' '*main'` printed only `remotes/origin/dev`; `git log --oneline dev..HEAD` failed with `fatal: ambiguous argument 'dev..HEAD': unknown revision or path not in the working tree.`; the `statistics-plan-writer` return (Phase D, #10) reported "`git log dev..HEAD` failed because this checkout has no local `dev` branch" and fell back to `origin/dev`; the A2 `architecture-reviewer` dispatch block carries `diff_base: dev`.
- **cost this run:** 3 dispatches (A2 #5, B #6, C2 #9) carried a `context_notes:` line naming `origin/dev`, recorded in `harness-runs/dispatch_additions/refactor_graphscene_layers.md`; one writer dispatch (#10) recovered on its own.
- **hypothesis:** a guess — run copies are cut from `origin/dev` and never create a local `dev`.

## A bare read-only `shasum` call was refused in the unattended session
- **category:** tooling-gap
- **evidence:** `shasum -a 256 harness-runs/task_prompts/refactor_graphscene_layers_task_prompt.md`, issued alone at session start, was refused with "Permission to use Bash has been denied because Claude Code is running in don't ask mode."
- **cost this run:** 1 refused call; the prompt's hash was taken from the screen's `plan` output (`safe … d33121ae…`) instead.

## The story plan says three conventions-document stalenesses were "Recorded in `corpus_staleness`", but no record of them reached any artifact
- **category:** silent-failure
- **evidence:** `harness-runs/story_plans/refactor_graphscene_layers_story_plan.md` → `## Scope register`, rows 9, 10 and 11 each say "Recorded in `corpus_staleness`"; planning was script-driven in an earlier session, so this session never received a `task-plan-writer.corpus_staleness` field; the A2 `architecture-reviewer` return (#5) stated "The story plan says this was 'Recorded in `corpus_staleness`', but I found no such record among the committed run files."
- **cost this run:** the stale `_NEGATIVES` path in `.claude/context/conventions.md` → `## What accompanies a new unit of each kind` (not on the task prompt's owed-after-merge list) reached the hand-off only through `branch-reviewer.questions`.

## Three end-of-branch reviewers produced no change on this branch
- **category:** optimization
- **evidence:** A2 `architecture-reviewer` (#5), B.2 `review-plan-reviewer` (#7) and C2 `skeptic-reviewer` (#9) each ran once over the branch, each returned `PASS`, and none wrote a file (`harness-runs/architecture_branch_reviews/refactor_graphscene_layers_arch_review.md`, `harness-runs/review_plan_reviews/refactor_graphscene_layers/` and `harness-runs/skeptic_reviews/refactor_graphscene_layers_skeptic_review.md` all absent).
- **cost this run:** 3 dispatches, unit count 1 (the branch).
