### 3. A node that fails for an infrastructure reason parks planning at once instead of being retried

**File:** `cli/templates/scripts/lib/planning-driver-lib.sh` (`pd_reap_one`) — "--outcome error) ;;"

**Problem.** Every `kind=error` from `pnl_reap`, and every stall kill (`pd_reap_one` sets `kind=error`, `reason=stalled`), is recorded at once with `flow-walker.sh next --node <node> --outcome error`. The graph routes `error` to `<escalate>` (`cli/templates/scripts/flows/task_plan_writing.graph.json`), the walker holds it to the join, and `pd_escalate_park` parks the run. The only retry today is for `undelivered`: no `result` event, or an API 500/503/529/Overloaded (`pd_undelivered`). So any of the following parks planning the first time it happens:

- one stall kill;
- a session that ended `error_max_turns` or with `is_error`;
- an `init` that did not come up;
- a result with no decision object.

The orchestrated path's `Agent` tool would often have recovered from these. `PNL_REAP_JQ` in `cli/templates/scripts/lib/planning-node-lib.sh` produces the reasons: `"the agent did not resolve: no init event"`, `"the session ended as <subtype>[ with is_error]"` and `"the result carries no decision object"`.

**Required behaviour** (the user's):

- **Split the `error` classes.**
  - **Agent-reported** `error` and `blocker` are the decision object's own outcome (`kind=returned`, outcome `error`/`blocker`). They keep parking at once, unchanged.
  - **Infrastructure-class** failures are retried: a stall kill, a session that ended not `success` or with `is_error`, a missing `init` event, and a missing decision object.
  - Every other `kind=error` reason `PNL_REAP_JQ` gives — tools that do not match the `init` event, an undeclared outcome, `FAIL`/`PASS` without `findings_file`, questions with a blank return — is not in the user's list. It keeps parking at once.
- **A retry re-dispatches only the failed node, never its siblings.** Siblings that finished keep their recorded outcomes, and the walker's `current` names the gates still due. `flow-walker.sh` → STATE: while a set is pending, `current` re-prints "the blocks of the gates with no recorded outcome".
- **At most 3 attempts per node in total**, the first plus two retries, with a backoff between them. While attempts remain, the user sees no park, pause or notification: only `[plan-drive]` log lines and one observations entry per retry.
- **When the attempts run out, the run parks once.** The park's question names the node, the agent, and how each attempt ended.
- **The existing three-strike undelivered self-pause stays as it is**, with a manual RESUME. Add no automatic resume.
- **Record the per-node attempt count** in the observations file's session table.

**Fix.**

1. **Classify in one place.** Have `pnl_reap` print the class with the verdict so the driver never parses reason prose. For example, add a `class=infra|agent` line, or a distinct reason key set in `PNL_REAP_JQ` on exactly the three infra branches: no `init`, non-success/`is_error`, no decision object. In `pd_reap_one`, `stalled=yes` is infra too. Document the new line in `pnl_reap`'s header (`STATUSES`/printed-lines comment) and in the library's header rule ("a node's result is a declared outcome, `error` or `undelivered`") if the classes change that sentence.
2. **Hold, don't record, an infra failure while attempts remain.** In `pd_reap_one`, an infra-class failure:
   - increments a per-node attempt count (for example `PD_ATTEMPTS_<node>`);
   - appends `attempt <k>: <reason>` to a per-node history (for example `PD_ATTEMPT_LOG_<node>`);
   - writes one `[plan-drive]` log line and one `pd_observe flow-efficiency` entry naming the node, agent, attempt k of 3 and the reason;
   - when attempts remain, does **not** call `pd_walk next` and marks the set for a retry (for example `PD_RETRY_NODES`).

   When the third attempt fails, record `--outcome error` exactly as today, so the walker's join prints the held `<escalate>` once all siblings have finished. Reset a node's attempt count and history when it records an outcome, so a later round starts at attempt 1.
3. **Re-dispatch the failed node alone.**
   - After the set's reap loop, when `PD_RETRY_NODES` is non-empty, return a new `PD_SET_RESULT=retry` from `pd_run_set`. A set fault (`PD_SET_FAULT`) still takes precedence.
   - In `pd_main`, handle `retry` like this:
     - sleep the backoff, for example `PD_BACKOFF_SECS`, defaulted and capped as `pd_undelivered` does, or a separate `PD_RETRY_BACKOFF_SECS` documented in the `GLOBALS` header;
     - then `pd_walk current` and continue the loop, so the next `pd_act` / `pd_run_set` dispatches only the still-due blocks `current` re-prints;
     - do not count the retry toward `recovers`, and do not touch `PD_STRIKES`.
   - Apply this to a single-node dispatch (a writer) as well: `current` re-prints its dispatch block.
   - The retry passes through the same per-set safety contract (STOP, PAUSE, dispatch cap), and each retry counts as one dispatch against `MAX_TOTAL_DISPATCHES`.
   - Undelivered sessions keep their own path and strike count (`pd_undelivered`). An undelivered re-dispatch does not consume an infra attempt.
4. **The park when attempts run out.**
   - In `pd_escalate_park` / `pd_session_detail`, for a held gate whose attempts ran out, write each attempt's outcome from the per-node history, so the question names the node, the agent and how each of the three attempts ended.
   - Keep the `## Q1 — How should planning continue?` shape.
   - The park happens once, after the siblings finished, because the walker holds the `error` to the join.
5. **The session table.** In `pd_finish`, the observation `Script-driven planning node sessions …` writes `seq node agent result duration cost`. Add the attempt number per row, for example `seq node agent attempt result duration cost` with `attempt` as `k/3`, and update the header literal. Every launched session, retries included, keeps its own row.
6. **Header and docs.**
   - Amend the library header's rule ("an `error`, a `blocker` or a stall kill ends that one session, never a sibling"), and the `GLOBALS` block if a tunable is added.
   - `docs/flow-graph-walker.md` → `## 5. The two drivers` → `### How each runs a parallel round`: **Decision.** and **Cost.** (which today say a stall kill is recorded as `error` and only undelivered sessions are re-dispatched), and `### The schema-from-graph rule, and the init check` where it says no `init` is `error`.
   - `docs/watcher.md` → `### Script-driven planning (opt-in pilot)`, wherever it describes what parks or pauses the driver.
7. **Tests.** Extend the stub in `cli/test/helpers/planning-driver.mjs` with an entry mode for each infra class the cases need. It already scripts per-call-index entries and supports `no-init`, `no-result`, `undeclared` and `sleepMs`. Add, for example, `mode: 'not-success'` (a `result` with `subtype: "error_max_turns"`) and `mode: 'no-decision'`, and a stall the driver kills (a `sleepMs` past a short `PD_NODE_STALL_SECS`). Update the helper's header for the new modes. In `cli/test/planning-driver-control.test.mjs` (or `cli/test/planning-driver-walk.test.mjs`):
   - two gates of a set pass while the third stalls once and then passes on its retry. There is no park, the siblings are each dispatched once, the retried gate is dispatched twice, and planning hands off;
   - a node that fails all three attempts parks exactly once, after its siblings finished. The question names the node, the agent and the three attempts' outcomes;
   - an agent-reported `blocker` (`outcome: 'blocker'`) still parks with no retry: one dispatch of that gate.

   The existing case `a session with no init event is held as error and parks` in `cli/test/planning-driver-walk.test.mjs` scripts `no-init` on call 0 only, so under this fix it retries and passes. Change it to `no-init` on all three attempts, asserting the single park after three dispatches, or replace it with the all-attempts case above. Keep `one error in a set is held while its siblings finish, then parks once` (agent-reported `error`) and `an undeclared outcome is held as error and parks` as they are. Set the backoff to 0 in every case so no case sleeps.

- **Deviations from plan:** (cli layer dispatch)
  - Item 6's `docs/flow-graph-walker.md` and `docs/watcher.md` edits lie outside the `cli` path and are left to this unit's `general` layer dispatch. What they must describe: `pnl_reap` prints `class=infra|agent` for every `kind=error`; a stall kill or a `class=infra` error is held unrecorded and its node alone is re-dispatched after `PD_BACKOFF_SECS` (shared with the undelivered backoff, default and ceiling 60), up to `PD_MAX_ATTEMPTS` (3) attempts; only the third is recorded as `error`; the park's per-node detail then carries `- agent:` and an `- attempts:` list; the session table header is `seq node agent attempt result duration cost`.
  - Backoff: no separate `PD_RETRY_BACKOFF_SECS`; the retry reuses `PD_BACKOFF_SECS` through a new `pd_backoff` helper that `pd_undelivered` also calls, and the `GLOBALS` header says so.
  - Where one set has both an undelivered session and an infra-held one, `undelivered` takes precedence as the set result (it carries the strike count and self-pause); the infra-held node rides that re-dispatch, because `current` re-prints every unrecorded gate, and its attempt is already counted.
  - `cli/test/planning-node-lib.test.mjs` was also edited, to pin `class=` on each `pnl_reap` rule case.
  - Stall test: `drive` takes a new `{ stallSecs }` option; the case uses `stallSecs: 3` against a 10 s stub sleep.
