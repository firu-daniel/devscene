### Task 5 — Test the plain round in the static checks, references and transitions

**Goal:** Pin, at the engine, that a round without `writer` gets only the round rules, and that a review loop still gets every clause. Each clause is planted both ways.

**Depends on:**
- Task 3, which scopes the clauses. On every round: check 8 *gate is a dispatch node*, and check 9 (i) and (iii). Only on a round declaring `writer`: check 8 *writer is a dispatch node*, and check 9 (ii), (iv) and (v). Only when the graph declares a review loop: check 8's *fail verdict with no increment is a gate of exactly one round*. Every reason string is unchanged. Task 3 also has `references.py` report `writer` and `counter` only when present.
- Task 2, after which `_dispatch` gives a plain round's gate its round's number and `converging` `None`, and gives a round number only to a review loop's writer.
- Task 4, which makes a writer-less round buildable and adds `graphscene/tests/fixtures/flow_graph/valid_plain_round.json`: round `checks` with gates `lint` and `license` and no `writer`, entered from the non-writer `intake`, which also routes `rejected` (verdict fail) to the terminal `discarded` with no increment.

**Where this task stops.** This task tests the engine modules only, through `build_flow_graph` and the engine functions. Loading through the public `load_graph` and walking through `Walker` is Task 6's.

### Targets

- `graphscene/tests/engine/test_static_check.py`
- `graphscene/tests/engine/test_references.py`
- `graphscene/tests/engine/test_transitions.py`

**Work:**

- [ ] `test_static_check.py`:
  - Add a `_plain_round(**overrides)` helper: `_round()` without `writer`, `counter` and `convergingFrom`.
  - Add planted cases. Each asserts the exact list returned, with reason strings hand-written from the f-strings in `graphscene/src/graphscene/engine/static_check.py`:
    - `_base()` with `r` a plain round returns `[]`, although `a` routes into `r` and is no writer, which is clause (v) on a review loop.
    - `_base()` with `r` plain and `a` also routing `rejected` → `t` with no increment returns `[]`. The same graph with `r` a review loop is the rewritten `test_gate_in_round_a_gate_in_zero_rounds_is_named` below.
    - A plain round whose gate declares no pass outcome returns `[]`; clause (ii) is covered on a review loop by the existing `test_round_fan_out_ii_…`.
    - A plain round whose gate routes `approved` elsewhere still returns its clause (i) violation.
    - A plain round whose gate skips elsewhere still returns its clause (iii) violation.
    - A plain round naming the terminal as a gate still returns check 8's non-dispatch-gate violation.
  - Add a case asserting `static_violations(build_flow_graph(_load("valid_plain_round.json"))) == []`.
  - Rewrite the one existing case whose expected list moves under Task 3's scoping, `test_gate_in_round_a_gate_in_zero_rounds_is_named`. Its graph today (`a` routing `done` and `rejected` to terminal `t`, no round) declares no review loop, so after Task 3 it returns `[]`.
    - The rewritten case plants a review loop: `_base()` with `nodes["a"] = _dispatch({"done": {"to": "r"}, "rejected": {"to": "t"}})`. `a` stays `r`'s writer and reachable from start, `rejected` → `t` closes no cycle, and `a`'s routes into the round are only `done`. It asserts exactly `[Violation("nodes.a", "gate-in-round: node 'a' routes a fail verdict with no increment and is a gate of 0 round nodes, not exactly one")]`, the same expected list as today.
    - Add the case's old graph as its own case, `test_gate_in_round_a_graph_declaring_no_review_loop_runs_no_graph_wide_clause`, which builds the unchanged no-round graph and asserts `[]`.
    - Every other existing case and `_NEGATIVES` stays unchanged. This rewrite is the only exception. The other no-round cases (`test_gate_in_round_an_incrementing_fail_edge_is_not_selected`, the `reaches_terminal` and `fail_cycle_capped` ones) expect no `gate-in-round` violation today, so Task 3's scoping does not move them.
  - Restate the header docstring to say that the review-loop clauses are planted on both kinds of round, and that check 8's graph-wide clause is planted on a graph with and a graph without a review loop.
- [ ] `test_references.py`:
  - A planted plain round, with no `writer` and no `counter`, returns no `node-known` or `counter-known` violation for the round.
  - A review loop whose `writer` names no node still returns its `node-known` violation at `nodes.<round>.writer`, if no existing case already asserts it; reuse an existing one if it does.
- [ ] `test_transitions.py`:
  - On a planted graph whose round declares no `writer`, arriving at the round dispatches each gate with `round_number=0` and `converging=None`.
  - The dispatch node that routes into that round is dispatched with `round_number=None`.
  - The existing writer and converging cases stay unchanged. Build the planted graph through the file's own helpers and `build_flow_graph`.

**Verification:**

- `bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py` passes.
- `bash scripts/python-service.sh --package graphscene test tests/engine/test_references.py` passes.
- `bash scripts/python-service.sh --package graphscene test tests/engine/test_transitions.py` passes.
- Each new expected `Violation` is a literal written from the code's f-string and the planted ids, never captured from a run.
