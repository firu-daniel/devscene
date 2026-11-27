### Task 23 — Document the planning driver and its command in `devscene-flow-host/README.md`

**Goal:** The package README describes the run driver as it now is:
- the second console script, `devscene-planning-driver`, its command line, its statuses and its launch route;
- the modules Tasks 9–17 added, each under the layer it sits in;
- the end of the bash driver.

It also removes the README's issue numbers (scope register row 10), so no file under `devscene-flow-host/` names one.

**Depends on:** Tasks 18 and 22.
- **Task 18** adds `devscene-planning-driver = "devscene_flow_host.commands.planning_driver:main"`, with the story index's argv contract: exit `0` with `consumed: …`, `3` with `stopped: <kind>`, and `2` with one `planning-driver: <cause>` line.
- **Task 22** finished the docstring side, so the README and the docstrings name the same owners.

**Where this task stops.** This README only. The decisions of record are **Task 24's**, in `docs/flow-graph-walker.md`. `.claude/context/devscene-flow-host.md` is a conventions document. Its sentence *"every caller launches it through `flow-walker.sh`'s hand-off"* is now false, and it is recorded in `corpus_staleness`, never edited here.

### Targets

- `devscene-flow-host/README.md`

**Work:**

- [ ] **The command line.** Add `devscene-planning-driver` beside `devscene-flow-walker`:
  - the argv contract and the three statuses, as the story index's `## Context` gives them;
  - the launch route: the watcher's `planning_driver_run`, through `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_exec`, from the main checkout's `<scriptsDir>/python/`;
  - that `flow-walker.sh` is `devscene-flow-walker`'s launcher only.
- [ ] **`## What it reads, answers and keeps`.**
  - List the new modules in their layers:
    - `records`: `records/core_limits.py`, and `records/clarifications.py`'s `max_question_index`;
    - `host`: `host/run_records.py`, `host/observations.py`, `host/run_control.py`, `host/node_sessions.py`, `host/agent_flags.py`, `host/planning_executor.py`, `host/planning_run.py` and `host/run_exits.py`;
    - `commands`: `commands/planning_driver.py`.
  - State the 5-dispatch limit as a flow-host constant.
  - The files the driver writes besides the walk:
    - the dispatch counter;
    - the park and pause files;
    - the observations file;
    - the node streams and the manifest under the log's `.planning/` directory.
- [ ] **The planning-hooks and entry sections.** *"Nothing in production calls these hooks until the run-mode cutover (#424)"* and *"Nothing in production calls `decide_planning_entry` until the run-mode cutover (#424)"* become statements that the planning driver calls them. Drop the two sentences about the bash driver making the same commits itself.
- [ ] **`## Differences from flow-walker.sh`**, issue numbers out:
  - *"from the bash walker #419 retired"* becomes *"from the retired bash walker"*;
  - *"before #419 merged"* becomes *"before the Python walker replaced it"*;
  - *"(#419 runs them)"* and *"so #419 moves no suite"* drop the number and keep what they say;
  - *"chosen in #472"* follows Task 22's wording.
  - Add one sentence: the bash planning driver's functions cited in this package's docstrings (`pd_*`, `pnl_*`, `prl_*`) name the retired `cli/templates/scripts/lib/planning-*-lib.sh`, readable in that directory's history before this branch.

**Verification:**

- `git grep -nE '#[0-9]+' -- devscene-flow-host` prints nothing. Combined with Tasks 8 and 22, `git grep -nE '#[0-9]+' -- graphscene devscene-flow-host` prints nothing.
- Every module, function and constant the README names exists under `devscene-flow-host/src/devscene_flow_host/` once Tasks 9–18 land. Check by grepping each name.

**Deviations from plan:**
- `git grep -nE '#[0-9]+' -- graphscene devscene-flow-host` is not empty after this task: it prints five lines in `devscene-flow-host/tests/test_node_sessions.py` and `devscene-flow-host/tests/test_planning_driver_walk.py`, each a `#<seq>` dispatch-sequence literal from `node_sessions.py` → `WITHHELD_LINE` / the session-table narration, not an issue number. They are outside this README-only task; the README itself carries no hit. The closing invariant's regex needs narrowing or those literals need an exemption — a decision for the plan owner, not made here.
- Beyond the listed bullets, the same README's other statements made false by Tasks 9–18 were updated so the file describes the driver as it now is (the Goal): `## What it is` (no longer "nothing in production calls the executor", now two command lines), `## The layers` table rows (the new modules plus `records/mcp_servers.py` and `read_run_mode_entries`), the `read_config` sentence (`scriptsDir`, `hr_scripts_dir`), the usage-sink paragraph's "not yet merged" pairing (now `NodeSessions`, matching Task 22's docstring), the hooks' "left to the run driver" (now `act_on_exit`), and `## Errors` (the driver's exit `2`).
- *"(#419 runs them)"* was kept as *"run against the command by the change that replaced the bash walker"*; *"chosen in #472"* does not occur in the README, so nothing followed Task 22's wording there.
- Left unchanged: `## The executor` → **The inactivity limit.** still says `planning_driver_run` computes the pilot's `PD_NODE_STALL_SECS` as `STALL_KILL_SECS` minus `POLL_INTERVAL_SECS`; `PD_NODE_STALL_SECS` no longer occurs under `cli/templates/scripts`. The sentence mirrors `host/claude_executor.py`'s comment above `NODE_INACTIVITY_LIMIT_SECONDS`, which Task 22 kept, so it is flagged rather than reworded here.
