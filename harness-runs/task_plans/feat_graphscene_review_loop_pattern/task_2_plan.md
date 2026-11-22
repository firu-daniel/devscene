### Task 2 — Dispatch a round's writer and gates through the review-loop pattern

**Goal:** Make the walk read a round's review-loop keys only through `graphscene.engine.review_loop`. A review loop's writer is dispatched with its round's number. A review loop's gate is dispatched with its round's number and with `converging`. A plain round's gate is dispatched with its round's number and with `converging` `None`.

**Depends on:** Task 1, which provides, in `graphscene/src/graphscene/engine/review_loop.py`:
- `ReviewLoop(round: str, writer: str, counter: str, converging_from: int)`;
- `review_loop(node: RoundNode) -> ReviewLoop | None`, which is `None` for a round that declares no `writer`;
- `review_loops(graph: FlowGraph) -> tuple[ReviewLoop, ...]`, in `nodes` key order;
- `is_converging(loop: ReviewLoop, counters: Mapping[str, int]) -> bool`.

Today every round is a review loop, so on every graph that loads today this task changes no returned step.

**Where this task stops.** Making `RoundNode.writer` / `.counter` / `.converging_from` optional is Task 4's. After this task, `transitions.py` reads none of those three attributes directly, so Task 4's type change needs no edit here. Testing the plain-round dispatch is Task 5's (`graphscene/tests/engine/test_transitions.py`), because a writer-less round can only be built after Task 4.

### Targets

- `graphscene/src/graphscene/engine/transitions.py`
- `graphscene/src/graphscene/engine/walker.py` — docstring only

**Work:**

- [ ] `transitions.py` → `_dispatch`:
  - When `node` is a gate of round `gate_of`, `round_number` is `draft.round_numbers[gate_of.id]` for every round. `converging` is `is_converging(loop, draft.counters)` when `review_loop(gate_of)` returns a loop, and `None` otherwise.
  - When `node` is no gate, it is a review loop's writer when some `loop` in `review_loops(graph)` has `loop.writer == node.id`. Its `round_number` is then `draft.round_numbers[loop.round]`; otherwise it stays `None`.
  - Remove the direct reads of `gate_of.counter`, `gate_of.converging_from` and `r.writer`.
- [ ] `transitions.py`, module docstring:
  - The rule's sentence *"carrying the round number and convergence of the round it is a gate of, or the round number of the round it writes"* becomes: *"carrying the round number of the round it is a gate of, with that round's convergence when it is a review loop, or the round number of the review loop it writes (`graphscene.engine.review_loop`)"*.
  - The *"Deliberately not covered"* bullet naming *"The review loop's rules"* stops claiming them for another module. It keeps *"recording a gate's outcome and the held join (`graphscene.engine.rounds`)"*.
- [ ] `walker.py`, module docstring only: the *"Deliberately not covered"* bullet *"The review loop's rules: the host's."* becomes *"What a host does with a review loop's round number, convergence and findings: the host's; which round is a review loop is `graphscene.engine.review_loop`'s."*. No code changes.

**Verification:**

- `git grep -nE "\.counter\b|\.converging_from|\.writer\b" -- graphscene/src/graphscene/engine/transitions.py graphscene/src/graphscene/engine/walker.py` prints nothing outside a `ReviewLoop`'s own `loop.counter` / `loop.writer` / `loop.round` reads. Read each line it prints.
- `Dispatch`'s fields are unchanged: `graphscene/src/graphscene/model/walk_actions.py` and `graphscene/src/graphscene/adapters/walk_json.py` are not in the unit's diff.
- **Deviations from plan:**
  - The first verification bullet's `git grep -nE` prints nothing on any input here, because git's ERE does not match `\b`. That empty output therefore proves nothing. I re-ran the same pattern through `grep -nE` and `git grep -nP` instead. Both print one line, `transitions.py:186` (`lp.writer == node.id`). That line is a `ReviewLoop`'s own `.writer` read. No `.counter` or `.converging_from` read remains in either file.
  - The `treeGuards` entry `tests/test_layers.py` (covers `graphscene/src/graphscene/**`) was not run. `bash scripts/python-service.sh --package graphscene test tests/test_layers.py` was refused by the tool layer ("Permission to use Bash has been denied because Claude Code is running in don't ask mode"). The layer-contract claim rests on reading the diff instead: `transitions.py` gains one import, `graphscene.engine.review_loop`. That is `engine` importing `engine`, with no `adapters` or `facade` import. The Run gates phase's `<test_cmd>` run is what verifies this guard.
