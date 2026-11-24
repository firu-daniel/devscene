"""Renders the host's `HostStep` as the stdout `flow-walker.sh` prints for the same action.

The rule: every line keeps `flow-walker.sh`'s form — its header's `OUTPUT` grammar, built as its
`render_block`, `render_set`, `record_in_set`, `take_binding` and `render_terminal` build it —
in the same keys and the same order, one `\\n`-terminated line each, so a caller parsing bash's
output reads this unchanged. The findings files a step carries are `HostStep.revision_findings`
when non-empty, otherwise the `detail` of each `GateRecord` of the action's `closed_round` that
has one, in that tuple's order. An action or passage type not named here raises `ValueError`
naming it, never a block guessed from its fields; so does a fault bash reports as exit 2.

Deliberately not covered:
- A `Refused` and every exit status: `commands/flow_walker.py`'s.
- Re-reading what bash re-prints from saved bytes: a `current` re-renders, so a non-round
  reviewer's `arg.iteration` and a cap's `rounds:` counts and evidence lines are read from disk
  again rather than re-printed.
"""

from pathlib import Path

from graphscene import (
    Dispatch,
    DispatchNode,
    DispatchSet,
    End,
    FlowGraph,
    GateRecord,
    Interrupt,
    LedgerPassage,
    Passage,
    RoundPassage,
    SkipPassage,
    Stop,
    Wait,
)

from devscene_flow_host.host.paths import render_path
from devscene_flow_host.host.refusals import ROUND_FILE_ATTEMPTS, Refusal
from devscene_flow_host.host.reviewers import review_iteration, round_of_gate, round_of_writer
from devscene_flow_host.host.round_gates import HostStep, RefusedWait
from devscene_flow_host.records.index_evidence import (
    REJECTED_FINDINGS_HEADING,
    SCOPE_REGISTER_HEADING,
    read_index_evidence,
)
from devscene_flow_host.records.round_files import fail_count


def render(
    step: HostStep, *, graph: FlowGraph, repo_root: Path, state_dir: str, branch: str
) -> str:
    action = step.action
    lines: list[str]
    if isinstance(action, Dispatch):
        lines = _block(
            action,
            _passed(action.passed) + _refused(step.refusals),
            step=step,
            graph=graph,
            repo_root=repo_root,
            state_dir=state_dir,
            branch=branch,
        )
    elif isinstance(action, DispatchSet):
        lines = []
        carried = _passed(action.passed) + _refused(step.refusals)
        for dispatch in action.dispatches:
            lines += _block(
                dispatch,
                carried,
                step=step,
                graph=graph,
                repo_root=repo_root,
                state_dir=state_dir,
                branch=branch,
            )
            carried = []
    elif isinstance(action, Wait):
        lines = ["action: wait", f"node: {action.round}"]
        lines.append(f"recorded: {action.recorded.gate} {action.recorded.outcome}")
        lines += [f"pending: {gate}" for gate in action.pending]
    elif isinstance(action, RefusedWait):
        lines = ["action: wait", f"node: {action.round}", _refused_line(action.refusal)]
        lines += [f"pending: {gate}" for gate in action.pending]
    elif isinstance(action, Interrupt):
        lines = _binding_head(action.binding, action.node, action.agent)
        lines.append(f"resume: {action.resume}")
        lines += _passed(action.passed)
    elif isinstance(action, Stop):
        lines = _binding_head(action.binding, action.node, action.agent)
        lines.append(f"reason: {action.reason}")
        if action.reason == "cap":
            lines += _cap_lines(
                action,
                step=step,
                graph=graph,
                repo_root=repo_root,
                state_dir=state_dir,
                branch=branch,
            )
        lines += [f"held: {record.gate} {record.outcome}" for record in action.held]
        lines += _refused(step.refusals)
        lines += _passed(action.passed)
    elif isinstance(action, End):
        lines = ["action: binding", f"binding: {action.binding}", f"node: {action.node}"]
        lines += [f"report: {slot} {status}" for slot, status in action.reports]
        lines += _passed(action.passed)
    else:
        raise ValueError(f"no rendering for the action type {type(action).__name__}")
    return "".join(line + "\n" for line in lines)


def _block(
    dispatch: Dispatch,
    carried: list[str],
    *,
    step: HostStep,
    graph: FlowGraph,
    repo_root: Path,
    state_dir: str,
    branch: str,
) -> list[str]:
    node = graph.nodes.get(dispatch.node)
    if not isinstance(node, DispatchNode):
        raise ValueError(f"graph has no dispatch node '{dispatch.node}'")
    lines = ["action: dispatch", f"node: {dispatch.node}", f"agent: {dispatch.agent}"]
    variant: str | None = None
    if node.prompts is not None:
        variant = dispatch.prompt if dispatch.prompt is not None else "initial"
        if variant not in node.prompts:
            raise ValueError(
                f"graph gives '{dispatch.node}' the unknown prompt variant '{variant}'"
            )
        lines.append(f"prompt: {variant}")
    if round_of_writer(graph, dispatch.node) is not None:
        lines.append(f"arg.iteration: {_round_number(dispatch)}")
    if variant == "revision":
        files = _findings_files(step, dispatch.closed_round)
        if not files:
            raise ValueError(
                f"a revision of '{dispatch.node}' is due and no findings file is recorded"
            )
        lines += [f"arg.findings_file: {path}" for path in files]
    if round_of_gate(graph, dispatch.node) is not None:
        lines.append(f"arg.iteration: {_round_number(dispatch)}")
        if dispatch.converging is not None:
            mode = "converging" if dispatch.converging else "full"
            lines.append(f"arg.review_mode: {mode}")
    else:
        # TODO: @claude add a follow up task for this: re-print a non-round reviewer's saved
        # arg.iteration on a current rather than re-reading its findings folder — flow-walker.sh
        # render_block
        index = review_iteration(graph, repo_root, state_dir, branch, dispatch.node)
        if index is not None:
            lines.append(f"arg.iteration: {index}")
    lines += carried
    iteration = dispatch.counters.get("iteration")
    heartbeat = node.heartbeat.replace("{iteration}", "" if iteration is None else str(iteration))
    lines.append(f"heartbeat: {heartbeat}  (#<total_dispatches>)")
    return lines


def _round_number(dispatch: Dispatch) -> int:
    if dispatch.round_number is None:
        raise ValueError(f"the dispatch of '{dispatch.node}' carries no round number")
    return dispatch.round_number


def _binding_head(binding: str, node: str, agent: str | None) -> list[str]:
    lines = ["action: binding", f"binding: {binding}", f"node: {node}"]
    if agent is not None:
        lines.append(f"agent: {agent}")
    return lines


def _cap_lines(
    stop: Stop,
    *,
    step: HostStep,
    graph: FlowGraph,
    repo_root: Path,
    state_dir: str,
    branch: str,
) -> list[str]:
    lines = [f"findings_file: {path}" for path in _findings_files(step, stop.closed_round)]
    # TODO: @claude add a follow up task for this: re-print a cap's saved rounds: counts and
    # evidence lines on a current rather than re-reading them from disk — flow-walker.sh
    # take_binding
    for counted in stop.round_counts:
        node = graph.nodes.get(counted)
        if not isinstance(node, DispatchNode) or node.findings_folder is None:
            raise ValueError(f"graph has no 'nodes.{counted}.findingsFolder'")
        folder = repo_root / render_path(node.findings_folder, state_dir, branch)
        lines.append(f"rounds: {counted} {fail_count(folder)}")
    if stop.evidence is not None:
        template = graph.paths.get(stop.evidence)
        if template is None:
            raise ValueError(f"graph has no 'paths.{stop.evidence}'")
        rendered = render_path(template, state_dir, branch)
        evidence = read_index_evidence(repo_root / rendered)
        index = f"{repo_root}/{rendered}"
        if evidence is not None:
            # TODO: @claude add a follow up task for this: interleave evidence.open: lines
            # under each ## Rejected findings heading rather than after the first —
            # flow-walker.sh fw_index_evidence
            if evidence.rejected_findings:
                lines.append(f"evidence: {index} {REJECTED_FINDINGS_HEADING}")
            lines += [f"evidence.open: {entry}" for entry in evidence.open_rejections]
            if evidence.scope_register:
                lines.append(f"evidence: {index} {SCOPE_REGISTER_HEADING}")
    if stop.summary is not None:
        lines.append(f"summary: {stop.summary}")
    return lines


def _findings_files(step: HostStep, closed_round: tuple[GateRecord, ...]) -> tuple[str, ...]:
    if step.revision_findings:
        return step.revision_findings
    return tuple(record.detail for record in closed_round if record.detail is not None)


def _passed(passed: tuple[Passage, ...]) -> list[str]:
    lines: list[str] = []
    for passage in passed:
        if isinstance(passage, SkipPassage):
            lines.append(f"skip: {passage.node} {passage.status}")
        elif isinstance(passage, RoundPassage):
            lines.append(f"round: {passage.number} {passage.verdict.upper()}")
        elif isinstance(passage, LedgerPassage):
            lines.append(f"ledger: {passage.entry}")
        else:
            raise ValueError(f"no rendering for the passage type {type(passage).__name__}")
    return lines


def _refused(refusals: tuple[Refusal, ...]) -> list[str]:
    return [_refused_line(refusal) for refusal in refusals]


def _refused_line(refusal: Refusal) -> str:
    return (
        f"refused: {refusal.gate} attempt {refusal.attempt} of {ROUND_FILE_ATTEMPTS}: "
        f"{refusal.reason}"
    )
