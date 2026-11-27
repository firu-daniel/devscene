"""The rule this file exists to enforce: STOP and PAUSE are answered from `<stateDir>/STOP` and
`<stateDir>/PAUSE` and re-read on every call; the kill switch is `AUTONOMOUS_STOP` under the main
checkout's configured `stateDir`; the dispatch counter resets to `0\\n`, writes each increment
whole as one decimal line and refuses a corrupt file with a `RecordError` naming it; and
`planning_limits` fixes every limit but the dispatch cap, at 5 concurrent dispatches, its backoff
read from `PD_BACKOFF_SECS` at call time with 60 seconds as default and ceiling. Both file
classes satisfy GraphScene's `RunSignals` and `DispatchCounter` structurally, which `mypy` `strict`
checks on the typed assignments below.

Every record is planted under `tmp_path`; every expected value is a literal written from the task
plan's rules, never taken from the output of the code under test.

Deliberately not covered:
- An `OSError` other than a missing counter file, which propagates unwrapped: no portable way to
  plant one under `tmp_path`.
"""

import json
from pathlib import Path

import pytest
from graphscene import DispatchCounter, RunSignals

from devscene_flow_host.host.run_control import (
    FileDispatchCounter,
    FileRunSignals,
    backoff_seconds,
    kill_switch_present,
    planning_limits,
)
from devscene_flow_host.records.errors import RecordError


def _state(root: Path) -> Path:
    state = root / "state"
    state.mkdir(parents=True, exist_ok=True)
    return state


def test_stop_and_pause_are_answered_from_the_planted_files(tmp_path: Path) -> None:
    state = _state(tmp_path)
    signals: RunSignals = FileRunSignals(tmp_path, "state")
    assert signals.stop_requested() is False
    assert signals.pause_requested() is False

    (state / "STOP").write_text("", encoding="utf-8")
    assert signals.stop_requested() is True
    assert signals.pause_requested() is False

    (state / "PAUSE").write_text("", encoding="utf-8")
    assert signals.pause_requested() is True


def test_stop_and_pause_are_re_read_after_the_file_is_removed(tmp_path: Path) -> None:
    state = _state(tmp_path)
    (state / "STOP").write_text("", encoding="utf-8")
    (state / "PAUSE").write_text("", encoding="utf-8")
    signals = FileRunSignals(tmp_path, "state")
    assert signals.stop_requested() is True
    assert signals.pause_requested() is True

    (state / "STOP").unlink()
    (state / "PAUSE").unlink()
    assert signals.stop_requested() is False
    assert signals.pause_requested() is False


def test_the_kill_switch_is_read_under_the_main_checkouts_configured_state_dir(
    tmp_path: Path,
) -> None:
    (tmp_path / "devscene.config.json").write_text(
        json.dumps({"defaultBranch": "main", "stateDir": "runs/"}), encoding="utf-8"
    )
    (tmp_path / "runs").mkdir()
    (tmp_path / "devscene").mkdir()
    (tmp_path / "devscene" / "AUTONOMOUS_STOP").write_text("", encoding="utf-8")
    assert kill_switch_present(tmp_path) is False

    (tmp_path / "runs" / "AUTONOMOUS_STOP").write_text("", encoding="utf-8")
    assert kill_switch_present(tmp_path) is True


def test_the_counter_resets_and_counts_with_exact_bytes(tmp_path: Path) -> None:
    state = _state(tmp_path)
    (state / ".dispatch_counter").write_bytes(b"17\n")
    counter = FileDispatchCounter(tmp_path, "state")
    typed: DispatchCounter = counter

    counter.reset()
    assert (state / ".dispatch_counter").read_bytes() == b"0\n"
    assert typed.total() == 0

    assert typed.increment() == 1
    assert typed.increment() == 2
    assert (state / ".dispatch_counter").read_bytes() == b"2\n"
    assert typed.total() == 2
    assert sorted(path.name for path in state.iterdir()) == [".dispatch_counter"]


@pytest.mark.parametrize("content", [b"two\n", b"", b"3", b"-1\n", b"1\n2\n", b"\xff\n"])
def test_a_corrupt_counter_is_a_record_error_naming_it(tmp_path: Path, content: bytes) -> None:
    (_state(tmp_path) / ".dispatch_counter").write_bytes(content)
    with pytest.raises(RecordError) as caught:
        FileDispatchCounter(tmp_path, "state").increment()
    assert str(caught.value) == "state/.dispatch_counter: not one decimal line"


def test_a_missing_counter_is_a_record_error_naming_it(tmp_path: Path) -> None:
    _state(tmp_path)
    with pytest.raises(RecordError) as caught:
        FileDispatchCounter(tmp_path, "state").total()
    assert str(caught.value) == "the dispatch counter 'state/.dispatch_counter' does not exist"


@pytest.mark.parametrize(
    ("environ", "expected"),
    [
        ({}, 60.0),
        ({"PD_BACKOFF_SECS": "0"}, 0.0),
        ({"PD_BACKOFF_SECS": "5"}, 5.0),
        ({"PD_BACKOFF_SECS": "61"}, 60.0),
        ({"PD_BACKOFF_SECS": "-1"}, 60.0),
        ({"PD_BACKOFF_SECS": "1.5"}, 60.0),
        ({"PD_BACKOFF_SECS": ""}, 60.0),
    ],
)
def test_the_backoff_is_read_as_pd_backoff_read_it(
    environ: dict[str, str], expected: float
) -> None:
    assert backoff_seconds(environ) == expected


def test_planning_limits_read_the_backoff_at_call_time(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PD_BACKOFF_SECS", "0")
    assert planning_limits(7).backoff_seconds == 0.0


def test_planning_limits_fix_every_limit_but_the_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PD_BACKOFF_SECS", raising=False)
    limits = planning_limits(40)
    assert limits.max_attempts == 3
    assert limits.backoff_seconds == 60.0
    assert limits.dispatch_cap == 40
    assert limits.run_timeout_seconds is None
    assert limits.max_concurrent_dispatches == 5
