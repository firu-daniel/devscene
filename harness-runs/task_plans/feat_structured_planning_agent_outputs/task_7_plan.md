### Task 7 — Read the planning writers' return fields in the semi-autonomous and autonomous planning forks

**Goal:** Make the two planning forks' binding values and overrides name the planning writers' and reviewers' returns by `outcome` and by field, in the citation form `` `<agent>.<field>` ``, so the questions a park writes, the summary a hand-off emits and the UI-test-plan commit trigger read the same return the core checked.

**Depends on:** Task 6, whose core reads every return through `plugin/instructions/agent_return_contract.md` → `## Reading a return` before any fork site acts on it — so the forks do not point at that module and do not re-check. Tasks 2 and 3 declare the fields used here: `` `task-plan-writer.questions` ``, `` `task-plan-writer.tasks_count` ``, `` `task-plan-writer.parity_exclusions` ``; `` `ui-tests-plan-writer.questions` ``, `` `ui-tests-plan-writer.reason` ``; the outcomes `questions`, `blocker`, `no_ui` and the reviewers' `PASS`.

**Where this task stops.** The clarification-channel file format (`## Clarification channel — file format (canonical, single source of truth)` in the autonomous fork) is unchanged: it already asks for one `## Q<k> — <decision needed>` section per question, and each `questions` item is one question. The driver renders the same items the same way on the script-driven path (Task 11). No fork gains a binding or loses one, and `## What this file does NOT redefine` / `## What this fork does NOT redefine` stay accurate.

### Targets

- `plugin/instructions/task_plan_writing_instructions_semi_autonomous.md`
- `plugin/instructions/task_plan_writing_instructions_autonomous.md`

**Work:**

- [ ] Semi-autonomous fork: the `<escalate>` row (an agent returning `error:` / `blocker:` → a `blocker` outcome, or a return the core passed as `error` after its third failed check); the `<ask>` row (surface the writer's `questions` items — `` `task-plan-writer.questions` `` or `` `ui-tests-plan-writer.questions` `` — verbatim); `### \`<terminal_handoff>\` — Present to user` steps 1 and 2 (the `no_ui` outcome; the task count from `` `task-plan-writer.tasks_count` ``; the excluded or deferred behaviours from `` `task-plan-writer.parity_exclusions` ``, with the same parity-on-only and "none reported" rules).
- [ ] Autonomous fork, bindings: the `<ask>` row and `### \`<escalate>\` / \`<ask>\` — the headless clarification reroute` (fires on a writer's `questions` outcome; the headless park writes one `## Q<k>` section per `questions` item; the manual entry point surfaces the items live; an agent's `blocker` outcome, or a return passed as `error`, is a blocker site); `### \`<terminal_handoff>\` — no approval gate` (both loops' convergence conditions by `outcome` — the task-plan round all `PASS`, the UI loop's reviewer `PASS` or the writer's `no_ui`; the summary's task count and parity exclusions by field).
- [ ] Autonomous fork, the UI-test-plan commit override: its **Trigger (when it fires).** (the `ui-tests-plan-reviewer`'s `outcome` of `PASS`) and its **`no_ui: true` short-circuit** paragraph (the `no_ui` outcome; keep the paragraph's bold lead-in recognisable and its "keep this separate from the run-mode skip" rule).

**Verification:**

- `git grep -nE 'verdict: (PASS|FAIL)|no_ui: true|## Questions|## Parity exclusions|error:' -- plugin/instructions/task_plan_writing_instructions_semi_autonomous.md plugin/instructions/task_plan_writing_instructions_autonomous.md` prints no line that reads a retired form of a planning agent's return. (A `## Questions` heading of another agent's return, if any line names one, is not this branch's.)
- Every `` `<agent>.<field>` `` citation in the two forks names a property the story index `## Context` field table lists for that agent.
- Each fork's binding table still carries exactly the five bindings `task_plan_writing_instructions_core.md` → `## Mode contract — bindings this file uses` declares.

**Deviations from plan:**

- The first verification grep also matched sites outside the Work list that read a retired form, so they were rewritten to the `outcome` form as well: both forks' `## What … NOT redefine` → `## UI-test-plan write loop` bullet (`no_ui: true` hand-off note / short-circuit → the core's **No-UI short-circuit** / the `no_ui` short-circuit); in the autonomous fork, Override 3's no-idempotency-guard sentence and **Push after the commit.** paragraph, Override 4's **Trigger (when it fires).** and Override 5's `P2` bullet. Without them the grep prints lines that read a retired return form.
- The semi-autonomous hand-off's UI-test count and the autonomous summary's `tests_count` now cite `` `ui-tests-plan-writer.tests_count` `` too (a field the story index lists), so both hand-offs name every writer field they read by citation.
- The verification grep still prints one line, autonomous Override 5 **Self-pause on API overload during planning.**: its `error:` match is the quoted API message `an API error: API Error: 529 Overloaded`, not an agent return.
