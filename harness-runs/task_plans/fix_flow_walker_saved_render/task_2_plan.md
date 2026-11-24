### Task 2 — Write the printed reads on `start` and `next`, and return them unchanged on `current`

**Goal:** Make the host's three entry points carry the printed reads.
- `record_outcome` and `start_walk` read them for the step they return and keep them in `PrintedReadsStore`, under the locks they already take.
- `current_step` returns the kept record rather than reading disk again.

A `current` then sees what `start` or `next` saw, as bash's `current` re-prints `out=` (`cli/templates/scripts/flow-walker.sh` → the `current)` arm, `load_state`).

**Depends on:** Task 1, which adds `devscene-flow-host/src/devscene_flow_host/host/printed_reads.py` with this exact contract:
- `PrintedReads`, a frozen dataclass: `review_iterations: tuple[tuple[str, int], ...] = ()`, `round_counts: tuple[tuple[str, int], ...] = ()`, `index_evidence: IndexEvidence | None = None`.
- `read_printed(graph: FlowGraph, repo_root: Path, state_dir: str, branch: str, action: Step) -> PrintedReads`, which returns `PrintedReads()` for every action other than a `Dispatch`, a `DispatchSet` or a cap `Stop`.
- `PrintedReadsStore(repo_root, state_dir, branch)` with `read() -> PrintedReads | None`, `None` only when the file is absent, and `write(reads) -> None`.

This task calls those three names and changes nothing in that module.

**Where this task stops.** `render` still reads disk after this task. Switching it to `HostStep.printed` is **Task 3's**, and Task 3 relies on the field this task adds.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py`
- `devscene-flow-host/src/devscene_flow_host/host/re_entry.py`
- `devscene-flow-host/tests/test_round_gates.py`
- `devscene-flow-host/tests/test_re_entry.py`

**Work:**

- [ ] **`round_gates.py` — `HostStep`.** Add a fourth field, `printed: PrintedReads = PrintedReads()`, after `revision_findings`. Extend the class docstring: `printed` holds the values the step read from disk when `start` or `next` returned it, as kept in `PrintedReadsStore`, and it is `PrintedReads()` on a `Refused` action. The default keeps every existing `HostStep(...)` construction and comparison valid.
- [ ] **`round_gates.py` — `record_outcome`.** Inside the existing `with store.lock():`, after the `Refused` early return and the kept-findings write/clear:
  - compute `printed = read_printed(graph, repo_root, state_dir, branch, result.action)`, or `PrintedReads()` when `result.action` is a `RefusedWait` (not a `graphscene` `Step`);
  - write it with `PrintedReadsStore(repo_root, state_dir, branch).write(printed)`;
  - return `dataclasses.replace(result, revision_findings=kept.read(), printed=printed)`.

  The early `Refused` return before the lock (a `fail` verdict with no findings) and the `Refused` return inside it write nothing. In the module docstring's rule, add that the printed reads are written with the refusal and kept-findings records, under the same lock and only when the action is not `Refused`.
- [ ] **`re_entry.py`.**
  - **`start_walk`:** inside its lock, in the same `if not isinstance(step, Refused):` branch that clears the two records, compute `read_printed(walker.graph, repo_root, state_dir, branch, step)`, write it, and return `HostStep(step, printed=printed)`. A refused start writes nothing.
  - **`current_step`:** after building the (filtered) step, read `PrintedReadsStore(repo_root, state_dir, branch).read()`. Only when that is `None`, meaning no `start` or `next` of this version has stepped the walk, use `read_printed(walker.graph, repo_root, state_dir, branch, step)`, which is what #465's `current` printed. Pass the result as `printed=`. `current_step` still takes no lock and writes nothing.
  - **The module docstring's rule:** `start_walk` writes the printed reads on a started walk; `current_step` returns them as kept, and reads disk only when no record exists.
- [ ] **`test_round_gates.py`.** Add cases, each expected value a literal:
  - Reaching `ui_review` through `record_outcome`, using the suite's existing `_at_ui_review`, gives `printed == PrintedReads(review_iterations=(("ui_review", 0),))`, and `PrintedReadsStore(...).read()` equals it.
  - A `Refused` result leaves the record byte-identical: `FAIL` at `ui_review` with no findings, which the suite already shows refused.
  - A `wait` result writes `PrintedReads()`.
- [ ] **`test_re_entry.py`.** Add cases:
  - `start_walk` writes the record, and a refused start leaves it unchanged, following the suite's `test_start_removes_the_kept_findings_file_and_a_refused_start_keeps_it`.
  - `current_step` returns the kept record unchanged after a `review_<n>.md` is planted in the folder it was read from. Plant a record with `review_iterations=(("ui_review", 0),)` and a walk at `ui_review`, add `review_0.md`, and `current_step(...).printed` is still `(("ui_review", 0),)`.
  - With no record file, `current_step` reads the folder: `(("ui_review", 1),)` after `review_0.md` is planted.

**Verification:**

- `tests/test_round_gates.py` and `tests/test_re_entry.py` pass, each run as `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py` from the repository root, the existing cases included: their `HostStep` comparisons over round sets and writer dispatches still hold because `printed` defaults to `PrintedReads()`.
- `current_step` contains no `lock()` call and no `write(`.
- Every `PrintedReadsStore.write` call sits inside a `with store.lock():` block.
