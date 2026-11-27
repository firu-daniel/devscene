"""The session args, per-agent MCP flags and session environment `ClaudeExecutor` takes from the
host.

The rule: each function builds its value as the retired bash pilot did
(`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`, in that file's history).
- `session_args` passes the watcher's shared flags through unchanged and appends
  `--add-dir <plugin_dir>` unless they already carry it, the bash `PD_PLUGIN_DIR_ADDED`. A shared
  flag that is an `EXECUTOR_FLAGS` member, bare or as `<member>=`, raises `ValueError` before any
  session.
- `agent_args` gives an agent whose `tools` name no `mcp__<server>__…` tool
  `--disallowedTools mcp__*`; any other agent `--strict-mcp-config --mcp-config` with a file
  `<scratch>/mcp-<agent>.json` holding `{"mcpServers": {…}}`, the servers it is handed cut to
  those named, in their given order. It writes nothing outside `scratch`.
- `session_env` drops `FLOW_HOST_LAUNCH_VARIABLES` and, given the flow host's environment
  directory, the `PATH` entries equal to its `bin`: the variables the flow host's `uv` launch
  adds (`cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_exec`), so no node
  session inherits the flow host's Python environment. Every other variable is kept.

Deliberately not covered:
- Reading `.mcp.json`, which is `records/mcp_servers.py`'s.
- Removing the scratch directory, which is its owner's.
- The watcher's shared flags themselves.
"""

import json
import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Final

from devscene_flow_host.host.claude_executor import EXECUTOR_FLAGS
from devscene_flow_host.records.plugin_contracts import AgentContract

FLOW_HOST_LAUNCH_VARIABLES: Final = (
    "VIRTUAL_ENV",
    "UV_PROJECT_ENVIRONMENT",
    "PYTHONPATH",
    "PYTHONDONTWRITEBYTECODE",
    "PYTHONHOME",
)
_MCP_TOOL_PREFIX: Final = "mcp__"
_MCP_TOOL_SEPARATOR: Final = "__"


def session_args(
    shared: Sequence[str], plugin_dir: Path, *, plugin_dir_added: bool
) -> tuple[str, ...]:
    for token in shared:
        if any(token == flag or token.startswith(f"{flag}=") for flag in EXECUTOR_FLAGS):
            raise ValueError(
                f"session_args: the shared flags carry '{token}', a flag the executor sets"
            )
    if plugin_dir_added:
        return tuple(shared)
    return (*shared, "--add-dir", str(plugin_dir))


def agent_args(
    contracts: Mapping[str, AgentContract], mcp_servers: Mapping[str, object], scratch: Path
) -> dict[str, tuple[str, ...]]:
    args: dict[str, tuple[str, ...]] = {}
    for agent, contract in contracts.items():
        named = _servers_named(contract.tools)
        if not named:
            args[agent] = ("--disallowedTools", "mcp__*")
            continue
        if "/" in agent or os.sep in agent:
            raise ValueError(f"agent_args: '{agent}' cannot name a file under {scratch}")
        path = scratch / f"mcp-{agent}.json"
        cut = {server: config for server, config in mcp_servers.items() if server in named}
        document = json.dumps({"mcpServers": cut}, ensure_ascii=False, separators=(",", ":"))
        path.write_text(f"{document}\n", encoding="utf-8")
        args[agent] = ("--strict-mcp-config", "--mcp-config", str(path))
    return args


def _servers_named(tools: Sequence[str]) -> frozenset[str]:
    servers: set[str] = set()
    for tool in tools:
        if not tool.startswith(_MCP_TOOL_PREFIX):
            continue
        rest = tool[len(_MCP_TOOL_PREFIX) :]
        server, separator, _ = rest.partition(_MCP_TOOL_SEPARATOR)
        if server and separator:
            servers.add(server)
    return frozenset(servers)


def session_env(environ: Mapping[str, str], *, venv: Path | None) -> dict[str, str]:
    env = {name: value for name, value in environ.items() if name not in FLOW_HOST_LAUNCH_VARIABLES}
    if venv is not None and "PATH" in env:
        venv_bin = str(venv / "bin")
        entries = env["PATH"].split(os.pathsep)
        env["PATH"] = os.pathsep.join(entry for entry in entries if entry != venv_bin)
    return env
