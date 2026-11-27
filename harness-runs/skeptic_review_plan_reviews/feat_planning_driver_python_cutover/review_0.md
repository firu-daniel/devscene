# Review plan meta-review — iteration 0

## Must Fix
1. **Finding 1's fix tells the implementer to run two tree guards it does not edit** — refers to review finding #1. Offending file: `harness-runs/skeptic_reviews/feat_planning_driver_python_cutover_skeptic_review/finding_1.md`.
   The finding's closing paragraph says: *"Both source edits are under `devscene-flow-host/src/devscene_flow_host/**`, so they also run the tree guards `tests/test_boundary.py` and `tests/test_layers.py` the same way."* The fix creates and edits neither file. Its edits are to `node_sessions.py`, `run_exits.py`, `tests/test_node_sessions.py` and `tests/test_run_exits.py`. `${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule` point 4 says: *"No plan names a tree guard the task neither creates nor edits … the guard run is the loop's, never the plan's"*. It binds *"the code-review and skeptic findings"* and requires every reviewer to raise a breach as a Must Fix. Point 7 already selects and runs those guards from the changed-path set (`devscene.config.json` → `treeGuards`), so the finding's sentence does two things wrong. It duplicates the loop's selection, and it puts a test run in a plan where the rule forbids one. The two run commands for the edited test files (`… test tests/test_node_sessions.py`, `… test tests/test_run_exits.py`) are allowed and stay.
   **Class:** Wrong build
   **Failure:** If the C2.4 implementer follows `finding_1.md` as written, then it runs `tests/test_boundary.py` and `tests/test_layers.py` because the finding instructs it to. Those are test files the fix neither creates nor edits, and `## The test-run rule` point 4 forbids a plan from naming them.
   **Fix:** In `finding_1.md`, delete the last sentence of the final paragraph (*"Both source edits are under … the same way."*). Keep the sentence that runs only the two edited test files. Leave the index and the readiness entry as they are.

## Should Fix
_None._

## Nice to Have
_None._
