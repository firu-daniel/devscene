### 1. The executor's host-input lists never name `--add-dir <plugin_dir>`

**File:** `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (module docstring, *"Deliberately not covered:"*) — "The per-agent MCP flags and the shared session flags: the host's input."; and `devscene-flow-host/README.md` (`## The executor`, the **What it is given.** table) — "| `session_args` | The shared session flags, passed through unchanged |"

**Problem.** The pilot passes `--add-dir <plugin_dir>` to every planning node's session: `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags` prints `--agent <plugin>:<agent>`, `--plugin-dir <plugin_dir>` and then `--add-dir <plugin_dir>`, leaving the `--add-dir` out only when `PD_PLUGIN_DIR_ADDED` is `1` (the caller's shared flag vector already carries it). `ClaudeExecutor.run` adds `--agent` and `--plugin-dir` but not `--add-dir`, and neither the module docstring's list of host inputs nor the README's `## The executor` says the host must supply it. A host that builds `session_args` from those two lists launches sessions without it. This was Should Fix 4 of the round-0 task-plan review (`harness-runs/task_plan_reviews/feat_flow_host_claude_executor/review_0.md`), and it was never applied.

**Fix.** Documentation only. Do not add `--add-dir` to the argument vector, and do not add it to `EXECUTOR_FLAGS`. The host still supplies it through `session_args`.

- In `claude_executor.py`'s module docstring, under *"Deliberately not covered:"*, replace the bullet `- The per-agent MCP flags and the shared session flags: the host's input.` with:

  ```
  - The per-agent MCP flags and the shared session flags: the host's input. The shared flags
    include `--add-dir <plugin_dir>`, which the executor does not add. The pilot passes it for
    every node (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`) unless its
    shared vector already carries it (`PD_PLUGIN_DIR_ADDED`).
  ```

- In `devscene-flow-host/README.md` → `## The executor` → the **What it is given.** table, change the `session_args` row's *What it is* cell to:

  ```
  The shared session flags, passed through unchanged. They include `--add-dir <plugin_dir>`, which the executor does not add: the pilot passes it for every node (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags`)
  ```

- In the same section's **The flags it adds.** paragraph, after the sentence listing the vector, add: `` `--add-dir <plugin_dir>` is not among them: the host passes it in `session_args`. ``

Name no issue or PR number in the new prose (Finding 3).
