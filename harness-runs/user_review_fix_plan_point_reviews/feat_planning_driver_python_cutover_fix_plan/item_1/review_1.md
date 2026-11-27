# general review — 1. Node output reaches the run log only when a node session ends — iteration 1

Scope: the catch-all dispatch. The only file in the uncommitted set that sits outside another layer's path is `docs/watcher.md`. The `devscene-flow-host/` files were graded against `.claude/context/devscene-flow-host.md` in `review_0.md` and are not graded again here. They were read only to check that the doc matches the code.

Checked against the code:
- **The node stall rule.**: the claim that the watchdog *"takes the newer of the log's and the run stream's mtimes"* matches `cli/templates/scripts/autonomous-watcher.sh` → `check_stalled_runs` (*"Liveness is the NEWEST mtime across the formatted log and the raw stream"*).
- The claim that thinking blocks and tool results do not move the log matches `cli/templates/scripts/autonomous-format-stream.sh` → *"WHAT IT DELIBERATELY DROPS"*.
- **Where node streams land.**: *"one formatter process per drive"* matches the code. `host/planning_run.py` → `run_planning` builds one `NodeSessions` and closes it in a `finally`, and `NodeSessions._format_live` starts one `Popen`.
- The run-stream and manifest timing in that section matches `NodeSessions._record_usage`.

Verification: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_node_sessions.py` was run from the repository root and exited 0 (23 passed).

## Should Fix

1. **The flow host's README still says the formatter gets one node's stream on stdin, but the live path now runs one long-lived formatter over every node's lines** — `devscene-flow-host/README.md` (the planning driver's options table, `--formatter` row) — "run as one argv word with a node's stream on stdin, its stdout appended to the log"
   This change makes `NodeSessions` start the formatter once per drive and send whole lines to it from every live node (`host/node_sessions.py` → `_format_live`). The per-node run now happens only on the record-only path, when no live stream was opened. `docs/watcher.md` → **Where node streams land.** now says *"through one formatter process per drive"*, so the README row and that doc disagree. This is a description that became false, and no step fails because of it. The file is not in this unit's diff, and the task plan does not list it.
   **Fix:** Reword the `--formatter` row to: "The watcher's stream formatter, a path or `cat`, run as one argv word: one long-lived process per drive receives every live node's whole lines on stdin, its stdout appended to the log (a usage recorded with no live stream is formatted by its own run)."
