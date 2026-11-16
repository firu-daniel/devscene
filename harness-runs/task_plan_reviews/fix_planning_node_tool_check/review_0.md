# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_3_plan.md` — the measured-entry form asks for a command the source does not give.** The Work bullet for `### Not yet measured, and the hand step that measures it` says to record each fact "in the same form as the existing `structured_output` entry: what was measured, on which version and date, the command, and the exact output". The same file says to add "no jq command it does not state". The task prompt gives the hand sessions' launch form, but it gives no command for reading node 1's `init` event (`## Measured, 2026-11-16, Claude Code 2.1.325`: "reading the `system`/`init` event's `tools`"). An implementer told to supply "the command" may borrow the hand step's `jq -c 'select(.type == "system" and .subtype == "init") | .tools' …` read, which would attribute the recorded values to a command nobody is recorded as running. The fix: have the node-1 entry name the driver's launch as its command and say plainly that the source records no read command. That keeps `.claude/context/conventions.md` → `## Documents of record` visible without breaking the prompt's "No measured result is invented" constraint.

## Nice to Have

1. **`task_3_plan.md` / story index `## Scope register` row 9 — the hand step's comparison sentence.** The register's command entry does not reach the sentence "Compare the first read with the `tools:` line of `plugin/agents/task-plan-writer.md` in the pinned plugin; …" (`docs/flow-graph-walker.md`, closing paragraph of the hand step). Task 3's Work does handle it ("Remove the first two reads and their comparison sentence, or recast them"). Row 9 already treats the hand step as one site, so this is not a missing site. Naming the sentence in row 9's Site cell would make the closure easier to read.
