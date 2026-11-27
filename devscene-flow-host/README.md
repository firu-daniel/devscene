# devscene-flow-host

**Who reads this:** a contributor changing this package. It owns what the package is, what it may depend on, how its lock follows GraphScene's, and how its toolchain is run here.

## What it is

`devscene-flow-host` is the harness's GraphScene host, imported as `devscene_flow_host`. It holds only the code that feeds GraphScene the harness's configuration, records, predicates and hooks, the harness's executor — `ClaudeExecutor`, which runs each dispatched node as one headless `claude` session — and the commands over it. The executor's caller is the planning driver, `run_planning` (`host/planning_run.py`), which walks script-driven planning in GraphScene's run mode (`graphscene/src/graphscene/engine/run_loop.py`). It reads the harness's configuration, flow-progress ledger and round and reviewer files, answers the planning graph's phase and run-mode predicates, applies the reviewer-file rules when a gate's outcome is recorded, resumes a round from the files on disk, and keeps each branch's walk, for GraphScene's `Walker`. It has two command lines (`## The command line`): `devscene-flow-walker`, `flow-walker.sh`'s compatibility command, which every caller reaches through `flow-walker.sh`'s hand-off, that script no longer carrying a bash walker; and `devscene-planning-driver`, one drive of a branch's planning walk, which the watcher launches. The bash planning driver is gone: this command replaced it. Any other DevScene Python integration gets its own `devscene`-prefixed package rather than a place here. Anything useful without DevScene goes in GraphScene (`graphscene/`), not here.

Its source stays in this repository. The npm package carries it, with `graphscene/`, under `dist/python/` (`cli/src/flowHost/layout.ts` → `stagedPythonDir`), and `init` copies both under an adopter's `<scriptsDir>/python/` (`flowHostDir`). Adopters still never import it: they reach it only through the scripts `init` writes.

## What it may depend on

- **The package imports only the standard library, itself and its declared runtime dependencies.** It reaches `graphscene` through its public surface only — `import graphscene` or `from graphscene import <name in graphscene.__all__>`, never a submodule such as `graphscene.engine` — and GraphScene never imports it.
- **`graphscene` is an editable path dependency on `../graphscene`** (`pyproject.toml` → `[tool.uv.sources]`), so one sync provisions both packages, this package's environment imports the checkout's current `graphscene/src/graphscene/`, and no release is needed.
- **The tests stay inside the same boundary, widened only by the `dev` dependency group.** A module under `tests/` imports the standard library, `devscene_flow_host`, the declared runtime dependencies through the same public surface, the `dev` group's tools, and the suite's own support modules — never another package's tests or another layer's source. Reading a tracked file of another layer as test input (the walker's graph file, GraphScene's manifest) is not an import and stays allowed.

`tests/test_boundary.py` and `tests/test_layers.py` enforce these rules for the package; `tests/` itself is not scanned, so the tests' rule is held by review.

## The layers

| Layer | Path | Holds | May import |
|---|---|---|---|
| `commands` | `src/devscene_flow_host/commands/` | The command lines over the host: `main` (`commands/flow_walker.py`), `parse` (`commands/arguments.py`), `render` (`commands/render.py`), the planning driver's `main` (`commands/planning_driver.py`) | `host`, `records`, `graphscene`'s public surface, the standard library |
| `host` | `src/devscene_flow_host/host/` | GraphScene's protocols over the records, and the harness's rules over them: `HarnessPredicateHost` (`host/predicates.py`), `walk_store` (`host/store.py`), `open_walker` (`host/walking.py`), `render_path` (`host/paths.py`), `round_of_gate`, `round_of_writer` and `review_iteration` (`host/reviewers.py`), `RefusalStore` (`host/refusals.py`), `RevisionFindingsStore` (`host/revision_findings.py`), `read_printed` and `PrintedReadsStore` (`host/printed_reads.py`), `round_resume` (`host/resume.py`), `record_outcome` and `HostStep` (`host/round_gates.py`), `start_walk` and `current_step` (`host/re_entry.py`), `judge_session` (`host/session_stream.py`), `run_session` (`host/session_process.py`), `ClaudeExecutor`, `UsageSink`, `AgentPromptBuilder` and `SessionUsage` (`host/claude_executor.py`), `CorePromptBuilder` (`host/agent_prompts.py`), `commit_artifact`, `flip_ledger_entry` and `CommitPointError` (`host/commit_points.py`), `PlanningHooks` (`host/planning_hooks.py`), `decide_planning_entry`, `PlanningDone`, `ContinueWalk` and `StartWalk` (`host/planning_entry.py`), `write_park` and `write_pause` (`host/run_records.py`), `Observations` (`host/observations.py`), `FileRunSignals`, `kill_switch_present`, `FileDispatchCounter`, `planning_limits` and `MAX_CONCURRENT_DISPATCHES` (`host/run_control.py`), `NodeSessions` (`host/node_sessions.py`), `session_args`, `agent_args` and `session_env` (`host/agent_flags.py`), `PlanningExecutor` (`host/planning_executor.py`), `run_planning` and `PlanningRequest` (`host/planning_run.py`), `act_on_exit` and `StopKind` (`host/run_exits.py`) | `records`, `graphscene`'s public surface, the standard library |
| `records` | `src/devscene_flow_host/records/` | The repository's records read into plain values: `read_config` (`records/config.py`), `read_run_mode`, `read_run_mode_entries` and `read_planning_marks` (`records/ledger.py`), `review_verdict`, `round_file_problem`, `next_review_index`, `fail_count` and `round_file_path` (`records/round_files.py`), `read_round_evidence` (`records/round_evidence.py`), `read_index_evidence` (`records/index_evidence.py`), `read_plugin_name`, `read_agent_contract` and `AgentContract` (`records/plugin_contracts.py`), `parse_prompt_source` and `read_prompt_blocks` (`records/prompt_blocks.py`), `read_answered_pairs`, `read_pair_text`, `max_question_index` and `AnsweredPair` (`records/clarifications.py`), `read_max_total_dispatches` (`records/core_limits.py`), `read_mcp_servers` (`records/mcp_servers.py`), `RecordError` (`records/errors.py`) | `records`, the standard library |

Imports point down only, and `records` never imports `graphscene`. The contracts `devscene-flow-host-layers` and `devscene-flow-host-graphscene-outside-records` in `pyproject.toml` hold this, and `tests/test_layers.py` runs them with no cache. A new module lands in the layer its work belongs to. A new layer or a changed import rule lands with its contract change, its planted cases in `tests/test_layers.py` and its row here. The package root exports nothing (`__all__ = []`), because adopters never import it.

## What it reads, answers and keeps

**Records.** `read_config` reads `devscene.config.json` for `stateDir`, `scriptsDir` and `phases` only, and refuses one with no `defaultBranch` as `hr_config_load` does, into a `HarnessConfig`, as `hr_state_dir`, `hr_scripts_dir` and `hr_phase_enabled` read them (`cli/templates/scripts/lib/harness-run-lib.sh`). `read_run_mode` reads the flow-progress ledger's `## Run mode` → `- skipped:` line, as `fw_run_mode_skipped` reads it (`cli/templates/scripts/lib/flow-walker-gates.sh`). Whenever the ledger exists it wins over the skipped ids the caller gives; those are used only when there is no ledger, and with neither the result is a `RunModeUnresolved` carrying the reason. `read_planning_marks` reads the ledger's `P1`–`P3` marks as `pd_ledger_read` does (`cli/templates/scripts/lib/planning-driver-lib.sh`): the last line opening with a mark followed by `<entry>.` wins, and no such line is `None`. `read_prompt_blocks` reads the fenced blocks under a node's `promptSource` heading as `pnl_core_scan` reads them and refuses as `pnl_init` does (`cli/templates/scripts/lib/planning-node-lib.sh`). `read_answered_pairs` reads `<stateDir>/clarifications/<branch>/`'s top-level answered pairs as `hr_top_level_answered_pairs` does, each with its question's `Raised by: ` origin, opening no answer file; `read_pair_text` reads one pair file, only for a pair the caller kept.

**Predicates.** `HarnessPredicateHost` answers `phase_<parity|qa|docs>_off`, true when that phase is off in `phases`, and `run_mode_skips_<id>`, true when the run mode skips `<id>`. Any other name, an unresolvable phase or an unresolved run mode is `None`, which the walk refuses rather than guesses; `refusal_reason` gives the reason. The records are re-read on every arrival, so a ledger written mid-walk is seen at the next one.

**The walk.** `walk_store` keeps one GraphScene `FileStateStore` per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json`, which this repository's ignore rule for that path covers. Another branch's walk is never read. A flat file at `<stateDir>/.flow_walker_state`, left by the retired bash walker, is deleted by `flow-walker.sh` before this command runs, so the walk starts fresh through the caller's `current` → exit `1` → `start`.

**Round and reviewer files.** Each reader reads as the bash function it names (`cli/templates/scripts/lib/flow-walker-gates.sh`). `review_verdict` reads a reviewer file's one `verdict: PASS` or `verdict: FAIL` line, as `fw_review_verdict` does. `round_file_problem` gives the reason a round gate may not use a file — no single verdict line, a `FAIL` with no numbered entry under `## Must Fix`, a `PASS` with one, or an entry lacking `**Class:**` or `**Failure:**` — as `fw_round_file_check` does. `next_review_index` and `fail_count` read a findings folder's next free `review_<n>.md` index and its `FAIL` count, as `fw_next_review_index` and `fw_fail_count` do. `read_round_evidence` reads a round's highest round number, each gate's status at it, whether the next revision note exists and whether the plan changed after the round's files were committed, asking `git` as `fw_round_evidence` does. `read_index_evidence` reads whether a story index has a `## Rejected findings` section, the entries there still open, and whether it has a `## Scope register` section, as `fw_index_evidence` does. A missing round file or findings folder is a value (`None`, `0`), never a `RecordError`, because the walk routes on it. `render_path` renders a graph path template's `{state_dir}`, `{branch}` and `{round}`, and `review_iteration` gives a reviewer outside a round the next free index in its `findingsFolder`.

**Recording a gate.** `record_outcome` records a gate's outcome under the four reviewer-file rules, as `flow-walker.sh`'s `next` does: an outcome whose verdict is `fail` requires a findings file, and so does any verdict outcome at a gate of the open round; a round gate's file must pass `round_file_problem` before its verdict is recorded; a refused file records nothing in the walk — its gate is left out of a `wait`'s pending list, and once no other gate is out every refused gate is re-dispatched as one set in the same round; a held gate at a join whose only gates out are refused ones does not escalate there — the refused gates are re-dispatched first, and the held gate escalates at the round's next join, once every re-dispatched gate has a verdict or is held, so the escalation carries the whole round's verdicts (`host/round_gates.py` → *"The rule:"*); and the third refusal of one gate in a round records the held outcome `error`. The refusals are the host's own record, `RefusalStore`, at `<stateDir>/.flow_walker_state/round_refusals/<percent-encoded branch>.json` behind the lock `<file>.lock`; every call that records takes that lock before the walk's own and releases it after. The `HostStep` returned carries the step and the `refused:` lines it brings.

**Kept findings files.** A findings file given outside an open round set — a non-round reviewer's `FAIL`, such as `ui_review`'s, or one given with `answered` — is kept for the writer's next revision, as `flow-walker.sh` → `next` keeps its one `revision_findings` key. The record is `RevisionFindingsStore`, at `<stateDir>/.flow_walker_state/revision_findings/<percent-encoded branch>.json`. `record_outcome` writes it, under `RefusalStore`'s lock and only when the returned action is not `Refused`; a held outcome at a gate of an open set never touches it; a result that closes a round clears it, as bash's `close_round` overwrites the key; and `start_walk` clears it when the walk started. `HostStep.revision_findings` carries the record as it stands after the call, and `current_step` returns it unchanged. When it is non-empty, `render` prints it as a revision's `arg.findings_file:` lines and a cap's `findings_file:` lines in place of the closed round's files: it takes precedence, as bash's single key holds whichever was written last.

**Printed reads.** The values a step read from disk when it was printed — a non-round reviewer's next free index, a cap's `FAIL` counts and the story index's evidence — are kept as the host's record `PrintedReadsStore`, at `<stateDir>/.flow_walker_state/printed_reads/<percent-encoded branch>.json`, as bash's `next` saves its `out=` lines. `read_printed` does those reads for a step. `record_outcome` and `start_walk` write the record under `RefusalStore`'s lock, and only when the returned action is not `Refused`. `HostStep.printed` carries it, and `render` prints from it and reads no file. `current_step` returns it as kept, so a file written since the step was printed changes nothing; it reads the files only when no record exists.

**Resuming a round.** `round_resume` builds a round's `RoundResume` for GraphScene's `Walker.start` from the files on disk, as `flow-walker.sh`'s `start_round` and `start_record` do. The entry is a round's writer or a round node; any other entry has no resume, and a round with no file has none either. Entered at the writer, the round resumes at the number after its highest. Entered at the round node: a round with files missing whose evidence is consistent records the present gates and opens only the missing ones; any other incomplete round opens the whole set at that round; a complete round that is unreadable or has no `FAIL` is reviewed again; a `FAIL` with the next revision note on disk opens the next round; and a `FAIL` without the note records every verdict, so the round closes at once. Convergence is never inferred from files. `start_walk` reads as `flow-walker.sh`'s `start`: it rebuilds the round position through `round_resume` and `Walker.start`, under the same lock order as `record_outcome`, and clears the refusal record only when the walk started. `current_step` reads as its `current`: it re-reads the saved step with every gate awaiting re-dispatch left out, takes no lock and changes nothing, so a refused gate is never dispatched twice, and it returns the printed reads as kept. The counter and the prompt variants a lost walk loses are lost here too, as in bash.

**The planning driver.** `run_planning` (`host/planning_run.py`) is one drive of a branch's planning walk: it asks `decide_planning_entry` where to enter, runs GraphScene's `start_run` or `continue_run` to a `RunExit`, and `act_on_exit` (`host/run_exits.py`) acts on that exit. Its modules, by layer:

- `records`: `read_max_total_dispatches` (`records/core_limits.py`) reads the planning core's `MAX_TOTAL_DISPATCHES`, the run's dispatch cap; `max_question_index` (`records/clarifications.py`) reads the highest `question_<n>.md` index under `<stateDir>/clarifications/<branch>/` and its `answered/`, as `hr_max_question_index` does; `read_mcp_servers` (`records/mcp_servers.py`) reads the worktree's `.mcp.json` servers; `read_run_mode_entries` (`records/ledger.py`) reads the `## Run mode` section's `- skipped:` value and `- ignored:` entries.
- `host`: `host/run_records.py` writes the park and pause files; `host/observations.py` collects the improvement observations and commits them; `host/run_control.py` answers STOP, PAUSE and the kill switch, keeps the dispatch counter and fixes the run's `ExecutionLimits`; `host/node_sessions.py` writes each node session's records and pairs its usage with GraphScene's `Launch` row; `host/agent_flags.py` builds the session args, the per-agent MCP flags and the session environment, less the variables the flow host's own launch adds; `host/planning_executor.py` wraps `ClaudeExecutor` with `record_outcome`'s findings-file, round-file and kept-findings rules, which run mode does not apply; `host/planning_run.py` composes them; `host/run_exits.py` acts on the exit.
- `commands`: `commands/planning_driver.py`, the command line over `run_planning` and `act_on_exit` (`## The command line`).

**At most 5 dispatches run at once.** `MAX_CONCURRENT_DISPATCHES` (`host/run_control.py`) is passed by `planning_limits` as `ExecutionLimits.max_concurrent_dispatches`. It is a flow-host constant, not a `devscene.config.json` key and not GraphScene's default.

Besides the walk, the driver writes:

- the dispatch counter, `<stateDir>/.dispatch_counter`, one decimal line reset to `0` at each drive (`FileDispatchCounter`);
- a park, `<stateDir>/clarifications/<branch>/question_<n>.md`, `<n>` one past `max_question_index` (`write_park`), and a pause, a block appended to `<stateDir>/PAUSE_PROGRESS.md` and the timestamp in `<stateDir>/PAUSE_ACK` (`write_pause`);
- the observations file, `<stateDir>/improvement_observations/<branch>.md`, committed as the `observations` artifact (`Observations.flush`);
- under the log's `.planning/` directory, `${log%.log}.planning/`, each node's stream as `<seq>-<node>.stream.jsonl` and the `node-sessions.jsonl` manifest; beside the log, the run stream `${log%.log}.stream.jsonl`; and in the log itself, its `[plan-drive] ` narration and each node's formatted output (`NodeSessions`).

## The executor

`ClaudeExecutor` (`host/claude_executor.py`) is the harness's `graphscene.Executor`: each `run` launches one headless `claude` session for the dispatched node and returns its `NodeResult`.

**What it is given.** Every input comes from the host and is copied at construction, so a later change to the caller's object changes nothing:

| Argument | What it is | Who supplies it |
|---|---|---|
| `command` | The argument vector that starts `claude`; must not be empty | The host |
| `plugin_dir` | The plugin's directory, passed as `--plugin-dir` | The host |
| `plugin_name` | The plugin's name, the `<name>:` prefix of `--agent` | `read_plugin_name` (`records/plugin_contracts.py`), which reads `.claude-plugin/plugin.json`'s `name` as `pnl_init` does |
| `cwd` | The session's working directory, and the base a relative `findings_file` is resolved against | The host |
| `contracts` | Each agent's `AgentContract`: its `tools:` line and its return schema | `read_agent_contract` (`records/plugin_contracts.py`), which reads them as `pnl_agent_tools_var` and `pnl_load_schemas` do |
| `inactivity_limit_seconds` | How long the stream may stay silent before the session is a stall; must be `> 0` | The host, as `NODE_INACTIVITY_LIMIT_SECONDS` below |
| `usage_sink` | The host's `UsageSink` | The host |
| `agent_prompt_builder` | The host's `AgentPromptBuilder`: given a `Dispatch`, returns the agent prompt, the text the session is given; it must return the same agent prompt for a repeated run of the same dispatch | The host |
| `session_args` | The shared session flags, passed through unchanged. They include `--add-dir <plugin_dir>`, which the executor does not add: the pilot passes it for every node (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`) | The host; default none |
| `agent_args` | Per-agent flags, such as an agent's MCP flags, keyed by an agent that has a contract | The host; default none |
| `env` | The session's environment; `None` inherits the host's | The host; default `None` |
| `kill_grace_seconds` | How long a killed group has between `SIGTERM` and `SIGKILL`; must be `>= 0` | Default `KILL_GRACE_SECONDS`, `5.0` |

Each contract's return schema is checked at construction through `graphscene.return_violations`, so an invalid schema raises `ValueError` there rather than failing mid-run.

**The agent prompt.** `Dispatch.prompt_variant` is GraphScene's prompt variant — `initial`, `revision`, or `None` for a node with no `prompts` — as `host/prompt_variants.py` reads it for `commands/render.py` → `_block`, and never the text a session is given. `run` calls `agent_prompt_builder` once per run, before the launch, and passes what it returns as the agent prompt. A dispatch whose agent has no contract raises `LookupError`, an exception from the builder propagates, and a builder that returns no non-blank string raises `ValueError`, each before the launch and with no usage record: they are defects in the caller, not a node's result.

`CorePromptBuilder` (`host/agent_prompts.py`) is the host's `AgentPromptBuilder`, reading as `pnl_init` and `pnl_prompt` build a prompt (`cli/templates/scripts/lib/planning-node-lib.sh`). At construction it cuts every dispatch node's `promptSource` blocks through `records/prompt_blocks.py`, in `graph.nodes` order, and raises at the first node that declares no `promptSource`, whose source does not parse or read, or whose heading carries a block count other than `len(prompts)` — or 1 for a node with no `prompts`; block `i` is the prompt of variant `prompts[i]`. It replaces the tokens over the whole text in `pnl_prompt`'s order — `<prompt_path>`, `<state_dir>`, `<branch>`, `<iteration>`, `<review_mode>`, then, only when findings files exist, `<findings_files>` and `<findings_file>` — and leaves every other `<…>` literal. The answered pairs it was given are spent by the first build that succeeds: appended between untrusted-data markers when that dispatch's node declares `prompts` (`consumed` then gives their indices), dropped otherwise, and never appended later, as `pd_run_set` and `pd_pairs_text` do (`cli/templates/scripts/lib/planning-driver-lib.sh`). A dispatch equal to one built before returns the same text.

**The flags it adds.** The session's argument vector is `command`, then `-p <agent prompt>`, then `session_args`, then `--output-format stream-json --verbose --agent <plugin_name>:<agent> --plugin-dir <plugin_dir>`, then the agent's `agent_args`. `--add-dir <plugin_dir>` is not among them: the host passes it in `session_args`. `session_args` and every `agent_args` entry may carry no member of `EXECUTOR_FLAGS` — `-p`, `--print`, `--output-format`, `--input-format`, `--agent`, `--plugin-dir` — bare or as `<flag>=…`; construction refuses one with `ValueError`.

**How a session becomes a result.** The first clause that holds decides:

1. the session could not be launched — `Failed("infra", …)`, every usage field empty;
2. the stream stayed silent for the inactivity limit — `Failed("infra", "stalled: …")`, the usage fields the stream did report kept;
3. otherwise `judge_session` (`host/session_stream.py`) reads the transcript as `PNL_REAP_JQ` does (`cli/templates/scripts/lib/planning-node-lib.sh`), in its order:
   1. no `system`/`init` event — `infra`;
   2. `init` grants a tool the contract does not declare — `agent`;
   3. no `result` event — `undelivered`;
   4. `is_error` with an overload marker in the result text — `undelivered`;
   5. `is_error`, or a subtype other than `success` — `infra`;
   6. no return block, the last fenced `json` block followed by nothing but whitespace — `infra`;
   7. a block that is not one JSON object — `infra`;
   8. a return that fails the contract's return schema — `infra`;
   9. a return with no non-empty string `outcome` — `infra`;
   10. otherwise `Completed`, its outcome the return's `outcome`.

Every reason is one line. `judge_session` departs from `PNL_REAP_JQ` twice: an outcome the node does not declare is `Completed`, because refusing it is the walk's; and a `FAIL`, or a round gate's `PASS`, with no findings file is not refused there, because that is `record_outcome`'s (`host/round_gates.py`).

**The detail.** A `Completed` result's `detail` is the return's non-blank `findings_file`, kept as given when absolute and resolved against `cwd` when relative, so the walk receives the path `cwd` makes absolute rather than one relative to the session; with no such field, or a blank one, the detail is `None`.

**The inactivity limit.** `NODE_INACTIVITY_LIMIT_SECONDS` is `2685.0`: the watcher's stall kill, `STALL_KILL_SECS` (2700), minus its poll interval, `POLL_INTERVAL_SECS` (15) (`cli/templates/scripts/autonomous-watcher.sh`), so a silent node is killed here before the watcher kills the run. It is the flow host's value, not a `devscene.config.json` key and not GraphScene's. `run_session` (`host/session_process.py`) has no default for it or for the kill grace: the caller owns both. Every chunk of stdout resets the clock.

**Killing the session.** `run_session` launches the session in a process group of its own, with stdin closed. On every path out — a normal exit, a stall, `asyncio.CancelledError` and any unexpected exception, whether or not the session's own process has exited — it sends `SIGTERM` to the group, waits up to the kill grace, then sends `SIGKILL` to the group and awaits the exit, so no process of the group is left behind. A cancellation is re-raised after the kill, never turned into a result. This is POSIX only, through `os.killpg`.

**The usage sink.** For every `run` that returns a result, `usage_sink.record` is called exactly once, immediately before the return, with a `SessionUsage`: the node, the agent, the agent prompt, the session id, the start time and duration, whether it stalled, the cost, the cache token counts, the model usage, the permission-denial count, the tools the contract declares that `init` withheld, the whole stdout stream, the stderr tail, the exit status, the validated return object for a `Completed` result (otherwise `None`), and the result itself. A cancelled or raising `run` records nothing. GraphScene writes its `Launch` row after `run` returns, and a node runs once at a time within a set, so a node's usage record comes just before that node's next `Launch` row: the host pairs the two on `node`, with an equal `result` as the check. A `Launch` row GraphScene writes for its total-run timeout (`graphscene/src/graphscene/engine/set_execution.py` → `_run`, its result `Failed("infra", "timed out: no result within <run_timeout_seconds>s")`) has no usage record: the deadline cancels `run`, which records nothing, so the host pairs nothing with that row and does not treat it as a pairing fault. That session's usage is lost, unlike a stall's. That pairing is `NodeSessions`'s (`host/node_sessions.py`); GraphScene's run mode (`graphscene/src/graphscene/engine/run_loop.py`) cannot build it. Writing the stream, and reading a return's fields other than `outcome` and `findings_file` (a writer's `questions`, say), are the planning driver's, from this record.

**`--json-schema` is not passed.** Measured on Claude Code 2.1.332 on 2026-11-26 with `claude -p --output-format stream-json --verbose --model haiku --plugin-dir <plugin> --agent devscene:prompt-injection-reviewer --json-schema <its return schema>`: the `init` event's `tools` carried no `StructuredOutput` tool, and the `result` event carried no `structured_output` key. The flag is not applied under `--agent`, so the executor reads the return from the final fenced `json` block instead.

## The planning hooks

`PlanningHooks` (`host/planning_hooks.py`) is the GraphScene `HookHost` for the planning graph's three hooks. Each is built from the two side effects in `host/commit_points.py`: `commit_artifact`, one `bash <wrapper> --repo <worktree> --artifact <kind> [--round <n>] [--entry <id>] --push` call as `prl_artifact_commit` makes it, and `flip_ledger_entry`, `prl_ledger_flip`'s file half (`cli/templates/scripts/lib/planning-record-lib.sh`). The wrapper is the main checkout's commit wrapper, whose path the caller passes as `commit_wrapper`; this package does not resolve it.

| Hook | Override | Call kinds | Commits |
|---|---|---|---|
| `commit_plan_round` | 6, as `pd_act` → `prl_round_commit` | `AfterRound` | one `plan-round` with the passage's round number |
| `flip_ledger` | 5's flips, as `pd_act` → `prl_ledger_flip` | `AfterRound`, `AfterDispatch`, `BeforeEnd`, `BeforeRound` | for each `LedgerPassage` in the step's `passed`, in order, an entry in `P1`–`P3` flipped then committed as `ledger-flip`, even when the flip changed nothing; any other entry skipped |
| `commit_convergence` | 3 and 4, then the `P3` flip, as `pd_handoff` → `prl_convergence_commits` then `prl_ledger_flip P3` | `BeforeEnd` | `ui-test-plan` when a UI-test plan was written, then `task-plan`, then the `P3` flip and its `ledger-flip` |

The step `flip_ledger` reads is `AfterRound.step`, `AfterDispatch.step`, `BeforeEnd.end` or `BeforeRound.dispatch_set`. Whether a UI-test plan was written is the `End`'s `ui_test` report, status `passed`; without that slot, the ledger decides: `P2` is `x` and the rendered `ui_test_index` exists.

`commit_artifact` returns `True` on the wrapper's exit `0`, `False` on exit `3` (nothing to commit), and raises `CommitPointError` naming the kind, the exit and the last stdout `error: ` line's cause on any other. `flip_ledger_entry` turns the first `- [ ] <id>.` line into `- [x] <id>.`, replacing the file atomically, and leaves a `[x]` or `[-]` entry untouched.

Every hook is repeatable: a commit with nothing new is the wrapper's exit `3`, and a resolved entry's flip leaves the ledger untouched. A hook run on a call kind it does not take raises `ValueError`, an unknown hook `LookupError`; `CommitPointError` and `RecordError` propagate. A pause's `plan-round-partial` commit and the `<ask>` / `<escalate>` parks are not hooks: each is a `RunExit`, acted on by `act_on_exit` (`host/run_exits.py`).

The planning driver calls these hooks: `run_planning` (`host/planning_run.py`) runs GraphScene's run mode with `PlanningHooks` over the main checkout's `<scriptsDir>/commit-on-branch.sh`.

## Where a planning walk enters

`decide_planning_entry` (`host/planning_entry.py`) decides from the ledger, the answered pairs, the saved walk and the drafts on disk, as `pd_entry` does with `pd_pairs`, `pd_walk_usable` and `pd_block_usable` (`cli/templates/scripts/lib/planning-driver-lib.sh`), in `pd_entry`'s order:

1. `P1`, `P2` and `P3` all resolved (`x` or `-`) is `PlanningDone`.
2. The writer pairs are the answered pairs (`records/clarifications.py` → `read_answered_pairs`) minus a `Phase G` origin and a prompt-injection screen origin; a kept pair raised by a UI-test agent makes them UI pairs.
3. A usable saved `Dispatch` or `DispatchSet` is `ContinueWalk` with `outcome=None`, carrying the pairs only when its first node declares `prompts`. A usable saved `Interrupt` is `ContinueWalk` with its `resume_outcome` only when there are writer pairs, so a parked writer keeps its saved variant. Every other saved step, and no saved walk, falls through.
4. Otherwise `StartWalk`, at the first entry that holds: with writer pairs, `ui_writer` for UI pairs else `plan_writer`; `P1` `x` with `P2` resolved, `convergence`; `P1` `x` with the UI-test index on disk, `ui_review`; `P1` `x`, `ui_writer`; the story index on disk, `plan_round`; else `plan_writer` — with `round_resume`'s resume for that entry.

The marks are read by `records/ledger.py` → `read_planning_marks`, as `pd_ledger_read` does. A saved step is unusable when the ledger contradicts its first node — `P1` `x` inside `P1`'s loop, `P2` resolved inside `P2`'s loop, `P1` open inside `P2`'s loop with no `LedgerPassage("P1")` in its `passed` — when a dispatch's required index is absent, or when a findings file a revision carries exists neither as given nor under the repository root. A ledger entry's loop is derived from the graph, not listed: every node with an outcome `RouteEdge` naming that entry, plus such a round node's gates and writer. A `RecordError` propagates.

The planning driver calls `decide_planning_entry`: `run_planning` (`host/planning_run.py`) asks it once per drive, after resetting the dispatch counter, and runs `start_run` for a `StartWalk` and `continue_run` for a `ContinueWalk`.

## Errors

`RecordError` is the one anticipated failure: a record absent, or not readable as the harness writes it, with a one-line message naming the file. Any other `OSError` propagates. A malformed refusal record raises `ValueError` naming the file, and its lock `TimeoutError`, as the walk's store does; a round gate with no `findingsFolder` raises `ValueError`. The `commands` layer alone turns these into exit statuses: `commands/flow_walker.py` → `failure` maps a `RecordError`, a `GraphError`, a lock's `TimeoutError` and any other `OSError` or `ValueError` to exit `2` with its own message, and any other exception to exit `2` as `internal error: <type>: <message>`; `commands/planning_driver.py` → `main` turns every fault into exit `2` the same way. `## The command line` gives both commands' statuses.

## The command line

`devscene-flow-walker` is `flow-walker.sh`'s compatibility command, to which `flow-walker.sh` hands every call: the same four verbs, the same flags plus `--flows`, the same `key: value` output on stdout, and the same exit statuses with one `flow-walker: <cause>` line on stderr (`commands/flow_walker.py` module docstring). It records an outcome only through `record_outcome`, starts only through `start_walk` and re-reads only through `current_step`. Where it answers differently from `flow-walker.sh` is `## Differences from flow-walker.sh`.

Install the console script into the package environment first, outside any sandbox (this provisions every package's environment):

```
bash scripts/python-service.sh provision
```

Then run each verb from the repository root. Inside Claude Code's sandbox, add `--no-cache` after `--no-sync`: without it `uv` exits `2` with `Failed to initialize cache at ~/.cache/uv`, because the sandbox refuses the cache (measured 2026-11-24 on macOS under a run's per-run profile, where `start` and `current` with `--no-cache` exited `0`). Start a walk:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker start --flow <flow> --branch <branch> --flows <dir> [--entry <node>] [--skipped <ids|none>]
```

Record an outcome:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker next --flow <flow> --branch <branch> --flows <dir> --outcome <outcome> [--node <node>] [--findings <path>] [--skipped <ids|none>]
```

Re-read the pending step:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker current --flow <flow> --branch <branch> --flows <dir>
```

Check a round file:

```
uv run --frozen --no-sync --project devscene-flow-host devscene-flow-walker check-round-file --findings <path>
```

| Flag | Verbs | Value |
|---|---|---|
| `--flow` | `start`, `next`, `current` | The flow, `[a-z0-9_]` only; required |
| `--branch` | `start`, `next`, `current` | The branch whose walk this is; required |
| `--flows` | `start`, `next`, `current` | **The launcher's, not `flow-walker.sh`'s**: the directory holding `<flow>.graph.json`, absolute as given or relative under the repository root; required, because bash finds its graph beside itself and this command cannot |
| `--entry` | `start` | The entry node |
| `--skipped` | `start`, `next` | The run mode's skipped ids, comma-separated, or `none`; read only when no flow-progress ledger exists |
| `--outcome` | `next` | The outcome, `[A-Za-z0-9_]` only; required. `FAIL` requires `--findings` |
| `--node` | `next` | The gate the outcome is for, `[a-z0-9_]` only |
| `--findings` | `next`, `check-round-file` | The reviewer's findings file, absolute as given or relative under the repository root, with no tab; required by `check-round-file` |

`parse` (`commands/arguments.py`) refuses a command line as `flow-walker.sh` → `# --- Arguments` does, with the same checks in the same order and the same words: a flag the verb does not take, a value carrying a newline, a required flag missing or given an empty value. A repeated flag keeps its last value.

| Exit | Meaning |
|---|---|
| `0` | An action was printed on stdout; for `check-round-file`, the file is valid and nothing is printed. |
| `1` | A refusal: a usage error; a step the walk refuses, whose cause is the predicate host's `last_refusal` when it has one; `next` or `current` with no saved walk; no `<flows>/<flow>.graph.json`. |
| `2` | A fault: not inside a git repository; a graph that does not load or declares another flow; and every other exception, through `failure`. |
| `3` | `check-round-file` only: the file is invalid or absent. |

Every non-zero exit writes exactly one `flow-walker: <cause>` line on stderr, a newline in the cause flattened, and nothing on stdout. Only `KeyboardInterrupt` and `SystemExit` escape `main`.

`bash scripts/python-service.sh run` is not a route to the command: its `devscene-flow-host` row names no console script.

In an adopting repository the project is `<scriptsDir>/python/devscene-flow-host`, and its environment is built by:

```
bash <scriptsDir>/flow-host-provision.sh
```

That environment is `<scriptsDir>/python/.venv`, set through `UV_PROJECT_ENVIRONMENT` (`cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_provision`), and is not this repository's `scripts/python-service.sh` environment.

Every caller in an adopting repository runs `bash <scriptsDir>/flow-walker.sh <verb> …`, which hands off with this line (`cli/templates/scripts/flow-walker.sh` → `HAND-OFF`):

```
UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv PYTHONPATH=<scriptsDir>/python/devscene-flow-host/src:<scriptsDir>/python/graphscene/src PYTHONDONTWRITEBYTECODE=1 uv run --frozen --no-sync --no-cache --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker <verb> … [--flows <scriptsDir>/flows]
```

It appends `--flows` for `start`, `next` and `current` only, replaces any inherited `PYTHONPATH`, and reads no environment variable to choose the environment, project or sources. An unprovisioned checkout — no `uv`, no environment, or no console script in it — is refused with exit `2`, naming `bash <scriptsDir>/flow-host-provision.sh`. For `start`, `next` and `current` it first deletes a regular file at `<stateDir>/.flow_walker_state` (`## What it reads, answers and keeps` → **The walk.**). `flow-walker.sh` launches `devscene-flow-walker` only; it never launches the planning driver.

**`devscene-planning-driver`** (`commands/planning_driver.py`) is one drive of a branch's planning walk, the watcher's middle step between its setup session and its engine session. Its command line:

```
devscene-planning-driver --branch <branch> --worktree <worktree> --main-repo <main_repo>
    --plugin-dir <plugin_dir> --flows <flows_dir> --log <log_path> --formatter <formatter>
    [--plugin-dir-added] -- <agent_cli> [<shared session flag>…]
```

| Argument | Value |
|---|---|
| `--branch` | The branch whose planning walk this is |
| `--worktree` | The run copy: the walk's repository root and every node session's working directory |
| `--main-repo` | The main checkout, from which the commit wrapper `<main_repo>/<scriptsDir>/commit-on-branch.sh` and the global kill switch `<main_repo>/<stateDir>/AUTONOMOUS_STOP` are resolved |
| `--plugin-dir` | The plugin's directory |
| `--flows` | The main checkout's `<scriptsDir>/flows`, holding `task_plan_writing.graph.json` |
| `--log` | The run log: the driver appends its `[plan-drive] ` narration and each node's formatted output, and writes the node records beside it (`## What it reads, answers and keeps` → **The planning driver.**) |
| `--formatter` | The watcher's stream formatter, a path or `cat`, run as one argv word with a node's stream on stdin, its stdout appended to the log |
| `--plugin-dir-added` | Given when the shared session flags already carry `--add-dir <plugin_dir>` |
| after `--` | The agent CLI, then the shared session flags: the watcher's session vector without `-p`, `--output-format` and `--verbose`, which the executor sets itself |

Every named flag but `--plugin-dir-added` is required with a non-empty value, and a repeated flag keeps its last value.

| Exit | Stdout | Meaning |
|---|---|---|
| `0` | Exactly one line: `consumed:`, then ` <i>` for each answered-pair index appended to a writer's prompt, in `CorePromptBuilder.consumed` order | Handed off: the walk reached its hand-off, or `P1`–`P3` were already resolved. |
| `3` | Exactly one line, `stopped: <kind>`, `<kind>` one of `park`, `pause` (a PAUSE file), `undelivered` (the self-pause after three undelivered sets), `stop` (a STOP file), `cap`, `kill-switch` | A clean stop, its files written. |
| `2` | Nothing | A fault, with one `planning-driver: <cause>` line on stderr, a newline in the cause flattened; once `--log` is known the cause is narrated there too. |

Only `KeyboardInterrupt` and `SystemExit` escape `main`.

The watcher launches it: `cli/templates/scripts/autonomous-watcher.sh` → `planning_driver_run` calls `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_exec` with the console script `devscene-planning-driver`, from the main checkout's `<scriptsDir>/python/`, under the same `uv run` line as `flow-walker.sh`'s hand-off above. `planning_driver_run` maps exit `3` to a stop it classifies from the park, pause or ledger on disk, and exit `0` with a well-formed `consumed:` line to the hand-off; anything else is a failed drive.

## Differences from flow-walker.sh

**Who reads this:** a contributor asking why the command answers differently from the retired bash walker. Each entry names what that walker did, what the command does, and the `cli/test/flow-walker*.test.mjs` cases changed for it when the Python walker replaced it; every suite move listed here is done.

The bash function names this package's docstrings and this README cite from `flow-walker.sh` or `flow-walker-gates.sh`, such as `start_round` and `fw_round_evidence`, name the retired walker's functions, readable in the history of `cli/templates/scripts/flow-walker.sh` and `cli/templates/scripts/lib/flow-walker-gates.sh` before the Python walker replaced it. Likewise the bash planning driver's functions cited in this package's docstrings and this README (`pd_*`, `pnl_*`, `prl_*`) name the retired `cli/templates/scripts/lib/planning-driver-lib.sh`, `planning-node-lib.sh` and `planning-record-lib.sh`, readable in that directory's history before this branch.

**Chosen** — the host's way wins; these stay:

- **The walk's state.** Bash keeps one flat file, `<stateDir>/.flow_walker_state`, for whichever branch is walking, and refuses a `next` or `current` naming another flow or branch. The command keeps one file per branch at `<stateDir>/.flow_walker_state/<percent-encoded branch>.json` (`host/store.py` → `walk_state_path`), so another branch's walk is never read and a different branch is never refused; only a mismatched flow is, in GraphScene's words (`the saved walk is of flow '<saved>', not '<flow>'`). With no saved walk the refusal names the per-branch file: `no walk in progress at <that file>: run 'start' first`. One state directory cannot hold both bash's file and the command's directory at `.flow_walker_state`, so `flow-walker.sh` deletes the flat file before handing `start`, `next` or `current` to the command. Suites: `flow-walker-ui-and-reentry.test.mjs` → *"(11) next for a branch other than the one started is refused"*; `flow-walker-resume.test.mjs`, which deletes and inspects the saved walk.
- **The run-mode refusal.** Bash says `no run-mode record: no flow-progress ledger for '<branch>' and no --skipped`; the command says `… and no skipped ids given` (`records/ledger.py` → `read_run_mode`). No caller outside the walker parses it, and no `flow-walker*` suite asserts its text.
- **The graph.** Bash reads `<its own dir>/flows/<flow>.graph.json` and refuses a `formatVersion` other than 3 with exit `1`. The command reads format 5 at `<flows>/<flow>.graph.json` (`commands/flow_walker.py` → `GRAPH_SUFFIX`); format 5's `vocabulary.hooks`, `promptSource`, `before` and `after` change nothing the command prints, and a graph GraphScene rejects, or one declaring another flow, exits `2` as `cannot load <file>: <violation>` or `graph <file> declares flow …`. A missing graph file still exits `1` as `unknown flow '<flow>': no <file>`. Suite: `cli/test/helpers/walker.mjs` → `WALKER_GRAPH_PATH`, which every `flow-walker*` suite's fixture uses.
- **The locks.** Bash takes one `mkdir` lock directory, `<state file>.lock`, breaks one older than a minute through a `.break` sibling, and gives up after 120 s with exit `2` and an `rmdir` remedy. The command takes two `flock` locks — `RefusalStore`'s, then the walk's — each polled every 0.1 s for 120 s; a lock dies with its process, so there is no stale-lock removal and no `rmdir` remedy. A timeout exits `2` as `cannot lock <file> within 120.0 s` (`host/refusals.py`) or `<file>: not acquired within 120.0 s` (GraphScene's `FileStateStore`). Suite: `flow-walker-concurrency.test.mjs` → *"(2) a lock older than a minute is broken"*, *"(3) a fresh lock held by another call is waited for"* and *"(4) two calls waiting on a stale lock"*; *"(1) three outcomes recorded by simultaneous next calls"* holds unchanged (`tests/test_flow_walker_concurrency.py`).
- **Refusal texts no caller parses.** A refusal the walk makes is worded by GraphScene or the host rather than bash — an undeclared outcome, a gate not pending, a missing `--node`, a finished walk, an `--entry` outside the flow's entries, an unresolvable phase flag; the exit status `1` and the `flow-walker: ` prefix are kept, and `parse`'s usage refusals keep bash's words. Suites asserting only the status and prefix hold unchanged: `flow-walker.test.mjs` → *"(10) an outcome the pending node does not declare is refused"*; `flow-walker-ui-and-reentry.test.mjs` → *"(9) an --entry outside the flow's entries is refused"*. `flow-walker-fan-out.test.mjs` → `assertRefused` also matches the cause: *"(3) an outcome for a gate not pending in the round"* (`/not pending in round 0/`) still matches, but *"(5) a gate's error with two verdicts recorded"* (`/the walk finished/`, GraphScene says `the walk has finished`) and *"(6) --node is required while a set is pending"* (`/name the gate with --node/`, GraphScene says `name the gate with node`) do not.
- **An unexpected exception.** Bash has no such case. The command exits `2` with `internal error: <type>: <message>`, never Python's own exit `1` and traceback (`commands/flow_walker.py` → `failure`). No suite pins it.
- **`current` re-renders.** Bash re-prints the saved action's bytes (`out=`). The command re-reads the saved step and renders it again; every line keeps bash's form. The values bash read from disk at print time — a non-round reviewer's `arg.iteration`, a cap's `rounds:` counts and its evidence lines — come from the printed-reads record (`commands/render.py` → `HostStep.printed`), so a file written since the step was printed changes nothing on `current`. Suites expected to hold unchanged, run against the command by the change that replaced the bash walker: `flow-walker-ui-and-reentry.test.mjs` → *"(10) current re-prints the pending set byte-identically"* and *"(4) UI reviewer FAILs until the cap"*; `flow-walker-resume.test.mjs` → *"(1) a set in flight is re-printed"*, *"(2) a revision a FAIL round queued is re-printed"* and *"(4) a UI reviewer in flight is re-dispatched"*; `flow-walker.test.mjs` → *"(3) architecture FAILs every round until the cap"*. The host's pins: `tests/test_flow_walker.py` → `test_current_reprints_a_ui_reviewers_index_after_its_file_is_written` and `test_current_reprints_the_plan_rounds_cap_after_a_fail_and_an_index_edit`.
- **A rendering fault after the save.** Bash renders before it writes, so every non-zero exit leaves its state file byte-identical. The command saves the walk inside `start_walk` or `record_outcome` and renders after, so a rendering fault exits `2` with the walk already saved (`commands/flow_walker.py` module docstring → *"Deliberately not covered"*). A fault in `read_printed` (`host/printed_reads.py`) after the save exits `2` the same way and removes the printed-reads record, so a later `current` reads the files again. No suite pins it.
- **The held-gate escalation.** At a join whose only gates out are refused, bash escalates the held gate at once (`flow-walker.sh` → `ROUNDS`, `record_in_set`); the refused gate is reviewed again only on resume: `fw_round_evidence` reads the refused file on disk as `unreadable`, so `start` at the round node reopens the round's whole set (`flow-walker.sh` → `STATE`, *"any other incomplete round opens the whole set at that round"*; `flow-walker-resume.test.mjs` → *"(9) inconsistent round evidence dispatches the whole set, and each gate replaces its file"*). The command re-dispatches the refused gates as one set in the same round and escalates at the round's next join, carrying the whole round's verdicts (`host/round_gates.py` → *"The rule:"*). GraphScene gives a host no way to set a due gate aside in an open round, and no GraphScene change is made for this. Both orders review the refused gate again; they differ in when. No `flow-walker*` suite pins this combination, so no suite moves for it: `flow-walker-fan-out.test.mjs` → *"(5) a gate's error with two verdicts recorded"* holds an `error` with no gate refused, and *"(10) the third refusal of a gate escalates"* escalates on the gate's own refusal with nothing else held; the other refused-gate tests, *"(7)"* to *"(9)"* and *"(11)"*, hold no gate. The host's order is pinned by `tests/test_round_gates.py` → `test_a_held_error_beside_a_refused_gate_re_dispatches_first` and `test_a_held_error_waits_while_its_refused_sibling_is_refused_again`.
- **A skipped gate in a round closed from its files.** Bash's `start` at a round node that closes the round from its files (`flow-walker.sh` → `start_round`'s close mode) filters a skipped gate out and prints no `skip:` line for it. The command passes the gate's `skip: <gate> skipped` line through before `round: <n> <PASS|FAIL>`, as a round opened live does; routing is unchanged, and callers already read `skip:` lines among the passed-through lines. Suite: `flow-walker-resume.test.mjs` → *"(6) a finished walk is recognised as finished and replaced by the ledger fallback"*, whose fallback revision now expects `skip: business_parity_review skipped` before `round: 4 FAIL`.

**Still open** — differences to be removed:

None is open. A repeated `## Rejected findings` heading was once listed here and is not a difference: `fw_index_evidence` prints one `evidence:` line however many such headings an index carries, then every open entry after it in file order, as the command does (`tests/test_index_evidence.py`, `tests/test_render.py`).

## The lock follows GraphScene

This package's `uv.lock` pins GraphScene's own runtime dependencies as resolved through the path source. A change to `graphscene/pyproject.toml` → `[project] dependencies` re-locks this package too:

```
bash scripts/python-service.sh --package devscene-flow-host lock
```

`tests/test_graphscene_dependency.py` fails until it is done.

## Running the toolchain

Every command goes through `scripts/python-service.sh`, run from the repository root.

Lint:

```
bash scripts/python-service.sh --package devscene-flow-host lint
```

Typecheck:

```
bash scripts/python-service.sh --package devscene-flow-host typecheck
```

Test:

```
bash scripts/python-service.sh --package devscene-flow-host test
```

`test` forwards paths to `pytest`, relative to `devscene-flow-host/`:

```
bash scripts/python-service.sh --package devscene-flow-host test tests/test_boundary.py
```

Provision every package's environment, outside any sandbox:

```
bash scripts/python-service.sh provision
```

## Gating

The package is gated by gate 13's legs 13h–13j ([`docs/development.md`](../docs/development.md) → `## 5. Verifying a change`).
