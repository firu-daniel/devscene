"""The rule this file exists to enforce: `run_session` returns every byte of stdout and the tail of
stderr with the exit status, reads a line longer than 64 KiB whole, treats only a stdout silent
past the inactivity limit as a stall, turns a launch `OSError` into `launch_error`, and on a stall
or a cancellation leaves no process of the session's group alive — the cancellation re-raised.

Every session is `fake_claude`, its scenario and pid files under `tmp_path`, and every expected
value is a literal written from the task plan's rules, never taken from `run_session`'s output.
No case asserts a duration: the only clocks are the bounded waits for a pid file to appear and
for a pid to disappear.

Deliberately not covered:
- The `SIGKILL` after an ignored `SIGTERM`: no scenario step ignores a signal, and a stall case
  already proves the group is gone.
"""

import asyncio
import errno
import os
import time
from collections.abc import Mapping
from pathlib import Path

import pytest

from devscene_flow_host.host.session_process import SessionRun, run_session
from fake_claude import plant

_BOUNDED_WAIT_SECONDS = 20.0
_POLL_SECONDS = 0.05


def _run(
    argv: tuple[str, ...], cwd: Path, *, limit: float = 10.0, grace: float = 2.0
) -> SessionRun:
    return asyncio.run(
        run_session(
            argv, cwd=cwd, env=None, inactivity_limit_seconds=limit, kill_grace_seconds=grace
        )
    )


def _assert_gone(pid: int) -> None:
    deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(_POLL_SECONDS)
    raise AssertionError(f"process {pid} outlived run_session")


def _scenario_with_pids(tmp_path: Path, steps: list[Mapping[str, object]]) -> dict[str, object]:
    return {
        "pid_file": str(tmp_path / "fake.pid"),
        "child_pid_file": str(tmp_path / "child.pid"),
        "steps": steps,
    }


def _pid(path: Path) -> int:
    return int(path.read_text(encoding="utf-8"))


def test_all_stdout_is_captured_with_a_line_over_64_kib_and_the_exit_status(
    tmp_path: Path,
) -> None:
    long_line = "x" * 70000
    argv = plant(
        tmp_path,
        {"steps": [{"stdout": "first"}, {"stdout": long_line}, {"stdout": "last"}], "exit": 3},
    )

    run = _run(argv, tmp_path)

    assert run == SessionRun(
        stdout="first\n" + "x" * 70000 + "\nlast\n",
        stderr_tail="",
        returncode=3,
        stalled=False,
        launch_error=None,
    )


def test_only_the_last_4096_bytes_of_stderr_are_kept(tmp_path: Path) -> None:
    argv = plant(tmp_path, {"steps": [{"stderr": "a" * 1000 + "b" * 4000}, {"stdout": "out"}]})

    run = _run(argv, tmp_path)

    assert run.stderr_tail == "a" * 95 + "b" * 4000 + "\n"
    assert run.stdout == "out\n"
    assert run.returncode == 0


def test_a_silent_stdout_is_a_stall_and_the_whole_group_is_killed(tmp_path: Path) -> None:
    argv = plant(tmp_path, _scenario_with_pids(tmp_path, [{"stdout": "only"}, {"sleep": 600}]))

    run = _run(argv, tmp_path, limit=0.5)

    assert run.stalled is True
    assert run.stdout == "only\n"
    assert run.launch_error is None
    _assert_gone(_pid(tmp_path / "fake.pid"))
    _assert_gone(_pid(tmp_path / "child.pid"))


def test_a_stream_active_past_the_limit_is_not_a_stall(tmp_path: Path) -> None:
    steps: list[Mapping[str, object]] = []
    for index in range(15):
        steps += [{"stdout": f"line {index}"}, {"sleep": 0.1}]
    argv = plant(tmp_path, {"steps": steps})

    run = _run(argv, tmp_path, limit=1.0)

    assert run.stalled is False
    assert run.stdout == "".join(f"line {index}\n" for index in range(15))
    assert run.returncode == 0


def test_a_cancelled_run_kills_the_group_and_re_raises(tmp_path: Path) -> None:
    argv = plant(tmp_path, _scenario_with_pids(tmp_path, [{"sleep": 600}]))
    pid_file = tmp_path / "fake.pid"

    async def cancel_once_started() -> None:
        task = asyncio.create_task(
            run_session(
                argv,
                cwd=tmp_path,
                env=None,
                inactivity_limit_seconds=600.0,
                kill_grace_seconds=2.0,
            )
        )
        deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
        while not pid_file.exists():
            assert time.monotonic() < deadline, "the fake never wrote its pid file"
            await asyncio.sleep(_POLL_SECONDS)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(cancel_once_started())

    _assert_gone(_pid(pid_file))
    _assert_gone(_pid(tmp_path / "child.pid"))


def test_a_command_that_does_not_exist_is_a_launch_error(tmp_path: Path) -> None:
    missing = tmp_path / "no-such-claude"

    run = _run((str(missing), "-p"), tmp_path)

    assert run == SessionRun(
        stdout="",
        stderr_tail="",
        returncode=None,
        stalled=False,
        launch_error=f"cannot launch {missing}: {os.strerror(errno.ENOENT)}",
    )
