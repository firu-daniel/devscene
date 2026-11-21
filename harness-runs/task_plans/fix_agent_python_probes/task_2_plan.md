### Task 2 — Run every Python package's lint and type check from `scripts/typecheck.sh`, grading exit 3 as `BLOCKED`

**Goal:** Make `commands.typecheck` (`bash scripts/typecheck.sh`) reach the Python packages' `ruff` and `mypy`, so every unit's whole-tree type check catches a Python defect. An unprovisioned environment must never read as a type error.

**Depends on:** Task 1, which adds `bash scripts/python-service.sh check`. The contract this task calls: it takes no argument; it prints one `python-service: check: <row> <leg> PASS|FAIL|BLOCKED` line per leg; it exits `0` when every leg passed, `1` when any leg failed, `3` when none failed and at least one is `BLOCKED` (unprovisioned), and `2` on usage. This task calls it and grades its status. It does not re-list the packages, which stay `python-service.sh`'s table's.

**Where this task stops.** `cli/templates/scripts/typecheck.sh` is **not** edited: what an adopter receives does not change. **Task 4** pins this task's grading. **Task 7** documents it.

### Targets

- `scripts/typecheck.sh` — this repository's hand-edited `commands.typecheck` wrapper.

**Work:**

- [ ] **Add the Python step** between `bash scripts/check-shell-parse.sh` and the `npm run build "$@"` line, so the build line stays the last one and the only one carrying the caller's arguments (the existing comment's rule). If `scripts/python-service.sh` is a regular file, run `bash scripts/python-service.sh check` with no argument and keep its status as `python_status`. Otherwise print `typecheck: python checks SKIPPED - scripts/python-service.sh is not in this checkout` and treat the step as passed.
- [ ] **Grade it.** If `python_status` is `3`, print `typecheck: python checks BLOCKED - a package environment is not provisioned; run bash scripts/python-service.sh provision outside the sandbox` and do not count it as a failure. Any other non-zero status is a failure. The exit precedence becomes: the build's status when the build failed, else the parse check's when it failed, else the Python step's failure status, else `0`. Both new lines go to stdout, ahead of the verdict, in plain ASCII.
- [ ] **Keep the verdict wire.** Print exactly one verdict line, in the two existing forms only: `PASS: typecheck` and `FAIL: typecheck (exit <status>)`. Extend the hand-added comment block that explains the parse step so it also states the Python step: why it is there (every unit runs this wrapper, so a Python defect fails the unit that wrote it rather than gate 13), that it calls `check` rather than listing packages, the `BLOCKED` grading on gate 13's ground, and that its output is not redirected.

**Verification:**

- This unit's own `<typecheck_cmd>` run is the first real per-unit run. Its output carries a `python-service: check:` line for each of the four legs, then either no Python step line (all `PASS`) or the `BLOCKED` line, then the verdict. Record which, quoting the lines. A `BLOCKED` line is recorded as an evidence downgrade naming the leg, never as a pass of the Python legs.
- Read the edited file and confirm that `npm run build "$@"` is still its last command line and that no new line forwards `"$@"`.
