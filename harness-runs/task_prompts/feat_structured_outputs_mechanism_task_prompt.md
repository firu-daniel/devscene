`feat_structured_outputs_mechanism` is the first of five branches that give every plugin agent a declared, schema-validated return. It settles three gaps in the mechanism that `feat_structured_planning_agent_outputs` built for the six planning agents. It then adopts that mechanism for its first non-planning agent, `prompt-injection-reviewer`, and its script caller, `prompt-injection-screen.sh`.

The four later branches each adopt the mechanism for one group of agents, using the decisions this branch records:

1. `feat_structured_outputs_mechanism`: this branch.
2. `feat_structured_outputs_unit_loop`: `layer-implementer`, `layer-reviewer`, `test-fix-plan-writer`.
3. `feat_structured_outputs_branch_review`: `branch-reviewer`, `skeptic-reviewer`, `review-plan-reviewer`, `user-review-fix-plan-writer`, `statistics-plan-writer`.
4. `feat_structured_outputs_setup`: `conventions-writer`, `conventions-reviewer`.
5. `feat_structured_outputs_docs_qa`: `docs-writer`, `docs-reviewer`, `qa-tester`, `qa-tester-mobile-maestro`, `qa-tester-mobile-mcp`. It also makes the static check require a schema for all 22 agents and closes the `ROADMAP.md` row.

## Why

`ROADMAP.md` → `## Quality and testing` → **Structured agent outputs**: *"Every agent's return validated against a declared schema at the seam — reviewer verdicts, writer file paths and counts, the statistics block. The contracts already exist in prose and callers parse those lines word for word, so renaming one breaks a caller silently today."*

`feat_structured_planning_agent_outputs` settled the mechanism and recorded it in `docs/structured-agent-returns.md`:

- **The return block.** The reply ends with one fenced `json` block holding one object.
- **The schemas.** Each agent's schema is `plugin/schemas/<agent>.return.json`, in a closed draft-07 dialect.
- **One discriminator.** Every variant routes on `outcome`.
- **Two validation paths.** The planning driver validates the whole object in jq (`cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`). An orchestrating session applies the lighter routing check in `plugin/instructions/agent_return_contract.md` → `## Reading a return`.
- **The static check.** `cli/test/agent-return-schemas.test.mjs` holds each adopted agent's schema, its `### Return fields`, its return-block sentence and every `` `<agent>.<field>` `` citation together.

Three things in that mechanism do not hold for the agents still to adopt it.

### Gap 1: the routing check contradicts a measured `Agent` result

The decision record lists as **not yet measured** that *"an orchestrating session's `Agent` result carries the sub-agent's final reply verbatim, return block included"*. Recent run streams answer it, and the answer breaks step 1 of `## Reading a return`: *"The reply's last fenced block opened with `json` exists, has only whitespace after its closing fence, and parses as one JSON object."*

**Measured, Claude Code 2.1.325, from run streams the watcher recorded.** The streams are `<state_dir>/autonomous_logs/feat_committer_as_script.stream.jsonl` and `<state_dir>/autonomous_logs/fix_run_commit_trailer_amend.stream.jsonl`, both on 2026-11-17. In both, the `tool_result` of an orchestrator `Agent` dispatch of `devscene:architecture-reviewer` (Run gates G.2 fix-plan review) differs from the agent's reply in two ways:

- **Every line of the reply is indented by two spaces.** The fence lines are included: the raw text reads `\n  \n  ```json\n  {\"outcome\": \"PASS\"}\n  ```\n`.
- **A Claude Code trailer follows the closing fence, at column 0:**

  ```
  agentId: <id> (use SendMessage with to: '<id>', summary: '<5-10 word recap>' to continue this agent)
  <usage>subagent_tokens: <n>
  tool_uses: <n>
  duration_ms: <n></usage>
  ```

Read the stream yourself with the `jq` one-liner in `docs/structured-agent-returns.md` → `## 3.`. Drop its `task-plan-writer` filter and select any `Agent` / `Task` `tool_result` whose text contains ```` ```json ````.

So a session that applied step 1 literally would reject every orchestrator-path return. Those runs went on regardless, so the sessions did not apply it literally. The screen's verdict files show the same: the orchestrator writes "its whole return verbatim" to the verdict file (`plugin/instructions/prompt_injection_screen.md`), and every recent run's screen printed `verdict: SAFE …`. The session therefore wrote the reply without the trailer. Reading the planning **driver** is unaffected, because the driver reads a node session's `result` event, not an `Agent` result.

**Settle:** reword `## Reading a return` so it states what the session actually receives and what it disregards, and record the measurement in `## 3.` with its version and date. Do not invent a fact the streams do not show. In particular, whether the indentation comes from Claude Code or from the agent is not measured.

### Gap 2: the dialect has no list of structured items

`### The return schema` allows `string`, `integer`, `boolean` and `array`, and `items` is only `{ "type": "string" }`. Several agents still to adopt the mechanism return lists whose items have several parts:

- `prompt-injection-reviewer`: `finding: <check-id> | <excerpt> | <reason>`, one per line.
- `conventions-reviewer`: findings, each carrying a document path, a check id, the claim, the evidence and the correction.
- `docs-writer`, survey mode: `targets:`, one line per target, `action · slug · output_path · reason · entry-hints`.
- `layer-implementer`: one verification result per test file and per tree guard.

Keeping such an item as a delimited string leaves the caller parsing a line, which is what this work removes. **Settle** whether the dialect gains an `array` of `object` items, or another shape, extending the mechanism minimally rather than adding a second one. If it does, change these together:

- `### The return schema` in `docs/structured-agent-returns.md`.
- `PNL_REAP_JQ`'s `vfail` and `schemafail`.
- `cli/test/agent-return-schemas.test.mjs`: the dialect check, and how `### Return fields` names a nested property and its type annotation.

### Gap 3: `error` is not an agent outcome, but some agents return `error:`

`### The return schema` says *"`error` is never an agent's outcome: a caller records it for a return that keeps failing"* `## Reading a return`. Two agents still to adopt the mechanism return `error:` as an ordinary result:

- **`qa-tester`.** Its `## Output contract` defines `error: blocked — test <T>: <one-line cause>` (one test blocked) and `error: <one-line reason>` (the run cannot proceed). Callers match the `error: blocked — ` literal. The two `qa-tester-mobile-*` stubs return the second shape on every dispatch.
- **`statistics-plan-writer`.** It returns an `error:` line that its callers treat as **non-halting**.

The six adopted schemas already use `blocker` for an agent's own blocked return (`task-plan-writer`: `returned`, `questions`, `blocker`; the reviewers: `PASS`, `FAIL`, `blocker`). **Settle** the rule a later branch applies when it renames an agent's `error:` return. Record it in `docs/structured-agent-returns.md` → `## 1. The decisions`. This branch renames no `qa-tester` or `statistics-plan-writer` return; their branches do.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## The agent this branch adopts: `prompt-injection-reviewer`

Its `## Output contract` today returns exactly one block, with no prose before or after:

- `verdict: SAFE` alone.
- Or `verdict: UNSAFE`, then one or more `finding: <check-id> | <excerpt> | <reason>` lines:
  - `<check-id>` is from `## The checks`.
  - `<excerpt>` is a verbatim single-line quote of at most 160 characters.
  - `<reason>` is one line.

A missing dispatch field or an unreadable file is a `blocker:` line, which the parser treats as `UNSAFE`. Anything else is `malformed-verdict` and parks the run.

Its callers:

- **`plugin/instructions/prompt_injection_screen.md`.** The orchestrator writes the return verbatim to `<state_dir>/scratch/prompt-injection-screen-<branch_fold>/verdict.md`, then runs `prompt-injection-screen.sh verdict --path … --verdict-file …`.
- **`cli/templates/scripts/prompt-injection-screen.sh`** → its `VERDICT` header and verb. It parses the return in bash and fails closed: only the exact SAFE block passes, and any other text is parked as UNSAFE with the finding `malformed-verdict`. `PI_CHECK_IDS` mirrors the agent's `## The checks` ids. The rewrite must stay fail-closed and must not loosen the SAFE test. This is a tripwire, so a parser that accepts more than it did is a regression.
- Every other document naming the agent:
  - `plugin/instructions/untrusted_input.md`
  - `plugin/instructions/clarification_digest_instructions.md`
  - `plugin/instructions/autonomous_pause_and_ledger.md`
  - `plugin/instructions/task_plan_writing_instructions_autonomous.md`
  - `plugin/instructions/user_review_fix_plan_writing_instructions_autonomous.md`
  - `plugin/docs/AUTONOMOUS_FLOW.md`
  - `cli/templates/scripts/README.md`
  
  `grep -rn "prompt-injection-reviewer\|verdict: SAFE\|verdict: UNSAFE" plugin cli` finds them. The park file's `Raised by: prompt-injection-reviewer (prompt-injection screen)` line (`PIS_RAISED`, and `PD_SCREEN_RAISED` in `cli/templates/scripts/lib/planning-driver-lib.sh`) is a park-file heading, not a return, and is not this branch's to change.

The script receives the return as a file, so it can apply the driver's full schema check rather than the session's lighter routing check. Whether it shares `PNL_REAP_JQ` or carries its own extraction is planning's choice. A changed generated or copied script obliges a `chore: Re-render …` follow-up, as earlier branches did.

## What to read first

- `docs/structured-agent-returns.md`, whole. It is the decision record this branch extends.
- `plugin/instructions/agent_return_contract.md`, whole.
- `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ` and `pnl_load_schemas`.
- `cli/test/agent-return-schemas.test.mjs`.
- `plugin/schemas/*.return.json`: the six existing schemas, as the dialect in use.
- `plugin/agents/prompt-injection-reviewer.md`, whole.
- `cli/templates/scripts/prompt-injection-screen.sh`: its header and the `verdict` verb.
- `plugin/instructions/prompt_injection_screen.md`.

## The goal

1. `docs/structured-agent-returns.md` records the three decisions above, each with its reason and cost, in the form `## 1.` already uses. `## 3.` records the measured `Agent` result shape.
2. `agent_return_contract.md` → `## Reading a return` matches what an orchestrating session receives.
3. `prompt-injection-reviewer` has a schema file, `### Return fields` and the return-block sentence. `cli/test/agent-return-schemas.test.mjs` holds it with no special case.
4. `prompt-injection-screen.sh` and every document reading the screen's return read the new object. No caller parses `verdict:` / `finding:` lines of the agent's return.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** Anything the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded in `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` or added there as unmeasured.
- No caller is left reading a field its agent no longer returns, at the end of any task.

