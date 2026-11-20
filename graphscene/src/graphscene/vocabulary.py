"""The vocabulary check: the part of a format-4 flow graph's validity JSON Schema cannot express.

The rule: every name a flow graph uses is one it declares, and each binding is used where its
primitive allows. `vocabulary_violations` takes an already schema-valid graph as a parsed mapping
and returns one `Violation` per violation, whose `str()` is that violation's `<path>: <reason>`
line, in document order: nodes in key order; within a node, a round's verdict violation, then its
`outcomes` in key order (each edge, then its `onCap`), then its `skip` entries, then a terminal's
`binding`. A binding that is not declared is
reported as undeclared alone, never also for how it is used.

Deliberately not checked:
- Schema validity: the caller validates the graph against the format-4 schema this package
  ships as data, `schemas/flow-graph.schema.json` inside the `graphscene` package
  (`graphscene/src/graphscene/schemas/` in this repository), first.
- Node-id references, reachability and counter caps, which belong to a static checker.
- Reading any file: the graph arrives already parsed.
"""

from collections.abc import Mapping

from graphscene.errors import Violation

_VERDICT_RULE = (
    "a round routes on one outcome declaring verdict pass and one declaring verdict fail"
)


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}
    return {key: child for key, child in value.items() if isinstance(key, str)}


def _strings(value: object) -> list[Violation]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


class _Binding:
    def __init__(self, primitive: str, reasons: list[str]) -> None:
        self.primitive = primitive
        self.reasons = reasons


def _bindings(vocabulary: Mapping[str, object]) -> dict[str, _Binding]:
    declared: dict[str, _Binding] = {}
    for name, declaration in _mapping(vocabulary.get("bindings")).items():
        fields = _mapping(declaration)
        primitive = fields.get("primitive")
        declared[name] = _Binding(
            primitive if isinstance(primitive, str) else "", _strings(fields.get("reasons"))
        )
    return declared


def _undeclared_binding(path: str, name: str) -> Violation:
    return Violation(f"{path}.binding", f"binding '{name}' is not declared in vocabulary.bindings")


def _reason_violations(
    path: str, name: str, binding: _Binding, edge: Mapping[str, object]
) -> list[Violation]:
    reason = edge.get("reason")
    if binding.primitive != "stop":
        if reason is None:
            return []
        return [Violation(f"{path}.reason", f"binding '{name}' is not a stop")]
    if not isinstance(reason, str):
        return [Violation(path, f"binding '{name}' is a stop and needs reason")]
    if reason not in binding.reasons:
        return [
            Violation(f"{path}.reason", f"'{reason}' is not a reason binding '{name}' declares")
        ]
    return []


def _binding_edge_violations(
    path: str, edge: Mapping[str, object], bindings: Mapping[str, _Binding]
) -> list[Violation]:
    name = edge.get("binding")
    if not isinstance(name, str):
        return []
    binding = bindings.get(name)
    if binding is None:
        return [_undeclared_binding(path, name)]
    found: list[Violation] = []
    if binding.primitive == "end":
        found.append(
            Violation(
                f"{path}.binding", f"binding '{name}' is an end; only a terminal node takes one"
            )
        )
    if binding.primitive == "interrupt":
        if "resume" not in edge:
            found.append(Violation(path, f"binding '{name}' is an interrupt and needs resume"))
    elif "resume" in edge:
        found.append(Violation(f"{path}.resume", f"binding '{name}' is not an interrupt"))
    found.extend(_reason_violations(path, name, binding, edge))
    return found


def _on_cap_violations(
    path: str, on_cap: Mapping[str, object], bindings: Mapping[str, _Binding]
) -> list[Violation]:
    name = on_cap.get("binding")
    if not isinstance(name, str):
        return []
    binding = bindings.get(name)
    if binding is None:
        return [_undeclared_binding(path, name)]
    if binding.primitive != "stop":
        return [Violation(f"{path}.binding", f"binding '{name}' is not a stop")]
    return _reason_violations(path, name, binding, on_cap)


def _round_violation(
    node_path: str, outcome_names: list[str], outcomes: Mapping[str, object]
) -> list[Violation]:
    verdicts = sorted(str(_mapping(outcomes[name]).get("verdict")) for name in outcome_names)
    if verdicts == ["fail", "pass"]:
        return []
    return [Violation(f"{node_path}.outcomes", _VERDICT_RULE)]


def _node_violations(
    node_id: str,
    node: Mapping[str, object],
    outcomes: Mapping[str, object],
    bindings: Mapping[str, _Binding],
    predicates: Mapping[str, object],
) -> list[Violation]:
    node_path = f"nodes.{node_id}"
    found: list[Violation] = []
    routes = _mapping(node.get("outcomes"))
    undeclared = [name for name in routes if name not in outcomes]

    if node.get("kind") == "round" and not undeclared:
        found.extend(_round_violation(node_path, list(routes), outcomes))

    for name, edge_value in routes.items():
        path = f"{node_path}.outcomes.{name}"
        if name in undeclared:
            found.append(
                Violation(path, f"outcome '{name}' is not declared in vocabulary.outcomes")
            )
        edge = _mapping(edge_value)
        if "binding" in edge:
            found.extend(_binding_edge_violations(path, edge, bindings))
        elif "onCap" in edge:
            found.extend(_on_cap_violations(f"{path}.onCap", _mapping(edge["onCap"]), bindings))

    skip = node.get("skip")
    for index, entry in enumerate(skip if isinstance(skip, list) else []):
        when = _mapping(entry).get("when")
        if isinstance(when, str) and when not in predicates:
            found.append(
                Violation(
                    f"{node_path}.skip[{index}].when",
                    f"predicate '{when}' is not declared in vocabulary.predicates",
                )
            )

    if node.get("kind") == "terminal":
        binding_name = node.get("binding")
        if isinstance(binding_name, str):
            binding = bindings.get(binding_name)
            if binding is None:
                found.append(_undeclared_binding(node_path, binding_name))
            elif binding.primitive != "end":
                found.append(
                    Violation(f"{node_path}.binding", f"binding '{binding_name}' is not an end")
                )
    return found


def vocabulary_violations(graph: Mapping[str, object]) -> list[Violation]:
    """Return one `Violation` per vocabulary violation in `graph`, whose `str()` is its
    `<path>: <reason>` line, in document order; `[]` when it has none."""
    vocabulary = _mapping(graph.get("vocabulary"))
    outcomes = _mapping(vocabulary.get("outcomes"))
    bindings = _bindings(vocabulary)
    predicates = _mapping(vocabulary.get("predicates"))
    found: list[Violation] = []
    for node_id, node in _mapping(graph.get("nodes")).items():
        found.extend(_node_violations(node_id, _mapping(node), outcomes, bindings, predicates))
    return found
