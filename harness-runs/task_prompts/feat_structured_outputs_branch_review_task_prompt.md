`feat_structured_outputs_branch_review` gives the end-of-branch review agents, the user-review fix-plan writer and the statistics writer a declared, schema-validated return. The agents are `branch-reviewer`, `skeptic-reviewer`, `review-plan-reviewer`, `user-review-fix-plan-writer` and `statistics-plan-writer`. It also moves every caller of those returns onto the new form.

It is branch 3 of five that give every plugin agent such a return:

1. `feat_structured_outputs_mechanism`: settles the mechanism gaps and adopts `prompt-injection-reviewer`.
2. `feat_structured_outputs_unit_loop`
3. **`feat_structured_outputs_branch_review`**: this branch.
4. `feat_structured_outputs_setup`
5. `feat_structured_outputs_docs_qa`

**Starts after `feat_structured_outputs_mechanism` and `feat_structured_outputs_unit_loop` have merged.** The second added the optional-field rule to `plugin/instructions/agent_return_contract.md` → `## Reading a return`, and the lessons ledger's rule that an outcome value is one token with no space. If `docs/structured-agent-returns.md` does not yet record the mechanism branch's three decisions, stop and say so rather than deciding them here.

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

Each agent's `## Output contract` and mode sections under `plugin/agents/` are the source. In short:

- **`branch-reviewer`.** It writes the split review (index plus per-finding files) and returns a **prose** summary: the index path, the per-finding folder path and the finding count. In two-pass mode it adds the line `Pass 2 carried over N items, skipped M (already covered) and K (stale).` A `## Questions` section, and an optional `## Unsolicited dispatch guidance`, sit above it.
- **`skeptic-reviewer`.** It returns `verdict: PASS`, or `verdict: FAIL` + `index_path:` + `must_fix_count:`. `## Questions` and `## Unsolicited dispatch guidance` sit above the block.
- **`review-plan-reviewer`.** It returns `verdict: PASS`, or saves `review_{iteration}.md` and returns its FAIL lines.
- **`user-review-fix-plan-writer`.** It returns `fix_plan_file:`, `fix_plan_dir:`, `valid_must_fix:`, `valid_should_fix:`, `valid_nice_to_have:` and `invalid:`. When it needs clarification, a `## Questions` section sits above the block and `fix_plan_file: (pending — questions for user)`.
- **`statistics-plan-writer`.** It returns `statistics_file:`, `story_points_total:`, `issue_cost_total:`, `story_plan_tasks:`, `user_review_issues:`, `success_rate:` (a percentage or `n/a`) and `status:` (`pre-user-review` / `post-user-review`). Its `## Invocation contract` says the caller parses five of those lines by name. It also has an `error:` return that callers treat as **non-halting**. `error` is never an agent outcome, so rename that return by the rule the mechanism branch recorded in `docs/structured-agent-returns.md` → `## 1. The decisions`, keeping it non-halting for its callers.

`feat_structured_planning_agent_outputs` made `## Questions` the `questions` field and kept `## Unsolicited dispatch guidance` as prose above the block. Follow that precedent here.

**Unchanged:** the review index, its `## Phase 2 Readiness — Ordered Fix List`, the per-finding files and the fix plan's `**Review comments:** ` line. That line is a file contract `cli/templates/scripts/remote-run.sh` → `deliver` reads, not a return.

## The goal

1. The five agents each have a schema file, `### Return fields` and the return-block sentence, in every mode. `cli/test/agent-return-schemas.test.mjs` holds them with no change to the suite unless the decision record calls for one.
2. No caller parses these agents' returns line by line in the old prose form. Each routing caller cites `` `<agent>.<field>` `` and points at `agent_return_contract.md`, and is listed in its `## Who may cite this`.
3. A failed statistics write still never halts a flow.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** Anything the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` or added there as unmeasured.
- No caller is left reading a field its agent no longer returns, at the end of any task.
