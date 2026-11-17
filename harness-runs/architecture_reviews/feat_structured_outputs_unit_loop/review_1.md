# Architecture review — round 1

verdict: PASS
review_mode: full

## Nice to Have

1. **`plugin/instructions/user_review_fixes_instructions_autonomous.md` → the `<per_unit_review>` binding row: "not the verdict parse" outlives the parse it names.** Task 1 replaces `unit_loop_core.md` → `### Per-unit review step`'s *"Parse the reviewer's return:"* with a read through `agent_return_contract.md` → `## Reading a return`. After that, the fork's binding row still says the fork restates *"not the dispatch block, not the verdict parse, not the cap"*. Scope register row 61 already accepts the same phrase in `plan_orchestration_instructions_autonomous.md` as naming a section of the cited loop. This is wording, not a placement or dependency-direction defect (`.claude/context/plugin.md` → `## Cores, forks and the single-owner rule` holds either way, because the fork still restates nothing). Reword it only if a task already touches that row.
