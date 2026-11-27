### 2. The flow host's docstrings cite this branch's plan task numbers, which no reader can resolve after the merge

**File:** `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` (module docstring) — "`host/run_exits.py` (Task 17)."; `devscene-flow-host/src/devscene_flow_host/host/run_control.py` (module docstring) — "deleted by Task 4"; `devscene-flow-host/tests/test_run_exits.py`, `devscene-flow-host/tests/test_planning_driver_walk.py`, `devscene-flow-host/tests/test_planning_driver_control.py` (module docstrings) — "Task 18's suite", "Task 20's suite", "Task 21's suite", "Task 19's suite"

**The problem.** The task prompt decides that, when this branch completes, no code in `graphscene/` or `devscene-flow-host/` names an issue number, keeping what each sentence says without the number. This branch removed every issue number, but it added seven references to its own plan's task numbers. Those numbers live only in `harness-runs/task_plans/feat_planning_driver_python_cutover/`. Take a maintainer reading `tests/test_planning_driver_walk.py`'s *"Deliberately not covered: … Task 20's suite"* after the merge: nothing in the package tells them which file that is, and they reach the wrong answer or none. The sibling file names already exist, and each reference resolves to one of them. This is the same defect the issue-number decision removed, carried by a different kind of number. It is a durable code comment, so it is graded Should Fix.

**Fix.** Replace each reference with the file it means, or drop it where the sentence already names the module:

| File | Text now | Replace with |
|---|---|---|
| `devscene-flow-host/src/devscene_flow_host/host/planning_run.py` | `` `host/run_exits.py` (Task 17). `` | `` `host/run_exits.py`. `` |
| same | `the command over this module (Task 18).` | `` the command over this module, `commands/planning_driver.py`. `` |
| `devscene-flow-host/src/devscene_flow_host/host/run_control.py` | `deleted by Task 4 and readable in that` | `retired and readable in that` (rewrap the line to stay within 100 characters) |
| same | `` `host/run_exits.py` (Task 17). `` | `` `host/run_exits.py`. `` |
| `devscene-flow-host/tests/test_run_exits.py` | `the observation flush: Task 18's suite.` | `` the observation flush: `tests/test_planning_driver_command.py`. `` |
| `devscene-flow-host/tests/test_planning_driver_walk.py` | `retries on their own and observations: Task 20's suite.` | `` retries on their own and observations: `tests/test_planning_driver_control.py`. `` |
| same | `The return fields the hand-off reads: Task 21's suite.` | `` The return fields the hand-off reads: `tests/test_driver_return_fields.py`. `` |
| `devscene-flow-host/tests/test_planning_driver_control.py` | `held gate's return that fails its schema: Task 19's suite.` | `` held gate's return that fails its schema: `tests/test_planning_driver_walk.py`. `` |

Then confirm that none is left: `git grep -n -E 'Task [0-9]+' -- devscene-flow-host graphscene` prints no hit.

Docstrings only change, so no behaviour moves. The edited test files are this fix's own test files; run each one alone as `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py`. Each source file edit also selects the tree guards `tests/test_boundary.py` and `tests/test_layers.py` (`devscene.config.json` → `treeGuards`).
