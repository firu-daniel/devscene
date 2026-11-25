### Task 3 — Add the per-node attempt rule `AttemptBook` in `engine/attempts.py`

**Goal:** Turn one node's `NodeResult` into its settlement, using the bounded per-node retry for infrastructure failures. A `Completed` result is recorded. An `agent` failure is recorded at once and never retried. An `infra` failure is retried for that node alone until its last attempt, and is then recorded with every attempt's reason. An `undelivered` result is re-dispatched without using up an attempt.

**Depends on:** Task 1, which declares these in `graphscene/src/graphscene/model/run_control.py`, used here exactly as follows:

- `ExecutionLimits.max_attempts: int`, validated `>= 1`;
- `NodeRecord(node: str, outcome: str, detail: str | None)`;
- `Recorded(record: NodeRecord)`;
- `Retry(node: str, attempt: int, reason: str)`, where `attempt` is the number the re-dispatch will be;
- `Redispatch(node: str, reason: str)`;
- `Settlement = Recorded | Retry | Redispatch`.

`Completed(outcome, detail)`, `Failed(failure, reason)` and `NodeResult` are `graphscene.model.execution`'s, as #487 defines them.

**Where this layer stops.** `AttemptBook` settles one result at a time. It runs nothing, sleeps no backoff and never calls the walker. Running the set, the backoff, the join order and the breaker are Task 4's `execute_set`. Recording a `NodeRecord` through `Walker.next` is the caller's, which in production is #484's loop. **The park is not built here.** A final failure becomes a `NodeRecord` with the host-named `failure_outcome`, such as the harness graph's held `error`, and the graph's binding for that outcome is what parks the walk. The public-surface entries and the README row are Task 5's.

### Targets

- `graphscene/src/graphscene/engine/attempts.py` (new)
- `graphscene/tests/engine/test_attempts.py` (new)

**Work:**

- [ ] Write the module docstring. Its *"The rule:"* paragraph states every rule in the bullets below. Its *"Deliberately not covered:"* list names whether `failure_outcome` is declared and held for the node (the walk refuses an undeclared outcome), the backoff, and persisting the book across processes.
- [ ] `class AttemptBook` keeps, per node id, the current attempt number and the infra reasons so far.
  - `attempt(self, node: str) -> int` returns the attempt the node's next run is: `1` for a node never seen, or one settled to `Recorded`.
  - `settle(self, node: str, result: NodeResult, limits: ExecutionLimits, failure_outcome: str) -> Settlement` applies, in this order:
    - `Completed(outcome, detail)` → `Recorded(NodeRecord(node, outcome, detail))`, and the node's count restarts.
    - `Failed("agent", reason)` → `Recorded(NodeRecord(node, failure_outcome, reason))` at once, whatever attempts remain, and the count restarts.
    - `Failed("undelivered", reason)` → `Redispatch(node, reason)`. The attempt number and the reasons are unchanged.
    - `Failed("infra", reason)` while the current attempt `k < max_attempts` → note `attempt k of <max>: <reason>` and return `Retry(node, k + 1, reason)`.
    - `Failed("infra", reason)` on attempt `k == max_attempts` → `Recorded(NodeRecord(node, failure_outcome, detail))`, and the count restarts. `detail` is exactly `all <max> attempts failed for an infrastructure reason` followed by one `\nattempt <i> of <max>: <reason_i>` line per attempt, in order.
- [ ] `test_attempts.py`. Its header is the *"The rule this file exists to enforce"* docstring. Every expected `Settlement` and `detail` is hand-written. Cases:
  - a completion records its outcome and detail;
  - an agent failure on attempt 1 records `failure_outcome` with no retry;
  - infra on attempts 1 and 2 returns `Retry(node, 2, …)` and then `Retry(node, 3, …)`;
  - infra on attempt 3 records the three-line detail;
  - an undelivered result between two infra failures leaves the attempt number unchanged;
  - after a completion, a node's next infra failure is attempt 1 again;
  - two nodes' counts are independent;
  - `max_attempts=1` records on the first infra failure.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_attempts.py` passes.
- An `agent` failure never yields `Retry`, and an `undelivered` one never changes `attempt(node)`. Both are asserted in the suite rather than inferred.
