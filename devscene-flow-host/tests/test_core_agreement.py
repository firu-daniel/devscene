"""The rule this file exists to enforce: `core_agreement_violations` holds the harness's planning
graph, `cli/templates/scripts/flows/task_plan_writing.graph.json`, to the three plugin documents
it duplicates — checks 4 `run-mode-id-known`, 5 `ledger-id-known`, 6 `findings-folder-in-core`,
7 `cap-matches-core` and 10 `prompt-source-in-core` — and refuses to pass when an owner
document, section or phrase yields nothing.

The suite reads the checkout's graph and the three plugin documents read-only. A graph-side case
changes one thing in the graph's JSON and loads it through `load_graph`, so the mutant passes
every library check; a document-side case plants every changed copy under `tmp_path`. Every
expected path and reason is a literal written from the contract, never taken from the checker's
output.

Deliberately not covered:
- Any flow other than `task_plan_writing`: no other flow has a row in `CORE_FOR_FLOW` yet.
"""

import json
from pathlib import Path
from typing import Any

from graphscene import DispatchNode, FlowGraph, Violation, load_graph, load_graph_file

from core_agreement import CORE_FOR_FLOW, LEDGER_DOC, RUN_MODE_DOC, core_agreement_violations

_REPO_ROOT = Path(__file__).resolve().parents[2]
_GRAPH = _REPO_ROOT / "cli" / "templates" / "scripts" / "flows" / "task_plan_writing.graph.json"
_CORE = CORE_FOR_FLOW["task_plan_writing"]
_SOURCE_PREFIX = "instructions/task_plan_writing_instructions_core.md → "


def _graph_json() -> dict[str, Any]:
    loaded: dict[str, Any] = json.loads(_GRAPH.read_text(encoding="utf-8"))
    return loaded


def _real_graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _plant(root: Path) -> None:
    """Copy the three owner documents, unchanged, to their repo-relative paths under `root`."""
    for relative in (RUN_MODE_DOC, LEDGER_DOC, _CORE):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((_REPO_ROOT / relative).read_text(encoding="utf-8"), encoding="utf-8")


def _replace(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{relative} no longer carries {old!r}; this case needs a new change"
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_the_real_graph_agrees_with_the_real_documents() -> None:
    graph = _real_graph()
    sourced = sorted(
        node_id
        for node_id, node in graph.nodes.items()
        if isinstance(node, DispatchNode) and node.prompt_source is not None
    )
    assert sourced == [
        "architecture_review",
        "business_parity_review",
        "plan_review",
        "plan_writer",
        "ui_review",
        "ui_writer",
    ]

    assert core_agreement_violations(graph, _REPO_ROOT) == []


def test_an_unknown_run_mode_id_is_found() -> None:
    graph = _graph_json()
    graph["vocabulary"]["predicates"]["run_mode_skips_nope"] = {
        "records": "passed-by-exclusion",
        "inRoundCounts": True,
    }
    graph["nodes"]["architecture_review"]["skip"].append(
        {"when": "run_mode_skips_nope", "to": "plan_round"}
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.architecture_review.skip[1].when",
            "run-mode-id-known: run-mode id 'nope' is not in the closed set of "
            "plugin/instructions/run_mode_instructions.md",
        )
    ]


def test_an_unknown_ledger_id_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_round"]["outcomes"]["PASS"]["ledger"] = "P9"

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_round.outcomes.PASS.ledger",
            "ledger-id-known: ledger 'P9' is not a task-engine entry of "
            "plugin/instructions/autonomous_pause_and_ledger.md",
        )
    ]


def test_a_findings_folder_missing_from_the_table_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["findingsFolder"] = "{state_dir}/plan_reviews_elsewhere/{branch}/"

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.findingsFolder",
            "findings-folder-in-core: findingsFolder '<state_dir>/plan_reviews_elsewhere/<branch>/'"
            " is not in plugin/instructions/task_plan_writing_instructions_core.md ## Setup step 2"
            " table",
        )
    ]


def test_a_revision_note_missing_from_the_table_and_the_loop_is_found_twice() -> None:
    graph = _graph_json()
    graph["paths"]["revision_note"] = "{state_dir}/revisions_elsewhere/{branch}/note_{round}.md"

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_round.revisionNote",
            "findings-folder-in-core: revision note '<state_dir>/revisions_elsewhere/<branch>/' is"
            " not in plugin/instructions/task_plan_writing_instructions_core.md ## Setup step 2"
            " table",
        ),
        Violation(
            "nodes.plan_round.revisionNote",
            "findings-folder-in-core: revision note"
            " '<state_dir>/revisions_elsewhere/<branch>/note_<iteration>.md' is not in"
            " plugin/instructions/task_plan_writing_instructions_core.md ## Loop",
        ),
    ]


def test_a_cap_the_core_does_not_state_is_found_at_every_anchor() -> None:
    graph = _graph_json()
    graph["counters"]["iteration"]["cap"] = 6

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "counters.iteration.cap",
            "cap-matches-core: graph cap 6, core states 5 at ## Setup step 4 `iteration >= <N>`",
        ),
        Violation(
            "counters.iteration.cap",
            "cap-matches-core: graph cap 6, core states 5 at ## Setup step 4"
            " `caps at <N> revisions`",
        ),
        Violation(
            "counters.iteration.cap",
            "cap-matches-core: graph cap 6, core states 5 at ## Safety contract step 2"
            " `<N>-revision caps`",
        ),
    ]


def test_a_graph_with_no_iteration_counter_is_found() -> None:
    graph = _graph_json()
    graph["counters"] = {"plan_iteration": graph["counters"].pop("iteration")}
    nodes = graph["nodes"]
    nodes["plan_round"]["counter"] = "plan_iteration"
    nodes["plan_round"]["outcomes"]["PASS"]["reset"] = "plan_iteration"
    nodes["plan_round"]["outcomes"]["FAIL"]["increment"] = "plan_iteration"
    nodes["ui_review"]["outcomes"]["FAIL"]["increment"] = "plan_iteration"

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation("counters", "cap-matches-core: graph has no counters.iteration")
    ]


def test_a_flow_with_no_core_is_found() -> None:
    graph = _graph_json()
    graph["flow"] = "other_flow"

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "flow", "findings-folder-in-core: flow 'other_flow' has no core in CORE_FOR_FLOW"
        ),
        Violation("flow", "cap-matches-core: flow 'other_flow' has no core in CORE_FOR_FLOW"),
        Violation("flow", "prompt-source-in-core: flow 'other_flow' has no core in CORE_FOR_FLOW"),
    ]


def test_a_dispatch_node_with_no_prompt_source_is_found() -> None:
    graph = _graph_json()
    del graph["nodes"]["plan_review"]["promptSource"]

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.promptSource",
            "prompt-source-in-core: dispatch node 'plan_review' declares no promptSource",
        )
    ]


def test_a_malformed_prompt_source_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["promptSource"] = (
        "instructions/task_plan_writing_instructions_core.md → ### 4. Spawn `task-plan-reviewer`"
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.promptSource",
            "prompt-source-in-core: prompt source"
            " 'instructions/task_plan_writing_instructions_core.md → ### 4. Spawn"
            " `task-plan-reviewer`' is not '<document> → ## <section> → ### <heading>'",
        )
    ]


def test_a_prompt_source_in_another_document_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["promptSource"] = (
        "instructions/run_mode_instructions.md → ## Loop → ### 4. Spawn `task-plan-reviewer`"
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.promptSource",
            "prompt-source-in-core: 'instructions/run_mode_instructions.md' is not"
            " plugin/instructions/task_plan_writing_instructions_core.md",
        )
    ]


def test_a_prompt_source_section_missing_from_the_core_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["promptSource"] = (
        _SOURCE_PREFIX + "## Elsewhere → ### 4. Spawn `task-plan-reviewer`"
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.promptSource",
            f"prompt-source-in-core: the heading '## Elsewhere' is not in '{_REPO_ROOT / _CORE}'",
        )
    ]


def test_a_prompt_source_heading_missing_from_its_section_is_found() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["promptSource"] = (
        _SOURCE_PREFIX + "## UI-test-plan write loop → ### 4. Spawn `task-plan-reviewer`"
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == [
        Violation(
            "nodes.plan_review.promptSource",
            "prompt-source-in-core: the heading '### 4. Spawn `task-plan-reviewer`' is not under"
            " '## UI-test-plan write loop' in"
            f" '{_REPO_ROOT / _CORE}'",
        )
    ]


def test_a_block_count_the_node_does_not_declare_is_found(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(
        tmp_path,
        _CORE,
        "\n### 5. Parse the reviewer's return",
        "```\nsecond block\n```\n\n### 5. Parse the reviewer's return",
    )

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "nodes.plan_review.promptSource",
            "prompt-source-in-core: '### 4. Spawn `task-plan-reviewer`' carries 2 fenced block(s)"
            " in plugin/instructions/task_plan_writing_instructions_core.md, node 'plan_review'"
            " declares 1 prompt(s)",
        )
    ]


def test_a_prompt_source_moved_to_another_core_heading_with_as_many_blocks_is_clean() -> None:
    graph = _graph_json()
    graph["nodes"]["plan_review"]["promptSource"] = (
        _SOURCE_PREFIX + "## Loop → ### 3. Architecture review (plan-review mode)"
    )

    assert core_agreement_violations(load_graph(graph), _REPO_ROOT) == []


def test_unchanged_planted_documents_yield_no_finding(tmp_path: Path) -> None:
    _plant(tmp_path)

    assert core_agreement_violations(_real_graph(), tmp_path) == []


def test_a_renamed_closed_set_heading_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(
        tmp_path,
        RUN_MODE_DOC,
        "## The closed directive set — the only four things a run mode may switch off",
        "## The directive set",
    )

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "run-mode-id-known: plugin/instructions/run_mode_instructions.md yields no closed-set"
            " ids; refusing to pass without them",
        )
    ]


def test_a_removed_task_engine_line_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(tmp_path, LEDGER_DOC, "**Task engine**", "Task engine")

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "ledger-id-known: plugin/instructions/autonomous_pause_and_ledger.md yields no"
            " task-engine ledger ids; refusing to pass without them",
        )
    ]


def test_a_step_2_table_without_backticks_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    path = tmp_path / _CORE
    lines = path.read_text(encoding="utf-8").split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("2. **Paths.**"))
    stop = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("3. "))
    assert any("`" in line for line in lines[start + 1 : stop])
    lines[start + 1 : stop] = [line.replace("`", "") for line in lines[start + 1 : stop]]
    path.write_text("\n".join(lines), encoding="utf-8")

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "findings-folder-in-core: plugin/instructions/task_plan_writing_instructions_core.md"
            " ## Setup step 2 table yields no backticked path; refusing to pass without it",
        )
    ]


def test_a_removed_iteration_phrase_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(tmp_path, _CORE, "`iteration >= 5`", "their own")

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "cap-matches-core: ## Setup step 4 `iteration >= <N>` yields no value in"
            " plugin/instructions/task_plan_writing_instructions_core.md; refusing to pass"
            " without it",
        )
    ]


def test_a_removed_caps_at_phrase_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(tmp_path, _CORE, "caps at 5 revisions", "caps its revisions")

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "cap-matches-core: ## Setup step 4 `caps at <N> revisions` yields no value in"
            " plugin/instructions/task_plan_writing_instructions_core.md; refusing to pass"
            " without it",
        )
    ]


def test_a_removed_revision_caps_phrase_refuses_to_pass(tmp_path: Path) -> None:
    _plant(tmp_path)
    _replace(tmp_path, _CORE, "5-revision caps", "revision caps")

    assert core_agreement_violations(_real_graph(), tmp_path) == [
        Violation(
            "",
            "cap-matches-core: ## Safety contract step 2 `<N>-revision caps` yields no value in"
            " plugin/instructions/task_plan_writing_instructions_core.md; refusing to pass"
            " without it",
        )
    ]
