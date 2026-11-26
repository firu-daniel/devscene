### 2. The pairing rule does not cover a `Launch` row written by GraphScene's total-run timeout

**File:** `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (module docstring, *"The rule:"*) — "the host pairs them on `node`, with equal `result` as the check."; and `devscene-flow-host/README.md` (`## The executor`, **The usage sink.**) — "the host pairs the two on `node`, with an equal `result` as the check."

**Problem.** The pairing rule says each `run` that returns a result records one usage record just before that node's next `Launch` row, and the host pairs them on `node`. One `Launch` row has no usage record. `graphscene/src/graphscene/engine/set_execution.py` → `_run` wraps `executor.run` in `asyncio.timeout(run_timeout_seconds)`. When that deadline expires, `ClaudeExecutor.run` sees `asyncio.CancelledError`, kills the session, re-raises and records no usage, as designed. The engine then returns `Failed("infra", "timed out: no result within <run_timeout_seconds>s")` itself, and `execute_set` writes the `Launch` row for it. Nothing in the docstring or the README says this row has no usage record, so a host that follows the rule as written reads it as a pairing fault. This was Should Fix 2 of the round-0 task-plan review (`harness-runs/task_plan_reviews/feat_flow_host_claude_executor/review_0.md`), and it was never applied.

**Fix.** Documentation only. Do not change the code or the sink's call rule.

- In `claude_executor.py`'s module docstring, directly after the *"The rule:"* paragraph that ends "the host pairs them on `node`, with equal `result` as the check.", add:

  ```
  A `Launch` row written by GraphScene's total-run timeout
  (`graphscene/src/graphscene/engine/set_execution.py` → `_run`, its result
  `Failed("infra", "timed out: no result within <run_timeout_seconds>s")`) has no usage record:
  the deadline cancels `run`, which records none. The host pairs nothing with that row and does
  not treat it as a pairing fault. The usage of a session killed this way is lost, unlike a
  stall's.
  ```

- In `devscene-flow-host/README.md` → `## The executor` → **The usage sink.**, directly after the sentence ending "the host pairs the two on `node`, with an equal `result` as the check.", add the same three facts in the README's prose: the timeout row (`set_execution.py` → `_run`, `Failed("infra", "timed out: no result within <run_timeout_seconds>s")`) has no usage record because the deadline cancels `run`, the host does not treat the unmatched row as a pairing fault, and that session's usage is lost, unlike a stall's.

Name no issue or PR number in the new prose (Finding 3).
