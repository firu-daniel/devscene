# Architecture review — round 1

verdict: PASS
review_mode: full

## Nice to Have

1. **`task_2_plan.md` — name the stale-rule entry in the task file as well as the index.** Task 2 adds an `## Output contract` to both mobile stubs. That breaks `.claude/context/plugin.md` → `## The sections an asset carries`: *"A declared-but-unimplemented variant carries neither"*. The task prompt requires the section (`## Scope: the agents and their current returns`: *"Each stub gains the `## Output contract` the static check requires"*). The story index records the conflict as a `stale-rule` entry (Scope register row 23), which is the route `.claude/context/conventions.md` prescribes for a rule change. So this is not a placement violation. Still, an implementer who reads only `task_2_plan.md` would not see that the conflict is known and already routed. One line under Task 2's **Goal** pointing at row 23 would close that gap.
