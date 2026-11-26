# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **The group is not killed on a normal exit, though the index says it is** — `task_3_plan.md`, together with the story index's `Top risks:` (`feat_flow_host_claude_executor_story_plan.md`).
   The index's first risk says Task 3 *"kills the whole group on stall, on cancellation and on every other exit path"*. Task 3's `**Work:**` limits the `try`/`finally` kill to paths out of `run_session` *"while it is still running: a stall, `asyncio.CancelledError` and any unexpected exception"*. A session whose leader exits normally while a child it started is still in the group (a background `Bash`-tool process, say) is never `killpg`'d. No case in `tests/test_session_process.py` covers that path. `os.killpg` still reaches the group after the leader is reaped, as long as any member remains. So the fix is one more `killpg` after EOF and exit, ignoring `ProcessLookupError`, plus a case: a `child_pid_file` scenario that exits `0`, after which the child is gone. Either make Task 3 match the index, or narrow the index's sentence to what Task 3 does. Graded Should Fix because it is not verified that a real `claude -p` session leaves such a child behind.

2. **The pairing rule says nothing about a run-timeout `Launch` row** — `task_4_plan.md` (module docstring) and the story index's *"Usage, and how it matches a launch row"*.
   `graphscene/src/graphscene/engine/set_execution.py` → `_run` wraps `executor.run` in `asyncio.timeout(run_timeout_seconds)`. When that expires, `ClaudeExecutor.run` sees `CancelledError`, re-raises it and reports no usage, as designed. The engine then writes `Launch(…, Failed("infra", "timed out: no result within …s"))` itself. That `Launch` row has no usage record. The docstring's pairing contract should say so, so that #484's host does not treat the unmatched row as a pairing fault. Usage is also lost for a session killed this way, unlike a stall.

3. **Nothing reads `SessionRun.stderr_tail`** — `task_4_plan.md`.
   Task 3 collects the last 4096 bytes of stderr, and Task 4 discards them. Take a session that dies at once with a usage error on stderr and nothing on stdout. It becomes `Failed("infra", "the agent did not resolve: no init event")`, and neither the reason nor `SessionUsage` keeps the one line that says why. Carry the tail: as a `SessionUsage` field, or appended (one-lined) to the `infra` reason when the stream has no `init`.

4. **`--add-dir` of the plugin directory is dropped without saying so** — `task_4_plan.md` (*"Deliberately not covered"*) and `task_5_plan.md` (`## The executor`).
   `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_agent_flags` emits `--add-dir <plugin_dir>` for each node, unless `PD_PLUGIN_DIR_ADDED` is `1`. The plan's executor adds only `--agent` and `--plugin-dir`, and its list of host-supplied flags names sandboxing, permission mode, settings, model, allowed tools and the MCP flags, but not `--add-dir`. Name it in the docstring's host-input list and in the README section, so the host that builds `session_args` (#484) carries it.

5. **Task 4 names its `session_events` imports but not their signatures** — `task_4_plan.md` → `**Depends on:**`.
   Task 4 restates `fake_claude.plant` and the scenario keys, but `tests/session_events.py` only by the names `init_event`, `result_event` and `return_block`. Its cases assert the usage record against *"the planted literals"*, which depend on `result_event`'s keyword parameters and defaults (`total_cost_usd=0.25`, `cache_creation_input_tokens=1000`, …). Restate the three signatures as Task 2 defines them.

## Nice to Have

1. **The index's flag list and `EXECUTOR_FLAGS` differ** — the story index says the executor refuses host flags carrying any of `-p`, `--output-format`, `--verbose`, `--agent` and `--plugin-dir`. Task 4's `EXECUTOR_FLAGS` drops `--verbose` and adds `--print` and `--input-format`. Make the two agree.
2. **The arguments `execute_set` needs** — `task_4_plan.md`: the end-to-end case names in-test `RunSignals`, `DispatchCounter` and `LaunchSink` classes. `graphscene.execute_set` also needs `book` (`AttemptBook()`), `breaker` (`UndeliveredBreaker()`), `limits` (`ExecutionLimits(...)`) and `failure_outcome`. Naming them saves the implementer a lookup.
3. **A non-string `result`** — `task_2_plan.md`: the pilot reads a non-string `result` as `""` (`PNL_REAP_JQ` → `if ($res.result | type) == "string" then $res.result else "" end`). State the same in the extraction bullet, so clause 6 (no return block) is the stated result rather than an implementer's guess.
