"""The rule this file exists to enforce: `AttemptBook.settle` records a completion and an agent
failure at once, never retrying an agent failure; re-dispatches an undelivered result without
using up an attempt; retries an infra failure for that node alone until its last attempt, then
records `failure_outcome` with every attempt's reason; and restarts a node's count once it is
recorded (`graphscene.engine.attempts`). Every expected `Settlement` and `detail` is hand-written.
"""

from graphscene.engine.attempts import AttemptBook
from graphscene.model.execution import Completed, Failed
from graphscene.model.run_control import (
    ExecutionLimits,
    NodeRecord,
    Recorded,
    Redispatch,
    Retry,
)

_LIMITS = ExecutionLimits(max_attempts=3)


def test_a_completion_records_its_outcome_and_detail() -> None:
    book = AttemptBook()
    settled = book.settle("draft", Completed("pass", "all good"), _LIMITS, "error")
    assert settled == Recorded(NodeRecord("draft", "pass", "all good"))
    assert book.attempt("draft") == 1


def test_an_agent_failure_on_attempt_one_records_the_failure_outcome_with_no_retry() -> None:
    book = AttemptBook()
    settled = book.settle("draft", Failed("agent", "could not finish"), _LIMITS, "error")
    assert settled == Recorded(NodeRecord("draft", "error", "could not finish"))
    assert not isinstance(settled, Retry)
    assert book.attempt("draft") == 1


def test_an_agent_failure_after_an_infra_retry_still_records_at_once() -> None:
    book = AttemptBook()
    book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    settled = book.settle("draft", Failed("agent", "gave up"), _LIMITS, "error")
    assert settled == Recorded(NodeRecord("draft", "error", "gave up"))
    assert not isinstance(settled, Retry)
    assert book.attempt("draft") == 1


def test_infra_on_attempts_one_and_two_retries_as_attempts_two_and_three() -> None:
    book = AttemptBook()
    assert book.attempt("draft") == 1
    first = book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    assert first == Retry("draft", 2, "crash")
    assert book.attempt("draft") == 2
    second = book.settle("draft", Failed("infra", "timeout"), _LIMITS, "error")
    assert second == Retry("draft", 3, "timeout")
    assert book.attempt("draft") == 3


def test_infra_on_attempt_three_records_the_three_line_detail() -> None:
    book = AttemptBook()
    book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    book.settle("draft", Failed("infra", "timeout"), _LIMITS, "error")
    settled = book.settle("draft", Failed("infra", "unparseable return"), _LIMITS, "error")
    assert settled == Recorded(
        NodeRecord(
            "draft",
            "error",
            "all 3 attempts failed for an infrastructure reason\n"
            "attempt 1 of 3: crash\n"
            "attempt 2 of 3: timeout\n"
            "attempt 3 of 3: unparseable return",
        )
    )
    assert book.attempt("draft") == 1


def test_an_undelivered_result_between_two_infra_failures_leaves_the_attempt_unchanged() -> None:
    book = AttemptBook()
    assert book.settle("draft", Failed("infra", "crash"), _LIMITS, "error") == Retry(
        "draft", 2, "crash"
    )
    assert book.attempt("draft") == 2
    settled = book.settle("draft", Failed("undelivered", "no result"), _LIMITS, "error")
    assert settled == Redispatch("draft", "no result")
    assert book.attempt("draft") == 2
    assert book.settle("draft", Failed("infra", "timeout"), _LIMITS, "error") == Retry(
        "draft", 3, "timeout"
    )
    assert book.settle("draft", Failed("infra", "crash again"), _LIMITS, "error") == Recorded(
        NodeRecord(
            "draft",
            "error",
            "all 3 attempts failed for an infrastructure reason\n"
            "attempt 1 of 3: crash\n"
            "attempt 2 of 3: timeout\n"
            "attempt 3 of 3: crash again",
        )
    )


def test_an_undelivered_result_on_a_fresh_node_leaves_it_on_attempt_one() -> None:
    book = AttemptBook()
    settled = book.settle("draft", Failed("undelivered", "provider down"), _LIMITS, "error")
    assert settled == Redispatch("draft", "provider down")
    assert book.attempt("draft") == 1


def test_after_a_completion_the_next_infra_failure_is_attempt_one_again() -> None:
    book = AttemptBook()
    book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    assert book.attempt("draft") == 2
    book.settle("draft", Completed("pass"), _LIMITS, "error")
    assert book.attempt("draft") == 1
    settled = book.settle("draft", Failed("infra", "timeout"), _LIMITS, "error")
    assert settled == Retry("draft", 2, "timeout")


def test_two_nodes_counts_are_independent() -> None:
    book = AttemptBook()
    book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    book.settle("draft", Failed("infra", "crash"), _LIMITS, "error")
    assert book.attempt("draft") == 3
    assert book.attempt("review") == 1
    settled = book.settle("review", Failed("infra", "timeout"), _LIMITS, "error")
    assert settled == Retry("review", 2, "timeout")
    assert book.attempt("draft") == 3


def test_max_attempts_one_records_on_the_first_infra_failure() -> None:
    book = AttemptBook()
    settled = book.settle(
        "draft", Failed("infra", "crash"), ExecutionLimits(max_attempts=1), "error"
    )
    assert settled == Recorded(
        NodeRecord(
            "draft",
            "error",
            "all 1 attempts failed for an infrastructure reason\nattempt 1 of 1: crash",
        )
    )
    assert book.attempt("draft") == 1
