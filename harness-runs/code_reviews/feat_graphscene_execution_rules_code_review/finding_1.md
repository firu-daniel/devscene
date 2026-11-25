### 1. An infrastructure-only retry pass resets the undelivered breaker, so a flapping provider parks the node as a failure instead of tripping the breaker

**File:** `graphscene/src/graphscene/engine/set_execution.py` (`execute_set`): "breaker.observe(undelivered)"
**Class:** Wrong behaviour
**Failure:** If a host runs `execute_set` on a node whose runs come back `undelivered`, `undelivered`, `infra`, `undelivered`, then the set does not return `Halt("undelivered", …)` after the fourth launch. It keeps re-dispatching, and after nine launches it records the node as `failure_outcome` with `halt=None`.

`execute_set` calls `breaker.observe(undelivered)` after every pass. A pass whose only re-dispatches are `Retry`, with no `Redispatch`, therefore calls `observe(False)`, and that resets the strikes to 0. The rule this branch moves from the planning driver says otherwise. In `docs/flow-graph-walker.md` → `### How each runs a parallel round` → **Cost.**: *"An infrastructure retry is a dispatch like any other: it passes the set's safety contract again and counts against `MAX_TOTAL_DISPATCHES`, but neither against the undelivered strikes nor as a recovery through `current`."* The pilot's code works the same way. In `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_main`, the `retry)` arm only backs off and leaves `PD_STRIKES` alone. Only the `out)` arm and the `*)` (recover) arm set `PD_STRIKES=0`. `graphscene/src/graphscene/engine/breaker.py` cites the same pilot rule (`docs/flow-graph-walker.md` → `pd_undelivered`) as its basis.

A probe confirmed the failure: `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/breaker_retry_probe.py`. It scripts node `b` as (`undelivered`, `undelivered`, `infra`) three times over, with the default `UndeliveredBreaker()` and `ExecutionLimits(backoff_seconds=0)`. It printed `started 9`, `SetResult(records=(NodeRecord(node='b', outcome='error', detail='all 3 attempts failed …'),), halt=None)` and `strikes 0`. Under the pilot's rule, the strikes after each pass go 1, 2, 2 (retry, unchanged), 3, so the set trips after the fourth launch. The outage is reported as a run-level undelivered halt, not as a node failure that parks the walk through the graph's `error` binding.

**Fix.** Finding 2 lands first in the readiness order, so the halt text below is the wording Finding 2 introduces. In `execute_set`, replace

```python
        breaker.observe(undelivered)
        if breaker.tripped:
            detail = f"{breaker.strikes} consecutive sets delivered nothing"
            return SetResult((*outcomes, *held), Halt("undelivered", detail))
```

(or the same block with Finding 2's wording already applied) with

```python
        if undelivered:
            breaker.observe(True)
            if breaker.tripped:
                detail = f"{breaker.strikes} consecutive sets had an undelivered result"
                return SetResult((*outcomes, *held), Halt("undelivered", detail))
        elif not again:
            breaker.observe(False)
```

The tripped check moves inside the `undelivered` branch. Without that, a breaker the host carried in already tripped would halt a set on a retry-only pass that added no strike.

In the module docstring's `The rule:` list, replace the bullet that begins "- After each pass, `UndeliveredBreaker.observe` is told whether the pass had a `Redispatch`" with:

```
- After a pass that had a `Redispatch`, `UndeliveredBreaker.observe(True)` is called, and once the
  breaker is tripped `Halt("undelivered", "<strikes> consecutive sets had an undelivered result")`
  is returned; its limit is the breaker's own. A pass whose every node was recorded calls
  `observe(False)`. A pass with a `Retry` and no `Redispatch` leaves the breaker unchanged: an
  infrastructure retry counts neither towards the strikes nor as a delivered set
  (`docs/flow-graph-walker.md` → `### How each runs a parallel round` → **Cost.**).
```

Add this case to `graphscene/tests/engine/test_set_execution.py`. Its expected values are hand-written from the script: strikes go 1, 2, unchanged, 3.

```python
def test_an_infra_retry_pass_between_undelivered_passes_leaves_the_strikes_unchanged() -> None:
    stub = _stub(
        {
            "b": [
                ScriptedFailure("undelivered", "no result"),
                ScriptedFailure("undelivered", "no result"),
                ScriptedFailure("infra", "crashed"),
                ScriptedFailure("undelivered", "no result"),
            ]
        }
    )
    result = _execute(["b"], stub, breaker=UndeliveredBreaker())
    assert stub.started == ("b", "b", "b", "b")
    assert result == SetResult(
        (), Halt("undelivered", "3 consecutive sets had an undelivered result")
    )
```

Run only that edited file: `bash scripts/python-service.sh --package graphscene test tests/engine/test_set_execution.py`.
