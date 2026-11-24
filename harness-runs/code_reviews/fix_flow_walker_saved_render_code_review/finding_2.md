### 2. The refused-result pin never reaches the lock, so the story's top risk (a write on a walk refusal) is untested

**File:** `devscene-flow-host/tests/test_round_gates.py` (`test_a_refused_result_leaves_the_printed_reads_unchanged`) — "step = _record(walker, tmp_path, \"FAIL\", \"ui_review\")"

The story index names its top risk as a printed-reads record written on a `Refused` result, which would make a later `current` print a step the walk never reached, and says Task 2 pins the refused case. The only refused-result case in the branch is `test_a_refused_result_leaves_the_printed_reads_unchanged`. It records `FAIL` with no `--findings`, and `record_outcome` refuses that at its first check, *before* `with store.lock():`, so it never reaches the code under test. The guard that actually protects the record is `if isinstance(result.action, Refused): return result`, which comes after `walker.next` inside the lock and before `PrintedReadsStore(...).write(printed)`. No case exercises it. If someone moved that write above the guard, every test would still pass. (`test_start_writes_the_printed_reads_and_a_refused_start_keeps_them` covers the matching path in `start_walk`. Only `record_outcome` has the gap.)

**Fix:** add one case to `devscene-flow-host/tests/test_round_gates.py`, beside the existing one. It needs an outcome the graph does not declare: that passes `record_outcome`'s pre-lock check (`declared` is `None`), and GraphScene then refuses it inside the lock:

```python
def test_a_walk_refusal_inside_the_lock_leaves_the_printed_reads_unchanged(
    tmp_path: Path,
) -> None:
    walker = _walker(tmp_path)
    _at_ui_review(walker, tmp_path)
    before = printed_reads_path(tmp_path, "state", _BRANCH).read_bytes()

    step = _record(walker, tmp_path, "undeclared_outcome")
    assert isinstance(step.action, Refused), step
    assert printed_reads_path(tmp_path, "state", _BRANCH).read_bytes() == before
```

The refusal's text belongs to GraphScene and no caller parses it (`devscene-flow-host/README.md` → **Refusal texts no caller parses.**), so the case asserts only the type and the unchanged bytes. Add one clause to the module docstring's sentence *"and left byte-identical by a `Refused` result"* so it reads *"and left byte-identical by a `Refused` result, whether refused before the lock or by the walk inside it"*.

Run only that file: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_round_gates.py`.
