# Finding grades

## Resolved values

This file declares no token: every `<…>` name here is defined by its own text at its use site.

## Must Fix

A finding is a Must Fix only when it meets both conditions below. Otherwise it is a Should Fix, or a Nice to Have when it is style, wording or ordering.

### 1. It belongs to one of four classes

| Class | The finding must show |
|---|---|
| **Wrong behaviour** | Running the code as this change leaves it, or as the plan will build it, gives a wrong result: incorrect data or output state, a crash, data loss, a security or permission hole, a failing test or type check, or a stated requirement not met. |
| **Wrong build** | An implementer following the plan or finding as written would build the wrong thing, leave out required work, or be unable to finish: tasks that contradict each other, a missing requirement, an undefined interface, a dependency ordered too late, a forbidden test run. |
| **Wrong action from operative text** | Text would, followed literally, cause a failed or harmful action. Operative text is anything a person, an agent or a program follows or reads as input: instructions, configuration, templates, schemas, literals other files depend on, and any command, path, flag, setup step or remedy given in documentation or program output. |
| **Broken contract** | A required accompanying item is missing, a reference does not resolve, a format a parser or loop reads is broken, a layer boundary is crossed, a mandated convention is bypassed, or business logic diverges from the reference implementation while the parity phase is on. |

### 2. The grader can complete the failure sentence

`If <actor> does <step>, then <observable wrong result>.`

- `<actor>` is a named consumer: the implementer, a named agent, an adopter or the running program.
- `<step>` exists in the artifact under review, and the finding quotes it or names the code path.
- `<observable wrong result>` can be checked. "May be confused", "may believe" and "could mislead" do not qualify.

### The entry fields

Every Must Fix entry carries both lines:

- `**Class:** <class name>`
- `**Failure:** <the sentence>`

### Checklist triggers

Each trigger an agent grades Must Fix names its class in that agent's `### Must Fix triggers` table. An instance whose failure sentence can be completed cannot be downgraded. An instance whose sentence cannot be completed is a Should Fix.

## Never a Must Fix on its own

- A code comment or doc comment.
- A sentence that only describes the project and has become false, including a stale count.
- Output wording that states something inaccurate but gives no step to follow.
- A hypothetical the grader did not verify.
- A line coordinate.

## Should Fix

- A real defect that fails either Must Fix condition.
- A line coordinate in a durable artifact (an instruction file, an agent definition, a catalog document, a standing tracked artifact, a code comment), stale or not.
- A citation that locates its site by a line coordinate alone.

## Nice to Have

- Style, wording or ordering.
- A stale line hint beside a resolving anchor in a point-in-time artifact (a plan, review, finding or QA report).

## Calibration

| Finding | Grade |
|---|---|
| A documentation page calls one flag "the one route", and this change makes that false. | Should Fix: it describes the tool, and no step now fails. |
| A page describes a behaviour without a new exception, and the remedy it gives still works. | Should Fix. |
| A program message states something inaccurate but gives no step that leads to a wrong result. | Should Fix. |
| A documented command now fails when run. | Must Fix, **Wrong action from operative text**. |
| A task breaks an existing test it does not edit. | Must Fix, **Wrong build**. |

## Who may cite this

These documents point at a section of this file:

- `${CLAUDE_PLUGIN_ROOT}/agents/architecture-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/branch-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/business-parity-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/layer-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/qa-tester.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/review-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/skeptic-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/task-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/test-fix-plan-writer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/ui-tests-plan-reviewer.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/user-review-fix-plan-writer.md`
- `${CLAUDE_PLUGIN_ROOT}/docs/AUTONOMOUS_FLOW.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/dispatch_discipline_instructions.md`
- `${CLAUDE_PLUGIN_ROOT}/instructions/plan_review_rounds.md`

A citer **points and never restates**, and no plugin asset beyond this list points at this file. A new citer joins this list. An edit that rewords or moves a heading updates every roster member in the same change.
