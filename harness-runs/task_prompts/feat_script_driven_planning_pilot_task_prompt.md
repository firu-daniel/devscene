`feat_script_driven_planning_pilot` moves the autonomous planning phase out of the orchestrator session. A script walks the planning graph and runs each node as its own headless session. This is a pilot: it is opt-in and the current path stays the default. Measuring it against the orchestrated path, to decide whether the unit loop follows, is a follow-up task, not this branch.

> ⚠️ **Find every anchor in this prompt by its quoted text or symbol name, never by line number.** Verify every claim marked *verify* before planning on it.

---

## Why

Measured on 2026-10-16 from the stream logs of 11 autonomous runs in this repository and 29 in a private adopter's repository. Each model call was attributed to the agent that made it, through `parent_tool_use_id` and the dispatching tool call's `subagent_type`.

- **The orchestrator session is the largest single reader of cached context:** 39.5% of all cache-read tokens here (mean context 231k, peak 408k) and 28.7% in the adopter's runs (mean 212k, peak 456k). It passes only paths, but every agent return, walker printout and ledger read accumulates in its context, and every later turn re-reads all of it.
- **Split by phase,** the planning phase accounts for ~14–15% of the orchestrator's cache reads and the unit loop for ~65%.

So planning is not where most of the saving is. It is the right pilot because it is the one flow that already has a declared graph (`cli/templates/scripts/flows/task_plan_writing.graph.json`, walked by `cli/templates/scripts/flow-walker.sh`), so the routing is done and only the driver changes. `docs/second-runtime-port-decision.md` withdrew a framework port partly because "the orchestrator's share is small". That was measured on planning-only sessions; the whole-run figures above are what this branch acts on. This branch is custom code over the existing walker, not a framework.

**This branch builds on `feat_parallel_plan_reviews` (#370).** That branch makes the gates of a planning round run in parallel, and puts every rule of a parallel round in the graph and the walker: which gates are due, recording outcomes under concurrent calls, the join, the held `error`/`blocker` binding, and resume. *Verify* that it has landed before planning, and read the parallel-round contract in `docs/flow-graph-walker.md`. That contract, not this prompt, is the authority on the walker's output form and its outcome-recording command. This driver follows it and restates none of it.

## What changes

**A driver script runs planning.** A new outer-loop script — or a mode of an existing one, the planner's choice, stated with its reason — drives the planning graph end to end:

1. `flow-walker.sh start`. For every dispatch the walker prints, it launches **one headless session for that node's agent**. The session receives the node's dispatch block, filled with the walker's values (`arg.iteration`, `arg.review_mode`, `arg.findings_file`, prompt variant). **When the walker prints a round's set of dispatches, the driver launches every session of the set at the same time**, from day one, with no sequential mode.
2. As each session ends, the driver parses its result into the node's declared outcome and records it through the walker's outcome-recording command. Results are recorded in the order sessions finish, not in gate order. The walker is safe under concurrent calls (#370), so recording needs no lock of the driver's own. While the walker reports gates still out, the driver waits for their sessions. The walker's response to the set's last outcome is the next action.
3. It repeats until the walk reaches `<terminal_handoff>`, `<ask>` or `<escalate>`.

**A failed session in a set.** When one session of a set ends in `error` or `blocker`, or the stall rules kill it, the driver lets the other sessions of the set finish and records their outcomes. It does not cancel them, because their round files are valid work that a resume keeps. The walker then prints the held binding once. *Verify* how the watcher's stall detection sees several concurrent node sessions, and that one stalled session does not count as the whole driver stalling.

**The session per node.** It uses the same binary seam (`${HARNESS_AGENT_CLI:-claude}`), the same permission profile (`--settings`), `--permission-mode`, `--model`, `--effort`, `--add-dir` and `stream-json` tee as the watcher's main launch. It names the agent with its scoped name, `--agent <plugin>:<agent>`. This keeps the containment property `.claude/CLAUDE.md` → *Agent authoring rules* depends on: measured on Claude Code 2.1.301 (`docs/orchestrator-cost-measurement.md` → `## 4.`), the session's main thread gets exactly the agent's `tools:` list, for plugin agents too, and `--tools`, `--allowedTools` and `bypassPermissions` do not widen it. The launcher must handle the three gaps that section names:
- **MCP tools are untested.** Until a run shows otherwise, pass `--disallowedTools "mcp__*"` (or `--strict-mcp-config`) to every node whose agent grants no MCP tool.
- **An unknown agent name exits 0 with no output.** Treat a node session whose `init` event is missing, or whose tools do not match the agent file's frontmatter, as `error`.
- **The agent set comes from the environment.** Pin the plugin source each node resolves, so an installed copy or a user-level agent of the same name cannot stand in.

**Outcomes come back structured.** Each node session returns its outcome through `--output-format json --json-schema`, the way the mention session in `cli/templates/scripts/remote-run.sh` already does. The schema per agent carries:
- the node's declared outcome key (for example `PASS`/`FAIL`/`blocker`/`error`, or `returned`/`questions`/`no_ui`);
- the findings path where one applies;
- an optional `harness_friction` list: problems with the harness itself the agent hit, such as a refused command, a missing file or a contract it could not follow.

An outcome the node does not declare is an `error`, never a guess.

**The orchestrator's non-routing duties move to the script.** The STOP check, the dispatch counter and its cap, the PAUSE check, heartbeats, and the commits the planning loop makes today, through the commit and push wrappers. The commits are the autonomous planning fork's Overrides 3–6 in `plugin/instructions/task_plan_writing_instructions_autonomous.md`, each with its own trigger, list of paths and subject. Override 6 fires on every `round: <n>` line the walker prints. The driver makes them with the same wrapper calls and never dispatches the committer. Questions (`<ask>`) park through the existing clarification channel the watcher already resumes from. A blocker (`<escalate>`) halts the run the way it does today.

**STOP, PAUSE and the cap work per dispatch set, not per node.** The driver checks STOP and PAUSE and the dispatch cap before launching a set, and it counts every session of the set against the cap. It launches a set only when the whole set fits under the cap. It never launches part of a set. A STOP or PAUSE that arrives while a set is running takes effect at the join, once every session of the set has ended and its outcome is recorded. The round's files are then committed and pushed as `autonomous_pause_and_ledger.md` and #370 state, so a resume dispatches only the gates still due.

**After planning, the orchestrator session starts as usual.** When the walk reaches `<terminal_handoff>`, the script records planning complete in the flow-progress ledger, exactly as the orchestrated loop does today. The watcher then launches the existing task engine session, which resumes from the ledger past planning into implementation. *Verify* that `plan_orchestration_instructions_core.md` already handles "a session that never dispatched a planner" holding the run mode from the record (its `## Setup` step 6 says so). Nothing in implementation, review, QA, gates or close changes on this branch.

**The pilot is opt-in.** Gate it on one switch, a configuration key or a watcher setting, with its reason. Off by default; the orchestrated planning path is untouched when it is off. A configuration key carries its four-place contract (schema, model, check, `docs/config.md`).

## Observations and dispatch additions on this path

- **Improvement observations.** The script appends the planning phase's entries to `<state_dir>/improvement_observations/<branch>.md`, in the format `plugin/instructions/improvement_observations_instructions.md` → `## The entry format` fixes, from two sources:
  - **mechanical facts it owns** — refused tool calls in a node's stream, retries, a loop that hit its cap, parks, non-zero exits, per-node duration and `total_cost_usd`;
  - **each node's `harness_friction` list**, copied with the node it came from.

  It writes on success **and** on a halt or park, because the script outlives the node that failed. The orchestrator's own Phase D block later in the run is unchanged.
- **Dispatch additions.** None on this path. A node's prompt is its dispatch block and nothing else, so there is no `context_notes:` and no `dispatch_additions/` block. Measured over this repository's 11 runs: 1 of 619 dispatches carried a `context_notes:` line.

## Tests

- The driver walks a fixture graph through dispatch → `FAIL` → revision → `PASS` → terminal with a stub agent CLI (`HARNESS_AGENT_CLI` pointing at a script that prints canned structured results).
- A round's set is launched concurrently. The stub records start and end times, and the sessions overlap. Outcomes recorded out of gate order close the round correctly.
- One session of a set ends in `error` while the others pass: they are not cancelled, their outcomes are recorded, and the held binding fires once after the last one.
- An undeclared outcome is treated as `error`.
- `<ask>` parks and a resume continues the saved walk (`flow-walker.sh current`).
- STOP and PAUSE are honoured between dispatch sets. One placed while a set runs takes effect at the join, with the round's files committed. Resuming dispatches only the gates still due.
- The dispatch cap halts, and a set that would cross it is not launched in part.
- Friction and mechanical entries land in the observations file, including on a halt.
- With the switch off, the orchestrated path's existing tests pass unchanged.

## Docs

- `docs/flow-graph-walker.md`: the walker now has two drivers, which one runs when, and how each runs a parallel round. Each one follows the contract #370 wrote there.
- `docs/watcher.md` → `## 2. The scripts`: the new script.
- The planning core: say in one place that on the script-driven path it is not read, and that its dispatch blocks are the prompts' source.
