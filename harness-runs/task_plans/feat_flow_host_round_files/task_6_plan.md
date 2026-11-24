### Task 6 — Build a round's `RoundResume` from the files on disk

**Goal:** Add `devscene-flow-host/src/devscene_flow_host/host/resume.py`, which turns a round's evidence into the `RoundResume` that GraphScene's `Walker.start(entry, resume=…)` takes. It follows the rules of `flow-walker.sh`'s `STATE` paragraph and `start_round`:

- no round file opens round 0's whole set;
- a round with files missing, whose evidence is consistent, records the present gates and opens only the missing ones;
- any other incomplete round opens the whole set at that round;
- a complete round that is unreadable or has no FAIL is reviewed again;
- a FAIL with the next revision note on disk opens the next round;
- a FAIL without the note records every verdict, so the round closes at once.

Convergence is never inferred from files.

**Depends on:**
- Task 2, which provides `devscene_flow_host.records.round_evidence`:
  - `read_round_evidence(repo_root: Path, note_template: str | None, plan_paths: Sequence[Path], gates: Sequence[tuple[str, Path]]) -> RoundEvidence`;
  - `RoundEvidence(round: int | None, gates: tuple[GateEvidence, ...], note_present: bool, plan: Literal["not-newer", "newer", "unknown"])`;
  - `GateEvidence(gate, status: Literal["PASS", "FAIL", "missing", "unreadable"], file: Path)`;
  - and `RecordError(f"git cannot answer in {repo_root}")`.
- Task 4, which provides `devscene_flow_host.host.paths.render_path(template, state_dir, branch, round_number=None) -> str` and `devscene_flow_host.host.reviewers.round_of_writer(graph, node) -> RoundNode | None`.

**Source:** `cli/templates/scripts/flow-walker.sh` (`start_round`, `start_record`, and the `STATE` paragraph from *"`round.number` is never the counter"* to *"convergence is never inferred from files"*).

**Where this layer stops.** `round_resume` returns a value and calls no walker. Task 8's `start_walk` passes it to `Walker.start` and clears the refusal record. The counter, the prompt variants and the refusal count are not rebuilt; that loss is accepted (`docs/flow-graph-walker.md` → *What `start` reads, and what it never carries*). Nothing about which **entry** to pick is decided here: the orchestrator picks it from the ledger.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/resume.py` (new)
- `devscene-flow-host/tests/test_resume.py` (new)

**Work:**

- [ ] **The entry's role.** `round_resume(graph: FlowGraph, host: PredicateHost, repo_root: Path, state_dir: str, branch: str, entry: str | None = None) -> RoundResume | None` takes `e = entry or graph.start`.
  - When `round_of_writer(graph, e)` is a round `rn`, the role is **writer**.
  - Otherwise, when `graph.nodes[e]` is a `RoundNode`, the role is **set** with `rn` that node.
  - Otherwise, return `None`, and the walk's round numbers stay 0.
- [ ] **The evidence arguments, as `start_round` builds them.**
  - `note_template`: `str(repo_root / render_path(graph.paths[rn.revision_note], state_dir, branch))`, leaving `{round}` in place, or `None` when `rn.revision_note` is `None`.
  - `plan_paths`: `repo_root / render_path(graph.paths[p], …)` for each `p` in `rn.plan or ()`.
  - The gates, in `rn.gates` order. Each gate's folder is `repo_root / render_path(node.findings_folder, …).rstrip("/")`. A gate whose node has no `findings_folder` raises `ValueError(f"round gate '{g}' declares no findingsFolder")`.
  - With the **set** role only, a gate the walk skips on this arrival is left out. Ask `host.answer(entry.when, g)` over the gate's `skip` entries in order: the first `True` leaves the gate out; a `None` stops asking and keeps the gate in, and `Walker.start` then refuses that predicate itself; `False` asks the next.
  - A `RecordError` from the reader is re-raised as `RecordError(f"cannot read the round evidence of '{rn.id}': {error}")`, the text `flow-walker.sh` faults with.
- [ ] **The mapping.**
  - `round` `None` → `None`.
  - **writer** → `RoundResume(rn.id, R + 1)`.
  - **set** with any `missing` gate:
    - with no `unreadable` gate and `plan == "not-newer"` → `RoundResume(rn.id, R, records)`;
    - otherwise → `RoundResume(rn.id, R)`.
  - **set** with no gate missing:
    - any `unreadable`, or no `FAIL` → `RoundResume(rn.id, R)`;
    - otherwise, `note_present` → `RoundResume(rn.id, R + 1)`;
    - otherwise → `RoundResume(rn.id, R, records)`.
  - `records` is one `GateRecord(gate, status, file.relative_to(repo_root).as_posix())` per PASS or FAIL gate, in gate order, as `start_record` stores `round.findings.<gate>` repo-relative.
  - Import `FlowGraph`, `RoundNode`, `DispatchNode`, `RoundResume`, `GateRecord` and `PredicateHost` from `graphscene`.
- [ ] **The module docstring.** **"The rule:"** quotes the six resume rules above and names `start_round`. **"Deliberately not covered"**: the counter, the prompt variants and the refusal count, which a lost walk loses as in bash; picking the entry.
- [ ] **`tests/test_resume.py`.** It opens with *"The rule this file exists to enforce"*. It loads the harness's v4 graph file, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, from a path built off `__file__`, and plants config, review files and git history under `tmp_path` through `tests/round_fixtures.py` (`init_repo`, `commit`, `plant_review`, `PASS_BODY`, `FAIL_BODY`). The host is an in-test class answering a fixed table. One case per mapping row, each expectation a literal `RoundResume`:
  - no file → `None`;
  - writer entry after round 3 → `RoundResume("plan_round", 4)`;
  - two of three round-3 files committed, PASS and FAIL → number 3 with those two records (repo-relative `state/…/review_3.md`);
  - the same with a later commit to the story index → number 3, no records;
  - the same with one file unreadable → number 3, no records;
  - all PASS → number 3, no records;
  - FAIL with `task_plan_revision_4.md` present → number 4;
  - FAIL without it → number 3 with every record;
  - the parity gate skipped by `phase_parity_off` answering `True` → left out of the evidence;
  - the re-raised `RecordError` message for a root that is not a git repository.

**Verification:**

- `tests/test_resume.py` passes. Each mapping row of `start_round` has its own case with a literal `RoundResume`, never one computed by `round_resume`.
- With every round file PASS, `round_resume` never returns a resume that carries records, so convergence is never inferred.
  - **Deviations from plan:** `tests/test_resume.py` plants no `devscene.config.json`: `round_resume` reads no configuration (`state_dir` is a parameter, and skip predicates are answered by the in-test host table), so a planted config would be read by nothing.
