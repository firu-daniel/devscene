"""The rule this file exists to enforce: `NodeSessions` writes each usage record's stream to
`<log stem>.planning/<seq>-<node>.stream.jsonl` and appends it to `<log stem>.stream.jsonl`,
appends one compact `{"session_id","seq","node"}` manifest line with `seq` a string, pipes the
stream through the formatter into the log; numbers past the `<n>-*.stream.jsonl` files already
there; pairs a `Launch` with a pending usage of its node carrying an equal `result`, or, for a
`Launch` whose result is `Failed("infra", …)`, with one carrying a `Completed`; gives a
timeout `Launch` with no usage a `-` row and no exception; keeps each node's last `Launch` result;
keeps a node's attempt log only when its last attempt also failed for an infrastructure reason;
and adds each per-session observation
category once for its case.

Every log path is under `tmp_path`; the formatter is `cat` or `true` on `PATH`; `Observations` is
a recording stand-in. Every expected value is a literal written from the task plan's contract,
never taken from the code under test.

Deliberately not covered:
- What the driver does with a `Failed` or a row: the driver's suites.
- Reading the manifest through `run-analytics.sh`: that script's own suite.
"""

from datetime import UTC, datetime
from pathlib import Path

from graphscene import Completed, Failed, Launch, LaunchSink, NodeResult

from devscene_flow_host.host.claude_executor import SessionUsage, UsageSink
from devscene_flow_host.host.node_sessions import NodeSessions
from devscene_flow_host.host.observations import Observations


class _RecordingObservations(Observations):
    def __init__(self) -> None:
        super().__init__()
        self.added: list[tuple[str, str, str, str]] = []

    def add(self, category: str, problem: str, evidence: str, cost: str) -> None:
        self.added.append((category, problem, evidence, cost))


def _usage(
    node: str,
    result: NodeResult,
    *,
    session_id: str | None = "s",
    stream: str = "",
    stderr_tail: str = "",
    denials: int = 0,
    cost: float | None = 0.5,
    return_document: dict[str, object] | None = None,
) -> SessionUsage:
    return SessionUsage(
        node=node,
        agent=f"{node}-agent",
        agent_prompt="",
        session_id=session_id,
        started_at=datetime(2026, 11, 27, tzinfo=UTC),
        duration_seconds=12.4,
        stalled=False,
        total_cost_usd=cost,
        cache_creation_input_tokens=None,
        cache_read_input_tokens=None,
        model_usage={},
        permission_denials=denials,
        withheld_tools=(),
        stream=stream,
        stderr_tail=stderr_tail,
        returncode=0,
        return_document=return_document,
        result=result,
    )


def _sessions(
    tmp_path: Path, formatter: str = "true"
) -> tuple[NodeSessions, _RecordingObservations, list[str]]:
    observations = _RecordingObservations()
    narrated: list[str] = []
    sessions = NodeSessions(
        log_path=tmp_path / "run.log",
        formatter=formatter,
        observations=observations,
        narrate=narrated.append,
    )
    return sessions, observations, narrated


def test_it_answers_both_sink_protocols(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    usage_sink: UsageSink = sessions
    launch_sink: LaunchSink = sessions
    assert usage_sink is sessions
    assert launch_sink is sessions


def test_two_sessions_write_their_streams_the_run_stream_and_the_manifest(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), session_id="a1", stream="w\n"))
    sessions.record(_usage("plan_review", Completed("approved"), session_id="b2", stream="r\n"))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("done")))
    sessions.record(Launch(2, "plan_review", "plan_review-agent", 1, 3, Completed("approved")))

    planning = tmp_path / "run.planning"
    assert (planning / "1-plan_writer.stream.jsonl").read_text(encoding="utf-8") == "w\n"
    assert (planning / "2-plan_review.stream.jsonl").read_text(encoding="utf-8") == "r\n"
    assert (tmp_path / "run.stream.jsonl").read_text(encoding="utf-8") == "w\nr\n"
    assert (planning / "node-sessions.jsonl").read_text(encoding="utf-8") == (
        '{"session_id":"a1","seq":"1","node":"plan_writer"}\n'
        '{"session_id":"b2","seq":"2","node":"plan_review"}\n'
    )
    assert sessions.rows == (
        "1 plan_writer plan_writer-agent 1/3 done 12s 0.5",
        "2 plan_review plan_review-agent 1/3 approved 12s 0.5",
    )


def test_a_session_without_an_id_writes_no_manifest_line(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), session_id=None, stream="w\n"))
    assert not (tmp_path / "run.planning" / "node-sessions.jsonl").exists()


def test_a_second_drive_numbers_past_the_files_already_there(tmp_path: Path) -> None:
    planning = tmp_path / "run.planning"
    planning.mkdir()
    (planning / "3-x.stream.jsonl").write_text("", encoding="utf-8")
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), stream="w\n"))
    assert (planning / "4-plan_writer.stream.jsonl").read_text(encoding="utf-8") == "w\n"


def test_a_cat_formatter_puts_the_stream_and_the_stderr_tail_into_the_log(tmp_path: Path) -> None:
    (tmp_path / "run.log").write_text("before\n", encoding="utf-8")
    sessions, _, _ = _sessions(tmp_path, formatter="cat")
    sessions.record(_usage("plan_writer", Completed("done"), stream="w\n", stderr_tail="oops"))
    assert (tmp_path / "run.log").read_text(encoding="utf-8") == "before\nw\noops\n"


def test_a_formatter_that_cannot_start_is_narrated(tmp_path: Path) -> None:
    missing = str(tmp_path / "no-such-formatter")
    sessions, _, narrated = _sessions(tmp_path, formatter=missing)
    sessions.record(_usage("plan_writer", Completed("done"), stream="w\n"))
    assert len(narrated) == 1
    assert narrated[0].startswith(f"the formatter '{missing}' could not run: ")


def test_a_timeout_launch_without_usage_gives_its_row_and_no_exception(tmp_path: Path) -> None:
    sessions, _, narrated = _sessions(tmp_path)
    timeout = Failed("infra", "timed out: no result within 5s")
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, timeout))
    assert sessions.rows == ("- plan_writer plan_writer-agent 1/3 failed - -",)
    assert narrated == ["no usage record for plan_writer (total-run timeout)"]


def test_a_mismatched_result_is_not_paired(tmp_path: Path) -> None:
    sessions, _, narrated = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done")))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("other")))
    assert sessions.rows == ("- plan_writer plan_writer-agent 1/3 other - -",)
    assert narrated == ["no usage record for plan_writer (total-run timeout)"]


def test_a_completed_usage_pairs_with_the_infra_failure_the_planning_executor_made(
    tmp_path: Path,
) -> None:
    sessions, _, narrated = _sessions(tmp_path)
    sessions.record(_usage("plan_review", Completed("PASS")))
    refused = Failed("infra", "PASS carries no findings_file")
    sessions.record(Launch(1, "plan_review", "plan_review-agent", 1, 3, refused))
    assert sessions.rows == ("1 plan_review plan_review-agent 1/3 failed 12s 0.5",)
    assert narrated == []


def test_a_missing_cost_is_a_dash(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), cost=None))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("done")))
    assert sessions.rows == ("1 plan_writer plan_writer-agent 1/3 done 12s -",)


def test_the_last_return_document_is_kept_per_node(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), return_document={"n": 1}))
    sessions.record(_usage("plan_writer", Completed("done"), return_document={"n": 2}))
    sessions.record(_usage("plan_writer", Completed("done")))
    assert sessions.return_document("plan_writer") == {"n": 2}
    assert sessions.return_document("plan_review") is None


def test_the_last_launch_result_is_kept_per_node(tmp_path: Path) -> None:
    sessions, _, _ = _sessions(tmp_path)
    sessions.record(Launch(1, "plan_review", "plan_review-agent", 1, 3, Failed("infra", "crash")))
    sessions.record(Launch(2, "plan_review", "plan_review-agent", 2, 3, Failed("agent", "no doc")))
    assert sessions.launch_result("plan_review") == Failed("agent", "no doc")
    assert sessions.launch_result("plan_writer") is None


def test_a_node_whose_every_attempt_failed_for_infra_keeps_its_attempt_log(
    tmp_path: Path,
) -> None:
    sessions, _, _ = _sessions(tmp_path)
    for attempt, reason in (
        (1, "launch failed"),
        (2, "PASS carries no findings_file"),
        (3, "stalled"),
    ):
        failed = Failed("infra", reason)
        sessions.record(_usage("plan_review", failed))
        sessions.record(Launch(attempt, "plan_review", "plan_review-agent", attempt, 3, failed))
    assert sessions.exhausted_attempts("plan_review") == (
        3,
        (
            "attempt 1 of 3 (#1): launch failed",
            "attempt 2 of 3 (#2): PASS carries no findings_file",
            "attempt 3 of 3 (#3): stalled",
        ),
    )


def test_a_node_that_recovers_after_an_infra_failure_keeps_no_attempt_log(
    tmp_path: Path,
) -> None:
    sessions, _, _ = _sessions(tmp_path)
    failed = Failed("infra", "launch failed")
    sessions.record(_usage("plan_review", failed))
    sessions.record(Launch(1, "plan_review", "plan_review-agent", 1, 3, failed))
    sessions.record(_usage("plan_review", Completed("PASS", "r.md")))
    sessions.record(Launch(2, "plan_review", "plan_review-agent", 2, 3, Completed("PASS", "r.md")))
    assert sessions.exhausted_attempts("plan_review") is None


def test_permission_denials_are_a_tooling_gap(tmp_path: Path) -> None:
    sessions, observations, _ = _sessions(tmp_path)
    sessions.record(_usage("plan_writer", Completed("done"), denials=2))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, Completed("done")))
    assert observations.added == [
        (
            "tooling-gap",
            "A planning node session met permission denials",
            "#1 plan_writer (plan_writer-agent): 2 denial(s)",
            "2 refused tool call(s)",
        )
    ]


def test_an_infra_failure_with_attempts_left_is_flow_efficiency(tmp_path: Path) -> None:
    sessions, observations, _ = _sessions(tmp_path)
    failed = Failed("infra", "crashed")
    sessions.record(_usage("plan_writer", failed))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, failed))
    assert observations.added == [
        (
            "flow-efficiency",
            "A planning node session failed for an infrastructure reason and was re-dispatched",
            "#1 plan_writer (plan_writer-agent): attempt 1 of 3: crashed",
            "one re-dispatch of plan_writer",
        )
    ]


def test_a_final_failure_is_a_silent_failure(tmp_path: Path) -> None:
    sessions, observations, _ = _sessions(tmp_path)
    failed = Failed("infra", "crashed")
    sessions.record(_usage("plan_writer", failed))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 3, 3, failed))
    agent_failed = Failed("agent", "gave up")
    sessions.record(_usage("plan_review", agent_failed))
    sessions.record(Launch(2, "plan_review", "plan_review-agent", 1, 3, agent_failed))
    assert observations.added == [
        (
            "silent-failure",
            "A planning node session ended in error",
            "#1 plan_writer (plan_writer-agent): crashed",
            "one dispatch recorded as error",
        ),
        (
            "silent-failure",
            "A planning node session ended in error",
            "#2 plan_review (plan_review-agent): gave up",
            "one dispatch recorded as error",
        ),
    ]


def test_an_undelivered_or_completed_session_adds_no_observation(tmp_path: Path) -> None:
    sessions, observations, _ = _sessions(tmp_path)
    undelivered = Failed("undelivered", "no result")
    sessions.record(_usage("plan_writer", undelivered))
    sessions.record(Launch(1, "plan_writer", "plan_writer-agent", 1, 3, undelivered))
    sessions.record(_usage("plan_review", Completed("approved")))
    sessions.record(Launch(2, "plan_review", "plan_review-agent", 1, 3, Completed("approved")))
    assert observations.added == []
