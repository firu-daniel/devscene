"""The two run-control files the planning driver writes: a clarification park and a pause.

The rule:
- `write_park` writes as `prl_park` did (`cli/templates/scripts/lib/planning-record-lib.sh`, now
  deleted and readable in that file's history, as `devscene-flow-host/README.md` states for the
  retired walker's code): `<stateDir>/clarifications/<branch>/question_<n>.md`, `<n>` one
  past `max_question_index`, its directory created when absent, an existing file at that path a
  `FileExistsError` naming it — a write collision, never a `RecordError`, which is a record that
  could not be read. The file is `# <title>`, `Raised by: <raised_by> (script-driven
  planning)`, a `## Q1 — <title>` section only when no body line starts `## Q` and a digit, then
  the body, each block followed by a blank line. It is written through a temporary file in the
  same directory and `os.replace`, with mode `0o644`, and the repo-relative path is returned.
- `write_pause` writes as `prl_pause` did (the same file): it appends a `## <ts> — <branch> paused
  (script-driven planning)` block to `<stateDir>/PAUSE_PROGRESS.md` and writes `<ts>` to
  `<stateDir>/PAUSE_ACK`, `<ts>` being `now` in UTC as `%Y-%m-%dT%H:%M:%SZ`.
- Every file either writes stays under `<stateDir>`.

Deliberately not covered:
- Committing either file.
- Deciding when to park or pause, and a park's title and body: the caller's.
- The partial commit: `host/commit_points.py` → `commit_artifact`.
"""

import contextlib
import os
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Final

from devscene_flow_host.records.clarifications import (
    CLARIFICATIONS_DIRECTORY,
    RAISED_BY_PREFIX,
    max_question_index,
)

RAISED_BY_SUFFIX: Final = " (script-driven planning)"
PAUSE_PROGRESS_FILE: Final = "PAUSE_PROGRESS.md"
PAUSE_ACK_FILE: Final = "PAUSE_ACK"
_PAUSE_TIMESTAMP: Final = "%Y-%m-%dT%H:%M:%SZ"
_QUESTION_MODE: Final = 0o644
_Q_SECTION: Final = re.compile(r"## Q[0-9]")


def write_park(
    repo_root: Path, state_dir: str, branch: str, *, raised_by: str, title: str, body: str
) -> str:
    rel_dir = PurePosixPath(state_dir, CLARIFICATIONS_DIRECTORY, branch)
    directory = repo_root / rel_dir
    directory.mkdir(parents=True, exist_ok=True)
    index = max_question_index(repo_root, state_dir, branch) + 1
    rel = (rel_dir / f"question_{index}.md").as_posix()
    path = repo_root / rel
    if os.path.lexists(path):
        raise FileExistsError(f"'{rel}' already exists")

    text = f"# {title}\n\n{RAISED_BY_PREFIX}{raised_by}{RAISED_BY_SUFFIX}\n\n"
    if not any(_Q_SECTION.match(line) for line in body.split("\n")):
        text += f"## Q1 — {title}\n\n"
    text += body

    descriptor, temporary = tempfile.mkstemp(dir=directory, prefix=".question.")
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.chmod(temporary, _QUESTION_MODE)
        os.replace(temporary, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)
        raise
    return rel


def write_pause(
    repo_root: Path, state_dir: str, branch: str, *, phase: str, next_step: str, now: datetime
) -> None:
    directory = repo_root / state_dir
    directory.mkdir(parents=True, exist_ok=True)
    ts = now.astimezone(UTC).strftime(_PAUSE_TIMESTAMP)
    block = (
        f"\n## {ts} — {branch} paused{RAISED_BY_SUFFIX}\n"
        f"- phase: {phase}\n"
        f"- next step: {next_step}\n"
    )
    with (directory / PAUSE_PROGRESS_FILE).open("ab") as handle:
        handle.write(block.encode("utf-8"))
    (directory / PAUSE_ACK_FILE).write_bytes(f"{ts}\n".encode())
