### Task 10 — Name the format-4 graph as the planning loop's routing graph in the plugin

**Goal:** The three plugin assets that name `flows/task_plan_writing.graph.json` as the owner of the planning loop's routing name the graph the walker now reads, `flows/task_plan_writing.v4.graph.json`. The plugin's invocations of `flow-walker.sh` are unchanged: the hand-off keeps every verb, flag, output line and exit status a caller parses.

**Depends on:** Task 1, which makes `flow-walker.sh` read `<scriptsDir>/flows/task_plan_writing.v4.graph.json` (passed as `--flows`) and ships that file into `scriptsDir`. The format-3 file still ships, read only by the watcher's planning driver for its node list, and its retirement is #459's. The plugin does not name it as the routing owner.

**Where this task stops.** No change to the instruction cores. The story index's `## Scope register` records them as `no-change`: their invocations, the exit-2 blocker route that now also carries the unprovisioned refusal, and *"Do NOT edit `<state_dir>/.flow_walker_state`"* all still hold.

### Targets

- `plugin/commands/branch-start-plan-autonomous.md` — the `<scripts_dir>` row of `## Resolved values`.
- `plugin/commands/branch-start-plan-semi-autonomous.md` — the `<scripts_dir>` row of `## Resolved values`.
- `plugin/docs/AUTONOMOUS_FLOW.md` — the table row *"Routing of the planning loop: next node, counter, cap, escalation payload"*.

**Work:**

- [ ] `branch-start-plan-autonomous.md`: in the `<scripts_dir>` cell, `flow-walker.sh` with its graph `flows/task_plan_writing.v4.graph.json`. Change nothing else in the cell.
- [ ] `branch-start-plan-semi-autonomous.md`: in the `<scripts_dir>` cell, `flow-walker.sh` and `flows/task_plan_writing.v4.graph.json` as the owners of the planning loop's routing and caps.
- [ ] `AUTONOMOUS_FLOW.md`: in that row, `flow-walker.sh` and `flows/task_plan_writing.v4.graph.json` in `<scripts_dir>`. The rest of the cell — agent-invocable, run by the orchestrating session or by the planning driver — stays.

**Verification:**

- Re-derive the readers before closing: `git grep -n 'task_plan_writing\.graph\.json' -- plugin` prints nothing, and `git grep -n 'task_plan_writing\.v4\.graph\.json' -- plugin` prints exactly the three edited lines.
- No adopter value becomes a literal: the new text names only the shipped file name under `<scripts_dir>` (`.claude/context/plugin.md` → *"No adopter's value is ever a literal here"*).
