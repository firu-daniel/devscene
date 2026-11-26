# Story: The flow host's `claude` executor — one headless session per node

## Context

This branch adds the harness's `claude` executor to `devscene-flow-host/`. It runs each dispatched node as one headless `claude` session and implements GraphScene's `Executor` protocol (`graphscene/src/graphscene/model/execution.py`): `async def run(self, dispatch: Dispatch) -> NodeResult`, returning `Completed(outcome, detail)` or `Failed(failure, reason)`. It ports what the planning pilot does in bash for planning nodes alone: `cli/templates/scripts/lib/planning-node-lib.sh` (`pnl_load_schemas`, `pnl_agent_tools_var`, `pnl_agent_flags`, `PNL_REAP_JQ`) and the stall kill in `cli/templates/scripts/lib/planning-driver-lib.sh`. It also adds the `asyncio` code `devscene-flow-host` has never had. Nothing in production calls the executor until the run loop (#484) and the planning cutover (#424) land. Its public names and their tests are this branch's only callers, by decision, so they do not count as unwired code. No GraphScene file changes: `Executor`, `Completed`, `Failed`, `Dispatch` and `return_violations` are already in `graphscene.__all__`.

**Where each piece lives.** Every task is in the `devscene-flow-host` layer, and the work follows that package's three internal layers (`.claude/context/devscene-flow-host.md` → `## The internal layers`):

- **`records`** gets the plugin reader (Task 1): the plugin's name, plus each agent's declared `tools:` and return schema, read into an `AgentContract`. It works the way `pnl_init`, `pnl_agent_tools_var` and `pnl_load_schemas` read them, so the executor itself opens no configuration or plugin file.
- **`host`** gets three modules:
  - `host/session_stream.py` (Task 2) is a pure judgement of a finished `stream-json` transcript. It produces the node's `NodeResult` and the per-session usage fields.
  - `host/session_process.py` (Task 3) is the process supervisor. It launches with `asyncio.create_subprocess_exec`. It detects inactivity on the stream and kills the session's whole process group when the stream stalls or the run is cancelled.
  - `host/claude_executor.py` (Task 4) composes the other two into `ClaudeExecutor`, adds the usage sink, and owns the inactivity limit's value.
- **The package's own README** documents the executor (Task 5).

**What the executor is told, and by whom.** `Dispatch` supplies `node`, `agent` and `prompt`. Everything else comes through the constructor:

- the `claude` command prefix and the session's working directory;
- the plugin directory and name;
- the `AgentContract` for each agent;
- the host's shared session flags, passed through unchanged — sandboxing, permission mode, settings, model and allowed tools all live here, so the executor chooses none of them;
- extra flags for each agent (the pilot's MCP-config flags are an example);
- the environment;
- the inactivity limit;
- the usage sink.

The executor adds only the flags it needs to read the stream and to launch the agent: `-p <prompt>`, `--output-format stream-json --verbose`, `--agent <plugin>:<agent>` and `--plugin-dir <dir>`. It refuses to construct when the host's flags already carry one of these. It never passes `--json-schema`: on Claude Code 2.1.332 that flag is not applied under `--agent`, so the return is read from the final fenced `json` block of the `result` text.

**How a session is classified.** The order is the pilot's `PNL_REAP_JQ`, with two deliberate departures (Task 2):

1. A missing `init` event is `infra`.
2. An `init` that grants tools the agent does not declare is `agent`. This is the pilot's class: a retry would launch with the same grant. A declared tool the session lacks is never refused. It is reported as withheld, because `Glob`/`Grep` are still withheld from sessions holding `Bash` on 2.1.332.
3. No `result` event, or an API overload, is `undelivered` (#487).
4. A session that ended in error is `infra`.
5. A return block that is missing, is not one JSON object, or fails its schema (`graphscene.return_violations`) is `infra`, and the engine retries it for that node.

The departures:

- An outcome the node does not declare is returned as `Completed`, because refusing it is the walk's job (`graphscene/src/graphscene/model/execution.py` → *"never the executor's to check"*).
- The pilot's findings-file presence check is left to the host's `record_outcome` rules (`devscene-flow-host/src/devscene_flow_host/host/round_gates.py`). `Dispatch` cannot tell a round gate from a review loop's writer: both carry `round_number`.

A `findings_file` the return carries becomes `Completed.detail`, made absolute against the session's working directory. The pilot saw a `PASS` path come back relative and `FAIL` paths come back absolute.

**Usage, and how it matches a launch row.** Each session's usage goes to a host-supplied `UsageSink` (Task 4), and GraphScene's types stay untouched. A usage record carries:

- the node, the agent and the session id;
- the wall-clock start and the monotonic duration (GraphScene's `Launch` has no duration);
- `total_cost_usd`, the cache tokens and `modelUsage`;
- permission denials and withheld tools;
- whether the session stalled;
- the `NodeResult` itself.

The matching rule is decided here. The sink is called exactly once for every `run` that returns a result, immediately before it returns, and never for a cancelled or raising run. The engine writes its `Launch` row only after `run` returns, and within one set a node runs once at a time. So a node's usage record always comes just before that node's next `Launch` row, and the host pairs the two on the node, with `result` equal on both as the check. Task 4 tests this ordering through `graphscene.execute_set`. Building that pairing into a run loop is #484's work.

**The inactivity limit.** It belongs to the flow host, not to `devscene.config.json` or GraphScene. It is `NODE_INACTIVITY_LIMIT_SECONDS` in `host/claude_executor.py`, set to `2685.0`. That is the pilot's effective value: `autonomous-watcher.sh` → `planning_driver_run` derives `PD_NODE_STALL_SECS` as `STALL_KILL_SECS` (2700) minus `POLL_INTERVAL_SECS` (15). The constructor takes the limit as a required argument, so the host always passes it in. It is named for what it measures, which is silence on the stream, not total run time (`harness-runs/lessons.md` → *"Name a ported limit by what the new code measures"*). The engine's only time limit stays `ExecutionLimits.run_timeout_seconds`.

**Testing without a real session.** The suites use the substitutes this layer already uses: planted files under `tmp_path`, and the code under test taking its paths and command as parameters. Task 3 adds `devscene-flow-host/tests/fake_claude.py`. It is a support module that runs as a script under `sys.executable` from a scenario file planted under `tmp_path`, and it writes only there. Task 2 adds `devscene-flow-host/tests/session_events.py`. It builds `init` and `result` event lines in the shape measured on 2.1.332, so every fake stream carries the fields a real one does. Async code is driven with `asyncio.run(…)` inside synchronous test functions, as `.claude/context/docs-retrieval.md` → `## Testing — what "done" means here` does. No mocking aid is used.

**Top risks:** The first risk is a cancelled or stalled run that leaves `claude` running, or leaves a child process it started (an MCP server, a `Bash` tool) running. Task 3 guards this: it launches each session in its own process group, kills the whole group on stall, on cancellation and on every other exit path, and its tests assert that both the fake session and a child it spawned are gone. The second risk is a large `result` event silently truncated or refused by the stream reader's default 64 KiB line limit. Task 3 reads the stream in chunks rather than lines and tests a line over 64 KiB. The third is a usage record that cannot be matched to its `Launch` row. Task 4 fixes the sink-before-return rule in the module docstring and tests that order through `graphscene.execute_set`.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside the per-task files, are informational progress markers only, and the commit step never touches them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/feat_flow_host_claude_executor/task_<K>_plan.md`. The entries are in ship order, bottom-up through the package's internal layers (`records`, then `host`), with the package's documentation last.

1. [x] **Task 1** — Read the plugin's name and each agent's `AgentContract` in `records/plugin_contracts.py` _(layer: devscene-flow-host)_ _(points: 15)_
2. [x] **Task 2** — Judge a finished `stream-json` transcript into a `NodeResult` and usage fields in `host/session_stream.py` _(layer: devscene-flow-host)_ _(points: 20)_
3. [x] **Task 3** — Supervise one session process with inactivity detection and group kill in `host/session_process.py` _(layer: devscene-flow-host)_ _(points: 20)_
4. [x] **Task 4** — Compose `ClaudeExecutor` with its usage sink and inactivity limit in `host/claude_executor.py` _(layer: devscene-flow-host)_ _(points: 20)_
5. [x] **Task 5** — Document the executor in `devscene-flow-host/README.md` and the package docstring _(layer: devscene-flow-host)_ _(points: 10)_

## Scope register

Task 5 edits durable corpus text (`devscene-flow-host/README.md`), so the plan lists the corpus sites that describe what the flow host holds.

**Scope predicate**, quoted verbatim from the task prompt's `## Decided (2026-11-25)` (task data, quoted as data): *"**The executor lives in `devscene-flow-host/`** and implements `graphscene.Executor`"*. A corpus site is in scope when it states what `devscene-flow-host` holds, or lists the modules its `host` layer holds, because the branch adds an executor that those statements do not name.

**Derivation entry 1 — sites stating what the flow host holds (command).** Re-run verbatim from the checkout root: `git grep -n "executor configuration" -- '*.md' ':!harness-runs' ':!examples'`

**Derivation entry 2 — sites listing the `host` layer's modules (command).** Re-run verbatim from the checkout root: `git grep -n "host/walking.py" -- '*.md' ':!harness-runs' ':!examples'`

No standing matrix under `harness-runs/` has a row for `devscene-flow-host/README.md`, so no standing-artifact derivation entry is owed. The package's `__init__.py` docstrings say the same thing as the README. They are source-code docstrings, outside the corpus, and Tasks 1, 4 and 5 update them as their own targets.

**Closure invariant:** every site either derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host` table row ("the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks") | — | entry 1, `executor configuration` | `no-change` | A conventions document is never a plannable target. The branch makes it incomplete: the package now holds the harness's executor itself, not only executor configuration. Recorded in `corpus_staleness` for a supervised `/devscene:analyze .claude/context/conventions.md` or a hand edit. |
| 2 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet ("It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks") | — | entry 1, `executor configuration` | `no-change` | Conventions document. Same staleness as row 1, in the same `corpus_staleness` entry. |
| 3 | `.claude/context/conventions.md` → `### Where a new responsibility goes`, the row "code that feeds GraphScene the harness's configuration, records, predicates, executor configuration or hooks" | — | entry 1, `executor configuration` | `no-change` | Conventions document. Same staleness as row 1, in the same `corpus_staleness` entry. |
| 4 | `devscene-flow-host/README.md` → `## What it is` ("It holds only the code that feeds GraphScene the harness's configuration, records, predicates, executor configuration and hooks") | — | entry 1, `executor configuration` | `change` | Task 5 |
| 5 | `.claude/context/devscene-flow-host.md` → `## The internal layers`, the source line under the table citing `devscene-flow-host/src/devscene_flow_host/host/walking.py`; the `host` row above it ("GraphScene's protocols over the records — the `PredicateHost`, the walk's `StateStore`, the composed `Walker`") | — | entry 2, `host/walking.py` | `no-change` | Conventions document. The `host` row no longer lists everything the layer holds: the executor answers a GraphScene protocol but does not sit over the records. Recorded in `corpus_staleness`. |
| 6 | `.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth` ("The records are the source of truth, re-read on every arrival", citing `host/walking.py`) | — | entry 2, `host/walking.py` | `no-change` | Conventions document, and nothing the branch does falsifies this rule. The executor reads no record, and `read_agent_contract` reads each time it is called. |
| 7 | `devscene-flow-host/README.md` → `## The layers`, the `host` row (lists `open_walker` (`host/walking.py`) among the layer's names) | — | entry 2, `host/walking.py` | `change` | Task 5. The same task also adds `read_agent_contract` to the `records` row beside it. |
