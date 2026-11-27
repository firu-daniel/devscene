### Task 12 — Answer STOP, PAUSE and the dispatch counter, and fix the planning limits, in `host/run_control.py`

**Goal:** Implement GraphScene's `RunSignals` and `DispatchCounter` over the harness's files, and fix the planning run's `ExecutionLimits` as flow-host constants. The task prompt's decision: *"The harness runs at most 5 dispatches at once, as a `devscene-flow-host` constant."* The pilot's retry and backoff values stay: `PD_MAX_ATTEMPTS=3`, and `PD_BACKOFF_SECS`, default and ceiling 60.

**Depends on:** Task 9, which adds `records/core_limits.py` → `read_max_total_dispatches(plugin_dir: Path) -> int`. That is the dispatch cap.

**Where this task stops.** It answers signals and counts. Halting on them is GraphScene's `clear_set`. What a halt does afterwards (log, pause files, partial commit) is **Task 17's**.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/run_control.py` (new)
- `devscene-flow-host/tests/test_run_control.py` (new)

**Work:**

- [ ] **`FileRunSignals(repo_root, state_dir)`.** `stop_requested()` is `<state_dir>/STOP` existing. `pause_requested()` is `<state_dir>/PAUSE` existing. Both are re-checked on every call, never cached. `STOP_FILE` and `PAUSE_FILE` are `Final` constants.
- [ ] **`kill_switch_present(main_repo) -> bool`.** It is `<main stateDir>/AUTONOMOUS_STOP` existing, as the retired `pd_main` read `hr_state_path "$PD_MAIN_REPO" AUTONOMOUS_STOP`. The main checkout's `stateDir` is read through `records/config.py` → `read_config`. `KILL_SWITCH_FILE` is a `Final` constant.
- [ ] **`FileDispatchCounter(repo_root, state_dir)`.**
  - It keeps its total in `<state_dir>/.dispatch_counter`, the `DISPATCH_COUNTER_FILE` constant, as one decimal line.
  - `reset()` writes `0\n`, as `pd_main` did at each drive.
  - `total()` reads the file.
  - `increment()` writes `total + 1` whole, through a temporary file and `os.replace`, and returns it.
  - An unreadable or non-integer file is a `RecordError` naming it.
- [ ] **The limits.** `MAX_CONCURRENT_DISPATCHES: Final = 5`, `MAX_ATTEMPTS: Final = 3`, `BACKOFF_SECONDS: Final = 60.0` and `UNDELIVERED_LIMIT: Final = 3`.
  - `planning_limits(dispatch_cap: int) -> ExecutionLimits` returns `ExecutionLimits(max_attempts=MAX_ATTEMPTS, backoff_seconds=BACKOFF_SECONDS, dispatch_cap=dispatch_cap, run_timeout_seconds=None, max_concurrent_dispatches=MAX_CONCURRENT_DISPATCHES)`.
  - The module docstring says why 5 is a flow-host constant, not a `devscene.config.json` key: the flow host is the harness's own implementation of its flows. It also says that GraphScene's default of 10 is for hosts that set none.
- [ ] **`tests/test_run_control.py`:**
  - its header rule;
  - STOP and PAUSE answered from planted files, and re-read after a file is removed;
  - the kill switch under a configured `stateDir`;
  - the counter's reset, two increments returning `1` then `2`, and its exact file bytes;
  - a corrupt counter's `RecordError` text;
  - `planning_limits(40)` field by field against literals, `max_concurrent_dispatches == 5` among them.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_run_control.py` passes.
- `FileRunSignals` and `FileDispatchCounter` satisfy GraphScene's protocols structurally. `mypy` `strict` passes on a test that assigns each to a `RunSignals` / `DispatchCounter`-typed variable.
