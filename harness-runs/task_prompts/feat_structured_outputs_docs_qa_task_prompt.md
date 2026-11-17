`feat_structured_outputs_docs_qa` gives the docs-phase agents and the interactive-test agents a declared, schema-validated return. The agents are `docs-writer`, `docs-reviewer`, `qa-tester`, `qa-tester-mobile-maestro` and `qa-tester-mobile-mcp`. It also moves every caller of those returns onto the new form. It then makes the static check require a return schema for **every** plugin agent and closes `ROADMAP.md` → **Structured agent outputs**.

It is branch 5 of five that give every plugin agent such a return:

1. `feat_structured_outputs_mechanism`: settles the mechanism gaps and adopts `prompt-injection-reviewer`.
2. `feat_structured_outputs_unit_loop`: `layer-implementer`, `layer-reviewer`, `test-fix-plan-writer`.
3. `feat_structured_outputs_branch_review`: `branch-reviewer`, `skeptic-reviewer`, `review-plan-reviewer`, `user-review-fix-plan-writer`, `statistics-plan-writer`.
4. `feat_structured_outputs_setup`: `conventions-writer`, `conventions-reviewer`.
5. **`feat_structured_outputs_docs_qa`**: this branch.

**Starts after branches 1–4 have merged**, because its closing check requires every agent to have a schema. Before planning, list `plugin/agents/*.md` and `plugin/schemas/*.return.json`. If any agent other than this branch's five has no schema file, stop and name it rather than adopting it here.

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

- **`docs-writer`.** Its returns depend on the mode:
  - **catalog / update:** `doc_path:`, `unverified:`, `parity_gaps:` and `notes:`.
  - **survey:** `targets:`, one line per target shaped `action(new|update) · slug · output_path · reason · entry-hints`, or `targets: none` with a reason; plus `notes:`.
  - **docs phase disabled:** `notes:` alone.
  
  `targets` is a list of structured items, so apply the decision record's rule for those.
- **`docs-reviewer`.** It returns `verdict:` (`PASS` / `FAIL`), `findings_file:`, `missed_docs:` (update mode only) and `summary:`. With the docs phase disabled, it returns `verdict: PASS` plus a one-line reason and no `findings_file:`.
- **`qa-tester`.** Its `## Output contract` has four returns, picked by priority:
  1. `verdict: PASS`
  2. `verdict: FAIL` + `findings_file:` + `must_fix_count:`
  3. `error: blocked — test <T>: <one-line cause>`
  4. `error: <one-line reason>` (the run cannot proceed)
  
  Callers tell 3 and 4 apart by the `blocked — ` marker. `error` is never an agent outcome, so rename returns 3 and 4 by the rule the mechanism branch recorded in `docs/structured-agent-returns.md` → `## 1. The decisions`. Keep the distinction callers act on: a blocked test is not a pass, and a run that cannot proceed halts.
- **`qa-tester-mobile-maestro` and `qa-tester-mobile-mcp`.** These are declared-but-unimplemented stubs with no `## Output contract`. On every dispatch they return return 4 of `qa-tester` (`error: qa.driver is … — no test was executed`, or the disabled-phase or wrong-driver reason). They adopt `qa-tester`'s four return shapes by pointer (`## Operating contract — inherited by pointer`), and the same callers dispatch whichever variant `qa.driver` names. So their schema is the subset of `qa-tester`'s that they can return, with the same field names. Each stub gains the `## Output contract` the static check requires, carrying the return-block sentence and its `### Return fields`. Their `tools:` allowlist stays `Read` alone.

The QA review index, its readiness list and the per-finding files `qa-tester` writes are file content and unchanged. So is the documentation `docs-writer` writes.

## Closing the work

- **Every agent covered.** Make `cli/test/agent-return-schemas.test.mjs` fail any `plugin/agents/*.md` agent definition with no `plugin/schemas/<agent>.return.json`. Today the suite deliberately skips such an agent (`docs/structured-agent-returns.md` → `### Adopting it for another agent`: *"An agent with no `plugin/schemas/<agent>.return.json` is outside every check until it gains one"*). Add a bad-sample test for the new rule, as the suite does for its others. Then reword that paragraph, and any other "adopt one at a time" wording in the decision record, to the rule now in force.
- **The roadmap row.** `ROADMAP.md` → `## Quality and testing` → **Structured agent outputs** is marked closed, its entry pointing at `docs/structured-agent-returns.md`. The numbered priority table near the top of `ROADMAP.md` lists the same row, so update it too.

## The goal

1. The five agents each have a schema file, `### Return fields` and the return-block sentence, in every mode. The two stubs' schemas are a subset of `qa-tester`'s.
2. No caller parses these agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`.
3. `cli/test/agent-return-schemas.test.mjs` covers all 22 agents and skips none, and fails a new agent added without a schema.
4. `ROADMAP.md` → **Structured agent outputs** is closed, pointing at `docs/structured-agent-returns.md`.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** Anything the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` or added there as unmeasured.
- No caller is left reading a field its agent no longer returns, at the end of any task.
