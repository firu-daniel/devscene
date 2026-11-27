"""The rule this module exists to enforce: it stands in for the agent CLI a planning node session
runs, answering each call as the scripted planning agent named by its `--agent` would, and writes
only the paths its script names and the findings file its prompt names.

Run as `python fake_planning_agent.py <script.json> <argv…>`, where `<argv…>` is what
`ClaudeExecutor` passes. The script is a JSON object:
- `calls_log`: one compact JSON line is appended per call — `agent`, `prompt` (the `-p` value),
  `argv`, `VIRTUAL_ENV` and `PYTHONPATH` from the environment (`null` when unset), and `start` /
  `end` in `time.time_ns()`;
- `returns` (optional): agent name to a list of entries, the next unused one taken per call of
  that agent, in order; with none left the agent's default is used.
An entry is an object of optional keys: `return`, the return object; `sleep`, seconds slept
before answering; `no_init`, no `init` event; `is_error`, a result with `is_error`;
`no_return_block`, a result text with no return block.

The agent is read from `--agent <plugin>:<agent>`, and its `tools:` line from
`<--plugin-dir>/agents/<agent>.md`; the `init` event grants exactly those tools. The default
return is `_WRITER_DEFAULTS`' for a writer and `PASS` for a reviewer — an agent whose name holds
`reviewer`. A reviewer whose prompt carries `findings_folder: <dir>` and `iteration: <n>` lines
writes `<dir>review_<n>.md`, under the working directory, with its return's verdict line and, for
`FAIL`, one Must Fix entry; its return carries `findings_file` when the branch of
`<--plugin-dir>/schemas/<agent>.return.json` for its outcome declares that property.

`plant` writes a script under a directory and returns the command prefix that runs it.
"""

import fcntl
import json
import os
import sys
import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Final

_WRITER_DEFAULTS: Final[Mapping[str, Mapping[str, object]]] = {
    "task-plan-writer": {
        "outcome": "returned",
        "story_file": "story.md",
        "task_files_dir": "tasks/",
        "tasks_count": 1,
        "story_points_total": 1,
    },
    "ui-tests-plan-writer": {
        "outcome": "returned",
        "ui_test_index": "ui.md",
        "ui_test_files_dir": "ui/",
        "tests_count": 1,
    },
}
_FAIL_BODY: Final = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"
_FINDINGS_FOLDER: Final = "findings_folder: "
_ITERATION: Final = "iteration: "


def plant(directory: Path, script: Mapping[str, object]) -> tuple[str, ...]:
    path = directory / "script.json"
    path.write_text(json.dumps(dict(script)), encoding="utf-8")
    return (sys.executable, str(Path(__file__).resolve()), str(path))


def read_calls(calls_log: Path) -> list[dict[str, object]]:
    if not calls_log.exists():
        return []
    return [json.loads(line) for line in calls_log.read_text(encoding="utf-8").splitlines()]


@contextmanager
def _locked(path: Path) -> Iterator[None]:
    with path.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _value(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


def _tools(plugin_dir: Path, agent: str) -> list[str]:
    for line in (plugin_dir / "agents" / f"{agent}.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("tools:"):
            return [item.strip() for item in line[len("tools:") :].split(",") if item.strip()]
    return []


def _next_entry(script: Mapping[str, object], script_path: Path, agent: str) -> dict[str, object]:
    returns = script.get("returns")
    entries = returns.get(agent, []) if isinstance(returns, dict) else []
    cursor = script_path.parent / f"{script_path.name}.{agent}.cursor"
    with _locked(script_path.parent / f"{script_path.name}.lock"):
        used = int(cursor.read_text(encoding="ascii")) if cursor.exists() else 0
        cursor.write_text(str(used + 1), encoding="ascii")
    if isinstance(entries, list) and used < len(entries) and isinstance(entries[used], dict):
        return dict(entries[used])
    return {}


def _prompt_line(prompt: str, prefix: str) -> str | None:
    for line in prompt.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def _declares_findings_file(plugin_dir: Path, agent: str, outcome: object) -> bool:
    schema = json.loads(
        (plugin_dir / "schemas" / f"{agent}.return.json").read_text(encoding="utf-8")
    )
    for branch in schema.get("oneOf", []):
        properties = branch.get("properties", {})
        if properties.get("outcome", {}).get("const") == outcome:
            return "findings_file" in properties
    return False


def _answer(
    entry: Mapping[str, object], agent: str, prompt: str, plugin_dir: Path
) -> dict[str, object]:
    reviewer = "reviewer" in agent
    scripted = entry.get("return")
    if isinstance(scripted, dict):
        document = dict(scripted)
    elif reviewer:
        document = {"outcome": "PASS"}
    else:
        document = dict(_WRITER_DEFAULTS.get(agent, {"outcome": "returned"}))
    outcome = document.get("outcome")
    folder = _prompt_line(prompt, _FINDINGS_FOLDER)
    iteration = _prompt_line(prompt, _ITERATION)
    if reviewer and folder and iteration and outcome in ("PASS", "FAIL"):
        path = Path.cwd() / folder / f"review_{iteration}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("verdict: PASS\n" if outcome == "PASS" else _FAIL_BODY, encoding="utf-8")
        if "findings_file" not in document and _declares_findings_file(plugin_dir, agent, outcome):
            document["findings_file"] = str(path)
    return document


def _emit(event: Mapping[str, object]) -> None:
    sys.stdout.write(json.dumps(dict(event)) + "\n")
    sys.stdout.flush()


def main(arguments: list[str]) -> int:
    start = time.time_ns()
    script_path = Path(arguments[0])
    loaded: object = json.loads(script_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit("fake_planning_agent: the script is not a JSON object")
    script: dict[str, object] = loaded
    argv = arguments[1:]
    agent = _value(argv, "--agent").partition(":")[2]
    plugin_dir = Path(_value(argv, "--plugin-dir"))
    prompt = _value(argv, "-p")
    entry = _next_entry(script, script_path, agent)

    sleep = entry.get("sleep")
    if isinstance(sleep, int | float):
        time.sleep(sleep)
    session_id = f"fake-{agent}-{os.getpid()}"
    if not entry.get("no_init"):
        _emit(
            {
                "type": "system",
                "subtype": "init",
                "session_id": session_id,
                "tools": _tools(plugin_dir, agent),
            }
        )
    document = _answer(entry, agent, prompt, plugin_dir)
    text = "done"
    if not entry.get("no_return_block"):
        text = f"done\n```json\n{json.dumps(document)}\n```"
    _emit(
        {
            "type": "result",
            "subtype": "success",
            "is_error": bool(entry.get("is_error")),
            "result": text,
            "session_id": session_id,
            "total_cost_usd": 0.0,
        }
    )

    calls_log = Path(str(script["calls_log"]))
    record = {
        "agent": agent,
        "prompt": prompt,
        "argv": argv,
        "VIRTUAL_ENV": os.environ.get("VIRTUAL_ENV"),
        "PYTHONPATH": os.environ.get("PYTHONPATH"),
        "start": start,
        "end": time.time_ns(),
    }
    with _locked(script_path.parent / f"{script_path.name}.lock"), calls_log.open("a") as log:
        log.write(json.dumps(record, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
