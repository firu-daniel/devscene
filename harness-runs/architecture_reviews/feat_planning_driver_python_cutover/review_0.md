# Architecture review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_14_plan.md` — the worktree's `.mcp.json` is read into a value inside `host/agent_flags.py`, not in `records`** (`.claude/context/devscene-flow-host.md` → `## The internal layers`)
   `agent_args` reads the worktree's `.mcp.json`, parses it, cuts its `mcpServers` and raises `RecordError` when it is not a JSON object. All of that happens in a `host` module. The layer document says *"Reading a record into a value is `records`; answering a GraphScene protocol over it is `host`"*. `RecordError` is also *"the one anticipated failure of reading a repository record"* (`## Errors`). No reader of `.mcp.json` exists under `records/` today (`records/plugin_contracts.py` reads the plugin's manifest, agent definitions and schemas only), and the task's Targets add none.
   **Raised against:** "When there is no `.mcp.json`, the file holds `{"mcpServers": {}}`. A `.mcp.json` that is not a JSON object is a `RecordError` naming it."
   **Must hold:** The worktree's `.mcp.json` is read into a plain value by a `records` module. That module carries its `Final` file-name constant, a docstring naming the bash reader it reads as (`pnl_agent_flags`), and a `RecordError` case per unreadable shape. `host/agent_flags.py` only cuts the value it is given and writes the per-agent scratch files.
   **Class:** Broken contract
   **Failure:** If the implementer builds `agent_args` as Task 14 states, then the parsing of `.mcp.json` and its `RecordError` land in `devscene-flow-host/src/devscene_flow_host/host/agent_flags.py`, a record read placed in `host`, which crosses the `records`/`host` boundary the layer document draws.
   **Fix:** Add a `records` target to Task 14, for example `records/mcp_servers.py` → `read_mcp_servers(worktree) -> Mapping[str, object]`. It gets an `MCP_CONFIG_FILENAME: Final = ".mcp.json"` constant, an empty mapping when the file is absent, and a `RecordError` with the exact message when the file is not a JSON object or has a non-object `mcpServers`. Add its test file `tests/test_mcp_servers.py`, and move the malformed-file case there. Change `agent_args` to take the read mapping, or call that reader, and keep only the cutting and the scratch writes in `host`.

2. **`task_16_plan.md` — `scriptsDir` is to be "read through `read_config(main_repo)`", which does not read it, and no `records` change is planned** (`.claude/context/devscene-flow-host.md` → `## The internal layers`, `## What accompanies a new unit here` → *A record reader*)
   `records/config.py` → `HarnessConfig` carries `state_dir` and `phases` only. Its docstring says *"`read_config` reads two keys, `stateDir` and `phases`"*, and *"Every other key"* is deliberately not checked. Task 16 needs the main checkout's `scriptsDir` to build the commit wrapper path, but neither Task 16 nor any other task targets `records/config.py` or `tests/test_config.py`. The implementer is left to read `scriptsDir` out of `devscene.config.json` inside `host/planning_run.py`, which puts a record read in `host`. The alternative is an unplanned edit to `records/config.py` with no docstring rule, no default and no test.
   **Raised against:** "`PlanningHooks` gets the main checkout's `<scriptsDir>/commit-on-branch.sh`, `scriptsDir` read through `read_config(main_repo)`."
   **Must hold:** The `scriptsDir` value Task 16 consumes comes from a `records` reader that reads it. That reader names the bash reader it reads as (`hr_scripts_dir` / `hr_config_load`), has a `Final` default for the schema's default, and has a test per shape. `host/planning_run.py` reads no configuration key itself.
   **Class:** Broken contract
   **Failure:** If the implementer follows Task 16, then `read_config(main_repo).scripts_dir` does not exist, and `scriptsDir` is parsed from `devscene.config.json` inside `host/planning_run.py`, a record read in `host`. Otherwise `records/config.py` changes outside every task's Targets, with no test and no docstring rule.
   **Fix:** Add `records/config.py` (a `scripts_dir` attribute read as the bash library reads `scriptsDir`, with a `DEFAULT_SCRIPTS_DIR` `Final`, and the docstring's two-keys rule extended) and `tests/test_config.py` (its cases) to the Targets of Task 16, or of an earlier `records` task that Task 16 `**Depends on:**`. Then cite the new attribute in Task 16's composition bullet.

3. **`task_17_plan.md` — the `📌 Run mode:` line is to be built by parsing the ledger's `## Run mode` inside `host/run_exits.py`** (`.claude/context/devscene-flow-host.md` → `## The internal layers`, `## Records, and which one is the truth`)
   `pd_run_mode_line` (`cli/templates/scripts/lib/planning-driver-lib.sh`) reads both the `- skipped:` line and every `- ignored:` line under `## Run mode`. `records/ledger.py` → `read_run_mode` returns the skipped ids only. Its heading constant `_RUN_MODE_HEADING` is private, and nothing in `records` reads `- ignored:`. Task 17 lists only `host/run_exits.py` and its test as targets, so the ledger section is parsed in `host`. The layer document says a ledger read is `records`' and that *"A reader returns values and decides nothing"*. Building the line is `host`'s. Reading the section is not.
   **Raised against:** "the `📌 Run mode:` line built as `pd_run_mode_line` built it from the ledger's `## Run mode`."
   **Must hold:** Every value the hand-off narration takes from the flow-progress ledger, including the `## Run mode` section's `- skipped:` value and its `- ignored:` entries, comes from a `records/ledger.py` reader. That reader has a docstring naming `pd_run_mode_line` and has its own test cases. `host/run_exits.py` only formats those values.
   **Class:** Broken contract
   **Failure:** If the implementer builds the hand-off narration as Task 17 states, then the ledger's `## Run mode` section is read line by line in `devscene-flow-host/src/devscene_flow_host/host/run_exits.py`, a record read in `host`. It also re-spells the private `_RUN_MODE_HEADING` / `_SKIPPED_PREFIX` literals that `records/ledger.py` owns.
   **Fix:** Add `records/ledger.py` (a reader returning the `## Run mode` section's skipped value and `ignored` entries as a frozen dataclass, read as `pd_run_mode_line` reads them, with a `Final` `- ignored: ` prefix) and `tests/test_ledger.py` (its cases) to Task 17's Targets, or to an earlier `records` task Task 17 depends on. Have `run_exits.py` format the line from that value. Also name the `records` readers for the `ui_test:` fallback, which is `records/ledger.py` → `read_planning_marks` for `P2`, as `host/planning_hooks.py` already uses it.

4. **`task_12_plan.md` — the new module's docstring is specified without its rule or its "Deliberately not covered" list** (`.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here`, row *A module under `devscene-flow-host/src/devscene_flow_host/`*)
   A new module must land with *"a docstring stating its rule and what it deliberately leaves out"* (`## Shared code and constants`: *"The rule:"* and *"Deliberately not covered"*). Task 12's only docstring instruction covers the 5-dispatch rationale.
   **Raised against:** "The module docstring says why 5 is a flow-host constant, not a `devscene.config.json` key"
   **Must hold:** Task 12 calls for `host/run_control.py`'s docstring to carry a *"The rule:"* paragraph (signals re-read on every call and never cached; the counter written whole; the kill switch read from the main checkout's `stateDir`) and a *"Deliberately not covered"* list (halting on a signal, which is GraphScene's; what a halt does afterwards, which is Task 17's).
   **Class:** Broken contract
   **Failure:** If the implementer writes `host/run_control.py` to Task 12's docstring bullet, then the module lands without the *"The rule:"* paragraph and the *"Deliberately not covered"* list that the layer's accompanying set requires.
   **Fix:** In Task 12's `**The limits.**` bullet, or in a new `**Module docstring.**` bullet, require *"The rule:"* naming `pd_main`'s counter reset and STOP/PAUSE reads as the bash it reads as, and *"Deliberately not covered"* naming halting and acting on a halt.

5. **`task_15_plan.md` — the module docstring has no "Deliberately not covered" list** (`.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here`)
   Task 15 asks for the rule and its bash sources but not for what the module deliberately leaves out.
   **Raised against:** "The docstring states the rule and names `record_outcome` and `pnl_reap` as the rules it reads as."
   **Must hold:** Task 15 calls for `host/planning_executor.py`'s docstring to carry a *"Deliberately not covered"* list, for example retrying a `Failed("infra")` (GraphScene's `AttemptBook`) and constructing the inner executor (Task 16's).
   **Class:** Broken contract
   **Failure:** If the implementer writes the docstring Task 15 specifies, then `host/planning_executor.py` lands without the *"Deliberately not covered"* list the layer's accompanying set requires.
   **Fix:** Extend the bullet: the docstring states *"The rule:"* as given, plus *"Deliberately not covered"* naming the retry and the inner executor's construction.

6. **`task_17_plan.md` — no module docstring is called for at all** (`.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here`)
   Task 17 adds `host/run_exits.py` and its Work names no docstring. Every other new `host` module in this plan carries a `**Module docstring.**` item.
   **Raised against:** "`devscene-flow-host/src/devscene_flow_host/host/run_exits.py` (new)"
   **Must hold:** Task 17 calls for `host/run_exits.py`'s docstring with *"The rule:"*, naming `pd_handoff`, `pd_stop_halt`, `pd_partial`, `pd_ask_park` and `pd_escalate_park` as retired, and *"Deliberately not covered"*, covering the convergence commits run by the `commit_convergence` hook and exit statuses, which are Task 18's.
   **Class:** Broken contract
   **Failure:** If the implementer follows Task 17's Work as written, then `host/run_exits.py` lands with no *"The rule:"* paragraph and no *"Deliberately not covered"* list, which the layer's accompanying set requires.
   **Fix:** Add a `**Module docstring.**` Work bullet to Task 17 carrying the content above.

7. **`task_18_plan.md` — the command module's docstring has no "Deliberately not covered" list** (`.claude/context/devscene-flow-host.md` → `## What accompanies a new unit here`)
   **Raised against:** "**The docstring** states this contract under *\"The rule:\"*, as `commands/flow_walker.py`'s states its own."
   **Must hold:** Task 18 calls for `commands/planning_driver.py`'s docstring to carry a *"Deliberately not covered"* list as well as *"The rule:"*, for example deciding any walk step, which is `host/planning_run.py`'s and `host/run_exits.py`'s.
   **Class:** Broken contract
   **Failure:** If the implementer writes the docstring Task 18 specifies, then `commands/planning_driver.py` lands without the *"Deliberately not covered"* list the layer's accompanying set requires.
   **Fix:** Extend the docstring bullet with a *"Deliberately not covered"* list.

## Should Fix
- **`task_1_plan.md` / `task_2_plan.md` — a flow-host console script launched other than through `flow-walker.sh`.** `.claude/context/conventions.md` → `## The layers` states *"Every caller launches it through `flow-walker.sh`"*, and `.claude/context/devscene-flow-host.md` → `## What this layer is, and what it is not` repeats it. The plan moves the single `uv` launch into `hr_flow_host_exec` and has the watcher call that directly. The convention's substance holds: one launch route, the provisioning refusal, no bash fallback. The plan records the falsified sentence (scope register rows 2–3) rather than hiding it. Graded Should Fix because no step fails, but the stale-rule record must actually reach a maintainer. Scope register rows 1–3 route it through `corpus_staleness`, while the task prompt says this branch *"drops `corpus_staleness`"* (that refers to the driver's own record, but the register should say which channel carries these three entries).
- **`task_10_plan.md` — `RecordError` raised for a write collision in `host/run_records.py`.** `RecordError` is defined as the failure of *reading* a record (`.claude/context/devscene-flow-host.md` → `## Errors`). A park path already occupied is a host write conflict. Prefer a host-owned error, or state in the module docstring why `RecordError` is reused, so that `commands`' exit-status mapping stays principled.
- **`task_4_plan.md` — "Record where each behaviour goes, in the commit body's record line."** The unit commit body is built by `commit-on-branch.sh --unit` from the `**Cause:**` line, in one of three fixed forms (`.claude/context/conventions.md` → `## Commit-message policy`). The implementer cannot write a free-form record line. Put the behaviour-to-task map in the task file or the test header instead. (Outside this lens. Noted in passing.)
- **`task_16_plan.md` — the missing-ledger check composes a `RecordError` in `host`.** `records/ledger.py` → `ledger_path` owns the path. Consider having the existence check and its message live beside it, so the message's path spelling has one owner.

## Nice to Have
- `task_13_plan.md` — `NodeSessions` satisfies both `UsageSink.record(usage)` and `LaunchSink.record(launch)` with one method name. State in the plan that `record` takes `SessionUsage | Launch` and dispatches on type, so the structural fit to both protocols is explicit.
