# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_2.md` — the `plan_orchestration_instructions_autonomous.md` sub-step echoes the module's rule in a file outside the module's roster** (source: `.claude/context/plugin.md` → `## Cores, forks and the single-owner rule`, "A policy file is activated by pointer and never restated … The same rule governs every shared module here"; `## Writing agent prose`, "Drop rationale the agent does not act on. Keep every edge case.")
   The sub-step reduces the fork's parenthetical to "(the field is optional: absent or empty means none)". That is the wording the fix gives `agent_return_contract.md` → `## Reading a return` step 4, and the fork is not on that module's `## Who may cite this` roster. So the module's rule gets a second, uncited copy, which is the drift the finding sets out to remove. The fork's read of `` `task-plan-writer.corpus_staleness` `` is also not a routing-check read. The task-plan-writer's routing check runs in `task_plan_writing_instructions_core.md`, whose `returned` section does not read that field. So the existing parenthetical says what an absent field *means* for the observation, and that is the same class of line as the display-side lines the finding already lists under **Leave alone**. The current clause also carries an edge case, "never \"the planner did not check\"", which the proposed reduction drops.
   Suggested: list this parenthetical under **Leave alone** as a field-meaning statement rather than a routing-check exception. If the implementer still wants it reduced, use the pointer form plus the roster entry, which the sub-step already names as the alternative. Either way, keep the "never the planner did not check" edge case.

## Nice to Have

1. **`finding_1.md` — name the docs-record sweep explicitly.** `docs/structured-agent-returns.md` currently has no `already passing` hit, so nothing needs changing there. Adding it to **Check before closing** alongside `plugin/` would cover the decision record's outcome-value statements (`### One discriminator, `outcome`, held to the graph`) in the same grep.
