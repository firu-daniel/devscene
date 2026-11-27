"""The rule this file exists to enforce: `graphscene.adapters.walk_json` turns a `WalkState` into
its version-2 JSON document and back with no loss, and refuses a malformed document with a
`ValueError` naming the dotted path and the reason; its step document of an action is that
action's `pending` encoding in the state document and of a `Refused` is
`{"kind": "refused", "reason": …}`; and it reads a round-resume document into a `RoundResume`,
refusing a malformed one in the state codec's words.

The round-trip states are hand-built, one per pending-action variant; together they carry every
passage kind, an `OpenRound` with records and every optional field both set and `None`. The
decoded document and every refusal text are hand-written from reading the planted documents,
never taken from the codec's output.
"""

import json
from types import MappingProxyType

import pytest

from graphscene.adapters.walk_json import (
    resume_from_json,
    state_from_json,
    state_to_json,
    step_document,
)
from graphscene.model.walk_actions import (
    Action,
    Dispatch,
    DispatchSet,
    End,
    GateRecord,
    Interrupt,
    LedgerPassage,
    Passage,
    Refused,
    RoundPassage,
    SkipPassage,
    Stop,
    Wait,
)
from graphscene.model.walk_state import Awaiting, OpenRound, RoundResume, WalkState

_SET_RECORD = GateRecord("review", "pass", "findings/review_0.md")
_NULL_RECORD = GateRecord("parity", "held", None)
_PASSED: tuple[Passage, ...] = (
    SkipPassage("parity", "no_parity"),
    RoundPassage("review_round", 2, "fail"),
    RoundPassage("review_round", 3, "pass"),
    LedgerPassage("lessons"),
)
_DISPATCH_SET_FIELDS = Dispatch(
    node="draft",
    agent="writer",
    prompt_variant="revise",
    counters=MappingProxyType({"rounds": 2, "drafts": 1}),
    round_number=2,
    converging=True,
    closed_round=(_SET_RECORD, _NULL_RECORD),
    passed=_PASSED,
)
_DISPATCH_NULL_FIELDS = Dispatch(
    node="review",
    agent="reviewer",
    prompt_variant=None,
    counters=MappingProxyType({}),
    round_number=None,
    converging=None,
    closed_round=(),
    passed=(),
)
_DISPATCH_FALSE = Dispatch(
    node="parity",
    agent="parity_reviewer",
    prompt_variant=None,
    counters=MappingProxyType({"rounds": 1}),
    round_number=1,
    converging=False,
    closed_round=(),
    passed=(),
)
_OPEN_ROUND = OpenRound(
    round="review_round",
    number=3,
    due=("review", "parity"),
    records=MappingProxyType({"review": _SET_RECORD, "parity": _NULL_RECORD}),
)

_ACTIONS: tuple[tuple[Awaiting, Action], ...] = (
    ("dispatch", _DISPATCH_SET_FIELDS),
    ("dispatch", _DISPATCH_NULL_FIELDS),
    (
        "set",
        DispatchSet(
            round="review_round",
            number=3,
            dispatches=(_DISPATCH_NULL_FIELDS, _DISPATCH_FALSE),
            passed=_PASSED,
        ),
    ),
    ("set", Wait("review_round", _NULL_RECORD, ("review",))),
    ("set", Wait("review_round", _SET_RECORD, ())),
    (
        "interrupt",
        Interrupt(
            binding="ask",
            node="review",
            agent="reviewer",
            resume="review",
            resume_outcome="answered",
            passed=_PASSED,
            closed_round=(_SET_RECORD,),
        ),
    ),
    ("interrupt", Interrupt("ask", "review_round", None, "review_round", "answered", ())),
    (
        "done",
        Stop(
            binding="halt",
            node="review_round",
            agent=None,
            reason="cap",
            summary=None,
            evidence=None,
            round_counts=(),
            held=(),
            closed_round=(),
            passed=(),
        ),
    ),
    (
        "done",
        Stop(
            binding="halt",
            node="review",
            agent="reviewer",
            reason="cap",
            summary="did not converge — gave up",
            evidence="review_findings",
            round_counts=("review", "parity"),
            held=(_NULL_RECORD,),
            closed_round=(_SET_RECORD,),
            passed=_PASSED,
        ),
    ),
    ("done", End("done", "finish", (("plan", "written"), ("parity", "skipped")), _PASSED)),
    ("done", End("done", "finish", (), ())),
)


def _state(awaiting: Awaiting, pending: Action, open_round: OpenRound | None) -> WalkState:
    return WalkState(
        flow="plan",
        node="review_round",
        awaiting=awaiting,
        pending=pending,
        counters=MappingProxyType({"rounds": 3}),
        round_numbers=MappingProxyType({"review_round": 3}),
        open_round=open_round,
        prompts=MappingProxyType({"draft": "revise"}),
        reports=MappingProxyType({"plan": "written"}),
        skipped=MappingProxyType({"parity": "no_parity"}),
    )


@pytest.mark.parametrize(
    ("awaiting", "pending"),
    _ACTIONS,
    ids=[f"{type(pending).__name__}-{index}" for index, (_, pending) in enumerate(_ACTIONS)],
)
@pytest.mark.parametrize("open_round", (_OPEN_ROUND, None), ids=("open-round", "no-round"))
def test_every_state_round_trips_with_no_loss(
    awaiting: Awaiting, pending: Action, open_round: OpenRound | None
) -> None:
    state = _state(awaiting, pending, open_round)
    assert state_from_json(state_to_json(state)) == state


def test_the_document_is_indented_json_with_a_trailing_newline() -> None:
    text = state_to_json(_state("done", End("done", "finish", (("plan", "written"),), ()), None))
    assert text.endswith("}\n")
    assert text.startswith('{\n "version": 2,\n "flow": "plan",\n')
    assert '"reports": [\n   [\n    "plan",\n    "written"\n   ]\n  ]' in text


def test_non_ascii_text_is_written_as_itself() -> None:
    text = state_to_json(_state("done", End("done", "fin — é", (), ()), None))
    assert '"fin — é"' in text


def test_the_decoded_state_is_immutable() -> None:
    state = state_from_json(state_to_json(_state("dispatch", _DISPATCH_SET_FIELDS, _OPEN_ROUND)))
    assert isinstance(state.counters, MappingProxyType)
    assert isinstance(state.open_round, OpenRound)
    assert isinstance(state.open_round.records, MappingProxyType)
    assert isinstance(state.open_round.due, tuple)
    assert isinstance(state.pending, Dispatch)
    assert isinstance(state.pending.counters, MappingProxyType)
    assert isinstance(state.pending.passed, tuple)


_DOCUMENT = """{
 "version": 2,
 "flow": "plan",
 "node": "review_round",
 "awaiting": "set",
 "pending": {
  "kind": "set",
  "round": "review_round",
  "number": 2,
  "dispatches": [
   {
    "kind": "dispatch",
    "node": "review",
    "agent": "reviewer",
    "prompt_variant": "second",
    "counters": {"rounds": 2},
    "round_number": 2,
    "converging": false,
    "closed_round": [{"gate": "review", "outcome": "fail", "detail": "f/review_1.md"}],
    "passed": []
   }
  ],
  "passed": [
   {"kind": "skip", "node": "parity", "status": "no_parity"},
   {"kind": "round", "round": "review_round", "number": 1, "verdict": "fail"},
   {"kind": "ledger", "entry": "lessons"}
  ]
 },
 "counters": {"rounds": 2, "drafts": 4},
 "round_numbers": {"review_round": 2},
 "open_round": {
  "round": "review_round",
  "number": 2,
  "due": ["review"],
  "records": {"review": {"gate": "review", "outcome": "pass", "detail": null}}
 },
 "prompts": {"review": "second"},
 "reports": {},
 "skipped": {"parity": "no_parity"}
}
"""


def test_a_hand_written_document_decodes_field_by_field() -> None:
    state = state_from_json(_DOCUMENT)
    assert state.flow == "plan"
    assert state.node == "review_round"
    assert state.awaiting == "set"
    assert dict(state.counters) == {"rounds": 2, "drafts": 4}
    assert list(state.counters) == ["rounds", "drafts"]
    assert dict(state.round_numbers) == {"review_round": 2}
    assert dict(state.prompts) == {"review": "second"}
    assert dict(state.reports) == {}
    assert dict(state.skipped) == {"parity": "no_parity"}

    assert state.open_round is not None
    assert state.open_round.round == "review_round"
    assert state.open_round.number == 2
    assert state.open_round.due == ("review",)
    assert dict(state.open_round.records) == {"review": GateRecord("review", "pass", None)}

    pending = state.pending
    assert isinstance(pending, DispatchSet)
    assert pending.round == "review_round"
    assert pending.number == 2
    assert pending.passed == (
        SkipPassage("parity", "no_parity"),
        RoundPassage("review_round", 1, "fail"),
        LedgerPassage("lessons"),
    )
    assert len(pending.dispatches) == 1
    dispatch = pending.dispatches[0]
    assert dispatch.node == "review"
    assert dispatch.agent == "reviewer"
    assert dispatch.prompt_variant == "second"
    assert dict(dispatch.counters) == {"rounds": 2}
    assert dispatch.round_number == 2
    assert dispatch.converging is False
    assert dispatch.closed_round == (GateRecord("review", "fail", "f/review_1.md"),)
    assert dispatch.passed == ()


def _planted(**changes: object) -> str:
    """The hand-written document with top-level keys replaced; a value of `...` drops the key."""
    document: dict[str, object] = json.loads(_DOCUMENT)
    for key, value in changes.items():
        if value is ...:
            del document[key]
        else:
            document[key] = value
    return json.dumps(document)


def _pending(**changes: object) -> dict[str, object]:
    pending: dict[str, object] = json.loads(_DOCUMENT)["pending"]
    pending.update(changes)
    return pending


_DISPATCH: dict[str, object] = json.loads(_DOCUMENT)["pending"]["dispatches"][0]


_REFUSALS: tuple[tuple[str, str, str], ...] = (
    (
        "parse-failure",
        '{"version": 2,',
        "(root): not valid JSON: Expecting property name enclosed in double quotes"
        " (line 1, column 15)",
    ),
    ("root-not-object", "[]", "(root): expected object"),
    ("version-missing", _planted(version=...), "version: missing key"),
    ("version-1", _planted(version=1), "version: unsupported version 1"),
    ("version-3", _planted(version=3), "version: unsupported version 3"),
    ("version-true", _planted(version=True), "version: unsupported version true"),
    ("version-float", _planted(version=2.0), "version: unsupported version 2.0"),
    ("missing-key", _planted(skipped=...), "skipped: missing key"),
    ("extra-key", _planted(history=[]), "history: unexpected key"),
    (
        "nested-missing-key",
        _planted(pending=_pending(passed=[{"kind": "ledger"}])),
        "pending.passed[0].entry: missing key",
    ),
    (
        "nested-extra-key",
        _planted(pending=_pending(passed=[{"kind": "ledger", "entry": "x", "at": 1}])),
        "pending.passed[0].at: unexpected key",
    ),
    ("missing-kind", _planted(pending={"round": "r"}), "pending.kind: missing key"),
    ("wrong-type-string", _planted(flow=7), "flow: expected string"),
    ("bool-is-not-int", _planted(counters={"rounds": True}), "counters.rounds: expected integer"),
    ("float-is-not-int", _planted(counters={"rounds": 2.5}), "counters.rounds: expected integer"),
    ("wrong-type-object", _planted(prompts=["second"]), "prompts: expected object"),
    ("wrong-type-array", _planted(pending=_pending(passed={})), "pending.passed: expected array"),
    (
        "wrong-type-boolean",
        _planted(pending=_pending(dispatches=[{**_DISPATCH, "converging": "no"}])),
        "pending.dispatches[0].converging: expected boolean",
    ),
    (
        "wrong-type-null-record-detail",
        _planted(
            open_round={
                "round": "review_round",
                "number": 2,
                "due": [],
                "records": {"review": {"gate": "review", "outcome": "pass", "detail": 3}},
            }
        ),
        "open_round.records.review.detail: expected string",
    ),
    (
        "report-pair-length",
        _planted(
            pending={
                "kind": "end",
                "binding": "done",
                "node": "finish",
                "reports": [["plan"]],
                "passed": [],
            }
        ),
        "pending.reports[0]: expected 2-element array",
    ),
    (
        "unknown-action-kind",
        _planted(pending=_pending(kind="refused")),
        "pending.kind: unknown kind 'refused'",
    ),
    (
        "unknown-passage-kind",
        _planted(pending=_pending(passed=[{"kind": "loop", "entry": "x"}])),
        "pending.passed[0].kind: unknown kind 'loop'",
    ),
    (
        "dispatch-kind-inside-set",
        _planted(pending=_pending(dispatches=[{"kind": "wait"}])),
        "pending.dispatches[0].kind: unknown kind 'wait'",
    ),
    (
        "awaiting-outside-literal",
        _planted(awaiting="paused"),
        "awaiting: expected one of 'dispatch', 'set', 'interrupt', 'done'",
    ),
    (
        "verdict-outside-literal",
        _planted(
            pending=_pending(
                passed=[{"kind": "round", "round": "r", "number": 1, "verdict": "held"}]
            )
        ),
        "pending.passed[0].verdict: expected one of 'pass', 'fail'",
    ),
)


@pytest.mark.parametrize(
    ("text", "message"), [(t, m) for _, t, m in _REFUSALS], ids=[i for i, _, _ in _REFUSALS]
)
def test_a_malformed_document_is_refused_naming_its_path(text: str, message: str) -> None:
    with pytest.raises(ValueError) as caught:
        state_from_json(text)
    assert str(caught.value) == message


@pytest.mark.parametrize(
    ("awaiting", "pending"),
    _ACTIONS,
    ids=[f"{type(pending).__name__}-{index}" for index, (_, pending) in enumerate(_ACTIONS)],
)
def test_the_step_document_of_an_action_is_its_pending_encoding(
    awaiting: Awaiting, pending: Action
) -> None:
    document = json.loads(state_to_json(_state(awaiting, pending, None)))
    assert step_document(pending) == document["pending"]


def test_the_step_document_of_a_refusal_carries_its_kind_first() -> None:
    document = step_document(Refused("no walk of flow 'plan' is saved"))
    assert document == {"kind": "refused", "reason": "no walk of flow 'plan' is saved"}
    assert list(document)[0] == "kind"


_RESUME = """{
 "round": "review_round",
 "number": 2,
 "records": [
  {"gate": "review", "outcome": "fail", "detail": "f/review_2.md"},
  {"gate": "parity", "outcome": "held", "detail": null}
 ]
}
"""


def test_a_hand_written_resume_document_decodes_field_by_field() -> None:
    resume = resume_from_json(_RESUME)
    assert resume == RoundResume(
        round="review_round",
        number=2,
        records=(
            GateRecord("review", "fail", "f/review_2.md"),
            GateRecord("parity", "held", None),
        ),
    )
    assert isinstance(resume.records, tuple)


def _resume(**changes: object) -> str:
    """The hand-written resume document with keys replaced; a value of `...` drops the key."""
    document: dict[str, object] = json.loads(_RESUME)
    for key, value in changes.items():
        if value is ...:
            del document[key]
        else:
            document[key] = value
    return json.dumps(document)


_RESUME_REFUSALS: tuple[tuple[str, str, str], ...] = (
    ("missing-records", _resume(records=...), "records: missing key"),
    ("extra-key", _resume(version=1), "version: unexpected key"),
    ("number-true", _resume(number=True), "number: expected integer"),
    ("number-fraction", _resume(number=1.5), "number: expected integer"),
    (
        "record-missing-detail",
        _resume(
            records=[
                {"gate": "review", "outcome": "fail", "detail": None},
                {"gate": "parity", "outcome": "held"},
            ]
        ),
        "records[1].detail: missing key",
    ),
    (
        "parse-failure",
        '{"round": "review_round",',
        "(root): not valid JSON: Expecting property name enclosed in double quotes"
        " (line 1, column 26)",
    ),
    ("root-is-array", "[]", "(root): expected object"),
)


@pytest.mark.parametrize(
    ("text", "message"),
    [(t, m) for _, t, m in _RESUME_REFUSALS],
    ids=[i for i, _, _ in _RESUME_REFUSALS],
)
def test_a_malformed_resume_document_is_refused_naming_its_path(text: str, message: str) -> None:
    with pytest.raises(ValueError) as caught:
        resume_from_json(text)
    assert str(caught.value) == message
