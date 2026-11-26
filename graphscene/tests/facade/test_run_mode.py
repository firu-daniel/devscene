"""The rule this file exists to enforce: a caller importing only from `graphscene` drives the
committed graph `valid_generic.json` end to end in run mode, `start_run` and `continue_run`, over
a real `FileStateStore`, and gets back the `RunExit` the graph and the script lead to — the graph's
`End`, the graph's own `Stop` binding, or a `Halt` that a later `continue_run` resumes from the
saved walk.

It imports the public names from `graphscene`, as a caller does (`.claude/context/graphscene.md` →
`## Tests`). Each case runs with `backoff_seconds=0` through `asyncio.run`. `Signals`, `Counter`,
`Rows` and `DictHost` are in-test classes satisfying `RunSignals`, `DispatchCounter`, `LaunchSink`
and `PredicateHost` structurally. Every expected literal is hand-written from the script and from
reading `valid_generic.json`, never taken from the code's output.

Deliberately not covered: the run loop's own cases (refusals, interrupts, cancellation, the
store's thread) are `graphscene/tests/engine/test_run_loop.py`'s.
"""

import asyncio
from pathlib import Path

from graphscene import (
    End,
    ExecutionLimits,
    FileStateStore,
    Halt,
    Launch,
    RoundPassage,
    RunExit,
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    Stop,
    StubExecutor,
    Walker,
    continue_run,
    load_graph_file,
    start_run,
)

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "flow_graph" / "valid_generic.json"

_HELD = "crashed"

_PUBLISHED = End(
    "<finish>",
    "published",
    reports=(("edit_check", "approved"),),
    passed=(RoundPassage("review_round", 0, "pass"),),
)


class Signals:
    """Answers STOP once `stop_requested` has been called more than `stop_after` times."""

    def __init__(self, stop_after: int | None = None) -> None:
        self._stop_after = stop_after
        self._stop_calls = 0

    def stop_requested(self) -> bool:
        self._stop_calls += 1
        return self._stop_after is not None and self._stop_calls > self._stop_after

    def pause_requested(self) -> bool:
        return False


class Counter:
    def __init__(self) -> None:
        self._total = 0

    def total(self) -> int:
        return self._total

    def increment(self) -> int:
        self._total += 1
        return self._total


class Rows:
    def __init__(self) -> None:
        self.rows: list[Launch] = []

    def record(self, launch: Launch) -> None:
        self.rows.append(launch)


class DictHost:
    def __init__(self, answers: dict[str, bool]) -> None:
        self.answers = answers

    def answer(self, predicate: str, node: str) -> bool | None:
        return self.answers.get(predicate)


def _walker(state_file: Path) -> Walker:
    return Walker(
        load_graph_file(_FIXTURE),
        FileStateStore(state_file),
        DictHost({"stage_disabled": False}),
    )


def _start(walker: Walker, stub: StubExecutor, signals: Signals) -> RunExit:
    return asyncio.run(
        start_run(
            walker,
            stub,
            signals=signals,
            counter=Counter(),
            sink=Rows(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome=_HELD,
        )
    )


def _continue(walker: Walker, stub: StubExecutor, signals: Signals) -> RunExit:
    return asyncio.run(
        continue_run(
            walker,
            stub,
            signals=signals,
            counter=Counter(),
            sink=Rows(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome=_HELD,
        )
    )


def _stub(script: dict[str, list[Scripted]]) -> StubExecutor:
    return StubExecutor(script)


def test_a_draft_and_an_approving_edit_check_end_at_published(tmp_path: Path) -> None:
    stub = _stub({"draft": [ScriptedOutcome("done")], "edit_check": [ScriptedOutcome("approved")]})
    assert _start(_walker(tmp_path / "walk.json"), stub, Signals()) == _PUBLISHED
    assert stub.started == ("draft", "edit_check")


def test_a_draft_failing_three_infra_attempts_stops_through_the_graphs_halt_binding(
    tmp_path: Path,
) -> None:
    stub = _stub(
        {
            "draft": [
                ScriptedFailure("infra", "session ended in error"),
                ScriptedFailure("infra", "no return block"),
                ScriptedFailure("infra", "return block failed its schema"),
            ]
        }
    )
    assert _start(_walker(tmp_path / "walk.json"), stub, Signals()) == Stop(
        "<halt>",
        node="draft",
        agent="article-writer",
        reason="crash",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(),
        closed_round=(),
        passed=(),
    )
    assert stub.started == ("draft", "draft", "draft")


def test_a_stop_after_the_draft_halts_and_continue_run_finishes_from_the_state_file(
    tmp_path: Path,
) -> None:
    state_file = tmp_path / "walk.json"
    first = _stub({"draft": [ScriptedOutcome("done")]})
    # The draft's set of 1 asks STOP once; the edit check's set asks a second time.
    assert _start(_walker(state_file), first, Signals(stop_after=1)) == Halt(
        "stop", "stop requested before a set of 1"
    )
    assert first.started == ("draft",)

    second = _stub({"edit_check": [ScriptedOutcome("approved")]})
    assert _continue(_walker(state_file), second, Signals()) == _PUBLISHED
    assert second.started == ("edit_check",)
