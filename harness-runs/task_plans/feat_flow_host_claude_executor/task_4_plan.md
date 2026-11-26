### Task 4 — Compose `ClaudeExecutor` with its usage sink and inactivity limit in `host/claude_executor.py`

**Goal:** Ship the harness's `claude` executor, `ClaudeExecutor`, which satisfies `graphscene.Executor` structurally. Each `run(dispatch)` launches one headless `claude` session for the dispatched node's agent, judges its stream, reports the session's usage to the host's `UsageSink`, and returns `Completed` or `Failed`. The flow host owns the inactivity limit's value here and passes it in.

**Depends on:** Tasks 1, 2 and 3. This task consumes these contracts exactly as written:

- **Task 1:** `devscene_flow_host.records.plugin_contracts.AgentContract`, with the fields `agent: str`, `tools: tuple[str, ...]` and `return_schema: Mapping[str, object]`.
- **Task 2:** `devscene_flow_host.host.session_stream.judge_session(stream: str, contract: AgentContract, cwd: Path) -> SessionReading`. `SessionReading` has these fields:
  - `result: NodeResult`;
  - `session_id: str | None`;
  - `total_cost_usd: float | None`;
  - `cache_creation_input_tokens: int | None`;
  - `cache_read_input_tokens: int | None`;
  - `model_usage: Mapping[str, object]`;
  - `permission_denials: int`;
  - `withheld_tools: tuple[str, ...]`.

  Task 2 also owns `tests/session_events.py` → `init_event`, `result_event` and `return_block`, which this task's test imports and does not edit.
- **Task 3:** `devscene_flow_host.host.session_process.run_session(argv: Sequence[str], *, cwd: Path, env: Mapping[str, str] | None, inactivity_limit_seconds: float, kill_grace_seconds: float) -> SessionRun`. `SessionRun` has the fields `stdout: str`, `stderr_tail: str`, `returncode: int | None`, `stalled: bool` and `launch_error: str | None`. `run_session` re-raises `CancelledError` after killing the session's process group. Task 3 also owns `tests/fake_claude.py` → `plant(directory, scenario) -> tuple[str, ...]` and the scenario keys `argv_file`, `pid_file`, `child_pid_file`, `steps` (`stdout`, `stderr` or `sleep`) and `exit`. This task's test uses them and does not edit that file.

**Where this layer stops.** No production caller is wired here: the run loop (#484) and the planning cutover (#424) construct this executor. The public names and this task's tests are its callers by decision. This task does not read `.mcp.json`, agent files or `devscene.config.json`. The host passes `contracts`, `session_args` and `agent_args` already built, and the executor passes the flags through unchanged.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (new)
- `devscene-flow-host/src/devscene_flow_host/host/__init__.py`: the layer docstring's list of what the layer answers
- `devscene-flow-host/tests/test_claude_executor.py` (new)

**Work:**

- [ ] `claude_executor.py`, the constants and the usage record.
  - `NODE_INACTIVITY_LIMIT_SECONDS: Final = 2685.0`. A comment beside it derives the value: the pilot's effective `PD_NODE_STALL_SECS`, which `cli/templates/scripts/autonomous-watcher.sh` → `planning_driver_run` computes as `STALL_KILL_SECS` (2700) minus `POLL_INTERVAL_SECS` (15). It is the flow host's value, not a `devscene.config.json` key and not GraphScene's.
  - `KILL_GRACE_SECONDS: Final = 5.0`.
  - `EXECUTOR_FLAGS: Final = ("-p", "--print", "--output-format", "--input-format", "--agent", "--plugin-dir")`.
  - `@dataclass(frozen=True) class SessionUsage` with these fields: `node: str`, `agent: str`, `session_id: str | None`, `started_at: datetime` (UTC wall clock), `duration_seconds: float` (monotonic), `stalled: bool`, `total_cost_usd: float | None`, `cache_creation_input_tokens: int | None`, `cache_read_input_tokens: int | None`, `model_usage: Mapping[str, object]`, `permission_denials: int`, `withheld_tools: tuple[str, ...]` and `result: NodeResult`.
  - `class UsageSink(Protocol)` with `def record(self, usage: SessionUsage) -> None: ...`, shaped like GraphScene's `LaunchSink`.
- [ ] The `ClaudeExecutor.__init__` signature, keyword-only: `command: Sequence[str]`, `plugin_dir: Path`, `plugin_name: str`, `cwd: Path`, `contracts: Mapping[str, AgentContract]`, `inactivity_limit_seconds: float` (**required, no default**: the host passes `NODE_INACTIVITY_LIMIT_SECONDS`), `usage_sink: UsageSink`, `session_args: Sequence[str] = ()`, `agent_args: Mapping[str, Sequence[str]] | None = None`, `env: Mapping[str, str] | None = None`, `kill_grace_seconds: float = KILL_GRACE_SECONDS`.

  Copy every input at construction (tuples, `MappingProxyType`), as `StubExecutor` does, so a later change to the caller's object changes nothing. Refuse each of these with `ValueError` and an exact one-line message:
  - an empty `command`;
  - `inactivity_limit_seconds` not `> 0`, or `kill_grace_seconds` not `>= 0`;
  - a `session_args` or `agent_args` token equal to an `EXECUTOR_FLAGS` member or starting with `<member>=`, the message naming the token;
  - an `agent_args` key with no contract.

  Also call `graphscene.return_violations({}, contract.return_schema)` once per contract, so an invalid schema raises its own `ValueError` here and never mid-run.
- [ ] `async def run(self, dispatch: Dispatch) -> NodeResult`:
  1. Refuse what the caller got wrong. If `dispatch.agent` has no contract, raise `LookupError(f"{dispatch.node}: no agent contract for '{dispatch.agent}'")`. If `dispatch.prompt` is `None`, raise `ValueError(f"{dispatch.node}: the dispatch carries no prompt")`. Both are defects, raised and not returned (`graphscene/src/graphscene/model/execution.py` → *"An exception out of `run` is a defect"*).
  2. Build the argument vector `[*command, "-p", prompt, *session_args, "--output-format", "stream-json", "--verbose", "--agent", f"{plugin_name}:{agent}", "--plugin-dir", str(plugin_dir), *agent_args.get(agent, ())]`. Never add `--json-schema`: on Claude Code 2.1.332 it is not applied under `--agent`, so the return is read from the final `json` block.
  3. Record `started_at` and a monotonic start, then `await run_session(…)` with `cwd`, `env`, the inactivity limit and the kill grace. `CancelledError` propagates untouched, with no usage reported.
  4. Decide the result:
     - a `launch_error` gives `Failed("infra", launch_error)`, with every usage field empty;
     - otherwise `reading = judge_session(run.stdout, contract, cwd)`;
     - when `stalled`, the result is `Failed("infra", f"stalled: the stream was silent for {limit:g} s; the session was killed")`, with the reading's usage fields kept;
     - otherwise the result is `reading.result`.
  5. Call `usage_sink.record(SessionUsage(…))` **exactly once, immediately before returning**.

  The module docstring opens with *"The rule:"* and states the pairing contract: the sink is called once for every `run` that returns a result, before the return, and never for a cancelled or raising run. GraphScene writes its `Launch` row after `run` returns, and a node runs once at a time within a set. So a node's usage record comes just before that node's next `Launch` row, and the host pairs them on `node`, with equal `result` as the check. It lists under *"Deliberately not covered"*:
  - building that pairing into a run loop (#484);
  - the per-agent MCP flags and the shared session flags, which are the host's input;
  - the findings-file presence rule (`host/round_gates.py` → `record_outcome`);
  - writing the stream or a session manifest.
- [ ] `host/__init__.py`: add `ClaudeExecutor`, the harness's `Executor`, to the docstring's list of what the layer answers, and say that it launches one `claude` session per dispatched node. Leave its rule paragraph unchanged.
- [ ] `tests/test_claude_executor.py` has a docstring opening *"The rule this file exists to enforce"*. Contracts are built in the test with the planted draft-07 schema `{"$schema": "http://json-schema.org/draft-07/schema#", "oneOf": [{"type": "object", "properties": {"outcome": {"const": "PASS"}, "findings_file": {"type": "string"}}, "required": ["outcome"], "additionalProperties": false}]}`. Streams are built with `tests/session_events.py`, run through `tests/fake_claude.py` → `plant` under `tmp_path`, and each case is driven with `asyncio.run(…)`. Include:
  - **A typed binding.** `executor: graphscene.Executor = ClaudeExecutor(…)`, so `mypy` `strict` proves the protocol is satisfied.
  - **The argument vector.** The `argv_file` equals a hand-written literal list, with the `session_args` and the per-agent args passed through unchanged and in place.
  - **`Completed` with a detail.** A relative `findings_file` is returned as `Completed("PASS", str(cwd / path))`, and the sink holds exactly one `SessionUsage` whose `node`, `agent`, `session_id`, `total_cost_usd`, cache tokens, `model_usage` and `result` equal the planted literals. `duration_seconds` is checked only as a non-negative `float`.
  - **No `result` event.** It gives `Failed("undelivered", "no result event")`, with one usage record.
  - **A stall.** `inactivity_limit_seconds=0.5`, with an `init` line then `sleep 600`, gives the exact stall reason, `stalled=True` on the usage record and `session_id` kept.
  - **Cancellation.** It re-raises `CancelledError`, the fake's pid is gone, and the sink is empty.
  - **A launch error** gives `Failed("infra", …)`.
  - **Each constructor refusal and each `run` defect** gives its exact message.
  - **A repeated run.** Two `run`s of the same dispatch give two equal argument-vector files and two usage records.
  - **End to end.** One dispatch is driven through `graphscene.execute_set`, with in-test `RunSignals`, `DispatchCounter` and `LaunchSink` classes and a shared event log. The log reads `[("usage", node), ("launch", node)]` in that order, and the `Launch.result` equals the usage record's `result`.

**Verification:**

- `tests/test_claude_executor.py` passes. Its end-to-end `execute_set` case covers the path from GraphScene's engine through `ClaudeExecutor`, `run_session` and `judge_session` to the usage sink and the `LaunchSink`. That is the story index's third `Top risks:` entry, and it is the wiring this branch's public surface owes.
- `bash scripts/typecheck.sh` reports nothing in the three targets. `claude_executor.py` imports from `graphscene` only names in `graphscene.__all__`, and from this package only `devscene_flow_host.records.plugin_contracts`, `devscene_flow_host.host.session_stream` and `devscene_flow_host.host.session_process`.
