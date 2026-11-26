### 1. The session's stream, stderr tail, exit status and validated return object never leave `ClaudeExecutor.run`, so the #484 deferral cannot hold and the return fields the pilot reads are lost

**File:** `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (`ClaudeExecutor.run`): "reading = judge_session(session.stdout, contract, self._cwd)"; also `devscene-flow-host/src/devscene_flow_host/host/session_stream.py` (`_classify`): "return Completed(outcome, _detail(document.get(DETAIL_FIELD), cwd))"
**Class:** Wrong behaviour
**Failure:** If #484's run loop drives `ClaudeExecutor.run` as `session_process.py` expects, it cannot write the session's stream: no value it receives carries it. If the #424 cutover drives a writer that returns `questions`, the park body gets no questions, and `tasks_count` / `tests_count` / `reason` cannot be read either: `judge_session` validates the return object and then throws it away.

**The problem.** `ClaudeExecutor.run` is the only caller of `run_session`. A `grep -rn "run_session\|stderr_tail\|returncode"` over `devscene-flow-host/src` and `graphscene/src` finds no other caller, and no reader of either field outside `session_process.py`. `run` passes `session.stdout` to `judge_session` and then drops it. It never reads `session.stderr_tail` or `session.returncode`. Nothing reaches the host except the `NodeResult` (`Completed(outcome, detail)` or `Failed(failure, reason)`) and the `SessionUsage` handed to the sink, and neither holds the stream, the stderr tail, the exit status or the return object. This breaks three things:

1. **The cited deferral does not hold.** `session_process.py`'s docstring defers *"Writing the stream anywhere: the run loop's (#484)."* #484's run loop only gets what `graphscene.Executor.run` returns plus what the sink receives, so it cannot write a stream it is never given. The pilot does write it: `cli/templates/scripts/autonomous-watcher.sh` → `engine_pipeline` tees the stream to `${log_path%.log}.stream.jsonl`. Per `harness-runs/lessons.md` (*"A client-visible divergence from the implementation being ported is justified only by a task-prompt exclusion or an entry-point deferred-work marker naming what reverts it"*), this deferral names an owner that cannot revert it.
2. **The stderr tail is collected and then thrown away.** Task 3 drains and keeps the last `STDERR_TAIL_BYTES`, and Task 4 discards them. Take a session that dies at startup: a bad flag in the host's `session_args`, an auth error, an unknown `--agent`. It prints its only diagnostic to stderr and exits non-zero with no stream events, so it becomes `Failed("infra", "the agent did not resolve: no init event")`. The engine retries it up to its attempt bound and then escalates, and the line that explains the failure is in neither the reason nor the usage record. The pilot keeps stderr: `session_exec` → `2>>"$log_path"`. The task-plan review round 0, Should Fix 3 (*"Nothing reads `SessionRun.stderr_tail`"*), raised this in planning. It was not applied, and no branch review re-raised it.
3. **The validated return object is discarded.** `_classify` parses the final `json` block, validates it against the contract's schema, and keeps only `outcome` and `findings_file`. The pilot this ports keeps it, and its driver reads it:
   - `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_ask_park` builds the park body from the object's `questions`;
   - `pd_ret_field plan_writer tasks_count`, `pd_ret_field ui_writer tests_count` and `pd_ret_field ui_writer reason` read single fields;
   - `pd_session_detail` prints the whole return text in an escalation.

   The task prompt says *"#424's planning cutover runs on this one"*. Once it does, those reads have no source, because `Completed` cannot carry them (`NodeResult` stays as #420 shipped it, by the prompt's decision). The only host-supplied channel out of the executor is the usage sink.

**Fix.** Carry these values on the one channel the host already owns, the `SessionUsage` the sink receives.

1. `devscene-flow-host/src/devscene_flow_host/host/session_stream.py`:
   - Add a field `return_document: Mapping[str, object] | None` to `SessionReading`, after `withheld_tools`.
   - Change `_classify` to return `tuple[NodeResult, Mapping[str, object] | None]`. Every `return Failed(…)` becomes `return Failed(…), None`. The final return becomes `return Completed(outcome, _detail(document.get(DETAIL_FIELD), cwd)), MappingProxyType(document)`.
   - In `judge_session`, unpack it as `result, document = _classify(init, init_tools, result_event, contract, cwd)`. Pass `result=result` and `return_document=document` to `SessionReading`.
   - In the module docstring, extend clause 10 to: *"otherwise `Completed`, its detail the return's non-blank `findings_file` resolved against `cwd`; the validated return object is kept as `return_document`, which is `None` on every other clause."*
2. `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py`:
   - Add these fields to `SessionUsage`, after `withheld_tools` and before `result`: `stream: str`, `stderr_tail: str`, `returncode: int | None`, `return_document: Mapping[str, object] | None`.
   - In the launch-error branch, pass `stream=""`, `stderr_tail=""`, `returncode=None`, `return_document=None`.
   - In the other branch, pass `stream=session.stdout`, `stderr_tail=session.stderr_tail`, `returncode=session.returncode`, `return_document=None if session.stalled else reading.return_document`.
   - Add a rule bullet to the module docstring: *"The usage record also carries the session's whole stdout stream, its stderr tail and its exit status, and, for a `Completed` result, the validated return object, so the host can write the stream and read the return's other fields, which `Completed` cannot carry."*
   - Change the *"Deliberately not covered"* bullet *"Writing the stream or a session manifest."* to *"Writing the stream (from `SessionUsage.stream`) or a session manifest: the host's (#484)."*
3. `devscene-flow-host/src/devscene_flow_host/host/session_process.py`: in the module docstring, change *"Writing the stream anywhere: the run loop's (#484)."* to *"Writing the stream anywhere: the run loop's (#484), which receives it through `ClaudeExecutor`'s `SessionUsage.stream`."*
4. `devscene-flow-host/README.md` → `## The executor` → **The usage sink.**: in the list of what `SessionUsage` carries, after *"the tools the contract declares that `init` withheld,"*, insert *"the whole stdout stream, the stderr tail, the exit status, the validated return object for a `Completed` result (otherwise `None`),"*. After *"Building that pairing into a run loop is #484."*, add the sentence *"Writing the stream, and reading a return's fields other than `outcome` and `findings_file` (a writer's `questions`, say), are the host's, from this record."*
5. Tests:
   - `devscene-flow-host/tests/test_session_stream.py`: in `test_clause_10_a_valid_return_is_completed_without_detail`, add `assert reading.return_document == {"outcome": "PASS"}`. In `test_clause_1_no_init_event_is_infra`, add `assert reading.return_document is None`.
   - `devscene-flow-host/tests/test_claude_executor.py` → `test_a_completed_session_returns_its_absolute_detail_and_one_usage_record`: add these assertions.

     ```python
     assert usage.return_document == {"outcome": "PASS", "findings_file": "reviews/plan_review.md"}
     assert usage.returncode == 0
     assert usage.stderr_tail == ""
     assert usage.stream.splitlines()[0] == init_event(_TOOLS)
     ```

   - `test_a_launch_error_is_an_infra_failure_with_empty_usage`: extend the asserted tuple with `usage.stream, usage.stderr_tail, usage.returncode, usage.return_document` and the expected tuple with `"", "", None, None`.
   - `test_a_stall_is_an_infra_failure_keeping_the_streams_usage`: add `assert sink.records[0].return_document is None`.
   - Add this case:

     ```python
     def test_a_session_that_dies_on_stderr_keeps_its_tail_and_status(tmp_path: Path) -> None:
         command = plant(tmp_path, {"steps": [{"stderr": "error: unknown option"}], "exit": 1})
         sink = Usages()

         result = asyncio.run(_executor(command, tmp_path, sink).run(_dispatch()))

         assert result == Failed("infra", "the agent did not resolve: no init event")
         usage = sink.records[0]
         assert (usage.stream, usage.stderr_tail, usage.returncode, usage.return_document) == (
             "",
             "error: unknown option\n",
             1,
             None,
         )
     ```

   The fix edits only `tests/test_session_stream.py` and `tests/test_claude_executor.py`, so those are the only suites it runs: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_session_stream.py tests/test_claude_executor.py`.
