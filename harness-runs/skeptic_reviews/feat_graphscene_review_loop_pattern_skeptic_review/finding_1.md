### 1. On a graph with no review loop, an uncapped fail cycle through a plain round's fan-out passes every static check and walks forever

**File:** `graphscene/src/graphscene/engine/static_check.py` (`_fail_cycle_capped`) — "if node_id in _reached(graph, [edge.to], _uncapped):"; the gating that exposes it is `_gate_in_round` — "if not (has_loops and _routes_uncapped_fail(graph, node)):"
**Class:** Wrong behaviour
**Failure:** If a graph that declares no review loop routes a non-gate dispatch node's fail verdict, with no increment, into a plain round whose gate's held outcome routes back to that node, then `load_graph` accepts it and `Walker` loops through it with no counter and no cap.

**The justification that does not hold.** The story index justifies gating check 8's graph-wide clause on "the graph declares at least one review loop" with: *"A graph without one may route a fail verdict anywhere, and check 3 (`fail-cycle-capped`) still refuses an uncapped fail cycle."* (`harness-runs/story_plans/feat_graphscene_review_loop_pattern_story_plan.md` → `## Context`). Check 3 does not refuse every uncapped fail cycle. Its successor relation F, `_uncapped`, is documented as *"uncapped route edges and skip edges"*: it leaves out a round's fan-out to its `gates`. That omission is deliberate, because otherwise every gate's fail verdict edge into its own round would be reported as a cycle (`round → fan-out → gate`), and `test_fail_cycle_capped_a_cycle_closed_only_through_fan_out_is_not_reported` pins it. The omission is safe only while check 8's graph-wide clause and round rule 9 (i) together guarantee that **every** uncapped fail verdict edge from a dispatch node is a gate's edge into its own round, where the round's join breaks the cycle. Before this branch that clause ran on every graph. On this branch it runs only when `review_loops(graph)` is non-empty, and clause 9 (v), which refused a non-gate edge into a round, runs only on a review loop. So on a graph with no review loop, a non-gate node's uncapped fail edge can enter a round, cross its fan-out (which F does not walk), and come back through a gate's non-verdict edge. No check sees the cycle. Lesson `## Trust checks` in `harness-runs/lessons.md` ("Never drop a protection because another route "can already" reach the same target until that route is measured") is the rule the story's scope register row 9 claims to comply with. This is the measurement it skipped.

**Why it is reachable.** A plain round is meant to be opened from any node (`test_round_fan_out_v_a_plain_round_admits_a_route_from_a_node_that_is_no_writer`). A gate's held outcome may be a route edge, and the held join follows the first held gate's edge (`graphscene/src/graphscene/engine/rounds.py` → `record_gate`, "return follow_edge(graph, host, draft, first.gate, held_edge, held=held)"). Nothing increments on that path.

**Proof (executed).** Probe `harness-runs/scratch/skeptic_plain_round_fail_cycle.py`, run with `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_plain_round_fail_cycle.py <repo_root>`. It starts from `valid_plain_round.json` and makes three edits: `intake.outcomes.rejected` (verdict fail) becomes `{"to": "checks"}`, gate `lint`'s held `crashed` becomes `{"to": "intake"}`, and the now-unreachable `discarded` is dropped.
- `load_graph` returns the graph: `LOADED`.
- The walk then repeats `Dispatch intake → (rejected) DispatchSet checks → (lint crashed) Wait → (license accepted) Dispatch intake` four times out of four, with `counters {}`. No counter exists to cap it.
- The same graph with `checks` opted in as a review loop is refused at stage `static` with `gate-in-round: node 'intake' routes a fail verdict with no increment and is a gate of 0 round nodes, not exactly one`, plus two `round-fan-out` (v) violations. That is exactly the protection the gating removed from plain-round graphs.

Second probe `harness-runs/scratch/skeptic_planted_case.py`, run the same way. Under today's code, the planted test graph below returns `[]` from `static_violations`. Under the fix below it returns exactly the one violation the test expects. Every existing case in `graphscene/tests/engine/test_static_check.py` still passes under the fix. A third probe, `harness-runs/scratch/skeptic_check3_fanout.py`, shows that the fix adds no violation to `valid_generic.json`, `valid_plain_round.json` or `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, and leaves the `fail-cycle-capped` result of every `static_negative_*.json` fixture unchanged.

**Fix.** Make check 3 walk a round's fan-out for every fail edge except a gate's verdict edge into its own round. That keeps the story's aim, a plain-round graph may still route a fail verdict anywhere that does not cycle, and keeps every reason string byte for byte.

1. In `graphscene/src/graphscene/engine/static_check.py`, add after `_uncapped`:

```python
def _uncapped_with_fan_out(node: Node) -> list[str]:
    """`_uncapped`, plus a round node's fan-out to each of its `gates`."""
    targets = _uncapped(node)
    if isinstance(node, RoundNode):
        targets.extend(node.gates)
    return targets
```

2. In `_fail_cycle_capped`, replace the line `            if node_id in _reached(graph, [edge.to], _uncapped):` with:

```python
            target = graph.nodes.get(edge.to)
            own_round = isinstance(target, RoundNode) and node_id in target.gates
            successors = _uncapped if own_round else _uncapped_with_fan_out
            if node_id in _reached(graph, [edge.to], successors):
```

3. In the module docstring, after the sentence ending "a round node's fan-out to each of its `gates`.", insert: "Check 3 walks F, a node's uncapped route edges and its skips; for a fail edge that is not a gate's edge into its own round, F also walks a round node's fan-out to its `gates`, since only that round's join breaks a cycle through its fan-out."

4. In `graphscene/tests/engine/test_static_check.py`, add after `test_fail_cycle_capped_a_cycle_closed_only_through_a_resume_is_not_reported`:

```python
def test_fail_cycle_capped_a_cycle_through_a_plain_rounds_fan_out_is_named() -> None:
    # `a` is no gate; it rejects into plain round `r` with no increment, and gate `g`'s held
    # outcome routes back to `a`, so the cycle closes through `r`'s fan-out.
    nodes = _base()
    nodes["a"] = _dispatch({"done": {"to": "r"}, "rejected": {"to": "r"}})
    nodes["g"] = _gate(
        outcomes={"approved": {"to": "r"}, "rejected": {"to": "r"}, "crashed": {"to": "a"}}
    )
    nodes["r"] = _plain_round()
    assert _check(nodes) == [
        Violation(
            "nodes.a.outcomes.rejected",
            "fail-cycle-capped: outcome 'rejected' routes 'a' -> 'r' with no increment, and 'r' "
            "reaches 'a' again",
        )
    ]
```

5. In the same file's module docstring, append to the paragraph ending "where it does not run." the sentence: "A fail cycle closed through a plain round's fan-out is planted on a graph declaring no review loop, where check 3 names it."

This fix edits one source module and the one test file that tests it, so run only that file, from the repository root:

```
bash scripts/python-service.sh --package graphscene test tests/engine/test_static_check.py
```
