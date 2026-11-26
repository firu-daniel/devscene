### 1. `_signal_group` lets a `PermissionError` from `os.killpg` escape after the leader has exited

**Site:** `devscene-flow-host/src/devscene_flow_host/host/session_process.py` → `_signal_group` (`os.killpg(pid, signal_number)` with only `except ProcessLookupError:`), reached from `_kill_group` (`_signal_group(process.pid, signal.SIGKILL)`), which `run_session`'s `finally:` calls on every path out. Line hints: around 137–151.

**Failing test:** `devscene-flow-host/tests/test_session_process.py` — reported by the log as `13j devscene-flow-host tests` (`1 failed, 434 passed`). The log's excerpt cuts off the test's name; the traceback's outer frame (`asyncio/tasks.py:488: in wait_for`, directly under `asyncio.run`) matches only `test_a_member_holding_stderr_does_not_hold_the_run`, the one case in the suite that wraps `run_session` in `asyncio.wait_for` (no other test or source module calls `run_session` under `asyncio.wait_for`).

**Class:** Wrong behaviour

**Failure:** If the `devscene-flow-host` pytest suite (gate 13j) runs `test_a_member_holding_stderr_does_not_hold_the_run`, then `run_session` raises out of its `finally:` block with `PermissionError: [Errno 1] Operation not permitted` from `os.killpg` on the `SIGKILL` leg instead of returning a `SessionRun`.

**The failure, quoted from the log:**

```
  FAIL  13j devscene-flow-host tests (exit 1, 15 s)
        src/devscene_flow_host/host/session_process.py:109: in run_session
            await _kill_group(process, kill_grace_seconds)
        src/devscene_flow_host/host/session_process.py:143: in _kill_group
            _signal_group(process.pid, signal.SIGKILL)
        pid = 11755, signal_number = <Signals.SIGKILL: 9>
        >           os.killpg(pid, signal_number)
        E           PermissionError: [Errno 1] Operation not permitted
        src/devscene_flow_host/host/session_process.py:149: PermissionError
        ======================== 1 failed, 434 passed in 14.54s ========================
```

**Class against earlier rounds:** first round — no earlier log; recorded as new this round.

**Diagnosis.**

- The scenario (`_group_member_scenario(tmp_path, "stderr")`) has the leader print `done` and exit 0 while a child it spawned in the same process group sleeps holding stderr. `run_session` reads stdout to EOF, awaits the leader's exit (reaping it), then `_kill_group` runs from the `finally:`.
- `_kill_group` sends `SIGTERM` to the group (line 138). That call **succeeded** — the traceback is at line 143, past it — so the group existed and was signalable by this process a moment earlier. The `SIGTERM` kills the child; `process.wait()` returns at once (the leader is already reaped); then `SIGKILL` to the same pgid raises `EPERM`.
- On Darwin, `killpg` on a process group whose only remaining members are zombies returns `EPERM`, not `ESRCH`. The child, orphaned when the leader exited and reparented to `launchd`, is a zombie between its `SIGTERM` death and `launchd` reaping it. Whether `SIGKILL` lands in that window is a race: when the child is already reaped, `killpg` gives `ESRCH` (`ProcessLookupError`, handled); when it is a zombie, `EPERM` (`PermissionError`, unhandled). That is why the stall, cancellation and detached-member cases, which run the same `_kill_group` path in the same run, passed.
- **Why this is not treated as a sandbox refusal.** The error carries the `Operation not permitted` signature, but it names no path and no host: it is a signal to the session's own process group, which this process created (`start_new_session=True`) and had just signalled successfully with `SIGTERM` in the same `_kill_group` call. A sandbox restriction on signalling would refuse consistently, not between two calls on the same group, and not only in one of the four cases that take this path. The fix below swallows `PermissionError` **only after the leader has exited and been reaped**, so a real refusal while the leader still runs still raises, and the test's `_assert_gone(child_pid)` check still fails if any member survives.
- The module docstring's rule (*"a `ProcessLookupError` means the group is gone"*) does not cover Darwin's zombie-only group, so the code follows the documented rule and still fails on the platform the gate ran on.

**Fix.**

- [ ] In `_signal_group`, take whether the leader has already exited (for example a keyword parameter `leader_exited: bool`, passed as `process.returncode is not None` at both call sites in `_kill_group`). Keep `except ProcessLookupError: pass`, and add `except PermissionError:` that returns silently when `leader_exited` is true and re-raises otherwise. Apply it to both the `SIGTERM` and the `SIGKILL` calls: the `SIGTERM` leg can hit the same zombie-only group on a normal exit whose remaining member has already died.
- [ ] Update the module docstring's *"The rule:"* bullet on killing the group to state the new case: after the leader has exited, a `PermissionError` from `killpg` means only zombies remain (Darwin answers `EPERM` for a zombie-only group), and is treated as the group being gone; before that, it propagates.
- [ ] Do not edit, skip or loosen `test_a_member_holding_stderr_does_not_hold_the_run` or its `_assert_gone` check: it is the proof that no live member survives.
