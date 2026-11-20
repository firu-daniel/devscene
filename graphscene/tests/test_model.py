"""The rule this file exists to enforce: the typed model (`graphscene.model.build_flow_graph`)
mirrors the declaration one to one, and keeps references as ids.

Every expected value is hand-written from reading `valid_generic.json`; a planted in-test graph
covers the optional keys that fixture leaves out.

Deliberately not covered:
- Validation: the builder runs after the schema and vocabulary checks, and is given only graphs
  that passed them, save the one planted shape its own `TypeError` refuses.
"""

import dataclasses
import json
from pathlib import Path
from typing import cast

import pytest

from graphscene.model import (
    BindingEdge,
    DispatchNode,
    FlowGraph,
    InterruptBinding,
    OnCapEdge,
    OutcomeDeclaration,
    PredicateDeclaration,
    RouteEdge,
    RoundNode,
    SkipEntry,
    StopBinding,
    TerminalNode,
    build_flow_graph,
)

_FIXTURES = Path(__file__).parent / "fixtures" / "flow_graph"


def _declared() -> dict[str, object]:
    loaded = json.loads((_FIXTURES / "valid_generic.json").read_text(encoding="utf-8"))
    return cast(dict[str, object], loaded)


def _fixture() -> FlowGraph:
    return build_flow_graph(_declared())


def _planted() -> dict[str, object]:
    return {
        "formatVersion": 4,
        "flow": "planted",
        "description": "Every optional key present.",
        "vocabulary": {
            "outcomes": {
                "done": {},
                "paused": {},
                "pass_out": {"verdict": "pass"},
                "fail_out": {"verdict": "fail"},
            },
            "bindings": {
                "<pause>": {"primitive": "interrupt", "resumeOutcome": "done"},
                "<halt>": {"primitive": "stop", "reasons": ["limit"]},
                "<finish>": {"primitive": "end"},
            },
            "predicates": {},
        },
        "start": "draft",
        "entries": ["draft"],
        "counters": {"attempt": {"cap": 2}},
        "paths": {"article": "{state_dir}/a.md", "note": "{state_dir}/note-{round}.md"},
        "reports": [],
        "nodes": {
            "draft": {
                "kind": "dispatch",
                "agent": "writer",
                "heartbeat": "[{iteration}]",
                "outcomes": {
                    "done": {"to": "round", "ledger": "P1.2", "reset": "attempt"},
                    "paused": {
                        "binding": "<pause>",
                        "resume": "draft",
                        "summary": "paused at {cap}",
                        "roundCounts": ["draft"],
                        "evidence": "article",
                    },
                },
            },
            "round": {
                "kind": "round",
                "parallel": True,
                "gates": ["draft"],
                "writer": "draft",
                "counter": "attempt",
                "convergingFrom": 0,
                "revisionNote": "note",
                "outcomes": {
                    "pass_out": {"to": "end"},
                    "fail_out": {"binding": "<halt>", "reason": "limit"},
                },
            },
            "end": {"kind": "terminal", "binding": "<finish>"},
        },
    }


def test_the_top_level_keys_mirror_the_fixture() -> None:
    graph = _fixture()
    assert graph.format_version == 4
    assert graph.start == "draft"
    assert graph.entries == ("draft", "review_round")
    assert list(graph.nodes) == ["draft", "edit_check", "review_round", "published"]
    assert graph.counters["attempt"].cap == 3


def test_the_vocabulary_mirrors_the_fixture() -> None:
    vocabulary = _fixture().vocabulary
    assert vocabulary.bindings["<pause>"] == InterruptBinding(resume_outcome="resumed")
    assert vocabulary.bindings["<halt>"] == StopBinding(reasons=("limit", "crash"))
    assert vocabulary.outcomes["crashed"].held is True
    assert vocabulary.outcomes["done"] == OutcomeDeclaration(verdict=None, held=False)
    assert vocabulary.predicates["stage_disabled"] == PredicateDeclaration(
        records="bypassed", in_round_counts=False
    )


def test_the_dispatch_nodes_mirror_the_fixture() -> None:
    graph = _fixture()
    draft = graph.nodes["draft"]
    assert isinstance(draft, DispatchNode)
    assert draft.prompts == ("first", "rework")
    assert draft.findings_folder is None
    assert draft.skip is None
    assert draft.outcomes["crashed"] == BindingEdge(
        binding="<halt>",
        resume=None,
        reason="crash",
        summary=None,
        round_counts=None,
        evidence=None,
    )
    edit_check = graph.nodes["edit_check"]
    assert isinstance(edit_check, DispatchNode)
    assert edit_check.skip == (
        SkipEntry(when="stage_disabled", to="review_round", report={"edit_check": "bypassed"}),
    )
    assert edit_check.findings_folder == "{state_dir}/edit_checks/{branch}/"


def test_the_round_and_terminal_nodes_mirror_the_fixture() -> None:
    graph = _fixture()
    review_round = graph.nodes["review_round"]
    assert isinstance(review_round, RoundNode)
    assert review_round.gates == ("edit_check",)
    assert review_round.writer == "draft"
    assert review_round.converging_from == 1
    assert review_round.plan == ("article",)
    assert review_round.revision_note is None
    rejected = review_round.outcomes["rejected"]
    assert isinstance(rejected, RouteEdge)
    assert rejected.increment == "attempt"
    assert rejected.prompt == "rework"
    assert rejected.on_cap == OnCapEdge(
        binding="<halt>",
        reason="limit",
        summary=(
            "the article did not converge in {cap} attempts; the gates open when it fired: "
            "{open_gates}"
        ),
        round_counts=("edit_check",),
        evidence="article",
    )
    assert graph.nodes["published"] == TerminalNode(id="published", binding="<finish>")


def test_every_optional_key_lands_on_its_snake_case_attribute() -> None:
    graph = build_flow_graph(_planted())
    draft = graph.nodes["draft"]
    assert isinstance(draft, DispatchNode)
    done = draft.outcomes["done"]
    assert isinstance(done, RouteEdge)
    assert done.ledger == "P1.2"
    assert done.reset == "attempt"
    assert draft.outcomes["paused"] == BindingEdge(
        binding="<pause>",
        resume="draft",
        reason=None,
        summary="paused at {cap}",
        round_counts=("draft",),
        evidence="article",
    )
    round_node = graph.nodes["round"]
    assert isinstance(round_node, RoundNode)
    assert round_node.revision_note == "note"


def test_references_stay_strings() -> None:
    draft = _fixture().nodes["draft"]
    assert isinstance(draft, DispatchNode)
    done = draft.outcomes["done"]
    assert isinstance(done, RouteEdge)
    assert done.to == "review_round"
    assert type(done.to) is str


def test_the_model_is_immutable() -> None:
    graph = _fixture()
    with pytest.raises(dataclasses.FrozenInstanceError):
        graph.start = "published"  # type: ignore[misc]
    with pytest.raises(TypeError):
        graph.nodes["draft"] = graph.nodes["published"]  # type: ignore[index]


def test_mutating_the_input_after_the_build_leaves_the_graph_unchanged() -> None:
    declared = _declared()
    graph = build_flow_graph(declared)
    nodes = cast(dict[str, object], declared["nodes"])
    draft = cast(dict[str, object], nodes["draft"])
    cast(dict[str, object], draft["outcomes"])["done"] = {"to": "published"}
    cast(list[str], draft["prompts"]).append("third")
    del nodes["published"]
    cast(list[str], declared["entries"]).clear()
    assert graph == _fixture()
    assert list(graph.nodes) == ["draft", "edit_check", "review_round", "published"]


def test_the_builder_refuses_a_shape_the_schema_would_have_refused() -> None:
    declared = _declared()
    draft = cast(dict[str, object], cast(dict[str, object], declared["nodes"])["draft"])
    draft["agent"] = 7
    with pytest.raises(TypeError) as raised:
        build_flow_graph(declared)
    assert str(raised.value) == "nodes.draft.agent: expected str"
