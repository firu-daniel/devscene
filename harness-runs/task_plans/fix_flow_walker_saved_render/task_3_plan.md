### Task 3 — Render from `HostStep.printed`, remove the three `TODO` markers, pin the repeated heading

**Goal:** Make `render` print a non-round reviewer's `arg.iteration` and a cap's `rounds:` / `evidence:` / `evidence.open:` lines from `HostStep.printed`, reading no file for them, and remove the three `TODO: @claude` markers #465 left in `devscene-flow-host/src/devscene_flow_host/commands/render.py`. Two markers are in `_cap_lines` and one in `_block`. Also pin, with literals written from bash, that a story index repeating `## Rejected findings` already prints as `flow-walker.sh` prints it.

**Depends on:** Task 2, which adds to `devscene_flow_host.host.round_gates.HostStep` the field `printed: PrintedReads = PrintedReads()`, filled by `start_walk`, `record_outcome` and `current_step`. `PrintedReads` is Task 1's, imported from `devscene_flow_host.host.printed_reads`:
- `review_iterations: tuple[tuple[str, int], ...]` — `(node, index)` per non-round reviewer dispatch;
- `round_counts: tuple[tuple[str, int], ...]` — `(node, FAIL count)` in `Stop.round_counts` order;
- `index_evidence: IndexEvidence | None` — `None` when the index was absent.

This task only reads that field.

**The third marker needs no change to the evidence order.** `cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_index_evidence` prints `evidence: <index> ## Rejected findings` only `if (!rj)`, once, at the first such heading. It prints `evidence.open: <line>` for every open `- ` line under any `## Rejected findings` heading, in file order, and `evidence: <index> ## Scope register` at `END`. `read_index_evidence` collects open entries in file order across every such heading, and `_cap_lines` prints one `evidence:` line, then every `evidence.open:` line, then the scope line. That is the same output, so the marker is removed and the case pinned, not "fixed".

### Targets

- `devscene-flow-host/src/devscene_flow_host/commands/render.py`
- `devscene-flow-host/tests/test_render.py`
- `devscene-flow-host/src/devscene_flow_host/records/index_evidence.py` (docstring only)
- `devscene-flow-host/tests/test_index_evidence.py`

**Work:**

- [ ] **`render.py`.**
  - **`_block`:** replace the `review_iteration(...)` call and its `TODO` with a lookup of `dispatch.node` in `dict(step.printed.review_iterations)`. Print `arg.iteration: <n>` when present and nothing when absent, as today's `if index is not None`.
  - **`_cap_lines`:** remove both `TODO`s. For each `counted` in `stop.round_counts`, print `rounds: {counted} {n}` from `dict(step.printed.round_counts)`. A name with no count raises `ValueError(f"the printed reads carry no count for '{counted}'")`, never a guessed `0`.
  - **Evidence:** keep the `graph.paths` lookup and its `ValueError` and the `index = f"{repo_root}/{rendered}"` string, and print from `step.printed.index_evidence` in today's order.
  - **Imports:** drop the now-unused `review_iteration`, `fail_count` and `read_index_evidence`, and `DispatchNode`/`render_path` only where nothing still uses them.
  - **Docstring:** the rule states that the values a step read from disk are `HostStep.printed`, read by the host when the step was first printed, so a `current` prints what `start` or `next` printed and `render` reads no file. Remove the *"Re-reading what bash re-prints from saved bytes"* bullet from **Deliberately not covered**.
- [ ] **`test_render.py`.** Rework the two cases that plant files so they build `HostStep(..., printed=PrintedReads(...))` instead and plant nothing. Their expected texts stay as they are:
  - `test_a_non_round_reviewer_gets_its_folders_next_free_index` becomes a case printing `arg.iteration: 1` from `review_iterations=(("ui_review", 1),)`;
  - `test_the_plan_round_cap_carries_files_counts_evidence_and_summary`.

  Add these cases, each expected text a literal:
  - **A folder that disagrees.** A folder planted with `review_0.md`–`review_2.md` beside `printed` saying `1` still prints `arg.iteration: 1`, which shows that `render` does not read the folder.
  - **A missing count.** A cap `Stop` whose `round_counts` names a gate missing from `printed.round_counts` raises `ValueError` with `the printed reads carry no count for 'architecture_review'`.
  - **A repeated heading.** A cap `Stop` with `evidence="story_index"` and `IndexEvidence(True, ("- **5** (rejected round 2) — r", "- **7** (rejected round 3) — r"), True)` prints, after `reason: cap`:
    - `evidence: <index> ## Rejected findings`
    - `evidence.open: - **5** (rejected round 2) — r`
    - `evidence.open: - **7** (rejected round 3) — r`
    - `evidence: <index> ## Scope register`

    The case comment cites `fw_index_evidence`'s `if (!rj)`.
- [ ] **`index_evidence.py`.** Add one sentence to the docstring's rule: a repeated `## Rejected findings` heading adds no entry of its own, and its open entries join the rest in file order, as `fw_index_evidence` prints one `evidence:` line for any number of such headings. The code does not change.
- [ ] **`test_index_evidence.py`.** Add a case reading this index:

  ```
  ## Rejected findings
  - **5** (rejected round 2) — r
  ## Scope register
  ## Rejected findings
  - **7** (rejected round 3) — r
  - **3** (rejected round 1; rebutted round 2 — call stands) — r
  ```

  It gives the literal `IndexEvidence(True, ("- **5** (rejected round 2) — r", "- **7** (rejected round 3) — r"), True)`.

**Verification:**

- `tests/test_render.py` and `tests/test_index_evidence.py` pass, each run as `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py` from the repository root.
- `grep -n "TODO" devscene-flow-host/src/devscene_flow_host/commands/render.py` prints nothing.
- `render.py` imports none of `review_iteration`, `fail_count` or `read_index_evidence`.
