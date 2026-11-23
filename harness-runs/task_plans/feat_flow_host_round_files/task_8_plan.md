### Task 8 — Start a walk from the round files and re-read it without its refused gates

**Goal:** Add `devscene-flow-host/src/devscene_flow_host/host/re_entry.py` with the two calls a re-entry makes (task prompt, *"A lost state file is the case this branch makes work"*):

- `start_walk` rebuilds the round position from the files on disk through GraphScene's generic entry, `Walker.start(entry, resume=RoundResume)`, and clears the refusal record, as bash's `start` overwrites its state.
- `current_step` re-reads the saved walk with every refused gate left out and the last step's `refused:` lines restored, as bash's `current` re-prints its saved `out=`.

**Depends on:**
- Task 1, for the tests only: `devscene-flow-host/tests/round_fixtures.py`, imported and never edited. The cases use:
  - `init_repo(root: Path) -> None`;
  - `commit(root: Path, paths: Sequence[Path], message: str) -> None`;
  - `plant_review(folder: Path, n: int, body: str) -> Path`, which creates the folder and writes `review_<n>.md`;
  - `PASS_BODY` (`"verdict: PASS\n"`) and `FAIL_BODY` (a `verdict: FAIL` file with one Must Fix entry carrying `**Class:**` and `**Failure:**`, which passes the round-file check).
- Task 5: `devscene_flow_host.host.refusals.RefusalStore(repo_root, state_dir, branch)`, with `read(round, number) -> RoundRefusals`, `read_announced() -> tuple[Refusal, ...]`, `clear()` and `lock()`. `RoundRefusals.gates` maps a gate to `GateRefusals(attempts, reason, redo)`. `Refusal(gate, attempt, reason)`.
- Task 6: `devscene_flow_host.host.resume.round_resume(graph, host, repo_root, state_dir, branch, entry=None) -> RoundResume | None`.
- Task 7: `devscene_flow_host.host.round_gates`:
  - `HostStep(action: Step | RefusedWait, refusals: tuple[Refusal, ...] = ())`;
  - `RefusedWait(round: str, refusal: Refusal, pending: tuple[str, ...])`, the answer to a refused round file below the cap, where `pending` holds the due, unrecorded, unrefused gates in `gates` order;
  - `record_outcome(walker: Walker, repo_root: Path, branch: str, outcome: str, *, node: str | None = None, findings: str | None = None) -> HostStep`. The refusal cases call it to record a gate's outcome with its findings file: a file that fails the round-file check (for example a `verdict: FAIL` body with no numbered entry) returns a `HostStep` whose action is a `RefusedWait` while a sibling gate is still out, and a re-dispatch `DispatchSet` of the refused gates, with their `Refusal`s on `refusals`, once none is.

**Source:** `cli/templates/scripts/flow-walker.sh` (the `start` sub-command, `current`, and `render_set`'s skipping of a gate with `round.redo.<gate>`).

**Where this layer stops.** `host/walking.py` → `open_walker` still composes the `Walker` and gains no resume parameter. These functions take the composed walker. This task does not choose an entry: the orchestrator picks it from the ledger. It reads no round file itself, because Task 6's `round_resume` does that.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/re_entry.py` (new)
- `devscene-flow-host/tests/test_re_entry.py` (new)

**Work:**

- [ ] **`start_walk(walker: Walker, repo_root: Path, branch: str, entry: str | None = None) -> HostStep`.** In order:
  1. Read `stateDir` with `read_config(repo_root)`.
  2. Under `RefusalStore.lock()`, compute `resume = round_resume(walker.graph, walker.host, repo_root, state_dir, branch, entry)`.
  3. Call `walker.start(entry, resume=resume)`.
  4. Unless the step is `Refused`, call `clear()`.
  5. Return `HostStep(step)`.

  A `RecordError` and the `ValueError` for a gate with no `findingsFolder` propagate.
- [ ] **`current_step(walker: Walker, repo_root: Path, branch: str) -> HostStep`.** It takes no lock. A `Refused` from `walker.current()` is returned as is. A pending `DispatchSet` has its dispatches for gates whose `read(set.round, set.number)` entry has `redo` removed. Every action carries `refusals=read_announced()`.
- [ ] **The module docstring.**
  - **"The rule:"** says that `start` is the only call that clears the refusal record, that `current` changes nothing, and that a refused gate is never dispatched twice.
  - **"Deliberately not covered"**: the loop counter and prompt variants a lost walk loses; choosing the entry.
- [ ] **`tests/test_re_entry.py`.** It opens with *"The rule this file exists to enforce"*. It loads the v4 graph, `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, from a path built off `__file__`, and plants config, ledger, review files and git history under `tmp_path` through `round_fixtures` (`init_repo`, `commit`, `plant_review`, `PASS_BODY`, `FAIL_BODY`). Its cases carry the `STATE` paragraph's resume rules in `flow-walker.sh` over to the host, with literal expectations:
  - no round file → round 0's whole set;
  - the saved walk's file deleted with two of three round-3 files committed → only the third gate, at round 3 and counter 0;
  - a no-verdict file or a newer plan commit → the whole set at round 3;
  - all PASS → reviewed again; a FAIL with `task_plan_revision_4.md` → round 4's set;
  - a held `error` with two verdicts committed → only the errored gate.
- [ ] **`tests/test_re_entry.py`, the refusal cases.** Using `record_outcome` from `round_gates` with the signature restated under **Depends on**, and files planted with `plant_review`:
  - `current_step` during a refusal wait, after `record_outcome` returned a `HostStep` whose action is a `RefusedWait(round, refusal, pending)`, leaves the refused gate out;
  - after the re-dispatch it carries the `refused:` refusal;
  - `start_walk` removes the refusal file.

**Verification:**

- `tests/test_re_entry.py` passes, with each expected set's gate list and round number written from the `STATE` paragraph's rules, never from the walker's output.
- After a lost-walk `start_walk`, the counter is 0 while the round number carries on from the files.

**Deviations from plan:** Step 2 put only `round_resume` under `RefusalStore.lock()`; `start_walk` holds that lock through steps 2–4 (`walker.start` and `clear()`), so a concurrent `record_outcome` cannot write a refusal between the start and the clear — the same lock order `record_outcome` uses (refusal lock before the walk's). The refusal cases also assert that a `Refused` start (entry `plan_review`, not an entry of the flow) keeps the refusal file, the step-4 clause.
