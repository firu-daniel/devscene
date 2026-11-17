`feat_structured_planning_agent_outputs` gives the six agents the planning graph dispatches a declared, schema-validated return. Its caller checks that return at the handoff on both drivers: the orchestrator's `Agent` dispatches and the planning driver's headless node sessions. It is the first half of `ROADMAP.md` → `## Quality and testing` → **Structured agent outputs** (row 20). It sets the mechanism. `feat_structured_outputs_remaining_agents` (#380) applies the same mechanism to the other 17 agents afterwards.

## Scope: the planning agents, in every mode they run in

The agents are the ones `cli/templates/scripts/flows/task_plan_writing.graph.json` dispatches: `task-plan-writer`, `task-plan-reviewer`, `architecture-reviewer`, `business-parity-reviewer`, `ui-tests-plan-writer` and `ui-tests-plan-reviewer`.

Several of them also run outside planning. `architecture-reviewer` and `business-parity-reviewer` review branch implementation, user-review fixes and Run gates. `ui-tests-plan-writer` writes the UI-test plan for the supervised QA flow and the user-review fix flow. `task-plan-writer` and `task-plan-reviewer` run in supervised and semi-autonomous planning too. An agent has one return contract, so each of the six changes in **all** its modes, and **every** caller that reads any of their returns changes with it, in this branch, wherever that caller sits. No other agent's return changes here.

## Why now

The roadmap row: *"Every agent's return validated against a declared schema at the seam — reviewer verdicts, writer file paths and counts, the statistics block, the committer's sha and subject. The contracts already exist in prose and callers parse those lines word for word, so renaming one breaks a caller silently today."*

The script-driven planning pilot (#375) made this a blocker. Its driver reads each node's decision from Claude Code's `--json-schema` output, the `result` event's `structured_output` (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_schema`, `PNL_REAP_JQ`). That does not work for an agent session:

## Measured, 2026-11-16, Claude Code 2.1.325

Each a `claude -p --output-format stream-json --verbose` session with a `--json-schema` of `{"type":"object","properties":{"outcome":{"type":"string","enum":["PASS","FAIL"]},"return":{"type":"string"}},"required":["outcome"]}`, reading the `result` event:

| Session | `structured_output` in the `result` event |
|---|---|
| Plain session, no `--agent`, asked to reply with outcome `PASS` | present: `{"outcome":"PASS","return":"probe ok"}`, and `result` is the same object as JSON text |
| Plain session, no `--agent`, one `Bash` tool call first | present: `{"outcome":"PASS","return":"hi"}` |
| `--plugin-dir <main>/plugin --agent devscene:prompt-injection-reviewer`, asked to reply with outcome `PASS` | **absent**: no `structured_output` key. `result` was prose: `probe ok` followed by the agent declining to return `PASS` because its own contract emits only `verdict: SAFE` or `verdict: UNSAFE` |
| The first real script-driven node, `--agent devscene:task-plan-writer` with the driver's schema (run `fix_run_commit_trailer_amend`) | **absent**: no `structured_output` key. `result` was the writer's prose return ending in its fenced `story_file:` / `task_files_dir:` / `tasks_count:` / `story_points_total:` block |

So under `--agent`, `--json-schema` is not applied, and the agent's own definition decides the shape of its reply. Only the remote mention control reads `structured_output` without `--agent` (`cli/templates/scripts/remote-run.sh` → `control_mention_session`), and it is unaffected.

The pilot's run did not park on this. It parked first on `the agent tools do not match its init event`, which `fix_planning_node_tool_check` (#378) fixes. With that fixed, every node would be read as an infrastructure `error` for a missing decision object, retried three times and parked.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## What to read first

- `ROADMAP.md` → row 20 and its `## Quality and testing` entry.
- The six agents' `## Output contract` sections under `plugin/agents/`, and their mode sections.
- Every caller that reads one of those six returns. `grep` each agent's name across `plugin/instructions/` and `plugin/commands/`. Among them are `plan_review_rounds.md`, `task_plan_writing_instructions_core.md` and its forks, `plan_orchestration_instructions_core.md`, `user_review_fixes_instructions_core.md`, `user_review_fix_plan_writing_instructions_core.md`, `qa_test_instructions.md`, `unit_loop_core.md`, `dispatch_discipline_instructions.md`, and the `branch-start-plan*`, `branch-qa-test`, `branch-start-user-review-fix-plan` and `branch-implement-*` commands. Then every literal wire string they share (`CLAUDE.md` → the corpus quotes wire strings across files).
- `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_schema`, `pnl_agent_flags` (the `--json-schema` flag) and `PNL_REAP_JQ` (rule 5: *"the decision is structured_output, else result parsed as JSON, else error"*); `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_reap_one`; their tests `cli/test/planning-node-lib.test.mjs`, `cli/test/planning-driver-*.test.mjs` and the stub in `cli/test/helpers/planning-driver.mjs`, which today emits `structured_output` that a real agent session does not.
- `docs/flow-graph-walker.md` → `## 5. The two drivers`, the decision on `--json-schema`, and `### Not yet measured, and the hand step that measures it`, whose `structured_output` entry records a plain-session probe only. The table above corrects it.
- `schemas/`, for how the repository already declares and checks JSON schemas.

## The goal

1. Each of the six agents' returns has one declared schema, owned in one place. Its prose `## Output contract` describes that schema and does not restate it in another form.
2. The orchestrator path and the planning driver read the **same** return. Each validates it against the agent's schema at the handoff, and a return that fails is handled as a defined outcome, never silently guessed at.
3. The planning driver no longer depends on `--json-schema` being applied under `--agent`. Its node outcome is derived from the validated return, with the graph still the one owner of which outcomes a node may have.
4. Renaming a field in one of the six returns breaks a check or a test, not a caller at run time.
5. The mechanism (return shape, where schemas live, how each path validates, what a failed validation does) is chosen so the other 17 agents can adopt it in #380 with no change to it, and is documented where that branch will read it.

## Proposals — for planning to settle, not constraints

- **Return shape.** A single fenced JSON block as the last thing in the agent's reply, or the whole reply as JSON with the human-readable part in a field. Planning weighs what an orchestrating session reads most reliably from an `Agent` result, and what the driver can extract from `result` text with jq 1.5.
- **Where the schemas live.** One schema file per agent under `schemas/`, or a section of each agent definition that a check extracts. Either way, a static check fails when an agent's documented contract and its schema disagree.
- **Validation on the orchestrator path.** An orchestrating session cannot run a JSON-schema validator on every dispatch for free. Planning decides between a validator script the flow calls on the reply, a validation step inside the existing safety contract, and a lighter check of the fields the flow routes on.
- **On a return that fails validation.** Treat it as the existing infrastructure class on the driver: re-dispatched, at most 3 attempts. On the orchestrator path, a re-dispatch or a blocker. Planning settles which and says why.
- **The driver's `--json-schema` flag.** Drop it, or keep it as harmless for a future Claude Code that applies it under `--agent`. The decision object's routing fields (`outcome`, `findings_file`) become part of, or derived from, each agent's own schema.
- **A static check over all agents.** The check that compares a documented contract with its schema can skip agents that have no schema yet, so #380 turns it on agent by agent.

## Constraints

- No new permission in any profile.
- Bash 3.2 and jq 1.5 floors for shell. No new runtime dependency for the outer loop.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- **No measured result is invented.** The table above is the record for `--json-schema` under `--agent`. Anything else the change relies on about how Claude Code returns an `Agent` result or a `result` event is either already recorded or added as unmeasured.
