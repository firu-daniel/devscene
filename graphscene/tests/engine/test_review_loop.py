"""The rule this file exists to enforce: a round node is a review loop exactly when it declares
`writer`, `counter` and `convergingFrom`, and a review loop is converging when its counter has
reached `convergingFrom` (`graphscene.engine.review_loop`).

Graphs are built through `graphscene.adapters.builder.build_flow_graph`, from
`valid_generic.json` or from a graph planted through
`graphscene/tests/engine/walk_support.py` → `planted`; every expected value is hand-written from
reading the graph.

Deliberately not covered:

- A built round node lacking the three fields: the schema, the model and the builder require
  them, so the absent case is pinned through `_loop` directly.
"""

import json
from pathlib import Path

from graphscene.adapters.builder import build_flow_graph
from graphscene.engine.review_loop import (
    ReviewLoop,
    _loop,
    is_converging,
    review_loop,
    review_loops,
)
from graphscene.model.flow_graph import RoundNode

from .walk_support import planted

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"


def _round(writer: str, counter: str, converging_from: int) -> dict[str, object]:
    return {
        "kind": "round",
        "parallel": True,
        "gates": ["gate"],
        "writer": writer,
        "counter": counter,
        "convergingFrom": converging_from,
        "outcomes": {"approved": {"to": "published"}},
    }


def test_the_fixture_round_is_a_review_loop() -> None:
    parsed: object = json.loads((_FIXTURES / "valid_generic.json").read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    node = build_flow_graph(parsed).nodes["review_round"]
    assert isinstance(node, RoundNode)
    assert review_loop(node) == ReviewLoop("review_round", "draft", "attempt", 1)


def test_review_loops_returns_every_round_in_nodes_key_order() -> None:
    graph = planted(
        {
            "second": _round("draft_b", "attempt", 2),
            "gate": {
                "kind": "dispatch",
                "agent": "worker",
                "heartbeat": "beat",
                "outcomes": {"done": {"to": "second"}},
            },
            "first": _round("draft_a", "pass", 0),
            "published": {"kind": "terminal", "binding": "<finish>"},
        }
    )
    assert review_loops(graph) == (
        ReviewLoop("second", "draft_b", "attempt", 2),
        ReviewLoop("first", "draft_a", "pass", 0),
    )


def test_a_loop_is_not_converging_one_below_converging_from() -> None:
    loop = ReviewLoop("review_round", "draft", "attempt", 2)
    assert is_converging(loop, {"attempt": 1}) is False


def test_a_loop_is_converging_at_converging_from() -> None:
    loop = ReviewLoop("review_round", "draft", "attempt", 2)
    assert is_converging(loop, {"attempt": 2}) is True


def test_no_writer_is_no_loop() -> None:
    assert _loop("review_round", None, "attempt", 1) is None


def test_no_counter_is_no_loop() -> None:
    assert _loop("review_round", "draft", None, 1) is None


def test_no_converging_from_is_no_loop() -> None:
    assert _loop("review_round", "draft", "attempt", None) is None
