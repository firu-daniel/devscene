### Task 3 — Record the 2.1.325 `init` measurements and the one-way `init` check in `docs/flow-graph-walker.md` and `docs/watcher.md`

**Goal:** Make the decision of record match the check Task 1 ships: refuse on an undeclared `init` tool, and log a withheld one. Record the task prompt's measurements in the form `docs/flow-graph-walker.md`'s documents of record require, so that the `init` tools under `--json-schema` and the plugins a node session loads are no longer listed as unmeasured, there or in `docs/watcher.md`.

**Depends on:** Task 1 and Task 2, whose behaviour this task describes and does not change:
- **Task 1:** `pnl_reap` refuses a session (`kind=error`, `class=agent`, reason `the init event grants tools the agent does not declare: [<tools>]`) only when its `init` tools carry one the agent's `tools:` line does not name. It prints the declared non-`mcp__` tools the `init` lacks on `withheld=`, and refuses nothing for them.
- **Task 2:** `pd_reap_one` writes one `[plan-drive] #<seq> <node> (<agent>): the init event lacks declared tools [<tools>]; not refused` line per session that withheld anything, and adds no observation.

Cite both by file and symbol (`planning-node-lib.sh` → `PNL_REAP_JQ`, `pnl_reap`; `planning-driver-lib.sh` → `pd_reap_one`), as the sections around them already do.

**The only source of measured values is the task prompt.** Every measured value this task writes comes from `harness-runs/task_prompts/fix_planning_node_tool_check_task_prompt.md`: its `## What happened` section (the run, its date, the Claude Code version, the `[plan-drive]` line and node 1's `init` tools) and its `## Measured, 2026-11-16, Claude Code 2.1.325` section (the launch form, the four-row table, the orchestrator-session sentence, and the plugins and `--json-schema` facts). Quote values exactly as the prompt gives them, and add none: no jq command it does not state, no output it does not quote, and none of the run's turn, cost or duration figures. **One substitution is required:** the prompt's `plugins` entry names the measuring machine's absolute plugin path. Write that `path` as `<main checkout>/plugin`, as the prompt's own launch form does, because nothing in this tree may name a location on the machine that wrote it (`.claude/context/conventions.md` → `## The testing bar`, the self-containment gate).

### Targets

- `docs/flow-graph-walker.md` — `## 5. The two drivers`: `### How each runs a parallel round`, `### The schema-from-graph rule, and the \`init\` check` and `### Not yet measured, and the hand step that measures it`.
- `docs/watcher.md` — `## 6. What a human must do, and what ships unexercised`, the bullet **The planning driver's unmeasured facts**.

Every heading named above keeps its text byte for byte. Each one is cited from elsewhere, `docs/watcher.md` cites the last of them by name, and only bodies change.

**Work:**

- [ ] `### How each runs a parallel round` → **Decision.**: in the **Every other `error`** list, replace "tools that do not match the `init` event" with "an `init` event carrying a tool the agent does not declare". Change nothing else in the section.
- [ ] `### The schema-from-graph rule, and the \`init\` check`: rewrite three paragraphs.
  - **Decision.**: an `init` whose tools carry one the agent file's `tools:` line does not name is an agent `error`, recorded at once. A declared tool the `init` lacks is not refused: `pnl_reap` prints it on `withheld=`, and the driver logs one `[plan-drive]` line for it (`pd_reap_one`).
  - **Reason.**: a missing tool cannot widen what a session does, and an agent that needs a withheld tool fails visibly in its own work. Claude Code 2.1.325 withholds `Glob` and `Grep` from every session that has `Bash` (the measurement below), so a two-way check refused every writer and gate node. In the **An unknown agent fails silently with exit 0:** clause, say that an unknown agent produces no `init` event (`docs/orchestrator-cost-measurement.md` → `## 4. …`, the `Unknown agent` row) and is caught by the no-`init` rule. Drop the claim that a tools mismatch catches it.
  - **Cost.**: a shadowing definition is now caught only when its `tools:` line names a tool the pinned one does not. A narrower one passes. The driver ties its refusal to nothing a Claude Code version withholds, and a change in what is withheld shows in `<branch>.log`, not as a park. A log line is the deliberate surface, not an observation.
- [ ] `### Not yet measured, and the hand step that measures it`: move the two facts out of the *"Two facts the driver depends on are not measured on a real Claude Code session:"* list. Record them as measured entries in the same form as the existing `structured_output` entry: what was measured, on which version and date, the command, and the exact output.
  - **The `init` tools under `--json-schema`.** On 2026-11-16, Claude Code 2.1.325, node 1 (`plan_writer`) of the run `fix_run_commit_trailer_amend`, launched by the driver with `--json-schema`, had an `init` `tools` list of `["Read","Write","Edit","Bash"]` against the `tools:` line `Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs`. `--json-schema` added no tool. Quote the four-row table from the prompt for the three sessions launched by hand in the form `claude -p --output-format stream-json --verbose --plugin-dir <main checkout>/plugin --agent devscene:<agent>`, with the prompt's conclusion: a session that has `Bash` is given neither `Glob` nor `Grep`, a session without `Bash` keeps them, and no session was given a tool its agent does not declare. Add the prompt's sentence on the orchestrator session, launched with no `--agent`. Quote the log line the old check produced, `[plan-drive] #1 plan_writer: error (the agent tools do not match its init event: missing [Glob, Grep], extra [])`, as the effect that motivated the change.
  - **Plugins loaded beside `--plugin-dir`.** On the same `init` event, `devscene` was loaded once, as `{"name":"devscene","path":"<main checkout>/plugin","source":"devscene@inline","version":"0.7.1"}`, beside Claude Code's built-in plugins, and no installed copy was loaded beside the `--plugin-dir` one.
- [ ] The same section's remainder:
  - State that the one fact still not measured on a node session is that its `result` event carries `structured_output` under `--json-schema`. The `structured_output` entry above measures it on a plain session, and the node-session question belongs to `feat_structured_agent_outputs` (#379), as the prompt says. Do not record a result for it.
  - Keep the hand step's key-setting command and the third (`structured_output`) `jq` read. Remove the first two reads and their comparison sentence, or recast them explicitly as the way to re-measure on a later Claude Code version, without claiming either produced the values recorded above.
  - Every command this task writes, the launch form above included, goes in a fenced block, one command per line, as the existing `structured_output` entry does (`<state_dir>/lessons.md` → `## Adopter-facing documentation`, first rule).
  - Keep the closing *"Each fact is recorded with its command, its exact output, …"* sentence.
- [ ] `docs/watcher.md` → **The planning driver's unmeasured facts**: rewrite the bullet so it no longer lists the `init` tools under `--json-schema` or plugin shadowing as unmeasured. It names `structured_output` on a node session as the one fact still unmeasured, and keeps its pointer to `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it`.

**Verification:**

- Re-run the story index's `## Scope register` command entry, verbatim, from the checkout root. Every hit must be a row of the register, and every row marked `change` must now read as this task's Work describes. A hit outside the register is a finding to raise, not to absorb.
- `git grep -nE '/Users/|/home/' -- docs/flow-graph-walker.md docs/watcher.md` adds no hit this task wrote.
- Every value in the two new measured entries can be found, character for character apart from the `<main checkout>` substitution, in the task prompt's `## What happened` or `## Measured, 2026-11-16, Claude Code 2.1.325` sections.
- `docs/flow-graph-walker.md` no longer contains *"whether the `init` tools under `--json-schema` are the agent's allowlist"* or *"whether an installed plugin copy shadows `--plugin-dir`"* as unmeasured items, and each heading listed under `### Targets` is unchanged.

**Deviations from plan:**

- **Reason.** wording: the plan says the two-way check "refused every writer and gate node"; the measured table shows `prompt-injection-reviewer` (no `Bash`) keeps `Glob`/`Grep` and would pass, so the sentence uses the task prompt's own scope, "every node whose agent declares `Bash` beside `Glob` or `Grep`".
- **Deferral citation:** `#379` is cited with `ROADMAP.md` → the `Structured agent outputs` row beside it, because `.claude/context/conventions.md` → `## Documents of record` requires a deferral to resolve against a roadmap row; `ROADMAP.md` carries no issue number for that row.
- **Hand step:** the first two `jq` reads are kept, recast as the re-measurement route for a later Claude Code version, with a sentence stating the 2.1.325 values were not recorded as their output.
