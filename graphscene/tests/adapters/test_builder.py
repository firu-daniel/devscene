"""The rule this file exists to enforce: the typed model
(`graphscene.adapters.builder.build_flow_graph`) mirrors the declaration one to one, and keeps
references as ids.

Every expected value is hand-written from reading `valid_generic.json`, `valid_plain_round.json`
or `valid_hooks.json`; a planted in-test graph covers the optional keys those fixtures leave
out.

Deliberately not covered:
- Validation: the builder runs after the schema and vocabulary checks, and is given only graphs
  that passed them, save the one planted shape its own `TypeError` refuses.
"""

import dataclasses
import json
from pathlib import Path
from typing import cast

import pytest

from graphscene.adapters.builder import build_flow_graph
from graphscene.model.flow_graph import (
    BindingEdge,
    DispatchNode,
    FlowGraph,
    HookDeclaration,
    InterruptBinding,
    OnCapEdge,
    OutcomeDeclaration,
    PredicateDeclaration,
    RoundNode,
    RouteEdge,
    SkipEntry,
    StopBinding,
    TerminalNode,
)

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"


def _declared() -> dict[str, object]:
    loaded = json.loads((_FIXTURES / "valid_generic.json").read_text(encoding="utf-8"))
    return cast(dict[str, object], loaded)


def _fixture() -> FlowGraph:
    return build_flow_graph(_declared())


def _hooked() -> FlowGraph:
    loaded = json.loads((_FIXTURES / "valid_hooks.json").read_text(encoding="utf-8"))
    return build_flow_graph(cast(dict[str, object], loaded))


def _planted() -> dict[str, object]:
    return {
        "formatVersion": 5,
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
    assert graph.format_version == 5
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
    assert graph.nodes["published"] == TerminalNode(id="published", binding="<finish>", before=None)


def test_a_round_without_a_writer_carries_none_for_the_review_loop_keys() -> None:
    loaded = json.loads((_FIXTURES / "valid_plain_round.json").read_text(encoding="utf-8"))
    checks = build_flow_graph(cast(dict[str, object], loaded)).nodes["checks"]
    assert isinstance(checks, RoundNode)
    assert checks.gates == ("lint", "license")
    assert checks.writer is None
    assert checks.counter is None
    assert checks.converging_from is None
    assert checks.plan is None
    assert checks.revision_note is None


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


def test_every_hook_key_lands_on_its_snake_case_attribute() -> None:
    graph = _hooked()
    hooks = graph.vocabulary.hooks
    assert hooks is not None
    assert list(hooks) == ["announce", "archive_draft"]
    assert hooks["announce"] == HookDeclaration()
    draft = graph.nodes["draft"]
    assert isinstance(draft, DispatchNode)
    assert draft.prompt_source == "prompts/article-writer.md"
    assert draft.before == ("announce",)
    assert draft.after == ("archive_draft", "announce")
    review_round = graph.nodes["review_round"]
    assert isinstance(review_round, RoundNode)
    assert review_round.before is None
    assert review_round.after == ("archive_draft",)
    assert graph.nodes["published"] == TerminalNode(
        id="published", binding="<finish>", before=("announce",)
    )


def test_absent_hook_keys_build_as_none() -> None:
    graph = _fixture()
    assert graph.vocabulary.hooks is None
    for node_id in ("draft", "edit_check"):
        node = graph.nodes[node_id]
        assert isinstance(node, DispatchNode)
        assert node.prompt_source is None
        assert node.before is None
        assert node.after is None
    review_round = graph.nodes["review_round"]
    assert isinstance(review_round, RoundNode)
    assert review_round.before is None
    assert review_round.after is None
    published = graph.nodes["published"]
    assert isinstance(published, TerminalNode)
    assert published.before is None


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
    hooks = _hooked().vocabulary.hooks
    assert hooks is not None
    with pytest.raises(TypeError):
        hooks["announce"] = HookDeclaration()  # type: ignore[index]


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
