"""The engine walk suites' shared support: a planted graph over `valid_generic.json`'s top level,
and a `PredicateHost` answering from a table.

`planted` builds through `graphscene.adapters.builder.build_flow_graph`, as
`graphscene/tests/engine/test_vocabulary.py` → `_graph` does: a planted graph passes no schema,
vocabulary or static check.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from graphscene.adapters.builder import build_flow_graph
from graphscene.model.flow_graph import FlowGraph

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"


def planted(nodes: dict[str, object], **overrides: object) -> FlowGraph:
    """Build `valid_generic.json`'s top level with `nodes` in place of its own, and each override
    (a serialized top-level key) replacing that key."""
    parsed: object = json.loads((_FIXTURES / "valid_generic.json").read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return build_flow_graph({**parsed, "nodes": nodes, **overrides})


@dataclass(frozen=True)
class AnswerTable:
    """Answers `(predicate, node)` from `answers`, and `False` for any pair not listed."""

    answers: dict[tuple[str, str], bool | None]

    def answer(self, predicate: str, node: str) -> bool | None:
        return self.answers.get((predicate, node), False)
