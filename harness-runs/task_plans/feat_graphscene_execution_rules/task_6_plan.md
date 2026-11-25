### Task 6 — Reproduce the pilot's engine-owned control cases through the public surface

**Goal:** Show that a caller who imports only from `graphscene` can apply the execution rules end to end, and that they reproduce the cases in `cli/test/planning-driver-control.test.mjs` that are the engine's — the rules over results and counts — on the `StubExecutor`. The park is shown going through a real `Walker` join on a committed graph.

**Depends on:** Task 5, which makes these public from `graphscene`: `execute_set`, `AttemptBook`, `UndeliveredBreaker`, `clear_set`, `ExecutionLimits`, `Halt`, `NodeRecord`, `SetResult`, `Launch`, `RunSignals`, `DispatchCounter` and `LaunchSink`, beside the existing `StubExecutor`, `ScriptedOutcome`, `ScriptedFailure`, `ScriptedStall`, `Walker`, `load_graph_file` and the walk-action types. The contracts used are those of Tasks 1–4, restated here:

- **The call.** `await execute_set(dispatches, executor, *, signals, counter, sink, book, breaker, limits, failure_outcome) -> SetResult(records, halt)`.
- **The limits.** `limits` is `ExecutionLimits(max_attempts=3, backoff_seconds=60.0, dispatch_cap=None, stall_seconds=None)`, which carries no undelivered-set limit. That limit is supplied only at `UndeliveredBreaker(limit=3)` construction, and the trip is the breaker's (`strikes >= limit`).
- **Record order.** `records` lists the outcomes in finish order, then the held final failures in finish order.
- **Final failures.** A final failure is `NodeRecord(node, failure_outcome, detail)`. After exhausted infra attempts, `detail` is `all <max> attempts failed for an infrastructure reason` followed by one `\nattempt <i> of <max>: <reason>` line per attempt. After an agent failure, `detail` is the reason.
- **Halts.** `halt` is `Halt("stop" | "pause" | "cap" | "undelivered", detail)` or `None`.
- **Stalls.** A stall under `stall_seconds` is `infra` with reason `stalled: no result within <stall_seconds>s`.
- **Launch rows.** There is one `Launch(seq, node, agent, attempt, max_attempts, result)` per launched session.

**Where this layer stops.** This is a test suite. It changes no source file. The escalation-resume cases (a)–(d), the `<ask>` questions park, round files and commits are the host's or #423's, and are named in this suite's *"Deliberately not covered"* rather than reproduced.

### Targets

- `graphscene/tests/facade/test_execution_rules.py` (new)

**Work:**

- [ ] Write the module docstring. It opens with *"The rule this file exists to enforce"*. It states that the suite is a caller importing only from `graphscene`, as `.claude/context/graphscene.md` → `## Tests` requires of a facade test (*"A facade test imports the public names from `graphscene`, as a caller does"*). It names `cli/test/planning-driver-control.test.mjs` as the source of the cases, and states that every expected literal is hand-written. Its *"Deliberately not covered:"* list names the escalation-resume cases (a)–(d), the `<ask>` park, round-file refusals and commits, each as the host's or #423's.
- [ ] Add in-test structural classes, each a plain class with no mocking aid:
  - `Signals`, whose STOP and PAUSE answers can be flipped after a set number of calls;
  - `Counter`, holding a plain integer total;
  - `Rows`, a list of `Launch`.
- [ ] Add one case per pilot case the engine owns, each named after it and run with `backoff_seconds=0`:
  - *STOP present before a set launches none of it*: `Halt("stop", …)`, `StubExecutor.started == ()`.
  - *STOP raised while a set runs lets the set finish, and launches nothing after*.
  - *PAUSE raised mid-set is honoured at the join*: the set's records are returned, and the next `execute_set` halts with `"pause"`.
  - *one gate undelivered three times running … self-pauses*: with `breaker=UndeliveredBreaker()`, `Halt("undelivered", "3 consecutive sets delivered nothing")`.
  - *a gate stalled once is re-dispatched alone and passes; its siblings run once*: uses `ScriptedStall` and `stall_seconds`.
  - *a return that fails its schema is retried as infrastructure, not parked*: scripted as `ScriptedFailure("infra", …)`.
  - *an agent-reported blocker parks with no retry*.
  - *the dispatch cap halts before a set that would pass it*.
  - *a session table names every session*: the `Rows` sink holds one row per launch, retries included.
- [ ] Add the park-through-the-walk case, *a gate failing all three attempts parks once, after its siblings, naming every attempt*:
  - Load `graphscene/tests/fixtures/flow_graph/valid_generic.json` with `load_graph_file`, reading the path from `__file__` as the existing facade suites do. Walk it with an in-test `PredicateHost` answering `stage_disabled=False`.
  - Run `draft` through `execute_set` to `done` and record it through `Walker.next`. Then run `review_round`'s set, the gate `edit_check`, whose three scripted `infra` failures exhaust its attempts, with `failure_outcome="crashed"`, the fixture's held outcome.
  - Record each returned `NodeRecord` with `Walker.next(outcome, node, detail)`. Assert the walk returns the `Stop` that the fixture binds `crashed` to (`<halt>`, reason `crash`). This shows the park is the graph's own binding.
- [ ] Keep the suite inside the boundary that `.claude/context/graphscene.md` → `## Tests` sets. It plants no file in the checkout, reads the fixture read-only, and asserts no duration.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/facade/test_execution_rules.py` passes.
- The file imports only `graphscene`, the standard library and `pytest`: no `graphscene.engine`, `graphscene.model` or `graphscene.adapters` submodule.
