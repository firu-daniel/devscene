"""Reads a worktree's `.mcp.json` into its MCP servers.

The rule: `read_mcp_servers` reads the file's `mcpServers` object as `pnl_agent_flags` read it,
through `jq '.mcpServers // {}'` (`cli/templates/scripts/lib/planning-node-lib.sh`, in that file's
history): server name to its configuration, in file order, read-only. An absent file, and an
absent or `null` `mcpServers`, are each an empty mapping. It reads values and decides nothing
with them.

Deliberately not covered:
- Which servers an agent may use, and writing any file: `host/agent_flags.py`'s.
- Each server entry's own shape, which `claude` checks.
"""

import json
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Final

from devscene_flow_host.records.errors import RecordError

MCP_CONFIG_FILENAME: Final = ".mcp.json"
_SERVERS_KEY: Final = "mcpServers"


def read_mcp_servers(worktree: Path) -> Mapping[str, object]:
    path = worktree / MCP_CONFIG_FILENAME
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return MappingProxyType({})
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RecordError(f"{path}: not valid JSON") from None
    if not isinstance(document, dict):
        raise RecordError(f"{path}: not a JSON object")
    servers = document.get(_SERVERS_KEY)
    if servers is None:
        return MappingProxyType({})
    if not isinstance(servers, dict):
        raise RecordError(f"{path}: {_SERVERS_KEY} is not a JSON object")
    return MappingProxyType(servers)
