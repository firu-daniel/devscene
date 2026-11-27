### Task 13 — Record each node session's stream, manifest line, formatted log and session-table row in `host/node_sessions.py`

**Goal:** Add the driver's `UsageSink` and `LaunchSink` in one class, `NodeSessions`. For every node session `ClaudeExecutor` reports, it writes what the bash `pnl_launch` / `pnl_reap` wrote:
- the node's stream file;
- the stream appended to the run's stream;
- the `node-sessions.jsonl` manifest line `run-analytics.sh` classes node sessions by;
- the formatted output in the run log.

It pairs each usage record with GraphScene's `Launch` row into the session table the driver observes at exit. It also keeps each node's last return document for Task 17's reads.

**Depends on:** Task 11, which adds `host/observations.py` → `Observations.add(category, problem, evidence, cost)`. This task calls it for the per-session observations.

**The two inputs, as their producers define them:**
- **The usage record.** `host/claude_executor.py` → `SessionUsage` carries `node`, `agent`, `session_id`, `started_at`, `duration_seconds`, `stalled`, `total_cost_usd`, `permission_denials`, `withheld_tools`, `stream`, `stderr_tail`, `returncode`, `return_document` and `result`. `UsageSink.record(usage)` is called once per `run` that returns, just before the return.
- **The `Launch` row.** `graphscene` → `Launch(seq, node, agent, attempt, max_attempts, result)` arrives through `LaunchSink.record` after that `run` returns. A `Launch` row from GraphScene's total-run timeout has no usage record, and that is not a pairing fault.

**Where this task stops.** It writes and pairs. It decides no outcome, and runs no hook.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py` (new)
- `devscene-flow-host/tests/test_node_sessions.py` (new)

**Work:**

- [ ] **Construction and numbering.** `NodeSessions(*, log_path: Path, formatter: str, observations: Observations, narrate: Callable[[str], None])`.
  - Its own sequence starts past every `<n>-*.stream.jsonl` already in `${log%.log}.planning/`, as `pd_seq_init` did, so a second drive never overwrites the first drive's files.
  - It does not use `Launch.seq`, because the dispatch counter resets per drive.
  - `PLANNING_DIRECTORY_SUFFIX = ".planning"` and `MANIFEST_NAME = "node-sessions.jsonl"` are `Final` constants.
- [ ] **`record(usage: SessionUsage)`, the usage sink.** It does the following, in order:
  - takes the next `seq` and writes `usage.stream` to `${log%.log}.planning/<seq>-<node>.stream.jsonl`;
  - appends the same bytes to `${log%.log}.stream.jsonl`;
  - when `usage.session_id` is set, appends `{"session_id": <id>, "seq": "<seq>", "node": <node>}` to the manifest, compact, with `seq` a string as `pnl_reap` wrote it;
  - runs `formatter` as one argv word with the stream on stdin, appending its stdout to the log;
  - appends `usage.stderr_tail`, when non-empty, to the log;
  - keeps `(seq, usage)` as pending for `usage.node`;
  - when `usage.return_document` is set, keeps it as that node's last return document.
- [ ] **`record(launch: Launch)`, the launch sink.**
  - It pairs `launch` with the pending usage of `launch.node` whose `result == launch.result`.
  - It appends one session-table row: `<seq> <node> <agent> <attempt>/<max_attempts> <result kind/outcome> <duration s> <cost or ->`.
  - A `Launch` with no pending usage gives a row with `-` for seq, duration and cost, and narrates `no usage record for <node> (total-run timeout)`.
  - The per-session observations are those the retired `pd_reap_one` made:
    - `permission_denials > 0` gives `tooling-gap`, *"A planning node session met permission denials"*;
    - a `Failed("infra", …)` with attempts left gives `flow-efficiency`, *"A planning node session failed for an infrastructure reason and was re-dispatched"*;
    - a final `Failed`, recorded as `error`, gives `silent-failure`, *"A planning node session ended in error"*.

  Expose two read-only properties:
  - `rows: tuple[str, ...]`;
  - `return_document(node) -> Mapping[str, object] | None`.
- [ ] **Module docstring.** *"The rule:"* covers the pairing on `node` with equal `result`, and the timeout row being no fault. It names `pnl_launch`, `pnl_reap` and `pd_seq_init`, retired. *"Deliberately not covered"*: what the run does with a `Failed`.
- [ ] **`tests/test_node_sessions.py`:**
  - its header rule;
  - two usages plus two launches give the files `1-plan_writer.stream.jsonl` and `2-plan_review.stream.jsonl`, the run stream holding both in order, and two manifest lines with exact JSON literals;
  - a pre-existing `3-x.stream.jsonl` starts the next drive at `4`;
  - a `cat` formatter puts the stream into the log;
  - a timeout `Launch` with no usage gives its row and no exception;
  - a mismatched `result` is not paired;
  - each observation category is added once for its case, through a recording stand-in for `Observations`.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_node_sessions.py` passes.
- The manifest lines the suite writes are read correctly by `cli/templates/scripts/run-analytics.sh`'s `NODE SESSIONS` rule as written: one object per line, with string `seq`, `session_id` and `node`.

**Deviations from plan:**
- The `run-analytics.sh` verification bullet was checked by reading, not by running the script: its manifest filter (`fromjson? | objects | select((.session_id | type) == "string" and (.node | type) == "string")`, then `(.seq // "") | tostring`) was compared with the exact literals `test_two_sessions_write_their_streams_the_run_stream_and_the_manifest` asserts. No suite of this flow runs that script over the written file.
- The plan leaves `<result kind/outcome>` open. The row shows `Completed.outcome`, else the result's `kind` (`failed`), following the retired `pd_reap_one`'s `${outcome:-$kind}`. Duration is rounded to whole seconds with an `s` suffix, and cost is `str(total_cost_usd)`.
- The plan does not say what happens when a formatter cannot be started. Such a formatter is narrated (`the formatter '<f>' could not run: …`) rather than raised, and its exit status is ignored, as the bash `tee | "$PD_FORMATTER"` pipeline ignored both.
- The observation evidence and cost texts copy `pd_reap_one`'s texts without its `round <n>` part, which neither input carries. The seq is `-` when no usage was paired.
