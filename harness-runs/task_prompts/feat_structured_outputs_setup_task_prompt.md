`feat_structured_outputs_setup` gives the two agents `/devscene:analyze` dispatches, `conventions-writer` and `conventions-reviewer`, a declared, schema-validated return. It also moves `plugin/commands/analyze.md` and every other caller onto it.

It is branch 4 of five that give every plugin agent such a return:

1. `feat_structured_outputs_mechanism`: settles the mechanism gaps and adopts `prompt-injection-reviewer`.
2. `feat_structured_outputs_unit_loop`
3. `feat_structured_outputs_branch_review`
4. **`feat_structured_outputs_setup`**: this branch.
5. `feat_structured_outputs_docs_qa`

**Starts after branches 1–3 have merged.** `feat_structured_outputs_unit_loop` added the optional-field rule to `plugin/instructions/agent_return_contract.md` → `## Reading a return`, and the lessons ledger's rule that an outcome value is one token with no space; `feat_structured_outputs_branch_review` may add more of the same kind. If `docs/structured-agent-returns.md` does not yet record the mechanism branch's three decisions, stop and say so rather than deciding them here.

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

Both agents return `key:` fields whose names their contracts call byte-stable. Both run on two axes, `pass: document` and `pass: corpus`, so every field has to be accounted for on each axis.

- **`conventions-writer`.** Its fields:
  - `document_path:`
  - `action_taken:` (`written` / `merged`)
  - `not_determined:` (a count)
  - `not_determined_lines:` (verbatim lines or `none`)
  - `conflicts:`
  - `shared_document_divergences:`. This field is **always emitted**: the caller's stop condition fires on an omitted field.
  - `findings_applied:` (a count or `n/a`)
  - `findings_declined:`
  - `evidence:`
  - `prior_document:` (`skeleton` / `filled` / `absent`)
  - `prior_prompts:`
  - `prior_rule_block:`
  - `notes:`

  Several of these are multi-line, verbatim lists or `none` / `n/a`. A fix dispatch re-emits the three `prior_*` fields exactly as the dispatch handed them.
- **`conventions-reviewer`.** On `pass: document` it returns `document_path:`, `findings:` and `summary:`. On `pass: corpus` it returns `findings:` and `summary:`, each finding naming its own document path and check id (`C1`–`C6`, or a document-pass check number). Each finding has several parts (claim, evidence, concrete correction). It writes no file, so the return is the only carrier of its findings.

These are the agents whose items have the most parts. Apply the decision record's rule for lists of structured items. Neither agent has an outcome today, so choose `outcome` values per `## 2.` → `### The return schema`.

**A wire string crosses files.** `Reviewer finding not applied — ` is carried by `plugin/agents/conventions-writer.md`, `plugin/agents/conventions-reviewer.md` and `plugin/commands/analyze.md`. It appears in the written document's `## Not determined` section (file content, unchanged) and in the writer's `findings_declined:` / `not_determined_lines:` return (in scope). Keep the three files agreeing on it.

## The goal

1. `conventions-writer` and `conventions-reviewer` each have a schema file, `### Return fields` and the return-block sentence, on both axes and every action. `cli/test/agent-return-schemas.test.mjs` holds them with no change to the suite unless the decision record calls for one.
2. `analyze.md` and every other caller read the new objects. No caller parses these returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`.
3. `Reviewer finding not applied — ` still agrees across the three files that carry it.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** Anything the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` or added there as unmeasured.
- No caller is left reading a field its agent no longer returns, at the end of any task.
