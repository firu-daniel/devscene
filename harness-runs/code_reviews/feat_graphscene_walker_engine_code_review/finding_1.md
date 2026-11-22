### 1. A gate skipped on an earlier arrival keeps its `skipped` entry after it is dispatched, so a cap stop's `round_counts` drops a gate that ran

**File:** `graphscene/src/graphscene/engine/transitions.py` (`_taken_skip`) — "draft.skipped[node.id] = entry.when"
**Class:** Wrong behaviour
**Failure:** If a host answers `stage_disabled` true for gate `g1` when round 0 opens and false when round 1 opens, and the round's fail edge then reaches its cap, then the `Stop` the walker returns carries `round_counts=('g2',)` although `g1` was dispatched and recorded `rejected` in round 1.

`_taken_skip` writes `draft.skipped[node.id]` when a skip entry holds, and never removes it when, on a later arrival, no entry holds. `WalkDraft.skipped` is carried from one step to the next through `WalkState.skipped`, so after the first skip the entry stays for the rest of the walk. `take_binding` then filters a stop's `round_counts` on it: `if n not in draft.skipped or graph.vocabulary.predicates[draft.skipped[n]].in_round_counts`. As a result, a gate whose predicate has `in_round_counts` false is dropped from every later cap stop, even in rounds where it was dispatched.

This contradicts the branch's own contract. Skips are answered by the host on every arrival and never cached (`engine/transitions.py` module docstring: *"on every arrival and never from a cache"*; story index `## Context` → *"Skips are answered by the host on every arrival. The answer is never cached"*). `model/walk_state.py` says `skipped` exists so that *"a cap's `round_counts` can drop a node whose predicate has `in_round_counts` false"*. That means a node the predicate skipped, not a node it skipped at some earlier point. The stale entry acts as a cache of an old answer.

**Confirmed by a probe.** A file under `harness-runs/scratch/` built a graph with a writer `draft`, a round `rr` over gates `g1` (skip `stage_disabled` → `rr`, `inRoundCounts: false`) and `g2`, a `rejected` edge with `increment: attempt` and an `onCap` stop with `roundCounts: ["g1", "g2"]`, and `attempt` capped at 2. It ran with `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/walker_stale_skip_probe.py`. It printed round 1's set dispatching both `g1` and `g2`, both recorded `rejected`, and then `Stop(... round_counts=('g2',) ...)` with `skipped {'g1': 'stage_disabled'}`.

**Fix:**

1. In `_taken_skip`, clear the node's entry when no skip entry holds on this arrival:

   ```python
   def _taken_skip(
       graph: FlowGraph, host: PredicateHost, draft: WalkDraft, node: DispatchNode
   ) -> SkipEntry | Refused | None:
       for entry in node.skip or ():
           answer = host.answer(entry.when, node.id)
           if answer is None:
               return Refused(f"the host cannot answer predicate '{entry.when}' for node '{node.id}'")
           if answer:
               _record_report(draft, entry.report)
               draft.passed.append(
                   SkipPassage(node.id, graph.vocabulary.predicates[entry.when].records)
               )
               draft.skipped[node.id] = entry.when
               return entry
       draft.skipped.pop(node.id, None)
       return None
   ```

   A `Refused` return leaves the entry as it was, which is correct: a refused step's draft is discarded.

2. Bring the two docstrings into line with the change:
   - In `graphscene/src/graphscene/engine/transitions.py`'s module docstring, the `arrive` bullet now reads *"an entry that holds records its report, a `SkipPassage` and the node's `skipped` entry"*. Append *"; an arrival where no entry holds clears that entry"*.
   - In `graphscene/src/graphscene/model/walk_state.py`'s module docstring, change the `skipped` bullet to *"`skipped` is node → the predicate name that skipped it on its latest arrival, so a cap's `round_counts` can drop a node whose predicate has `in_round_counts` false."*

3. Add a case to `graphscene/tests/engine/test_transitions.py`:

   ```python
   def test_a_gate_dispatched_after_an_earlier_skip_is_counted_again() -> None:
       graph = _article()
       draft = WalkDraft.fresh(graph)
       open_round(graph, AnswerTable({("stage_disabled", "g1"): True}), draft, "review_round")
       assert draft.skipped == {"g1": "stage_disabled"}
       draft.open_round = None
       step = open_round(graph, _NO_ANSWERS, draft, "review_round")
       assert isinstance(step, DispatchSet)
       assert tuple(d.node for d in step.dispatches) == ("g1", "g2")
       assert draft.skipped == {}
       stop = take_binding(
           graph,
           draft,
           "review_round",
           "<halt>",
           reason="limit",
           resume=None,
           summary=None,
           round_counts=("g1", "g2"),
           evidence=None,
       )
       assert isinstance(stop, Stop)
       assert stop.round_counts == ("g1", "g2")
   ```

   In `_article()`, `g1` skips under `stage_disabled`, which `valid_generic.json` declares with `inRoundCounts: false`. Without the fix, the last assertion gets `("g2",)`.

This fix edits only one test file, `graphscene/tests/engine/test_transitions.py`, so that is the only test file it runs: `bash scripts/python-service.sh --package graphscene test tests/engine/test_transitions.py`.
