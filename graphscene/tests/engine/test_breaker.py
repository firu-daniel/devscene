"""The rule this file exists to enforce: `UndeliveredBreaker` trips once its consecutive
undelivered sets reach its limit, `3` by default and otherwise the constructor's argument; a
delivered set and `reset` clear its strikes; and a limit below 1 is refused with an exact
`ValueError` (`graphscene.engine.breaker`).
"""

import pytest

from graphscene.engine.breaker import UndeliveredBreaker


def test_the_default_limit_is_three_and_the_third_undelivered_set_trips_it() -> None:
    breaker = UndeliveredBreaker()
    assert breaker.limit == 3
    assert breaker.observe(True) == 1
    assert breaker.observe(True) == 2
    assert not breaker.tripped
    assert breaker.observe(True) == 3
    assert breaker.tripped


def test_a_limit_of_two_trips_on_the_second_set() -> None:
    breaker = UndeliveredBreaker(2)
    breaker.observe(True)
    assert not breaker.tripped
    breaker.observe(True)
    assert breaker.tripped
    assert breaker.strikes == 2


def test_a_delivered_set_in_between_resets_the_strikes() -> None:
    breaker = UndeliveredBreaker()
    breaker.observe(True)
    breaker.observe(True)
    assert breaker.observe(False) == 0
    breaker.observe(True)
    breaker.observe(True)
    assert breaker.strikes == 2
    assert not breaker.tripped


def test_reset_clears_a_tripped_breaker() -> None:
    breaker = UndeliveredBreaker(1)
    breaker.observe(True)
    assert breaker.tripped
    breaker.reset()
    assert breaker.strikes == 0
    assert not breaker.tripped


def test_a_limit_below_one_is_refused() -> None:
    with pytest.raises(ValueError) as raised:
        UndeliveredBreaker(0)
    assert str(raised.value) == "UndeliveredBreaker: limit must be >= 1, got 0"
