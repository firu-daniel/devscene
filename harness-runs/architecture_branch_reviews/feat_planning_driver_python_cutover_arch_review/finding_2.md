### 2. Stop using `RecordError` for a host write collision and a host-side ledger check

**Sites:**
- `devscene-flow-host/src/devscene_flow_host/host/run_records.py` → `write_park`, the substring `raise RecordError(f"'{rel}' already exists")`.
- `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` → `run_planning`, the substring `if not ledger.is_file():` and the `RecordError(... "the setup session creates it")` it raises.

**The problem.**

`.claude/context/devscene-flow-host.md` → `## Errors` defines `RecordError` as *"the one anticipated failure of **reading** a repository record — absent, or not readable as the harness writes it"*, and `## The internal layers` gives reading a record into a value to `records`. Two of the new `host` modules stretch that:

- **`write_park` uses it for a write collision.** It raises `RecordError` when the park path it is about to *write* already exists. That is a host write conflict, not a record that could not be read. The module docstring names the behaviour (*"an existing file at that path a `RecordError` naming it"*) but does not argue why a reading error is reused for it.
- **`run_planning` does a record check in `host`.** It checks the flow-progress ledger's existence and composes the message itself. The ledger path and its readers belong to `devscene-flow-host/src/devscene_flow_host/records/ledger.py` (`ledger_path`, `read_planning_marks`, `read_run_mode_entries`), and each of those readers already raises its own `RecordError` (*"the flow-progress ledger '…' does not exist"*) with a different spelling of the path.

This review's plan-time round raised both points as Should Fix (`harness-runs/architecture_reviews/feat_planning_driver_python_cutover/review_0.md` → `## Should Fix`, the `task_10_plan.md` and `task_16_plan.md` bullets). Neither was taken up.

The exit status is `2` either way, so no caller sees a different answer. That is why this is a Should Fix.

**The fix.**

1. **`host/run_records.py`.** Either raise a host-owned error for the collision and add it to `commands/planning_driver.py` → `failure`'s anticipated set, or keep `RecordError` and say in the module docstring, under *"The rule:"*, why a park collision is reported as a record failure.
2. **`host/planning_run.py`.** Move the existence check behind `records/ledger.py`. For example, add a `require_ledger(repo_root, state_dir, branch) -> None` there that raises the `RecordError` with the message the readers already use, and call it from `run_planning` in place of the inline `is_file()` check and message. Keep the *"the setup session creates it"* clause if the suites assert it, and update the planted-message cases in `devscene-flow-host/tests/test_planning_run.py` and `devscene-flow-host/tests/test_ledger.py` to the one spelling.
