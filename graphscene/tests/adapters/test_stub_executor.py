"""The rule this file exists to enforce: `graphscene.adapters.stub_executor.StubExecutor` satisfies
`Executor` structurally, plays each node's script in order from its own copy, raises on an
exhausted node and a negative delay with exact text, records started, finished and cancelled
nodes, and re-raises cancellation out of a stall or a delay rather than returning a result.

No duration is asserted: order is read from the record, never by timing a run.
"""

import asyncio
import math
from types import MappingProxyType

import pytest

from graphscene.adapters.stub_executor import (
    Scripted,
    ScriptedFailure,
    ScriptedOutcome,
    ScriptedStall,
    StubExecutor,
)
from graphscene.model.execution import Completed, Executor, Failed, FailureClass, NodeResult
from graphscene.model.walk_actions import Dispatch


def _dispatch(node: str, round_number: int | None = None) -> Dispatch:
    return Dispatch(
        node=node,
        agent="reviewer",
        prompt=None,
        counters=MappingProxyType({}),
        round_number=round_number,
        converging=None,
        closed_round=(),
        passed=(),
    )


def test_the_stub_satisfies_the_executor_protocol() -> None:
    executor: Executor = StubExecutor({"draft": [ScriptedOutcome("done")]})
    assert asyncio.run(executor.run(_dispatch("draft"))) == Completed("done", None)


def test_a_scripted_outcome_returns_its_completed() -> None:
    stub = StubExecutor({"draft": [ScriptedOutcome("done", "notes.md")]})
    assert asyncio.run(stub.run(_dispatch("draft"))) == Completed("done", "notes.md")
    assert stub.started == ("draft",)
    assert stub.finished == ("draft",)
    assert stub.cancelled == ()


@pytest.mark.parametrize("failure", ("infra", "agent", "undelivered"))
def test_each_failure_class_returns_its_failed(failure: FailureClass) -> None:
    stub = StubExecutor({"draft": [ScriptedFailure(failure, "went wrong")]})
    assert asyncio.run(stub.run(_dispatch("draft"))) == Failed(failure, "went wrong")
    assert stub.finished == ("draft",)


def test_a_node_scripted_twice_returns_its_entries_in_order() -> None:
    stub = StubExecutor({"draft": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("done")]})

    async def twice() -> tuple[NodeResult, NodeResult]:
        return await stub.run(_dispatch("draft")), await stub.run(_dispatch("draft"))

    assert asyncio.run(twice()) == (Failed("infra", "crashed"), Completed("done", None))
    assert stub.started == ("draft", "draft")


def test_an_exhausted_node_raises_lookup_error() -> None:
    stub = StubExecutor({"draft": [ScriptedOutcome("done")]})

    async def twice() -> None:
        await stub.run(_dispatch("draft"))
        await stub.run(_dispatch("draft"))

    with pytest.raises(LookupError) as raised:
        asyncio.run(twice())
    assert str(raised.value) == "draft: the stub has no scripted run left"


def test_an_unscripted_node_raises_lookup_error() -> None:
    stub = StubExecutor({})
    with pytest.raises(LookupError) as raised:
        asyncio.run(stub.run(_dispatch("review")))
    assert str(raised.value) == "review: the stub has no scripted run left"


def test_a_negative_delay_is_refused() -> None:
    with pytest.raises(ValueError) as outcome:
        ScriptedOutcome("done", delay=-1.0)
    assert str(outcome.value) == "ScriptedOutcome: delay must be >= 0, got -1.0"
    with pytest.raises(ValueError) as failure:
        ScriptedFailure("agent", "refused", delay=-0.5)
    assert str(failure.value) == "ScriptedFailure: delay must be >= 0, got -0.5"
    with pytest.raises(ValueError) as nan:
        ScriptedOutcome("done", delay=math.nan)
    assert str(nan.value) == "ScriptedOutcome: delay must be >= 0, got nan"


def test_mutating_the_script_after_construction_changes_nothing() -> None:
    entries: list[Scripted] = [ScriptedOutcome("done")]
    script: dict[str, list[Scripted]] = {"draft": entries}
    stub = StubExecutor(script)
    entries.clear()
    entries.append(ScriptedOutcome("changed"))
    script["draft"] = []
    script["review"] = [ScriptedOutcome("added")]

    assert asyncio.run(stub.run(_dispatch("draft"))) == Completed("done", None)
    with pytest.raises(LookupError) as raised:
        asyncio.run(stub.run(_dispatch("review")))
    assert str(raised.value) == "review: the stub has no scripted run left"


def test_concurrent_gates_finish_in_delay_order_not_call_order() -> None:
    stub = StubExecutor(
        {
            "security": [ScriptedOutcome("pass", delay=0.05)],
            "style": [ScriptedOutcome("pass", delay=0.0)],
            "tests": [ScriptedFailure("agent", "found a defect", delay=0.0)],
        }
    )

    async def round_of_three() -> list[NodeResult]:
        return list(
            await asyncio.gather(
                stub.run(_dispatch("security", round_number=1)),
                stub.run(_dispatch("style", round_number=1)),
                stub.run(_dispatch("tests", round_number=1)),
            )
        )

    assert asyncio.run(round_of_three()) == [
        Completed("pass", None),
        Completed("pass", None),
        Failed("agent", "found a defect"),
    ]
    assert stub.started == ("security", "style", "tests")
    assert stub.finished == ("style", "tests", "security")


def test_a_stall_is_cancelled_by_the_callers_deadline() -> None:
    stub = StubExecutor({"draft": [ScriptedStall()]})

    async def with_deadline() -> NodeResult:
        return await asyncio.wait_for(stub.run(_dispatch("draft")), timeout=0.01)

    with pytest.raises(TimeoutError):
        asyncio.run(with_deadline())
    assert stub.started == ("draft",)
    assert stub.cancelled == ("draft",)
    assert stub.finished == ()


def test_a_delayed_result_is_cancelled_by_the_callers_deadline() -> None:
    stub = StubExecutor({"draft": [ScriptedOutcome("done", delay=60.0)]})

    async def with_deadline() -> NodeResult:
        return await asyncio.wait_for(stub.run(_dispatch("draft")), timeout=0.01)

    with pytest.raises(TimeoutError):
        asyncio.run(with_deadline())
    assert stub.started == ("draft",)
    assert stub.cancelled == ("draft",)
    assert stub.finished == ()
