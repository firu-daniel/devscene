"""The rule this file exists to enforce: `record_outcome` records a gate's outcome under
`flow-walker.sh`'s reviewer-file rules on the harness's own format-4 graph,
`cli/templates/scripts/flows/task_plan_writing.v4.graph.json` — a verdict needs a findings file,
a round gate's file must pass the round-file check, a refused file records nothing and its gate
is re-dispatched in the same round once no other gate is out, and the third refusal holds it as
`error` — and that a refusal below the cap never reaches GraphScene's saved walk.

It also enforces that a findings file given outside an open set — a non-round reviewer's `FAIL`,
or `answered` — is kept as `flow-walker.sh` → `next` keeps `revision_findings`, that a closing
round clears it as `close_round` overwrites that key, and that a held outcome at a gate of an
open set keeps nothing.

It pins the host's held-gate order, chosen over bash's in #472: a held gate whose only siblings
out are refused ones waits while they are re-dispatched in the same round, and escalates at the
round's next join.

Records and review files are planted under `tmp_path`. Every expected value is a literal written
from `flow-walker.sh` → `A REFUSED ROUND FILE`, its `REPRO` block's refused-file walk and its
`revision_findings` writers, and, for the held-gate cases, from `host/round_gates.py` →
*"The rule:"* and `flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar ("node: and agent: are the
first held gate's in `gates` order, reason: its outcome, then held: <gate> <outcome> per held
gate, one refused: line per gate held by refusal"), never taken from the output of the code under
test.
"""

import json
import threading
from pathlib import Path
from typing import Final

from graphscene import (
    Dispatch,
    DispatchSet,
    GateRecord,
    Interrupt,
    LedgerPassage,
    Refused,
    RoundPassage,
    Stop,
    Wait,
    Walker,
    load_graph_file,
)

from devscene_flow_host.host.refusals import Refusal, refusals_path
from devscene_flow_host.host.revision_findings import revision_findings_path
from devscene_flow_host.host.round_gates import HostStep, RefusedWait, record_outcome
from devscene_flow_host.host.store import walk_state_path
from devscene_flow_host.host.walking import open_walker
from round_fixtures import FAIL_BODY, PASS_BODY, plant_review

_GRAPH: Final = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.v4.graph.json"
)
_BRANCH: Final = "feat_x"
_PARITY: Final = "state/business_parity_reviews/feat_x"
_ARCH: Final = "state/architecture_reviews/feat_x"
_PLAN: Final = "state/task_plan_reviews/feat_x"
_UI: Final = "state/ui_test_plan_reviews/feat_x"
# `flow-walker.sh` → REPRO's `bad.md`.
_NO_CLASS_BODY: Final = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Failure:** x\n"
_NO_CLASS: Final = "Must Fix entry 1 lacks **Class:**"
_PASS_WITH_ENTRY_BODY: Final = (
    "verdict: PASS\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"
)


def _gate_dispatch(node: str, agent: str) -> Dispatch:
    """A round-0 gate's block: `arg.iteration: 0`, `arg.review_mode: full`."""
    return Dispatch(
        node=node,
        agent=agent,
        prompt=None,
        counters={"iteration": 0},
        round_number=0,
        converging=False,
        closed_round=(),
        passed=(),
    )


_PARITY_DISPATCH: Final = _gate_dispatch("business_parity_review", "business-parity-reviewer")
_ARCH_DISPATCH: Final = _gate_dispatch("architecture_review", "architecture-reviewer")
_PLAN_DISPATCH: Final = _gate_dispatch("plan_review", "task-plan-reviewer")


def _started(root: Path) -> Walker:
    """A walk of `feat_x` with every phase on, `start`ed at `plan_writer`."""
    (root / "devscene.config.json").write_text(
        json.dumps(
            {"defaultBranch": "main", "stateDir": "state", "phases": {"parity": True, "qa": True}}
        ),
        encoding="utf-8",
    )
    walker = open_walker(root, _BRANCH, load_graph_file(_GRAPH), skipped="none")
    walker.start()
    return walker


def _walker(root: Path) -> Walker:
    """A walk of `feat_x` with every phase on, `start`ed and `returned` into round 0's set."""
    walker = _started(root)
    assert walker.next("returned") == DispatchSet(
        "plan_round", 0, (_PARITY_DISPATCH, _ARCH_DISPATCH, _PLAN_DISPATCH), ()
    )
    return walker


def _file(root: Path, folder: str, body: str) -> str:
    plant_review(root / folder, 0, body)
    return f"{folder}/review_0.md"


def _record(
    walker: Walker,
    root: Path,
    outcome: str,
    node: str | None = None,
    findings: str | None = None,
) -> HostStep:
    return record_outcome(walker, root, _BRANCH, outcome, node=node, findings=findings)


def _refusal_file(root: Path) -> Path:
    return refusals_path(root, "state", _BRANCH)


def test_fail_without_findings_is_refused(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    assert _record(walker, tmp_path, "FAIL", "plan_review") == HostStep(
        Refused("outcome FAIL requires --findings with the reviewer's findings_file")
    )


def test_pass_at_a_round_gate_without_findings_is_refused(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    assert _record(walker, tmp_path, "PASS", "plan_review") == HostStep(
        Refused(
            "outcome PASS at round gate 'plan_review' requires --findings with the reviewer's "
            "findings_file"
        )
    )


def test_a_valid_file_is_recorded_as_a_wait(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    plan = _file(tmp_path, _PLAN, PASS_BODY)
    assert _record(walker, tmp_path, "PASS", "plan_review", plan) == HostStep(
        Wait(
            "plan_round",
            GateRecord("plan_review", "PASS", "state/task_plan_reviews/feat_x/review_0.md"),
            ("business_parity_review", "architecture_review"),
        )
    )


def test_a_refused_file_waits_for_its_siblings_then_is_dispatched_alone(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)
    walk = walk_state_path(tmp_path, "state", _BRANCH)
    before = walk.read_bytes()

    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        RefusedWait(
            "plan_round",
            Refusal("plan_review", 1, _NO_CLASS),
            ("business_parity_review", "architecture_review"),
        )
    )
    assert walk.read_bytes() == before

    parity = _file(tmp_path, _PARITY, PASS_BODY)
    assert _record(walker, tmp_path, "PASS", "business_parity_review", parity) == HostStep(
        Wait(
            "plan_round",
            GateRecord(
                "business_parity_review", "PASS", "state/business_parity_reviews/feat_x/review_0.md"
            ),
            ("architecture_review",),
        )
    )
    arch = _file(tmp_path, _ARCH, PASS_BODY)
    assert _record(walker, tmp_path, "PASS", "architecture_review", arch) == HostStep(
        DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()),
        (Refusal("plan_review", 1, _NO_CLASS),),
    )

    failed = _file(tmp_path, "state/fail", FAIL_BODY)
    step = _record(walker, tmp_path, "FAIL", "plan_review", failed)
    assert isinstance(step.action, Dispatch), step
    assert (step.action.node, step.action.prompt, step.action.round_number) == (
        "plan_writer",
        "revision",
        1,
    )
    assert step.action.passed == (RoundPassage("plan_round", 0, "fail"),)
    assert step.refusals == ()
    assert not _refusal_file(tmp_path).exists()


def test_two_refused_gates_return_as_one_set(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)

    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        RefusedWait(
            "plan_round",
            Refusal("plan_review", 1, _NO_CLASS),
            ("business_parity_review", "architecture_review"),
        )
    )
    assert _record(walker, tmp_path, "FAIL", "architecture_review", bad) == HostStep(
        RefusedWait(
            "plan_round",
            Refusal("architecture_review", 1, _NO_CLASS),
            ("business_parity_review",),
        )
    )
    parity = _file(tmp_path, _PARITY, PASS_BODY)
    assert _record(walker, tmp_path, "PASS", "business_parity_review", parity) == HostStep(
        DispatchSet("plan_round", 0, (_ARCH_DISPATCH, _PLAN_DISPATCH), ()),
        (
            Refusal("architecture_review", 1, _NO_CLASS),
            Refusal("plan_review", 1, _NO_CLASS),
        ),
    )


def test_the_third_refusal_holds_the_gate_as_error(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)
    _record(walker, tmp_path, "FAIL", "plan_review", bad)
    _record(walker, tmp_path, "PASS", "business_parity_review", _file(tmp_path, _PARITY, PASS_BODY))
    _record(walker, tmp_path, "PASS", "architecture_review", _file(tmp_path, _ARCH, PASS_BODY))

    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()),
        (Refusal("plan_review", 2, _NO_CLASS),),
    )
    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        Stop(
            binding="<escalate>",
            node="plan_review",
            agent="task-plan-reviewer",
            reason="error",
            summary=None,
            evidence=None,
            round_counts=(),
            held=(GateRecord("plan_review", "error", None),),
            closed_round=(),
            passed=(),
        ),
        (Refusal("plan_review", 3, _NO_CLASS),),
    )


def test_a_pass_file_carrying_a_must_fix_entry_is_refused(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    plan = _file(tmp_path, _PLAN, _PASS_WITH_ENTRY_BODY)
    assert _record(walker, tmp_path, "PASS", "plan_review", plan) == HostStep(
        RefusedWait(
            "plan_round",
            Refusal("plan_review", 1, "verdict: PASS with a numbered entry under ## Must Fix"),
            ("business_parity_review", "architecture_review"),
        )
    )


def test_a_held_error_beside_a_refused_gate_re_dispatches_first(tmp_path: Path) -> None:
    """The held `architecture_review` waits while the refused `plan_review` is re-dispatched,
    and escalates at the round's next join. Bash would escalate it at once."""
    walker = _walker(tmp_path)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)
    _record(walker, tmp_path, "FAIL", "plan_review", bad)
    _record(walker, tmp_path, "PASS", "business_parity_review", _file(tmp_path, _PARITY, PASS_BODY))

    assert _record(walker, tmp_path, "error", "architecture_review") == HostStep(
        DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()),
        (Refusal("plan_review", 1, _NO_CLASS),),
    )
    plan = _file(tmp_path, "state/pass", PASS_BODY)
    assert _record(walker, tmp_path, "PASS", "plan_review", plan) == HostStep(
        Stop(
            binding="<escalate>",
            node="architecture_review",
            agent="architecture-reviewer",
            reason="error",
            summary=None,
            evidence=None,
            round_counts=(),
            held=(GateRecord("architecture_review", "error", None),),
            closed_round=(),
            passed=(),
        )
    )
    assert not _refusal_file(tmp_path).exists()


def test_a_held_error_waits_while_its_refused_sibling_is_refused_again(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)
    _record(walker, tmp_path, "FAIL", "plan_review", bad)
    _record(walker, tmp_path, "PASS", "business_parity_review", _file(tmp_path, _PARITY, PASS_BODY))

    assert _record(walker, tmp_path, "error", "architecture_review") == HostStep(
        DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()),
        (Refusal("plan_review", 1, _NO_CLASS),),
    )
    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()),
        (Refusal("plan_review", 2, _NO_CLASS),),
    )
    assert _record(walker, tmp_path, "FAIL", "plan_review", bad) == HostStep(
        Stop(
            binding="<escalate>",
            node="architecture_review",
            agent="architecture-reviewer",
            reason="error",
            summary=None,
            evidence=None,
            round_counts=(),
            held=(
                GateRecord("architecture_review", "error", None),
                GateRecord("plan_review", "error", None),
            ),
            closed_round=(),
            passed=(),
        ),
        (Refusal("plan_review", 3, _NO_CLASS),),
    )


def test_two_threads_recording_two_gates_join_exactly_once(tmp_path: Path) -> None:
    _walker(tmp_path)
    graph = load_graph_file(_GRAPH)
    bad = _file(tmp_path, _PLAN, _NO_CLASS_BODY)
    first = open_walker(tmp_path, _BRANCH, graph, skipped="none")
    _record(first, tmp_path, "FAIL", "plan_review", bad)
    plan = _file(tmp_path, "state/pass", PASS_BODY)
    assert _record(first, tmp_path, "PASS", "plan_review", plan) == HostStep(
        Wait(
            "plan_round",
            GateRecord("plan_review", "PASS", "state/pass/review_0.md"),
            ("business_parity_review", "architecture_review"),
        )
    )

    calls = (
        ("business_parity_review", _file(tmp_path, _PARITY, PASS_BODY)),
        ("architecture_review", _file(tmp_path, _ARCH, PASS_BODY)),
    )
    barrier = threading.Barrier(len(calls))
    results: list[HostStep] = []
    errors: list[BaseException] = []

    def record(gate: str, findings: str) -> None:
        try:
            walker = open_walker(tmp_path, _BRANCH, graph, skipped="none")
            barrier.wait()
            results.append(_record(walker, tmp_path, "PASS", gate, findings))
        except BaseException as error:
            errors.append(error)

    threads = [threading.Thread(target=record, args=call) for call in calls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert errors == []
    joins = [step.action for step in results if isinstance(step.action, Dispatch)]
    waits = [step.action for step in results if isinstance(step.action, Wait)]
    assert len(joins) == 1 and len(waits) == 1, results
    assert joins[0].node == "ui_writer"
    assert joins[0].passed == (RoundPassage("plan_round", 0, "pass"), LedgerPassage("P1"))
    assert not _refusal_file(tmp_path).exists()


def _kept_file(root: Path) -> Path:
    return revision_findings_path(root, "state", _BRANCH)


def _at_ui_review(walker: Walker, root: Path) -> None:
    for gate, folder in (
        ("business_parity_review", _PARITY),
        ("architecture_review", _ARCH),
        ("plan_review", _PLAN),
    ):
        _record(walker, root, "PASS", gate, _file(root, folder, PASS_BODY))
    ui_review = _record(walker, root, "returned")
    assert isinstance(ui_review.action, Dispatch), ui_review
    assert ui_review.action.node == "ui_review"


def test_a_non_round_reviewers_findings_file_is_kept_for_the_revision(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    _at_ui_review(walker, tmp_path)

    assert _record(walker, tmp_path, "FAIL", "ui_review") == HostStep(
        Refused("outcome FAIL requires --findings with the reviewer's findings_file")
    )
    assert not _kept_file(tmp_path).exists()
    findings = _file(tmp_path, _UI, FAIL_BODY)
    assert _record(walker, tmp_path, "FAIL", "ui_review", findings) == HostStep(
        Dispatch(
            node="ui_writer",
            agent="ui-tests-plan-writer",
            prompt="revision",
            counters={"iteration": 1},
            round_number=None,
            converging=None,
            closed_round=(),
            passed=(),
        ),
        revision_findings=("state/ui_test_plan_reviews/feat_x/review_0.md",),
    )
    # An outcome given no findings file leaves the record as it was.
    step = _record(walker, tmp_path, "returned")
    assert isinstance(step.action, Dispatch), step
    assert step.action.node == "ui_review"
    assert step.revision_findings == ("state/ui_test_plan_reviews/feat_x/review_0.md",)
    assert not _refusal_file(tmp_path).exists()


def test_a_findings_file_given_with_answered_is_kept(tmp_path: Path) -> None:
    walker = _started(tmp_path)
    asked = _record(walker, tmp_path, "questions")
    assert isinstance(asked.action, Interrupt), asked
    assert asked.revision_findings == ()

    step = _record(walker, tmp_path, "answered", findings="state/answers.md")
    assert isinstance(step.action, Dispatch), step
    assert step.action.node == "plan_writer"
    assert step.revision_findings == ("state/answers.md",)


def test_a_closing_round_clears_an_earlier_kept_file(tmp_path: Path) -> None:
    walker = _started(tmp_path)
    _record(walker, tmp_path, "questions")
    _record(walker, tmp_path, "answered", findings="state/answers.md")
    assert _record(walker, tmp_path, "returned") == HostStep(
        DispatchSet("plan_round", 0, (_PARITY_DISPATCH, _ARCH_DISPATCH, _PLAN_DISPATCH), ()),
        revision_findings=("state/answers.md",),
    )

    for gate, folder in (("business_parity_review", _PARITY), ("architecture_review", _ARCH)):
        waited = _record(walker, tmp_path, "FAIL", gate, _file(tmp_path, folder, FAIL_BODY))
        assert isinstance(waited.action, Wait), waited
        assert waited.revision_findings == ("state/answers.md",)
    step = _record(walker, tmp_path, "FAIL", "plan_review", _file(tmp_path, _PLAN, FAIL_BODY))
    assert isinstance(step.action, Dispatch), step
    assert (step.action.node, step.action.prompt) == ("plan_writer", "revision")
    assert step.action.passed == (RoundPassage("plan_round", 0, "fail"),)
    assert step.revision_findings == ()
    assert not _kept_file(tmp_path).exists()


def test_a_held_outcome_at_a_gate_of_an_open_set_keeps_nothing(tmp_path: Path) -> None:
    walker = _walker(tmp_path)
    assert _record(
        walker, tmp_path, "error", "plan_review", "state/task_plan_reviews/feat_x/review_0.md"
    ) == HostStep(
        Wait(
            "plan_round",
            GateRecord("plan_review", "error", None),
            ("business_parity_review", "architecture_review"),
        )
    )
    assert not _kept_file(tmp_path).exists()
