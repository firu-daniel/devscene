### 1. `run_session` kills the group only while the leader runs, so a member that outlives a normal exit is left behind, and one holding stderr stops the run from ever returning

**File:** `devscene-flow-host/src/devscene_flow_host/host/session_process.py` (`run_session`): "if process.returncode is None:"
**Class:** Wrong behaviour
**Failure:** If `ClaudeExecutor.run` launches a session whose process starts a child in its group and then exits, `run_session` returns with that child still running when the child has detached its stdio, and never returns at all when the child holds stderr. In the second case the inactivity limit never applies, and GraphScene's `run_timeout_seconds` defaults to `None`.

**The problem.** The `finally` block kills the group only `if process.returncode is None`, that is, only while the leader is still running. After stdout reaches EOF the function awaits `process.wait()` and then `await stderr_task`, and neither wait has a bound. Two paths follow:

- **A member left behind on a normal exit.** The leader exits, stdout reaches EOF, `process.wait()` returns, and the `finally` skips the kill because `returncode` is set. Any member of the session's process group that no longer holds the stdout pipe (an MCP server or a background command that redirected its stdio) is still running when `run_session` returns. This contradicts the module docstring's opening line, *"Runs one session process to its end, leaving no process of its group behind"*, Task 3's goal, *"with nothing left behind"*, and the story index's first `Top risks:` entry, *"kills the whole group on stall, on cancellation and on every other exit path"*. The README's `## The executor` → **Killing the session.** also says *"so no process of the group is left behind"*.
- **A run that never returns.** If a member still holds the stderr pipe after the leader exits, `_drain_tail` never sees EOF, and `await stderr_task` waits forever. No inactivity limit covers that wait. If the engine then cancels the run, the `finally` still skips the kill because the leader's `returncode` is set, so that member survives the cancellation too.

**Confirmed by a probe, on a fake session only.** The command was `bash scripts/python-service.sh --package devscene-flow-host probe harness-runs/scratch/branch_review_session_process_probe.py`. The probe called `run_session` on a `sys.executable -c …` leader that starts one `time.sleep(30)` child and exits 0. It printed:

- `detached: returncode=0 stalled=False child_alive_after_return=True` for a child with stdin, stdout and stderr all on `DEVNULL`;
- `stderr_holder: still waiting after 12.0s with inactivity limit 2.0s (outer probe timeout fired)` for a child with stdout on `DEVNULL` and stderr inherited.

The probe did not test whether a real `claude` session's MCP servers or background tools take either shape. The defect is that `run_session` breaks its own documented contract, which the probe shows for any session.

**Fix.** Kill the group on every path out, whatever the leader's state. Bound the wait for the leader after stdout EOF by the inactivity limit, and bound the stderr drain after the kill.

1. In `devscene-flow-host/src/devscene_flow_host/host/session_process.py`, add `import contextlib`, and add this beside `STDERR_TAIL_BYTES`:

   ```python
   STDERR_DRAIN_SECONDS: Final = 5.0
   ```

2. Replace everything in `run_session` from `stderr_task = asyncio.create_task(_drain_tail(process.stderr))` to the closing `)` of the final `return SessionRun(...)` with:

   ```python
       stderr_task = asyncio.create_task(_drain_tail(process.stderr))
       chunks: list[bytes] = []
       stalled = False
       tail = b""
       try:
           while True:
               try:
                   chunk = await asyncio.wait_for(
                       stdout.read(READ_CHUNK_BYTES), inactivity_limit_seconds
                   )
               except TimeoutError:
                   stalled = True
                   break
               if not chunk:
                   break
               chunks.append(chunk)
           if not stalled:
               try:
                   await asyncio.wait_for(process.wait(), inactivity_limit_seconds)
               except TimeoutError:
                   stalled = True
       finally:
           # The leader may already have exited while members of its group run on, so the group
           # is killed on every path out, never only while the leader runs.
           await _kill_group(process, kill_grace_seconds)
           tail = await _stderr_tail(stderr_task)
       return SessionRun(
           stdout=b"".join(chunks).decode("utf-8", errors="replace"),
           stderr_tail=tail.decode("utf-8", errors="replace"),
           returncode=process.returncode,
           stalled=stalled,
           launch_error=None,
       )
   ```

   Then add this helper after `_drain_tail`:

   ```python
   async def _stderr_tail(task: asyncio.Task[bytes]) -> bytes:
       done, _ = await asyncio.wait({task}, timeout=STDERR_DRAIN_SECONDS)
       if task in done:
           return task.result()
       task.cancel()
       with contextlib.suppress(asyncio.CancelledError):
           await task
       return b""
   ```

   `_kill_group` already works once the leader has been reaped: `process.wait()` returns at once, `os.killpg` still reaches the group's remaining members, and a `ProcessLookupError` from an empty group is ignored.

3. Update the module docstring's rule bullets to match:
   - *"At stdout EOF the process's exit and the stderr task are awaited."* becomes *"At stdout EOF the process's exit is awaited, bounded by the inactivity limit; a leader still running past it is a stall."*
   - *"On every path out while the process is still running — a stall, …"* becomes *"On every path out — a normal exit, a stall, `asyncio.CancelledError`, any unexpected exception — the group is killed, whether or not the leader has exited, and the stderr drain is then awaited for at most `STDERR_DRAIN_SECONDS`."*

4. In `devscene-flow-host/README.md` → `## The executor` → **Killing the session.**, replace *"On a stall, on `asyncio.CancelledError` and on any unexpected exception, while the process is still running, it sends"* with *"On every path out — a normal exit, a stall, `asyncio.CancelledError` and any unexpected exception, whether or not the session's own process has exited — it sends"*.

5. Tests. In `devscene-flow-host/tests/fake_claude.py`, add an optional scenario key `child_stdio` and document it in the module docstring beside `child_pid_file`. It takes one of three values:
   - `"inherit"`, the default and today's behaviour;
   - `"detached"`, the child started with `stdin`, `stdout` and `stderr` all `subprocess.DEVNULL`;
   - `"stderr"`, the child started with `stdin` and `stdout` `subprocess.DEVNULL` and stderr inherited.

   In `devscene-flow-host/tests/test_session_process.py`, add two cases. Each plants `child_pid_file` and `pid_file` with steps `[{"stdout": "done"}]` and exit `0`:
   - `test_a_group_member_left_by_a_normal_exit_is_killed`: `child_stdio` `"detached"`. Assert `run.returncode == 0`, `run.stalled is False`, and `_assert_gone` on the child's pid.
   - `test_a_member_holding_stderr_does_not_hold_the_run`: `child_stdio` `"stderr"`, `limit=10.0`. Call `run_session` inside `asyncio.wait_for(…, _BOUNDED_WAIT_SECONDS)` so a regression fails instead of hanging the suite. Assert `run.returncode == 0`, `run.stdout == "done\n"`, and `_assert_gone` on the child's pid.

   Then widen the file header's rule sentence from *"on a stall or a cancellation leaves no process of the session's group alive"* to *"on a normal exit, a stall or a cancellation leaves no process of the session's group alive"*.

   `tests/test_session_process.py` is the only test file this fix edits, so it is the only test file the fix runs, through `bash scripts/python-service.sh --package devscene-flow-host test tests/test_session_process.py`.
