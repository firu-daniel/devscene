"""The rule this file exists to enforce: `devscene-planning-driver` answers the watcher by the
story index's command-line contract — `0` with exactly `consumed:` and its indices, `3` with
exactly `stopped: <kind>`, `2` with one `planning-driver: <cause>` stderr line and empty stdout —
refuses each malformed command line with a cause naming the flag, is declared as the console
script `[project.scripts]` names, and keeps the name `harness-run-lib.sh` launches.

Each case drives `main` with `io.StringIO` streams over a configuration, ledger and commit wrapper
planted under `tmp_path`, with `--flows` naming the checkout's own `cli/templates/scripts/flows`
and `--plugin-dir` its `plugin/`, both read-only. Every expected text is a literal written from
the task plan's contract, never taken from the output of the code under test.

Deliberately not covered:
- Walks that dispatch: Tasks 19–21's suites drive the real command against a fake agent CLI.
"""

import io
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Final

import pytest

from devscene_flow_host.commands.planning_driver import answer, main
from devscene_flow_host.host.run_exits import StopKind

_CHECKOUT: Final = Path(__file__).resolve().parents[2]
_FLOWS: Final = _CHECKOUT / "cli" / "templates" / "scripts" / "flows"
_PLUGIN_DIR: Final = _CHECKOUT / "plugin"
_MANIFEST: Final = _CHECKOUT / "devscene-flow-host" / "pyproject.toml"
_HARNESS_RUN_LIB: Final = _CHECKOUT / "cli" / "templates" / "scripts" / "lib" / "harness-run-lib.sh"
_BRANCH: Final = "feat_x"
_LEDGER_TEMPLATE: Final = (
    "# Flow progress\n"
    "\n"
    "## Run mode\n"
    "- skipped: none\n"
    "\n"
    "## Planning\n"
    "- [{p1}] P1. Task plan converged\n"
    "- [{p2}] P2. UI-test plan converged\n"
    "- [{p3}] P3. Planning committed\n"
)


def _plant_repo(root: Path, *, p1: str = " ", p2: str = " ", p3: str = " ") -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": "state",
                "scriptsDir": "bin",
                "phases": {"parity": False, "qa": False},
            }
        ),
        encoding="utf-8",
    )
    ledger = root / "state" / "flow_progress" / "feat_x_progress.md"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(_LEDGER_TEMPLATE.format(p1=p1, p2=p2, p3=p3), encoding="utf-8")
    wrapper = root / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    wrapper.chmod(0o755)


def _argv(root: Path, log: Path, *, flows: Path = _FLOWS) -> list[str]:
    return [
        "--branch",
        _BRANCH,
        "--worktree",
        str(root),
        "--main-repo",
        str(root),
        "--plugin-dir",
        str(_PLUGIN_DIR),
        "--flows",
        str(flows),
        "--log",
        str(log),
        "--formatter",
        "cat",
        "--",
        "claude",
        "--model",
        "m",
    ]


def _main(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    status = main(argv, stdout=out, stderr=err)
    return status, out.getvalue(), err.getvalue()


_FULL_FLAGS: Final = [
    "--branch",
    "b",
    "--worktree",
    "w",
    "--main-repo",
    "m",
    "--plugin-dir",
    "p",
    "--flows",
    "f",
    "--log",
    "l",
    "--formatter",
    "cat",
]


@pytest.mark.parametrize(
    ("argv", "cause"),
    [
        ([], "missing '--' and the agent CLI after it"),
        (_FULL_FLAGS, "missing '--' and the agent CLI after it"),
        ([*_FULL_FLAGS, "--"], "missing the agent CLI after '--'"),
        ([*_FULL_FLAGS, "--", ""], "missing the agent CLI after '--'"),
        ([*_FULL_FLAGS[:-2], "--", "claude"], "missing --formatter"),
        ([*_FULL_FLAGS[2:], "--", "claude"], "missing --branch"),
        (["--branch", "", *_FULL_FLAGS[2:], "--", "claude"], "--branch needs a non-empty value"),
        (["--bogus", "x", *_FULL_FLAGS, "--", "claude"], "unknown flag '--bogus'"),
        (
            ["--plugin-dir-added=1", *_FULL_FLAGS, "--", "claude"],
            "unknown flag '--plugin-dir-added=1'",
        ),
        ([*_FULL_FLAGS, "--log", "--", "claude"], "--log needs a value"),
        ([*_FULL_FLAGS, "--log"], "--log needs a value"),
    ],
)
def test_a_malformed_command_line_is_a_usage_fault(argv: list[str], cause: str) -> None:
    assert _main(argv) == (2, "", "planning-driver: " + cause + "\n")


def test_a_fully_resolved_ledger_hands_off_consuming_nothing(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root, p1="x", p2="-", p3="x")
    argv = _argv(root, tmp_path / "run.log")
    separator = argv.index("--")
    argv[separator:separator] = ["--plugin-dir-added"]
    assert _main(argv) == (0, "consumed:\n", "")


def test_a_planted_kill_switch_is_a_clean_stop(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    (root / "state" / "AUTONOMOUS_STOP").write_text("", encoding="utf-8")
    log = tmp_path / "run.log"
    assert _main(_argv(root, log)) == (3, "stopped: kill-switch\n", "")
    assert log.read_text(encoding="utf-8").splitlines()[0] == (
        f"[plan-drive] halted: the global kill switch {root}/state/AUTONOMOUS_STOP is present"
    )
    observed = (root / "state" / "improvement_observations" / "feat_x.md").read_text(
        encoding="utf-8"
    )
    assert "## The global kill switch ended script-driven planning\n" in observed


def test_a_graph_directory_without_the_graph_is_a_fault_naming_the_file(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root)
    flows = tmp_path / "flows"
    flows.mkdir()
    log = tmp_path / "run.log"
    cause = f"no planning graph at {flows}/task_plan_writing.graph.json"
    assert _main(_argv(root, log, flows=flows)) == (2, "", "planning-driver: " + cause + "\n")
    assert log.read_text(encoding="utf-8") == "[plan-drive] " + cause + "\n"


@pytest.mark.parametrize(
    ("kind", "consumed", "expected"),
    [
        ("handed_off", (), (0, "consumed:\n")),
        ("handed_off", (2, 5), (0, "consumed: 2 5\n")),
        ("park", (), (3, "stopped: park\n")),
        ("pause", (), (3, "stopped: pause\n")),
        ("undelivered", (), (3, "stopped: undelivered\n")),
        ("stop", (), (3, "stopped: stop\n")),
        ("cap", (), (3, "stopped: cap\n")),
        ("kill_switch", (1,), (3, "stopped: kill-switch\n")),
    ],
)
def test_each_stop_kind_answers_its_status_and_line(
    kind: StopKind, consumed: tuple[int, ...], expected: tuple[int, str]
) -> None:
    assert answer(kind, consumed) == expected


def test_the_module_runs_as_a_program_writing_to_the_real_stdout(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _plant_repo(root, p1="x", p2="-", p3="x")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "devscene_flow_host.commands.planning_driver",
            *_argv(root, tmp_path / "run.log"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert (result.returncode, result.stdout, result.stderr) == (0, "consumed:\n", "")


def test_the_manifest_declares_the_console_script() -> None:
    manifest = tomllib.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert (
        manifest["project"]["scripts"]["devscene-planning-driver"]
        == "devscene_flow_host.commands.planning_driver:main"
    )


def test_the_watcher_launches_the_declared_name() -> None:
    lines = _HARNESS_RUN_LIB.read_text(encoding="utf-8").splitlines()
    assert "HR_FLOW_HOST_DRIVER='devscene-planning-driver'" in lines, (
        "cli/templates/scripts/lib/harness-run-lib.sh → HR_FLOW_HOST_DRIVER no longer names "
        "devscene-planning-driver: edit it and devscene-flow-host/pyproject.toml → "
        "[project.scripts] together"
    )
