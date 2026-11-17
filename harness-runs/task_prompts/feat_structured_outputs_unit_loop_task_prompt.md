`feat_structured_outputs_unit_loop` gives the agents of the unit loop and the Run gates phase (`layer-implementer`, `layer-reviewer` and `test-fix-plan-writer`) a declared, schema-validated return. It also moves every caller of those returns onto the new form.

It is branch 2 of five that give every plugin agent such a return:

1. `feat_structured_outputs_mechanism`: settles the mechanism gaps and adopts `prompt-injection-reviewer`.
2. **`feat_structured_outputs_unit_loop`**: this branch.
3. `feat_structured_outputs_branch_review`
4. `feat_structured_outputs_setup`
5. `feat_structured_outputs_docs_qa`

**Starts after `feat_structured_outputs_mechanism` has merged.** If `docs/structured-agent-returns.md` does not yet record that branch's three decisions, stop and say so rather than deciding them here.

## Why

`ROADMAP.md` → `## Quality and testing` → **Structured agent outputs**: *"Every agent's return validated against a declared schema at the seam — reviewer verdicts, writer file paths and counts, the statistics block. The contracts already exist in prose and callers parse those lines word for word, so renaming one breaks a caller silently today."*

The mechanism is settled, and this branch adopts it without re-deciding it. `feat_structured_planning_agent_outputs` built it for the six planning agents. `feat_structured_outputs_mechanism` extended it with three decisions:

- how an orchestrating session reads an `Agent` result, given the measured Claude Code trailer after the reply;
- how the schema dialect represents a list whose items have several parts;
- what an agent's former `error:` return becomes, since `error` is never an agent outcome.

All of it is recorded in `docs/structured-agent-returns.md`. Where this prompt names one of those decisions, the decision record is the authority. If the record disagrees with this prompt, follow the record and say so in the plan.

In short:

- **The return block.** The agent ends its reply with one fenced `json` block holding one object.
- **The schema file.** The schema is `plugin/schemas/<agent>.return.json`, in the closed dialect `## 2.` → `### The return schema` lists.
- **What the agent sees.** The agent's `## Output contract` carries `### Return fields` and the canonical return-block sentence, never the schema.
- **How callers cite fields.** Callers cite a field as `` `<agent>.<field>` `` and an outcome as "an `outcome` of `PASS`".
- **How callers check a return.** Callers that route on a return point at `plugin/instructions/agent_return_contract.md` → `## Reading a return` and `## A return that fails the check`. Each new citing document joins that module's `## Who may cite this`.
- **What the static check holds.** `cli/test/agent-return-schemas.test.mjs` holds each adopted agent to all of this with no change to the suite. The adoption steps are `## 2.` → `### Adopting it for another agent`.

`verdict:` lines, readiness lists and other content inside a **file** an agent writes (a review index, a fix plan, a round file) are file content, not a return, and are unchanged.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## Scope: the agents and their current returns

**`layer-implementer`** (`plugin/agents/layer-implementer.md` → `## Output contract`) returns either of two things today.

- **On success:** a numbered prose report with seven parts:
  1. files created, modified or renamed;
  2. `Renamed: <old> → <new>` lines;
  3. the evidence its layer's conventions document requires;
  4. parity confirmations when `phases.parity` is `true`;
  5. verification: the type check, each test file, each selected tree guard, and the row-`G.4` before/after;
  6. plan deviations;
  7. items to flag to the user, including `**Unactioned under a gate:**` parts.
- **When blocked:** one of three named forms that callers tell apart by the string:
  - `blocker: <one-line cause>`
  - `blocker: prohibited — <one-line cause>; disposition appended to <detail_file>`
  - `blocker: already passing — <one-line cause>; record appended to <detail_file>`

Planning decides which of the seven parts become fields a caller routes or records on, and which stay prose above the block. Use the decision record's rule for lists of structured items, for example per-test verification results.

**A script depends on this agent's text.** Since `feat_committer_as_script`, `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_record_cause` reads the `**Cause:**` line of the detail file's `## Disposition` or `## Already passing` section into the commit body. `layer-implementer.md` requires that line to be *"the same text as"* the cause in its `blocker: prohibited — …` / `blocker: already passing — …` return. Keep that agreement true when the cause moves into a field. The detail-file line is file content the script reads; it is not a return.

**`layer-reviewer`** returns `verdict: PASS` or `verdict: FAIL`, the latter with its findings-file and Must Fix lines, per `## Output contract`'s three outcomes. A Should-Fix-only review writes a file and still returns `verdict: PASS`.

**`test-fix-plan-writer`** returns `fix_plan_file:`, `fix_plan_dir:`, `fixable:` and `not_fixable:`. When only the user can settle a failure, it puts a `## Questions` section above that block and sets `fix_plan_file: (pending — questions for user)`. `feat_structured_planning_agent_outputs` made the same `## Questions` heading a `questions` field for the planning writers. Follow that precedent.

## The goal

1. `layer-implementer`, `layer-reviewer` and `test-fix-plan-writer` each have a schema file, `### Return fields` and the return-block sentence, in every mode. `cli/test/agent-return-schemas.test.mjs` holds them with no change to the suite unless the decision record calls for one.
2. No caller parses these three agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`.
3. The commit body's dispositioned cause still equals the agent's returned cause.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** Anything the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` or added there as unmeasured.
- No caller is left reading a field its agent no longer returns, at the end of any task.

