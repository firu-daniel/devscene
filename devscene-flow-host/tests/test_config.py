"""The rule this file exists to enforce: `read_config` reads `stateDir` and `phases` from
`devscene.config.json` as the bash walker's readers do (`hr_config_dir` / `hr_state_dir`,
`hr_phase_enabled`), and raises `RecordError` with one exact line for each record it cannot read.

Every case plants its configuration under `tmp_path`; every expected value is written from the
rules in the task plan, never taken from `read_config`'s output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant
  one under `tmp_path`.
"""

import dataclasses
from pathlib import Path

import pytest

from devscene_flow_host.records.config import HarnessConfig, read_config
from devscene_flow_host.records.errors import RecordError


def _plant(root: Path, text: str) -> Path:
    (root / "devscene.config.json").write_text(text, encoding="utf-8")
    return root


def _plant_bytes(root: Path, data: bytes) -> Path:
    (root / "devscene.config.json").write_bytes(data)
    return root


def test_a_full_configuration_is_read(tmp_path: Path) -> None:
    root = _plant(
        tmp_path,
        '{"defaultBranch": "main", "stateDir": "harness-runs/",'
        ' "phases": {"parity": true, "qa": false}}',
    )
    config = read_config(root)
    assert config.state_dir == "harness-runs"
    assert dict(config.phases) == {"parity": True, "qa": False, "docs": False}
    assert list(config.phases) == ["parity", "qa", "docs"]


def test_an_absent_state_dir_takes_the_default(tmp_path: Path) -> None:
    assert read_config(_plant(tmp_path, "{}")).state_dir == "devscene"


def test_a_state_dir_of_only_slashes_takes_the_default(tmp_path: Path) -> None:
    assert read_config(_plant(tmp_path, '{"stateDir": "/"}')).state_dir == "devscene"


def test_every_trailing_slash_is_stripped(tmp_path: Path) -> None:
    assert read_config(_plant(tmp_path, '{"stateDir": "a//"}')).state_dir == "a"


def test_absent_phases_are_all_off(tmp_path: Path) -> None:
    config = read_config(_plant(tmp_path, "{}"))
    assert dict(config.phases) == {"parity": False, "qa": False, "docs": False}


def test_a_non_boolean_phase_is_unresolvable(tmp_path: Path) -> None:
    config = read_config(_plant(tmp_path, '{"phases": {"qa": "yes"}}'))
    assert dict(config.phases) == {"parity": False, "qa": None, "docs": False}


def test_phases_that_are_not_an_object_are_all_unresolvable(tmp_path: Path) -> None:
    config = read_config(_plant(tmp_path, '{"phases": []}'))
    assert dict(config.phases) == {"parity": None, "qa": None, "docs": None}


def test_a_missing_file_is_a_record_error(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as error:
        read_config(tmp_path)
    assert str(error.value) == f"no devscene.config.json at {tmp_path}"


def test_bytes_that_are_not_utf8_are_not_valid_json(tmp_path: Path) -> None:
    root = _plant_bytes(tmp_path, b'{"stateDir": "\xff"}')
    with pytest.raises(RecordError) as error:
        read_config(root)
    assert str(error.value) == f"{tmp_path / 'devscene.config.json'}: not valid JSON"


def test_text_that_is_not_json_is_not_valid_json(tmp_path: Path) -> None:
    root = _plant(tmp_path, "x")
    with pytest.raises(RecordError) as error:
        read_config(root)
    assert str(error.value) == f"{tmp_path / 'devscene.config.json'}: not valid JSON"


def test_a_top_level_that_is_not_an_object_is_a_record_error(tmp_path: Path) -> None:
    root = _plant(tmp_path, "[]")
    with pytest.raises(RecordError) as error:
        read_config(root)
    assert str(error.value) == f"{tmp_path / 'devscene.config.json'}: not a JSON object"


def test_a_state_dir_that_is_not_a_string_is_a_record_error(tmp_path: Path) -> None:
    root = _plant(tmp_path, '{"stateDir": 3}')
    with pytest.raises(RecordError) as error:
        read_config(root)
    assert str(error.value) == f"{tmp_path / 'devscene.config.json'}: stateDir is not a string"


def test_the_config_is_frozen_and_its_phases_cannot_be_assigned(tmp_path: Path) -> None:
    config: HarnessConfig = read_config(_plant(tmp_path, "{}"))
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.phases = {}  # type: ignore[misc]
    with pytest.raises(TypeError):
        config.phases["qa"] = True  # type: ignore[index]
