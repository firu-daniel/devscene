### 1. `static_check.py` says each check reports nodes in key order, but `round-fan-out` does not

**File:** `graphscene/src/graphscene/engine/static_check.py` (module docstring) — "Each check reports nodes in key order, and every"
**Also:** `graphscene/tests/engine/test_static_check.py` (module docstring) — "each reporting nodes in key order with a reason opening"

The module's `The rule:` paragraph says every one of the five graph checks reports nodes in key order. Checks 1, 2, 3 and 8 do, because each one loops over `graph.nodes.items()` and emits as it goes. Check 9 (`_round_fan_out`) does not. For each round node it emits:

1. the gate clauses (`_gate_clauses`), in the round's `gates` order;
2. the writer clause;
3. the stray edges and skips (`_stray_edges`), by source node in key order.

So a stray edge from a node keyed before a gate is reported after that gate's clause.

Probe (run with `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/branch_review_static_probe3.py`): take `valid_generic.json` and add a dispatch node `aaa` as the first node. `aaa` routes `done` to `review_round`. Then route `edit_check`'s `approved` to `published`. Two `round-fan-out` violations come back in this order:

```
nodes.edit_check.outcomes.approved: round-fan-out: gate 'edit_check' of round 'review_round' does not route outcome 'approved' to the round
nodes.aaa.outcomes.done: round-fan-out: round 'review_round' is targeted by 'aaa' outcome 'done', which is neither a verdict edge of one of its gates nor an edge of its writer
```

`aaa` is first in key order but is reported second. The test file's header says the same false thing, and no case in that file has two check-9 violations that would show the order.

This is a docstring that misstates the order, not wrong output. No caller depends on the order yet, which is why this is a Should Fix and not a Must Fix. It still needs fixing: the docstring is the rule a reader and the cutover (#419) will take as the contract.

**Fix:** state the order the code actually produces. Do not change the code.

In `graphscene/src/graphscene/engine/static_check.py`, in the module docstring, replace:

```
ids `scripts/check-flow-graph.sh` gives them. Each check reports nodes in key order, and every
reason opens with its check id. The walked edge set W is: …
```

with:

```
ids `scripts/check-flow-graph.sh` gives them. Checks 1, 2, 3 and 8 report nodes in key order;
check 9 reports round by round, rounds in key order, and within a round each gate's clauses in
`gates` order, then the writer, then the other edges and skips that target the round, by source
node in key order. Every reason opens with its check id. The walked edge set W is: …
```

Keep the rest of the sentence that follows ("a `RouteEdge`'s `to`, …") as it is, and re-wrap the lines to the 100-column limit.

In `graphscene/tests/engine/test_static_check.py`, in the module docstring, replace:

```
and 9 (`round-fan-out`), in that order, each reporting nodes in key order with a reason opening
with its check id.
```

with:

```
and 9 (`round-fan-out`), in that order and in the report order `graphscene.engine.static_check`
states, each reason opening with its check id.
```

Then run the one test file this fix edits, from the repository root:

```
bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py
```
