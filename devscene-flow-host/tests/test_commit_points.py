"""The rule this file exists to enforce: `commit_artifact` runs the commit wrapper as one fixed
argument vector under the worktree, maps exit `0` to `True`, exit `3` to `False` and any other
exit to a `CommitPointError` naming the last stdout `error: ` line's cause or `no message`, and
leaves no child behind when cancelled; `flip_ledger_entry` flips only an open entry's first line,
leaves a resolved one byte-identical, and refuses an unknown entry, a missing ledger and a missing
line with their exact messages.

Every wrapper is a fake planted under `tmp_path` that logs its arguments, prints a scripted
stdout and exits with a scripted status; every ledger is planted under `tmp_path`. Every expected
value is a literal written from the task plan's rules, never taken from the code under test. No
case asserts a duration: the only clocks are the bounded waits for a pid file to appear and for a
pid to disappear.

Deliberately not covered:
- The real `commit-on-branch.sh`: its subjects, path sets, re-sync and push are its own suites'.
"""

import asyncio
import os
import stat
import time
from pathlib import Path

import pytest

from devscene_flow_host.host.commit_points import (
    CommitPointError,
    commit_artifact,
    flip_ledger_entry,
)
from devscene_flow_host.records.errors import RecordError

_BOUNDED_WAIT_SECONDS = 20.0
_POLL_SECONDS = 0.05
_STATE_DIR = "devscene"
_BRANCH = "feat_x"
_LEDGER_REL = "devscene/flow_progress/feat_x_progress.md"


def _plant_wrapper(tmp_path: Path, *, stdout: str = "", status: int = 0, body: str = "") -> Path:
    wrapper = tmp_path / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "bin" / "stdout.txt").write_text(stdout, encoding="utf-8")
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
        "(IFS=$'\\t'; printf '%s\\n' \"$*\") >>\"$here/calls.log\"\n"
        'pwd -P >>"$here/cwd.log"\n'
        f"{body}"
        'cat "$here/stdout.txt"\n'
        f"exit {status}\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


def _worktree(tmp_path: Path) -> Path:
    worktree = tmp_path / "worktree"
    worktree.mkdir(exist_ok=True)
    return worktree


def _calls(wrapper: Path) -> list[str]:
    return (wrapper.parent / "calls.log").read_text(encoding="utf-8").splitlines()


def _commit(
    wrapper: Path,
    worktree: Path,
    kind: str,
    *,
    round_number: int | None = None,
    entry: str | None = None,
) -> bool:
    return asyncio.run(
        commit_artifact(wrapper, worktree, kind, round_number=round_number, entry=entry)
    )


def test_a_plan_round_call_passes_its_round(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path)
    worktree = _worktree(tmp_path)
    _commit(wrapper, worktree, "plan-round", round_number=2)
    assert _calls(wrapper) == [f"--repo\t{worktree}\t--artifact\tplan-round\t--round\t2\t--push"]
    assert (wrapper.parent / "cwd.log").read_text(encoding="utf-8") == f"{worktree.resolve()}\n"


def test_a_ledger_flip_call_passes_its_entry(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path)
    worktree = _worktree(tmp_path)
    _commit(wrapper, worktree, "ledger-flip", entry="P1")
    assert _calls(wrapper) == [f"--repo\t{worktree}\t--artifact\tledger-flip\t--entry\tP1\t--push"]


def test_a_task_plan_call_passes_neither_round_nor_entry(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path)
    worktree = _worktree(tmp_path)
    _commit(wrapper, worktree, "task-plan")
    assert _calls(wrapper) == [f"--repo\t{worktree}\t--artifact\ttask-plan\t--push"]


def test_exit_0_is_committed(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path, stdout="commit_sha: abc\n", status=0)
    assert _commit(wrapper, _worktree(tmp_path), "task-plan") is True


def test_exit_3_is_nothing_to_commit(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path, stdout="error: nothing to commit\n", status=3)
    assert _commit(wrapper, _worktree(tmp_path), "task-plan") is False


def test_exit_1_raises_with_the_last_error_line(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(
        tmp_path, stdout="staged: x\nerror: earlier\nerror: refused\ndone\n", status=1
    )
    with pytest.raises(CommitPointError) as caught:
        _commit(wrapper, _worktree(tmp_path), "task-plan")
    assert str(caught.value) == "commit-on-branch.sh --artifact task-plan exited 1: refused"


def test_exit_2_without_an_error_line_raises_with_no_message(tmp_path: Path) -> None:
    wrapper = _plant_wrapper(tmp_path, stdout="something else\n", status=2)
    with pytest.raises(CommitPointError) as caught:
        _commit(wrapper, _worktree(tmp_path), "plan-round", round_number=1)
    assert str(caught.value) == "commit-on-branch.sh --artifact plan-round exited 2: no message"


def _wait_for_pid(pid_file: Path) -> int:
    deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
    while time.monotonic() < deadline:
        text = pid_file.read_text(encoding="utf-8") if pid_file.exists() else ""
        if text.endswith("\n"):
            return int(text)
        time.sleep(_POLL_SECONDS)
    raise AssertionError(f"{pid_file} never appeared")


def _assert_gone(pid: int) -> None:
    deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(_POLL_SECONDS)
    raise AssertionError(f"process {pid} outlived the cancelled commit_artifact")


def test_a_cancelled_call_leaves_no_child(tmp_path: Path) -> None:
    pid_file = tmp_path / "wrapper.pid"
    wrapper = _plant_wrapper(tmp_path, body=f"echo $$ >'{pid_file}'\nexec sleep 300\n")
    worktree = _worktree(tmp_path)

    async def scenario() -> int:
        task = asyncio.create_task(commit_artifact(wrapper, worktree, "task-plan"))
        pid = await asyncio.to_thread(_wait_for_pid, pid_file)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        return pid

    _assert_gone(asyncio.run(scenario()))


def _plant_ledger(tmp_path: Path, text: str) -> Path:
    ledger = tmp_path / _LEDGER_REL
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(text.encode("utf-8"))
    return ledger


def test_an_open_entry_is_flipped_with_the_rest_of_its_line_kept(tmp_path: Path) -> None:
    ledger = _plant_ledger(
        tmp_path,
        "# Progress\n\n- [x] P1. Story plan written\n- [ ] P2. Task plans — round 3\n"
        "- [ ] P3. Plan review\n- [ ] P2. a later duplicate\n",
    )
    assert flip_ledger_entry(tmp_path, _STATE_DIR, _BRANCH, "P2") is True
    assert ledger.read_bytes() == (
        b"# Progress\n\n- [x] P1. Story plan written\n- [x] P2. Task plans \xe2\x80\x94 round 3\n"
        b"- [ ] P3. Plan review\n- [ ] P2. a later duplicate\n"
    )
    assert stat.S_IMODE(ledger.stat().st_mode) == 0o644
    assert sorted(entry.name for entry in ledger.parent.iterdir()) == ["feat_x_progress.md"]


@pytest.mark.parametrize("mark", ["- [x] ", "- [-] "])
def test_a_resolved_entry_is_left_byte_identical(tmp_path: Path, mark: str) -> None:
    text = f"# Progress\n{mark}P1. done already\n- [ ] P1. a later open line\n"
    ledger = _plant_ledger(tmp_path, text)
    ledger.chmod(0o600)
    assert flip_ledger_entry(tmp_path, _STATE_DIR, _BRANCH, "P1") is False
    assert ledger.read_bytes() == text.encode("utf-8")
    assert stat.S_IMODE(ledger.stat().st_mode) == 0o600


def test_a_ledger_with_no_line_for_the_entry_is_refused(tmp_path: Path) -> None:
    _plant_ledger(tmp_path, "# Progress\n- [ ] P1. a\n- [ ] P10. not P1\n")
    with pytest.raises(RecordError) as caught:
        flip_ledger_entry(tmp_path, _STATE_DIR, _BRANCH, "P3")
    assert str(caught.value) == (
        "the ledger 'devscene/flow_progress/feat_x_progress.md' carries no P3 line"
    )


def test_a_missing_ledger_is_refused(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as caught:
        flip_ledger_entry(tmp_path, _STATE_DIR, _BRANCH, "P1")
    assert str(caught.value) == (
        "the ledger 'devscene/flow_progress/feat_x_progress.md' does not exist"
    )


def test_an_unknown_entry_is_refused(tmp_path: Path) -> None:
    _plant_ledger(tmp_path, "- [ ] P4. x\n")
    with pytest.raises(ValueError) as caught:
        flip_ledger_entry(tmp_path, _STATE_DIR, _BRANCH, "P4")
    assert str(caught.value) == "flip_ledger_entry takes P1, P2 or P3, not 'P4'"
