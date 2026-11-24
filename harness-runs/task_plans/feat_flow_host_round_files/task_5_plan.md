### Task 5 — Keep a round's reviewer-file refusals in the host's own file beside the walk

**Goal:** Give the refusal count a home. Add `devscene-flow-host/src/devscene_flow_host/host/refusals.py`, the host's own per-branch record of a round's reviewer-file refusals. It plays the part of the bash state's `round.refused.<gate>`, `round.refusal.<gate>` and `round.redo.<gate>` keys, plus the `refused:` lines the last printed step carried. The record lives in the walk's own directory under its own lock. (Story index `## Context`, **Decided here — where the refusal count lives.**)

**Source:** `cli/templates/scripts/flow-walker.sh` (`refuse_round_file`, `refused_line`, `refusals_spent`, `FW_ROUND_FILE_ATTEMPTS`, and the `STATE` paragraph's *"a refused round file's count, last reason and re-dispatch mark"*).

**Where this layer stops.** This module stores and reads. It never decides when a refusal is counted, when a gate is re-dispatched, or when a third refusal is held. Those decisions are Task 7's (`record_outcome`). It never clears itself on a `start`; that is Task 8's (`start_walk`). It never touches the walk's own file.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/refusals.py` (new)
- `devscene-flow-host/tests/test_refusals.py` (new)

**Work:**

- [ ] **Constants and values.** Constants: `ROUND_FILE_ATTEMPTS: Final = 3` and `REFUSALS_DIRECTORY: Final = "round_refusals"`. Frozen dataclasses, consumed by Tasks 7 and 8 exactly as named:
  - `Refusal(gate: str, attempt: int, reason: str)`: one `refused: <gate> attempt <n> of 3: <reason>` line's content.
  - `GateRefusals(attempts: int, reason: str, redo: bool)`.
  - `RoundRefusals(round: str, number: int, gates: Mapping[str, GateRefusals], announced: tuple[Refusal, ...])`. `gates` is a `MappingProxyType` over a fresh dict. `announced` holds the refusals the last step written carried.

  Add `RoundRefusals.empty(round: str, number: int) -> RoundRefusals` and `RoundRefusals.refusal(gate: str) -> Refusal`.
- [ ] **The path.** `refusals_path(repo_root: Path, state_dir: str, branch: str) -> Path` is `repo_root / state_dir / STATE_DIRECTORY / REFUSALS_DIRECTORY / (quote(branch, safe="") + ".json")`.
  - Import `STATE_DIRECTORY` from `devscene_flow_host.host.store` rather than retyping it.
  - Refuse an empty branch with the same `ValueError` text as `walk_state_path`: `"a walk's branch is empty"`.
  - The `round_refusals` directory cannot collide with a walk file: those all end in `.json`, `.json.lock` or start with `.`.
- [ ] **`RefusalStore(repo_root, state_dir, branch, *, lock_timeout: float = 120.0)`.**
  - `read(round: str, number: int) -> RoundRefusals` returns `RoundRefusals.empty(round, number)` when the file is absent, or when it records another round or number. In that second case it still carries the file's `announced`.
  - `read_announced() -> tuple[Refusal, ...]` returns `()` when the file is absent.
  - `write(refusals: RoundRefusals) -> None` writes `{"version": 1, "round", "number", "gates": {gate: {"attempts", "reason", "redo"}}, "announced": [{"gate", "attempt", "reason"}]}` through a temporary file in the same directory and `os.replace`, creating the directories.
  - `clear() -> None` removes the file if it exists.
  - `lock()` is a context manager. It takes `fcntl.flock` on `<file>.lock`, retrying every 0.1 s, and raises `TimeoutError(f"cannot lock {lock_path} within {lock_timeout} s")` when it runs out. It releases in a `finally`.
  - A document that is not this shape (another version, a missing or extra key, a wrong type) raises `ValueError(f"{path}: <reason>")`, as GraphScene's `FileStateStore` refuses a malformed state.
- [ ] **The module docstring.**
  - **"The rule:"** says three things. First, a count applies only to the round and number it was recorded for. Second, every caller that records a gate takes `lock()` **before** the walk's own lock and never inside it, which is why the two locks cannot deadlock. Third, the file is position, never a record: a lost or stale file costs at most two extra re-dispatches.
  - **"Deliberately not covered"**: a crash between this write and the walk's write, which leaves the count one step behind; removing a finished branch's file.
- [ ] **`tests/test_refusals.py`.** It opens with *"The rule this file exists to enforce"* and plants under `tmp_path`. Cases:
  - the path for a branch carrying `/` (`feat/x` → `feat%2Fx.json` under `round_refusals/`);
  - a write–read round trip, including `announced`;
  - `read` for another number giving the empty record while `read_announced` keeps the file's lines;
  - `clear` on an absent file;
  - one malformed document per clause, each with its exact `ValueError` text;
  - everything written staying inside `<stateDir>/.flow_walker_state/`;
  - a second `lock()` from another thread with `lock_timeout=0.2` raising the exact `TimeoutError` text.

**Verification:**

- `tests/test_refusals.py` passes, with each error asserted as an exact string.
- After every case, the walk's own directory holds nothing but `round_refusals/` and its contents: the store writes only its file, its lock and its temporary files.
