# Structured agent returns — the mechanism's decisions and measurements

**Who reads this:** a maintainer changing an agent's return, and the author of `feat_structured_outputs_remaining_agents` (#380; `ROADMAP.md` → the `Structured agent outputs` row), who adopts the mechanism for the agents that do not carry it yet.

**What it owns.** The decisions of record for how an agent declares its return, how each caller reads and checks it, and what a return that fails its check costs; and what of that is measured. It restates no rule an agent or a caller follows: those are `plugin/instructions/agent_return_contract.md`'s — the block (`## The return block`), the schema dialect (`## The return schema`), the prose description (`## Return fields`), the citation form (`## Citing a field`), the routing check (`## Reading a return`), the failed-return route (`## A return that fails the check`) and the adoption steps (`## Adopting it for another agent`). The planning driver's side of it is `docs/flow-graph-walker.md` → `## 5. The two drivers`.

The mechanism was settled on `feat_structured_planning_agent_outputs` for the six agents the planning graph dispatches — `task-plan-writer`, `task-plan-reviewer`, `architecture-reviewer`, `business-parity-reviewer`, `ui-tests-plan-writer` and `ui-tests-plan-reviewer` — in every mode each runs in.

---

## 1. The decisions

### The return shape — one fenced `json` block, last

**Decision.** An agent's reply ends with its return object, one fenced `json` block holding one JSON object, with only whitespace after the closing fence; prose may sit above it (`agent_return_contract.md` → `## The return block`). The alternative weighed was the whole reply as JSON, with the human-readable part in a field.

**Reason.** A node session's `result` text is the agent's final reply verbatim, fences included: the first real script-driven node's `result` ended in the writer's own fenced block (§3, the fourth row). So the driver can take the block with jq 1.5 `split` alone, with no regex: the text after the last line opening ```` ```json ````, cut at the next closing fence, with only whitespace allowed after it (`cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`). An orchestrating session reads a fenced block at the end of an `Agent` result the way it read the fenced `key: value` block these agents returned before. A whole-JSON reply would put every agent's explanatory prose inside a string, escaped by the agent.

**Cost.** Anything after the closing fence — a sign-off, a second block — makes the return fail its check, and a failed return is re-dispatched (`### A return that fails its check`, below). That an orchestrating session's `Agent` result carries the reply verbatim is not measured (§3).

### Everything a caller routes or records on is a field

**Decision.** What a caller reads from these returns is a field of the object, so no caller parses a prose heading of them: the former `## Questions`, `## Corpus staleness`, `## Parity exclusions / deferrals` and `## Manual setup required` sections are the fields `questions`, `corpus_staleness`, `parity_exclusions` and `manual_setup`, each per the agent's own `## Return schema`. One section deliberately stays prose above the block: `## Unsolicited dispatch guidance`. The `verdict:` lines inside a round file or a review index are file content, not a return, and are unchanged.

**Reason.** A prose heading is a wire no check can hold, so a renamed one breaks a caller only at run time. `## Unsolicited dispatch guidance` is owned across every graded agent by `plugin/instructions/dispatch_discipline_instructions.md`, whose wording and record are not this mechanism's, and its "above the fenced block" placement stays true.

**Cost.** `## Unsolicited dispatch guidance` stays outside every check. A field holding free text — a question, a staleness entry — is a JSON string the agent must escape correctly, or the whole return fails.

### The schema lives in the agent's own definition

**Decision.** Each agent's definition carries a `## Return schema` section, directly after its `## Output contract`, holding one draft-07 JSON Schema in the closed dialect `agent_return_contract.md` → `## The return schema` lists. The `## Output contract` describes it in `### Return fields` and never restates it in another form. The alternative weighed was one file per agent under `schemas/`.

**Reason.** The installed plugin carries only `plugin/`, so a schema under `schemas/` is not in the pinned plugin the driver reads at run time; the agent's own definition is (`planning-node-lib.sh` → `pnl_agent_schema_scan`, `pnl_load_schemas`). The model reads its own schema in its own definition, and the definition stays the one owner of its return. The dialect is closed so the driver can validate it in jq 1.5.

**Cost.** These schemas are not under `schemas/` and `ajv` does not validate them; `cli/test/agent-return-schemas.test.mjs` holds them to the dialect instead. A keyword the dialect lacks is a change to the module, to `PNL_REAP_JQ`'s `vfail` and `schemafail`, and to that suite together. Every dispatch of the agent carries the schema in its definition.

### One discriminator, `outcome`, held to the graph

**Decision.** Every variant of a schema carries `outcome` as a `const`, and for an agent the planning graph dispatches its values are exactly that node's outcome keys in `cli/templates/scripts/flows/task_plan_writing.graph.json`, minus `error`. `error` is never an agent's outcome: a caller records it for a return that keeps failing its check.

**Reason.** The graph stays the one owner of which outcomes a node may have, and the schema can only agree with it. One discriminator lets the driver pick the variant by `const` and a caller route on one field.

**Cost.** An outcome added to the graph is a variant added to the agent's schema in the same change, and the reverse; `cli/test/agent-return-schemas.test.mjs` fails until both agree. An agent the graph does not dispatch has no second owner to be held to.

### Validation on each path, and why no validator script

**Decision.** The driver validates the whole object against the agent's `## Return schema` at reap time, in jq (`PNL_REAP_JQ`). The orchestrating session applies the lighter routing check `agent_return_contract.md` → `## Reading a return` defines. A caller names a field it reads in the citation form `` `<agent>.<field>` `` (`## Citing a field`), and `cli/test/agent-return-schemas.test.mjs` holds every such citation, and every `pd_ret_field` call in the driver, to the named agent's schema.

**Reason.** An orchestrating session cannot run a validator for free. A validator script would need a write per dispatch to hand it the reply, and an agent-invocable row in `OUTER_LOOP_SCRIPTS` with the permission-profile entries that flag implies (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, the outer-loop-script row); the branch's task prompt allowed no new permission. The routing check covers what the session acts on: the block, the outcome it routes on, and the fields it reads for that outcome. The static check moves a renamed field from a run-time break to a test failure on either path.

**Cost.** The two paths check with different strength. The routing check does not check a field's type, `additionalProperties` or a field the section does not read, so a return the driver would refuse can be acted on by an orchestrating session. The check is prose the session follows, not code.

### A return that fails its check

**Decision.** On the driver, a return with no block, a block that is not one JSON object, or an object that fails its schema is the existing infrastructure class: the node alone is re-dispatched, at most `PD_MAX_ATTEMPTS` (3) attempts, and only the last is recorded `error` (`planning-node-lib.sh` → `PNL_REAP_JQ`; `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_reap_one`). On the orchestrator path it is treated as a dispatch that did not return, and the third consecutive failure takes the section's `error` route (`agent_return_contract.md` → `## A return that fails the check`). The alternative weighed for the orchestrator path was an immediate blocker.

**Reason.** A malformed reply is the failure a re-dispatch of the same prompt can remedy, so one bound of three on both paths treats it alike, and neither path guesses at a malformed return.

**Cost.** An agent that fails its check every time costs three dispatches before `error`, and every retry counts against `MAX_TOTAL_DISPATCHES` on both paths. On the orchestrator path the consecutive count is followed as prose, not held by code.

### `--json-schema`, `structured_output` and `harness_friction` are dropped

**Decision.** The driver launches a node with no `--json-schema` and reads no `structured_output`; `pnl_schema`, the graph-built schema it fed that flag, is removed with them, and so is `harness_friction`, which existed only as a property of that schema. The remote mention control (`cli/templates/scripts/remote-run.sh` → `control_mention_session`) runs without `--agent`, still reads `structured_output`, and is unaffected.

**Reason.** Under `--agent`, `--json-schema` is not applied and the `result` event carries no `structured_output` (§3, the third and fourth rows). Kept as a fallback, the flag would be a second schema owner built from the graph, and if a later Claude Code applied it under `--agent` it would force the graph's decision shape over the agent's own. No agent session ever received `harness_friction`'s description and no agent contract asks for it, so its observation path was removed rather than kept as dead code.

**Cost.** A later Claude Code that applies `--json-schema` under `--agent` gives the driver nothing until a measurement re-opens this decision.

---

## 2. Adopting it for another agent

The steps are `agent_return_contract.md` → `## Adopting it for another agent`, in that section's order; an agent with no `## Return schema` section is outside every check until it gains one, so agents adopt one at a time. Once an agent has the section, `cli/test/agent-return-schemas.test.mjs` holds it, with no change to the suite, to: the closed dialect; its `### Return fields` naming exactly the schema's properties; the return-block sentence carried verbatim in its `## Output contract`; the planning graph's outcome keys, where the graph dispatches it; and every `` `<agent>.<field>` `` citation of it in the plugin. That work is #380's (`ROADMAP.md` → the `Structured agent outputs` row).

---

## 3. Measured, and not yet measured

**Measured, 2026-11-16, Claude Code 2.1.325**, as recorded in `harness-runs/task_prompts/feat_structured_planning_agent_outputs_task_prompt.md` → `## Measured, 2026-11-16, Claude Code 2.1.325`. Each row is a `claude -p --output-format stream-json --verbose` session with the `--json-schema`

```
{"type":"object","properties":{"outcome":{"type":"string","enum":["PASS","FAIL"]},"return":{"type":"string"}},"required":["outcome"]}
```

reading the `result` event:

| Session | `structured_output` in the `result` event |
|---|---|
| Plain session, no `--agent`, asked to reply with outcome `PASS` | present: `{"outcome":"PASS","return":"probe ok"}`, and `result` is the same object as JSON text |
| Plain session, no `--agent`, one `Bash` tool call first | present: `{"outcome":"PASS","return":"hi"}` |
| `--plugin-dir <main checkout>/plugin --agent devscene:prompt-injection-reviewer`, asked to reply with outcome `PASS` | **absent**: no `structured_output` key. `result` was prose: `probe ok` followed by the agent declining to return `PASS` because its own contract emits only `verdict: SAFE` or `verdict: UNSAFE` |
| The first real script-driven node, `--agent devscene:task-plan-writer` with the driver's schema (run `fix_run_commit_trailer_amend`) | **absent**: no `structured_output` key. `result` was the writer's prose return ending in its fenced `story_file:` / `task_files_dir:` / `tasks_count:` / `story_points_total:` block |

**Not yet measured: an orchestrating session's `Agent` result carries the sub-agent's final reply verbatim, return block included.** The orchestrator path's routing check depends on it, and no result is recorded for it here. The hand step that measures it is one autonomous run on the orchestrated path, with `execution.scriptDrivenPlanning` off (its default), from a terminal outside any agent session, run from the main checkout with `<state_dir>` your configured value. Drop a task prompt for a throwaway branch `<branch>` as usual. Once its first `task-plan-writer` dispatch has returned, read that dispatch's `tool_result` text out of the run stream the watcher already records:

```
jq -R -r -s '[split("\n")[] | fromjson? | objects] as $ev | ([$ev[] | select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and (.name == "Agent" or .name == "Task") and ((.input.subagent_type // "") | endswith("task-plan-writer"))) | .id] | if length > 0 then .[0] else "" end) as $id | [$ev[] | select(.type == "user") | .message.content[]? | select(.type == "tool_result" and .tool_use_id == $id) | .content | if type == "string" then . elif type == "array" then ([.[] | select(.type == "text") | .text] | join("\n")) else tojson end] | if length > 0 then .[0] else "no tool_result for the first task-plan-writer dispatch" end' <state_dir>/autonomous_logs/<branch>.stream.jsonl
```

It prints the text the orchestrating session received. The fact holds when that text ends in the writer's fenced `json` return block as the writer wrote it; record the Claude Code version, the date and the printed tail beside the table above. The seam exists, so nothing new ships for this step. The event shapes the command selects on — an assistant `tool_use` named `Agent` or `Task` with `input.subagent_type`, answered by a `tool_result` with the same `tool_use_id` — are themselves read by this step, not recorded.
