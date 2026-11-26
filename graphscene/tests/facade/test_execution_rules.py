"""The rule this file exists to enforce: a caller importing only from `graphscene` applies the
execution rules end to end, and they reproduce the engine-owned control cases of
`cli/test/planning-driver-control.test.mjs` on the `StubExecutor` — STOP and the dispatch cap send
nothing of a set, a STOP or PAUSE raised while a set runs lets the set finish and is honoured
before the next one, a gate undelivered three sets running self-pauses, an infrastructure failure
(a stall or a return failing its schema among them) is re-dispatched alone, an agent-reported
blocker is held with no retry, every launched session gets one `Launch` row, and a gate failing all
three attempts is held and recorded through a real `Walker` join, where the committed graph's own
binding stops the walk.

It imports the public names from `graphscene`, as a caller does (`.claude/context/graphscene.md` →
`## Tests`). Each case is named after its pilot case and runs with `backoff_seconds=0` through
`asyncio.run`. `Signals`, `Counter`, `Rows` and `DictHost` are in-test classes satisfying
`RunSignals`, `DispatchCounter`, `LaunchSink` and `PredicateHost` structurally. Every expected
literal is hand-written from the script and from reading `valid_generic.json`, never taken from
the code's output.

Deliberately not covered:

- The escalation-resume cases (a)-(d): which gates a resume re-dispatches is the host's.
- The `<ask>` questions park: the host's.
- Round-file refusals and their re-dispatch: the host's.
- Commits, the run log and the clarification and pause files: the host's, and the run loop's
  (#423).
"""

import asyncio
from collections.abc import Sequence
from pathlib import Path

from graphscene import (
    AttemptBook,
    Completed,
    Dispatch,
    DispatchSet,
    ExecutionLimits,
    Failed,
    FileStateStore,
    GateRecord,
    Halt,
    Launch,
    NodeRecord,
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    SetResult,
    Stop,
    StubExecutor,
    UndeliveredBreaker,
    Walker,
    execute_set,
    load_graph_file,
)

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "flow_graph" / "valid_generic.json"

_HELD = "crashed"
_GATES = ("parity_review", "architecture_review", "plan_review")


class Signals:
    """Answers STOP once `stop_requested` has been called more than `stop_after` times, and PAUSE
    once `pause_requested` has been called more than `pause_after` times."""

    def __init__(self, stop_after: int | None = None, pause_after: int | None = None) -> None:
        self._stop_after = stop_after
        self._pause_after = pause_after
        self._stop_calls = 0
        self._pause_calls = 0

    def stop_requested(self) -> bool:
        self._stop_calls += 1
        return self._stop_after is not None and self._stop_calls > self._stop_after

    def pause_requested(self) -> bool:
        self._pause_calls += 1
        return self._pause_after is not None and self._pause_calls > self._pause_after


class Counter:
    def __init__(self, total: int = 0) -> None:
        self._total = total

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


class Run:
    """One run's state, shared by every set it executes."""

    def __init__(
        self,
        stub: StubExecutor,
        *,
        signals: Signals | None = None,
        counter: Counter | None = None,
        dispatch_cap: int | None = None,
    ) -> None:
        self.stub = stub
        self.signals = signals or Signals()
        self.counter = counter or Counter()
        self.rows = Rows()
        self.book = AttemptBook()
        self.breaker = UndeliveredBreaker()
        self.limits = ExecutionLimits(backoff_seconds=0, dispatch_cap=dispatch_cap)

    def execute(self, dispatches: Sequence[Dispatch]) -> SetResult:
        return asyncio.run(
            execute_set(
                dispatches,
                self.stub,
                signals=self.signals,
                counter=self.counter,
                sink=self.rows,
                book=self.book,
                breaker=self.breaker,
                limits=self.limits,
                failure_outcome=_HELD,
            )
        )


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent=f"{node}-agent",
        prompt=None,
        counters={},
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )


def _gates() -> list[Dispatch]:
    return [_dispatch(gate) for gate in _GATES]


def _writer() -> list[Dispatch]:
    return [_dispatch("plan_writer")]


def _stub(script: dict[str, list[Scripted]]) -> StubExecutor:
    return StubExecutor(script)


def _all_approve() -> dict[str, list[Scripted]]:
    return {gate: [ScriptedOutcome("approved")] for gate in _GATES}


def test_stop_present_before_a_set_launches_none_of_it() -> None:
    run = Run(_stub(_all_approve()), signals=Signals(stop_after=0))
    assert run.execute(_gates()) == SetResult((), Halt("stop", "stop requested before a set of 3"))
    assert run.stub.started == ()
    assert run.rows.rows == []
    assert run.counter.total() == 0


def test_stop_raised_while_a_set_runs_lets_the_set_finish_and_launches_nothing_after() -> None:
    script = _all_approve()
    script["plan_review"] = [ScriptedFailure("infra", "session ended in error")]
    script["plan_writer"] = [ScriptedOutcome("done")]
    # The first set's clear asks STOP once per gate; every later ask answers STOP.
    run = Run(_stub(script), signals=Signals(stop_after=3))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("architecture_review", "approved", None),
        ),
        Halt("stop", "stop requested before a set of 1"),
    )
    assert run.stub.started == _GATES
    assert run.stub.cancelled == ()
    assert run.execute(_writer()) == SetResult((), Halt("stop", "stop requested before a set of 1"))
    assert run.stub.started == _GATES
    assert run.counter.total() == 3


def test_pause_raised_mid_set_is_honoured_at_the_join() -> None:
    script = _all_approve()
    script["plan_writer"] = [ScriptedOutcome("done")]
    # The first set's clear asks PAUSE once; every later ask answers PAUSE.
    run = Run(_stub(script), signals=Signals(pause_after=1))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("architecture_review", "approved", None),
            NodeRecord("plan_review", "approved", None),
        ),
        None,
    )
    assert run.execute(_writer()) == SetResult(
        (), Halt("pause", "pause requested before a set of 1")
    )
    assert run.stub.started == _GATES


def test_one_gate_undelivered_three_times_running_self_pauses() -> None:
    script = _all_approve()
    script["architecture_review"] = [
        ScriptedFailure("undelivered", "no result from the provider"),
        ScriptedFailure("undelivered", "no result from the provider"),
        ScriptedFailure("undelivered", "provider unavailable"),
    ]
    run = Run(_stub(script))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("plan_review", "approved", None),
        ),
        Halt("undelivered", "3 consecutive sets had an undelivered result"),
    )
    assert run.stub.started == (
        "parity_review",
        "architecture_review",
        "plan_review",
        "architecture_review",
        "architecture_review",
    )
    assert [(row.node, row.attempt) for row in run.rows.rows] == [
        ("parity_review", 1),
        ("architecture_review", 1),
        ("plan_review", 1),
        ("architecture_review", 1),
        ("architecture_review", 1),
    ]


def test_a_gate_stalled_once_is_re_dispatched_alone_and_passes_its_siblings_run_once() -> None:
    script = _all_approve()
    script["architecture_review"] = [
        ScriptedFailure("infra", "stalled: its stream was silent", delay=0.01),
        ScriptedOutcome("approved"),
    ]
    run = Run(_stub(script))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("plan_review", "approved", None),
            NodeRecord("architecture_review", "approved", None),
        ),
        None,
    )
    assert run.stub.started == (
        "parity_review",
        "architecture_review",
        "plan_review",
        "architecture_review",
    )
    assert run.stub.cancelled == ()
    assert run.rows.rows[2] == Launch(
        2,
        "architecture_review",
        "architecture_review-agent",
        1,
        3,
        Failed("infra", "stalled: its stream was silent"),
    )
    assert run.rows.rows[3] == Launch(
        4, "architecture_review", "architecture_review-agent", 2, 3, Completed("approved")
    )


def test_a_return_that_fails_its_schema_is_retried_as_infrastructure_not_parked() -> None:
    script = _all_approve()
    script["plan_review"] = [
        ScriptedFailure("infra", "return block failed its schema: findings_file is required"),
        ScriptedOutcome("approved"),
    ]
    run = Run(_stub(script))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("architecture_review", "approved", None),
            NodeRecord("plan_review", "approved", None),
        ),
        None,
    )
    assert run.stub.started == (*_GATES, "plan_review")


def test_an_agent_reported_blocker_parks_with_no_retry() -> None:
    script = _all_approve()
    script["architecture_review"] = [ScriptedFailure("agent", "blocker: the plan names no layer")]
    run = Run(_stub(script))
    assert run.execute(_gates()) == SetResult(
        (
            NodeRecord("parity_review", "approved", None),
            NodeRecord("plan_review", "approved", None),
            NodeRecord("architecture_review", _HELD, "blocker: the plan names no layer"),
        ),
        None,
    )
    assert run.stub.started == _GATES


def test_the_dispatch_cap_halts_before_a_set_that_would_pass_it() -> None:
    script = _all_approve()
    script["plan_writer"] = [ScriptedOutcome("done")]
    run = Run(_stub(script), dispatch_cap=3)
    assert run.execute(_writer()) == SetResult((NodeRecord("plan_writer", "done", None),), None)
    assert run.execute(_gates()) == SetResult(
        (),
        Halt(
            "cap",
            "1 dispatched; a set of 3 (parity_review, architecture_review, plan_review)"
            " would pass the cap 3",
        ),
    )
    assert run.stub.started == ("plan_writer",)
    assert run.rows.rows == [Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("done"))]


def test_a_session_table_names_every_session() -> None:
    script = _all_approve()
    script["plan_writer"] = [ScriptedOutcome("done")]
    script["parity_review"] = [ScriptedFailure("infra", "crashed"), ScriptedOutcome("approved")]
    script["architecture_review"] = [ScriptedFailure("agent", "blocker: no layer")]
    run = Run(_stub(script))
    run.execute(_writer())
    run.execute(_gates())
    assert run.rows.rows == [
        Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("done")),
        Launch(2, "parity_review", "parity_review-agent", 1, 3, Failed("infra", "crashed")),
        Launch(
            3,
            "architecture_review",
            "architecture_review-agent",
            1,
            3,
            Failed("agent", "blocker: no layer"),
        ),
        Launch(4, "plan_review", "plan_review-agent", 1, 3, Completed("approved")),
        Launch(5, "parity_review", "parity_review-agent", 2, 3, Completed("approved")),
    ]


def test_a_gate_failing_all_three_attempts_parks_once_after_its_siblings_naming_every_attempt(
    tmp_path: Path,
) -> None:
    walker = Walker(
        load_graph_file(_FIXTURE),
        FileStateStore(tmp_path / "walk.json"),
        DictHost({"stage_disabled": False}),
    )
    run = Run(
        _stub(
            {
                "draft": [ScriptedOutcome("done")],
                "edit_check": [
                    ScriptedFailure("infra", "session ended in error"),
                    ScriptedFailure("infra", "no return block"),
                    ScriptedFailure("infra", "return block failed its schema"),
                ],
            }
        )
    )

    draft = walker.start()
    assert isinstance(draft, Dispatch)
    drafted = run.execute([draft])
    assert drafted == SetResult((NodeRecord("draft", "done", None),), None)
    review = walker.next("done", "draft", None)
    assert isinstance(review, DispatchSet)
    assert [d.node for d in review.dispatches] == ["edit_check"]

    reviewed = run.execute(review.dispatches)
    detail = (
        "all 3 attempts failed for an infrastructure reason"
        "\nattempt 1 of 3: session ended in error"
        "\nattempt 2 of 3: no return block"
        "\nattempt 3 of 3: return block failed its schema"
    )
    assert reviewed == SetResult((NodeRecord("edit_check", "crashed", detail),), None)
    assert run.stub.started == ("draft", "edit_check", "edit_check", "edit_check")

    steps = [walker.next(r.outcome, r.node, r.detail) for r in reviewed.records]
    assert steps == [
        Stop(
            "<halt>",
            node="edit_check",
            agent="article-editor",
            reason="crash",
            summary=None,
            evidence=None,
            round_counts=(),
            held=(GateRecord("edit_check", "crashed", detail),),
            closed_round=(),
            passed=(),
        )
    ]
