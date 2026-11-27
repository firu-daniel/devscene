"""The rule this file exists to enforce: a caller importing only from `graphscene` drives the
committed graphs `valid_generic.json` and `valid_plain_round.json` end to end in run mode,
`start_run` and `continue_run`, over a real `FileStateStore`, and gets back the `RunExit` the graph
and the script lead to — the graph's `End`, the graph's own `Stop` binding, or a `Halt`, between
sets or mid-round, that a later `continue_run` resumes from the saved walk. A planted format-5
graph declaring `vocabulary.hooks` runs its dispatch, round and terminal hooks through the
caller's `HookHost` at their firing points, and the same graph with one hook undeclared is refused
at stage `vocabulary`.

It imports the public names from `graphscene`, as a caller does (`.claude/context/graphscene.md` →
`## Tests`). Each case runs with `backoff_seconds=0` through `asyncio.run`. `Signals`, `Counter`,
`Rows`, `DictHost` and `LoggingHooks` are in-test classes satisfying `RunSignals`,
`DispatchCounter`, `LaunchSink`, `PredicateHost` and `HookHost` structurally. Every expected
literal is hand-written from the script and from reading the fixture or the planted graph, never
taken from the code's output.

Deliberately not covered: the run loop's own cases (refusals, interrupts, cancellation, the
store's thread) are `graphscene/tests/engine/test_run_loop.py`'s.
"""

import asyncio
from pathlib import Path
from types import MappingProxyType

import pytest

from graphscene import (
    AfterDispatch,
    AfterRound,
    BeforeDispatch,
    BeforeEnd,
    BeforeRound,
    Completed,
    Dispatch,
    DispatchNode,
    DispatchSet,
    End,
    ExecutionLimits,
    FileStateStore,
    GraphError,
    Halt,
    HookCall,
    HookHost,
    Launch,
    RoundPassage,
    RunExit,
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    Stop,
    StubExecutor,
    Violation,
    Walker,
    continue_run,
    load_graph,
    load_graph_file,
    start_run,
)

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "flow_graph" / "valid_generic.json"
_PLAIN_ROUND = Path(__file__).parents[1] / "fixtures" / "flow_graph" / "valid_plain_round.json"

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


def test_a_stop_mid_round_saves_the_recorded_gate_and_continue_run_finishes_from_the_state_file(
    tmp_path: Path,
) -> None:
    state_file = tmp_path / "walk.json"
    stub = _stub(
        {
            "lint": [
                ScriptedFailure("infra", "session ended in error"),
                ScriptedOutcome("accepted"),
            ],
            "license": [ScriptedOutcome("accepted", "license.md")],
        }
    )

    def walker() -> Walker:
        return Walker(load_graph_file(_PLAIN_ROUND), FileStateStore(state_file), DictHost({}))

    # The first pass's clear asks STOP once per gate; lint's retry pass's first ask is the third.
    assert asyncio.run(
        start_run(
            walker(),
            stub,
            signals=Signals(stop_after=2),
            counter=Counter(),
            sink=Rows(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome=_HELD,
            entry="checks",
        )
    ) == Halt("stop", "stop requested before a set of 1")
    lint = Dispatch(
        node="lint",
        agent="lint-checker",
        prompt_variant=None,
        counters=MappingProxyType({}),
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )
    assert walker().current() == DispatchSet("checks", 0, (lint,), ())

    rows = Rows()
    assert asyncio.run(
        continue_run(
            walker(),
            stub,
            signals=Signals(),
            counter=Counter(),
            sink=rows,
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome=_HELD,
        )
    ) == End("<finish>", "published", reports=(), passed=(RoundPassage("checks", 0, "pass"),))
    assert rows.rows == [Launch(1, "lint", "lint-checker", 1, 3, Completed("accepted"))]


_HOOKS = ("prep", "note", "open", "close", "publish")


def _hooked(declared: tuple[str, ...] = _HOOKS) -> dict[str, object]:
    """`intake` runs `prep` before and `note` after, the `checks` round runs `open` before and
    `close` after, and `published` runs `publish` before; `declared` is `vocabulary.hooks`."""

    def gate(agent: str) -> dict[str, object]:
        return {
            "kind": "dispatch",
            "agent": agent,
            "heartbeat": f"[checks · attempt {{iteration}}] → {agent}",
            "outcomes": {"accepted": {"to": "checks"}, "rejected": {"to": "checks"}},
        }

    return {
        "formatVersion": 5,
        "flow": "hooked_release",
        "description": "An intake, a round of two checks and a publish, each node hooked.",
        "vocabulary": {
            "outcomes": {
                "accepted": {"verdict": "pass"},
                "rejected": {"verdict": "fail"},
                "crashed": {"held": True},
            },
            "bindings": {
                "<halt>": {"primitive": "stop", "reasons": ["failed", "crash"]},
                "<finish>": {"primitive": "end"},
            },
            "predicates": {},
            "hooks": {name: {} for name in declared},
        },
        "start": "intake",
        "entries": ["intake"],
        "counters": {},
        "paths": {},
        "reports": [],
        "nodes": {
            "intake": {
                "kind": "dispatch",
                "agent": "release-intake",
                "heartbeat": "[intake · attempt {iteration}] → release-intake",
                "promptSource": "prompts/release-intake.md",
                "outcomes": {
                    "accepted": {"to": "checks"},
                    "rejected": {"to": "discarded"},
                    "crashed": {"binding": "<halt>", "reason": "crash"},
                },
                "before": ["prep"],
                "after": ["note"],
            },
            "lint": gate("lint-checker"),
            "license": gate("license-checker"),
            "checks": {
                "kind": "round",
                "parallel": True,
                "gates": ["lint", "license"],
                "outcomes": {
                    "accepted": {"to": "published"},
                    "rejected": {"binding": "<halt>", "reason": "failed"},
                },
                "before": ["open"],
                "after": ["close"],
            },
            "published": {"kind": "terminal", "binding": "<finish>", "before": ["publish"]},
            "discarded": {"kind": "terminal", "binding": "<finish>"},
        },
    }


class LoggingHooks:
    """Provides every hook and logs each run as `(hook, call.kind, node or round, detail)`."""

    def __init__(self) -> None:
        self.lines: list[tuple[str, str, str, str]] = []

    def provides(self, hook: str) -> bool:
        return True

    async def run(self, hook: str, call: HookCall) -> None:
        if isinstance(call, BeforeDispatch):
            line = (call.dispatch.node, f"seq {call.seq} attempt {call.attempt}")
        elif isinstance(call, AfterDispatch):
            line = (call.record.node, f"{call.record.outcome} -> {call.step.kind}")
        elif isinstance(call, BeforeRound):
            gates = ",".join(d.node for d in call.dispatch_set.dispatches)
            line = (call.dispatch_set.round, f"{call.dispatch_set.number}: {gates}")
        elif isinstance(call, AfterRound):
            line = (call.passage.round, f"{call.passage.number}: {call.passage.verdict}")
        else:
            assert isinstance(call, BeforeEnd)
            line = (call.end.node, call.end.binding)
        self.lines.append((hook, call.kind, *line))


def test_a_hooked_graph_runs_its_dispatch_round_and_terminal_hooks_in_order(
    tmp_path: Path,
) -> None:
    graph = load_graph(_hooked())
    intake = graph.nodes["intake"]
    assert isinstance(intake, DispatchNode)
    assert intake.prompt_source == "prompts/release-intake.md"
    stub = _stub(
        {
            "intake": [ScriptedOutcome("accepted")],
            "lint": [ScriptedOutcome("accepted")],
            "license": [ScriptedOutcome("accepted")],
        }
    )
    logging_hooks = LoggingHooks()
    hooks: HookHost = logging_hooks
    assert asyncio.run(
        start_run(
            Walker(graph, FileStateStore(tmp_path / "walk.json"), DictHost({})),
            stub,
            signals=Signals(),
            counter=Counter(),
            sink=Rows(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome=_HELD,
            hooks=hooks,
        )
    ) == End("<finish>", "published", reports=(), passed=(RoundPassage("checks", 0, "pass"),))
    assert logging_hooks.lines == [
        ("prep", "before_dispatch", "intake", "seq 1 attempt 1"),
        ("note", "after_dispatch", "intake", "accepted -> set"),
        ("open", "before_round", "checks", "0: lint,license"),
        ("close", "after_round", "checks", "0: pass"),
        ("publish", "before_end", "published", "<finish>"),
    ]


def test_the_hooked_graph_with_one_hook_undeclared_is_refused_at_the_vocabulary_stage() -> None:
    with pytest.raises(GraphError) as raised:
        load_graph(_hooked(declared=("prep", "note", "open", "close")))
    assert raised.value.stage == "vocabulary"
    assert raised.value.violations == (
        Violation(
            "nodes.published.before[0]", "hook 'publish' is not declared in vocabulary.hooks"
        ),
    )
