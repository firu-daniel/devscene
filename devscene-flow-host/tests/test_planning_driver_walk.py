"""The rule this file exists to enforce: `devscene-planning-driver` walks the planning graph the
host routes, launching a round's three gates as one concurrent set that closes once, and a session
whose return it cannot take — a return failing its schema, a gate `PASS` whose schema-valid return
omits the `findings_file` the round needs, no `init` event, or a round file with no verdict line,
on each of its three attempts — is held as `error` while its siblings run to their end, then
parks; one whose `init` event merely lacks declared tools is not refused, and is logged. A
hand-off logs the `tasks_count` the writer's return object carries. This is the rule the retired
`cli/test/planning-driver-walk.test.mjs` held for `pd_drive`, re-said against the Python driver.

Each case runs `main` end to end over `cli/templates/scripts/flows` and a plugin directory built
under `tmp_path` from this checkout's `plugin/` — the manifest, the six planning agents, their
return schemas and the planning core, copied from a read-only source. Every node session is
`fake_planning_agent.py`, behind an agent CLI planted under `tmp_path` that can hand the fake a
second plugin copy, so the fake and the driver read different contracts; the commit wrapper is a
fake logging each `--artifact` call. Every expected literal — a wrapper call, a prompt's first
line, a `held:` section, a log line — is written here, never read from the graph or the code
under test.

A held case spends GraphScene's two 60-second retry backoffs, as the run does: no case shortens
them.

Deliberately not covered:
- Parks for questions, stops, retries on their own and observations:
  `tests/test_planning_driver_control.py`.
- The return fields the hand-off reads: `tests/test_driver_return_fields.py`.
"""

import io
import json
import os
import shlex
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import pytest

from devscene_flow_host.commands.planning_driver import main
from fake_planning_agent import plant, read_calls

_CHECKOUT: Final = Path(__file__).resolve().parents[2]
_SOURCE_PLUGIN: Final = _CHECKOUT / "plugin"
_FLOWS: Final = _CHECKOUT / "cli" / "templates" / "scripts" / "flows"
_BRANCH: Final = "feat_x"
_PLANNING_AGENTS: Final = (
    "task-plan-writer",
    "business-parity-reviewer",
    "architecture-reviewer",
    "task-plan-reviewer",
    "ui-tests-plan-writer",
    "ui-tests-plan-reviewer",
)
_CORE: Final = "instructions/task_plan_writing_instructions_core.md"
_WRITER: Final = "task-plan-writer"
_GATES: Final = ("business-parity-reviewer", "architecture-reviewer", "task-plan-reviewer")
_LEDGER: Final = "devscene/flow_progress/feat_x_progress.md"
_PROMPT: Final = "devscene/task_prompts/feat_x_task_prompt.md"
_QUESTION: Final = "devscene/clarifications/feat_x/question_1.md"
_LEDGER_TEXT: Final = (
    "# Flow progress — feat_x   (engine: task)\n"
    "\n"
    "## Run mode\n"
    "Source: devscene/task_prompts/feat_x_task_prompt.md → `### Run mode`\n"
    "- skipped: none\n"
    "- phases: parity=true, qa=false, docs=false\n"
    "- remote-skipped: none\n"
    "\n"
    "## Planning\n"
    "- [x] P0. Untrusted input screened (prompt-injection-reviewer SAFE)\n"
    "- [ ] P1. Task plan converged (business_parity + architecture + task-plan-reviewer all PASS)\n"
    "- [ ] P2. UI-test plan converged (ui-tests-plan-reviewer PASS) — or no_ui\n"
    "- [ ] P3. Plans committed & pushed (story index + per-task dir + UI-test plan)\n"
    "\n"
    "## Implementation\n"
    "- [ ] A.      Tasks implemented (story-index readiness all [x])\n"
)
_GIT_IDENTITY: Final = (
    "-c",
    "user.name=fixture",
    "-c",
    "user.email=fixture@example.invalid",
    "-c",
    "commit.gpgsign=false",
)


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


@dataclass(frozen=True)
class Drive:
    status: int
    stdout: str
    stderr: str
    calls: list[dict[str, object]]
    wrapper: list[str]
    stamps: list[tuple[int, str]]
    log: list[str]
    repo: Path


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *_GIT_IDENTITY, "-C", str(repo), *args], check=True, capture_output=True)


def _plant_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": "devscene",
                "scriptsDir": "bin",
                "phases": {"parity": True, "qa": False},
            }
        ),
        encoding="utf-8",
    )
    for relative, text in (
        (_LEDGER, _LEDGER_TEXT),
        (_PROMPT, "# Task prompt\n\nAdd a fixture feature.\n"),
    ):
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    wrapper = repo / "bin" / "commit-on-branch.sh"
    wrapper.parent.mkdir()
    calls = shlex.quote(str(tmp_path / "wrapper-calls.log"))
    stamps = shlex.quote(str(tmp_path / "wrapper-stamps.log"))
    clock = f"{shlex.quote(sys.executable)} -c 'import time; print(time.time_ns())'"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        'args=("$@")\n'
        'call="${args[*]:3:$(($# - 4))}"\n'
        f"printf '%s\\n' \"$call\" >>{calls}\n"
        f'printf \'%s %s\\n\' "$({clock})" "$call" >>{stamps}\n'
        "exit 0\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    _git(repo, "init", "-q", "-b", _BRANCH)
    _git(repo, "add", "--", "devscene.config.json", _LEDGER, _PROMPT, "bin/commit-on-branch.sh")
    _git(repo, "commit", "-q", "-m", "fixture: seed")
    return repo


def _plant_plugin(directory: Path) -> Path:
    for relative in (
        ".claude-plugin/plugin.json",
        _CORE,
        *(f"agents/{agent}.md" for agent in _PLANNING_AGENTS),
        *(f"schemas/{agent}.return.json" for agent in _PLANNING_AGENTS),
    ):
        target = directory / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_SOURCE_PLUGIN / relative, target)
    return directory


def _plant_agent_cli(tmp_path: Path, returns: dict[str, object], fake_plugin: Path | None) -> Path:
    directory = tmp_path / "agent"
    directory.mkdir()
    script = {"calls_log": str(directory / "calls.jsonl"), "returns": returns}
    command = " ".join(shlex.quote(word) for word in plant(directory, script))
    if fake_plugin is None:
        body = f'exec {command} "$@"\n'
    else:
        body = (
            "args=()\n"
            'while [ "$#" -gt 0 ]; do\n'
            '  if [ "$1" = --plugin-dir ]; then\n'
            f'    args+=("$1" {shlex.quote(str(fake_plugin))}); shift 2; continue\n'
            "  fi\n"
            '  args+=("$1"); shift\n'
            "done\n"
            f'exec {command} "${{args[@]}}"\n'
        )
    cli = directory / "agent-cli"
    cli.write_text("#!/usr/bin/env bash\n" + body, encoding="utf-8")
    cli.chmod(0o755)
    return cli


def _drive(
    tmp_path: Path,
    returns: dict[str, object] | None = None,
    *,
    fake_plugin_edit: Callable[[Path], None] | None = None,
    repo_files: dict[str, str] | None = None,
) -> Drive:
    repo = _plant_repo(tmp_path)
    for relative, text in (repo_files or {}).items():
        (repo / relative).write_text(text, encoding="utf-8")
    plugin = _plant_plugin(tmp_path / "plugin")
    fake_plugin = None
    if fake_plugin_edit is not None:
        fake_plugin = _plant_plugin(tmp_path / "fake-plugin")
        fake_plugin_edit(fake_plugin)
    cli = _plant_agent_cli(tmp_path, returns or {}, fake_plugin)
    log = tmp_path / "run.log"
    out, err = io.StringIO(), io.StringIO()
    status = main(
        [
            "--branch",
            _BRANCH,
            "--worktree",
            str(repo),
            "--main-repo",
            str(repo),
            "--plugin-dir",
            str(plugin),
            "--flows",
            str(_FLOWS),
            "--log",
            str(log),
            "--formatter",
            "true",
            "--",
            str(cli),
        ],
        stdout=out,
        stderr=err,
    )
    calls_log = tmp_path / "wrapper-calls.log"
    stamps_log = tmp_path / "wrapper-stamps.log"
    stamps: list[tuple[int, str]] = []
    if stamps_log.exists():
        for line in stamps_log.read_text(encoding="utf-8").splitlines():
            stamp, _, call = line.partition(" ")
            stamps.append((int(stamp), call))
    return Drive(
        status=status,
        stdout=out.getvalue(),
        stderr=err.getvalue(),
        calls=read_calls(tmp_path / "agent" / "calls.jsonl"),
        wrapper=calls_log.read_text(encoding="utf-8").splitlines() if calls_log.exists() else [],
        stamps=stamps,
        log=log.read_text(encoding="utf-8").splitlines() if log.exists() else [],
        repo=repo,
    )


def _of(drive: Drive, agent: str) -> list[dict[str, object]]:
    return [call for call in drive.calls if call["agent"] == agent]


def _time(call: dict[str, object], key: str) -> int:
    value = call[key]
    assert isinstance(value, int)
    return value


def _show(drive: Drive) -> str:
    return "\n".join(
        [f"status {drive.status}", drive.stdout, drive.stderr, *drive.wrapper, *drive.log]
    )


def test_a_full_walk_revises_once_and_hands_off(tmp_path: Path) -> None:
    drive = _drive(
        tmp_path,
        {"architecture-reviewer": [{"return": {"outcome": "FAIL", "must_fix_count": 1}}]},
    )
    assert (drive.status, drive.stdout, drive.stderr) == (0, "consumed:\n", ""), _show(drive)

    assert drive.wrapper[:2] == ["plan-round --round 0", "plan-round --round 1"], _show(drive)
    assert drive.wrapper.count("plan-round --round 0") == 1
    assert drive.wrapper.count("plan-round --round 1") == 1
    flip_p1 = drive.wrapper.index("ledger-flip --entry P1")
    task_plan = drive.wrapper.index("task-plan")
    flip_p3 = drive.wrapper.index("ledger-flip --entry P3")
    assert 1 < flip_p1 < task_plan < flip_p3, _show(drive)
    assert drive.wrapper.count("task-plan") == 1

    ledger = (drive.repo / _LEDGER).read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("- [x] P1. ") for line in ledger), ledger
    assert any(line.startswith("- [x] P3. ") for line in ledger), ledger

    writers = _of(drive, _WRITER)
    assert len(writers) == 2
    # `judge_session` resolves each `findings_file` against the session's working directory.
    repo = drive.repo.resolve()
    assert str(writers[1]["prompt"]).split("\n")[0] == (
        f"Revise the task plan per findings at "
        f"{repo}/devscene/business_parity_reviews/feat_x/review_0.md, "
        f"{repo}/devscene/architecture_reviews/feat_x/review_0.md, "
        f"{repo}/devscene/task_plan_reviews/feat_x/review_0.md."
    )
    for gate in _GATES:
        assert len(_of(drive, gate)) == 2, gate


def test_a_rounds_gates_run_as_one_set_that_closes_once_after_its_last_gate(
    tmp_path: Path,
) -> None:
    drive = _drive(
        tmp_path,
        {
            "business-parity-reviewer": [{"sleep": 1.0}],
            "architecture-reviewer": [{"sleep": 0.4}],
            "task-plan-reviewer": [{"sleep": 0.4}],
        },
    )
    assert (drive.status, drive.stdout) == (0, "consumed:\n"), _show(drive)
    round_0 = [_of(drive, gate)[0] for gate in _GATES]
    assert max(_time(call, "start") for call in round_0) < min(
        _time(call, "end") for call in round_0
    ), round_0
    assert [call for _, call in drive.stamps].count("plan-round --round 0") == 1, _show(drive)
    closed = next(stamp for stamp, call in drive.stamps if call == "plan-round --round 0")
    assert closed > max(_time(call, "end") for call in round_0)


def _omit_pass_findings_file(plugin: Path) -> None:
    path = plugin / "schemas" / "architecture-reviewer.return.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    del schema["oneOf"][0]["properties"]["findings_file"]
    path.write_text(json.dumps(schema), encoding="utf-8")


_NO_VERDICT_FILE: Final = "no-verdict-round-file.md"


@pytest.mark.parametrize(
    ("agent", "node", "entries", "edit", "reason"),
    [
        pytest.param(
            "task-plan-reviewer",
            "plan_review",
            [{"return": {"outcome": "PASS", "stray": True}}] * 3,
            None,
            "the return fails its schema: ",
            id="schema",
        ),
        pytest.param(
            "architecture-reviewer",
            "architecture_review",
            [],
            _omit_pass_findings_file,
            "PASS carries no findings_file",
            id="no-findings-file",
        ),
        pytest.param(
            "business-parity-reviewer",
            "business_parity_review",
            [{"no_init": True}] * 3,
            None,
            "the agent did not resolve: no init event",
            id="no-init",
        ),
        pytest.param(
            "task-plan-reviewer",
            "plan_review",
            [{"return": {"outcome": "PASS", "findings_file": _NO_VERDICT_FILE}}] * 3,
            None,
            "the round file was refused: no single verdict line",
            id="no-verdict-line",
        ),
    ],
)
def test_a_session_the_driver_cannot_take_is_held_while_its_siblings_finish_then_parks(
    tmp_path: Path,
    agent: str,
    node: str,
    entries: list[dict[str, object]],
    edit: Callable[[Path], None] | None,
    reason: str,
) -> None:
    siblings = [gate for gate in _GATES if gate != agent]
    returns: dict[str, object] = {agent: entries}
    for sibling in siblings:
        returns[sibling] = [{"sleep": 1.0}]
    drive = _drive(
        tmp_path,
        returns,
        fake_plugin_edit=edit,
        repo_files={_NO_VERDICT_FILE: "# review\n"},
    )

    assert (drive.status, drive.stdout) == (3, "stopped: park\n"), _show(drive)
    held = _of(drive, agent)
    assert len(held) == 3, _show(drive)
    for sibling in siblings:
        calls = _of(drive, sibling)
        assert len(calls) == 1, sibling
        assert _time(held[0], "end") < _time(calls[0], "end"), sibling
    assert len(_of(drive, _WRITER)) == 1, "nothing dispatched after the park"

    question = (drive.repo / _QUESTION).read_text(encoding="utf-8")
    heading = f"\n### `{node}` — error\n\n- agent: `{agent}`\n- reason: "
    assert heading in question, question
    assert question.split(heading, 1)[1].startswith(reason), question
    assert not (drive.repo / "devscene/clarifications/feat_x/question_2.md").exists()


def _withhold_glob_and_grep(plugin: Path) -> None:
    path = plugin / "agents" / "task-plan-writer.md"
    declared = "tools: Read, Write, Edit, Bash, Glob, Grep, mcp__devscene-docs__search_docs\n"
    text = path.read_text(encoding="utf-8")
    assert declared in text
    path.write_text(
        text.replace(declared, "tools: Read, Write, Edit, Bash, mcp__devscene-docs__search_docs\n"),
        encoding="utf-8",
    )


def test_a_hand_off_logs_the_writers_tasks_count_and_a_withheld_tool_is_logged_not_refused(
    tmp_path: Path,
) -> None:
    drive = _drive(
        tmp_path,
        {
            _WRITER: [
                {
                    "return": {
                        "outcome": "returned",
                        "story_file": "story.md",
                        "task_files_dir": "tasks/",
                        "tasks_count": 3,
                        "story_points_total": 1,
                    }
                }
            ]
        },
        fake_plugin_edit=_withhold_glob_and_grep,
    )
    assert (drive.status, drive.stdout) == (0, "consumed:\n"), _show(drive)
    assert "[plan-drive] tasks_count: 3" in drive.log, _show(drive)
    assert (
        "[plan-drive] #1 plan_writer (task-plan-writer): the init event lacks declared tools "
        "[Glob, Grep] (a lacking tool is never refused)"
    ) in drive.log, _show(drive)
    assert len(_of(drive, _WRITER)) == 1
    assert "ledger-flip --entry P3" in drive.wrapper, _show(drive)
