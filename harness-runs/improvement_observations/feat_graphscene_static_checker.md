# Script-driven planning — 2026-11-22T07:28:35Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 583s 3.9378268000000007; #2 architecture_review architecture-reviewer 1/3 PASS 93s 1.2618682; #3 plan_review task-plan-reviewer 1/3 PASS 229s 2.8583188000000006
- **cost this run:** 3 node session(s)

# Task run (Phase D)

## A task plan's combined two-file test command was refused, so the implementer ran each file separately
- **category:** tooling-gap
- **evidence:** Task 4's `layer-implementer` return (harness-runs/task_plans/feat_graphscene_static_checker/task_4_plan.md): "I ran the two files separately because the combined command from the plan was refused". It then ran `bash scripts/python-service.sh --package graphscene test tests/test_public_surface.py` (32 passed) and `… test tests/facade/test_loading.py` (33 passed) as two calls.
- **cost this run:** one refused tool call, plus a second test invocation; no coverage lost
- **hypothesis:** (guess) the unattended profile allows the single-file `python-service.sh … test <file>` form, but not the form with two path arguments that the plan wrote.

## The plan reported corpus staleness in `.claude/context/graphscene.md` and `.claude/context/conventions.md`
- **category:** tooling-gap
- **evidence:** this session resumed after script-driven planning and never saw the `task-plan-writer.corpus_staleness` return. The committed story index's `## Scope register` (harness-runs/story_plans/feat_graphscene_static_checker_story_plan.md) says rows 1 and 3–6 are "recorded in `corpus_staleness`". They are all `stale-rule` sites. In `.claude/context/conventions.md`, `## What accompanies a new unit of each kind` does not name the new `static_negative_*.json` family. In `.claude/context/graphscene.md`, `## The model and its wire form` still says the checker is a later one. In the same file, `## Errors and the loading order` still says only schema and vocabulary failures raise, and gives the old loading order. In the same file, `## Example` still says the vocabulary check runs before the builder. The Phase A2 `architecture-reviewer` return found the same three `graphscene.md` sites independently.
- **cost this run:** a follow-up restatement of `.claude/context/graphscene.md` (three sections) and of the fixture row in `.claude/context/conventions.md`, which an implementing run may not edit
