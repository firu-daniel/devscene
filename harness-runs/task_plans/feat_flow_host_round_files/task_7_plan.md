### Task 7 — Record a gate's outcome under the reviewer-file rules

**Goal:** Add `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` with `record_outcome`, the host's `next`. It applies the reviewer-file rules around GraphScene's `Walker.next`:

- `FAIL` requires a findings file, and so do `PASS` and `FAIL` at a round gate.
- A round gate's file must pass the round-file check before its verdict is recorded.
- A refused file records nothing and its gate is re-dispatched in the same round.
- The third refusal holds the gate as `error`.

It returns `HostStep`, the shape Task 8 and the compatibility command consume.

**Depends on:**
- Task 1: `devscene_flow_host.records.round_files.round_file_path(repo_root: Path, findings: str) -> Path` and `round_file_problem(path: Path) -> str | None`.
- Task 4: `devscene_flow_host.host.reviewers.round_of_gate(graph, node) -> RoundNode | None`.
- Task 5: `devscene_flow_host.host.refusals`:
  - `ROUND_FILE_ATTEMPTS` (3);
  - `Refusal(gate, attempt, reason)`;
  - `GateRefusals(attempts, reason, redo)`;
  - `RoundRefusals(round, number, gates, announced)` with `empty(...)` and `refusal(gate)`;
  - `RefusalStore(repo_root, state_dir, branch)` with `read(round, number)`, `read_announced()`, `write(...)`, `clear()` and `lock()`. Its lock is taken **outside** the walk's lock.

**Source:** `cli/templates/scripts/flow-walker.sh`:
- `next`'s *"outcome FAIL requires --findings"* check;
- `record_in_set`, `refuse_round_file`, `close_round`'s clearing of `round.refused.*`;
- the `A REFUSED ROUND FILE` paragraph.

**Where this layer stops.** `record_outcome` returns values and renders nothing. Two things belong to Task 8 (`devscene_flow_host/host/re_entry.py`): `start_walk`, and `current_step`, which filters refused gates out of a re-read. `record_outcome` never calls `Walker.start` and never clears the record on a `start`.

**A second departure, deferred with a marker.** `flow-walker.sh` → `next` keeps a findings file given outside a round gate: its `dispatch)` arm runs `elif [ -n "$A_FINDINGS" ]; then st_set revision_findings "$A_FINDINGS"`, its `answer)` arm runs `[ -z "$A_FINDINGS" ] || st_set revision_findings "$A_FINDINGS"`, and `render_block` prints it as `arg.findings_file:` on the writer's revision (in the v4 graph, `ui_review` → `FAIL` → `ui_writer`, `"prompt": "revision"`). GraphScene refuses a `detail` outside a round, so this task sends a non-gate call to `walker.next(outcome, node, None)`. A non-round `FAIL`'s findings file is still required (rule 1), but it is not kept, and neither is one given with `answered`. This divergence is backed by the second entry-point marker in the Work list. It is not excluded by the task prompt: #465 takes the command and its rendering, not the host's record of the file.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py` (new)
- `devscene-flow-host/tests/test_round_gates.py` (new)

**Work:**

- [ ] **The answer types.** Task 8 consumes these exactly as named:
  - `RefusedWait(round: str, refusal: Refusal, pending: tuple[str, ...])` is bash's `wait` whose `refused:` line stands where `recorded:` would.
  - `HostStep(action: Step | RefusedWait, refusals: tuple[Refusal, ...] = ())`. `refusals` holds the `refused:` lines the action carries: one per gate of a re-dispatched set, or one per gate whose attempts reached `ROUND_FILE_ATTEMPTS` at an escalating join.

  Constant: `REFUSAL_HELD_OUTCOME: Final = "error"`.
- [ ] **`record_outcome(walker: Walker, repo_root: Path, branch: str, outcome: str, *, node: str | None = None, findings: str | None = None) -> HostStep`, in this order:**
  1. When the graph's vocabulary declares `outcome` with `verdict == "fail"` and `findings` is empty, return `HostStep(Refused(f"outcome {outcome} requires --findings with the reviewer's findings_file"))`.
  2. Read `stateDir` with `read_config(repo_root)` and take the `RefusalStore` lock.
  3. Read the saved walk with `walker.store.read()`. The **gate path** applies only when all of these hold:
     - the walk's flow is `walker.graph.flow`;
     - `awaiting == "set"`;
     - `node` is due in `open_round` and has no record there;
     - `node` declares `outcome`;
     - the outcome's declaration carries a verdict.

     Every other call goes straight to `walker.next(outcome, node, None)`, so GraphScene's own refusal texts stand. That non-gate branch is where the second departure marker goes (below).
  4. On the gate path, empty `findings` returns `Refused(f"outcome {outcome} at round gate '{node}' requires --findings with the reviewer's findings_file")`. Otherwise `round_file_problem(round_file_path(repo_root, findings))`:
     - `None` → `walker.next(outcome, node, findings)`.
     - A reason → `attempts + 1` with that reason. At `ROUND_FILE_ATTEMPTS`, clear the mark and call `walker.next(REFUSAL_HELD_OUTCOME, node, None)`. Below it, set `redo` and call nothing.
- [ ] **Turning the result into a `HostStep`; the record is written only when the action is not `Refused`.**
  - A refusal below the cap → `RefusedWait(round, refusal, out)`, where `out` is the due, unrecorded, unmarked gates in `gates` order.
  - A GraphScene `Wait` → the same `Wait` with marked gates removed from `pending`. When a refusal led to it, a `RefusedWait` carrying the third attempt's `Refusal` takes its place.
  - Either answer with nothing left out → **re-dispatch**: `walker.current()`'s `DispatchSet` cut to the marked gates, with their refusals in `gates` order. Their marks are then cleared and `announced` set to those refusals.
  - Every other answer → the join. Spent gates' refusals ride on `refusals` and `announced`. With none spent, the record is cleared.
  - A recorded gate's own mark is cleared. `announced` is reset on every written answer but a re-dispatch or a spent join.
  - Outside a set, a written answer clears the record.
- [ ] **The two departure markers and the docstring.** Write each as a Python comment at its entry point.
  - At the re-dispatch branch:

    `# TODO: @claude add a follow up task for this: escalate a held gate at a join whose only gates out are refused ones, as flow-walker.sh → record_in_set does ("With none out: a held gate escalates") — needs a GraphScene way for a host to set a due gate aside in an open round`
  - At the non-gate branch of `record_outcome`, the `walker.next(outcome, node, None)` call:

    `# TODO: @claude add a follow up task for this: keep a findings file given outside a round gate (a non-round reviewer's FAIL, or answered) as flow-walker.sh → next keeps revision_findings, so the writer's revision dispatch carries it as arg.findings_file — needs a host-side record of revision_findings for a non-round reviewer and for answered, cleared as bash clears it on start`

  - **Deviations from plan:** Each marker's text is kept verbatim but wrapped over consecutive `#` lines at 100 columns, because `ruff`'s `E` rules (`devscene-flow-host/pyproject.toml` → `[tool.ruff]`, `line-length = 100`) flag the single-line form; the opening `# TODO: @claude add a follow up task for this:` stays on the first line.

  The docstring:
  - **"The rule:"** states the four rules and the lock order.
  - **"Deliberately not covered"** names three things: the held-gate departure (the host re-dispatches first), with its marker; the non-round findings departure (a findings file given at a non-gate call is required but not kept, and neither is one given with `answered`), with its marker; and rendering.
- [ ] **`tests/test_round_gates.py`.** It opens with *"The rule this file exists to enforce"* and names the two departures it pins. It uses `open_walker` on the v4 graph with config and ledger under `tmp_path`, plus `round_fixtures` (`plant_review`, `PASS_BODY`, `FAIL_BODY`), and starts with `walker.start()` then `returned`. Cases, with literal expectations written from `flow-walker.sh` → `A REFUSED ROUND FILE` and its `REPRO` block's refused-file walk:
  - FAIL without findings;
  - PASS at a round gate without findings;
  - a valid file recorded as a `Wait`;
  - a refused file waiting for its siblings, then dispatched alone;
  - two refused gates returning as one set;
  - three refusals escalating with `refused: … attempt 3 of 3` on `refusals`;
  - a PASS file carrying a Must Fix entry refused;
  - a held `error` plus a refused gate re-dispatching first;
  - two threads recording two gates at once, with exactly one join;
  - the non-round findings departure as it stands: walking to `ui_review` and calling `record_outcome(walker, tmp_path, "feat_x", "FAIL", node="ui_review", findings=<a planted file>)` returns `ui_writer`'s revision dispatch with no findings file on it, and the saved walk holds no record of the file. The case's docstring names the second marker.

**Verification:**

- `tests/test_round_gates.py` passes. Every `Refusal` reason, `RefusedWait.pending` and `Refused` text is asserted as a literal.
- After a refusal below the cap, the saved walk is byte-identical to the one before the call: a refusal never reaches GraphScene's state.
- After a round closes on PASS or FAIL, the refusal file is gone.
