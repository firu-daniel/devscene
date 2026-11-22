"""The rule this file exists to enforce: a caller importing only from `graphscene` walks a graph
loaded by `load_graph` or `load_graph_file` through a `Walker` over a `FileStateStore`, with a host
answering skips, from the start to an end, a cap, a held crash or a skipped gate; a round with no
review loop dispatches its gates with no `converging` and stops on its own `rejected` edge, writing
only the state file and its lock; `current` re-reads the saved step through a new `Walker` and
store on the same path; and when a round's gates are recorded from concurrent threads, each with
its own `Walker` and store, exactly one call returns the join and every other returns a `Wait`
naming its own gate.

Every expected value is hand-written from reading `valid_generic.json` and
`valid_plain_round.json`, never taken from the walker's output.

Deliberately not covered:

- Every refusal's exact text, the lock order and the state codec: the engine's and the adapters'
  suites.
"""

import copy
import json
import threading
from pathlib import Path

from graphscene import (
    Dispatch,
    DispatchSet,
    End,
    FileStateStore,
    FlowGraph,
    GateRecord,
    RoundPassage,
    SkipPassage,
    Step,
    Stop,
    Wait,
    Walker,
    load_graph,
    load_graph_file,
)

_FIXTURES = Path(__file__).parents[1] / "fixtures" / "flow_graph"
_FIXTURE = _FIXTURES / "valid_generic.json"
_PLAIN_ROUND = _FIXTURES / "valid_plain_round.json"

_EXTRA_GATES = ("style_check", "fact_check", "legal_check")


class DictHost:
    """A `PredicateHost` answering each predicate from a dict, whatever the node."""

    def __init__(self, answers: dict[str, bool]) -> None:
        self.answers = answers

    def answer(self, predicate: str, node: str) -> bool | None:
        return self.answers.get(predicate)


_ENABLED = DictHost({"stage_disabled": False})


def _walker(path: Path, graph: FlowGraph | None = None, host: DictHost = _ENABLED) -> Walker:
    loaded = graph if graph is not None else load_graph_file(_FIXTURE)
    return Walker(loaded, FileStateStore(path), host)


def _editor(number: int, converging: bool, attempt: int) -> Dispatch:
    return Dispatch(
        node="edit_check",
        agent="article-editor",
        prompt=None,
        counters={"attempt": attempt},
        round_number=number,
        converging=converging,
        closed_round=(),
        passed=(),
    )


def _rejected(walker: Walker, detail: str | None = None) -> Step:
    """One round: the writer's `done`, then `edit_check` rejected."""
    walker.next("done")
    return walker.next("rejected", node="edit_check", detail=detail)


# whole walks


def test_draft_review_publish(tmp_path: Path) -> None:
    walker = _walker(tmp_path / "walk.json")
    assert walker.start() == Dispatch(
        node="draft",
        agent="article-writer",
        prompt=None,
        counters={"attempt": 0},
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )
    assert walker.next("done") == DispatchSet("review_round", 0, (_editor(0, False, 0),), ())
    assert walker.next("rejected", node="edit_check", detail="f0") == Dispatch(
        node="draft",
        agent="article-writer",
        prompt="rework",
        counters={"attempt": 1},
        round_number=1,
        converging=None,
        closed_round=(GateRecord("edit_check", "rejected", "f0"),),
        passed=(RoundPassage("review_round", 0, "fail"),),
    )
    assert walker.next("done") == DispatchSet("review_round", 1, (_editor(1, True, 1),), ())
    assert walker.next("approved", node="edit_check") == End(
        "<finish>",
        "published",
        reports=(("edit_check", "approved"),),
        passed=(RoundPassage("review_round", 1, "pass"),),
    )


def test_three_rejected_rounds_stop_at_the_cap(tmp_path: Path) -> None:
    walker = _walker(tmp_path / "walk.json")
    walker.start()
    _rejected(walker)
    _rejected(walker)
    assert _rejected(walker) == Stop(
        "<halt>",
        node="review_round",
        agent=None,
        reason="limit",
        summary=(
            "the article did not converge in 3 attempts; the gates open when it fired: edit_check"
        ),
        evidence="article",
        round_counts=("edit_check",),
        held=(),
        closed_round=(GateRecord("edit_check", "rejected", None),),
        passed=(RoundPassage("review_round", 2, "fail"),),
    )


def test_a_crash_at_a_gate_is_held_and_stops_the_walk(tmp_path: Path) -> None:
    walker = _walker(tmp_path / "walk.json")
    walker.start()
    walker.next("done")
    assert walker.next("crashed", node="edit_check") == Stop(
        "<halt>",
        node="edit_check",
        agent="article-editor",
        reason="crash",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(GateRecord("edit_check", "crashed", None),),
        closed_round=(),
        passed=(),
    )


def test_a_skipped_gate_closes_the_round_as_a_pass_at_once(tmp_path: Path) -> None:
    walker = _walker(tmp_path / "walk.json", host=DictHost({"stage_disabled": True}))
    walker.start()
    assert walker.next("done") == End(
        "<finish>",
        "published",
        reports=(("edit_check", "bypassed"),),
        passed=(SkipPassage("edit_check", "bypassed"), RoundPassage("review_round", 0, "pass")),
    )


def _checker(node: str, agent: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent=agent,
        prompt=None,
        counters={},
        round_number=0,
        converging=None,
        closed_round=(),
        passed=(),
    )


def test_a_round_with_no_review_loop_stops_on_its_rejected_edge(tmp_path: Path) -> None:
    walker = _walker(tmp_path / "walk.json", load_graph_file(_PLAIN_ROUND))
    assert walker.start() == Dispatch(
        node="intake",
        agent="release-intake",
        prompt=None,
        counters={},
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )
    assert walker.next("accepted") == DispatchSet(
        "checks",
        0,
        (_checker("lint", "lint-checker"), _checker("license", "license-checker")),
        (),
    )
    assert walker.next("accepted", node="lint") == Wait(
        "checks", GateRecord("lint", "accepted", None), ("license",)
    )
    assert walker.next("rejected", node="license") == Stop(
        "<halt>",
        node="checks",
        agent=None,
        reason="failed",
        summary=None,
        evidence=None,
        round_counts=(),
        held=(),
        closed_round=(
            GateRecord("lint", "accepted", None),
            GateRecord("license", "rejected", None),
        ),
        passed=(RoundPassage("checks", 0, "fail"),),
    )
    assert sorted(path.name for path in tmp_path.iterdir()) == ["walk.json", "walk.json.lock"]


def test_current_re_reads_the_saved_step_through_a_new_walker(tmp_path: Path) -> None:
    path = tmp_path / "walk.json"
    walker = _walker(path)
    walker.start()
    pending = walker.next("done")
    assert _walker(path).current() == pending
    assert pending == DispatchSet("review_round", 0, (_editor(0, False, 0),), ())


# concurrency


def _four_gate_graph() -> FlowGraph:
    """`valid_generic.json` with three copies of `edit_check` added to `review_round.gates`."""
    document = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    nodes = document["nodes"]
    for gate in _EXTRA_GATES:
        nodes[gate] = copy.deepcopy(nodes["edit_check"])
    nodes["review_round"]["gates"] = ["edit_check", *_EXTRA_GATES]
    return load_graph(document)


def test_concurrent_gates_join_exactly_once(tmp_path: Path) -> None:
    path = tmp_path / "walk.json"
    graph = _four_gate_graph()
    walker = _walker(path, graph)
    walker.start()
    walker.next("done")

    gates = ("edit_check", *_EXTRA_GATES)
    barrier = threading.Barrier(len(gates))
    results: dict[str, Step] = {}
    failures: list[BaseException] = []

    def record(gate: str) -> None:
        try:
            own = _walker(path, graph)
            barrier.wait()
            results[gate] = own.next("approved", node=gate)
        except BaseException as error:
            failures.append(error)

    threads = [threading.Thread(target=record, args=(gate,)) for gate in gates]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert failures == []
    joins = [step for step in results.values() if not isinstance(step, Wait)]
    assert len(joins) == 1
    waits = {gate: step for gate, step in results.items() if isinstance(step, Wait)}
    assert len(waits) == 3
    for gate, wait in waits.items():
        assert wait.recorded == GateRecord(gate, "approved", None)
    assert isinstance(joins[0], End)
    assert _walker(path, graph).current() == joins[0]
