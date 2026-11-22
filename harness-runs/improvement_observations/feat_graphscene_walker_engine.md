# Script-driven planning — 2026-11-22T09:23:46Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #5 architecture_review (architecture-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 521s 3.4822911999999997; #2 architecture_review architecture-reviewer 1/3 PASS 85s 1.3341075999999998; #3 plan_review task-plan-reviewer 1/3 FAIL 239s 2.795572600000001; #4 plan_writer task-plan-writer 1/3 returned 31s 0.2815186; #5 architecture_review architecture-reviewer 1/3 PASS 94s 1.4761212000000001; #6 plan_review task-plan-reviewer 1/3 PASS 226s 2.402824
- **cost this run:** 6 node session(s)

# Task run (Phase D)

## Compound or piped Bash forms were refused on first attempt in seven implementation-half sessions
- **category:** tooling-gap
- **evidence:** orchestrator, twice (the session transcript): a read-only compound of `cd`, `grep`, `awk` and `cat` over `plugin/instructions/improvement_observations_instructions.md` (main checkout), and a `head` followed by a `for` loop over `harness-runs/task_plans/feat_graphscene_walker_engine/`, each refused with "Permission to use Bash has been denied because Claude Code is running in don't ask mode". Five sub-agent returns reported the same refusal for their first command form, each then re-run bare: layer-implementer Task 7 (a `cd` before the single-file test command), code-review Item 1 (test output piped through `tail`), code-review Item 2 (two test files in one command), skeptic Item 1 (chained and piped test runs), statistics-plan-writer (a combined `mkdir`).
- **cost this run:** 7 refused tool calls, each followed by a re-issued bare form; no unit failed for it
- **hypothesis:** (a guess) agents reach for compound shell forms by default, and only the refusal teaches them the plain single-statement form the profile allows

## A conventions document states a rule this branch falsified
- **category:** tooling-gap
- **evidence:** `stale-rule` — `.claude/context/graphscene.md` says the library "keeps no persisted or shared state", which `StateStore` and `FileStateStore` (`graphscene/src/graphscene/model/walk_state.py`, `graphscene/src/graphscene/adapters/state_file.py`) now make false. The story index's scope register records it as row 1, `no-change`, a stale rule (`harness-runs/story_plans/feat_graphscene_walker_engine_story_plan.md`), and the Phase A2 architecture-reviewer and Phase B branch-reviewer returns each flagged it as not a finding against this diff. The `task-plan-writer.corpus_staleness` return itself was produced in an earlier, script-driven planning session and was not seen by this session.
- **cost this run:** a follow-up restatement of that rule in `.claude/context/graphscene.md` is owed
