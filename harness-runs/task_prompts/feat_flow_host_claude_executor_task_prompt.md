`feat_flow_host_claude_executor` builds the harness's `claude` executor in `devscene-flow-host/`: one headless `claude` session per node, implementing GraphScene's `Executor` protocol from #420. Part of #376.

## Why

`lib/planning-node-lib.sh` does this in bash, for planning only. Every flow the harness turns into a graph should share one executor, and #424's planning cutover runs on this one.

## Decided (2026-11-25)

- **GraphScene names no model provider, so no generic `claude` executor ships in `graphscene/`.** This replaces the 2026-11-22 decision to put an optional generic `claude` executor in GraphScene's `adapters` layer. GraphScene's nodes are declared data, and `agent` is a string the host interprets. An adopter writes an executor against #420's interface for whatever runs their nodes: Claude, another provider, a local model, a script or a human. The only built-in executor is #420's `StubExecutor`. `.claude/context/graphscene.md` → *"executing its agents … in a separate distribution outside `graphscene/`"* now holds as written.
- **The executor lives in `devscene-flow-host/`** and implements `graphscene.Executor`: `async def run(self, dispatch: Dispatch) -> NodeResult`, returning `Completed(outcome, detail)` or `Failed(failure, reason)` with `failure` one of `infra`, `agent` or `undelivered`.
- **Per-session usage goes to a usage sink the host passes in when it constructs the executor.** `NodeResult` stays as #420 shipped it. Cost and cache tokens are provider-specific, so they never enter GraphScene's types.
- **Detecting a stall is this executor's** _(updated 2026-11-26)._ A stall is an inactive session, such as a stream that stops producing events, as the pilot's `PD_NODE_STALL_SECS` measures it. Only the executor sees the stream, so it kills the session and returns `Failed("infra", …)`, with the inactivity limit passed in by the host. The engine's only time limit is an optional total-run limit (`ExecutionLimits.run_timeout_seconds`, default `None`), applied by `execute_set`.
- **The inactivity limit's value is `devscene-flow-host`'s** _(decided 2026-11-26)._ The host keeps it and passes it to the executor's constructor. It is not a `devscene.config.json` key, and not GraphScene's: the flow host is the harness's own implementation of its flows, so values that tune them stay in it.
- **It chooses no sandbox or permission setting.** Sandboxing, permission mode and allowed tools come from the harness configuration through the host, and are passed through to `claude` unchanged.
- **The public surface and its tests are this branch's callers.** Nothing in production calls this executor until #484's run loop and #424's cutover. That is expected for this milestone and is not un-wired code.

## Leads

_The leads below are starting points from #376, #420 and the discussion that split them, not requirements. The planning session decides what holds when this branch is planned._

- **What #420 shipped, as merged.** `graphscene/src/graphscene/model/execution.py` states the protocol's rules:
  - `run` must be cancellable: on `asyncio.CancelledError` it releases what it holds and re-raises;
  - an anticipated failure is returned as a `Failed`, never raised;
  - a run may be repeated for the same dispatch, so side effects must be repeatable.

  For a subprocess, cancellation means terminating the `claude` process before re-raising. With an `asyncio` interface the launch is `asyncio.create_subprocess_exec`, not blocking `subprocess`.
- **What the executor is told, and by whom.** `Dispatch` carries `node`, `agent` and `prompt`. Everything else comes through the constructor, from the host: the CLI arguments, the plugin directory, the return schema for each agent, the sandbox and permission settings, and the usage sink. The executor reads no configuration file itself.
- **The return check.** `graphscene.return_violations(document, schema)` validates an already parsed document. Taking the final fenced `json` block out of the session's `result` and parsing it stays the executor's job. A missing, unparsable or schema-violating return is `Failed("infra", …)`, retried for that node. `undelivered` is kept for a session that delivered nothing readable at all, such as no `result` event or an API overload (#487). Every `plugin/schemas/*.return.json` declares draft-07 and uses no `$ref`. `return_violations` refuses a `$ref` that does not resolve inside the schema, without retrieving anything.
- **Testing without a real session.** `.claude/context/graphscene.md` and `.claude/context/devscene-flow-host.md` leave mocking aids undetermined. The substitutes these suites already use are planted files and the code under test taking its paths as parameters. A planted fake `claude` script whose path the executor is given (or that is put first on `PATH`) fits that pattern. #420's `StubExecutor` is GraphScene's fake for the engine side, not for this one.
- **`devscene-flow-host` has no `asyncio` code today.** This branch adds the first. Its conventions say nothing on `asyncio`, so `.claude/context/docs-retrieval.md` → *"Async code is driven with `asyncio.run(…)` inside synchronous test functions"* is the precedent #420 followed.

What the planning pilot learned. The pilot measured these on Claude Code 2.1.325; the first three were re-measured on 2.1.332 on 2026-11-26, with `claude -p --output-format stream-json --verbose --model haiku`:

- `--agent <plugin>:<agent>` with `--plugin-dir` launches the agent. **`--json-schema` is still not applied under `--agent` on 2.1.332.** A plain session given `--json-schema` gets a `StructuredOutput` tool in its `init` tools, and its `result` event carries `structured_output`. A `--plugin-dir <main checkout>/plugin --agent devscene:prompt-injection-reviewer` session given its own `plugin/schemas/prompt-injection-reviewer.return.json` as `--json-schema` got no `StructuredOutput` tool, and its `result` event had no `structured_output` key, although its `result` text was a schema-valid `json` block. So the return is still read from the final `json` block.
- **`Glob`/`Grep` are still withheld from sessions holding `Bash` on 2.1.332.** The `init` tools of `--agent devscene:task-plan-writer` were `Read, Write, Edit, Bash`, and those of `--agent devscene:architecture-reviewer` were `Read, Bash, Write`, the same as on 2.1.325. `devscene:prompt-injection-reviewer`, which has no `Bash`, kept `Read, Grep, Glob`. The `init` tools check must keep allowing that omission.
- **The `result` event still carries the usage fields on 2.1.332:** `total_cost_usd`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens` and `modelUsage`, under `--agent` too. These are what a usage sink reads.
- The return read from the agent's final `json` block and validated against its schema.
- The pilot's infra/agent/undelivered classification and its stall timeout.
- A `PASS` `findings_file` came back relative, while `FAIL` ones were absolute.
- Per-session usage (cost, cache tokens) for the observations and for the prompt-cache check in #376. This now goes to the usage sink.

- **Matching usage to a launch row is open.** The engine writes one `Launch(seq, node, agent, attempt, max_attempts, result)` row per launched session to the host's `LaunchSink`, after the run returns. The executor is handed only the `Dispatch` (no `seq`, no attempt), so its usage sink cannot key a session by `seq`. Within one set a node runs once at a time, so matching on the node is possible, but planning decides how. `Launch` also has no duration, which the pilot's observation row has, so timing comes from the executor's side too.

## Depends on

#420
