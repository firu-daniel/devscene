### Task 4 — Record a gate's outcome in an open round and join the set in `engine/rounds.py`

**Goal:** Record one gate's outcome while a round's set is out, in any order. Until the last gate is in, return `Wait`. At the last one, join: a `held` outcome waits for its siblings and never cancels them. At the join, the first held gate's edge is taken and the round is not closed. With none held, the round closes through Task 3's `close_round`.

**Depends on:** Task 3. This task calls these functions from `graphscene.engine.transitions` exactly as declared there:

- `close_round(graph, host, draft, round_id) -> Step`;
- `follow_edge(graph, host, draft, node_id, edge, *, advance=None, closed_round=(), open_gates=(), held=()) -> Step`;
- `take_binding(graph, draft, node_id, name, *, reason, resume, summary, round_counts, evidence, cap=None, open_gates=(), held=(), closed_round=()) -> Step`;
- `WalkDraft`, whose fields are `flow`, `node`, `awaiting`, `pending`, `counters`, `round_numbers`, `open_round`, `prompts`, `reports`, `skipped` and `passed`. Each function sets `draft.pending` and `draft.awaiting`.

From `graphscene.model.walk_actions` it consumes `Wait(round, recorded, pending)`, `DispatchSet(round, number, dispatches, passed)`, `GateRecord(gate, outcome, detail)`, `Refused(reason)` and `Step`. From `graphscene.model.walk_state` it consumes `OpenRound(round, number, due, records)`.

**Where this layer stops.** Whether a set is pending at all (`awaiting == "set"`) and whether `node` was named are checked by **Task 5's** `Walker.next` before it calls `record_gate`. This module assumes `draft.open_round` is set and asserts it. Reading or writing state is Task 5's.

### Targets

- `graphscene/src/graphscene/engine/rounds.py` (new)
- `graphscene/tests/engine/test_rounds.py` (new)

**Work:**

- [ ] **Docstring and refusals.** The module docstring has a *"The rule:"* paragraph: a gate's outcome is recorded once; a held outcome waits for the gates still out; the join takes the first held gate's edge in `gates` order, or else closes the round. Then `record_gate(graph, host, draft, gate, outcome, detail) -> Step` refuses, with these exact reasons and in this order:
  - `f"'{gate}' is not pending in round {number}"` when `gate` is not in `open_round.due`;
  - `f"an outcome for '{gate}' is already recorded in round {number}"`;
  - `f"outcome '{outcome}' is not declared by node '{gate}'"`;
  - `f"outcome '{outcome}' of round gate '{gate}' declares neither a verdict nor held"`, when the outcome's `OutcomeDeclaration` has `verdict is None and not held`.
- [ ] **Recording.**
  - Store `GateRecord(gate, outcome, detail)` in a new `OpenRound` whose `records` gains the gate.
  - For a verdict outcome, record its `RouteEdge.report` into `draft.reports`. The edge's `to` is the round, as check 9 guarantees, and is not followed.
  - While gates remain unrecorded, return `Wait(round, recorded=<the record>, pending=<unrecorded due gates in gates order>)`. Set `draft.pending` to a `DispatchSet` of only those gates' `Dispatch` blocks, with the stored set's `passed` kept, so Task 5's `current` re-prints only what is still out. Keep `awaiting="set"`.
- [ ] **The join.** Once every due gate is recorded:
  - **Held gates first.** The held records are those whose outcome declares `held`, in `gates` order. When there are any, clear `draft.open_round` and take the first held gate's edge as an ordinary outcome of that gate, with no `RoundPassage`, `node` set to the gate and `held=<every held record>`:
    - a `BindingEdge` goes to `take_binding(..., held=...)`;
    - a `RouteEdge` goes to `follow_edge`.
  - **Otherwise** `return close_round(graph, host, draft, open_round.round)`.
- [ ] **`test_rounds.py`.** Its module docstring opens *"The rule this file exists to enforce"*. Plant a two-gate round through `graphscene/tests/engine/walk_support.py` → `planted` and drive it from `open_round` with `AnswerTable`. Cover these:
  - each refusal's exact text;
  - recording in reverse `gates` order;
  - `Wait.pending` and the re-printable `DispatchSet` after the first record;
  - a held outcome recorded first, which still waits for its sibling and joins to a `Stop` whose `node` is the held gate, `reason` the edge's reason, and `held` the held records;
  - two held gates, where the first in `gates` order wins;
  - an all-verdict join closing `fail` when one gate failed, with the closed records in `gates` order;
  - a `detail` carried through to `closed_round`.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/engine/test_rounds.py` passes.
- [ ] `rounds.py` imports `graphscene.engine.transitions`, `graphscene.model` and the standard library only, and `transitions.py` does not import `rounds.py`.
