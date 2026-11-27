### 1. An escalation park for a gate whose three attempts all failed for an infrastructure reason no longer lists those attempts

**File:** `devscene-flow-host/src/devscene_flow_host/host/run_exits.py` (`_Actor._session_detail`) — "text += SESSION_REASON.format(reason=self._launch_reason(node) or NOT_CAPTURED)"; `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py` (`NodeSessions._record_launch`) — "self._results[launch.node] = result"

**The problem.** The retired bash driver wrote one extra block in an `<escalate>` park's per-session section when the held node had used up its infrastructure attempts. `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_session_detail` (at `origin/dev`) printed it right after the `- reason:` line:

```sh
pd_node_var "$node" EXHAUSTED
if [ -n "$PD_V" ]; then
  printf -- '- attempts: all %s ended for an infrastructure reason, each re-dispatched alone while attempts remained:\n' "$PD_MAX_ATTEMPTS"
  while IFS= read -r line; do
    [ -z "$line" ] || printf -- '  - %s\n' "$line"
  done <<EOF
$PD_V
EOF
fi
```

`pd_reap_one` filled that value. Each `error`/`infra` reap appended `attempt <k> of <max> (#<seq>): <reason>` to the node's attempt log. On the reap that went on to record an outcome, `PD_EXHAUSTED_<node>` became the log if this was the last attempt and empty otherwise, and the log was then cleared. An `undelivered` reap touched neither.

The Python port drops the block without saying so. `_session_detail` writes `- agent:`, `- reason:` (the **last** `Launch` result's reason only) and `- return text:`. `NodeSessions` keeps only the last result per node (`launch_result`). It keeps no attempt history, so `act_on_exit` has nothing to print. None of these mark the omission as a divergence: the story plan, `task_17_plan.md`, the module docstrings and `docs/flow-graph-walker.md`. The story's `## Context` says the opposite: *"Wherever the run-mode pieces leave a rule to the host, the driver behaves as the pilot did."* No retired `cli` suite pinned this line, so the Task 3 retirement map did not catch the loss either.

**Why it is reachable.** `host/run_control.py` → `planning_limits` sets `max_attempts=3`. GraphScene's `AttemptBook` records a gate that fails `infra` on its third attempt as `FAILURE_OUTCOME` (`"error"`), which is held at the round and escalates as a `Stop` whose `held` names the gate. `act_on_exit` → `_escalate` → `_session_detail` then writes the park the operator answers. This is the exact path `tests/test_planning_driver_control.py` drives for a gate held as `error` after three attempts (`task_20_plan.md`: *"A gate held as `error` after three attempts escalates with a `plan-round-partial` call before the park"*). In that park, the operator sees one reason, for example `stalled: the stream was silent for 2685 s; the session was killed`. They cannot see that the two earlier attempts failed for different reasons, such as a launch error and then a missing `findings_file`. The pilot's park showed all three.

Confirmed by reading only. The two functions were read at `origin/dev` and compared with `_session_detail` and `NodeSessions` on this branch. No probe was run.

**Fix.** Keep a per-node attempt log in `NodeSessions`, expose the exhausted one, and print it in `_session_detail` exactly as `pd_session_detail` did.

1. In `devscene-flow-host/src/devscene_flow_host/host/node_sessions.py`:
   - In `__init__`, add:
     ```python
     self._attempt_log: dict[str, list[str]] = {}
     self._exhausted: dict[str, tuple[int, tuple[str, ...]]] = {}
     ```
   - Add the public reader beside `launch_result`:
     ```python
     def exhausted_attempts(self, node: str) -> tuple[int, tuple[str, ...]] | None:
         return self._exhausted.get(node)
     ```
   - In `_record_launch`, directly before `self._rows.append(`, add `self._track_attempts(launch, seq_text)`. Then add the method:
     ```python
     def _track_attempts(self, launch: Launch, seq_text: str) -> None:
         result = launch.result
         if isinstance(result, Failed) and result.failure == "undelivered":
             return
         log = self._attempt_log.setdefault(launch.node, [])
         infra = isinstance(result, Failed) and result.failure == "infra"
         if infra:
             log.append(
                 f"attempt {launch.attempt} of {launch.max_attempts} (#{seq_text}): {result.reason}"
             )
             if launch.attempt < launch.max_attempts:
                 return
             self._exhausted[launch.node] = (launch.max_attempts, tuple(log))
         else:
             self._exhausted.pop(launch.node, None)
         self._attempt_log[launch.node] = []
     ```
   - In the module docstring, after the sentence that opens *"The last return document each node's usage carried is kept"*, add: *"Each node's `Failed("infra", …)` launches are logged as `attempt <k> of <max> (#<seq>): <reason>`, as the retired `pd_reap_one` logged them; a launch that ends the node's attempts keeps the log for `exhausted_attempts(node)` when it was the last `infra` attempt and clears it otherwise, and an undelivered launch touches neither."*

2. In `devscene-flow-host/src/devscene_flow_host/host/run_exits.py`:
   - Add two constants beside `SESSION_REASON`:
     ```python
     SESSION_ATTEMPTS: Final = (
         "- attempts: all {max} ended for an infrastructure reason, each re-dispatched alone "
         "while attempts remained:\n"
     )
     SESSION_ATTEMPT_ITEM: Final = "  - {line}\n"
     ```
   - In `_Actor._session_detail`, directly after the `text += SESSION_REASON.format(...)` line, add:
     ```python
     sessions = self._outcome.sessions
     exhausted = None if sessions is None else sessions.exhausted_attempts(node)
     if exhausted is not None:
         maximum, lines = exhausted
         text += SESSION_ATTEMPTS.format(max=maximum)
         text += "".join(SESSION_ATTEMPT_ITEM.format(line=line) for line in lines)
     ```
   - In the module docstring's rule, extend the `Stop` bullet with: *"each held node's section lists its attempts when all of them ended for an infrastructure reason, as `pd_session_detail` did"*.

3. Tests (literal expected values, written from the rules above):
   - In `devscene-flow-host/tests/test_node_sessions.py`, add:
     ```python
     def test_a_node_whose_every_attempt_failed_for_infra_keeps_its_attempt_log(
         tmp_path: Path,
     ) -> None:
         sessions, _, _ = _sessions(tmp_path)
         for attempt, reason in ((1, "launch failed"), (2, "PASS carries no findings_file"), (3, "stalled")):
             failed = Failed("infra", reason)
             sessions.record(_usage("plan_review", failed))
             sessions.record(Launch(attempt, "plan_review", "plan_review-agent", attempt, 3, failed))
         assert sessions.exhausted_attempts("plan_review") == (
             3,
             (
                 "attempt 1 of 3 (#1): launch failed",
                 "attempt 2 of 3 (#2): PASS carries no findings_file",
                 "attempt 3 of 3 (#3): stalled",
             ),
         )


     def test_a_node_that_recovers_after_an_infra_failure_keeps_no_attempt_log(
         tmp_path: Path,
     ) -> None:
         sessions, _, _ = _sessions(tmp_path)
         failed = Failed("infra", "launch failed")
         sessions.record(_usage("plan_review", failed))
         sessions.record(Launch(1, "plan_review", "plan_review-agent", 1, 3, failed))
         sessions.record(_usage("plan_review", Completed("PASS", "r.md")))
         sessions.record(Launch(2, "plan_review", "plan_review-agent", 2, 3, Completed("PASS", "r.md")))
         assert sessions.exhausted_attempts("plan_review") is None
     ```
     Wrap the long tuple line to stay within the package's `ruff` line length.
   - In `devscene-flow-host/tests/test_run_exits.py`, add a case after `test_an_escalation_holding_gates_commits_the_partial_then_parks`. It records three `infra` attempts for `plan_review` directly on `run.sessions`: each a `SessionUsage` built as `_Run.session` builds it, followed by `Launch(k, "plan_review", "plan_review-agent", k, 3, Failed("infra", "stalled"))` for `k` in 1..3. It then acts on a `Stop` holding only `GateRecord("plan_review", "error", None)`, the same as the existing case's `Stop` with that one gate. Assert that `run.question(1)` contains this exact block after `- reason: stalled\n`:
     ```
     - attempts: all 3 ended for an infrastructure reason, each re-dispatched alone while attempts remained:
       - attempt 1 of 3 (#1): stalled
       - attempt 2 of 3 (#2): stalled
       - attempt 3 of 3 (#3): stalled
     ```
     Its `- return text:` line is `not captured in this session`.

Run only the two edited test files, each on its own: `bash scripts/python-service.sh --package devscene-flow-host test tests/test_node_sessions.py`, then `… test tests/test_run_exits.py`.
