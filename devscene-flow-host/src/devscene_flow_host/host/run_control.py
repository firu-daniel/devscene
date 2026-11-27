"""GraphScene's `RunSignals` and `DispatchCounter` over the harness's files, the kill switch, and
the planning run's `ExecutionLimits`.

The rule:
- `FileRunSignals` answers STOP as `<stateDir>/STOP` existing and PAUSE as `<stateDir>/PAUSE`
  existing, re-read on every call and never cached, as `pd_stop_present` and `pd_run_set` read them
  (`cli/templates/scripts/lib/planning-driver-lib.sh`, deleted by Task 4 and readable in that
  file's history).
- `kill_switch_present` is `<stateDir>/AUTONOMOUS_STOP` existing in the **main** checkout, its
  `stateDir` read from that checkout's `devscene.config.json`, as `pd_main` read
  `hr_state_path "$PD_MAIN_REPO" AUTONOMOUS_STOP`.
- `FileDispatchCounter` keeps its total in `<stateDir>/.dispatch_counter` as one decimal line.
  `reset` writes `0\\n`, as `pd_main` did at each drive; `increment` writes `total + 1` whole,
  through a temporary file in the same directory and `os.replace`, and returns it. A missing or
  non-decimal counter file is a `RecordError` naming it.
- `planning_limits` fixes every limit but the dispatch cap, which the caller reads from the
  planning core.

Deliberately not covered:
- Halting on a signal or on the cap: GraphScene's `clear_set`.
- What a halt does afterwards — the narration, the pause files, the partial commit:
  `host/run_exits.py` (Task 17).

`MAX_CONCURRENT_DISPATCHES` is a flow-host constant, not a `devscene.config.json` key, because the
flow host is the harness's own implementation of its flows; GraphScene's default of 10 is for hosts
that set none.
"""

import contextlib
import os
import re
import tempfile
from pathlib import Path, PurePosixPath
from typing import Final

from graphscene import ExecutionLimits

from devscene_flow_host.records.config import read_config
from devscene_flow_host.records.errors import RecordError

STOP_FILE: Final = "STOP"
PAUSE_FILE: Final = "PAUSE"
KILL_SWITCH_FILE: Final = "AUTONOMOUS_STOP"
DISPATCH_COUNTER_FILE: Final = ".dispatch_counter"

MAX_CONCURRENT_DISPATCHES: Final = 5
MAX_ATTEMPTS: Final = 3
BACKOFF_SECONDS: Final = 60.0
UNDELIVERED_LIMIT: Final = 3

_COUNTER_LINE: Final = re.compile("([0-9]+)\n")


class FileRunSignals:
    def __init__(self, repo_root: Path, state_dir: str) -> None:
        self._state = repo_root / state_dir

    def stop_requested(self) -> bool:
        return (self._state / STOP_FILE).exists()

    def pause_requested(self) -> bool:
        return (self._state / PAUSE_FILE).exists()


def kill_switch_present(main_repo: Path) -> bool:
    return (main_repo / read_config(main_repo).state_dir / KILL_SWITCH_FILE).exists()


class FileDispatchCounter:
    def __init__(self, repo_root: Path, state_dir: str) -> None:
        self._rel = PurePosixPath(state_dir, DISPATCH_COUNTER_FILE).as_posix()
        self._path = repo_root / self._rel

    def reset(self) -> None:
        self._write(0)

    def total(self) -> int:
        try:
            raw = self._path.read_bytes()
        except FileNotFoundError:
            raise RecordError(f"the dispatch counter '{self._rel}' does not exist") from None
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError:
            text = ""
        line = _COUNTER_LINE.fullmatch(text)
        if line is None:
            raise RecordError(f"{self._rel}: not one decimal line")
        return int(line.group(1), 10)

    def increment(self) -> int:
        total = self.total() + 1
        self._write(total)
        return total

    def _write(self, total: int) -> None:
        descriptor, temporary = tempfile.mkstemp(
            dir=self._path.parent, prefix=f"{DISPATCH_COUNTER_FILE}."
        )
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(f"{total}\n".encode("ascii"))
            os.replace(temporary, self._path)
        except BaseException:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(temporary)
            raise


def planning_limits(dispatch_cap: int) -> ExecutionLimits:
    return ExecutionLimits(
        max_attempts=MAX_ATTEMPTS,
        backoff_seconds=BACKOFF_SECONDS,
        dispatch_cap=dispatch_cap,
        run_timeout_seconds=None,
        max_concurrent_dispatches=MAX_CONCURRENT_DISPATCHES,
    )
