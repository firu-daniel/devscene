"""The rule this file exists to enforce: the package root exposes exactly the graph-model, checker
and walker surface, and each name it exposes is the object its own module defines.

`__all__` is compared as a list, so adding, removing or reordering a name is a reviewed change.
"""

import pytest

import graphscene
import graphscene.adapters.return_schema
import graphscene.adapters.state_file
import graphscene.adapters.stub_executor
import graphscene.engine.attempts
import graphscene.engine.breaker
import graphscene.engine.run_loop
import graphscene.engine.safety
import graphscene.engine.set_execution
import graphscene.engine.static_check
import graphscene.engine.vocabulary
import graphscene.engine.walker
import graphscene.facade
import graphscene.facade.loading
import graphscene.model.errors
import graphscene.model.execution
import graphscene.model.flow_graph
import graphscene.model.hooks
import graphscene.model.run_control
import graphscene.model.walk_actions
import graphscene.model.walk_state

_EXPECTED: list[str] = [
    "load_graph",
    "load_graph_file",
    "GraphError",
    "Stage",
    "Violation",
    "vocabulary_violations",
    "static_violations",
    "FlowGraph",
    "NodeKind",
    "Primitive",
    "Verdict",
    "BindingDeclaration",
    "Edge",
    "Node",
    "OutcomeDeclaration",
    "InterruptBinding",
    "StopBinding",
    "EndBinding",
    "PredicateDeclaration",
    "HookDeclaration",
    "Vocabulary",
    "CounterDeclaration",
    "OnCapEdge",
    "RouteEdge",
    "BindingEdge",
    "SkipEntry",
    "DispatchNode",
    "RoundNode",
    "TerminalNode",
    "Walker",
    "FileStateStore",
    "StateStore",
    "PredicateHost",
    "WalkState",
    "OpenRound",
    "RoundResume",
    "Awaiting",
    "Step",
    "Action",
    "Dispatch",
    "DispatchSet",
    "Wait",
    "Interrupt",
    "Stop",
    "End",
    "Refused",
    "GateRecord",
    "Passage",
    "SkipPassage",
    "RoundPassage",
    "LedgerPassage",
    "Executor",
    "NodeResult",
    "Completed",
    "Failed",
    "FailureClass",
    "return_violations",
    "StubExecutor",
    "Scripted",
    "ScriptedOutcome",
    "ScriptedFailure",
    "ScriptedStall",
    "ExecutionLimits",
    "HaltReason",
    "Halt",
    "NodeRecord",
    "Recorded",
    "Retry",
    "Redispatch",
    "Settlement",
    "SetResult",
    "Launch",
    "RunSignals",
    "DispatchCounter",
    "LaunchSink",
    "clear_set",
    "UndeliveredBreaker",
    "AttemptBook",
    "execute_set",
    "RunExit",
    "start_run",
    "continue_run",
    "HookHost",
    "HookCall",
    "BeforeDispatch",
    "AfterDispatch",
    "BeforeRound",
    "AfterRound",
    "BeforeEnd",
]

_DEFINED_IN: dict[str, object] = {
    "load_graph": graphscene.facade.loading,
    "load_graph_file": graphscene.facade.loading,
    "GraphError": graphscene.model.errors,
    "Stage": graphscene.model.errors,
    "Violation": graphscene.model.errors,
    "vocabulary_violations": graphscene.engine.vocabulary,
    "static_violations": graphscene.engine.static_check,
    # FlowGraph through TerminalNode, HookDeclaration among them.
    **{name: graphscene.model.flow_graph for name in _EXPECTED[7:29]},
    "Walker": graphscene.engine.walker,
    "FileStateStore": graphscene.adapters.state_file,
    "StateStore": graphscene.model.walk_state,
    "PredicateHost": graphscene.model.walk_state,
    "WalkState": graphscene.model.walk_state,
    "OpenRound": graphscene.model.walk_state,
    "RoundResume": graphscene.model.walk_state,
    "Awaiting": graphscene.model.walk_state,
    "Step": graphscene.model.walk_actions,
    "Action": graphscene.model.walk_actions,
    "Dispatch": graphscene.model.walk_actions,
    "DispatchSet": graphscene.model.walk_actions,
    "Wait": graphscene.model.walk_actions,
    "Interrupt": graphscene.model.walk_actions,
    "Stop": graphscene.model.walk_actions,
    "End": graphscene.model.walk_actions,
    "Refused": graphscene.model.walk_actions,
    "GateRecord": graphscene.model.walk_actions,
    "Passage": graphscene.model.walk_actions,
    "SkipPassage": graphscene.model.walk_actions,
    "RoundPassage": graphscene.model.walk_actions,
    "LedgerPassage": graphscene.model.walk_actions,
    "Executor": graphscene.model.execution,
    "NodeResult": graphscene.model.execution,
    "Completed": graphscene.model.execution,
    "Failed": graphscene.model.execution,
    "FailureClass": graphscene.model.execution,
    "return_violations": graphscene.adapters.return_schema,
    "StubExecutor": graphscene.adapters.stub_executor,
    "Scripted": graphscene.adapters.stub_executor,
    "ScriptedOutcome": graphscene.adapters.stub_executor,
    "ScriptedFailure": graphscene.adapters.stub_executor,
    "ScriptedStall": graphscene.adapters.stub_executor,
    "ExecutionLimits": graphscene.model.run_control,
    "HaltReason": graphscene.model.run_control,
    "Halt": graphscene.model.run_control,
    "NodeRecord": graphscene.model.run_control,
    "Recorded": graphscene.model.run_control,
    "Retry": graphscene.model.run_control,
    "Redispatch": graphscene.model.run_control,
    "Settlement": graphscene.model.run_control,
    "SetResult": graphscene.model.run_control,
    "Launch": graphscene.model.run_control,
    "RunSignals": graphscene.model.run_control,
    "DispatchCounter": graphscene.model.run_control,
    "LaunchSink": graphscene.model.run_control,
    "clear_set": graphscene.engine.safety,
    "UndeliveredBreaker": graphscene.engine.breaker,
    "AttemptBook": graphscene.engine.attempts,
    "execute_set": graphscene.engine.set_execution,
    "RunExit": graphscene.model.run_control,
    "start_run": graphscene.engine.run_loop,
    "continue_run": graphscene.engine.run_loop,
    "HookHost": graphscene.model.hooks,
    "HookCall": graphscene.model.hooks,
    "BeforeDispatch": graphscene.model.hooks,
    "AfterDispatch": graphscene.model.hooks,
    "BeforeRound": graphscene.model.hooks,
    "AfterRound": graphscene.model.hooks,
    "BeforeEnd": graphscene.model.hooks,
}


def test_the_public_surface_is_exactly_the_graph_model() -> None:
    assert graphscene.__all__ == _EXPECTED


@pytest.mark.parametrize("name", _EXPECTED)
def test_each_public_name_is_the_object_its_module_defines(name: str) -> None:
    assert getattr(graphscene, name) is getattr(_DEFINED_IN[name], name)


def test_the_unvalidated_builder_is_not_exported() -> None:
    assert "build_flow_graph" not in graphscene.__all__


def test_the_named_examples_resolve_to_their_modules() -> None:
    assert graphscene.load_graph is graphscene.facade.loading.load_graph
    assert graphscene.Violation is graphscene.model.errors.Violation


def test_the_facade_exposes_exactly_the_root_surface() -> None:
    assert graphscene.facade.__all__ == graphscene.__all__
