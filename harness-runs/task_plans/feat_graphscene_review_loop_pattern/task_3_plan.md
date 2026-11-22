### Task 3 — Split checks 8 and 9 into round rules and review-loop rules

**Goal:** Check 8 (`gate-in-round`) and check 9 (`round-fan-out`) keep every clause and every reason string. What changes is *where* each clause runs. The engine's round rules run on every round. The review-loop rules run only on a round that declares `writer`, and check 8's graph-wide clause runs only on a graph that declares at least one review loop. The reference check reports `writer` and `counter` only where they are present.

**Depends on:** Task 1, which provides, in `graphscene/src/graphscene/engine/review_loop.py`:
- `review_loop(node: RoundNode) -> ReviewLoop | None`, `None` for a round declaring no `writer`;
- `review_loops(graph: FlowGraph) -> tuple[ReviewLoop, ...]`;
- `ReviewLoop.writer: str`.

**Where this task stops.** After this task, neither module reads `RoundNode.writer`, `.counter` or `.converging_from` as a non-optional value. Task 4 makes those fields `| None` and edits neither file. Planting a writer-less round in tests is Task 5's (`graphscene/tests/engine/test_static_check.py`, `graphscene/tests/engine/test_references.py`), because one can only be built after Task 4. On every graph that loads today this task returns the identical list. One existing planted case changes: `test_gate_in_round_a_gate_in_zero_rounds_is_named`, whose graph declares no round; Task 5 rewrites it. This task does not edit `graphscene/tests/engine/test_static_check.py`.

**The split, as the story index's `## Context` decides it** (clause labels as `graphscene/tests/engine/test_static_check.py` names them):
- **Round rules, every round:**
  - check 8, *a gate is a dispatch node* (`nodes.<round>.gates[i]`);
  - check 9 (i), *a gate's verdict outcome routes to the round as a route edge*;
  - check 9 (iii), *a gate's skip goes to the round*.
- **Review-loop rules, only when `review_loop(round)` is not `None`:**
  - check 8, *the writer is a dispatch node* (`nodes.<round>.writer`);
  - check 9 (ii), *the gate routes an outcome declaring each verdict*;
  - check 9 (iv), *the writer routes an outcome to the round*;
  - check 9 (v), *the stray-edge clause* (`_stray_edges`).
- **Graph-wide, only when `review_loops(graph)` is non-empty:** check 8, *a dispatch node routing a fail verdict with no increment is a gate of exactly one round* (`nodes.<node>`).

### Targets

- `graphscene/src/graphscene/engine/static_check.py`
- `graphscene/src/graphscene/engine/references.py`

**Work:**

- [ ] `static_check.py` → `_gate_in_round`:
  - The dispatch-node clause runs only when `review_loops(graph)` is non-empty.
  - The non-dispatch-gate clause runs for every round.
  - The writer clause runs only when `review_loop(node)` returns a loop, and reads `loop.writer` instead of `node.writer`.
  - Every `Violation` path and reason string stays as it is today, character for character.
- [ ] `static_check.py` → `_round_fan_out`, `_gate_clauses`, `_admitted`, `_stray_edges`:
  - Compute `loop = review_loop(r)` once per round.
  - `_gate_clauses` always emits clauses (i) and (iii), and emits clause (ii) only when `loop` is not `None`. Pass that as a `bool` parameter, or pass the loop itself.
  - The writer clause (iv) and `_stray_edges` (v) run only when `loop` is not `None`, and read `loop.writer`.
  - The report order the docstring states holds unchanged on a review loop: each gate's clauses in `gates` order, then the writer, then the other edges.
- [ ] `static_check.py`, module docstring:
  - Restate **"The rule:"** to name the two kinds: checks 8 and 9's round rules on every round, and their review-loop rules on a round `graphscene.engine.review_loop` reports as a review loop. Name check 8's graph-wide clause as one that runs only when the graph declares a review loop.
  - Keep the check order, the report order and *"Every reason opens with its check id"*.
- [ ] `references.py` → `_round`:
  - Report `writer` as `node-known` only when it is present. A private `_opt_node_known(path: str, name: str | None, graph: FlowGraph) -> list[Violation]` returns `[]` for `None`, and is typed so that it type-checks before and after Task 4.
  - `counter` keeps going through `_counter_known`, which already takes `str | None`.
  - The module docstring's order sentence becomes *"`gates[i]`, `writer` and `counter` when present, `plan[i]`, `revisionNote`"*.

**Verification:**

- `git grep -nE "r\.writer|node\.writer|\.converging_from|gate_of\.counter" -- graphscene/src/graphscene/engine/static_check.py graphscene/src/graphscene/engine/references.py` prints only the `references.py` line that passes `node.writer` into `_opt_node_known`.
- Reading `static_negative_gate_in_round.json` and `static_negative_round_fan_out.json` against the new code: each still yields exactly the violation `graphscene/tests/engine/test_static_check.py` → `_NEGATIVES` lists for it, because `valid_generic.json`'s `review_round` declares `writer`.
- `git diff` shows no change to any reason f-string's text in `static_check.py`.
