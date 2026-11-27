"""The rule this file exists to enforce: `Observations.add` refuses an unknown category and an
empty problem and flattens each text to one line; `Observations.flush` writes the blocks under a
`# Script-driven planning — <ts>` heading after the existing file, moving its closing
`# Task run (Phase D)` label to the end; it rewrites the worktree, the main checkout and the home
directory where a delimiter follows them and nowhere else; and it commits the file as the
`observations` artifact, or restores the previous file and logs, never raising, when a machine
path survives the rewrite or the wrapper fails.

Every wrapper is a fake planted under `tmp_path` that logs its argument vector; every worktree,
main checkout and home directory is a directory under `tmp_path`. Every expected value is a
literal written from the task plan's contract, never taken from the code under test.

Deliberately not covered:
- Which driver events become observations, and flushing on every exit: the driver's suites.
- The real `commit-on-branch.sh` and `commit_artifact`'s exit mapping:
  `tests/test_commit_points.py`.
"""

import asyncio
from datetime import UTC, datetime
from pathlib import Path

import pytest

from devscene_flow_host.host.observations import (
    Needle,
    Observations,
    machine_needles,
    rewrite_machine_paths,
)

_BRANCH = "feat_x"
_STATE_DIR = "state"
_REL = "state/improvement_observations/feat_x.md"
_NOW = datetime(2026, 11, 27, 10, 0, 0, tzinfo=UTC)
_HEADING = "# Script-driven planning — 2026-11-27T10:00:00Z\n\n"


def _plant_wrapper(tmp_path: Path, *, status: int = 0) -> Path:
    wrapper = tmp_path / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
        'printf \'%s\\n\' "$*" >>"$here/calls.log"\n'
        f"if [ {status} -ne 0 ]; then echo 'error: refused'; fi\n"
        f"exit {status}\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return wrapper


def _calls(wrapper: Path) -> list[str]:
    log = wrapper.parent / "calls.log"
    return log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _dirs(tmp_path: Path) -> tuple[Path, Path, Path]:
    worktree, main, home = tmp_path / "wt", tmp_path / "main", tmp_path / "home"
    for directory in (worktree, main, home):
        directory.mkdir()
    return worktree, main, home


def _flush(observations: Observations, tmp_path: Path, wrapper: Path, lines: list[str]) -> None:
    worktree, main, home = tmp_path / "wt", tmp_path / "main", tmp_path / "home"
    asyncio.run(
        observations.flush(
            repo_root=worktree,
            main_repo=main,
            state_dir=_STATE_DIR,
            branch=_BRANCH,
            wrapper=wrapper,
            home=str(home),
            now=_NOW,
            log=lines.append,
        )
    )


def test_an_unknown_category_is_refused() -> None:
    with pytest.raises(ValueError, match="^'idea' is not an observation category$"):
        Observations().add("idea", "p", "e", "c")


def test_an_empty_problem_is_refused() -> None:
    with pytest.raises(ValueError, match="^an observation needs a problem statement$"):
        Observations().add("convention", "", "e", "c")


def test_a_multi_line_problem_is_flattened(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    observations = Observations()
    observations.add("tooling-gap", "first\nsecond\r\nthird", "ev\nidence", "one\rtwo")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert (worktree / _REL).read_text(encoding="utf-8") == (
        _HEADING + "## first second  third\n"
        "- **category:** tooling-gap\n"
        "- **evidence:** ev idence\n"
        "- **cost this run:** one two\n"
        "\n"
        "# Task run (Phase D)\n"
    )


def test_a_flush_into_no_file_writes_and_commits_it(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    observations = Observations()
    observations.add("convention", "p", "e", "c")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert (worktree / _REL).read_bytes() == (
        b"# Script-driven planning \xe2\x80\x94 2026-11-27T10:00:00Z\n\n"
        b"## p\n- **category:** convention\n- **evidence:** e\n- **cost this run:** c\n\n"
        b"# Task run (Phase D)\n"
    )
    assert _calls(wrapper) == [f"--repo {worktree} --artifact observations --push"]
    assert lines == []


def test_a_flush_with_no_blocks_does_nothing(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    lines: list[str] = []
    _flush(Observations(), tmp_path, wrapper, lines)
    assert not (worktree / _REL).exists()
    assert _calls(wrapper) == []
    assert lines == []


def test_the_closing_label_moves_to_the_end(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    target = worktree / _REL
    target.parent.mkdir(parents=True)
    target.write_text(
        "# Improvement observations\n\nearlier\n\n# Task run (Phase D)\n\n\n", encoding="utf-8"
    )
    wrapper = _plant_wrapper(tmp_path)
    observations = Observations()
    observations.add("optimization", "p", "e", "c")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert target.read_text(encoding="utf-8") == (
        "# Improvement observations\n"
        "\n"
        "earlier\n"
        "\n" + _HEADING + "## p\n- **category:** optimization\n- **evidence:** e\n"
        "- **cost this run:** c\n\n"
        "# Task run (Phase D)\n"
    )
    assert _calls(wrapper) == [f"--repo {worktree} --artifact observations --push"]


def test_each_needle_is_rewritten(tmp_path: Path) -> None:
    worktree, main, home = _dirs(tmp_path)
    wrapper = _plant_wrapper(tmp_path)
    observations = Observations()
    observations.add(
        "shared-state",
        f"see {worktree}/src/a.py and {worktree} here",
        f"`{main}/docs/x.md` and ({main})",
        f"{home}/.config/y, {home}",
    )
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert (worktree / _REL).read_bytes() == (
        b"# Script-driven planning \xe2\x80\x94 2026-11-27T10:00:00Z\n\n"
        b"## see src/a.py and . here\n"
        b"- **category:** shared-state\n"
        b"- **evidence:** `docs/x.md (main checkout)` and (. (main checkout))\n"
        b"- **cost this run:** ~/.config/y, ~\n\n"
        b"# Task run (Phase D)\n"
    )
    assert len(_calls(wrapper)) == 1


def test_a_needle_followed_by_a_non_delimiter_is_left_alone() -> None:
    needles = (Needle("/a/wt", "worktree"), Needle("/a/home", "home"))
    assert rewrite_machine_paths("/a/wtx /a/homes\n/a/wt-1", needles) == (
        "/a/wtx /a/homes\n/a/wt-1"
    )


def test_an_unusable_needle_is_dropped_with_a_log_line() -> None:
    lines: list[str] = []
    assert machine_needles(worktree="/", main_repo="/solo", home="/x/it's", log=lines.append) == ()
    assert lines == [
        "observations: the worktree needle is empty or quoted; dropped",
        "observations: the main checkout needle '/solo' is one path segment; dropped",
        "observations: the home needle is empty or quoted; dropped",
    ]


def test_the_main_checkout_equal_to_the_worktree_is_dropped_and_longer_needles_go_first() -> None:
    lines: list[str] = []
    assert machine_needles(
        worktree="/a/b/", main_repo="/a/b", home="/a/b/c/d", log=lines.append
    ) == (Needle("/a/b/c/d", "home"), Needle("/a/b", "worktree"))
    assert lines == []


def test_a_residual_needle_restores_the_file_without_a_commit(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    target = worktree / _REL
    target.parent.mkdir(parents=True)
    target.write_bytes(b"# Improvement observations\n")
    wrapper = _plant_wrapper(tmp_path)
    observations = Observations()
    observations.add("silent-failure", f"{worktree}x", "e", "c")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert target.read_bytes() == b"# Improvement observations\n"
    assert _calls(wrapper) == []
    assert lines == [
        f"observations: '{_REL}' still carries a machine path after the rewrite; not committed"
    ]


def test_a_failing_wrapper_restores_the_file_and_logs(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    target = worktree / _REL
    target.parent.mkdir(parents=True)
    target.write_bytes(b"# Improvement observations\n")
    wrapper = _plant_wrapper(tmp_path, status=1)
    observations = Observations()
    observations.add("agent-contract", "p", "e", "c")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert target.read_bytes() == b"# Improvement observations\n"
    assert _calls(wrapper) == [f"--repo {worktree} --artifact observations --push"]
    assert lines == [
        f"observations: the commit of '{_REL}' failed: "
        "commit-on-branch.sh --artifact observations exited 1: refused"
    ]


def test_a_failing_wrapper_removes_a_file_that_did_not_exist(tmp_path: Path) -> None:
    worktree, _, _ = _dirs(tmp_path)
    wrapper = _plant_wrapper(tmp_path, status=1)
    observations = Observations()
    observations.add("flow-efficiency", "p", "e", "c")
    lines: list[str] = []
    _flush(observations, tmp_path, wrapper, lines)
    assert not (worktree / _REL).exists()
    assert len(lines) == 1
