"""The rule this file exists to enforce: over the harness's own format-5 graph,
`cli/templates/scripts/flows/task_plan_writing.graph.json`, `PlanningExecutor` passes on every
`Failed` and every non-verdict `Completed` unchanged; a verdict with no findings file where one is
required, or a round gate's refused file, becomes `Failed("infra", …)`; and a lone reviewer's
`FAIL` findings file is kept in `RevisionFindingsStore` until `clear_revision_findings`.

Every expected value is hand-written from reading the graph file and the rules, never taken from
the output of the code under test.
"""

import asyncio
from pathlib import Path

from graphscene import (
    Completed,
    Dispatch,
    Executor,
    Failed,
    FlowGraph,
    NodeResult,
    load_graph_file,
)

from devscene_flow_host.host.planning_executor import PlanningExecutor, clear_revision_findings
from devscene_flow_host.host.revision_findings import RevisionFindingsStore
from round_fixtures import FAIL_BODY, PASS_BODY, plant_review

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_STATE_DIR = "state"
_BRANCH = "feat_x"


class _Scripted:
    def __init__(self, result: NodeResult) -> None:
        self._result = result

    async def run(self, dispatch: Dispatch) -> NodeResult:
        return self._result


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent="agent",
        prompt_variant=None,
        counters={},
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


def _run(root: Path, node: str, result: NodeResult) -> NodeResult:
    executor: Executor = PlanningExecutor(
        _Scripted(result), graph=_graph(), repo_root=root, state_dir=_STATE_DIR, branch=_BRANCH
    )
    return asyncio.run(executor.run(_dispatch(node)))


def _kept(root: Path) -> tuple[str, ...]:
    return RevisionFindingsStore(root, _STATE_DIR, _BRANCH).read()


def test_a_non_verdict_completed_is_passed_through(tmp_path: Path) -> None:
    result = Completed("returned")
    assert _run(tmp_path, "plan_writer", result) is result


def test_a_failed_is_passed_through_unchanged(tmp_path: Path) -> None:
    result = Failed("agent", "the agent gave up")
    assert _run(tmp_path, "plan_review", result) is result


def test_a_gate_pass_with_no_detail_is_infra(tmp_path: Path) -> None:
    assert _run(tmp_path, "plan_review", Completed("PASS")) == Failed(
        "infra", "PASS carries no findings_file"
    )


def test_a_fail_with_a_blank_detail_is_infra(tmp_path: Path) -> None:
    assert _run(tmp_path, "ui_review", Completed("FAIL", "  ")) == Failed(
        "infra", "FAIL carries no findings_file"
    )
    assert _kept(tmp_path) == ()


def test_a_gate_pass_whose_round_file_has_no_verdict_line_is_infra(tmp_path: Path) -> None:
    plant_review(tmp_path / "reviews", 0, "## Must Fix\n")
    assert _run(tmp_path, "plan_review", Completed("PASS", "reviews/review_0.md")) == Failed(
        "infra", "the round file was refused: no single verdict line"
    )


def test_a_valid_round_file_is_passed_through_and_not_kept(tmp_path: Path) -> None:
    path = plant_review(tmp_path / "reviews", 0, PASS_BODY)
    passed = Completed("PASS", str(path))
    assert _run(tmp_path, "plan_review", passed) is passed
    plant_review(tmp_path / "reviews", 1, FAIL_BODY)
    failed = Completed("FAIL", "reviews/review_1.md")
    assert _run(tmp_path, "architecture_review", failed) is failed
    assert _kept(tmp_path) == ()


def test_a_lone_reviewers_fail_is_kept_until_cleared(tmp_path: Path) -> None:
    result = Completed("FAIL", "state/ui_test_plan_reviews/feat_x/review_0.md")
    assert _run(tmp_path, "ui_review", result) is result
    assert _kept(tmp_path) == ("state/ui_test_plan_reviews/feat_x/review_0.md",)
    clear_revision_findings(tmp_path, _STATE_DIR, _BRANCH)
    assert _kept(tmp_path) == ()
