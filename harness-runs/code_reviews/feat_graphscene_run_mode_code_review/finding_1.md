### 1. `test_run_loop.py` has no case for two clauses of the run loop's rule: a gate's detail is recorded, and a refused record does not stop its siblings being recorded

**File:** `graphscene/tests/engine/test_run_loop.py` (module docstring and the cases after `test_cancelling_a_stalled_start_run_re_raises_and_leaves_the_dispatch_pending`); the rule under test is `graphscene/src/graphscene/engine/run_loop.py` (`_drive`) — "detail = record.detail if is_set else None" and "if refused is None and isinstance(last, Refused):"

`graphscene/src/graphscene/engine/run_loop.py`'s module docstring states, under *"The rule:"*, that every record of a set is recorded "a gate of a set as `(outcome, node, detail)`" and that "A refusal does not stop the remaining records from being recorded." The suite's own header repeats the first clause ("a gate with its detail, a lone dispatch without"). No case pins either one:

- Every gate in the suite is scripted `ScriptedOutcome("approved")` with no detail, so a `_drive` that passed `None` for every record — gate or lone dispatch — passes the whole suite unchanged. The only detail case, `test_a_lone_dispatchs_detail_is_not_recorded_and_the_launch_row_carries_it`, covers the lone-dispatch half.
- The only refusal case, `test_an_undeclared_outcome_is_refused_with_the_exact_text_and_writes_nothing`, refuses a lone dispatch, so a `_drive` that returned on the first `Refused` and dropped the rest of a set's records also passes.

Both behaviours are correct in the code today. Confirmed by a probe run through `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/run_loop_probe2.py <repo_root>`, which imported this suite's own `MemoryStore`, `Signals`, `_start`, `_stub`, `_walker` and `_gate_dispatch` and printed `1 eq: True`, `2 eq: True` and `2 current: True` for exactly the assertions below. What is missing is the cases.

**Fix:** In `graphscene/tests/engine/test_run_loop.py`, add `GateRecord` to the `from graphscene.model.walk_actions import (...)` list, then append these two cases at the end of the file:

```python
def test_a_gates_detail_is_recorded_with_its_outcome() -> None:
    stub = _stub(
        {
            "g1": [ScriptedOutcome("approved", "g1.md")],
            "g2": [ScriptedFailure("infra", "crashed"), ScriptedOutcome("approved")],
        }
    )
    store = MemoryStore()
    # The first pass's clear asks STOP once per gate; the retry pass's first ask is the third.
    assert _start(
        _walker(store), stub, signals=Signals(stop_after=2), entry="review_round"
    ) == Halt("stop", "stop requested before a set of 1")
    assert store.state is not None and store.state.open_round is not None
    assert dict(store.state.open_round.records) == {"g1": GateRecord("g1", "approved", "g1.md")}


def test_a_refused_gate_record_does_not_stop_its_siblings_being_recorded() -> None:
    stub = _stub({"g1": [ScriptedOutcome("done")], "g2": [ScriptedOutcome("approved")]})
    store = MemoryStore()
    walker = _walker(store)
    assert _start(walker, stub, entry="review_round") == Refused(
        "outcome 'done' is not declared by node 'g1'"
    )
    assert store.state is not None and store.state.open_round is not None
    assert dict(store.state.open_round.records) == {"g2": GateRecord("g2", "approved", None)}
    assert walker.current() == DispatchSet("review_round", 0, (_gate_dispatch("g1"),), ())
```

The expected values come from `_graph()`. `g1` and `g2` declare `approved`, `rejected` and `crashed`, so `done` is undeclared for `g1`. Both gates finish together and are taken in set order, so `g1` is refused first and `g2` is still recorded. In the header, extend "return the first `Refused`" to "return the first `Refused`, having still recorded every record after it". This test file is the one the fix edits, so it is the only test the fix runs.
