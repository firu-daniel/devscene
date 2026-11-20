"""The typed, immutable form of a declared format-4 flow graph, and `build_flow_graph`, which builds
it from an already-validated parsed graph.

The mapping rules, from the schema's declaration to the model:
- Attribute names: each attribute is its schema key in snake_case — `formatVersion` →
  `format_version`, `resumeOutcome` → `resume_outcome`, `inRoundCounts` → `in_round_counts`,
  `convergingFrom` → `converging_from`, `revisionNote` → `revision_note`, `findingsFolder` →
  `findings_folder`, `onCap` → `on_cap`, `roundCounts` → `round_counts`; every other key keeps
  its own name. The one addition is a node's `id`, its key in `nodes`.
- Containers: a JSON array becomes a `tuple`; a JSON object becomes a read-only
  `types.MappingProxyType` over a fresh `dict`, keeping the declaration's key order and never
  aliasing the caller's input.
- Absent keys: an absent optional key is `None`. The one exception is `held`, which the schema
  allows only as `true`: it is a `bool`, `False` when absent.
- Integers: a number the schema accepts as an integer, `3` or `3.0`, becomes an `int`.
- Which classes: an edge carrying `binding` is a `BindingEdge` and any other edge a `RouteEdge`,
  as the schema's `edge` `if`/`then` decides; a node's class follows `kind`; a binding's class
  follows `primitive`.
- Fixed words: the only fixed words are the schema's own enums, typed as `NodeKind`, `Primitive`
  and `Verdict`.

The builder does not validate. A shape the schema would have refused is a programming error here:
it raises `TypeError` naming the dotted path — object keys joined with ".", array indices as
"[i]", as `graphscene.errors.Violation.path` writes them — never a `GraphError`.

Deliberately not covered:
- Validation, which is the loader's: the schema check and the vocabulary check run first.
- Resolving node-id and other name references (`to`, `resume`, `gates`, `writer`, `start`,
  `entries`, `round_counts`, counter, path, report-slot, prompt and binding names): they stay
  `str` ids, and checking that they exist belongs to a later static checker.
- Any harness name.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, Literal, TypeAlias

NodeKind: TypeAlias = Literal["dispatch", "round", "terminal"]
Primitive: TypeAlias = Literal["interrupt", "stop", "end"]
Verdict: TypeAlias = Literal["pass", "fail"]


@dataclass(frozen=True)
class OutcomeDeclaration:
    verdict: Verdict | None
    held: bool


@dataclass(frozen=True)
class InterruptBinding:
    primitive: ClassVar[Literal["interrupt"]] = "interrupt"
    resume_outcome: str


@dataclass(frozen=True)
class StopBinding:
    primitive: ClassVar[Literal["stop"]] = "stop"
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EndBinding:
    primitive: ClassVar[Literal["end"]] = "end"


BindingDeclaration: TypeAlias = InterruptBinding | StopBinding | EndBinding


@dataclass(frozen=True)
class PredicateDeclaration:
    records: str
    in_round_counts: bool


@dataclass(frozen=True)
class Vocabulary:
    outcomes: Mapping[str, OutcomeDeclaration]
    bindings: Mapping[str, BindingDeclaration]
    predicates: Mapping[str, PredicateDeclaration]


@dataclass(frozen=True)
class CounterDeclaration:
    cap: int


@dataclass(frozen=True)
class OnCapEdge:
    binding: str
    reason: str
    summary: str | None
    round_counts: tuple[str, ...] | None
    evidence: str | None


@dataclass(frozen=True)
class RouteEdge:
    to: str
    increment: str | None
    reset: str | None
    prompt: str | None
    ledger: str | None
    report: Mapping[str, str] | None
    on_cap: OnCapEdge | None


@dataclass(frozen=True)
class BindingEdge:
    binding: str
    resume: str | None
    reason: str | None
    summary: str | None
    round_counts: tuple[str, ...] | None
    evidence: str | None


Edge: TypeAlias = RouteEdge | BindingEdge


@dataclass(frozen=True)
class SkipEntry:
    when: str
    to: str
    report: Mapping[str, str] | None


@dataclass(frozen=True)
class DispatchNode:
    kind: ClassVar[Literal["dispatch"]] = "dispatch"
    id: str
    agent: str
    heartbeat: str
    outcomes: Mapping[str, Edge]
    prompts: tuple[str, ...] | None
    findings_folder: str | None
    skip: tuple[SkipEntry, ...] | None


@dataclass(frozen=True)
class RoundNode:
    kind: ClassVar[Literal["round"]] = "round"
    id: str
    parallel: bool
    gates: tuple[str, ...]
    writer: str
    counter: str
    converging_from: int
    plan: tuple[str, ...] | None
    revision_note: str | None
    outcomes: Mapping[str, Edge]


@dataclass(frozen=True)
class TerminalNode:
    kind: ClassVar[Literal["terminal"]] = "terminal"
    id: str
    binding: str


Node: TypeAlias = DispatchNode | RoundNode | TerminalNode


@dataclass(frozen=True)
class FlowGraph:
    format_version: Literal[4]
    flow: str
    description: str
    vocabulary: Vocabulary
    start: str
    entries: tuple[str, ...]
    counters: Mapping[str, CounterDeclaration]
    paths: Mapping[str, str]
    reports: tuple[str, ...]
    nodes: Mapping[str, Node]


def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def _object(value: object, path: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{path or '(root)'}: expected object")
    return value


def _str(value: object, path: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{path}: expected str")
    return value


def _int(value: object, path: str) -> int:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{path}: expected int")
    return value


def _bool(value: object, path: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{path}: expected bool")
    return value


def _strs(value: object, path: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise TypeError(f"{path}: expected array")
    return tuple(_str(item, f"{path}[{index}]") for index, item in enumerate(value))


def _opt_str(fields: Mapping[str, object], key: str, path: str) -> str | None:
    return _str(fields[key], _join(path, key)) if key in fields else None


def _opt_strs(fields: Mapping[str, object], key: str, path: str) -> tuple[str, ...] | None:
    return _strs(fields[key], _join(path, key)) if key in fields else None


def _str_map(value: object, path: str) -> Mapping[str, str]:
    fields = _object(value, path)
    return MappingProxyType({key: _str(child, _join(path, key)) for key, child in fields.items()})


def _opt_str_map(fields: Mapping[str, object], key: str, path: str) -> Mapping[str, str] | None:
    return _str_map(fields[key], _join(path, key)) if key in fields else None


def _outcome(value: object, path: str) -> OutcomeDeclaration:
    fields = _object(value, path)
    verdict: Verdict | None = None
    if "verdict" in fields:
        raw = fields["verdict"]
        if raw == "pass":
            verdict = "pass"
        elif raw == "fail":
            verdict = "fail"
        else:
            raise TypeError(f"{_join(path, 'verdict')}: expected 'pass' or 'fail'")
    held = _bool(fields["held"], _join(path, "held")) if "held" in fields else False
    return OutcomeDeclaration(verdict=verdict, held=held)


def _binding(value: object, path: str) -> BindingDeclaration:
    fields = _object(value, path)
    primitive = fields.get("primitive")
    if primitive == "interrupt":
        key = "resumeOutcome"
        return InterruptBinding(resume_outcome=_str(fields.get(key), _join(path, key)))
    if primitive == "stop":
        return StopBinding(reasons=_strs(fields.get("reasons"), _join(path, "reasons")))
    if primitive == "end":
        return EndBinding()
    raise TypeError(f"{_join(path, 'primitive')}: expected 'interrupt', 'stop' or 'end'")


def _predicate(value: object, path: str) -> PredicateDeclaration:
    fields = _object(value, path)
    key = "inRoundCounts"
    return PredicateDeclaration(
        records=_str(fields.get("records"), _join(path, "records")),
        in_round_counts=_bool(fields.get(key), _join(path, key)),
    )


def _vocabulary(value: object, path: str) -> Vocabulary:
    fields = _object(value, path)
    outcomes = _object(fields.get("outcomes"), _join(path, "outcomes"))
    bindings = _object(fields.get("bindings"), _join(path, "bindings"))
    predicates = _object(fields.get("predicates"), _join(path, "predicates"))
    return Vocabulary(
        outcomes=MappingProxyType(
            {name: _outcome(d, _join(path, f"outcomes.{name}")) for name, d in outcomes.items()}
        ),
        bindings=MappingProxyType(
            {name: _binding(d, _join(path, f"bindings.{name}")) for name, d in bindings.items()}
        ),
        predicates=MappingProxyType(
            {
                name: _predicate(d, _join(path, f"predicates.{name}"))
                for name, d in predicates.items()
            }
        ),
    )


def _counter(value: object, path: str) -> CounterDeclaration:
    return CounterDeclaration(cap=_int(_object(value, path).get("cap"), _join(path, "cap")))


def _on_cap(value: object, path: str) -> OnCapEdge:
    fields = _object(value, path)
    return OnCapEdge(
        binding=_str(fields.get("binding"), _join(path, "binding")),
        reason=_str(fields.get("reason"), _join(path, "reason")),
        summary=_opt_str(fields, "summary", path),
        round_counts=_opt_strs(fields, "roundCounts", path),
        evidence=_opt_str(fields, "evidence", path),
    )


def _edge(value: object, path: str) -> Edge:
    fields = _object(value, path)
    if "binding" in fields:
        return BindingEdge(
            binding=_str(fields["binding"], _join(path, "binding")),
            resume=_opt_str(fields, "resume", path),
            reason=_opt_str(fields, "reason", path),
            summary=_opt_str(fields, "summary", path),
            round_counts=_opt_strs(fields, "roundCounts", path),
            evidence=_opt_str(fields, "evidence", path),
        )
    return RouteEdge(
        to=_str(fields.get("to"), _join(path, "to")),
        increment=_opt_str(fields, "increment", path),
        reset=_opt_str(fields, "reset", path),
        prompt=_opt_str(fields, "prompt", path),
        ledger=_opt_str(fields, "ledger", path),
        report=_opt_str_map(fields, "report", path),
        on_cap=_on_cap(fields["onCap"], _join(path, "onCap")) if "onCap" in fields else None,
    )


def _edges(value: object, path: str) -> Mapping[str, Edge]:
    fields = _object(value, path)
    return MappingProxyType({name: _edge(e, _join(path, name)) for name, e in fields.items()})


def _skip_entry(value: object, path: str) -> SkipEntry:
    fields = _object(value, path)
    return SkipEntry(
        when=_str(fields.get("when"), _join(path, "when")),
        to=_str(fields.get("to"), _join(path, "to")),
        report=_opt_str_map(fields, "report", path),
    )


def _skip(value: object, path: str) -> tuple[SkipEntry, ...]:
    if not isinstance(value, list):
        raise TypeError(f"{path}: expected array")
    return tuple(_skip_entry(item, f"{path}[{index}]") for index, item in enumerate(value))


def _node(node_id: str, value: object, path: str) -> Node:
    fields = _object(value, path)
    kind = fields.get("kind")
    if kind == "terminal":
        return TerminalNode(id=node_id, binding=_str(fields.get("binding"), _join(path, "binding")))
    if kind == "round":
        return RoundNode(
            id=node_id,
            parallel=_bool(fields.get("parallel"), _join(path, "parallel")),
            gates=_strs(fields.get("gates"), _join(path, "gates")),
            writer=_str(fields.get("writer"), _join(path, "writer")),
            counter=_str(fields.get("counter"), _join(path, "counter")),
            converging_from=_int(fields.get("convergingFrom"), _join(path, "convergingFrom")),
            plan=_opt_strs(fields, "plan", path),
            revision_note=_opt_str(fields, "revisionNote", path),
            outcomes=_edges(fields.get("outcomes"), _join(path, "outcomes")),
        )
    if kind == "dispatch":
        return DispatchNode(
            id=node_id,
            agent=_str(fields.get("agent"), _join(path, "agent")),
            heartbeat=_str(fields.get("heartbeat"), _join(path, "heartbeat")),
            outcomes=_edges(fields.get("outcomes"), _join(path, "outcomes")),
            prompts=_opt_strs(fields, "prompts", path),
            findings_folder=_opt_str(fields, "findingsFolder", path),
            skip=_skip(fields["skip"], _join(path, "skip")) if "skip" in fields else None,
        )
    raise TypeError(f"{_join(path, 'kind')}: expected 'dispatch', 'round' or 'terminal'")


def build_flow_graph(graph: Mapping[str, object]) -> FlowGraph:
    """Build the typed model of `graph`, a parsed format-4 flow graph that already passed the
    schema check and the vocabulary check."""
    fields = _object(graph, "")
    if fields.get("formatVersion") != 4 or isinstance(fields.get("formatVersion"), bool):
        raise TypeError("formatVersion: expected 4")
    counters = _object(fields.get("counters"), "counters")
    nodes = _object(fields.get("nodes"), "nodes")
    return FlowGraph(
        format_version=4,
        flow=_str(fields.get("flow"), "flow"),
        description=_str(fields.get("description"), "description"),
        vocabulary=_vocabulary(fields.get("vocabulary"), "vocabulary"),
        start=_str(fields.get("start"), "start"),
        entries=_strs(fields.get("entries"), "entries"),
        counters=MappingProxyType(
            {name: _counter(c, f"counters.{name}") for name, c in counters.items()}
        ),
        paths=_str_map(fields.get("paths"), "paths"),
        reports=_strs(fields.get("reports"), "reports"),
        nodes=MappingProxyType(
            {node_id: _node(node_id, n, f"nodes.{node_id}") for node_id, n in nodes.items()}
        ),
    )
