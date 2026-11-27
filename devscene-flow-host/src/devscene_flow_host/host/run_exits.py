"""`act_on_exit`: what the planning driver does once its walk has stopped — the hand-off narration,
the halts, the pauses and the parks — returning the stop kind the command turns into its status.

The rule: each `RunExit` is acted on as the retired bash driver acted on where its walk stopped,
reading as `pd_handoff` (with `pd_run_mode_line`), `pd_stop_halt`, `pd_partial`, `pd_ask_park`
and `pd_escalate_park` in `cli/templates/scripts/lib/planning-driver-lib.sh`, retired and readable
in that file's history:
- `done` and an `End` are `handed_off`; an `End` first narrates the Done summary in
  `pd_handoff`'s order, its `ui_test:` line from the `End`'s `ui_test` report, else from the
  ledger's `P2` mark, the `qa` phase and the UI-test index on disk.
- `kill_switch`, a STOP (`stop_file` or `Halt("stop")`) and `Halt("cap")` narrate their halt and
  add their observation.
- `Halt("pause")` and `Halt("undelivered")` make the `plan-round-partial` commit for the pending
  round, else the last committed round, else narrate that none is known; then write the pause.
- An `Interrupt`, a `Stop` and a `Refused` each write one clarification park; a `Stop` holding
  gates makes the partial commit first, for the last dispatched round, else the last committed one;
  each held node's section lists its attempts when all of them ended for an infrastructure reason,
  as `pd_session_detail` did.
- Every return-document read names its node and field through the `Final`s below, listed in
  `RETURN_FIELD_READS`.
It formats the values the `records` readers return and reads no record line itself.

Deliberately not covered:
- The convergence commits and the `P3` flip: the `commit_convergence` hook runs them before an
  `End` is returned (`host/planning_hooks.py`).
- Exit statuses, the stdout line and the observation flush: `commands/planning_driver.py`.
- Reading the ledger or the configuration: `records`'.
"""

import asyncio
import json
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Final, Literal, TypeAlias

from graphscene import (
    Completed,
    DispatchNode,
    End,
    Failed,
    FlowGraph,
    Halt,
    Interrupt,
    Refused,
    SkipPassage,
    Stop,
)

from devscene_flow_host.host.commit_points import commit_artifact
from devscene_flow_host.host.observations import Observations
from devscene_flow_host.host.paths import render_path
from devscene_flow_host.host.planning_entry import (
    PLAN_WRITER_ENTRY,
    STORY_INDEX_PATH,
    UI_WRITER_ENTRY,
)
from devscene_flow_host.host.planning_hooks import UI_TEST_INDEX_PATH, UI_TEST_SLOT
from devscene_flow_host.host.planning_run import PlanningOutcome
from devscene_flow_host.host.run_control import KILL_SWITCH_FILE, STOP_FILE
from devscene_flow_host.host.run_records import write_park, write_pause
from devscene_flow_host.records.clarifications import CLARIFICATIONS_DIRECTORY
from devscene_flow_host.records.config import read_config
from devscene_flow_host.records.ledger import (
    DONE_VALUE,
    SKIPPED_VALUE,
    ledger_path,
    read_planning_marks,
    read_run_mode_entries,
)

StopKind: TypeAlias = Literal[
    "handed_off", "park", "pause", "undelivered", "stop", "cap", "kill_switch"
]

PLAN_WRITER_NODE: Final = PLAN_WRITER_ENTRY
UI_WRITER_NODE: Final = UI_WRITER_ENTRY
QUESTIONS_FIELD: Final = "questions"
TASKS_COUNT_FIELD: Final = "tasks_count"
TESTS_COUNT_FIELD: Final = "tests_count"
REASON_FIELD: Final = "reason"
QUESTION_NODES: Final = (PLAN_WRITER_NODE, UI_WRITER_NODE)
RETURN_FIELD_READS: Final[tuple[tuple[str, str], ...]] = (
    (PLAN_WRITER_NODE, QUESTIONS_FIELD),
    (UI_WRITER_NODE, QUESTIONS_FIELD),
    (PLAN_WRITER_NODE, TASKS_COUNT_FIELD),
    (UI_WRITER_NODE, TESTS_COUNT_FIELD),
    (UI_WRITER_NODE, REASON_FIELD),
)

TASK_FILES_PATH: Final = "task_files"
UI_TEST_FILES_TEMPLATE: Final = "{state_dir}/ui_test_plans/{branch}/"
PLAN_REVIEWS_TEMPLATE: Final = "{state_dir}/task_plan_reviews/{branch}/"
QA_PHASE: Final = "qa"
REENTRY_COMMAND: Final = "/devscene:branch-start-plan-autonomous"
PARTIAL_ARTIFACT: Final = "plan-round-partial"
PLAN_ROUND_RAISER: Final = "plan_round"
NOT_REPORTED: Final = "not reported in this session"
NOT_CAPTURED: Final = "not captured in this session"
NONE_TEXT: Final = "none"
HELD_DETAIL_REASONS: Final = ("error", "blocker")

UI_PASSED: Final = "passed"
UI_NO_UI: Final = "no_ui"
UI_QA_OFF: Final = "qa-phase-off"
UI_RUN_MODE_SKIPPED: Final = "run-mode-skipped"

CONVERGED_LINE: Final = "CONVERGED: {branch} — planning handed off"
TASKS_COUNT_LINE: Final = "tasks_count: {tasks}"
STORY_INDEX_LINE: Final = "story index: {path}"
TASK_FILES_LINE: Final = "per-task files: {path}"
UI_PASSED_LINE: Final = "ui_test: {index}, per-test files {files}, tests_count: {tests}"
UI_NO_UI_LINE: Final = "ui_test: no-UI (QA skipped)"
UI_NO_UI_REASON: Final = " — {reason}"
UI_QA_OFF_LINE: Final = "ui_test: QA phase not enabled"
UI_RUN_MODE_LINE: Final = "ui_test: skipped by run mode"
UI_NOT_WALKED_LINE: Final = "ui_test: not walked by this walk"
SKIPS_LINE: Final = "passed without dispatch: {skips}"
SKIP_ITEM: Final = "{node} {status};"
DISPATCH_ADDITIONS_LINE: Final = "📌 Dispatch additions: none"
RUN_MODE_NONE_LINE: Final = "📌 Run mode: none{ignored}"
RUN_MODE_SKIPPED_LINE: Final = (
    "📌 Run mode: skipped {skipped} — authority {ledger} ## Run mode{ignored}"
)
IGNORED_ITEM: Final = ' | ignored: "{text}"'
IGNORED_REASON: Final = " ({reason}"

KILL_SWITCH_LINE: Final = "halted: the global kill switch {path} is present"
STOP_LINE: Final = (
    "Halted by STOP file at {state_dir}/"
    + STOP_FILE
    + ". Delete the file and re-run "
    + REENTRY_COMMAND
    + " to continue."
)
CAP_LINE: Final = (
    "Halted: exceeded MAX_TOTAL_DISPATCHES ({cap}). Dispatches ran past both loops' 5-revision "
    "caps, so this is a re-dispatch runaway rather than non-convergence. Inspect the story index "
    "{story_index} (and per-task files under {task_files}) and the latest findings under "
    "{reviews}. If the story index has a `## Rejected findings` section, read it first."
)
NO_ROUND_LINE: Final = "no round number is known for the interrupted dispatch: no partial commit"
PAUSED_LINE: Final = "PAUSED: {branch} — {phase}"
PARKED_LINE: Final = "PARKED: {branch} — 1 question(s) at {directory}/"

PAUSE_PHASE: Final = "planning"
PAUSE_NEXT_STEP: Final = "dispatch {nodes}"
UNDELIVERED_PHASE: Final = "planning (API overload)"
UNDELIVERED_NEXT_STEP: Final = (
    "re-dispatch {nodes}; three consecutive dispatches undelivered: {detail}"
)

QUESTION_SECTION: Final = "## Q{k} — {first}\n\n{item}\n\n"
QUESTIONS_NOT_CAPTURED: Final = (
    "The writer `{agent}` returned questions, but its return text was not captured in this "
    "session.\n"
)
QUESTIONS_TITLE: Final = "Questions from {agent}"
ESCALATION_TITLE: Final = "Planning escalated at {node} ({reason})"
REFUSED_TITLE: Final = "Planning walk refused a step"
ESCALATION_OPENING: Final = (
    "The planning walk escalated at `{node}`, reason `{reason}`.\n\n"
    "```text\nsummary: {summary}\nevidence: {evidence}\nround_counts: {round_counts}\n```\n"
)
SESSION_HEADING: Final = "\n### `{node}` — {outcome}\n\n"
SESSION_AGENT: Final = "- agent: `{agent}`\n"
SESSION_REASON: Final = "- reason: {reason}\n"
SESSION_ATTEMPTS: Final = (
    "- attempts: all {max} ended for an infrastructure reason, each re-dispatched alone "
    "while attempts remained:\n"
)
SESSION_ATTEMPT_ITEM: Final = "  - {line}\n"
SESSION_RETURN: Final = "- return text:\n\n~~~~text\n{text}\n~~~~\n"
SESSION_NO_RETURN: Final = "- return text: " + NOT_CAPTURED + "\n"
REFUSED_OPENING: Final = "The planning walk refused a step:\n\n```text\n{reason}\n```\n"
CONTINUE_SECTION: Final = (
    "\n## Q1 — How should planning continue?\n\n"
    "The walker ended this walk at the escalation above and routes nowhere past it.\n"
)

FLOW_EFFICIENCY: Final = "flow-efficiency"
SILENT_FAILURE: Final = "silent-failure"
KILL_SWITCH_PROBLEM: Final = "The global kill switch ended script-driven planning"
STOP_PROBLEM: Final = "A STOP file ended script-driven planning"
CAP_PROBLEM: Final = "The dispatch cap halted script-driven planning"
PAUSE_PROBLEM: Final = "A PAUSE request paused script-driven planning"
UNDELIVERED_PROBLEM: Final = "Sustained undelivered dispatches self-paused script-driven planning"
ASK_PROBLEM: Final = "A writer's questions parked script-driven planning"
ESCALATE_PROBLEM: Final = "A walker escalation parked script-driven planning"
REFUSED_PROBLEM: Final = "The planning walk refused a step during script-driven planning"
PRESENT_EVIDENCE: Final = "{path} present"
PAUSE_EVIDENCE: Final = "before dispatching {nodes}"
UNDELIVERED_EVIDENCE: Final = "nodes: {nodes}"
ASK_EVIDENCE: Final = "{agent} at {node}"
ESCALATE_EVIDENCE: Final = "binding <escalate> at {node}, reason {reason}"
NO_DISPATCH_COST: Final = "no dispatch"
NO_FURTHER_DISPATCH_COST: Final = "no further dispatch"
HALTED_COST: Final = "planning halted"
PAUSED_COST: Final = "planning paused"
PARKED_COST: Final = "planning parked"
REFUSED_COST: Final = "the walk stopped; parked"


async def act_on_exit(
    outcome: PlanningOutcome,
    *,
    graph: FlowGraph,
    repo_root: Path,
    main_repo: Path,
    state_dir: str,
    branch: str,
    wrapper: Path,
    observations: Observations,
    narrate: Callable[[str], None],
    now: datetime,
) -> StopKind:
    actor = _Actor(
        outcome,
        graph=graph,
        repo_root=repo_root,
        main_repo=main_repo,
        state_dir=state_dir,
        branch=branch,
        wrapper=wrapper,
        observations=observations,
        narrate=narrate,
        now=now,
    )
    return await actor.act()


class _Actor:
    def __init__(
        self,
        outcome: PlanningOutcome,
        *,
        graph: FlowGraph,
        repo_root: Path,
        main_repo: Path,
        state_dir: str,
        branch: str,
        wrapper: Path,
        observations: Observations,
        narrate: Callable[[str], None],
        now: datetime,
    ) -> None:
        self._outcome = outcome
        self._graph = graph
        self._repo_root = repo_root
        self._main_repo = main_repo
        self._state_dir = state_dir
        self._branch = branch
        self._wrapper = wrapper
        self._observations = observations
        self._narrate = narrate
        self._now = now

    async def act(self) -> StopKind:
        outcome = self._outcome
        if outcome.kind == "done":
            return "handed_off"
        if outcome.kind == "kill_switch":
            return self._kill_switch()
        if outcome.kind == "stop_file":
            return self._stop()
        exit_ = outcome.exit
        if isinstance(exit_, End):
            self._handoff(exit_)
            return "handed_off"
        if isinstance(exit_, Halt):
            return await self._halt(exit_)
        if isinstance(exit_, Interrupt):
            return await self._ask(exit_)
        if isinstance(exit_, Stop):
            return await self._escalate(exit_)
        if isinstance(exit_, Refused):
            return await self._refused(exit_)
        raise ValueError(f"a '{outcome.kind}' planning outcome carries no run exit")

    # --- The hand-off --------------------------------------------------------------------------

    def _handoff(self, end: End) -> None:
        tasks = self._field(PLAN_WRITER_NODE, TASKS_COUNT_FIELD) or NOT_REPORTED
        lines = [
            CONVERGED_LINE.format(branch=self._branch),
            TASKS_COUNT_LINE.format(tasks=tasks),
            STORY_INDEX_LINE.format(path=self._path(self._graph.paths[STORY_INDEX_PATH])),
            TASK_FILES_LINE.format(path=self._path(self._graph.paths[TASK_FILES_PATH])),
            self._ui_line(self._ui_status(end)),
        ]
        skips: list[str] = []
        for passage in end.passed:
            if isinstance(passage, SkipPassage):
                item = SKIP_ITEM.format(node=passage.node, status=passage.status)
                if item not in skips:
                    skips.append(item)
        if skips:
            lines.append(SKIPS_LINE.format(skips=" ".join(skips)))
        lines.append(DISPATCH_ADDITIONS_LINE)
        lines.append(self._run_mode_line())
        for line in lines:
            self._narrate(line)

    def _ui_status(self, end: End) -> str | None:
        reports = dict(end.reports)
        if UI_TEST_SLOT in reports:
            return reports[UI_TEST_SLOT]
        marks = read_planning_marks(self._repo_root, self._state_dir, self._branch)
        if marks.p2 == SKIPPED_VALUE:
            qa = read_config(self._repo_root).phases[QA_PHASE] is True
            return UI_RUN_MODE_SKIPPED if qa else UI_QA_OFF
        if marks.p2 == DONE_VALUE:
            index = self._path(self._graph.paths[UI_TEST_INDEX_PATH])
            return UI_PASSED if (self._repo_root / index).exists() else UI_NO_UI
        return None

    def _ui_line(self, status: str | None) -> str:
        if status == UI_PASSED:
            return UI_PASSED_LINE.format(
                index=self._path(self._graph.paths[UI_TEST_INDEX_PATH]),
                files=self._path(UI_TEST_FILES_TEMPLATE),
                tests=self._field(UI_WRITER_NODE, TESTS_COUNT_FIELD) or NOT_REPORTED,
            )
        if status == UI_NO_UI:
            reason = self._field(UI_WRITER_NODE, REASON_FIELD)
            return UI_NO_UI_LINE + (UI_NO_UI_REASON.format(reason=reason) if reason else "")
        if status == UI_QA_OFF:
            return UI_QA_OFF_LINE
        if status == UI_RUN_MODE_SKIPPED:
            return UI_RUN_MODE_LINE
        return UI_NOT_WALKED_LINE

    def _run_mode_line(self) -> str:
        entries = read_run_mode_entries(self._repo_root, self._state_dir, self._branch)
        ignored = "".join(
            IGNORED_ITEM.format(text=entry.text)
            + (IGNORED_REASON.format(reason=entry.reason) if entry.reason is not None else "")
            for entry in entries.ignored
        )
        if entries.skipped in ("", NONE_TEXT):
            return RUN_MODE_NONE_LINE.format(ignored=ignored)
        ledger = ledger_path(self._repo_root, self._state_dir, self._branch)
        return RUN_MODE_SKIPPED_LINE.format(
            skipped=entries.skipped,
            ledger=ledger.relative_to(self._repo_root).as_posix(),
            ignored=ignored,
        )

    # --- The halts -----------------------------------------------------------------------------

    def _kill_switch(self) -> StopKind:
        path = self._main_repo / read_config(self._main_repo).state_dir / KILL_SWITCH_FILE
        self._narrate(KILL_SWITCH_LINE.format(path=path))
        self._observe(
            FLOW_EFFICIENCY,
            KILL_SWITCH_PROBLEM,
            PRESENT_EVIDENCE.format(path=path),
            NO_DISPATCH_COST,
        )
        return "kill_switch"

    def _stop(self) -> StopKind:
        self._narrate(STOP_LINE.format(state_dir=self._state_dir))
        stop_path = f"{self._state_dir}/{STOP_FILE}"
        self._observe(
            FLOW_EFFICIENCY,
            STOP_PROBLEM,
            PRESENT_EVIDENCE.format(path=stop_path),
            NO_FURTHER_DISPATCH_COST,
        )
        return "stop"

    async def _halt(self, halt: Halt) -> StopKind:
        if halt.reason == "stop":
            return self._stop()
        if halt.reason == "cap":
            cap = self._outcome.dispatch_cap
            self._narrate(
                CAP_LINE.format(
                    cap=halt.detail if cap is None else cap,
                    story_index=self._path(self._graph.paths[STORY_INDEX_PATH]),
                    task_files=self._path(self._graph.paths[TASK_FILES_PATH]),
                    reviews=self._path(PLAN_REVIEWS_TEMPLATE),
                )
            )
            self._observe(FLOW_EFFICIENCY, CAP_PROBLEM, halt.detail, HALTED_COST)
            return "cap"
        nodes = " ".join(self._outcome.pending_nodes)
        pending = self._outcome.pending_round
        await self._partial(pending if pending is not None else self._outcome.last_round)
        if halt.reason == "pause":
            await self._pause(PAUSE_PHASE, PAUSE_NEXT_STEP.format(nodes=nodes))
            self._observe(
                FLOW_EFFICIENCY, PAUSE_PROBLEM, PAUSE_EVIDENCE.format(nodes=nodes), PAUSED_COST
            )
            return "pause"
        await self._pause(
            UNDELIVERED_PHASE, UNDELIVERED_NEXT_STEP.format(nodes=nodes, detail=halt.detail)
        )
        self._observe(
            FLOW_EFFICIENCY,
            UNDELIVERED_PROBLEM,
            UNDELIVERED_EVIDENCE.format(nodes=nodes),
            PAUSED_COST,
        )
        return "undelivered"

    async def _partial(self, round_number: int | None) -> None:
        if round_number is None:
            self._narrate(NO_ROUND_LINE)
            return
        await commit_artifact(
            self._wrapper, self._repo_root, PARTIAL_ARTIFACT, round_number=round_number
        )

    async def _pause(self, phase: str, next_step: str) -> None:
        await asyncio.to_thread(
            write_pause,
            self._repo_root,
            self._state_dir,
            self._branch,
            phase=phase,
            next_step=next_step,
            now=self._now,
        )
        self._narrate(PAUSED_LINE.format(branch=self._branch, phase=phase))

    # --- The parks -----------------------------------------------------------------------------

    async def _ask(self, interrupt: Interrupt) -> StopKind:
        agent = interrupt.agent or interrupt.node
        body = ""
        if interrupt.node in QUESTION_NODES:
            document = self._document(interrupt.node)
            questions = None if document is None else document.get(QUESTIONS_FIELD)
            if isinstance(questions, list):
                for k, raw in enumerate(questions, start=1):
                    item = _text(raw)
                    body += QUESTION_SECTION.format(k=k, first=item.split("\n")[0], item=item)
        if not body:
            body = QUESTIONS_NOT_CAPTURED.format(agent=agent)
        await self._park(agent, QUESTIONS_TITLE.format(agent=agent), body)
        self._observe(
            FLOW_EFFICIENCY,
            ASK_PROBLEM,
            ASK_EVIDENCE.format(agent=agent, node=interrupt.node),
            PARKED_COST,
        )
        return "park"

    async def _escalate(self, stop: Stop) -> StopKind:
        evidence = NONE_TEXT
        if stop.evidence is not None:
            template = self._graph.paths.get(stop.evidence)
            evidence = stop.evidence if template is None else self._path(template)
        body = ESCALATION_OPENING.format(
            node=stop.node,
            reason=stop.reason,
            summary=stop.summary or NONE_TEXT,
            evidence=evidence,
            round_counts=", ".join(stop.round_counts) or NONE_TEXT,
        )
        for gate in stop.held:
            body += self._session_detail(gate.gate, gate.outcome)
        if not stop.held and stop.reason in HELD_DETAIL_REASONS:
            body += self._session_detail(stop.node, stop.reason)
        body += CONTINUE_SECTION
        if stop.held:
            dispatched = self._outcome.dispatched_round
            await self._partial(dispatched if dispatched is not None else self._outcome.last_round)
        await self._park(
            stop.agent or PLAN_ROUND_RAISER,
            ESCALATION_TITLE.format(node=stop.node, reason=stop.reason),
            body,
        )
        self._observe(
            FLOW_EFFICIENCY,
            ESCALATE_PROBLEM,
            ESCALATE_EVIDENCE.format(node=stop.node, reason=stop.reason),
            PARKED_COST,
        )
        return "park"

    def _session_detail(self, node: str, outcome: str) -> str:
        text = SESSION_HEADING.format(node=node, outcome=outcome)
        found = self._graph.nodes.get(node)
        if isinstance(found, DispatchNode):
            text += SESSION_AGENT.format(agent=found.agent)
        text += SESSION_REASON.format(reason=self._launch_reason(node) or NOT_CAPTURED)
        sessions = self._outcome.sessions
        exhausted = None if sessions is None else sessions.exhausted_attempts(node)
        if exhausted is not None:
            maximum, lines = exhausted
            text += SESSION_ATTEMPTS.format(max=maximum)
            text += "".join(SESSION_ATTEMPT_ITEM.format(line=line) for line in lines)
        document = self._document(node)
        if document is None:
            return text + SESSION_NO_RETURN
        rendered = json.dumps(dict(document), indent=2, ensure_ascii=False)
        return text + SESSION_RETURN.format(text=rendered)

    def _launch_reason(self, node: str) -> str | None:
        sessions = self._outcome.sessions
        result = None if sessions is None else sessions.launch_result(node)
        if isinstance(result, Failed):
            return result.reason or None
        if isinstance(result, Completed):
            return result.detail or None
        return None

    async def _refused(self, refused: Refused) -> StopKind:
        body = REFUSED_OPENING.format(reason=refused.reason) + CONTINUE_SECTION
        await self._park(PLAN_ROUND_RAISER, REFUSED_TITLE, body)
        self._observe(SILENT_FAILURE, REFUSED_PROBLEM, refused.reason, REFUSED_COST)
        return "park"

    async def _park(self, raised_by: str, title: str, body: str) -> None:
        await asyncio.to_thread(
            write_park,
            self._repo_root,
            self._state_dir,
            self._branch,
            raised_by=raised_by,
            title=title,
            body=body,
        )
        directory = f"{self._state_dir}/{CLARIFICATIONS_DIRECTORY}/{self._branch}"
        self._narrate(PARKED_LINE.format(branch=self._branch, directory=directory))

    # --- Shared --------------------------------------------------------------------------------

    def _path(self, template: str) -> str:
        return render_path(template, self._state_dir, self._branch)

    def _document(self, node: str) -> Mapping[str, object] | None:
        sessions = self._outcome.sessions
        return None if sessions is None else sessions.return_document(node)

    def _field(self, node: str, field: str) -> str | None:
        document = self._document(node)
        value = None if document is None else document.get(field)
        if value is None:
            return None
        return _text(value) or None

    def _observe(self, category: str, problem: str, evidence: str, cost: str) -> None:
        self._observations.add(category, problem, evidence, cost)


def _text(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)
