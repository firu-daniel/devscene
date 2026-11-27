### 1. Node output reaches the run log only when a node session ends

**File:** `devscene-flow-host/src/devscene_flow_host/host/session_process.py` (`run_session`) — `chunks.append(chunk)`. The change also touches:
- `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (`ClaudeExecutor.run`) — `session = await run_session(`
- `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py` (`NodeSessions._record_usage`, `_format`) — `(self._directory / f"{seq}-{usage.node}{RUN_STREAM_SUFFIX}").write_bytes(data)`
- `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` — `sessions = NodeSessions(`
- `docs/watcher.md` → **The node stall rule.** and **Where node streams land.**
**Class:** Wrong behaviour
**Failure:** If the watcher's stall watchdog polls a run while a planning set's node sessions are working, then neither `<branch>.log` nor `<branch>.stream.jsonl` has grown since the set began. `autonomous-watcher.sh` judges liveness as the newest mtime of those two files, and `docs/watcher.md` → **The node stall rule.** states *"sees no node traffic until then"*. So the run reads as silent, and past `STALL_KILL_SECS` (2700) only the busy-CPU guard keeps it from being killed. The retired pilot's run log grew as each node wrote.

**Problem.** The retired pilot's `pnl_launch` (`cli/templates/scripts/lib/planning-node-lib.sh`, read at `613de204^`) piped each session's stdout through `tee "$stream" | "$PD_FORMATTER" >>"$log_path"`. The node's `<seq>-<node>.stream.jsonl` and the formatted run log therefore grew as the session wrote. Only the run stream and the manifest were written at reap. The Python path works differently:

- `run_session` collects every stdout chunk in memory and returns it when the process ends.
- `ClaudeExecutor.run` puts it in `SessionUsage.stream`.
- `NodeSessions._record_usage` writes the node file, the run stream, the manifest and the formatted log in one go.

GraphScene is not involved. The stream reaches the host only through the flow host's own executor and session process.

**Fix.** Stream stdout to the host as it is read. Write each node's stream file and the formatted log live. Keep the run stream (`${log%.log}.stream.jsonl`), the manifest and the stderr tail at session end, as now. The user allowed this.

- [ ] **`host/session_process.py` → `run_session`.** Add an optional keyword parameter `on_stdout: Callable[[bytes], None] | None = None`. In the read loop, call `on_stdout(chunk)` for every non-empty chunk, before `chunks.append(chunk)`. An exception from it propagates, so the existing `finally` kills the group. The returned `SessionRun` is unchanged. In the module docstring:
  - Add the rule: each stdout chunk is handed to `on_stdout` as it is read.
  - Reword *"Writing the stream anywhere"* under *"Deliberately not covered"*: the caller writes it, through `on_stdout` live and `SessionUsage.stream` at the end.
- [ ] **`host/claude_executor.py`.** Add two protocols beside `UsageSink`:

  ```python
  class LiveStream(Protocol):
      """One session's stdout as it is read; `close` is called exactly once, on every path out."""

      def write(self, chunk: bytes) -> None: ...

      def close(self) -> None: ...


  class StreamSink(Protocol):
      """Opens one `LiveStream` per session launched."""

      def open(self, node: str, agent: str) -> LiveStream: ...
  ```

  Add the constructor keyword `stream_sink: StreamSink | None = None`. In `run`, after the agent prompt is built and before `run_session`, do `live = self._stream_sink.open(dispatch.node, dispatch.agent)` when a sink is set. Pass `on_stdout=live.write` to `run_session`, and call `live.close()` in a `finally` around `run_session`, so it also runs on cancellation, including GraphScene's total-run timeout, and on a launch error. `close` runs before `usage_sink.record`. Update the module docstring's rule and *"Deliberately not covered"* to match.
- [ ] **`host/node_sessions.py` → `NodeSessions` implements `StreamSink`.**
  - `open(node, agent)` takes the next `seq`, which moves `seq` allocation from `_record_usage` to `open`. It stores it as `self._live[node] = seq`, which overwrites any stale entry left by a cancelled run (a node runs once at a time within a set). It creates `<planning dir>/<seq>-<node>.stream.jsonl` empty and returns a `LiveStream`.
  - The `LiveStream`'s `write(chunk)` appends the raw bytes to that node file at once, as `tee` did. It also keeps a per-session buffer of the bytes after the last `\n`, and passes only **complete lines** to the formatter (below).
  - `close()` passes any non-empty buffered remainder to the formatter with `\n` appended.
  - `_record_usage(usage)` pops `self._live.get(usage.node)`.
    - When a live seq is present, it uses that seq and skips writing the node file and formatting, because both already happened live. It still appends `usage.stream` to the run stream, writes the manifest line, appends a non-empty `stderr_tail` to the log and narrates `WITHHELD_LINE`, exactly as now.
    - When none is present, it allocates a seq and writes everything as today. That covers a usage recorded with no live stream opened, which the existing `test_node_sessions.py` cases rely on.
- [ ] **No partial lines in the run log.** Use **one formatter process per `NodeSessions`**, so a single writer produces every formatted line.
  - Start it lazily, on the first complete line: `subprocess.Popen([formatter], stdin=subprocess.PIPE, stdout=<the log opened in append-binary mode>)`.
  - Write each complete line to its stdin in a single `write` followed by `flush`, from whichever session's `write` produced it. Every caller runs on the event loop's thread, so whole lines from concurrent nodes are serialized and never split.
  - `autonomous-format-stream.sh` is a per-line `jq -Rr --unbuffered` filter that holds no state across lines, and a non-JSON line is a no-op, so interleaving whole lines from different nodes is safe.
  - Narrate a formatter that cannot be started with the existing literal `the formatter '<formatter>' could not run: <error>`, once. After that, live formatting is skipped for the drive, and the node files are still written.
  - When the formatter exits early, swallow the `BrokenPipeError` / `OSError` from writing to it and stop formatting for the drive. Its exit status stays ignored, as now. The tests' default formatter, `true`, exits at once, so this path must not raise or narrate.
  - Add `NodeSessions.close()`: close the formatter's stdin and wait for it to exit, so every formatted line is in the log before the driver returns. In `host/planning_run.py`, call `sessions.close()` in a `finally` around the `start_run` / `continue_run` call, and pass `stream_sink=sessions` to `ClaudeExecutor(...)`.
- [ ] **Tests.**
  - `devscene-flow-host/tests/fake_claude.py`: add a step `{"wait_for": <path>}`. It polls until that path exists, checking every 0.01 s, and exits 1 if the path has not appeared after 60 s. Document it in the module docstring's scenario list.
  - `devscene-flow-host/tests/test_node_sessions.py`: add a case that sees output in the log **before the fake session ends**. Build a `ClaudeExecutor` over `fake_claude.plant`, with `usage_sink=sessions` and `stream_sink=sessions`, and a `NodeSessions` with `formatter="cat"`. Copy the executor construction from `tests/test_claude_executor.py`'s helper. The scenario has three steps: a stdout `system` / `init` event line, `{"wait_for": "<tmp_path>/release"}`, then a stdout `result` event line. Inside `asyncio.run`, start `executor.run(dispatch)` as a task, then:
    - Poll `run.log` with `await asyncio.sleep(0.01)` until it contains the init line, failing after a bounded number of polls.
    - Assert that the task is not done, and that neither `run.log` nor `1-<node>.stream.jsonl` holds the result line yet.
    - Assert that the node file already holds the init line.
    - Create `release`, await the task, and assert that both lines are in `run.log` and in `run.stream.jsonl`.

    The poll bound is a guard, not a duration assertion.
  - Add a second case in the same file that interleaves partial chunks from two live streams without a subprocess fake. Call `a.write(b'{"a":')`, `b.write(b'{"b":')`, `a.write(b'1}\n')`, `b.write(b'2}\n')`, then close both and `sessions.close()`. With the `cat` formatter, `run.log` must be exactly the lines `{"a":1}` then `{"b":2}`, in the order the lines completed. The node files must hold their own bytes.
  - Keep the existing `test_node_sessions.py` cases. They exercise the record-only path.
- [ ] **`docs/watcher.md`.**
  - **The node stall rule.** Replace *"While a set runs, a node's lines reach the run log and the run stream only when its session ends (**Where node streams land.**, below), so the watchdog, which judges those two files, sees no node traffic until then; its busy-but-quiet CPU guard is what defers its kill over a set whose sessions are working."* The replacement should say that a node's formatted lines reach the run log as its session writes them, so the watchdog, which takes the newer of the log's and the run stream's mtimes, sees a working set's traffic. Only events the formatter keeps move the log; thinking blocks and tool results do not, as on the orchestrated path.
  - **Where node streams land.** State that each node's raw events go to `<seq>-<node>.stream.jsonl` as the session writes them, and that its formatted lines go to `<branch>.log` at the same time, whole lines only, through one formatter. The run's `<branch>.stream.jsonl` and the `node-sessions.jsonl` manifest are still written when the node's session ends.
  - **Node sessions, and the run's time.** *"each node's stream joins the run's `<branch>.stream.jsonl` when its session ends"* stays true, so leave it.
  - `docs/flow-graph-walker.md` → **Node streams reach the run stream one node late.** stays true for the run stream, so leave it.
- The edited test files are the unit's own. Run them under that rule.
