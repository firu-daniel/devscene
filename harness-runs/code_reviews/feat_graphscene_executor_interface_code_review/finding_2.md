### 2. The stub's cancellation during a scripted delay is promised but never tested

**File:** `graphscene/tests/adapters/test_stub_executor.py` (`test_a_stall_is_cancelled_by_the_callers_deadline`); the rule under test is in `graphscene/src/graphscene/adapters/stub_executor.py` (module docstring) — "On `asyncio.CancelledError`, during a delay or a stall"

`StubExecutor`'s rule states that cancellation is recorded in `cancelled` and re-raised **during a delay or a stall**. The suite cancels only a `ScriptedStall`. The delay path is a separate code path: `_play` awaits `asyncio.sleep(entry.delay)` and never reaches `asyncio.Event().wait()`. That path is the one #484's engine-owned deadline will hit when a scripted outcome is slower than the deadline. No case covers it, so a regression there would pass the suite. For example, a refactor might move the `try` so that it wraps only the stall branch. The story plan's second top risk is *"A stub that swallows cancellation"*.

The behaviour holds today. `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_probe2.py` ran a `ScriptedOutcome("done", delay=10.0)` under `asyncio.wait_for(…, timeout=0.01)` and printed `started == ('x',)`, `finished == ()` and `cancelled == ('x',)`. This finding asks only for the missing case.

**Fix.** Add this case to `graphscene/tests/adapters/test_stub_executor.py`, directly after `test_a_stall_is_cancelled_by_the_callers_deadline`:

```python
def test_a_delayed_result_is_cancelled_by_the_callers_deadline() -> None:
    stub = StubExecutor({"draft": [ScriptedOutcome("done", delay=60.0)]})

    async def with_deadline() -> NodeResult:
        return await asyncio.wait_for(stub.run(_dispatch("draft")), timeout=0.01)

    with pytest.raises(TimeoutError):
        asyncio.run(with_deadline())
    assert stub.started == ("draft",)
    assert stub.cancelled == ("draft",)
    assert stub.finished == ()
```

Then add one clause to the file's module docstring. Its last sentence currently reads *"and re-raises cancellation out of a stall rather than returning a result"*. Change it to *"and re-raises cancellation out of a stall or a delay rather than returning a result"*. No duration is asserted, which keeps the header's *"No duration is asserted"* rule.

This test file is the one the fix edits, so it is the only test file the fix runs.
