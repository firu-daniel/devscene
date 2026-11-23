"""The rule this file exists to enforce: `HarnessPredicateHost` answers `phase_<p>_off` from
`phases.<p>` and `run_mode_skips_<id>` from the run mode, re-reading both records on every call;
whatever it cannot answer is `None` with one exact `refusal_reason`, and a `RecordError`
propagates.

Every record is planted under `tmp_path`; every expected value is a literal written from the
rules in the task plan.
"""

import json
from pathlib import Path

import pytest
from graphscene import PredicateHost

from devscene_flow_host.host.predicates import HarnessPredicateHost
from devscene_flow_host.records.errors import RecordError

_BRANCH = "feat_x"
_RUN_MODE_PREDICATES = ("run_mode_skips_parity", "run_mode_skips_architecture", "run_mode_skips_qa")


def _plant_config(root: Path, phases: object) -> None:
    (root / "devscene.config.json").write_text(
        json.dumps({"defaultBranch": "main", "stateDir": "state/", "phases": phases}),
        encoding="utf-8",
    )


def _plant_ledger(root: Path, skipped: str) -> None:
    path = root / "state" / "flow_progress" / f"{_BRANCH}_progress.md"
    path.parent.mkdir(parents=True)
    path.write_text(f"## Run mode\n- skipped: {skipped}\n", encoding="utf-8")


def test_it_satisfies_graphscenes_predicate_host(tmp_path: Path) -> None:
    host: PredicateHost = HarnessPredicateHost(tmp_path, _BRANCH)
    assert isinstance(host, HarnessPredicateHost)


def test_a_phase_off_skips_and_a_phase_on_does_not(tmp_path: Path) -> None:
    _plant_config(tmp_path, {"parity": False, "qa": True})
    host = HarnessPredicateHost(tmp_path, _BRANCH)
    assert host.answer("phase_parity_off", "parity_review") is True
    assert host.answer("phase_qa_off", "ui_writer") is False
    assert host.answer("phase_docs_off", "docs") is True
    for predicate in ("phase_parity_off", "phase_qa_off", "phase_docs_off"):
        assert host.refusal_reason(predicate) is None


def test_an_unresolvable_phase_is_refused(tmp_path: Path) -> None:
    _plant_config(tmp_path, {"parity": "on"})
    host = HarnessPredicateHost(tmp_path, _BRANCH)
    assert host.answer("phase_parity_off", "parity_review") is None
    assert host.refusal_reason("phase_parity_off") == (
        f"cannot resolve phases.parity in {tmp_path}/devscene.config.json"
    )


def test_the_ledger_wins_over_the_skipped_argument(tmp_path: Path) -> None:
    _plant_config(tmp_path, {})
    _plant_ledger(tmp_path, "parity")
    host = HarnessPredicateHost(tmp_path, _BRANCH, skipped="qa")
    assert host.answer("run_mode_skips_parity", "parity_review") is True
    assert host.answer("run_mode_skips_qa", "ui_writer") is False
    assert host.answer("run_mode_skips_architecture", "architecture") is False
    for predicate in _RUN_MODE_PREDICATES:
        assert host.refusal_reason(predicate) is None


def test_with_no_ledger_the_skipped_argument_answers(tmp_path: Path) -> None:
    _plant_config(tmp_path, {})
    host = HarnessPredicateHost(tmp_path, _BRANCH, skipped="none")
    for predicate in _RUN_MODE_PREDICATES:
        assert host.answer(predicate, "node") is False
        assert host.refusal_reason(predicate) is None


def test_with_no_ledger_and_no_skipped_argument_the_run_mode_is_refused(tmp_path: Path) -> None:
    _plant_config(tmp_path, {})
    host = HarnessPredicateHost(tmp_path, _BRANCH)
    for predicate in _RUN_MODE_PREDICATES:
        assert host.answer(predicate, "node") is None
        assert host.refusal_reason(predicate) == (
            "no run-mode record: no flow-progress ledger for 'feat_x' and no skipped ids given"
        )


def test_an_unknown_name_is_refused(tmp_path: Path) -> None:
    _plant_config(tmp_path, {})
    host = HarnessPredicateHost(tmp_path, _BRANCH, skipped="none")
    assert host.answer("stage_disabled", "node") is None
    assert host.refusal_reason("stage_disabled") == (
        "'stage_disabled' is not a predicate the harness answers"
    )
    assert host.answer("phase_lint_off", "node") is None
    assert host.refusal_reason("phase_lint_off") == (
        "'phase_lint_off' is not a predicate the harness answers"
    )


def test_the_records_are_re_read_on_every_call(tmp_path: Path) -> None:
    _plant_config(tmp_path, {})
    host = HarnessPredicateHost(tmp_path, _BRANCH, skipped="none")
    assert host.answer("run_mode_skips_qa", "ui_writer") is False
    _plant_ledger(tmp_path, "qa")
    assert host.answer("run_mode_skips_qa", "ui_writer") is True


def test_a_missing_config_raises_a_record_error(tmp_path: Path) -> None:
    host = HarnessPredicateHost(tmp_path, _BRANCH)
    with pytest.raises(RecordError):
        host.answer("phase_qa_off", "ui_writer")
