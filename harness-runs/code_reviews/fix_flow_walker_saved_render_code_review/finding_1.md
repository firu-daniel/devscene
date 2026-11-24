### 1. A read fault after the walk is saved leaves the previous step's printed reads, so `current` prints the new step from them

**File:** `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` (`record_outcome`) — "else read_printed(graph, repo_root, state_dir, branch, result.action)"; and `devscene-flow-host/src/devscene_flow_host/host/re_entry.py` (`start_walk`) — "printed = read_printed(walker.graph, repo_root, state_dir, branch, step)"
**Class:** Wrong behaviour
**Failure:** If `next` reaches `ui_review` while that reviewer's findings folder cannot be listed, then `next` exits 2 with the walk already saved at `ui_review`, and once the folder can be listed again `current` exits 0 and prints the `ui_review` dispatch with no `arg.iteration:` line. Before this branch, the same `current` printed `arg.iteration: 0`.

`record_outcome` saves the walk inside `_record` (`walker.next`) and only then calls `read_printed` for the returned step. `start_walk` does the same after `walker.start`. `read_printed` reads disk: `review_iteration` lists a findings folder, `fail_count` reads each review file, and `read_index_evidence` raises `RecordError` for a story index that is not UTF-8. If any of those raises, the exception propagates and `PrintedReadsStore.write` never runs. The walk has moved to the new step, but the record on disk still holds the previous step's reads.

`current_step` then finds a record, so it skips its disk fallback (`if printed is None:`) and returns the stale record:
- For a non-round reviewer, `render` → `_block` looks the node up with `dict(step.printed.review_iterations).get(dispatch.node)`. It gets `None` and silently drops the `arg.iteration:` line, which the orchestrator parses.
- For a cap, `_cap_lines` raises `the printed reads carry no count for '<gate>'`, and it keeps raising after the faulty file is fixed. Before this branch, `current` re-read the files and recovered as soon as the file was fixed.

The module docstring's *"A crash between the walk's write and this one, which leaves the previous step's reads"* names a process crash. This is an ordinary, deterministic exception path, and `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **A rendering fault after the save.** does not record it.

Confirmed by a probe run with `bash scripts/python-service.sh --package devscene-flow-host probe harness-runs/scratch/printed_reads_stale_probe.py <repo_root>`. The probe built the `test_round_gates.py` walk (every phase on, `start`, `returned`, three `PASS`es, so the walk is at `ui_writer`), set the empty `state/ui_test_plan_reviews/feat_x` folder to mode `0`, and called `record_outcome(..., "returned")`. That call raised `PermissionError [Errno 13] Permission denied: '…/state/ui_test_plan_reviews/feat_x'`. With the mode restored to `0o755`, `walker.current()` was `Dispatch(node='ui_review', …)`, and `current_step(...).printed` was `PrintedReads(review_iterations=(), round_counts=(), index_evidence=None)`: no entry for `ui_review`.

**Fix:** when `read_printed` raises after the walk is saved, remove the printed-reads record before re-raising. `current` then falls back to reading the files, as it did before this branch, and recovers once the file is fixed.

1. In `devscene-flow-host/src/devscene_flow_host/host/printed_reads.py`, give `PrintedReadsStore` a `clear` method like `RevisionFindingsStore.clear`:

   ```python
   def clear(self) -> None:
       self._path.unlink(missing_ok=True)
   ```

   Replace the docstring's *"Deliberately not covered"* bullet *"A crash between the walk's write and this one, which leaves the previous step's reads."* with:
   *"A crash between the walk's write and this one, which leaves the previous step's reads; an exception from `read_printed` after the walk's write clears the record instead (`clear`), so `current_step` reads the files."*

2. In `record_outcome` (`round_gates.py`), replace the `printed = (...)` assignment and the `PrintedReadsStore(...).write(printed)` line with:

   ```python
   printed_store = PrintedReadsStore(repo_root, state_dir, branch)
   try:
       printed = (
           PrintedReads()
           if isinstance(result.action, RefusedWait)
           else read_printed(graph, repo_root, state_dir, branch, result.action)
       )
   except BaseException:
       printed_store.clear()
       raise
   printed_store.write(printed)
   ```

3. In `start_walk` (`re_entry.py`), replace the two lines `printed = read_printed(...)` / `PrintedReadsStore(...).write(printed)` with:

   ```python
   printed_store = PrintedReadsStore(repo_root, state_dir, branch)
   try:
       printed = read_printed(walker.graph, repo_root, state_dir, branch, step)
   except BaseException:
       printed_store.clear()
       raise
   printed_store.write(printed)
   ```

   Both stay inside the existing `with store.lock():` block.

4. In `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **A rendering fault after the save.**, append this sentence after *"so a rendering fault exits `2` with the walk already saved"*'s sentence:
   *"A fault in `read_printed` (`host/printed_reads.py`) after the save exits `2` the same way and removes the printed-reads record, so a later `current` reads the files again."*

5. Pin it in `devscene-flow-host/tests/test_flow_walker.py`:
   - Move the `cap = _text(...)` literal out of `test_current_reprints_the_plan_rounds_cap_after_a_fail_and_an_index_edit` into a module-level `def _plan_cap(root: Path) -> str:` that returns it, and call it from that test.
   - Add this case:

   ```python
   def test_a_read_fault_at_the_cap_leaves_current_reading_the_files(tmp_path: Path) -> None:
       root = _repo(tmp_path)
       index = root / _STORY_INDEX
       index.parent.mkdir(parents=True)
       index.write_bytes(b"## Rejected findings\n- \xff\n")
       architecture = root / "devscene" / "architecture_reviews" / _BRANCH
       plant_review(architecture, 0, FAIL_BODY)
       plant_review(architecture, 1, FAIL_BODY)
       with pytest.raises(AssertionError, match="not UTF-8 text"):
           _to_the_plan_cap(root)
       index.write_text(_STORY_INDEX_BODY, encoding="utf-8")
       assert _ok(root, "current", *_WALK) == _plan_cap(root)
   ```

   The `next` that reaches the cap exits 2 with `RecordError`'s `<index>: not UTF-8 text`, and `_ok` turns that into the `AssertionError`. Without steps 1–3, the `current` exits 2 with `the printed reads carry no count for 'business_parity_review'`.

   Run the suite this step edits: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_flow_walker.py`.
