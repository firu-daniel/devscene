`feat_graphscene_execution_rules` moves the planning driver's execution rules into the GraphScene engine so every graph gets them. Part of #376.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

As the pilot built them (`docs/flow-graph-walker.md` → `## 5. The two drivers` → `### How each runs a parallel round` and `### The return schema, the graph's outcomes, and the \`init\` check`; #376 holds the same material but an unattended run cannot open it):

- The safety contract per dispatch set (STOP, PAUSE, cap over the whole set).
- Finish-order recording.
- The join with a held failure.
- The per-node retry for infrastructure failures, with agent-reported ones parking at once.
- The undelivered breaker as a separate run-level rule.
- The park as an interrupt.
- One observation row per launched session. _Since #421's rescope (2026-11-25):_ the engine counts the launches, and the row's usage figures come from the host, through the usage sink its executor writes to. `NodeResult` carries no usage.

`planning-driver-control.test.mjs` shows the cases to reproduce with the stub executor.

- **Which of those cases are the engine's.** Retry, the join with a held failure, the undelivered breaker, the dispatch cap, and STOP and PAUSE checked before a set are rules over results and counts. The stub can drive all of them. The escalation-resume cases (a)–(d) commit the round's files and read the ledger, which is host work (`devscene-flow-host/`) or #423's entry and resume hook, not GraphScene's.
- **The limits are the host's to pass, with GraphScene defaults.** The pilot's values are the attempts per node (3, `PD_MAX_ATTEMPTS`), the backoff before a retry (`PD_BACKOFF_SECS`), the dispatch cap (`MAX_TOTAL_DISPATCHES`, read from the plugin core) and the consecutive undelivered sets before a pause (3). Under the decision below that the harness's meanings come from the host, these are values the host supplies, never constants the engine hard-codes for the harness.
- **A timeout is `infra`.** The engine owns the stall deadline (#420 as merged; #484 acts on it). The pilot records a stall kill as an infrastructure failure, retried for that node. #484 says which class a timeout is recorded as is this branch's to settle.

- **The rules are the engine's, and the harness's meanings come from the host** _Decided 2026-11-22 with #418._ The engine applies STOP, PAUSE, the cap, retry, the breaker and the park the same way for every host. Where the harness's STOP and PAUSE markers live, what `.dispatch_counter` counts and where an observation row is written are supplied by `devscene-flow-host/`, DevScene's GraphScene host package (#451, renamed by #455), never read by GraphScene.

- **The failure classes as #487 defines them** _Decided 2026-11-25._ `graphscene/src/graphscene/model/execution.py` is the source:
  - `infra`: a crash, a session that ended in error, a stall, or a return that is absent, unparsable or fails its schema. Retried for that node alone, a bounded number of times.
  - `agent`: the agent reported the failure. Recorded at once, never retried.
  - `undelivered`: nothing readable was delivered at all, such as no result or the provider being unavailable. Re-dispatched without counting as one of the node's attempts. Repeated across sets, it trips the run-level breaker.

  This matches the pilot's classes. #420 first described a schema-failing return as `undelivered`, and #487 corrected that.
- **The public surface and its tests are this branch's callers.** Nothing runs these rules until #484's loop applies them. That is expected for this milestone and is not un-wired code.
- **Tested on the stub, not on a real executor** _Decided 2026-11-25._ #421 is now the harness's `claude` executor in `devscene-flow-host/`, and GraphScene ships no provider's executor. These rules depend on #420 alone, and #421 is no longer a prerequisite.
- **The rules, not the loop** _Decided 2026-11-25 with #420._ This branch ships the rules as engine components, tested against #420's stub executor. #484 then applies them in the engine-driven run loop. The rules are written against #420's `asyncio` interface.

## Depends on

#420, #487
