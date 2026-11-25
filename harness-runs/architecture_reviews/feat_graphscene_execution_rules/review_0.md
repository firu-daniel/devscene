# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` — `NodeRecord` repeats the shape of the existing `GateRecord` without saying why it is a separate type.** Task 1 declares `NodeRecord(node: str, outcome: str, detail: str | None)` in `graphscene/src/graphscene/model/run_control.py`. `graphscene/src/graphscene/model/walk_actions.py` already declares `GateRecord(gate: str, outcome: str, detail: str | None)`, which is a frozen `model` type with the same three fields. The two do mean different things. `GateRecord` is a passage the walk records for a round's gate. `NodeRecord` holds the arguments to `Walker.next(outcome, node, detail)`, and it applies to any dispatched node, a plain `Dispatch` included. So this is not a layer violation. Even so, `.claude/context/conventions.md` → `### Where a new responsibility goes` says *"A responsibility that already has a home does not get a second one"*, and `.claude/context/conventions.md` → `## Shared code, and where it lives` gives the drift risk (*"Before adding a copy of anything, grep for it"*). An implementer or reviewer who comes across both types will ask why there are two. Suggested change: in Task 1's docstring bullet, add one sentence saying why `NodeRecord` is not `GateRecord`: it is a dispatched node's settlement passed to `Walker.next`, not a round's recorded passage. Alternatively, reuse `GateRecord` if Task 4's records only ever come from round gates. They do not, because `execute_set` also takes a single `Dispatch`, so the docstring sentence is the likelier fix.

## Nice to Have

1. **`task_1_plan.md` → `**Verification:**` — *"`graphscene.model.walk_actions` if needed"*.** Task 1's own declarations need no `walk_actions` name: `Dispatch` is used only in Tasks 2 and 4. The Verification bullet would be more precise if it named only `graphscene.model.execution` (for `NodeResult`) besides the standard library.
