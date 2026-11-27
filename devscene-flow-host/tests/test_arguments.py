"""The rule this file exists to enforce: `parse` reads a command line as `flow-walker.sh` →
`# --- Arguments` reads it — the four verbs, each verb's flags plus the added `--flows`, the value
checks in bash's order — and refuses with bash's exact text, without the `flow-walker: ` prefix.

Every expected text is a literal written from `cli/templates/scripts/flow-walker.sh`'s argument
section and header `USAGE`, never taken from the output of the code under test. Resolving paths and
the exit status are `commands/flow_walker.py`'s and not covered here.
"""

from typing import Final

import pytest

from devscene_flow_host.commands.arguments import Invocation, UsageError, parse

_WALK: Final = ["--flow", "task_plan_writing", "--branch", "feat_x", "--flows", "flows"]


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        ([], "missing subcommand: start, next, current or check-round-file"),
        (["walk"], "unknown subcommand 'walk': expected start, next, current or check-round-file"),
        (["start", "--outcome", "PASS"], "'--outcome' is not a flag of 'start'"),
        (["check-round-file", "--flow", "x"], "'--flow' is not a flag of 'check-round-file'"),
        (["check-round-file", "--flows", "flows"], "'--flows' is not a flag of 'check-round-file'"),
        (["current", *_WALK, "--skipped", "none"], "'--skipped' is not a flag of 'current'"),
        (["start", "--flow"], "--flow requires a value"),
        (["start", "--branch", "a\nb"], "the value of --branch carries a newline"),
        (["next", "--findings", "a\tb"], "the value of --findings carries a tab"),
        (["next", "--node", "Writer"], "'Writer' is not a node name"),
        (["next", "--node", ""], "'' is not a node name"),
        (["check-round-file"], "missing required flag --findings"),
        (["check-round-file", "--findings", ""], "missing required flag --findings"),
        (["start", "--branch", "b", "--flows", "f"], "missing required flag --flow"),
        (["start", "--flow", "f", "--flows", "f"], "missing required flag --branch"),
        (["start", "--flow", "f", "--branch", "b"], "missing required flag --flows"),
        (["next", *_WALK], "missing required flag --outcome"),
        (["next", *_WALK, "--outcome", "PA-SS"], "outcome 'PA-SS' is not an outcome name"),
        (
            ["next", *_WALK, "--outcome", "FAIL"],
            "outcome FAIL requires --findings with the reviewer's findings_file",
        ),
        (
            ["start", "--flow", "Task-plan", "--branch", "b", "--flows", "f"],
            "unknown flow 'Task-plan'",
        ),
    ],
)
def test_each_refusal_carries_bashs_text(argv: list[str], message: str) -> None:
    with pytest.raises(UsageError) as raised:
        parse(argv)
    assert str(raised.value) == message


def test_the_flag_check_comes_before_the_value_check() -> None:
    with pytest.raises(UsageError) as raised:
        parse(["current", "--entry"])
    assert str(raised.value) == "'--entry' is not a flag of 'current'"


def test_start_parses() -> None:
    assert parse(["start", *_WALK, "--entry", "writer", "--skipped", "none"]) == Invocation(
        command="start",
        flow="task_plan_writing",
        branch="feat_x",
        flows="flows",
        entry="writer",
        skipped="none",
    )


def test_next_parses() -> None:
    argv = ["next", *_WALK, "--outcome", "FAIL", "--node", "gate_1", "--findings", "r/f.md"]
    assert parse([*argv, "--skipped", "D,E"]) == Invocation(
        command="next",
        flow="task_plan_writing",
        branch="feat_x",
        flows="flows",
        outcome="FAIL",
        node="gate_1",
        findings="r/f.md",
        skipped="D,E",
    )


def test_current_parses() -> None:
    assert parse(["current", *_WALK]) == Invocation(
        command="current", flow="task_plan_writing", branch="feat_x", flows="flows"
    )


def test_check_round_file_parses() -> None:
    assert parse(["check-round-file", "--findings", "r/f.md"]) == Invocation(
        command="check-round-file", findings="r/f.md"
    )


def test_a_flow_with_a_tab_reaches_the_flow_name_check() -> None:
    with pytest.raises(UsageError) as raised:
        parse(["current", "--flow", "a\tb", "--branch", "b", "--flows", "f"])
    assert str(raised.value) == "unknown flow 'a\tb'"


def test_a_branch_with_a_tab_is_kept() -> None:
    parsed = parse(["current", "--flow", "f", "--branch", "a\tb", "--flows", "f"])
    assert parsed.branch == "a\tb"


def test_a_repeated_flag_keeps_its_last_value() -> None:
    parsed = parse(["current", *_WALK, "--branch", "feat_y"])
    assert parsed.branch == "feat_y"
