### Task 7 — Name the Python planning driver in the planning core and the autonomous flow document

**Goal:** Two plugin sentences describe the bash driver, and the cutover falsifies both. Correct them:
- the planning core's opening paragraph, which names `<scripts_dir>/lib/planning-driver-lib.sh` and `planning-node-lib.sh` as what keys on its headings;
- `AUTONOMOUS_FLOW.md`'s routing row, which says the driver runs `flow-walker.sh`.

**Depends on:** Task 2, which makes `devscene-planning-driver` the script-driven path's driver.

**Where this task stops.** These two sentences only. The core's headings, its fences and its `MAX_TOTAL_DISPATCHES = ` line stay byte-identical, because they are wire text, keyed on by the graph's `promptSource` and by Task 9's reader. No other plugin file names the bash driver (scope register rows 17–19).

### Targets

- `plugin/instructions/task_plan_writing_instructions_core.md` — the opening paragraph that begins *"On the opt-in script-driven planning path no session reads this file"*
- `plugin/docs/AUTONOMOUS_FLOW.md` — the table row *"Routing of the planning loop: …"*

**Work:**

- [ ] Planning core:
  - The driver is the watcher's planning driver, `devscene-planning-driver`. It walks the graph in run mode itself and runs no `flow-walker.sh`.
  - It takes each dispatch's prompt from the fenced blocks under the heading that node's `promptSource` names in `<scripts_dir>/flows/task_plan_writing.graph.json`.
  - It takes `MAX_TOTAL_DISPATCHES` as its cap.
  - One repo-relative citation for what keys on the dispatch headings, a module that exists today: `devscene-flow-host/src/devscene_flow_host/host/agent_prompts.py` → `CorePromptBuilder`. Name the cap's reader as *"the planning driver"*, without a module path: Task 9 adds that reader later, and the flow host's README names it (Task 23).
  - Keep the closing list of what is wire text exactly as it stands: the `## Setup (once per session)` heading and its `MAX_TOTAL_DISPATCHES = ` line; the two loop headings; each `###` heading carrying a dispatch block; and the fence count under each.
- [ ] `AUTONOMOUS_FLOW.md`: the routing row keeps *"`flow-walker.sh` and `flows/task_plan_writing.graph.json`"* and its agent-invocable clause. Its script-driven clause now says that on the opt-in script-driven path the watcher's planning driver walks the same graph in-process, running each node as its own headless session. It no longer says the driver runs `flow-walker.sh`.

**Verification:**

- `git grep -nE 'planning-(driver|node|record)-lib' -- plugin` prints nothing.
- `git diff` on the core touches only that opening paragraph. Every `##` / `###` heading and every fence is unchanged.
- Each citation added resolves to a path and symbol that exists when this task lands. The core cites the harness repository's files repo-relative, never as a `${CLAUDE_PLUGIN_ROOT}` path (`.claude/context/plugin.md` → `## Citation`).
