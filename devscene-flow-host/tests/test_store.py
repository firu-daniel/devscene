"""The rule this file exists to enforce: branch `b`'s walk is saved in its own file,
`<stateDir>/.flow_walker_state/<quote(b, safe="")>.json`, so one branch's walk is never read for
another, and nothing the store writes lands outside that directory. A flat file in the
directory's place makes the write raise an `OSError` and is left unchanged.

Every file is planted under `tmp_path`; every expected path is a literal.
"""

from pathlib import Path

import pytest
from graphscene import End, WalkState

from devscene_flow_host.host.store import walk_state_path, walk_store

_STATE = WalkState(
    flow="harness",
    node="done",
    awaiting="done",
    pending=End(binding="done", node="done", reports=(), passed=()),
    counters={},
    round_numbers={},
    open_round=None,
    prompts={},
    reports={},
    skipped={},
)


def test_a_plain_branch_is_its_own_file_name(tmp_path: Path) -> None:
    assert walk_state_path(tmp_path, "state", "feat_x") == (
        tmp_path / "state" / ".flow_walker_state" / "feat_x.json"
    )


def test_a_slash_is_encoded_rather_than_a_subdirectory(tmp_path: Path) -> None:
    assert walk_state_path(tmp_path, "state", "feat/x") == (
        tmp_path / "state" / ".flow_walker_state" / "feat%2Fx.json"
    )


def test_a_percent_is_encoded_so_the_encoding_is_injective(tmp_path: Path) -> None:
    assert walk_state_path(tmp_path, "state", "a%b") == (
        tmp_path / "state" / ".flow_walker_state" / "a%25b.json"
    )


def test_an_empty_branch_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        walk_state_path(tmp_path, "state", "")
    assert str(raised.value) == "a walk's branch is empty"


def test_two_branches_have_two_walks(tmp_path: Path) -> None:
    walk_store(tmp_path, "state", "feat/a").write(_STATE)
    assert walk_store(tmp_path, "state", "feat/b").read() is None
    assert walk_store(tmp_path, "state", "feat/a").read() == _STATE


def test_everything_written_stays_inside_the_state_directory(tmp_path: Path) -> None:
    store = walk_store(tmp_path, "state", "feat/a")
    store.write(_STATE)
    with store.lock():
        pass
    directory = tmp_path / "state" / ".flow_walker_state"
    for path in tmp_path.rglob("*"):
        if path in directory.parents or path == directory:
            continue
        assert directory in path.parents, path
    assert {path.name for path in directory.iterdir()} == {"feat%2Fa.json", "feat%2Fa.json.lock"}


def test_a_flat_file_in_the_way_raises_and_is_left_unchanged(tmp_path: Path) -> None:
    flat = tmp_path / "state" / ".flow_walker_state"
    flat.parent.mkdir()
    flat.write_bytes(b"node: build\n")
    with pytest.raises(OSError):
        walk_store(tmp_path, "state", "feat/a").write(_STATE)
    assert flat.read_bytes() == b"node: build\n"
