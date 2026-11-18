### Task 4 — Create `finding_grades.md` and extend the Must Fix entry

**Goal:** Create the one file that owns the three grades, and add `**Class:**` and `**Failure:**` to the plan-round Must Fix entry.

**Where this task stops.** The agents are repointed by Tasks 5–10, and the samples, dispatch discipline and flow map by Task 11. This file lists them as citers first, because a contract lands before its consumers.

### Targets

- `plugin/instructions/finding_grades.md` (new)
- `plugin/instructions/plan_review_rounds.md`

**Work:**

- [ ] Create `finding_grades.md` with no frontmatter: `# Finding grades`; `## Resolved values`, stating that the file declares no token; then `## Must Fix`. It says a finding is a Must Fix only when it meets both conditions below, and otherwise is a Should Fix, or a Nice to Have when it is style, wording or ordering. Under `### 1. It belongs to one of four classes`, use this table:

  | Class | The finding must show |
  |---|---|
  | **Wrong behaviour** | Running the code as this change leaves it, or as the plan will build it, gives a wrong result: incorrect data or output state, a crash, data loss, a security or permission hole, a failing test or type check, or a stated requirement not met. |
  | **Wrong build** | An implementer following the plan or finding as written would build the wrong thing, leave out required work, or be unable to finish: tasks that contradict each other, a missing requirement, an undefined interface, a dependency ordered too late, a forbidden test run. |
  | **Wrong action from operative text** | Text would, followed literally, cause a failed or harmful action. Operative text is anything a person, an agent or a program follows or reads as input: instructions, configuration, templates, schemas, literals other files depend on, and any command, path, flag, setup step or remedy given in documentation or program output. |
  | **Broken contract** | A required accompanying item is missing, a reference does not resolve, a format a parser or loop reads is broken, a layer boundary is crossed, a mandated convention is bypassed, or business logic diverges from the reference implementation while the parity phase is on. |

- [ ] Continue the file. `### 2. The grader can complete the failure sentence` gives `If <actor> does <step>, then <observable wrong result>.` and three rules: `<actor>` is a named consumer (the implementer, a named agent, an adopter or the running program); `<step>` exists in the artifact under review, and the finding quotes it or names the code path; `<observable wrong result>` can be checked, and "may be confused", "may believe" and "could mislead" do not qualify. `### The entry fields` requires `**Class:** <class name>` and `**Failure:** <the sentence>` on every Must Fix entry. `### Checklist triggers` says each trigger an agent grades Must Fix names its class in that agent's `### Must Fix triggers` table, and an instance whose failure sentence can be completed cannot be downgraded; an instance whose sentence cannot be completed is a Should Fix.
- [ ] Add `## Never a Must Fix on its own`: a code comment or doc comment; a sentence that only describes the project and has become false, including a stale count; output wording that states something inaccurate but gives no step to follow; a hypothetical the grader did not verify; a line coordinate. Add `## Should Fix`: a real defect that fails either condition, plus a line coordinate in a durable artifact (an instruction file, an agent definition, a catalog document, a standing tracked artifact, a code comment), stale or not, and a citation that locates its site by a line coordinate alone. Add `## Nice to Have`: style, wording, ordering, and a stale line hint beside a resolving anchor in a point-in-time artifact (a plan, review, finding or QA report).
- [ ] Add `## Calibration`, with no path or file type of any one repository: a documentation page calling one flag "the one route" that this change makes false is a Should Fix, because it describes the tool and no step now fails; a page describing a behaviour without a new exception is a Should Fix when the remedy it gives still works; a program message that states something inaccurate but gives no step that leads to a wrong result is a Should Fix; a documented command that now fails when run is a Must Fix, **Wrong action from operative text**; a task that breaks an existing test it does not edit is a Must Fix, **Wrong build**. Add `## Who may cite this`, with the "points and never restates" rule and this roster, each as `${CLAUDE_PLUGIN_ROOT}/…`: `agents/architecture-reviewer.md`, `agents/branch-reviewer.md`, `agents/business-parity-reviewer.md`, `agents/layer-reviewer.md`, `agents/qa-tester.md`, `agents/review-plan-reviewer.md`, `agents/skeptic-reviewer.md`, `agents/task-plan-reviewer.md`, `agents/test-fix-plan-writer.md`, `agents/ui-tests-plan-reviewer.md`, `agents/user-review-fix-plan-writer.md`, `docs/AUTONOMOUS_FLOW.md`, `instructions/dispatch_discipline_instructions.md`, `instructions/plan_review_rounds.md`.
- [ ] In `plan_review_rounds.md`: in `## The round file`, say an existing `review_<iteration>.md` comes from an interrupted round or one the round-file check refused, and is replaced either way. In `## The Must Fix entry`, write each entry as a column-0 numbered item, add `**Class:**` and `**Failure:**` to the required lines with a pointer to `${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md`, and state the check: a `verdict: FAIL` file with no numbered entry, a `verdict: PASS` file with one, or an entry lacking either field is refused and does not reach the writer; the gate is dispatched again within the round, and its third refusal escalates. Keep every existing heading byte-identical.

**Verification:**

- `grep -nE 'Grade every finding by consequence|would do the wrong thing|[Tt]he rubric' plugin/instructions/finding_grades.md` prints nothing.
- `grep -nE 'harness-runs|cli/|\.ts|\.mjs|--reset-config|--upgrade' plugin/instructions/finding_grades.md` prints nothing, so the definition names nothing specific to this repository.
- Every roster path resolves under `plugin/`, and every heading other files cite in `plan_review_rounds.md` is unchanged.
