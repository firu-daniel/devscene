"""The rule this file exists to enforce: `render` prints a `HostStep` as `flow-walker.sh` prints
the same action — its header's `OUTPUT` grammar, key for key and in order — with the findings
files taken from `revision_findings` when non-empty and otherwise from the closed round's
records, and raises `ValueError` for the faults bash reports as exit 2.

Each `HostStep` is built by hand from `graphscene`'s public dataclasses over the harness's own
format-4 graph, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, read-only. The
values a step read from disk are given as `HostStep.printed`; the one review folder planted under
`tmp_path` disagrees with them, to show `render` reads none. Every expected text is a literal
written from `flow-walker.sh`'s `OUTPUT` grammar and `REPRO` block, never taken from the output
of the code under test.
"""

from pathlib import Path
from typing import Final

import pytest
from graphscene import (
    Dispatch,
    DispatchSet,
    End,
    FlowGraph,
    GateRecord,
    Interrupt,
    LedgerPassage,
    Refused,
    RoundPassage,
    SkipPassage,
    Stop,
    Wait,
    load_graph_file,
)

from devscene_flow_host.commands.render import render
from devscene_flow_host.host.printed_reads import PrintedReads
from devscene_flow_host.host.refusals import Refusal
from devscene_flow_host.host.round_gates import HostStep, RefusedWait
from devscene_flow_host.records.index_evidence import IndexEvidence
from round_fixtures import FAIL_BODY, plant_review

_GRAPH: Final = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.v4.graph.json"
)
_STATE_DIR: Final = "state"
_BRANCH: Final = "feat_x"
_NO_CLASS: Final = "Must Fix entry 1 lacks **Class:**"
_PLAN_HEARTBEAT: Final = (
    "heartbeat: [plan-write · iter {}] → task-plan-writer  (#<total_dispatches>)"
)
_UI_HEARTBEAT: Final = (
    "heartbeat: [ui-test-write · iter {}] → ui-tests-plan-writer  (#<total_dispatches>)"
)
_CLOSED_FAIL_ROUND: Final = (
    GateRecord("business_parity_review", "PASS", "b0.md"),
    GateRecord("architecture_review", "FAIL", "f0.md"),
    GateRecord("plan_review", "PASS", "p0.md"),
)
# `flow-walker-gates.sh` → REPRO's `i.md`, as `fw_index_evidence` reads it.
_REPRO_EVIDENCE: Final = IndexEvidence(True, ("- **5** (rejected round 2) — r",), True)
_SHOWN_INDEX: Final = "state/story_plans/feat_x_story_plan.md"


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _render(step: HostStep, repo_root: Path) -> str:
    return render(step, graph=_graph(), repo_root=repo_root, state_dir=_STATE_DIR, branch=_BRANCH)


def _text(*lines: str) -> str:
    return "".join(line + "\n" for line in lines)


def _plan_writer(
    prompt: str | None,
    iteration: int,
    round_number: int,
    closed_round: tuple[GateRecord, ...] = (),
    passed: tuple[SkipPassage | RoundPassage | LedgerPassage, ...] = (),
) -> Dispatch:
    return Dispatch(
        node="plan_writer",
        agent="task-plan-writer",
        prompt=prompt,
        counters={"iteration": iteration},
        round_number=round_number,
        converging=None,
        closed_round=closed_round,
        passed=passed,
    )


def _gate(node: str, agent: str, iteration: int, round_number: int, converging: bool) -> Dispatch:
    return Dispatch(
        node=node,
        agent=agent,
        prompt=None,
        counters={"iteration": iteration},
        round_number=round_number,
        converging=converging,
        closed_round=(),
        passed=(),
    )


def _gates(iteration: int, round_number: int, converging: bool) -> tuple[Dispatch, ...]:
    return (
        _gate(
            "business_parity_review",
            "business-parity-reviewer",
            iteration,
            round_number,
            converging,
        ),
        _gate("architecture_review", "architecture-reviewer", iteration, round_number, converging),
        _gate("plan_review", "task-plan-reviewer", iteration, round_number, converging),
    )


def _gate_block(
    node: str,
    agent: str,
    tag: str,
    iteration: int,
    round_number: int,
    mode: str,
    *carried: str,
) -> tuple[str, ...]:
    return (
        "action: dispatch",
        f"node: {node}",
        f"agent: {agent}",
        f"arg.iteration: {round_number}",
        f"arg.review_mode: {mode}",
        *carried,
        f"heartbeat: [plan-write{tag} · iter {iteration}] → {agent}  (#<total_dispatches>)",
    )


def test_the_writers_initial_dispatch_carries_the_round_it_feeds(tmp_path: Path) -> None:
    step = HostStep(_plan_writer(None, 0, 0))
    assert _render(step, tmp_path) == _text(
        "action: dispatch",
        "node: plan_writer",
        "agent: task-plan-writer",
        "prompt: initial",
        "arg.iteration: 0",
        _PLAN_HEARTBEAT.format(0),
    )


def test_a_revision_after_a_fail_round_carries_the_closed_rounds_files(tmp_path: Path) -> None:
    dispatch = _plan_writer(
        "revision", 1, 1, _CLOSED_FAIL_ROUND, (RoundPassage("plan_round", 0, "fail"),)
    )
    assert _render(HostStep(dispatch), tmp_path) == _text(
        "action: dispatch",
        "node: plan_writer",
        "agent: task-plan-writer",
        "prompt: revision",
        "arg.iteration: 1",
        "arg.findings_file: b0.md",
        "arg.findings_file: f0.md",
        "arg.findings_file: p0.md",
        "round: 0 FAIL",
        _PLAN_HEARTBEAT.format(1),
    )


def test_the_three_gate_set_is_three_full_blocks_back_to_back(tmp_path: Path) -> None:
    step = HostStep(DispatchSet("plan_round", 0, _gates(0, 0, False), ()))
    assert _render(step, tmp_path) == _text(
        *_gate_block(
            "business_parity_review", "business-parity-reviewer", " · parity", 0, 0, "full"
        ),
        *_gate_block("architecture_review", "architecture-reviewer", " · arch", 0, 0, "full"),
        *_gate_block("plan_review", "task-plan-reviewer", "", 0, 0, "full"),
    )


def test_the_sets_passed_lines_go_in_the_first_block_only(tmp_path: Path) -> None:
    passed = (RoundPassage("plan_round", 1, "fail"), LedgerPassage("P0"))
    step = HostStep(DispatchSet("plan_round", 2, _gates(2, 2, True), passed))
    assert _render(step, tmp_path) == _text(
        *_gate_block(
            "business_parity_review",
            "business-parity-reviewer",
            " · parity",
            2,
            2,
            "converging",
            "round: 1 FAIL",
            "ledger: P0",
        ),
        *_gate_block("architecture_review", "architecture-reviewer", " · arch", 2, 2, "converging"),
        *_gate_block("plan_review", "task-plan-reviewer", "", 2, 2, "converging"),
    )


def test_a_skipped_gates_line_leads_the_first_block_of_the_set(tmp_path: Path) -> None:
    gates = _gates(0, 0, False)[1:]
    passed = (SkipPassage("business_parity_review", "passed-by-exclusion"),)
    step = HostStep(DispatchSet("plan_round", 0, gates, passed))
    assert _render(step, tmp_path) == _text(
        *_gate_block(
            "architecture_review",
            "architecture-reviewer",
            " · arch",
            0,
            0,
            "full",
            "skip: business_parity_review passed-by-exclusion",
        ),
        *_gate_block("plan_review", "task-plan-reviewer", "", 0, 0, "full"),
    )


def test_a_re_dispatched_set_carries_its_refused_line(tmp_path: Path) -> None:
    gate = _gate("plan_review", "task-plan-reviewer", 0, 0, False)
    step = HostStep(
        DispatchSet("plan_round", 0, (gate,), ()), (Refusal("plan_review", 1, _NO_CLASS),)
    )
    assert _render(step, tmp_path) == _text(
        *_gate_block(
            "plan_review",
            "task-plan-reviewer",
            "",
            0,
            0,
            "full",
            f"refused: plan_review attempt 1 of 3: {_NO_CLASS}",
        ),
    )


def test_a_wait_names_the_recorded_gate_and_the_gates_out(tmp_path: Path) -> None:
    step = HostStep(
        Wait(
            "plan_round",
            GateRecord("plan_review", "PASS", "p0.md"),
            ("business_parity_review", "architecture_review"),
        )
    )
    assert _render(step, tmp_path) == _text(
        "action: wait",
        "node: plan_round",
        "recorded: plan_review PASS",
        "pending: business_parity_review",
        "pending: architecture_review",
    )


def test_a_refused_wait_puts_its_refused_line_where_recorded_stands(tmp_path: Path) -> None:
    step = HostStep(
        RefusedWait(
            "plan_round",
            Refusal("plan_review", 1, _NO_CLASS),
            ("business_parity_review", "architecture_review"),
        )
    )
    assert _render(step, tmp_path) == _text(
        "action: wait",
        "node: plan_round",
        f"refused: plan_review attempt 1 of 3: {_NO_CLASS}",
        "pending: business_parity_review",
        "pending: architecture_review",
    )


def test_a_ui_writer_revision_carries_the_kept_findings_file(tmp_path: Path) -> None:
    dispatch = Dispatch(
        node="ui_writer",
        agent="ui-tests-plan-writer",
        prompt="revision",
        counters={"iteration": 1},
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )
    kept = "state/ui_test_plan_reviews/feat_x/review_0.md"
    assert _render(HostStep(dispatch, revision_findings=(kept,)), tmp_path) == _text(
        "action: dispatch",
        "node: ui_writer",
        "agent: ui-tests-plan-writer",
        "prompt: revision",
        f"arg.findings_file: {kept}",
        _UI_HEARTBEAT.format(1),
    )


_UI_REVIEW: Final = Dispatch(
    node="ui_review",
    agent="ui-tests-plan-reviewer",
    prompt=None,
    counters={"iteration": 1},
    round_number=None,
    converging=None,
    closed_round=(),
    passed=(),
)
_UI_REVIEW_TEXT: Final = (
    "action: dispatch",
    "node: ui_review",
    "agent: ui-tests-plan-reviewer",
    "arg.iteration: 1",
    "heartbeat: [ui-test-write · iter 1] → ui-tests-plan-reviewer  (#<total_dispatches>)",
)


def test_a_non_round_reviewer_prints_its_printed_iteration(tmp_path: Path) -> None:
    step = HostStep(_UI_REVIEW, printed=PrintedReads(review_iterations=(("ui_review", 1),)))
    assert _render(step, tmp_path) == _text(*_UI_REVIEW_TEXT)


def test_a_folder_that_disagrees_with_the_printed_iteration_is_not_read(tmp_path: Path) -> None:
    folder = tmp_path / _STATE_DIR / "ui_test_plan_reviews" / _BRANCH
    for n in range(3):
        plant_review(folder, n, FAIL_BODY)
    step = HostStep(_UI_REVIEW, printed=PrintedReads(review_iterations=(("ui_review", 1),)))
    assert _render(step, tmp_path) == _text(*_UI_REVIEW_TEXT)


def test_the_ask_interrupt_names_where_it_resumes(tmp_path: Path) -> None:
    step = HostStep(
        Interrupt("<ask>", "plan_writer", "task-plan-writer", "plan_writer", "answered", ())
    )
    assert _render(step, tmp_path) == _text(
        "action: binding",
        "binding: <ask>",
        "node: plan_writer",
        "agent: task-plan-writer",
        "resume: plan_writer",
    )


def test_a_join_held_by_refusal_escalates_with_its_held_and_refused_lines(
    tmp_path: Path,
) -> None:
    stop = Stop(
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
    )
    step = HostStep(stop, (Refusal("plan_review", 3, _NO_CLASS),))
    assert _render(step, tmp_path) == _text(
        "action: binding",
        "binding: <escalate>",
        "node: plan_review",
        "agent: task-plan-reviewer",
        "reason: error",
        "held: plan_review error",
        f"refused: plan_review attempt 3 of 3: {_NO_CLASS}",
    )


def _cap(
    round_counts: tuple[str, ...], summary: str | None, closed_round: tuple[GateRecord, ...]
) -> Stop:
    return Stop(
        binding="<escalate>",
        node="plan_round",
        agent=None,
        reason="cap",
        summary=summary,
        evidence="story_index",
        round_counts=round_counts,
        held=(),
        closed_round=closed_round,
        passed=(),
    )


def test_the_plan_round_cap_carries_files_counts_evidence_and_summary(tmp_path: Path) -> None:
    summary = "the plan loop reached its 5-revision cap; the gates open when it fired: arch"
    stop = _cap(
        ("business_parity_review", "architecture_review", "plan_review"),
        summary,
        (
            GateRecord("business_parity_review", "PASS", "b4.md"),
            GateRecord("architecture_review", "FAIL", "f4.md"),
            GateRecord("plan_review", "PASS", "p4.md"),
        ),
    )
    printed = PrintedReads(
        round_counts=(
            ("business_parity_review", 0),
            ("architecture_review", 5),
            ("plan_review", 1),
        ),
        index_evidence=_REPRO_EVIDENCE,
    )
    shown = f"{tmp_path}/{_SHOWN_INDEX}"
    assert _render(HostStep(stop, printed=printed), tmp_path) == _text(
        "action: binding",
        "binding: <escalate>",
        "node: plan_round",
        "reason: cap",
        "findings_file: b4.md",
        "findings_file: f4.md",
        "findings_file: p4.md",
        "rounds: business_parity_review 0",
        "rounds: architecture_review 5",
        "rounds: plan_review 1",
        f"evidence: {shown} ## Rejected findings",
        "evidence.open: - **5** (rejected round 2) — r",
        f"evidence: {shown} ## Scope register",
        f"summary: {summary}",
    )


def test_a_cap_count_missing_from_the_printed_reads_is_a_fault(tmp_path: Path) -> None:
    stop = _cap(("architecture_review",), None, ())
    with pytest.raises(ValueError) as raised:
        _render(HostStep(stop), tmp_path)
    assert str(raised.value) == "the printed reads carry no count for 'architecture_review'"


def test_a_repeated_rejected_findings_heading_prints_one_evidence_line(tmp_path: Path) -> None:
    # `flow-walker-gates.sh` → `fw_index_evidence` prints the heading's `evidence:` line only
    # `if (!rj)`, at the first heading, and every open entry under any such heading after it.
    evidence = IndexEvidence(
        True, ("- **5** (rejected round 2) — r", "- **7** (rejected round 3) — r"), True
    )
    step = HostStep(_cap((), None, ()), printed=PrintedReads(index_evidence=evidence))
    shown = f"{tmp_path}/{_SHOWN_INDEX}"
    assert _render(step, tmp_path) == _text(
        "action: binding",
        "binding: <escalate>",
        "node: plan_round",
        "reason: cap",
        f"evidence: {shown} ## Rejected findings",
        "evidence.open: - **5** (rejected round 2) — r",
        "evidence.open: - **7** (rejected round 3) — r",
        f"evidence: {shown} ## Scope register",
    )


def test_the_ui_review_cap_carries_the_kept_file_and_no_rounds_line(tmp_path: Path) -> None:
    summary = "5 UI-test-plan-review iterations did not converge"
    stop = Stop(
        binding="<escalate>",
        node="ui_review",
        agent="ui-tests-plan-reviewer",
        reason="cap",
        summary=summary,
        evidence="ui_test_index",
        round_counts=(),
        held=(),
        closed_round=(),
        passed=(),
    )
    kept = "state/ui_test_plan_reviews/feat_x/review_4.md"
    assert _render(HostStep(stop, revision_findings=(kept,)), tmp_path) == _text(
        "action: binding",
        "binding: <escalate>",
        "node: ui_review",
        "agent: ui-tests-plan-reviewer",
        "reason: cap",
        f"findings_file: {kept}",
        f"summary: {summary}",
    )


def test_the_terminal_handoff_carries_its_report_lines(tmp_path: Path) -> None:
    end = End(
        "<terminal_handoff>",
        "convergence",
        (
            ("business_parity_review", "passed"),
            ("architecture_review", "passed"),
            ("plan_review", "passed"),
            ("ui_test", "passed"),
        ),
        (LedgerPassage("P2"),),
    )
    assert _render(HostStep(end), tmp_path) == _text(
        "action: binding",
        "binding: <terminal_handoff>",
        "node: convergence",
        "report: business_parity_review passed",
        "report: architecture_review passed",
        "report: plan_review passed",
        "report: ui_test passed",
        "ledger: P2",
    )


def test_an_unknown_prompt_variant_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        _render(HostStep(_plan_writer("draft", 0, 0)), tmp_path)
    assert str(raised.value) == "graph gives 'plan_writer' the unknown prompt variant 'draft'"


def test_a_revision_with_no_findings_file_is_a_fault(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        _render(HostStep(_plan_writer("revision", 1, 1)), tmp_path)
    assert str(raised.value) == (
        "a revision of 'plan_writer' is due and no findings file is recorded"
    )


def test_an_action_with_no_rendering_is_refused_by_type(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as raised:
        _render(HostStep(Refused("x")), tmp_path)
    assert str(raised.value) == "no rendering for the action type Refused"
