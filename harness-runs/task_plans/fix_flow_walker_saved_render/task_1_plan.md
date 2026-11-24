### Task 1 — Add the host's printed-reads record, `read_printed` and `PrintedReadsStore`

**Goal:** Give the `host` layer one place that reads, for a step about to be printed, every value `render` takes from disk today, and a per-branch record that keeps those values beside the walk. A later `current` can then print what the step printed, as `flow-walker.sh` re-prints its saved `out=` bytes (`cli/templates/scripts/flow-walker.sh` → `load_state`, `save_state`).

**Where this task stops.** This task adds a new module and its suite and changes no existing file. `record_outcome`, `start_walk` and `current_step` do not call it yet: wiring them, and adding the `HostStep.printed` field, is **Task 2's**. `render` keeps reading disk until **Task 3** switches it to `HostStep.printed`. Until then the same three reads exist in two places, and Task 3 removes the copy in `render`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/printed_reads.py` (new)
- `devscene-flow-host/tests/test_printed_reads.py` (new)

**Work:**

- [ ] **`printed_reads.py` — the value.** Add a frozen dataclass `PrintedReads` with exactly three fields, all defaulting to empty, so `PrintedReads()` means "this step read nothing":
  - `review_iterations: tuple[tuple[str, int], ...] = ()` — `(node, index)` per non-round reviewer dispatch, in dispatch order;
  - `round_counts: tuple[tuple[str, int], ...] = ()` — `(node, FAIL count)` per `Stop.round_counts` entry, in that order;
  - `index_evidence: IndexEvidence | None = None` — `devscene_flow_host.records.index_evidence.IndexEvidence`, imported from its defining module.
- [ ] **`printed_reads.py` — the read.** Add `read_printed(graph: FlowGraph, repo_root: Path, state_dir: str, branch: str, action: Step) -> PrintedReads`. `Step` is `graphscene`'s public type, as `host/round_gates.py` imports it. Do not import `RefusedWait` or anything else from `host/round_gates.py`, which will import this module in Task 2. It does exactly the reads `commands/render.py` does today, moved rather than re-derived:
  - **`Dispatch`** — `host/reviewers.py` → `review_iteration(graph, repo_root, state_dir, branch, node)`, kept only when not `None`.
  - **`DispatchSet`** — the same read for each of its `dispatches`, in order.
  - **`Stop` whose `reason == "cap"`** — for each name in `stop.round_counts`, `records/round_files.py` → `fail_count` over `repo_root / render_path(node.findings_folder, state_dir, branch)`. A name whose node is not a `DispatchNode` with a `findings_folder` raises `ValueError(f"graph has no 'nodes.{counted}.findingsFolder'")`, the text `render._cap_lines` raises today. When `stop.evidence` is not `None`: `graph.paths.get(stop.evidence)`, or `ValueError(f"graph has no 'paths.{stop.evidence}'")`, then `records/index_evidence.py` → `read_index_evidence(repo_root / render_path(template, state_dir, branch))`.
  - **Any other action** — `PrintedReads()`.
- [ ] **`printed_reads.py` — the store.**
  - **Directory and path.** `PRINTED_READS_DIRECTORY: Final = "printed_reads"`. `printed_reads_path(repo_root, state_dir, branch)` gives `repo_root / state_dir / STATE_DIRECTORY / PRINTED_READS_DIRECTORY / (quote(branch, safe="") + ".json")`, with `STATE_DIRECTORY` imported from `host/store.py`, and raises `ValueError("a walk's branch is empty")` for an empty branch. This is the shape of `host/revision_findings.py` → `revision_findings_path`.
  - **`PrintedReadsStore(repo_root, state_dir, branch)`.** `read() -> PrintedReads | None` returns `None` only when the file is absent. `write(reads: PrintedReads) -> None` writes the file whole, through a temporary file in the same directory and `os.replace`, as `RevisionFindingsStore.write` does. There is no `clear`.
  - **The document.** `{"version": 1, "review_iterations": [[node, n], …], "round_counts": [[node, n], …], "index_evidence": null | {"rejected_findings": bool, "open_rejections": [str, …], "scope_register": bool}}`.
  - **Decoding.** Strict, raising `ValueError(f"{path}: {cause}")` with these causes:
    - `not valid JSON`
    - `the document is not an object`
    - `the document has no <key>`
    - `the document has an unexpected key <json-dumped key>`
    - `version <json> is not 1`
    - `<field> is not a list`
    - `<field>[<i>] is not a [node, count] pair` — the node a `str`, the count an `int` that is not a `bool` and is `>= 0`
    - `index_evidence is not an object or null`
    - `index_evidence has no <key>`
    - `index_evidence has an unexpected key <json-dumped key>`
    - `index_evidence.<key> is not a boolean`
    - `index_evidence.open_rejections is not a list of strings`
- [ ] **`printed_reads.py` — the docstring.**
  - **The rule:** what the record plays the part of. That is the part of bash's `out=` lines that `render_block` (`fw_next_review_index`) and `take_binding` (`fw_fail_count`, `fw_index_evidence`) read from disk at print time.
  - **The lock:** every write happens while the caller holds `RefusalStore`'s lock, and this module takes no lock. `read` takes none, because `write` replaces the file whole.
  - **Confinement:** the store writes only its file and its temporary files inside `printed_reads/`.
  - **Deliberately not covered:** when the record is written or read, which is the caller's; rendering, which is the `commands` layer's; removing a finished branch's file; a crash between the walk's write and this one, which leaves the previous step's reads.
- [ ] **`test_printed_reads.py`.** Open the module docstring with *"The rule this file exists to enforce"* (`.claude/context/conventions.md` → `## The testing bar`). Use the read-only graph `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, as `tests/test_render.py` → `_GRAPH` does, and plant folders with `round_fixtures.plant_review`. Write every expected value as a literal. Cases:
  - **An autouse fixture**, modelled on `tests/test_revision_findings.py` → `_only_revision_files`, asserting that every file the store writes is inside `state/.flow_walker_state/printed_reads/`.
  - **Path:** a `/` in the branch is percent-encoded; an empty branch is refused with `a walk's branch is empty`.
  - **Absent file:** reads as `None`.
  - **Round trip:** a write of a non-empty `PrintedReads` reads back equal.
  - **The written document:** equals a literal JSON object.
  - **Malformed documents:** one parametrized case per decoding cause above, asserting the exact `<path>: <cause>` message.
  - **`read_printed` on `ui_review`:** a `ui_review` `Dispatch` over a folder planted with `review_0.md` gives `PrintedReads(review_iterations=(("ui_review", 1),))`.
  - **`read_printed` on round gates:** the three-gate `plan_round` `DispatchSet` gives `PrintedReads()`.
  - **`read_printed` on the plan-round cap:** reuse the planted shape of `tests/test_render.py` → `test_the_plan_round_cap_carries_files_counts_evidence_and_summary`. It gives `round_counts=(("business_parity_review", 0), ("architecture_review", 5), ("plan_review", 1))` and the `IndexEvidence(True, ("- **5** (rejected round 2) — r",), True)` of `flow-walker-gates.sh` → REPRO's `i.md`.
  - **`read_printed` on a non-cap `Stop`:** a `Stop` with `reason="error"` gives `PrintedReads()`.

**Verification:**

- `tests/test_printed_reads.py` passes, run as `bash scripts/python-service.sh --package devscene-flow-host test tests/test_printed_reads.py` from the repository root.
- `printed_reads.py` imports only the standard library, `graphscene`'s public surface, and `devscene_flow_host.host.{paths,reviewers,store}` and `devscene_flow_host.records.{index_evidence,round_files}` by their defining modules. It imports nothing from `host/round_gates.py` or `host/re_entry.py`.
- No existing file is changed by this task.
