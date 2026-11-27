"""The rule this file exists to enforce: `session_args` passes the shared flags through unchanged
and appends `--add-dir <plugin_dir>` unless `plugin_dir_added`, refusing an `EXECUTOR_FLAGS`
member bare or as `<member>=`; `agent_args` gives an agent naming no MCP server
`--disallowedTools mcp__*` and any other
`--strict-mcp-config --mcp-config <scratch>/mcp-<agent>.json`, the file holding the handed
servers cut to those named, in their given order, as `pnl_agent_flags` did; `session_env`
drops the flow host's launch variables and its `<venv>/bin` `PATH` entry and keeps everything
else.

Every case builds its inputs as literals and writes under `tmp_path`; every expected value is
written from the task plan's rules, never taken from the code's output.

Deliberately not covered:
- Reading `.mcp.json`, which `tests/test_mcp_servers.py` covers.
"""

from pathlib import Path

import pytest

from devscene_flow_host.host.agent_flags import agent_args, session_args, session_env
from devscene_flow_host.records.plugin_contracts import AgentContract

_SCHEMA: dict[str, object] = {"oneOf": []}


def _contract(agent: str, *tools: str) -> AgentContract:
    return AgentContract(agent=agent, tools=tools, return_schema=_SCHEMA)


def test_session_args_appends_the_plugin_directory() -> None:
    assert session_args(["--model", "opus"], Path("/p/plugin"), plugin_dir_added=False) == (
        "--model",
        "opus",
        "--add-dir",
        "/p/plugin",
    )


def test_session_args_passes_shared_flags_unchanged_when_the_directory_is_added() -> None:
    shared = ["--add-dir", "/p/plugin", "--model", "opus"]
    assert session_args(shared, Path("/p/plugin"), plugin_dir_added=True) == (
        "--add-dir",
        "/p/plugin",
        "--model",
        "opus",
    )


@pytest.mark.parametrize(
    ("token", "message"),
    [
        ("--agent", "session_args: the shared flags carry '--agent', a flag the executor sets"),
        (
            "--output-format=json",
            "session_args: the shared flags carry '--output-format=json', a flag the executor sets",
        ),
    ],
)
def test_session_args_refuses_an_executor_flag(token: str, message: str) -> None:
    with pytest.raises(ValueError) as caught:
        session_args(["--model", "opus", token], Path("/p"), plugin_dir_added=False)
    assert str(caught.value) == message


def test_an_agent_with_no_mcp_tool_disallows_every_mcp_tool(tmp_path: Path) -> None:
    contracts = {"plain": _contract("plain", "Read", "Grep")}
    servers = {"docs": {"command": "d"}}
    assert agent_args(contracts, servers, tmp_path) == {
        "plain": ("--disallowedTools", "mcp__*"),
    }
    assert list(tmp_path.iterdir()) == []


def test_an_agent_naming_two_servers_gets_them_cut_in_mapping_order(tmp_path: Path) -> None:
    contracts = {
        "reader": _contract(
            "reader", "Read", "mcp__gamma__find", "mcp__alpha__search", "mcp__alpha__fetch"
        )
    }
    servers = {
        "alpha": {"command": "a", "args": ["x"]},
        "beta": {"command": "b"},
        "gamma": {"url": "http://g"},
    }
    file = tmp_path / "mcp-reader.json"
    assert agent_args(contracts, servers, tmp_path) == {
        "reader": ("--strict-mcp-config", "--mcp-config", str(file)),
    }
    assert file.read_text(encoding="utf-8") == (
        '{"mcpServers":{"alpha":{"command":"a","args":["x"]},"gamma":{"url":"http://g"}}}\n'
    )
    assert sorted(path.name for path in tmp_path.iterdir()) == ["mcp-reader.json"]


def test_an_empty_server_mapping_writes_an_empty_server_set(tmp_path: Path) -> None:
    contracts = {"reader": _contract("reader", "mcp__docs__search")}
    file = tmp_path / "mcp-reader.json"
    assert agent_args(contracts, {}, tmp_path) == {
        "reader": ("--strict-mcp-config", "--mcp-config", str(file)),
    }
    assert file.read_text(encoding="utf-8") == '{"mcpServers":{}}\n'
    assert sorted(path.name for path in tmp_path.iterdir()) == ["mcp-reader.json"]


def test_session_env_drops_the_flow_host_launch_and_keeps_the_rest() -> None:
    environ = {
        "VIRTUAL_ENV": "/s/python/.venv",
        "UV_PROJECT_ENVIRONMENT": "/s/python/.venv",
        "PYTHONPATH": "/s/python/devscene-flow-host/src",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHOME": "/usr",
        "PATH": "/s/python/.venv/bin:/usr/local/bin:/s/python/.venv/bin:/usr/bin",
        "DEVSCENE_MAIN_REPO": "/work/main",
        "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "60000",
    }
    assert session_env(environ, venv=Path("/s/python/.venv")) == {
        "PATH": "/usr/local/bin:/usr/bin",
        "DEVSCENE_MAIN_REPO": "/work/main",
        "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "60000",
    }


def test_session_env_without_a_venv_keeps_path_unchanged() -> None:
    environ = {"PATH": "/s/python/.venv/bin:/usr/bin", "VIRTUAL_ENV": "/s/python/.venv"}
    assert session_env(environ, venv=None) == {"PATH": "/s/python/.venv/bin:/usr/bin"}
