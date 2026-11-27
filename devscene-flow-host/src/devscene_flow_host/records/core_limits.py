"""Reads the planning core's `MAX_TOTAL_DISPATCHES`.

The rule: `read_max_total_dispatches` reads the planning core as `pnl_init` read it
(`cli/templates/scripts/lib/planning-node-lib.sh`, retired): a trailing CR is stripped from every
line; a line equal to `## Setup (once per session)` opens the setup section and any other `## `
line closes it; inside it, the first line carrying the marker followed by a digit ends the search,
and its value is the run of digits after the line's first marker, read base-10. It reads the value
and decides nothing with it.

Deliberately not covered:
- Using the value as a dispatch cap: the caller's.
- Cutting the core's prompt blocks: `records/prompt_blocks.py`'s.
"""

import re
from pathlib import Path
from typing import Final

from devscene_flow_host.records.errors import RecordError

CORE_DOCUMENT: Final = "instructions/task_plan_writing_instructions_core.md"
SETUP_HEADING: Final = "## Setup (once per session)"
MAX_DISPATCHES_MARKER: Final = "MAX_TOTAL_DISPATCHES = "
_SECTION_PREFIX: Final = "## "
_MARKED_VALUE: Final = re.compile(re.escape(MAX_DISPATCHES_MARKER) + "[0-9]")
_DIGITS: Final = re.compile("[0-9]*")


def read_max_total_dispatches(plugin_dir: Path) -> int:
    path = plugin_dir / CORE_DOCUMENT
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise RecordError(f"the planning core '{path}' does not exist") from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise RecordError(f"{path}: not UTF-8 text") from None

    in_setup = False
    for raw_line in text.split("\n"):
        line = raw_line.removesuffix("\r")
        if line.startswith(_SECTION_PREFIX):
            in_setup = line == SETUP_HEADING
            continue
        if in_setup and _MARKED_VALUE.search(line):
            # `${line#*MARKER}` cuts at the first marker, which need not be the digit-led one.
            after = line[line.index(MAX_DISPATCHES_MARKER) + len(MAX_DISPATCHES_MARKER) :]
            digits = _DIGITS.match(after)
            if digits and digits.group():
                return int(digits.group(), 10)
            break
    raise RecordError(f"no '{MAX_DISPATCHES_MARKER}<n>' line under '{SETUP_HEADING}' in '{path}'")
