"""The rule this file exists to enforce: `main` answers each verb as `flow-walker.sh` does — the
action on stdout, and every other outcome as its header's `EXIT CODES` status with one
`flow-walker: <cause>` line on stderr and nothing on stdout — walking only through the host's
entry points.

Each case drives `main` with `io.StringIO` streams and `cwd` at a git repository planted under
`tmp_path` through `round_fixtures`, with `--flows` naming the checkout's own
`cli/templates/scripts/flows` directory, read-only. Every expected text is a literal written from
`flow-walker.sh`'s `REPRO`, `OUTPUT` and `EXIT CODES` blocks, never taken from the output of the
code under test. `current` prints the values the step read from disk as they were when it was
printed.
"""

import io
import json
import os
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Final

import pytest

from devscene_flow_host.commands.flow_walker import failure, main
from devscene_flow_host.records.errors import RecordError
from round_fixtures import FAIL_BODY, PASS_BODY, init_repo, plant_review

_CHECKOUT: Final = Path(__file__).resolve().parents[2]
_FLOWS: Final = str(_CHECKOUT / "cli" / "templates" / "scripts" / "flows")
_MANIFEST: Final = _CHECKOUT / "devscene-flow-host" / "pyproject.toml"
_BRANCH: Final = "feat_x"
_WALK: Final = ("--flow", "task_plan_writing", "--branch", _BRANCH, "--flows", _FLOWS)
_NONE: Final = ("--skipped", "none")
# `flow-walker.sh` → REPRO's `bad.md`.
_NO_CLASS_BODY: Final = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Failure:** x\n"
_UI_FINDINGS: Final = "devscene/ui_test_plan_reviews/feat_x/review_0.md"
_STORY_INDEX: Final = "devscene/story_plans/feat_x_story_plan.md"
# `flow-walker-gates.sh` → REPRO's `i.md`.
_STORY_INDEX_BODY: Final = (
    "## Rejected findings\n"
    "- **3** (rejected round 1; rebutted round 2 — call stands) — r\n"
    "- **5** (rejected round 2) — r\n"
    "## Scope register\n"
)
_VERDICTS: Final = {
    "business_parity_review": ("PASS", "b0.md"),
    "architecture_review": ("FAIL", "f0.md"),
    "plan_review": ("PASS", "p0.md"),
}
_TERMINAL: Final = (
    "action: binding",
    "binding: <terminal_handoff>",
    "node: convergence",
    "report: business_parity_review passed",
    "report: architecture_review passed",
    "report: plan_review passed",
    "report: ui_test passed",
    "ledger: P2",
)


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _text(*lines: str) -> str:
    return "".join(line + "\n" for line in lines)


def _repo(root: Path, *, config: bool = True) -> Path:
    """REPRO's fixture: its config and its `p0.md`, `b0.md`, `a0.md`, `f0.md` and `bad.md`."""
    init_repo(root)
    if config:
        (root / "devscene.config.json").write_text(
            json.dumps(
                {
                    "defaultBranch": "main",
                    "stateDir": "devscene/",
                    "phases": {"parity": True, "qa": True},
                }
            ),
            encoding="utf-8",
        )
    for name in ("p0.md", "b0.md", "a0.md"):
        (root / name).write_text(PASS_BODY, encoding="utf-8")
    (root / "f0.md").write_text(FAIL_BODY, encoding="utf-8")
    (root / "bad.md").write_text(_NO_CLASS_BODY, encoding="utf-8")
    return root.resolve()


def _call(root: Path, *argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    status = main(list(argv), stdout=out, stderr=err, cwd=root)
    return status, out.getvalue(), err.getvalue()


def _ok(root: Path, *argv: str) -> str:
    status, out, err = _call(root, *argv)
    assert (status, err) == (0, ""), (status, err)
    return out


def _refused(root: Path, status: int, *argv: str) -> str:
    """The one stderr line of a non-zero exit, with stdout asserted empty."""
    got, out, err = _call(root, *argv)
    assert (got, out) == (status, ""), (got, out, err)
    assert err.count("\n") == 1 and err.endswith("\n"), err
    return err


def _next(root: Path, outcome: str, *flags: str) -> str:
    return _ok(root, "next", *_WALK, "--outcome", outcome, *flags, *_NONE)


def _gate_block(node: str, agent: str, tag: str) -> tuple[str, ...]:
    return (
        "action: dispatch",
        f"node: {node}",
        f"agent: {agent}",
        "arg.iteration: 0",
        "arg.review_mode: full",
        f"heartbeat: [plan-write{tag} · iter 0] → {agent}  (#<total_dispatches>)",
    )


def _through_the_gates(root: Path, verdicts: Sequence[tuple[str, str, str]]) -> str:
    _ok(root, "start", *_WALK, *_NONE)
    _next(root, "returned")
    last = ""
    for node, outcome, findings in verdicts:
        last = _next(root, outcome, "--node", node, "--findings", findings)
    return last


def _at_ui_review(root: Path) -> None:
    _through_the_gates(
        root,
        (
            ("plan_review", "PASS", "p0.md"),
            ("business_parity_review", "PASS", "b0.md"),
            ("architecture_review", "PASS", "a0.md"),
        ),
    )
    _next(root, "returned")


def test_the_repro_walk_end_to_end(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    assert _ok(root, "start", *_WALK, *_NONE) == _text(
        "action: dispatch",
        "node: plan_writer",
        "agent: task-plan-writer",
        "prompt: initial",
        "arg.iteration: 0",
        "heartbeat: [plan-write · iter 0] → task-plan-writer  (#<total_dispatches>)",
    )
    assert _next(root, "returned") == _text(
        *_gate_block("business_parity_review", "business-parity-reviewer", " · parity"),
        *_gate_block("architecture_review", "architecture-reviewer", " · arch"),
        *_gate_block("plan_review", "task-plan-reviewer", ""),
    )
    assert _next(root, "PASS", "--node", "plan_review", "--findings", "p0.md") == _text(
        "action: wait",
        "node: plan_round",
        "recorded: plan_review PASS",
        "pending: business_parity_review",
        "pending: architecture_review",
    )
    assert _next(root, "PASS", "--node", "business_parity_review", "--findings", "b0.md") == (
        _text(
            "action: wait",
            "node: plan_round",
            "recorded: business_parity_review PASS",
            "pending: architecture_review",
        )
    )
    assert _next(root, "PASS", "--node", "architecture_review", "--findings", "a0.md") == _text(
        "action: dispatch",
        "node: ui_writer",
        "agent: ui-tests-plan-writer",
        "prompt: initial",
        "round: 0 PASS",
        "ledger: P1",
        "heartbeat: [ui-test-write · iter 0] → ui-tests-plan-writer  (#<total_dispatches>)",
    )
    assert _next(root, "returned") == _text(
        "action: dispatch",
        "node: ui_review",
        "agent: ui-tests-plan-reviewer",
        "arg.iteration: 0",
        "heartbeat: [ui-test-write · iter 0] → ui-tests-plan-reviewer  (#<total_dispatches>)",
    )
    assert _next(root, "PASS") == _text(*_TERMINAL)
    assert _refused(root, 1, "next", *_WALK, "--outcome", "PASS") == (
        "flow-walker: the walk has finished\n"
    )


def test_a_fail_round_reaches_the_writers_revision_with_its_files(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    last = _through_the_gates(
        root,
        (
            ("business_parity_review", "PASS", "b0.md"),
            ("plan_review", "PASS", "p0.md"),
            ("architecture_review", "FAIL", "f0.md"),
        ),
    )
    assert last == _text(
        "action: dispatch",
        "node: plan_writer",
        "agent: task-plan-writer",
        "prompt: revision",
        "arg.iteration: 1",
        "arg.findings_file: b0.md",
        "arg.findings_file: f0.md",
        "arg.findings_file: p0.md",
        "round: 0 FAIL",
        "heartbeat: [plan-write · iter 1] → task-plan-writer  (#<total_dispatches>)",
    )


def test_a_ui_review_fail_reaches_the_ui_writers_revision_and_current_reprints_it(
    tmp_path: Path,
) -> None:
    root = _repo(tmp_path)
    _at_ui_review(root)
    plant_review(root / "devscene" / "ui_test_plan_reviews" / _BRANCH, 0, FAIL_BODY)
    revision = _text(
        "action: dispatch",
        "node: ui_writer",
        "agent: ui-tests-plan-writer",
        "prompt: revision",
        f"arg.findings_file: {_UI_FINDINGS}",
        "heartbeat: [ui-test-write · iter 1] → ui-tests-plan-writer  (#<total_dispatches>)",
    )
    assert _next(root, "FAIL", "--findings", _UI_FINDINGS) == revision
    assert _ok(root, "current", *_WALK) == revision


def test_current_reprints_a_ui_reviewers_index_after_its_file_is_written(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    _at_ui_review(root)
    plant_review(root / "devscene" / "ui_test_plan_reviews" / _BRANCH, 0, FAIL_BODY)
    assert _ok(root, "current", *_WALK) == _text(
        "action: dispatch",
        "node: ui_review",
        "agent: ui-tests-plan-reviewer",
        "arg.iteration: 0",
        "heartbeat: [ui-test-write · iter 0] → ui-tests-plan-reviewer  (#<total_dispatches>)",
    )


def _to_the_plan_cap(root: Path) -> str:
    """Writer `returned`, then each printed gate's verdict, until the first binding."""
    _ok(root, "start", *_WALK, *_NONE)
    for _round in range(6):
        printed = _next(root, "returned")
        gates = [
            line[len("node: ") :] for line in printed.splitlines() if line.startswith("node: ")
        ]
        for gate in gates:
            outcome, findings = _VERDICTS[gate]
            last = _next(root, outcome, "--node", gate, "--findings", findings)
            if last.startswith("action: binding"):
                return last
    raise AssertionError("the plan round never reached its cap")


def _plan_cap(root: Path) -> str:
    return _text(
        "action: binding",
        "binding: <escalate>",
        "node: plan_round",
        "reason: cap",
        "findings_file: b0.md",
        "findings_file: f0.md",
        "findings_file: p0.md",
        "rounds: business_parity_review 0",
        "rounds: architecture_review 2",
        "rounds: plan_review 0",
        f"evidence: {root}/{_STORY_INDEX} ## Rejected findings",
        "evidence.open: - **5** (rejected round 2) — r",
        f"evidence: {root}/{_STORY_INDEX} ## Scope register",
        "summary: the plan loop reached its 5-revision cap; the gates open when it fired: "
        "architecture_review",
        # `start` resumes at round 2 from the two planted files (`round_resume`, writer entry), so
        # the fifth FAIL closes round 6.
        "round: 6 FAIL",
    )


def test_current_reprints_the_plan_rounds_cap_after_a_fail_and_an_index_edit(
    tmp_path: Path,
) -> None:
    root = _repo(tmp_path)
    index = root / _STORY_INDEX
    index.parent.mkdir(parents=True)
    index.write_text(_STORY_INDEX_BODY, encoding="utf-8")
    architecture = root / "devscene" / "architecture_reviews" / _BRANCH
    plant_review(architecture, 0, FAIL_BODY)
    plant_review(architecture, 1, FAIL_BODY)
    cap = _plan_cap(root)
    assert _to_the_plan_cap(root) == cap
    plant_review(architecture, 2, FAIL_BODY)
    index.write_text(
        _STORY_INDEX_BODY.replace(
            "## Scope register\n", "- **9** (rejected round 5) — r\n## Scope register\n"
        ),
        encoding="utf-8",
    )
    assert _ok(root, "current", *_WALK) == cap


def test_a_read_fault_at_the_cap_leaves_current_reading_the_files(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    index = root / _STORY_INDEX
    index.parent.mkdir(parents=True)
    index.write_bytes(b"## Rejected findings\n- \xff\n")
    architecture = root / "devscene" / "architecture_reviews" / _BRANCH
    plant_review(architecture, 0, FAIL_BODY)
    plant_review(architecture, 1, FAIL_BODY)
    with pytest.raises(AssertionError, match="not UTF-8 text"):
        _to_the_plan_cap(root)
    index.write_text(_STORY_INDEX_BODY, encoding="utf-8")
    assert _ok(root, "current", *_WALK) == _plan_cap(root)


@pytest.mark.parametrize("verb", ["next", "current"])
def test_no_saved_walk_is_refused_naming_the_state_file(tmp_path: Path, verb: str) -> None:
    root = _repo(tmp_path)
    flags = ("--outcome", "returned") if verb == "next" else ()
    assert _refused(root, 1, verb, *_WALK, *flags) == (
        f"flow-walker: no walk in progress at {root}/devscene/.flow_walker_state/feat_x.json: "
        "run 'start' first\n"
    )
    assert not (root / "devscene" / ".flow_walker_state").exists()


def test_an_unresolved_run_mode_is_refused_with_the_hosts_reason(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    _ok(root, "start", *_WALK, *_NONE)
    assert _refused(root, 1, "next", *_WALK, "--outcome", "returned") == (
        "flow-walker: no run-mode record: no flow-progress ledger for 'feat_x' and no skipped "
        "ids given\n"
    )


def test_check_round_file_passes_silently_and_refuses_with_status_3(tmp_path: Path) -> None:
    root = _repo(tmp_path, config=False)
    assert _call(root, "check-round-file", "--findings", "p0.md") == (0, "", "")
    assert _refused(root, 3, "check-round-file", "--findings", "bad.md") == (
        "flow-walker: bad.md: Must Fix entry 1 lacks **Class:**\n"
    )
    assert _refused(root, 3, "check-round-file", "--findings", "absent.md") == (
        "flow-walker: absent.md: no single verdict line\n"
    )


def test_a_usage_error_is_refused_with_bashs_text(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    assert _refused(root, 1, "walk") == (
        "flow-walker: unknown subcommand 'walk': expected start, next, current or "
        "check-round-file\n"
    )


def test_an_unknown_flow_is_refused_naming_the_graph_file(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    argv = ("start", "--flow", "nope", "--branch", _BRANCH, "--flows", _FLOWS)
    assert _refused(root, 1, *argv) == (
        f"flow-walker: unknown flow 'nope': no {_FLOWS}/nope.graph.json\n"
    )


def test_a_directory_outside_any_repository_is_a_fault(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.resolve()))
    plain = tmp_path / "plain"
    plain.mkdir()
    assert _refused(plain, 2, "start", *_WALK, *_NONE) == (
        "flow-walker: not inside a git repository\n"
    )


def test_a_malformed_saved_walk_is_a_fault_that_leaves_it_unchanged(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    state = root / "devscene" / ".flow_walker_state" / "feat_x.json"
    state.parent.mkdir(parents=True)
    state.write_bytes(b"{not json")
    err = _refused(root, 2, "next", *_WALK, "--outcome", "returned", *_NONE)
    assert err.startswith(f"flow-walker: {state}: "), err
    assert state.read_bytes() == b"{not json"


def test_failure_maps_each_error_type_to_status_2() -> None:
    assert failure(TimeoutError("lock held for over 120 s")) == (2, "lock held for over 120 s")
    assert failure(RecordError("no devscene.config.json at /r")) == (
        2,
        "no devscene.config.json at /r",
    )
    assert failure(KeyError("k")) == (2, "internal error: KeyError: 'k'")


def test_the_manifest_declares_the_console_script() -> None:
    manifest = tomllib.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["project"]["scripts"] == {
        "devscene-flow-walker": "devscene_flow_host.commands.flow_walker:main"
    }


def test_the_module_runs_as_a_program_writing_to_the_real_stdout(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "devscene_flow_host.commands.flow_walker", "start", *_WALK, *_NONE],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert (result.returncode, result.stderr) == (0, "")
    assert result.stdout == _text(
        "action: dispatch",
        "node: plan_writer",
        "agent: task-plan-writer",
        "prompt: initial",
        "arg.iteration: 0",
        "heartbeat: [plan-write · iter 0] → task-plan-writer  (#<total_dispatches>)",
    )
