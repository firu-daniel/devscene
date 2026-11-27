"""The rule this module exists to enforce: it stands in for a `claude` session, driven only by a
scenario file, and writes only to the paths the scenario names.

Run as `python fake_claude.py <scenario.json> [args…]`. The scenario is a JSON object:
- `argv_file` (optional): the JSON list of the args after the scenario path is written there;
- `child_pid_file` (optional): a child sleeping for 600 s is spawned in this process's group and
  its pid written there, before `pid_file`;
- `child_stdio` (optional, default `"inherit"`): the child's stdio — `"inherit"` shares this
  process's; `"detached"` puts stdin, stdout and stderr on `DEVNULL`; `"stderr"` puts stdin and
  stdout on `DEVNULL` and inherits stderr;
- `pid_file` (optional): this process's own pid is written there;
- `steps`: a list of `{"stdout": <text>}` or `{"stderr": <text>}`, each written with a newline and
  flushed, `{"sleep": <seconds>}`, or `{"wait_for": <path>}`, which polls every 0.01 s until that
  path exists and exits 1 if it has not appeared after 60 s;
- `exit` (optional, default `0`): the exit status.
Every file is written whole, through a rename, so a reader that sees it sees all of it.

`plant` writes a scenario under a directory and returns the command prefix that runs it.
"""

import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping
from pathlib import Path

_CHILD_SOURCE = "import time; time.sleep(600)"
_WAIT_FOR_SECONDS = 60.0
_WAIT_FOR_POLL_SECONDS = 0.01


def plant(directory: Path, scenario: Mapping[str, object]) -> tuple[str, ...]:
    path = directory / "scenario.json"
    path.write_text(json.dumps(dict(scenario)), encoding="utf-8")
    return (sys.executable, str(Path(__file__).resolve()), str(path))


def _write_whole(path: str, text: str) -> None:
    partial = f"{path}.partial"
    Path(partial).write_text(text, encoding="utf-8")
    os.replace(partial, path)


def _optional_path(scenario: Mapping[str, object], key: str) -> str | None:
    value = scenario.get(key)
    return value if isinstance(value, str) else None


def _wait_for(path: Path) -> bool:
    deadline = time.monotonic() + _WAIT_FOR_SECONDS
    while not path.exists():
        if time.monotonic() >= deadline:
            return False
        time.sleep(_WAIT_FOR_POLL_SECONDS)
    return True


def main(arguments: list[str]) -> int:
    loaded: object = json.loads(Path(arguments[0]).read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit("fake_claude: the scenario is not a JSON object")
    scenario: dict[str, object] = loaded
    argv_file = _optional_path(scenario, "argv_file")
    if argv_file is not None:
        _write_whole(argv_file, json.dumps(arguments[1:]))
    child_pid_file = _optional_path(scenario, "child_pid_file")
    if child_pid_file is not None:
        child_stdio = scenario.get("child_stdio", "inherit")
        quiet = subprocess.DEVNULL if child_stdio in ("detached", "stderr") else None
        child = subprocess.Popen(
            [sys.executable, "-c", _CHILD_SOURCE],
            stdin=quiet,
            stdout=quiet,
            stderr=subprocess.DEVNULL if child_stdio == "detached" else None,
        )
        _write_whole(child_pid_file, str(child.pid))
    pid_file = _optional_path(scenario, "pid_file")
    if pid_file is not None:
        _write_whole(pid_file, str(os.getpid()))
    steps = scenario.get("steps", [])
    for step in steps if isinstance(steps, list) else []:
        if not isinstance(step, dict):
            continue
        if isinstance(step.get("stdout"), str):
            sys.stdout.write(f"{step['stdout']}\n")
            sys.stdout.flush()
        elif isinstance(step.get("stderr"), str):
            sys.stderr.write(f"{step['stderr']}\n")
            sys.stderr.flush()
        elif isinstance(step.get("sleep"), int | float):
            time.sleep(step["sleep"])
        elif isinstance(step.get("wait_for"), str) and not _wait_for(Path(step["wait_for"])):
            return 1
    status = scenario.get("exit", 0)
    return status if isinstance(status, int) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
