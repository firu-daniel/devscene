# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix
- `task_4_plan.md`, the **Measured, 2026-11-18: what can precede the frame.** paragraph: the Work bullets never state which Claude Code versions the 87 streams were recorded under. The only version the paragraph names is 2.1.327, attached to the park that prompted the change, so a reader can take it for the version of the whole measurement. The streams' `system` / `init` events record `claude_code_version`, and the 87 span 2.1.287 to 2.1.327. `.claude/context/conventions.md` → `## Documents of record` wants a measured fact recorded so that a later version behaving differently is detectable, and the 2026-11-17 entry beside it names its version in its heading. Have the paragraph state the range.

## Nice to Have
- `task_1_plan.md`, **The contract Tasks 2, 3 and 4 rely on.**: "A tools-used line anywhere after the frame leaves the result wrapped" is still not true of an indented line inside the reply, which is unwrapped and then refused by the parse, as the task's own fourth Work bullet says. The outcome, `malformed-verdict`, is the same either way.
