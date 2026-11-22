### 1. Resuming an interrupted revision writer drops its closed round, so the re-dispatched revision has no gate records to revise against

**File:** `graphscene/src/graphscene/engine/walker.py` (`Walker._step`) — "return arrive(graph, host, draft, pending.resume)"
**Class:** Wrong behaviour
**Failure:** If a host walks `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` to a failed `plan_round` and then calls `next("questions")` and `next("answered")`, then the `Dispatch` it gets back is `plan_writer` with `prompt='revision'` and `closed_round=()`. The dispatch it replaces carried all three of round 0's `GateRecord`s.

**The defect.** A failed round reaches its writer through `close_round` → `follow_edge(..., closed_round=closed)` → `arrive(..., closed_round=closed)`. The writer's `Dispatch` carries `closed_round`, the round's records, and each record's `detail` holds the host's findings path. `WalkState` does not store that tuple anywhere except inside `pending`. When the writer then takes an interrupt binding, three things lose it:

- `_step` follows the edge with `follow_edge(graph, host, draft, state.node, edge)` and passes no `closed_round`.
- `take_binding` builds `Interrupt(name, node_id, agent, resume, binding.resume_outcome, tuple(draft.passed))`, and `Interrupt` has no field to hold the tuple.
- The resume calls `arrive(graph, host, draft, pending.resume)` with the default `closed_round=()`.

`prompts` survives the interrupt (`model/walk_state.py`: *"an interrupt's resume re-dispatches with it"*), so the writer is dispatched again as a `revision`. The records it is supposed to revise against do not survive. The host gets a revision dispatch with nothing to revise, and the saved state no longer holds the round's records.

**Why this is a requirement, not a refinement.** The task prompt says *"The `flow-walker*.test.mjs` suites show what behaviour is expected"*, and the story index's `## Context` says they *"show the behaviour expected of the routing"*. Two of those suites assert the opposite of what this code does:

- `cli/test/flow-walker.test.mjs` → `'(7) writer questions route through <ask> and resume the writer on the prompt it had'` expects `writer(1, roundFiles(0))` after `ask`. Its comment reads: *"the prompt it had, so a revision stays a revision against the same round's files, and no round closes again."*
- `cli/test/flow-walker-resume.test.mjs` → `'(5) a parked <ask> resumes at the writer that parked, on its stored revision'` expects the same.

The bash walker persists the closed round as `revision_findings` (`cli/templates/scripts/flow-walker.sh`, the `STATE` comment: *"`revision_findings` (the closed round's files …)"*). It treats a revision with no findings as a fault: *"a revision of '$node' is due and no findings file is recorded"*.

No task plan settles this differently. `task_5_plan.md` step 6 says only *"when it matches, `arrive(graph, host, draft, pending.resume)`"*. The branch's own test, `graphscene/tests/engine/test_walker.py` → `test_an_interrupt_resumes_only_on_its_resume_outcome_with_the_stored_prompt`, hand-writes the loss as the expected value: `_writer("rework", 1, 1)` with `closed_round=()`. None of the committed reviews raised it.

**Confirmed by a probe.** I wrote one file under `harness-runs/scratch/` that loads the harness graph through `load_graph_file`, uses an in-memory store and a host that answers `False` to every predicate, and walks `start` → `returned` → `FAIL`/`PASS`/`PASS` (with details `parity_0.md`, `arch_0.md`, `plan_0.md`) → `questions` → `answered`. I ran it with `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/skeptic_resume_closed_round_probe.py <repo_root>`. It printed:

- the revision dispatch: `Dispatch(node='plan_writer', ..., prompt='revision', ..., round_number=1, ..., closed_round=(GateRecord(gate='business_parity_review', outcome='FAIL', detail='parity_0.md'), GateRecord(gate='architecture_review', outcome='PASS', detail='arch_0.md'), GateRecord(gate='plan_review', outcome='PASS', detail='plan_0.md')), ...)`;
- the interrupt: `Interrupt(binding='<ask>', node='plan_writer', ..., resume='plan_writer', resume_outcome='answered', passed=())`;
- the resumed dispatch: `Dispatch(node='plan_writer', ..., prompt='revision', ..., round_number=1, ..., closed_round=(), passed=())`.

**Fix.** Carry the interrupted dispatch's closed round on the `Interrupt`, and re-arrive with it on resume. A stop binding's `Stop.closed_round` does not change.

1. `graphscene/src/graphscene/model/walk_actions.py` → `Interrupt`: add a last field, `closed_round: tuple[GateRecord, ...] = ()`, after `passed`. In the module docstring's *Field meanings* list, add this bullet: *"`Interrupt.closed_round` is the closed round the interrupted dispatch carried; the resume re-dispatches with it."*

2. `graphscene/src/graphscene/engine/transitions.py` → `take_binding`, the `InterruptBinding` branch: construct
   ```python
   interrupt = Interrupt(
       name, node_id, agent, resume, binding.resume_outcome, tuple(draft.passed), closed_round
   )
   ```
   In the module docstring's `take_binding` bullet, change *"an interrupt pauses at the node"* to *"an interrupt pauses at the node, carrying the closed round it was given"*.

3. `graphscene/src/graphscene/engine/walker.py`:
   - Change the imports to `from graphscene.model.flow_graph import BindingEdge, DispatchNode, FlowGraph, InterruptBinding, RoundNode` and `from graphscene.model.walk_actions import Dispatch, GateRecord, Interrupt, Refused, Step`.
   - In `_step`'s interrupt branch, replace `return arrive(graph, host, draft, pending.resume)` with `return arrive(graph, host, draft, pending.resume, closed_round=pending.closed_round)`.
   - Replace the last line, `return follow_edge(graph, host, draft, state.node, edge)`, with:
     ```python
     carried: tuple[GateRecord, ...] = ()
     if (
         isinstance(edge, BindingEdge)
         and isinstance(graph.vocabulary.bindings[edge.binding], InterruptBinding)
         and isinstance(pending, Dispatch)
     ):
         carried = pending.closed_round
     return follow_edge(graph, host, draft, state.node, edge, closed_round=carried)
     ```

4. `graphscene/src/graphscene/adapters/walk_json.py`:
   - In `_action_out`'s `Interrupt` dict, add `"closed_round": _records_out(action.closed_round),` immediately before `"passed"`.
   - In `_action`'s `interrupt` branch, add `"closed_round"` to the key tuple immediately before `"passed"`. Pass `closed_round=_tuple(_record, fields["closed_round"], _join(path, "closed_round")),` to `Interrupt`.
   - The document stays `"version": 1`: no released state file exists.

5. Tests:
   - `graphscene/tests/engine/test_walker.py` → `test_an_interrupt_resumes_only_on_its_resume_outcome_with_the_stored_prompt`:
     - bind `closed = (GateRecord("g1", "rejected", None), GateRecord("g2", "approved", None))`, the records `_rejected_once` produces;
     - expect `Interrupt("<pause>", "draft", "article-writer", "draft", "resumed", (), closed)` from `walker.next("crashed")`;
     - expect `_writer("rework", 1, 1, closed_round=closed)` from `walker.next("resumed")`.
   - `graphscene/tests/adapters/test_walk_json.py` → `_ACTIONS`: in the first `Interrupt(...)` entry (keyword form, `binding="ask"`, `node="review"`), add `closed_round=(_SET_RECORD,)`, so the round trip covers the new key.

This fix edits two test files, so those are the only test files it runs:
- `bash scripts/python-service.sh --package graphscene test tests/engine/test_walker.py`
- `bash scripts/python-service.sh --package graphscene test tests/adapters/test_walk_json.py`
