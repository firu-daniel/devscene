"""The rule this file exists to enforce: a node declaring no `prompts` runs no variant; one that
does runs the dispatch's `prompt`, or `initial` when it carries none; `dispatch_variant` refuses a
variant the node does not declare, naming the node and the variant, while `declared_variant` checks
nothing; and a revision's findings files are the recorded ones when there are any, otherwise the
closed round's gate details that exist, in order.

Every expected value is a literal written from that rule, never taken from the output of the code
under test.
"""

from types import MappingProxyType

import pytest
from graphscene import Dispatch, DispatchNode, GateRecord

from devscene_flow_host.host.prompt_variants import (
    declared_variant,
    dispatch_variant,
    findings_files,
)


def _node(prompts: tuple[str, ...] | None) -> DispatchNode:
    return DispatchNode(
        id="plan_writer",
        agent="task-plan-writer",
        heartbeat="writing",
        outcomes=MappingProxyType({}),
        prompts=prompts,
        findings_folder=None,
        skip=None,
        prompt_source=None,
        before=None,
        after=None,
    )


def _dispatch(prompt: str | None) -> Dispatch:
    return Dispatch(
        node="plan_writer",
        agent="task-plan-writer",
        prompt=prompt,
        counters=MappingProxyType({}),
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


def test_a_node_without_prompts_runs_no_variant() -> None:
    assert declared_variant(_node(None), _dispatch("revision")) is None
    assert dispatch_variant(_node(None), _dispatch("revision")) is None


def test_an_absent_prompt_runs_initial() -> None:
    assert declared_variant(_node(("initial", "revision")), _dispatch(None)) == "initial"
    assert dispatch_variant(_node(("initial", "revision")), _dispatch(None)) == "initial"


def test_a_carried_prompt_runs_as_given() -> None:
    assert dispatch_variant(_node(("initial", "revision")), _dispatch("revision")) == "revision"


def test_an_undeclared_variant_is_refused_only_by_dispatch_variant() -> None:
    node = _node(("initial", "revision"))
    assert declared_variant(node, _dispatch("rework")) == "rework"
    with pytest.raises(ValueError) as raised:
        dispatch_variant(node, _dispatch("rework"))
    assert str(raised.value) == "graph gives 'plan_writer' the unknown prompt variant 'rework'"


def test_an_absent_initial_is_refused_when_the_node_does_not_declare_it() -> None:
    with pytest.raises(ValueError) as raised:
        dispatch_variant(_node(("revision",)), _dispatch(None))
    assert str(raised.value) == "graph gives 'plan_writer' the unknown prompt variant 'initial'"


_CLOSED = (
    GateRecord("plan_review", "fail", "state/reviews/a.md"),
    GateRecord("arch_review", "pass", None),
    GateRecord("parity_review", "fail", "state/reviews/b.md"),
)


def test_recorded_findings_win_over_the_closed_round() -> None:
    assert findings_files(("state/rf.md",), _CLOSED) == ("state/rf.md",)


def test_without_recorded_findings_the_closed_round_details_are_used_in_order() -> None:
    assert findings_files((), _CLOSED) == ("state/reviews/a.md", "state/reviews/b.md")


def test_with_neither_there_are_no_findings_files() -> None:
    assert findings_files((), (GateRecord("plan_review", "pass", None),)) == ()
