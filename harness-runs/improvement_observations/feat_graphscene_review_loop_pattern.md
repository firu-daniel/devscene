# Script-driven planning — 2026-11-22T12:09:46Z

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #1 plan_writer (task-plan-writer), round 0: 2 denial(s)
- **cost this run:** 2 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #2 architecture_review (architecture-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #3 plan_review (task-plan-reviewer), round 0: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## A planning node session met permission denials
- **category:** tooling-gap
- **evidence:** #6 plan_review (task-plan-reviewer), round 1: 1 denial(s)
- **cost this run:** 1 refused tool call(s)

## Script-driven planning node sessions (pd_drive returned 0)
- **category:** flow-efficiency
- **evidence:** seq node agent attempt result duration cost: #1 plan_writer task-plan-writer 1/3 returned 690s 4.3554396; #2 architecture_review architecture-reviewer 1/3 PASS 94s 1.2351120000000002; #3 plan_review task-plan-reviewer 1/3 FAIL 259s 2.7200280000000006; #4 plan_writer task-plan-writer 1/3 returned 84s 0.4429867999999999; #5 architecture_review architecture-reviewer 1/3 PASS 143s 1.5711901999999998; #6 plan_review task-plan-reviewer 1/3 PASS 339s 3.0633148000000006
- **cost this run:** 6 node session(s)

# Task run (Phase D)

## A layer-implementer's tree-guard run was refused in one unit and allowed in the others
- **category:** tooling-gap
- **evidence:** Phase A, Task 2 (`[A · Task 2 · graphscene · iter 0] → layer-implementer  (#2)`): the implementer reported `bash scripts/python-service.sh --package graphscene test tests/test_layers.py` refused ("running in don't ask mode") and returned the flag "The graphscene layer-contract tree guard (tests/test_layers.py) was not run: the command was refused." The same command ran and passed (11 tests) in the Task 1, 3 and 4 dispatches and in code-review Findings 2 and 3 and skeptic Finding 1, in the same session; commit e15c6909 carries Task 2 without the guard run
- **cost this run:** the `tests/test_layers.py` tree guard went unrun for Task 2's change to `graphscene/src/graphscene/engine/transitions.py`; it was covered only later, by the next unit's guard run and the Phase G round-1 full suite (`pass`)
- **hypothesis:** (guess) the refusal depends on the exact command form the sub-agent issued, not on the command itself
