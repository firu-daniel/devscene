### 2. The breaker's halt says "consecutive sets delivered nothing" even when those sets delivered other nodes' outcomes

**File:** `graphscene/src/graphscene/engine/set_execution.py` (`execute_set`): "consecutive sets delivered nothing"

The breaker gets a strike for a pass that had **any** `Redispatch`, even when its siblings completed in that same pass. Every `Halt("undelivered", …)` carries the detail `"<strikes> consecutive sets delivered nothing"`. The branch's own cases show that text is false. In `graphscene/tests/facade/test_execution_rules.py` → `test_one_gate_undelivered_three_times_running_self_pauses`, the first set delivers `parity_review` and `plan_review` as `approved`, and the halt still reads `"3 consecutive sets delivered nothing"`. `graphscene/tests/engine/test_set_execution.py` → `test_the_third_consecutive_undelivered_pass_halts_with_the_default_breaker` does the same, with `a` passing in the first pass. A host that shows this detail to an operator therefore misreports what happened. The pilot's pause message words it as dispatches undelivered (`cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_undelivered`, "three consecutive dispatches undelivered").

**Fix.** Replace the wording in every place it appears:

1. `graphscene/src/graphscene/engine/set_execution.py`, in `execute_set`:
   `detail = f"{breaker.strikes} consecutive sets delivered nothing"` becomes
   `detail = f"{breaker.strikes} consecutive sets had an undelivered result"`.
2. In the same file's module docstring, `Halt("undelivered", "<strikes> consecutive sets delivered nothing")` becomes `Halt("undelivered", "<strikes> consecutive sets had an undelivered result")`.
3. `graphscene/tests/engine/test_set_execution.py`: in `test_the_third_consecutive_undelivered_pass_halts_with_the_default_breaker`, `"3 consecutive sets delivered nothing"` becomes `"3 consecutive sets had an undelivered result"`. In `test_the_hosts_breaker_limit_takes_effect`, `"2 consecutive sets delivered nothing"` becomes `"2 consecutive sets had an undelivered result"`.
4. `graphscene/tests/facade/test_execution_rules.py` → `test_one_gate_undelivered_three_times_running_self_pauses`: `"3 consecutive sets delivered nothing"` becomes `"3 consecutive sets had an undelivered result"`.

Run the two edited test files, one command each:
`bash scripts/python-service.sh --package graphscene test tests/engine/test_set_execution.py` and
`bash scripts/python-service.sh --package graphscene test tests/facade/test_execution_rules.py`.
