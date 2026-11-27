"""The rule this file exists to enforce: `act_on_exit` acts on each `RunExit` as the retired bash
driver did — an `End` narrates the Done summary in `pd_handoff`'s order, its `ui_test:` line
falling back to the ledger, the `qa` phase and the UI-test index when the `End` carries no
`ui_test` report, and its `📌 Run mode:` line as `pd_run_mode_line` formatted it; STOP, the cap and
the kill switch narrate their exact halt text; a pause or an undelivered halt makes the
`plan-round-partial` commit for the known round, or narrates that none is known, then writes the
pause files; `<ask>`, `<escalate>` and a `Refused` each write their exact clarification file, the
escalation committing the partial first only when it holds gates; and `QUESTION_NODES` is every
node of the planning graph with an outcome bound to `<ask>`.

Every exit is built by hand from GraphScene's public types; the graph is
`cli/templates/scripts/flows/task_plan_writing.graph.json`, read-only; the commit wrapper is a fake
planted under `tmp_path` logging its arguments from `--artifact` to before `--push`; every
configuration and ledger is planted under `tmp_path`; `Observations` and the narration are
recording stand-ins. Every expected value is a literal written from the task plan's contract and
the retired bash text, never taken from the code under test.

Deliberately not covered:
- The convergence commits and the `P3` flip: `tests/test_planning_hooks.py`.
- Exit statuses, the stdout line and the observation flush: `tests/test_planning_driver_command.py`.
"""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from graphscene import (
    BindingEdge,
    Completed,
    End,
    Failed,
    FlowGraph,
    GateRecord,
    Halt,
    Interrupt,
    Launch,
    NodeResult,
    Refused,
    RunExit,
    SkipPassage,
    Stop,
    load_graph_file,
)

from devscene_flow_host.host.claude_executor import SessionUsage
from devscene_flow_host.host.node_sessions import NodeSessions
from devscene_flow_host.host.observations import Observations
from devscene_flow_host.host.planning_run import PlanningKind, PlanningOutcome
from devscene_flow_host.host.run_exits import (
    QUESTION_NODES,
    QUESTIONS_FIELD,
    REASON_FIELD,
    RETURN_FIELD_READS,
    TASKS_COUNT_FIELD,
    TESTS_COUNT_FIELD,
    StopKind,
    act_on_exit,
)

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_BRANCH = "feat_x"
_NOW = datetime(2026, 11, 27, 10, 0, 0, tzinfo=UTC)
_LEDGER = (
    "# Flow progress\n"
    "\n"
    "## Run mode\n"
    "{run_mode}"
    "\n"
    "## Planning\n"
    "- [x] P1. Task plan converged\n"
    "- [{p2}] P2. UI-test plan converged\n"
    "- [x] P3. Planning committed\n"
)
_CONTINUE = (
    "\n## Q1 — How should planning continue?\n\n"
    "The walker ended this walk at the escalation above and routes nowhere past it.\n"
)


class _RecordingObservations(Observations):
    def __init__(self) -> None:
        super().__init__()
        self.added: list[tuple[str, str, str, str]] = []

    def add(self, category: str, problem: str, evidence: str, cost: str) -> None:
        self.added.append((category, problem, evidence, cost))


class _Run:
    def __init__(
        self, tmp_path: Path, *, p2: str = "x", qa: bool = False, run_mode: str = ""
    ) -> None:
        self.root = tmp_path / "repo"
        self.root.mkdir(parents=True)
        (self.root / "devscene.config.json").write_text(
            json.dumps(
                {
                    "defaultBranch": "main",
                    "stateDir": "state",
                    "scriptsDir": "bin",
                    "phases": {"qa": qa},
                }
            ),
            encoding="utf-8",
        )
        ledger = self.root / "state" / "flow_progress" / "feat_x_progress.md"
        ledger.parent.mkdir(parents=True)
        ledger.write_text(
            _LEDGER.format(run_mode=run_mode or "- skipped: none\n", p2=p2), encoding="utf-8"
        )
        self.wrapper = self.root / "bin" / "commit-on-branch.sh"
        self.wrapper.parent.mkdir()
        self.wrapper.write_text(
            "#!/usr/bin/env bash\n"
            'here="$(cd "$(dirname "$0")" && pwd -P)"\n'
            'args=("$@")\n'
            'printf \'%s\\n\' "${args[*]:2:$(($# - 3))}" >>"$here/calls.log"\n'
            "exit 0\n",
            encoding="utf-8",
        )
        self.wrapper.chmod(0o755)
        self.graph: FlowGraph = load_graph_file(_GRAPH)
        self.observations = _RecordingObservations()
        self.narrated: list[str] = []
        self.sessions = NodeSessions(
            log_path=tmp_path / "planning.log",
            formatter="true",
            observations=Observations(),
            narrate=lambda _line: None,
        )

    def session(
        self, node: str, result: NodeResult, document: dict[str, object] | None = None
    ) -> None:
        self.sessions.record(
            SessionUsage(
                node=node,
                agent=f"{node}-agent",
                agent_prompt="",
                session_id=None,
                started_at=_NOW,
                duration_seconds=1.0,
                stalled=False,
                total_cost_usd=None,
                cache_creation_input_tokens=None,
                cache_read_input_tokens=None,
                model_usage={},
                permission_denials=0,
                withheld_tools=(),
                stream="",
                stderr_tail="",
                returncode=0,
                return_document=document,
                result=result,
            )
        )
        self.sessions.record(Launch(1, node, f"{node}-agent", 1, 3, result))

    def act(
        self,
        exit_: RunExit | None,
        *,
        kind: PlanningKind = "run",
        last_round: int | None = None,
        pending_round: int | None = None,
        pending_nodes: tuple[str, ...] = (),
        dispatched_round: int | None = None,
        dispatch_cap: int | None = None,
    ) -> StopKind:
        outcome = PlanningOutcome(
            kind,
            exit=exit_,
            last_round=last_round,
            pending_round=pending_round,
            sessions=self.sessions,
            pending_nodes=pending_nodes,
            dispatched_round=dispatched_round,
            dispatch_cap=dispatch_cap,
        )
        return asyncio.run(
            act_on_exit(
                outcome,
                graph=self.graph,
                repo_root=self.root,
                main_repo=self.root,
                state_dir="state",
                branch=_BRANCH,
                wrapper=self.wrapper,
                observations=self.observations,
                narrate=self.narrated.append,
                now=_NOW,
            )
        )

    def calls(self) -> list[str]:
        log = self.root / "bin" / "calls.log"
        return log.read_text(encoding="utf-8").splitlines() if log.exists() else []

    def question(self, n: int) -> str:
        path = self.root / "state" / "clarifications" / _BRANCH / f"question_{n}.md"
        return path.read_text(encoding="utf-8")

    def state_file(self, name: str) -> str:
        return (self.root / "state" / name).read_text(encoding="utf-8")


def _end(reports: tuple[tuple[str, str], ...] = (), passed: tuple[SkipPassage, ...] = ()) -> End:
    return End("<terminal_handoff>", "convergence", reports, passed)


def test_the_return_field_constants_name_the_graph_nodes_and_fields() -> None:
    assert (QUESTIONS_FIELD, TASKS_COUNT_FIELD, TESTS_COUNT_FIELD, REASON_FIELD) == (
        "questions",
        "tasks_count",
        "tests_count",
        "reason",
    )
    assert QUESTION_NODES == ("plan_writer", "ui_writer")
    assert RETURN_FIELD_READS == (
        ("plan_writer", "questions"),
        ("ui_writer", "questions"),
        ("plan_writer", "tasks_count"),
        ("ui_writer", "tests_count"),
        ("ui_writer", "reason"),
    )


def test_question_nodes_are_every_node_with_an_outcome_bound_to_ask() -> None:
    graph = load_graph_file(_GRAPH)
    asking = {
        node_id
        for node_id, node in graph.nodes.items()
        for edge in getattr(node, "outcomes", {}).values()
        if isinstance(edge, BindingEdge) and edge.binding == "<ask>"
    }
    assert set(QUESTION_NODES) == asking


def test_done_hands_off_without_narration(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    assert run.act(None, kind="done") == "handed_off"
    assert run.narrated == []
    assert run.calls() == []


def test_an_end_narrates_the_done_summary_in_order(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    run.session("plan_writer", Completed("returned"), {"tasks_count": 4})
    run.session("ui_writer", Completed("returned"), {"tests_count": 2})
    end = _end(
        (("plan_review", "passed"), ("ui_test", "passed")),
        (
            SkipPassage("business_parity_review", "phase_parity_off"),
            SkipPassage("business_parity_review", "phase_parity_off"),
        ),
    )
    assert run.act(end) == "handed_off"
    assert run.narrated == [
        "CONVERGED: feat_x — planning handed off",
        "tasks_count: 4",
        "story index: state/story_plans/feat_x_story_plan.md",
        "per-task files: state/task_plans/feat_x/",
        "ui_test: state/ui_test_plans/feat_x_ui_test_plan.md, per-test files "
        "state/ui_test_plans/feat_x/, tests_count: 2",
        "passed without dispatch: business_parity_review phase_parity_off;",
        "📌 Dispatch additions: none",
        "📌 Run mode: none",
    ]
    assert run.calls() == []
    assert run.observations.added == []


def test_an_end_with_no_return_documents_says_not_reported(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    run.act(_end((("ui_test", "no_ui"),)))
    assert run.narrated[1] == "tasks_count: not reported in this session"
    assert run.narrated[4] == "ui_test: no-UI (QA skipped)"


def test_the_no_ui_line_carries_the_writers_reason(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    run.session("ui_writer", Completed("no_ui"), {"reason": "a command-line change"})
    run.act(_end((("ui_test", "no_ui"),)))
    assert run.narrated[4] == "ui_test: no-UI (QA skipped) — a command-line change"


def test_the_run_mode_line_lists_the_skipped_ids_and_each_ignored_entry(tmp_path: Path) -> None:
    run = _Run(
        tmp_path,
        run_mode=(
            "- skipped: P2   (set by the operator)\n"
            "- ignored: skip the docs (not a planning entry)\n"
            "- ignored: run fast\n"
        ),
    )
    run.act(_end((("ui_test", "qa-phase-off"),)))
    assert run.narrated[-1] == (
        "📌 Run mode: skipped P2 — authority state/flow_progress/feat_x_progress.md ## Run mode"
        ' | ignored: "skip the docs" (not a planning entry) | ignored: "run fast"'
    )
    assert run.narrated[4] == "ui_test: QA phase not enabled"


def test_a_skipped_value_of_none_is_run_mode_none_with_its_ignored_entries(tmp_path: Path) -> None:
    run = _Run(tmp_path, run_mode="- skipped: none\n- ignored: go faster (not a phase)\n")
    run.act(_end((("ui_test", "run-mode-skipped"),)))
    assert run.narrated[-1] == '📌 Run mode: none | ignored: "go faster" (not a phase)'
    assert run.narrated[4] == "ui_test: skipped by run mode"


def test_the_ui_test_fallback_with_p2_skipped_and_qa_on_is_run_mode_skipped(
    tmp_path: Path,
) -> None:
    run = _Run(tmp_path, p2="-", qa=True)
    run.act(_end())
    assert run.narrated[4] == "ui_test: skipped by run mode"


def test_the_ui_test_fallback_with_p2_skipped_and_qa_off_is_qa_phase_off(tmp_path: Path) -> None:
    run = _Run(tmp_path, p2="-", qa=False)
    run.act(_end())
    assert run.narrated[4] == "ui_test: QA phase not enabled"


def test_the_ui_test_fallback_with_p2_done_and_an_index_is_passed(tmp_path: Path) -> None:
    run = _Run(tmp_path, p2="x")
    index = run.root / "state" / "ui_test_plans" / "feat_x_ui_test_plan.md"
    index.parent.mkdir(parents=True)
    index.write_text("# UI tests\n", encoding="utf-8")
    run.act(_end())
    assert run.narrated[4] == (
        "ui_test: state/ui_test_plans/feat_x_ui_test_plan.md, per-test files "
        "state/ui_test_plans/feat_x/, tests_count: not reported in this session"
    )


def test_the_ui_test_fallback_with_p2_done_and_no_index_is_no_ui(tmp_path: Path) -> None:
    run = _Run(tmp_path, p2="x")
    run.act(_end())
    assert run.narrated[4] == "ui_test: no-UI (QA skipped)"


def test_the_ui_test_fallback_with_p2_open_is_not_walked(tmp_path: Path) -> None:
    run = _Run(tmp_path, p2=" ")
    run.act(_end())
    assert run.narrated[4] == "ui_test: not walked by this walk"


def test_the_kill_switch_narrates_and_observes(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    assert run.act(None, kind="kill_switch") == "kill_switch"
    path = f"{run.root}/state/AUTONOMOUS_STOP"
    assert run.narrated == [f"halted: the global kill switch {path} is present"]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "The global kill switch ended script-driven planning",
            f"{path} present",
            "no dispatch",
        )
    ]


def test_a_stop_file_and_a_stop_halt_narrate_the_stop_text(tmp_path: Path) -> None:
    expected = (
        "Halted by STOP file at state/STOP. Delete the file and re-run "
        "/devscene:branch-start-plan-autonomous to continue."
    )
    observation = (
        "flow-efficiency",
        "A STOP file ended script-driven planning",
        "state/STOP present",
        "no further dispatch",
    )
    first = _Run(tmp_path / "a")
    assert first.act(None, kind="stop_file") == "stop"
    second = _Run(tmp_path / "b")
    assert second.act(Halt("stop", "stop requested before a set of 1")) == "stop"
    for run in (first, second):
        assert run.narrated == [expected]
        assert run.observations.added == [observation]
        assert run.calls() == []


def test_the_cap_halt_narrates_the_max_total_dispatches_text(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    detail = "40 dispatched; a set of 3 (a, b, c) would pass the cap 40"
    assert run.act(Halt("cap", detail), dispatch_cap=40) == "cap"
    assert run.narrated == [
        "Halted: exceeded MAX_TOTAL_DISPATCHES (40). Dispatches ran past both loops' 5-revision "
        "caps, so this is a re-dispatch runaway rather than non-convergence. Inspect the story "
        "index state/story_plans/feat_x_story_plan.md (and per-task files under "
        "state/task_plans/feat_x/) and the latest findings under "
        "state/task_plan_reviews/feat_x/. If the story index has a `## Rejected findings` "
        "section, read it first."
    ]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "The dispatch cap halted script-driven planning",
            detail,
            "planning halted",
        )
    ]
    assert run.calls() == []


def test_a_pause_commits_the_pending_round_and_writes_the_pause_files(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    kind = run.act(
        Halt("pause", "pause requested before a set of 1"),
        pending_round=1,
        last_round=0,
        pending_nodes=("plan_writer",),
    )
    assert kind == "pause"
    assert run.calls() == ["--artifact plan-round-partial --round 1"]
    assert run.state_file("PAUSE_PROGRESS.md") == (
        "\n## 2026-11-27T10:00:00Z — feat_x paused (script-driven planning)\n"
        "- phase: planning\n"
        "- next step: dispatch plan_writer\n"
    )
    assert run.state_file("PAUSE_ACK") == "2026-11-27T10:00:00Z\n"
    assert run.narrated == ["PAUSED: feat_x — planning"]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "A PAUSE request paused script-driven planning",
            "before dispatching plan_writer",
            "planning paused",
        )
    ]


def test_a_pause_with_no_known_round_makes_no_commit(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    kind = run.act(
        Halt("pause", "pause requested before a set of 1"), pending_nodes=("plan_writer",)
    )
    assert kind == "pause"
    assert run.calls() == []
    assert run.narrated == [
        "no round number is known for the interrupted dispatch: no partial commit",
        "PAUSED: feat_x — planning",
    ]
    assert run.state_file("PAUSE_ACK") == "2026-11-27T10:00:00Z\n"


def test_an_undelivered_halt_commits_the_last_round_and_self_pauses(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    detail = "3 consecutive sets had an undelivered result"
    kind = run.act(
        Halt("undelivered", detail),
        last_round=0,
        pending_nodes=("architecture_review", "plan_review"),
    )
    assert kind == "undelivered"
    assert run.calls() == ["--artifact plan-round-partial --round 0"]
    assert run.state_file("PAUSE_PROGRESS.md") == (
        "\n## 2026-11-27T10:00:00Z — feat_x paused (script-driven planning)\n"
        "- phase: planning (API overload)\n"
        "- next step: re-dispatch architecture_review plan_review; three consecutive "
        "dispatches undelivered: 3 consecutive sets had an undelivered result\n"
    )
    assert run.narrated == ["PAUSED: feat_x — planning (API overload)"]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "Sustained undelivered dispatches self-paused script-driven planning",
            "nodes: architecture_review plan_review",
            "planning paused",
        )
    ]


def test_an_ask_parks_one_q_section_per_returned_question(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    run.session(
        "plan_writer",
        Completed("questions"),
        {
            "outcome": "questions",
            "questions": [
                "Which storage key does the feature use?\n"
                "The feature persists one value across launches.",
                "Should the value be cleared on sign-out?",
            ],
        },
    )
    interrupt = Interrupt("<ask>", "plan_writer", "task-plan-writer", "plan_writer", "returned", ())
    assert run.act(interrupt) == "park"
    assert run.question(1) == (
        "# Questions from task-plan-writer\n"
        "\n"
        "Raised by: task-plan-writer (script-driven planning)\n"
        "\n"
        "## Q1 — Which storage key does the feature use?\n"
        "\n"
        "Which storage key does the feature use?\n"
        "The feature persists one value across launches.\n"
        "\n"
        "## Q2 — Should the value be cleared on sign-out?\n"
        "\n"
        "Should the value be cleared on sign-out?\n"
        "\n"
    )
    assert run.narrated == ["PARKED: feat_x — 1 question(s) at state/clarifications/feat_x/"]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "A writer's questions parked script-driven planning",
            "task-plan-writer at plan_writer",
            "planning parked",
        )
    ]
    assert run.calls() == []


def test_an_ask_with_no_return_document_parks_the_not_captured_body(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    interrupt = Interrupt("<ask>", "ui_writer", "ui-tests-plan-writer", "ui_writer", "returned", ())
    run.act(interrupt)
    assert run.question(1) == (
        "# Questions from ui-tests-plan-writer\n"
        "\n"
        "Raised by: ui-tests-plan-writer (script-driven planning)\n"
        "\n"
        "## Q1 — Questions from ui-tests-plan-writer\n"
        "\n"
        "The writer `ui-tests-plan-writer` returned questions, but its return text was not "
        "captured in this session.\n"
    )


def test_an_escalation_holding_gates_commits_the_partial_then_parks(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    run.session("plan_review", Failed("agent", "no return document"))
    run.session(
        "architecture_review",
        Completed("blocker", "the plan names no owner"),
        {"outcome": "blocker"},
    )
    stop = Stop(
        "<escalate>",
        "plan_review",
        "task-plan-reviewer",
        "error",
        None,
        None,
        (),
        (
            GateRecord("plan_review", "error", None),
            GateRecord("architecture_review", "blocker", None),
        ),
        (),
        (),
    )
    assert run.act(stop, dispatched_round=2, last_round=1) == "park"
    assert run.calls() == ["--artifact plan-round-partial --round 2"]
    assert run.question(1) == (
        "# Planning escalated at plan_review (error)\n"
        "\n"
        "Raised by: task-plan-reviewer (script-driven planning)\n"
        "\n"
        "The planning walk escalated at `plan_review`, reason `error`.\n"
        "\n"
        "```text\n"
        "summary: none\n"
        "evidence: none\n"
        "round_counts: none\n"
        "```\n"
        "\n"
        "### `plan_review` — error\n"
        "\n"
        "- agent: `task-plan-reviewer`\n"
        "- reason: no return document\n"
        "- return text: not captured in this session\n"
        "\n"
        "### `architecture_review` — blocker\n"
        "\n"
        "- agent: `architecture-reviewer`\n"
        "- reason: the plan names no owner\n"
        "- return text:\n"
        "\n"
        "~~~~text\n"
        "{\n"
        '  "outcome": "blocker"\n'
        "}\n"
        "~~~~\n" + _CONTINUE
    )
    assert run.narrated == ["PARKED: feat_x — 1 question(s) at state/clarifications/feat_x/"]
    assert run.observations.added == [
        (
            "flow-efficiency",
            "A walker escalation parked script-driven planning",
            "binding <escalate> at plan_review, reason error",
            "planning parked",
        )
    ]


def test_an_escalation_with_no_held_gate_commits_nothing(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    stop = Stop(
        "<escalate>",
        "plan_round",
        None,
        "cap",
        "the plan loop reached its 5-revision cap",
        "story_index",
        ("business_parity_review", "architecture_review", "plan_review"),
        (),
        (),
        (),
    )
    assert run.act(stop, dispatched_round=5, last_round=5) == "park"
    assert run.calls() == []
    assert run.question(1) == (
        "# Planning escalated at plan_round (cap)\n"
        "\n"
        "Raised by: plan_round (script-driven planning)\n"
        "\n"
        "The planning walk escalated at `plan_round`, reason `cap`.\n"
        "\n"
        "```text\n"
        "summary: the plan loop reached its 5-revision cap\n"
        "evidence: state/story_plans/feat_x_story_plan.md\n"
        "round_counts: business_parity_review, architecture_review, plan_review\n"
        "```\n" + _CONTINUE
    )


def test_a_refused_step_parks_and_observes_a_silent_failure(tmp_path: Path) -> None:
    run = _Run(tmp_path)
    reason = "the saved walk's pending action is a wait, which names no dispatch"
    assert run.act(Refused(reason)) == "park"
    assert run.question(1) == (
        "# Planning walk refused a step\n"
        "\n"
        "Raised by: plan_round (script-driven planning)\n"
        "\n"
        "The planning walk refused a step:\n"
        "\n"
        "```text\n"
        "the saved walk's pending action is a wait, which names no dispatch\n"
        "```\n" + _CONTINUE
    )
    assert run.observations.added == [
        (
            "silent-failure",
            "The planning walk refused a step during script-driven planning",
            reason,
            "the walk stopped; parked",
        )
    ]
    assert run.calls() == []
