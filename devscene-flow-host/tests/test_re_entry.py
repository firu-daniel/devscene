"""The rule this file exists to enforce: `start_walk` places a walk from the round files as
`flow-walker.sh`'s `start` does — its `STATE` paragraph's resume rules, with the counter at 0
and the round number carried on from the files — and clears the refusal record and the kept
findings record (`revision_findings`, which bash's `start` clears), while `current_step` re-reads
the saved walk with every refused gate left out, the last step's `refused:` lines restored and
the kept findings record unchanged, as its `current` re-prints `out=` built by `render_set`.

The graph is the harness's own format-4 graph,
`cli/templates/scripts/flows/task_plan_writing.v4.graph.json`. Config, review files and git
history are planted under `tmp_path` through `round_fixtures`. Every expected set's gates and
round number are literals written from the `STATE` paragraph and `A REFUSED ROUND FILE`, never
taken from the output of the code under test.
"""

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Final

import pytest
from graphscene import Dispatch, DispatchSet, Refused, Stop, Walker, load_graph_file

from devscene_flow_host.host.re_entry import current_step, start_walk
from devscene_flow_host.host.refusals import Refusal, refusals_path
from devscene_flow_host.host.revision_findings import RevisionFindingsStore, revision_findings_path
from devscene_flow_host.host.round_gates import HostStep, RefusedWait, record_outcome
from devscene_flow_host.host.store import walk_state_path
from devscene_flow_host.host.walking import open_walker
from round_fixtures import FAIL_BODY, PASS_BODY, commit, init_repo, plant_review

_GRAPH: Final = (
    Path(__file__).resolve().parents[2]
    / "cli"
    / "templates"
    / "scripts"
    / "flows"
    / "task_plan_writing.v4.graph.json"
)
_BRANCH: Final = "feat_x"
_PARITY: Final = "state/business_parity_reviews/feat_x"
_ARCH: Final = "state/architecture_reviews/feat_x"
_PLAN: Final = "state/task_plan_reviews/feat_x"
_STORY_INDEX: Final = "state/story_plans/feat_x_story_plan.md"
_TASK_FILE: Final = "state/task_plans/feat_x/task_1_plan.md"
_NOTE_4: Final = "state/plan_revisions/feat_x/task_plan_revision_4.md"
_NO_VERDICT_BODY: Final = "notes, and no verdict line\n"
# `flow-walker.sh` → REPRO's `bad.md`.
_NO_CLASS_BODY: Final = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Failure:** x\n"
_NO_CLASS: Final = "Must Fix entry 1 lacks **Class:**"


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def _dispatch(node: str, agent: str, round_number: int) -> Dispatch:
    """A gate's block on a fresh `start`: `arg.iteration: 0`, never converging."""
    return Dispatch(
        node=node,
        agent=agent,
        prompt=None,
        counters={"iteration": 0},
        round_number=round_number,
        converging=False,
        closed_round=(),
        passed=(),
    )


def _parity(n: int) -> Dispatch:
    return _dispatch("business_parity_review", "business-parity-reviewer", n)


def _arch(n: int) -> Dispatch:
    return _dispatch("architecture_review", "architecture-reviewer", n)


def _plan(n: int) -> Dispatch:
    return _dispatch("plan_review", "task-plan-reviewer", n)


def _plant(root: Path, n: int, reviews: Mapping[str, str]) -> Walker:
    """A repository with every phase on whose story index, task file and round-`n` review files
    under `reviews` (folder → body) are committed together, and a walker over it."""
    init_repo(root)
    (root / "devscene.config.json").write_text(
        json.dumps(
            {"defaultBranch": "main", "stateDir": "state", "phases": {"parity": True, "qa": True}}
        ),
        encoding="utf-8",
    )
    planted = []
    for relative in (_STORY_INDEX, _TASK_FILE):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("plan\n", encoding="utf-8")
        planted.append(path)
    for folder, body in reviews.items():
        planted.append(plant_review(root / folder, n, body))
    commit(root, planted, f"round {n}")
    return open_walker(root, _BRANCH, load_graph_file(_GRAPH), skipped="none")


def _start(walker: Walker, root: Path, entry: str | None = "plan_round") -> HostStep:
    return start_walk(walker, root, _BRANCH, entry)


def test_no_round_file_opens_round_0s_whole_set(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 0, {})
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 0, (_parity(0), _arch(0), _plan(0)), ())
    )


def test_a_lost_walk_opens_only_the_missing_gate_at_counter_0(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 3, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY})
    walker.start()
    walker.next("returned")
    walker.next("FAIL", "plan_review", "x")
    walker.next("PASS", "business_parity_review", "x")
    revision = walker.next("PASS", "architecture_review", "x")
    assert isinstance(revision, Dispatch), revision
    assert revision.counters == {"iteration": 1}
    walk = walk_state_path(tmp_path, "state", _BRANCH)
    walk.unlink()

    assert _start(walker, tmp_path) == HostStep(DispatchSet("plan_round", 3, (_plan(3),), ()))
    assert walk.exists()


def test_a_no_verdict_file_opens_the_whole_set_at_its_round(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 3, {_PARITY: PASS_BODY, _ARCH: _NO_VERDICT_BODY})
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 3, (_parity(3), _arch(3), _plan(3)), ())
    )


def test_a_newer_plan_commit_opens_the_whole_set_at_its_round(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 3, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY})
    (tmp_path / _STORY_INDEX).write_text("plan changed\n", encoding="utf-8")
    commit(tmp_path, [tmp_path / _STORY_INDEX], "plan")
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 3, (_parity(3), _arch(3), _plan(3)), ())
    )


def test_a_complete_round_of_passes_is_reviewed_again(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 3, {_PARITY: PASS_BODY, _ARCH: PASS_BODY, _PLAN: PASS_BODY})
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 3, (_parity(3), _arch(3), _plan(3)), ())
    )


def test_a_fail_with_the_next_note_opens_the_next_rounds_set(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 3, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY, _PLAN: PASS_BODY})
    note = tmp_path / _NOTE_4
    note.parent.mkdir(parents=True)
    note.write_text("note\n", encoding="utf-8")
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 4, (_parity(4), _arch(4), _plan(4)), ())
    )


def test_a_held_error_beside_two_committed_verdicts_opens_only_the_errored_gate(
    tmp_path: Path,
) -> None:
    walker = _plant(tmp_path, 0, {_PARITY: PASS_BODY, _ARCH: FAIL_BODY})
    walker.start()
    walker.next("returned")
    walker.next("PASS", "business_parity_review", f"{_PARITY}/review_0.md")
    walker.next("FAIL", "architecture_review", f"{_ARCH}/review_0.md")
    held = walker.next("error", "plan_review")
    assert isinstance(held, Stop), held
    assert held.reason == "error"

    assert _start(walker, tmp_path) == HostStep(DispatchSet("plan_round", 0, (_plan(0),), ()))


def _refused_wait(walker: Walker, root: Path) -> None:
    """`plan_review`'s file refused at round 0 while its two siblings are still out."""
    walker.start()
    walker.next("returned")
    plant_review(root / _PLAN, 0, _NO_CLASS_BODY)
    assert record_outcome(
        walker, root, _BRANCH, "FAIL", node="plan_review", findings=f"{_PLAN}/review_0.md"
    ) == HostStep(
        RefusedWait(
            "plan_round",
            Refusal("plan_review", 1, _NO_CLASS),
            ("business_parity_review", "architecture_review"),
        )
    )


def test_current_during_a_refusal_wait_leaves_the_refused_gate_out(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 0, {})
    _refused_wait(walker, tmp_path)
    walk = walk_state_path(tmp_path, "state", _BRANCH).read_bytes()
    refusals = refusals_path(tmp_path, "state", _BRANCH).read_bytes()

    assert current_step(walker, tmp_path, _BRANCH) == HostStep(
        DispatchSet("plan_round", 0, (_parity(0), _arch(0)), ())
    )
    assert walk_state_path(tmp_path, "state", _BRANCH).read_bytes() == walk
    assert refusals_path(tmp_path, "state", _BRANCH).read_bytes() == refusals


def test_current_after_the_re_dispatch_carries_the_refusal(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 0, {})
    _refused_wait(walker, tmp_path)
    for gate, folder in (("business_parity_review", _PARITY), ("architecture_review", _ARCH)):
        plant_review(tmp_path / folder, 0, PASS_BODY)
        record_outcome(
            walker, tmp_path, _BRANCH, "PASS", node=gate, findings=f"{folder}/review_0.md"
        )

    assert current_step(walker, tmp_path, _BRANCH) == HostStep(
        DispatchSet("plan_round", 0, (_plan(0),), ()),
        (Refusal("plan_review", 1, _NO_CLASS),),
    )


def test_start_removes_the_refusal_file_and_a_refused_start_keeps_it(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 0, {})
    _refused_wait(walker, tmp_path)
    refusals = refusals_path(tmp_path, "state", _BRANCH)

    assert _start(walker, tmp_path, "plan_review") == HostStep(
        Refused("'plan_review' is not an entry of flow 'task_plan_writing'")
    )
    assert refusals.exists()

    # `plan_review`'s refused round-0 file reads `unreadable`, so the whole set opens at round 0.
    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 0, (_parity(0), _arch(0), _plan(0)), ())
    )
    assert not refusals.exists()


def _keep(root: Path) -> Path:
    RevisionFindingsStore(root, "state", _BRANCH).write(("state/answers.md",))
    return revision_findings_path(root, "state", _BRANCH)


def test_start_removes_the_kept_findings_file_and_a_refused_start_keeps_it(
    tmp_path: Path,
) -> None:
    walker = _plant(tmp_path, 0, {})
    kept = _keep(tmp_path)

    assert _start(walker, tmp_path, "plan_review") == HostStep(
        Refused("'plan_review' is not an entry of flow 'task_plan_writing'")
    )
    assert kept.exists()

    assert _start(walker, tmp_path) == HostStep(
        DispatchSet("plan_round", 0, (_parity(0), _arch(0), _plan(0)), ())
    )
    assert not kept.exists()


def test_current_returns_the_kept_findings_file_unchanged(tmp_path: Path) -> None:
    walker = _plant(tmp_path, 0, {})
    _start(walker, tmp_path)
    kept = _keep(tmp_path)
    before = kept.read_bytes()

    assert current_step(walker, tmp_path, _BRANCH) == HostStep(
        DispatchSet("plan_round", 0, (_parity(0), _arch(0), _plan(0)), ()),
        revision_findings=("state/answers.md",),
    )
    assert kept.read_bytes() == before
