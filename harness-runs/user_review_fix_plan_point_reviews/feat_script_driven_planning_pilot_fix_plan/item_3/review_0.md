# cli review — ### 3. A node that fails for an infrastructure reason parks planning at once instead of being retried — iteration 0

Confirmation note: every finding below was confirmed by reading `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_main`, `pd_run_set`, `pd_reap_one`, `pd_undelivered`, `pd_drive`). The affected suites (`cli/test/planning-driver-control.test.mjs`, `cli/test/planning-driver-walk.test.mjs`, `cli/test/planning-node-lib.test.mjs`) were **not** executed in this review: the build-and-test command was refused by the session's permission mode. The walker's `next`/`current` behaviour for a set that is partly recorded (`action: wait`, then `current` re-printing only the unrecorded gate) was taken from the task file's citation of `flow-walker.sh` → STATE, not run.

## Should Fix

1. **A set that has both an undelivered session and an infra-held one re-dispatches the held node with no backoff on the first strike** — `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_run_set`) — "if [ -n \"$PD_UNDELIV_NODES\" ]; then\n    PD_SET_RESULT=undelivered\n  elif [ -n \"$PD_RETRY_NODES\" ]; then"
   When one set yields both `undelivered` and an infra-held node, `undelivered` wins. `pd_undelivered` then logs `undelivered: re-dispatching … at once` on strike 1 and sleeps only on strike 2. The infra-held node rides that re-dispatch, so its next attempt goes out with no backoff. The user's requirement (task file, **Required behaviour**: "a backoff between them") is then not met for that node. The third deviation bullet records the precedence but not that it skips the backoff. The run still ends correctly: no wrong park, and the attempt cap still holds. That is why this is Should Fix, not Must Fix.
   **Fix:** in `pd_main`'s `undelivered)` arm, when `PD_RETRY_NODES` is non-empty and `pd_undelivered` returned 0 without sleeping, call `pd_backoff` and sleep `PD_V` before `pd_walk current`. Or, if skipping the backoff is intended, extend the deviation bullet to say the infra-held node goes out with the undelivered set's own backoff (none on strike 1).

## Nice to Have

1. **Attempt counts reset when `pd_drive` restarts, so a PAUSE or STOP between retries allows more than three attempts in all** — `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_drive`) — "unset ${!PD_ATTEMPTS_@} ${!PD_ATTEMPT_LOG_@} ${!PD_EXHAUSTED_@} ${!PD_AGENT_@}"
   A retry set passes through the per-set safety contract. If a PAUSE or STOP is present before the retry goes out, the run stops, and the resumed `pd_drive` starts the held node again at attempt 1. The user asked for "at most 3 attempts per node in total". Only an operator-initiated stop opens the gap, so no unattended decision turns on it.
   **Fix:** either state in the library header's rule sentence that the count is per `pd_drive` call, or add a one-line deviation saying so.

2. **The suite header's rule sentence in `cli/test/planning-driver-walk.test.mjs` now runs past the file's wrap width** — `cli/test/planning-driver-walk.test.mjs` (file header) — "attempts — is held as `error` while its siblings run to their end, then parks.** Each case is graded on `git log`, the ledger, the"
   **Fix:** re-wrap the paragraph to the file's existing column width.
