"""The rule this file exists to enforce: `start` and `next` hold a lock from before the walk is
read until after it is replaced, so simultaneous `next` calls recording one round's gates all land
and exactly one of them prints the round's result; `current` takes no lock.

The property is `cli/templates/scripts/flow-walker.sh` → `CONCURRENCY`'s, pinned for bash by
`cli/test/flow-walker-concurrency.test.mjs`. Here it is held at the process level: each call is a
subprocess of `sys.executable -m devscene_flow_host.commands.flow_walker` in a git repository
planted under `tmp_path` through `round_fixtures`, with `--flows` naming the checkout's own
`cli/templates/scripts/flows` directory, read-only. Every expected text is a literal written from
`flow-walker.sh`'s `REPRO` and `OUTPUT` blocks, never taken from the output of the code under test.

Deliberately not covered:
- Waiting out the 120 s lock timeout: `tests/test_flow_walker.py` →
  `test_failure_maps_each_error_type_to_status_2` covers the `TimeoutError` → exit `2` mapping.
- Bash's stale-lock breaking: a `flock` is released by the kernel when its holder exits, so no lock
  is ever left stale.
- Any duration beyond the subprocess timeout that keeps a hang from stalling the suite.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Final

import pytest

from devscene_flow_host.host.refusals import RefusalStore
from round_fixtures import PASS_BODY, init_repo

_CHECKOUT: Final = Path(__file__).resolve().parents[2]
_FLOWS: Final = str(_CHECKOUT / "cli" / "templates" / "scripts" / "flows")
_BRANCH: Final = "feat_x"
_STATE_DIR: Final = "devscene/"
_WALK: Final = ("--flow", "task_plan_writing", "--branch", _BRANCH, "--flows", _FLOWS)
_NONE: Final = ("--skipped", "none")
_COMMAND: Final = (sys.executable, "-m", "devscene_flow_host.commands.flow_walker")
_HANG_SECONDS: Final = 60
_GATES: Final = (
    ("plan_review", "p0.md"),
    ("business_parity_review", "b0.md"),
    ("architecture_review", "a0.md"),
)
_JOIN: Final = "round: 0 PASS\n"


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _text(*lines: str) -> str:
    return "".join(line + "\n" for line in lines)


def _gate_block(node: str, agent: str, tag: str) -> tuple[str, ...]:
    return (
        "action: dispatch",
        f"node: {node}",
        f"agent: {agent}",
        "arg.iteration: 0",
        "arg.review_mode: full",
        f"heartbeat: [plan-write{tag} · iter 0] → {agent}  (#<total_dispatches>)",
    )


_PENDING_SET: Final = _text(
    *_gate_block("business_parity_review", "business-parity-reviewer", " · parity"),
    *_gate_block("architecture_review", "architecture-reviewer", " · arch"),
    *_gate_block("plan_review", "task-plan-reviewer", ""),
)


def _launch(root: Path, *argv: str) -> "subprocess.Popen[str]":
    return subprocess.Popen(
        [*_COMMAND, *argv],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _finish(process: "subprocess.Popen[str]") -> str:
    """The stdout of a call that exited `0` with nothing on stderr."""
    out, err = process.communicate(timeout=_HANG_SECONDS)
    assert (process.returncode, err) == (0, ""), (process.returncode, err)
    return out


def _ok(root: Path, *argv: str) -> str:
    return _finish(_launch(root, *argv))


def _gate_call(root: Path, node: str, findings: str) -> tuple[str, ...]:
    return ("next", *_WALK, "--outcome", "PASS", "--node", node, "--findings", findings, *_NONE)


def _at_plan_round(root: Path) -> Path:
    """REPRO's fixture, walked through the command to `plan_round`'s three pending gates."""
    init_repo(root)
    (root / "devscene.config.json").write_text(
        json.dumps(
            {
                "defaultBranch": "main",
                "stateDir": _STATE_DIR,
                "phases": {"parity": True, "qa": True},
            }
        ),
        encoding="utf-8",
    )
    for _, findings in _GATES:
        (root / findings).write_text(PASS_BODY, encoding="utf-8")
    resolved = root.resolve()
    _ok(resolved, "start", *_WALK, *_NONE)
    assert _ok(resolved, "next", *_WALK, "--outcome", "returned", *_NONE) == _PENDING_SET
    return resolved


def test_simultaneous_gate_calls_print_the_rounds_result_exactly_once(tmp_path: Path) -> None:
    root = _at_plan_round(tmp_path)
    calls = [_launch(root, *_gate_call(root, node, findings)) for node, findings in _GATES]
    outputs = [_finish(call) for call in calls]
    joins = [i for i, out in enumerate(outputs) if _JOIN in out.splitlines(keepends=True)]
    assert len(joins) == 1, outputs
    assert outputs[joins[0]] == _text(
        "action: dispatch",
        "node: ui_writer",
        "agent: ui-tests-plan-writer",
        "prompt: initial",
        "round: 0 PASS",
        "ledger: P1",
        "heartbeat: [ui-test-write · iter 0] → ui-tests-plan-writer  (#<total_dispatches>)",
    )
    waits = [out for i, out in enumerate(outputs) if i != joins[0]]
    assert len(waits) == 2 and all(out.startswith("action: wait\n") for out in waits), outputs
    assert _ok(root, "current", *_WALK).startswith(
        _text("action: dispatch", "node: ui_writer", "agent: ui-tests-plan-writer")
    )


def test_current_takes_no_lock_and_next_waits_for_it(tmp_path: Path) -> None:
    root = _at_plan_round(tmp_path)
    node, findings = _GATES[0]
    with RefusalStore(root, _STATE_DIR, _BRANCH).lock():
        recording = _launch(root, *_gate_call(root, node, findings))
        assert _ok(root, "current", *_WALK) == _PENDING_SET
        assert recording.poll() is None
    assert _finish(recording) == _text(
        "action: wait",
        "node: plan_round",
        "recorded: plan_review PASS",
        "pending: business_parity_review",
        "pending: architecture_review",
    )
