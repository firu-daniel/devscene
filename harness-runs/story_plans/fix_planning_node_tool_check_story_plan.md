# Story: Stop the planning driver refusing a node whose `init` event lacks a declared tool

## Context

The script-driven planning driver refuses a node session as an agent-class `error` whenever the session's `system`/`init` event's `tools` differ from the agent file's `tools:` line in either direction (`cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`, the `$missing` / `$extra` rule). The task prompt records that Claude Code 2.1.325 gives a session that has `Bash` neither `Glob` nor `Grep`, whatever the agent declares, so every node whose agent declares `Bash` beside `Glob` or `Grep` — `task-plan-writer`, `architecture-reviewer`, `business-parity-reviewer`, `task-plan-reviewer` — is refused, and the first real run with `execution.scriptDrivenPlanning` on parked after node 1.

**The settled design: refuse on `extra` only, and report `missing`.** The prompt leaves the choice between "refuse on `extra` only" and "tolerate a named set" to planning. This plan takes the first. A tool the session lacks cannot widen what it does, so the refusal keeps exactly the protection the check exists for (goal 2): any tool the session was given that the agent does not declare is still an agent `error` at once. The named-set alternative would tie the driver to one Claude Code version's behaviour and park the next run the moment that version changes what it withholds. The other job the two-way comparison did, confirming that the agent resolved, is covered without it. An unknown `--agent` produces no `init` event at all (`docs/orchestrator-cost-measurement.md` → `## 4. Does a session's main agent keep its \`tools:\` allowlist?`, the `Unknown agent` row: exit 0, empty stdout), which `pnl_reap`'s first rule already classes as `error`. The prompt also records that node 1 loaded `devscene` once, so no shadowing copy was loaded. What the one-way check gives up is catching a shadowing definition whose `tools:` line is *narrower*. Task 3 records that as a cost in the decision of record and does not hide it. The trust-check lessons in `<state_dir>/lessons.md` are kept: nothing is widened to "present is fine", and the protection dropped (refusing on `missing`) is one whose other route, no `init` event, is measured.

**The withheld set is still made visible, as the prompt asks.** `pnl_reap` prints it on a new `withheld=` key, and the driver writes one `[plan-drive]` log line per session that withheld anything. It is deliberately a log line and not an observation. Under 2.1.325, every writer and gate session of every run withholds `Glob, Grep`, so an observation per session would flood the improvement-observations intake with a fact that is already recorded. A log line is enough to make a future change in what Claude Code withholds visible in `<branch>.log`.

**Three single-layer tasks in bottom-up order.** Task 1 (`cli`) changes the decision and adds the `withheld=` key in `planning-node-lib.sh` and its suite. Task 2 (`cli`) has the driver read that key and log it, and extends the driver suite's stub so the whole walk is exercised with tools withheld. Task 3 (`general`) records the prompt's measurements in `docs/flow-graph-walker.md`, as its documents of record require, rewrites the decision of record for the `init` check, and updates the one `docs/watcher.md` bullet that still lists those facts as unmeasured. **No measured result is invented.** Task 3 records only what the task prompt's `## Measured, 2026-11-16, Claude Code 2.1.325` section and its `## What happened` log line state, and the `structured_output`-on-a-node-session fact stays unmeasured: the prompt assigns it to `feat_structured_agent_outputs` (#379).

**Constraints every task carries:**
- Bash 3.2 and jq 1.5 floors, as both libraries' headers state (no regex in jq, every jq `if` has an `else`).
- No new permission entry in any profile.
- `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass. Those are the Run gates round's to run, not a unit's.

**Top risks:** The first is a refusal loosened past `missing`, so that a session given an undeclared tool slips through. Task 1 guards it with a case where a session both lacks a declared tool and carries an undeclared one: it must still be `error`/`agent`, and its reason must name the extra tool only. The second is a key `pnl_reap` prints that the driver never reads, leaving the withheld set invisible in the run log. Task 2 guards it by driving a whole walk whose writer session withholds `Glob, Grep` and asserting both that planning hands off and that the exact `[plan-drive]` line is in the log. The third is a document of record that states something the prompt did not measure, or that leaks the measuring machine's absolute plugin path into the tree and so breaks the self-containment gate. Task 3 renders that path as `<main checkout>/plugin` and quotes only the prompt's own values.

**Manual setup required:** after this branch merges, this repository's self-adopted copies `scripts/lib/planning-node-lib.sh` and `scripts/lib/planning-driver-lib.sh` stay at the old bytes until a maintainer runs the forced self-adopt render `docs/development.md` describes (**Regenerating this repository's adoption after a `cli/templates/` change is one forced self-adopt run, read as a dry run first.**). #377 set that precedent as a separate chore after #375. Until then, a run in this repository with `execution.scriptDrivenPlanning` on still parks at node 1. No task in this plan depends on the step, and an adopter's copies follow `init --force` as usual.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom. **Only the committing role flips a marker to `[x]`**: the `committer` agent in every flow that dispatches one, and the orchestrator itself in the supervised flow, which dispatches none. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside per-task files, are informational progress markers only. They are never the iteration source, and the committer never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_planning_node_tool_check/task_<K>_plan.md`. The entries are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [ ] **Task 1** — Refuse a node session only on `init` tools its agent does not declare, and report the withheld ones as `withheld=` _(layer: cli)_ _(points: 15)_
2. [ ] **Task 2** — Log each session's withheld tools as one `[plan-drive]` line, and drive a walk whose sessions withhold `Glob, Grep` _(layer: cli)_ _(points: 15)_
3. [ ] **Task 3** — Record the 2.1.325 `init` measurements and the one-way `init` check in `docs/flow-graph-walker.md` and `docs/watcher.md` _(layer: general)_ _(points: 15)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (goal 3): *"`docs/flow-graph-walker.md` records the measurements above in the form its documents of record require, and no longer lists the plugins and `init`-tools facts as unmeasured."* The register also covers every corpus sentence that states how the `init` tools check decides, because Task 1 changes that decision. The plan's other targets (`cli/templates/scripts/lib/*.sh`, `cli/test/**`) are source and owe no rows.

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root:

```
git grep -nE 'init. tools|init. event.s .?tools|init. whose tools|tools (that )?do not match|shadows .--plugin-dir|unmeasured facts|tool check|the .init. check' -- docs ARCHITECTURE.md README.md ROADMAP.md plugin
```

The plan claims no standing-artifact row class. No standing tracked matrix under `<state_dir>` covers either corpus target, so no procedure entry is owed.

**Closure invariant:** every site the command entry reaches appears as a row below, and every row's site is reached by it.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `ARCHITECTURE.md` → the `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`, `pnl_launch` and `pnl_reap` row ("the `init` event's `tools`, compared with the agent file's `tools:` line") | — | `init. event.s .?tools` | `no-change` | The row names the inputs the outcome is read from and what the coupling to the CLI is. Both stay true: the `tools` are still compared, now one way. It states no refusal rule. |
| 2 | `docs/flow-graph-walker.md` → `### How each runs a parallel round` → **Decision.** ("tools that do not match the `init` event") | — | `tools (that )?do not match` | `change` | Task 3 |
| 3 | `docs/flow-graph-walker.md` → the heading `### The schema-from-graph rule, and the \`init\` check` | — | `the .init. check` | `no-change` | The heading still names the section's subject. It is an anchor, so its text stays byte-stable, and only the body under it changes (rows 4–6). |
| 4 | `docs/flow-graph-walker.md` → `### The schema-from-graph rule, and the \`init\` check` → **Decision.** ("an `init` whose tools differ from the agent file's `tools:` line is an agent `error`") | — | `init. whose tools` | `change` | Task 3 |
| 5 | `docs/flow-graph-walker.md` → the same section → **Reason.** ("a session with tools that do not match is `error` at once") | — | `tools (that )?do not match` | `change` | Task 3 |
| 6 | `docs/flow-graph-walker.md` → the same section → **Cost.** ("a session whose `init` tools carry anything that line does not name is refused") | — | `init. tools` | `change` | Task 3 |
| 7 | `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it` → the bullet "whether the `init` tools under `--json-schema` are the agent's allowlist and nothing more" | — | `init. tools`, `tool check` | `change` | Task 3 |
| 8 | `docs/flow-graph-walker.md` → the same section → the bullet "whether an installed plugin copy shadows `--plugin-dir` for a scoped `--agent`" | — | `shadows .--plugin-dir`, `tool check` | `change` | Task 3 |
| 9 | `docs/flow-graph-walker.md` → the same section → the hand step ("read that node's stream, one command at a time — its `init` tools:") | — | `init. tools` | `change` | Task 3 |
| 10 | `docs/orchestrator-cost-measurement.md` → `## 4. Does a session's main agent keep its \`tools:\` allowlist?` → the measured table's header row | — | `init. tools` | `no-change` | A dated measurement on Claude Code 2.1.301. Its rows are what that version did, and the 2.1.325 figures are recorded beside the decision they change (Task 3), not written over this record. |
| 11 | `docs/orchestrator-cost-measurement.md` → the same section → **Three things a launcher must handle:** → "check that the `init` event's tools match the agent file" | — | `init. event.s .?tools` | `no-change` | The same dated record. Its unknown-agent finding (exit 0, empty stdout) is what the new decision of record cites for the "agent resolved" half, and Task 3's **Reason.** says how the driver now answers it, by the no-`init`-event rule. |
| 12 | `docs/watcher.md` → `## 6. What a human must do, and what ships unexercised` → the bullet **The planning driver's unmeasured facts** | — | `unmeasured facts`, `shadows .--plugin-dir` | `change` | Task 3 |
