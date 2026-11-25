"""The rule this module exists to enforce: the harness's planning graph agrees with the plugin
documents it duplicates. `core_agreement_violations` returns the findings of four checks, in
this order:

- 4 `run-mode-id-known`: every skip entry whose `when` matches `RUN_MODE_PREDICATE` names an id
  of `RUN_MODE_DOC`'s closed directive set.
- 5 `ledger-id-known`: every route edge's `ledger` is a task-engine entry of `LEDGER_DOC` →
  `### 1.3 Templates`.
- 6 `findings-folder-in-core`: every dispatch node's `findingsFolder`, and the directory of every
  round node's revision note, is a backticked path in the flow core's `## Setup` step 2 table,
  and the whole revision note appears in the core's `## Loop`.
- 7 `cap-matches-core`: `counters.iteration.cap` equals every integer the core's three cap
  phrases state.

An owner document, section or phrase that yields nothing is a finding, never an empty pass.
Within a check, nodes come in key order, and a node's skip entries and outcomes in declaration
order.

This is the harness's own dev-time check, never shipped: it reads `plugin/instructions/…` by
repo-relative path, and the package an adopter receives under `<scriptsDir>/python/` has no
`plugin/` beside it. So the flow-to-core table is `CORE_FOR_FLOW`, held here and never in the
graph.

Deliberately not covered:
- Checks 1–3, 8 and 9: they are `graphscene.static_violations`, run inside every `load_graph`.
"""

import re
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Final

from graphscene import DispatchNode, FlowGraph, RoundNode, RouteEdge, Violation

from devscene_flow_host.host.predicates import RUN_MODE_PREDICATE

RUN_MODE_DOC: Final = "plugin/instructions/run_mode_instructions.md"
LEDGER_DOC: Final = "plugin/instructions/autonomous_pause_and_ledger.md"
CORE_FOR_FLOW: Final[Mapping[str, str]] = MappingProxyType(
    {"task_plan_writing": "plugin/instructions/task_plan_writing_instructions_core.md"}
)

_CLOSED_SET_HEADING: Final = (
    "## The closed directive set — the only four things a run mode may switch off"
)
_RUN_MODE_ROW: Final = re.compile(r"^\| `([^`]+)` \|")
_TEMPLATES_HEADING: Final = "### 1.3 Templates"
_TASK_ENGINE: Final = "**Task engine**"
_USER_REVIEW_ENGINE: Final = "**User-review engine**"
_LEDGER_ENTRY: Final = re.compile(r"^- \[ \] ([A-Za-z0-9.]+)\.\s")
_SETUP_HEADING: Final = "## Setup (once per session)"
_PATHS_STEP: Final = "2. **Paths.**"
_NEXT_STEP: Final = "3. "
_LOOP_HEADING: Final = "## Loop"
_SAFETY_HEADING: Final = "## Safety contract — applies before EVERY Agent dispatch"
_STEP4_PHRASE: Final = "MAX_TOTAL_DISPATCHES = "
_HALT_PHRASE: Final = "Halted: exceeded MAX_TOTAL_DISPATCHES"
_BACKTICKED: Final = re.compile(r"`[^`]*`")
_COUNTER: Final = "iteration"

# Taken over verbatim from the retired `scripts/check-flow-graph.sh` here-doc `ANCHORS`:
# label, source text, pattern.
_ANCHORS: Final[tuple[tuple[str, str, re.Pattern[str]], ...]] = (
    ("## Setup step 4 `iteration >= <N>`", "step4", re.compile(r"`iteration >= [0-9]+`")),
    ("## Setup step 4 `caps at <N> revisions`", "step4", re.compile(r"caps at [0-9]+ revisions")),
    ("## Safety contract step 2 `<N>-revision caps`", "halt", re.compile(r"[0-9]+-revision caps")),
)


def _read(repo_root: Path, relative: str) -> list[str]:
    """A missing document reads as empty, so its check refuses rather than passes."""
    try:
        return (repo_root / relative).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []


def _between(lines: list[str], start: str, stop: str) -> list[str]:
    """The lines after the first line starting with `start`, up to the next starting with `stop`."""
    found: list[str] = []
    on = False
    for line in lines:
        if not on:
            on = line.startswith(start)
            continue
        if line.startswith(stop):
            break
        found.append(line)
    return found


def _written_back(template: str) -> str:
    return (
        template.replace("{state_dir}", "<state_dir>")
        .replace("{branch}", "<branch>")
        .replace("{round}", "<iteration>")
    )


def _run_mode_violations(graph: FlowGraph, repo_root: Path) -> list[Violation]:
    section = _between(_read(repo_root, RUN_MODE_DOC), _CLOSED_SET_HEADING, "## ")
    ids = {m.group(1) for line in section if (m := _RUN_MODE_ROW.match(line))}
    if not ids:
        return [
            Violation(
                "",
                f"run-mode-id-known: {RUN_MODE_DOC} yields no closed-set ids; "
                "refusing to pass without them",
            )
        ]
    found: list[Violation] = []
    for node_id, node in graph.nodes.items():
        if not isinstance(node, DispatchNode):
            continue
        for index, entry in enumerate(node.skip or ()):
            match = RUN_MODE_PREDICATE.match(entry.when)
            if match and match.group(1) not in ids:
                found.append(
                    Violation(
                        f"nodes.{node_id}.skip[{index}].when",
                        f"run-mode-id-known: run-mode id '{match.group(1)}' is not in the "
                        f"closed set of {RUN_MODE_DOC}",
                    )
                )
    return found


def _ledger_violations(graph: FlowGraph, repo_root: Path) -> list[Violation]:
    templates = _between(_read(repo_root, LEDGER_DOC), _TEMPLATES_HEADING, "### ")
    section = _between(templates, _TASK_ENGINE, _USER_REVIEW_ENGINE)
    ids = {m.group(1) for line in section if (m := _LEDGER_ENTRY.match(line))}
    if not ids:
        return [
            Violation(
                "",
                f"ledger-id-known: {LEDGER_DOC} yields no task-engine ledger ids; "
                "refusing to pass without them",
            )
        ]
    found: list[Violation] = []
    for node_id, node in graph.nodes.items():
        if isinstance(node, (DispatchNode, RoundNode)):
            for outcome, edge in node.outcomes.items():
                if isinstance(edge, RouteEdge) and edge.ledger is not None:
                    if edge.ledger not in ids:
                        found.append(
                            Violation(
                                f"nodes.{node_id}.outcomes.{outcome}.ledger",
                                f"ledger-id-known: ledger '{edge.ledger}' is not a task-engine "
                                f"entry of {LEDGER_DOC}",
                            )
                        )
    return found


def _findings_folder_violations(
    graph: FlowGraph, core: str, core_lines: list[str]
) -> list[Violation]:
    """With no backticked path in the table, the refusal replaces every table comparison; the
    `## Loop` comparison still runs."""
    setup = _between(core_lines, _SETUP_HEADING, "## ")
    table = "\n".join(_between(setup, _PATHS_STEP, _NEXT_STEP))
    loop = "\n".join(_between(core_lines, _LOOP_HEADING, "## "))
    has_table = _BACKTICKED.search(table) is not None
    found: list[Violation] = []
    if not has_table:
        found.append(
            Violation(
                "",
                f"findings-folder-in-core: {core} ## Setup step 2 table yields no backticked "
                "path; refusing to pass without it",
            )
        )
    else:
        for node_id, node in graph.nodes.items():
            if isinstance(node, DispatchNode) and node.findings_folder is not None:
                folder = _written_back(node.findings_folder)
                if f"`{folder}`" not in table:
                    found.append(
                        Violation(
                            f"nodes.{node_id}.findingsFolder",
                            f"findings-folder-in-core: findingsFolder '{folder}' is not in "
                            f"{core} ## Setup step 2 table",
                        )
                    )
    for node_id, node in graph.nodes.items():
        if not isinstance(node, RoundNode) or node.revision_note is None:
            continue
        template = graph.paths.get(node.revision_note)
        if template is None:
            continue
        note = _written_back(template)
        directory = note.rsplit("/", 1)[0] + "/"
        if has_table and f"`{directory}`" not in table:
            found.append(
                Violation(
                    f"nodes.{node_id}.revisionNote",
                    f"findings-folder-in-core: revision note '{directory}' is not in "
                    f"{core} ## Setup step 2 table",
                )
            )
        if note not in loop:
            found.append(
                Violation(
                    f"nodes.{node_id}.revisionNote",
                    f"findings-folder-in-core: revision note '{note}' is not in {core} ## Loop",
                )
            )
    return found


def _cap_violations(graph: FlowGraph, core: str, core_lines: list[str]) -> list[Violation]:
    counter = graph.counters.get(_COUNTER)
    if counter is None:
        return [Violation("counters", "cap-matches-core: graph has no counters.iteration")]
    setup = _between(core_lines, _SETUP_HEADING, "## ")
    safety = _between(core_lines, _SAFETY_HEADING, "## ")
    sources = {
        "step4": "\n".join(line for line in setup if _STEP4_PHRASE in line),
        "halt": "\n".join(line for line in safety if _HALT_PHRASE in line),
    }
    found: list[Violation] = []
    for label, source, pattern in _ANCHORS:
        values = [re.sub(r"[^0-9]", "", m) for m in pattern.findall(sources[source])]
        if not values:
            found.append(
                Violation(
                    "",
                    f"cap-matches-core: {label} yields no value in {core}; "
                    "refusing to pass without it",
                )
            )
        for value in values:
            if int(value) != counter.cap:
                found.append(
                    Violation(
                        "counters.iteration.cap",
                        f"cap-matches-core: graph cap {counter.cap}, core states {value} "
                        f"at {label}",
                    )
                )
    return found


def core_agreement_violations(graph: FlowGraph, repo_root: Path) -> list[Violation]:
    found = _run_mode_violations(graph, repo_root) + _ledger_violations(graph, repo_root)
    core = CORE_FOR_FLOW.get(graph.flow)
    if core is None:
        return [
            *found,
            Violation(
                "flow",
                f"findings-folder-in-core: flow '{graph.flow}' has no core in CORE_FOR_FLOW",
            ),
            Violation(
                "flow", f"cap-matches-core: flow '{graph.flow}' has no core in CORE_FOR_FLOW"
            ),
        ]
    core_lines = _read(repo_root, core)
    return (
        found
        + _findings_folder_violations(graph, core, core_lines)
        + _cap_violations(graph, core, core_lines)
    )
