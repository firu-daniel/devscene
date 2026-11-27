"""The rule this file exists to enforce: an executor's results, `Completed` and `Failed`, are
immutable plain types with fixed `kind` discriminators and three failure classes, and `Executor` is
a structural protocol a caller satisfies without subclassing, including by wrapping blocking work in
`asyncio.to_thread` (`graphscene.model.execution`).

The protocol cases are graded by `mypy`, which checks each in-test class against the annotated
local it is assigned to; at run time they show the coroutine runs and returns the expected result.
"""

import asyncio
import dataclasses
import typing
from types import MappingProxyType

import pytest

from graphscene.model.execution import Completed, Executor, Failed, FailureClass, NodeResult
from graphscene.model.walk_actions import Dispatch


def _dispatch(node: str) -> Dispatch:
    return Dispatch(
        node=node,
        agent="writer",
        prompt_variant=None,
        counters=MappingProxyType({}),
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


@pytest.mark.parametrize(
    "instance",
    (Completed("done", "plan.md"), Failed("infra", "crashed")),
    ids=lambda i: type(i).__name__,
)
def test_every_result_is_frozen(instance: object) -> None:
    first_field = dataclasses.fields(instance)[0].name  # type: ignore[arg-type]
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(instance, first_field, "changed")


def test_a_completed_detail_defaults_to_none() -> None:
    assert Completed("done").detail is None


def test_each_result_carries_its_kind() -> None:
    assert Completed.kind == "completed"
    assert Failed.kind == "failed"


def test_the_failure_classes_are_infra_agent_and_undelivered_in_order() -> None:
    assert typing.get_args(FailureClass) == ("infra", "agent", "undelivered")


class _ByNode:
    async def run(self, dispatch: Dispatch) -> NodeResult:
        if dispatch.node == "draft":
            return Completed("written", "plan.md")
        return Failed("agent", "the agent reported failure")


def test_a_plain_class_with_an_async_run_is_an_executor() -> None:
    executor: Executor = _ByNode()
    assert asyncio.run(executor.run(_dispatch("draft"))) == Completed("written", "plan.md")
    assert asyncio.run(executor.run(_dispatch("review"))) == Failed(
        "agent", "the agent reported failure"
    )


def _blocking_work(node: str) -> str:
    return f"{node} ran"


class _Blocking:
    async def run(self, dispatch: Dispatch) -> NodeResult:
        detail = await asyncio.to_thread(_blocking_work, dispatch.node)
        return Completed("done", detail)


def test_blocking_work_wrapped_in_to_thread_is_an_executor() -> None:
    executor: Executor = _Blocking()
    assert asyncio.run(executor.run(_dispatch("draft"))) == Completed("done", "draft ran")
