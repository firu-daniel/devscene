### Task 3 — Supervise one session process with inactivity detection and group kill in `host/session_process.py`

**Goal:** Run one session process to its end on `asyncio`, with nothing left behind. Launch it with `asyncio.create_subprocess_exec` in its own process group. Collect its stdout in full and the tail of its stderr. Treat a stdout that stays silent past the inactivity limit as a stall and kill the group. On `asyncio.CancelledError`, or on any other exit path, kill the group before the exception leaves. This is the first `asyncio` code in `devscene-flow-host`.

**Where this layer stops.** This module knows nothing about `claude`, its flags or its events. It runs the argument vector it is given, under the working directory and environment it is given, and returns raw text and flags. **Task 2**'s `judge_session` judges the text. **Task 4** builds the argument vector, owns the inactivity limit's value (`NODE_INACTIVITY_LIMIT_SECONDS`) and the kill grace's value (`KILL_GRACE_SECONDS`), and turns a stall or a launch error into a `Failed`. This module has no default for either value.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/session_process.py` (new)
- `devscene-flow-host/tests/fake_claude.py` (new), a test-support module that is also run as a script
- `devscene-flow-host/tests/test_session_process.py` (new)

**Work:**

- [ ] `session_process.py` defines `@dataclass(frozen=True) class SessionRun` with these fields:
  - `stdout: str`, every byte, decoded as UTF-8 with `errors="replace"`;
  - `stderr_tail: str`, the last 4096 bytes, decoded the same way;
  - `returncode: int | None`;
  - `stalled: bool`;
  - `launch_error: str | None`.

  It also defines `async def run_session(argv: Sequence[str], *, cwd: Path, env: Mapping[str, str] | None, inactivity_limit_seconds: float, kill_grace_seconds: float) -> SessionRun`. The read chunk size (65536) and the stderr tail size (4096) are module-level `Final` constants. The module docstring opens with *"The rule:"*, states every bullet below, and lists under *"Deliberately not covered"*:
  - a platform without `os.killpg`: POSIX only, as GraphScene's `FileStateStore` is POSIX-only through `fcntl`;
  - writing the stream anywhere: the run loop's (#484);
  - what a stall or an exit status means for the node: `host/claude_executor.py`.
- [ ] Launch and read. Launch with `asyncio.create_subprocess_exec(*argv, cwd=cwd, env=None if env is None else dict(env), stdin=DEVNULL, stdout=PIPE, stderr=PIPE, start_new_session=True)`. An `OSError` raised by the launch is anticipated: return `SessionRun(stdout="", stderr_tail="", returncode=None, stalled=False, launch_error=f"cannot launch {argv[0]}: {error.strerror}")`.
  - Read stdout in **chunks** with `read(65536)`, never with `readline`, so a `result` line longer than the reader's default 64 KiB limit is neither refused nor cut. Each read is under `asyncio.wait_for(…, inactivity_limit_seconds)`, so any chunk resets the clock.
  - Drain stderr concurrently in its own task, keeping the tail, so a chatty stderr can never block the child.
  - At stdout EOF, await the process's exit and the stderr task.
  - A read that times out is a stall: kill the group (next bullet) and return with `stalled=True` and the stdout read so far.
- [ ] Killing the group: send `SIGTERM` to the group with `os.killpg(process.pid, …)`, wait up to `kill_grace_seconds` for exit, then send `SIGKILL` to the group and await exit. A `ProcessLookupError` means the group is already gone and is ignored. Use a `try`/`finally` so the group is killed and the process awaited on **every** path out of `run_session` while it is still running: a stall, `asyncio.CancelledError` and any unexpected exception. `CancelledError` is always re-raised after the kill and never turned into a `SessionRun` (`graphscene/src/graphscene/model/execution.py` → *"On `asyncio.CancelledError` it releases what it holds and re-raises"*). The function writes no file, so repeating a run for the same argument vector repeats nothing.
- [ ] `tests/fake_claude.py` is a support module with a docstring stating its rule: it stands in for a `claude` session, driven only by a scenario file, and writes only to paths the scenario names. It runs as `python fake_claude.py <scenario.json> [args…]`. **Task 4's test uses it unchanged; this task owns it.** The scenario is a JSON object:
  - `argv_file` (optional): write the JSON list of the args after the scenario path there;
  - `pid_file` (optional): write the process's own pid there;
  - `child_pid_file` (optional): spawn a child `sys.executable -c "import time; time.sleep(600)"` in the same process group and write its pid there;
  - `steps`: a list of `{"stdout": <text>}` (written with a newline and flushed), `{"stderr": <text>}` (written with a newline and flushed) or `{"sleep": <seconds>}`;
  - `exit` (optional, default `0`): the exit status.

  It also exposes `plant(directory: Path, scenario: Mapping[str, object]) -> tuple[str, ...]`, which writes the scenario under `directory` and returns the command prefix `(sys.executable, <this file's path>, <scenario path>)`.
- [ ] `tests/test_session_process.py` has a docstring opening *"The rule this file exists to enforce"*. Each case runs `run_session` through `asyncio.run(…)` inside a synchronous test function, with every scenario and pid file under `tmp_path`. Include:
  - all stdout captured, including one line over 64 KiB, with `returncode` equal to the scenario's `exit`;
  - the stderr tail captured;
  - a stall: one line, then `sleep 600`, with `inactivity_limit_seconds=0.5`. The result has `stalled=True` and that line in `stdout`, and both the fake's pid and its child's pid are gone, polled with `os.kill(pid, 0)` until it raises `ProcessLookupError` within a bounded wait;
  - an active stream that is not a stall: lines every 0.1 s for 1.5 s under a 1.0 s limit;
  - cancellation: the `run_session` task is cancelled once the pid file exists, `CancelledError` reaches the test, and the fake and its child are both gone;
  - a launch error for a command path that does not exist, asserting the exact `launch_error` literal, which carries the platform's `strerror`.

  No case asserts a duration.

**Verification:**

- `tests/test_session_process.py` passes. The stall and cancellation cases prove that no process of the session's group outlives `run_session`, which is the story index's first `Top risks:` entry.
- `bash scripts/typecheck.sh` reports nothing in the three targets. `session_process.py` imports only the standard library.
