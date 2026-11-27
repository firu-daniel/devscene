"""The rule this file exists to enforce: a path template renders as `flow-walker.sh`'s
`render_path` — every `{state_dir}`, then every `{branch}`, then `{round}` only when a round number
is given — and on the harness's own format-5 graph,
`cli/templates/scripts/flows/task_plan_writing.graph.json`, a node's round is the round that
gates it or names it as its writer, and a reviewer's index outside a round is the next free index
under its rendered `findingsFolder`.

Every expected value is hand-written from reading the graph file, never taken from the output of
the code under test.
"""

from pathlib import Path

from graphscene import FlowGraph, load_graph_file

from devscene_flow_host.host.paths import render_path
from devscene_flow_host.host.reviewers import review_iteration, round_of_gate, round_of_writer
from round_fixtures import PASS_BODY, plant_review

_GRAPH = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.graph.json"
)
_REVISION_NOTE = "{state_dir}/plan_revisions/{branch}/task_plan_revision_{round}.md"


def _graph() -> FlowGraph:
    return load_graph_file(_GRAPH)


def test_every_placeholder_renders_when_a_round_is_given() -> None:
    assert (
        render_path(_REVISION_NOTE, "state", "feat_x", 4)
        == "state/plan_revisions/feat_x/task_plan_revision_4.md"
    )


def test_round_stays_in_place_without_a_round_number() -> None:
    assert (
        render_path(_REVISION_NOTE, "state", "feat_x")
        == "state/plan_revisions/feat_x/task_plan_revision_{round}.md"
    )


def test_every_occurrence_is_replaced_and_a_trailing_slash_kept() -> None:
    assert render_path("{branch}/{state_dir}/{branch}/", "s", "b") == "b/s/b/"


def test_a_gate_finds_the_round_that_lists_it() -> None:
    found = round_of_gate(_graph(), "plan_review")
    assert found is not None and found.id == "plan_round"


def test_a_writer_finds_the_round_that_names_it() -> None:
    found = round_of_writer(_graph(), "plan_writer")
    assert found is not None and found.id == "plan_round"


def test_a_reviewer_outside_a_round_has_no_round() -> None:
    graph = _graph()
    assert round_of_gate(graph, "ui_review") is None
    assert round_of_writer(graph, "ui_review") is None


def test_the_index_outside_a_round_follows_the_highest_review(tmp_path: Path) -> None:
    folder = tmp_path / "state" / "ui_test_plan_reviews" / "feat_x"
    plant_review(folder, 0, PASS_BODY)
    plant_review(folder, 2, PASS_BODY)
    assert review_iteration(_graph(), tmp_path, "state", "feat_x", "ui_review") == 3


def test_the_index_outside_a_round_is_zero_with_no_review(tmp_path: Path) -> None:
    assert review_iteration(_graph(), tmp_path, "state", "feat_x", "ui_review") == 0


def test_a_round_gate_has_no_index_here(tmp_path: Path) -> None:
    assert review_iteration(_graph(), tmp_path, "state", "feat_x", "plan_review") is None


def test_a_node_with_no_findings_folder_has_no_index(tmp_path: Path) -> None:
    assert review_iteration(_graph(), tmp_path, "state", "feat_x", "plan_writer") is None


def test_a_node_that_is_not_a_dispatch_has_no_index(tmp_path: Path) -> None:
    assert review_iteration(_graph(), tmp_path, "state", "feat_x", "plan_round") is None
