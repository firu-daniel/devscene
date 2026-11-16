# general review — ### 3. A node that fails for an infrastructure reason parks planning at once instead of being retried — iteration 1

Confirmation note: every finding below was confirmed by reading only. I compared the `docs/` edits with `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_main`, `pd_run_set`, `pd_reap_one`, `pd_session_detail`, `pd_undelivered`, `pd_backoff`) and `cli/templates/scripts/lib/planning-node-lib.sh` (`PNL_REAP_JQ`, `pnl_reap`). I ran no probe or test.

## Should Fix

1. **The unmeasured-facts bullet says every node parks, but the run parks at the first node that fails three times** — `docs/flow-graph-walker.md` (the unmeasured-facts list, the `structured_output` bullet) — "so if neither is ever carried, every node parks after three attempts"
   Planning parks once, at the first node (or first set) whose third attempt also has no decision object. No later node is ever dispatched. A reader judging how bad this gap is would picture one park per node.
   **Fix:** "so if neither is ever carried, planning parks at its first node after three attempts."

2. **The number of `[plan-drive]` lines per retry is wrong** — `docs/flow-graph-walker.md` (`### How each runs a parallel round` → **Cost.**) — "one `[plan-drive]` line and one observation per retry"; and `docs/watcher.md` (`### Script-driven planning (opt-in pilot)` → **What parks or pauses the driver, and what it retries.**) — "carries a `[plan-drive]` line per retry"
   `pd_reap_one` logs `#<seq> <node>: error (<reason>)` and then `<node> (<agent>): attempt k of 3 failed …`. `pd_main`'s `retry)` arm adds `infrastructure retry: backing off …`. That is three lines per retry, not one. The observation count is right: one `flow-efficiency` entry, with no `silent-failure` entry.
   **Fix:** write "`[plan-drive]` lines" with no count, or name the attempt line: "a `[plan-drive]` `attempt k of 3` line and one observation per retry".

## Nice to Have

1. **The docs say the held node is re-dispatched "after `PD_BACKOFF_SECS`", which is not true when the set also has an undelivered session** — `docs/watcher.md` (**What parks or pauses the driver, and what it retries.**) — "the node alone is dispatched again after `PD_BACKOFF_SECS`"; `docs/flow-graph-walker.md` (**Decision.**) — "after `PD_BACKOFF_SECS` its node alone is dispatched again"
   When a set has both, the **Cost.** paragraph says the held node "goes out with its re-dispatch". That re-dispatch takes `pd_undelivered`'s timing: no wait on strike 1. It is also not "alone". The code-side Should Fix in `review_0.md` covers the same case, so these sentences should follow whichever way that is settled.
   **Fix:** once the code decision is made, add to **Cost.** "with the undelivered path's own backoff (none on its first strike)", or drop the clause if the code gains the backoff.

2. **The "Every other `error`" list includes `blocker`, and its citation sits on the wrong sentence** — `docs/flow-graph-walker.md` (**Decision.**) — "**Every other `error`** — an agent-reported `error` or `blocker`" … "(`planning-driver-lib.sh` → `pd_reap_one`, `pd_run_set`'s `retry` result)"
   `blocker` is a declared outcome, not an `error`. The `retry` result belongs to the infrastructure sentence, not the "recorded at once" one.
   **Fix:** "**Everything else** — an agent-reported `error` or `blocker`, …". Move "`pd_run_set`'s `retry` result" to the end of the infrastructure-failure sentence.
