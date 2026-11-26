"""The rule this file exists to enforce: `read_plugin_name` and `read_agent_contract` read the
plugin's manifest name, an agent's `tools:` line and its return schema as the bash readers do
(`pnl_init`, `pnl_agent_tools_var`, `pnl_load_schemas`), raise `RecordError` with one exact line
for each record they cannot read, and raise `ValueError` for a name that is not an agent name.

Every refusal and the clean case plant a plugin under `tmp_path`; one case reads this checkout's
own tracked plugin files as read-only input. Every expected value is written from the task plan's
rules or from reading the named plugin files, never taken from the reader's output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

import dataclasses
from pathlib import Path

import graphscene
import pytest

from devscene_flow_host.records.errors import RecordError
from devscene_flow_host.records.plugin_contracts import (
    AgentContract,
    read_agent_contract,
    read_plugin_name,
)

_CHECKOUT_PLUGIN = Path(__file__).resolve().parents[2] / "plugin"
_SCHEMA = '{"oneOf": []}'
_DEFINITION = "---\nname: a\ntools: Read\n---\n"


def _plant_manifest(plugin_dir: Path, data: bytes) -> Path:
    (plugin_dir / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    path = plugin_dir / ".claude-plugin" / "plugin.json"
    path.write_bytes(data)
    return path


def _plant_agent(plugin_dir: Path, definition: bytes | None, schema: bytes | None) -> None:
    if definition is not None:
        (plugin_dir / "agents").mkdir(parents=True, exist_ok=True)
        (plugin_dir / "agents" / "a.md").write_bytes(definition)
    if schema is not None:
        (plugin_dir / "schemas").mkdir(parents=True, exist_ok=True)
        (plugin_dir / "schemas" / "a.return.json").write_bytes(schema)


def test_a_missing_manifest_is_a_record_error(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as error:
        read_plugin_name(tmp_path)
    assert str(error.value) == f"no .claude-plugin/plugin.json under {tmp_path}"


@pytest.mark.parametrize("data", [b'{"name": "\xff"}', b"x"])
def test_a_manifest_that_is_not_utf8_json_is_not_valid_json(tmp_path: Path, data: bytes) -> None:
    path = _plant_manifest(tmp_path, data)
    with pytest.raises(RecordError) as error:
        read_plugin_name(tmp_path)
    assert str(error.value) == f"{path}: not valid JSON"


def test_a_manifest_that_is_not_an_object_is_a_record_error(tmp_path: Path) -> None:
    path = _plant_manifest(tmp_path, b'["devscene"]')
    with pytest.raises(RecordError) as error:
        read_plugin_name(tmp_path)
    assert str(error.value) == f"{path}: not a JSON object"


@pytest.mark.parametrize("data", [b"{}", b'{"name": ""}', b'{"name": 3}', b'{"name": null}'])
def test_a_manifest_with_no_non_empty_name_is_a_record_error(tmp_path: Path, data: bytes) -> None:
    path = _plant_manifest(tmp_path, data)
    with pytest.raises(RecordError) as error:
        read_plugin_name(tmp_path)
    assert str(error.value) == f"{path}: carries no non-empty name"


def test_a_missing_agent_definition_is_a_record_error(tmp_path: Path) -> None:
    _plant_agent(tmp_path, None, _SCHEMA.encode())
    with pytest.raises(RecordError) as error:
        read_agent_contract(tmp_path, "a")
    assert str(error.value) == f"no agent definition at {tmp_path / 'agents' / 'a.md'}"


@pytest.mark.parametrize(
    "definition",
    [
        b"name: a\ntools: Read\n",
        b"---\nname: a\n---\ntools: Read\n",
        b"---\nname: a\ntools: , ,\t\n---\n",
        b"---\nname: a\n",
        b"",
    ],
    ids=["no-opening-fence", "tools-after-closing-fence", "empty-list", "no-tools-line", "empty"],
)
def test_a_definition_with_no_tools_line_is_a_record_error(
    tmp_path: Path, definition: bytes
) -> None:
    _plant_agent(tmp_path, definition, _SCHEMA.encode())
    with pytest.raises(RecordError) as error:
        read_agent_contract(tmp_path, "a")
    assert str(error.value) == f"{tmp_path / 'agents' / 'a.md'}: carries no tools: line"


def test_a_missing_return_schema_is_a_record_error(tmp_path: Path) -> None:
    _plant_agent(tmp_path, _DEFINITION.encode(), None)
    with pytest.raises(RecordError) as error:
        read_agent_contract(tmp_path, "a")
    assert str(error.value) == f"no return schema at {tmp_path / 'schemas' / 'a.return.json'}"


@pytest.mark.parametrize(
    "schema",
    [b'{"oneOf": ["\xff"]}', b"x", b"", b'{"oneOf": []} {"oneOf": []}', b"[]"],
    ids=["not-utf8", "not-json", "empty", "two-objects", "an-array"],
)
def test_a_schema_that_is_not_one_object_is_a_record_error(tmp_path: Path, schema: bytes) -> None:
    _plant_agent(tmp_path, _DEFINITION.encode(), schema)
    with pytest.raises(RecordError) as error:
        read_agent_contract(tmp_path, "a")
    assert str(error.value) == f"{tmp_path / 'schemas' / 'a.return.json'}: is not one JSON object"


@pytest.mark.parametrize("schema", [b"{}", b'{"oneOf": {}}', b'{"anyOf": []}'])
def test_a_schema_with_no_top_level_one_of_array_is_a_record_error(
    tmp_path: Path, schema: bytes
) -> None:
    _plant_agent(tmp_path, _DEFINITION.encode(), schema)
    with pytest.raises(RecordError) as error:
        read_agent_contract(tmp_path, "a")
    expected = f"{tmp_path / 'schemas' / 'a.return.json'}: carries no top-level oneOf array"
    assert str(error.value) == expected


@pytest.mark.parametrize("agent", ["", "A", "-a", "a/b", "../a", "a\n", "a_b"])
def test_a_name_that_is_not_an_agent_name_is_a_value_error(tmp_path: Path, agent: str) -> None:
    with pytest.raises(ValueError) as error:
        read_agent_contract(tmp_path, agent)
    assert str(error.value) == f"not an agent name: {agent!r}"


def test_a_clean_planted_agent_is_read(tmp_path: Path) -> None:
    definition = b"---\r\nname: a\r\ntools:  Read ,\tGrep,, mcp__docs__search \r\n---\r\nBody\r\n"
    _plant_agent(tmp_path, definition, b'{"title": "a", "oneOf": [{"type": "object"}]}')
    contract = read_agent_contract(tmp_path, "a")
    assert contract.agent == "a"
    assert contract.tools == ("Read", "Grep", "mcp__docs__search")
    assert dict(contract.return_schema) == {"title": "a", "oneOf": [{"type": "object"}]}


def test_the_contract_is_frozen_and_its_schema_cannot_be_assigned(tmp_path: Path) -> None:
    _plant_agent(tmp_path, _DEFINITION.encode(), _SCHEMA.encode())
    contract: AgentContract = read_agent_contract(tmp_path, "a")
    with pytest.raises(dataclasses.FrozenInstanceError):
        contract.tools = ()  # type: ignore[misc]
    with pytest.raises(TypeError):
        contract.return_schema["oneOf"] = []  # type: ignore[index]


def test_this_checkouts_plugin_is_read() -> None:
    assert read_plugin_name(_CHECKOUT_PLUGIN) == "devscene"
    contract = read_agent_contract(_CHECKOUT_PLUGIN, "task-plan-reviewer")
    assert contract.tools == (
        "Read",
        "Glob",
        "Grep",
        "Bash",
        "Write",
        "mcp__devscene-docs__search_docs",
    )
    assert contract.return_schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert graphscene.return_violations({}, contract.return_schema) != []
