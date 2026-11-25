### 3. `_check_delay` accepts a NaN delay

**File:** `graphscene/src/graphscene/adapters/stub_executor.py` (`_check_delay`) — "if delay < 0:"

`_check_delay` refuses a negative delay with `delay < 0`. That comparison is `False` for `float("nan")`, so `ScriptedOutcome("done", delay=math.nan)` constructs without complaint. A probe confirmed this: `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_probe2.py` printed `nan accepted ScriptedOutcome(outcome='done', detail=None, delay=nan)`. The NaN then reaches `asyncio.sleep`, whose timer arithmetic with NaN is not something any test author means to script. The guard exists to refuse a delay that is not a non-negative number, and NaN is one.

**Fix.** In `graphscene/src/graphscene/adapters/stub_executor.py`, change the guard so that the comparison fails for NaN too. Keep the message unchanged:

```python
def _check_delay(owner: object, delay: float) -> None:
    if not delay >= 0:
        raise ValueError(f"{type(owner).__name__}: delay must be >= 0, got {delay}")
```

In `graphscene/tests/adapters/test_stub_executor.py`, extend `test_a_negative_delay_is_refused` with one more assertion, and add `import math` to the imports:

```python
    with pytest.raises(ValueError) as nan:
        ScriptedOutcome("done", delay=math.nan)
    assert str(nan.value) == "ScriptedOutcome: delay must be >= 0, got nan"
```

This test file is the one the fix edits, so it is the only test file the fix runs.
