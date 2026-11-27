"""The rule this file exists to enforce: `read_max_total_dispatches` reads the planning core's
`MAX_TOTAL_DISPATCHES = <n>` as `pnl_init` read it, from under `## Setup (once per session)` only,
base-10, and raises `RecordError` with one exact line for each core it cannot read.

Every case but the last plants a plugin directory under `tmp_path`; the last reads the real
`plugin/instructions/task_plan_writing_instructions_core.md` read-only. Every expected value is
written from the task plan's rules or from reading that file, never taken from the reader's output.

Deliberately not covered:
- An `OSError` other than a missing file, which propagates unwrapped: no portable way to plant one
  under `tmp_path`.
"""

from pathlib import Path
from typing import Final

import pytest

from devscene_flow_host.records.core_limits import read_max_total_dispatches
from devscene_flow_host.records.errors import RecordError

_PLUGIN: Final = Path(__file__).resolve().parents[2] / "plugin"
_CORE: Final = "instructions/task_plan_writing_instructions_core.md"


def _plant(plugin_dir: Path, data: bytes) -> Path:
    path = plugin_dir / _CORE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def test_the_value_under_the_setup_heading_is_read(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"# Core\n\n## Setup (once per session)\r\n\n"
        b"4. Set:\n   - `MAX_TOTAL_DISPATCHES = 40` - a backstop.\r\n\n## Loop\n",
    )
    assert read_max_total_dispatches(tmp_path) == 40


def test_a_marker_outside_the_setup_section_is_ignored(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        b"## Intro\nMAX_TOTAL_DISPATCHES = 7\n"
        b"## Setup (once per session)\nMAX_TOTAL_DISPATCHES = 12\n"
        b"## Loop\nMAX_TOTAL_DISPATCHES = 99\n",
    )
    assert read_max_total_dispatches(tmp_path) == 12


def test_a_value_with_leading_zeros_is_read_base_10(tmp_path: Path) -> None:
    _plant(tmp_path, b"## Setup (once per session)\nMAX_TOTAL_DISPATCHES = 010\n")
    assert read_max_total_dispatches(tmp_path) == 10


def test_a_missing_core_is_a_record_error(tmp_path: Path) -> None:
    with pytest.raises(RecordError) as error:
        read_max_total_dispatches(tmp_path)
    assert str(error.value) == f"the planning core '{tmp_path / _CORE}' does not exist"


def test_a_core_that_is_not_utf8_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(tmp_path, b"## Setup (once per session)\n\xff\n")
    with pytest.raises(RecordError) as error:
        read_max_total_dispatches(tmp_path)
    assert str(error.value) == f"{path}: not UTF-8 text"


def test_a_core_with_no_marker_under_the_setup_heading_is_a_record_error(tmp_path: Path) -> None:
    path = _plant(
        tmp_path,
        b"## Setup (once per session)\nNo cap here.\n## Loop\nMAX_TOTAL_DISPATCHES = 40\n",
    )
    with pytest.raises(RecordError) as error:
        read_max_total_dispatches(tmp_path)
    assert str(error.value) == (
        f"no 'MAX_TOTAL_DISPATCHES = <n>' line under '## Setup (once per session)' in '{path}'"
    )


def test_the_real_planning_core_declares_forty() -> None:
    assert read_max_total_dispatches(_PLUGIN) == 40
