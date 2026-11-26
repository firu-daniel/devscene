"""The rule this file exists to enforce: `ClaudeExecutor` satisfies `graphscene.Executor`, launches
each dispatch with the argument vector its module docstring fixes, returns `judge_session`'s result
— or `Failed("infra", …)` for a launch error or a stall — and calls the usage sink exactly once
immediately before returning, never for a cancelled run; its constructor and `run` refuse each
caller defect with an exact message; and through `graphscene.execute_set` each usage record comes
just before that node's `Launch` row, with equal `result`.

Every session is `fake_claude`, its scenario and files under `tmp_path`, every stream is built from
`session_events`, and every expected value is a literal written from the task plan's rules, never
taken from the executor's output. `duration_seconds` is checked only as a non-negative `float`.
"""

import asyncio
import errno
import json
import os
import time
from collections.abc import Mapping, Sequence
from datetime import UTC
from pathlib import Path
from types import MappingProxyType

import pytest
from graphscene import (
    AttemptBook,
    Completed,
    Dispatch,
    ExecutionLimits,
    Executor,
    Failed,
    Launch,
    UndeliveredBreaker,
    execute_set,
)

from devscene_flow_host.host.claude_executor import ClaudeExecutor, SessionUsage
from devscene_flow_host.records.plugin_contracts import AgentContract
from fake_claude import plant
from session_events import init_event, result_event, return_block

_SCHEMA: Mapping[str, object] = MappingProxyType(
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "oneOf": [
            {
                "type": "object",
                "properties": {
                    "outcome": {"const": "PASS"},
                    "findings_file": {"type": "string"},
                },
                "required": ["outcome"],
                "additionalProperties": False,
            }
        ],
    }
)
_TOOLS = ("Read", "Write")
_CONTRACT = AgentContract(agent="reviewer", tools=_TOOLS, return_schema=_SCHEMA)
_MODEL_USAGE: Mapping[str, object] = {"claude-opus": {"inputTokens": 10, "costUSD": 0.25}}
_BOUNDED_WAIT_SECONDS = 20.0
_POLL_SECONDS = 0.05


class Usages:
    def __init__(self) -> None:
        self.records: list[SessionUsage] = []

    def record(self, usage: SessionUsage) -> None:
        self.records.append(usage)


def _dispatch(prompt: str | None = "Review the plan.", agent: str = "reviewer") -> Dispatch:
    return Dispatch(
        node="plan_review",
        agent=agent,
        prompt=prompt,
        counters={},
        round_number=None,
        converging=None,
        closed_round=(),
        passed=(),
    )


def _executor(
    command: Sequence[str],
    tmp_path: Path,
    sink: Usages,
    *,
    limit: float = 30.0,
    session_args: Sequence[str] = (),
    agent_args: Mapping[str, Sequence[str]] | None = None,
    contracts: Mapping[str, AgentContract] | None = None,
) -> ClaudeExecutor:
    return ClaudeExecutor(
        command=command,
        plugin_dir=tmp_path / "plugin",
        plugin_name="devscene",
        cwd=tmp_path,
        contracts={"reviewer": _CONTRACT} if contracts is None else contracts,
        inactivity_limit_seconds=limit,
        usage_sink=sink,
        session_args=session_args,
        agent_args=agent_args,
        kill_grace_seconds=2.0,
    )


def _stream(document: Mapping[str, object]) -> list[Mapping[str, object]]:
    return [
        {"stdout": init_event(_TOOLS)},
        {
            "stdout": result_event(
                return_block(document),
                total_cost_usd=0.5,
                cache_creation_input_tokens=111,
                cache_read_input_tokens=222,
                model_usage=_MODEL_USAGE,
            )
        },
    ]


def _assert_gone(pid: int) -> None:
    deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(_POLL_SECONDS)
    raise AssertionError(f"process {pid} outlived the executor's run")


def test_the_executor_satisfies_graphscenes_executor_protocol(tmp_path: Path) -> None:
    executor: Executor = _executor(("claude",), tmp_path, Usages())

    assert isinstance(executor, ClaudeExecutor)


def test_the_argument_vector_passes_the_hosts_args_through_in_place(tmp_path: Path) -> None:
    argv_file = tmp_path / "argv.json"
    command = plant(tmp_path, {"argv_file": str(argv_file), "steps": _stream({"outcome": "PASS"})})
    executor = _executor(
        command,
        tmp_path,
        Usages(),
        session_args=("--permission-mode", "dontAsk", "--model", "opus"),
        agent_args={"reviewer": ("--mcp-config", "mcp.json", "--strict-mcp-config")},
    )

    asyncio.run(executor.run(_dispatch()))

    assert json.loads(argv_file.read_text(encoding="utf-8")) == [
        "-p",
        "Review the plan.",
        "--permission-mode",
        "dontAsk",
        "--model",
        "opus",
        "--output-format",
        "stream-json",
        "--verbose",
        "--agent",
        "devscene:reviewer",
        "--plugin-dir",
        str(tmp_path / "plugin"),
        "--mcp-config",
        "mcp.json",
        "--strict-mcp-config",
    ]


def test_a_completed_session_returns_its_absolute_detail_and_one_usage_record(
    tmp_path: Path,
) -> None:
    command = plant(
        tmp_path,
        {"steps": _stream({"outcome": "PASS", "findings_file": "reviews/plan_review.md"})},
    )
    sink = Usages()

    result = asyncio.run(_executor(command, tmp_path, sink).run(_dispatch()))

    expected = Completed("PASS", str(tmp_path / "reviews/plan_review.md"))
    assert result == expected
    assert len(sink.records) == 1
    usage = sink.records[0]
    assert usage.node == "plan_review"
    assert usage.agent == "reviewer"
    assert usage.session_id == "s-1"
    assert usage.total_cost_usd == 0.5
    assert usage.cache_creation_input_tokens == 111
    assert usage.cache_read_input_tokens == 222
    assert usage.model_usage == {"claude-opus": {"inputTokens": 10, "costUSD": 0.25}}
    assert usage.permission_denials == 0
    assert usage.withheld_tools == ()
    assert usage.stalled is False
    assert usage.result == expected
    assert usage.started_at.tzinfo is UTC
    assert isinstance(usage.duration_seconds, float)
    assert usage.duration_seconds >= 0


def test_a_session_with_no_result_event_is_undelivered(tmp_path: Path) -> None:
    command = plant(tmp_path, {"steps": [{"stdout": init_event(_TOOLS)}]})
    sink = Usages()

    result = asyncio.run(_executor(command, tmp_path, sink).run(_dispatch()))

    assert result == Failed("undelivered", "no result event")
    assert [usage.result for usage in sink.records] == [Failed("undelivered", "no result event")]


def test_a_stall_is_an_infra_failure_keeping_the_streams_usage(tmp_path: Path) -> None:
    command = plant(tmp_path, {"steps": [{"stdout": init_event(_TOOLS)}, {"sleep": 600}]})
    sink = Usages()

    result = asyncio.run(_executor(command, tmp_path, sink, limit=0.5).run(_dispatch()))

    expected = Failed("infra", "stalled: the stream was silent for 0.5 s; the session was killed")
    assert result == expected
    assert len(sink.records) == 1
    assert sink.records[0].stalled is True
    assert sink.records[0].session_id == "s-1"
    assert sink.records[0].result == expected


def test_a_cancelled_run_re_raises_kills_the_session_and_reports_no_usage(
    tmp_path: Path,
) -> None:
    pid_file = tmp_path / "fake.pid"
    command = plant(tmp_path, {"pid_file": str(pid_file), "steps": [{"sleep": 600}]})
    sink = Usages()
    executor = _executor(command, tmp_path, sink, limit=600.0)

    async def cancel_once_started() -> None:
        task = asyncio.create_task(executor.run(_dispatch()))
        deadline = time.monotonic() + _BOUNDED_WAIT_SECONDS
        while not pid_file.exists():
            assert time.monotonic() < deadline, "the fake never wrote its pid file"
            await asyncio.sleep(_POLL_SECONDS)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(cancel_once_started())

    _assert_gone(int(pid_file.read_text(encoding="utf-8")))
    assert sink.records == []


def test_a_launch_error_is_an_infra_failure_with_empty_usage(tmp_path: Path) -> None:
    missing = tmp_path / "no-such-claude"
    sink = Usages()

    result = asyncio.run(_executor((str(missing),), tmp_path, sink).run(_dispatch()))

    expected = Failed("infra", f"cannot launch {missing}: {os.strerror(errno.ENOENT)}")
    assert result == expected
    assert len(sink.records) == 1
    usage = sink.records[0]
    assert (
        usage.session_id,
        usage.stalled,
        usage.total_cost_usd,
        usage.cache_creation_input_tokens,
        usage.cache_read_input_tokens,
        dict(usage.model_usage),
        usage.permission_denials,
        usage.withheld_tools,
        usage.result,
    ) == (None, False, None, None, None, {}, 0, (), expected)


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"command": ()}, "ClaudeExecutor: command must not be empty"),
        (
            {"inactivity_limit_seconds": 0.0},
            "ClaudeExecutor: inactivity_limit_seconds must be > 0, got 0.0",
        ),
        (
            {"kill_grace_seconds": -1.0},
            "ClaudeExecutor: kill_grace_seconds must be >= 0, got -1.0",
        ),
        (
            {"session_args": ("--model", "opus", "--verbose", "-p")},
            "ClaudeExecutor: session_args carries '-p', a flag the executor sets",
        ),
        (
            {"session_args": ("--output-format=json",)},
            "ClaudeExecutor: session_args carries '--output-format=json', a flag the executor sets",
        ),
        (
            {"agent_args": {"reviewer": ("--plugin-dir", "elsewhere")}},
            "ClaudeExecutor: agent_args['reviewer'] carries '--plugin-dir', a flag the executor "
            "sets",
        ),
        (
            {"agent_args": {"writer": ("--mcp-config", "mcp.json")}},
            "ClaudeExecutor: agent_args names 'writer', which has no contract",
        ),
        (
            {
                "contracts": {
                    "reviewer": AgentContract(
                        agent="reviewer",
                        tools=_TOOLS,
                        return_schema={"$schema": "http://example.com/no-draft", "oneOf": []},
                    )
                }
            },
            "return schema: $schema 'http://example.com/no-draft' names no draft jsonschema knows",
        ),
    ],
)
def test_the_constructor_refuses_each_caller_defect(
    tmp_path: Path, overrides: Mapping[str, object], message: str
) -> None:
    arguments: dict[str, object] = {
        "command": ("claude",),
        "plugin_dir": tmp_path / "plugin",
        "plugin_name": "devscene",
        "cwd": tmp_path,
        "contracts": {"reviewer": _CONTRACT},
        "inactivity_limit_seconds": 30.0,
        "usage_sink": Usages(),
        **overrides,
    }

    with pytest.raises(ValueError) as raised:
        ClaudeExecutor(**arguments)  # type: ignore[arg-type]

    assert str(raised.value) == message


def test_run_raises_for_an_agent_with_no_contract(tmp_path: Path) -> None:
    executor = _executor(("claude",), tmp_path, Usages())

    with pytest.raises(LookupError) as raised:
        asyncio.run(executor.run(_dispatch(agent="writer")))

    assert str(raised.value) == "plan_review: no agent contract for 'writer'"


def test_run_raises_for_a_dispatch_with_no_prompt(tmp_path: Path) -> None:
    sink = Usages()
    executor = _executor(("claude",), tmp_path, sink)

    with pytest.raises(ValueError) as raised:
        asyncio.run(executor.run(_dispatch(prompt=None)))

    assert str(raised.value) == "plan_review: the dispatch carries no prompt"
    assert sink.records == []


def test_a_later_change_to_the_callers_inputs_changes_nothing(tmp_path: Path) -> None:
    argv_file = tmp_path / "argv.json"
    command = list(
        plant(tmp_path, {"argv_file": str(argv_file), "steps": _stream({"outcome": "PASS"})})
    )
    session_args = ["--model", "opus"]
    contracts = {"reviewer": _CONTRACT}
    executor = _executor(
        command, tmp_path, Usages(), session_args=session_args, contracts=contracts
    )
    command.append("--extra")
    session_args.append("--extra")
    contracts.clear()

    asyncio.run(executor.run(_dispatch()))

    assert json.loads(argv_file.read_text(encoding="utf-8"))[2:4] == ["--model", "opus"]
    assert "--extra" not in json.loads(argv_file.read_text(encoding="utf-8"))


def test_a_repeated_run_launches_the_same_vector_and_reports_twice(tmp_path: Path) -> None:
    argv_file = tmp_path / "argv.json"
    command = plant(tmp_path, {"argv_file": str(argv_file), "steps": _stream({"outcome": "PASS"})})
    sink = Usages()
    executor = _executor(command, tmp_path, sink)

    asyncio.run(executor.run(_dispatch()))
    first = argv_file.read_text(encoding="utf-8")
    argv_file.unlink()
    asyncio.run(executor.run(_dispatch()))
    second = argv_file.read_text(encoding="utf-8")

    assert first == second
    assert [usage.node for usage in sink.records] == ["plan_review", "plan_review"]


class Signals:
    def stop_requested(self) -> bool:
        return False

    def pause_requested(self) -> bool:
        return False


class Counter:
    def __init__(self) -> None:
        self._total = 0

    def total(self) -> int:
        return self._total

    def increment(self) -> int:
        self._total += 1
        return self._total


class EventLog:
    """One log the usage sink and the launch sink both append to, in call order."""

    def __init__(self) -> None:
        self.events: list[tuple[str, str]] = []
        self.usages: list[SessionUsage] = []
        self.launches: list[Launch] = []


class LoggedUsages:
    def __init__(self, log: EventLog) -> None:
        self._log = log

    def record(self, usage: SessionUsage) -> None:
        self._log.events.append(("usage", usage.node))
        self._log.usages.append(usage)


class LoggedLaunches:
    def __init__(self, log: EventLog) -> None:
        self._log = log

    def record(self, launch: Launch) -> None:
        self._log.events.append(("launch", launch.node))
        self._log.launches.append(launch)


def test_through_execute_set_the_usage_record_precedes_its_launch_row(tmp_path: Path) -> None:
    command = plant(tmp_path, {"steps": _stream({"outcome": "PASS"})})
    log = EventLog()
    executor = ClaudeExecutor(
        command=command,
        plugin_dir=tmp_path / "plugin",
        plugin_name="devscene",
        cwd=tmp_path,
        contracts={"reviewer": _CONTRACT},
        inactivity_limit_seconds=30.0,
        usage_sink=LoggedUsages(log),
        kill_grace_seconds=2.0,
    )

    asyncio.run(
        execute_set(
            [_dispatch()],
            executor,
            signals=Signals(),
            counter=Counter(),
            sink=LoggedLaunches(log),
            book=AttemptBook(),
            breaker=UndeliveredBreaker(),
            limits=ExecutionLimits(backoff_seconds=0),
            failure_outcome="FAIL",
        )
    )

    assert log.events == [("usage", "plan_review"), ("launch", "plan_review")]
    assert log.launches[0].result == Completed("PASS", None)
    assert log.launches[0].result == log.usages[0].result
