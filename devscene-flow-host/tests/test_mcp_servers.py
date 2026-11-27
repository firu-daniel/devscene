"""The rule this file exists to enforce: `read_mcp_servers` reads a worktree's `.mcp.json`
`mcpServers` object as `pnl_agent_flags` read it through `jq '.mcpServers // {}'`, in file order
and read-only, an absent file or an absent or `null` `mcpServers` being an empty mapping, and
raises `RecordError` with one exact line for each shape it cannot read.

Every case plants its file under `tmp_path`; every expected value is written from the task plan's
rules, never taken from the reader's output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

from pathlib import Path

import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.mcp_servers import read_mcp_servers


def _plant(root: Path, data: bytes) -> Path:
    (root / ".mcp.json").write_bytes(data)
    return root


def test_three_servers_are_read_in_file_order(tmp_path: Path) -> None:
    root = _plant(
        tmp_path,
        b'{"mcpServers": {"zeta": {"command": "z"}, "alpha": {"command": "a"},'
        b' "mid": {"url": "http://m"}}, "other": 1}',
    )
    servers = read_mcp_servers(root)
    assert list(servers.items()) == [
        ("zeta", {"command": "z"}),
        ("alpha", {"command": "a"}),
        ("mid", {"url": "http://m"}),
    ]


def test_no_file_is_an_empty_mapping(tmp_path: Path) -> None:
    assert dict(read_mcp_servers(tmp_path)) == {}


def test_an_absent_mcp_servers_is_an_empty_mapping(tmp_path: Path) -> None:
    assert dict(read_mcp_servers(_plant(tmp_path, b'{"other": {}}'))) == {}


def test_a_null_mcp_servers_is_an_empty_mapping(tmp_path: Path) -> None:
    assert dict(read_mcp_servers(_plant(tmp_path, b'{"mcpServers": null}'))) == {}


@pytest.mark.parametrize("data", [b"{not json", b'{"mcpServers": "\xff"}'])
def test_text_that_is_not_json_is_refused(tmp_path: Path, data: bytes) -> None:
    root = _plant(tmp_path, data)
    with pytest.raises(RecordError) as caught:
        read_mcp_servers(root)
    assert str(caught.value) == f"{tmp_path}/.mcp.json: not valid JSON"


def test_a_top_level_that_is_not_an_object_is_refused(tmp_path: Path) -> None:
    root = _plant(tmp_path, b"[]")
    with pytest.raises(RecordError) as caught:
        read_mcp_servers(root)
    assert str(caught.value) == f"{tmp_path}/.mcp.json: not a JSON object"


def test_an_mcp_servers_that_is_not_an_object_is_refused(tmp_path: Path) -> None:
    root = _plant(tmp_path, b'{"mcpServers": []}')
    with pytest.raises(RecordError) as caught:
        read_mcp_servers(root)
    assert str(caught.value) == f"{tmp_path}/.mcp.json: mcpServers is not a JSON object"


def test_the_returned_mapping_refuses_assignment(tmp_path: Path) -> None:
    servers = read_mcp_servers(_plant(tmp_path, b'{"mcpServers": {"a": {}}}'))
    with pytest.raises(TypeError):
        servers["b"] = {}  # type: ignore[index]
