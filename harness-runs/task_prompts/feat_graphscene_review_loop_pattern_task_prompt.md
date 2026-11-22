`feat_graphscene_review_loop_pattern` turns the review loop from rules the walker enforces on every graph into a pattern a graph opts into. Part of #376.

## Why

Today the walker enforces the planning loop everywhere: `FAIL` requires `--findings`, plus the `revision` prompt variant, `review_mode`, `findingsFolder` and a round's `writer`. A graph with no review loop shouldn't carry those rules.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- The pattern: write → parallel gates → round → revise with findings, with a revision cap and the held-failure join.
- Its rules checked only where a graph declares it.
- Expanding to plain nodes may let the builder and YAML shorthands reuse it later.
- The harness's planning graph opts in and keeps its behaviour.
- **The main open question: checks 8 and 9 now apply to every graph that has a round.** _From #415 as merged (#444, 2026-11-22)._ `load_graph` rejects a graph that breaks `gate-in-round` (a dispatch node routing a fail verdict with no increment must be a gate of exactly one round; a round's gates and writer must be dispatch nodes) or `round-fan-out` (each gate routes its pass, fail and skip edges to the round and nowhere else; the writer routes at least one route edge to it; nothing else targets it). Those are review-loop shape rules, applied unconditionally, which is the opposite of this branch's aim. Decide whether they become part of the pattern, checked only where a graph opts in, or whether they are round rules the engine keeps (a round is an engine node kind with a required `writer`).
- **Check 8 no longer reads `findingsFolder`:** a gate is picked by its fail verdict with no increment, so moving `findingsFolder` into the pattern does not touch the checker.
- **The reference checks read keys this branch may move:** `prompt-known` (an edge's `prompt` must be one of its target dispatch node's `prompts`), and `path-known` over a round's `plan` and `revisionNote` and an `onCap`'s `evidence`. Whatever key moves into the pattern, its reference check moves with it (`graphscene/src/graphscene/engine/references.py`).
- **The "Why" above describes the bash walker, not the Python one** _From #416 as merged (#446, 2026-11-22)._ `FAIL` requiring `--findings`, `review_mode` and the per-findings-file arguments live only in `cli/templates/scripts/flow-walker.sh`; GraphScene's walker never ported them. A gate's `GateRecord.detail` is optional and opaque (`graphscene/src/graphscene/model/walk_actions.py`), and the engine never reads `findings_folder`. If the harness still needs those rules, they may belong to #418's `flow-walker.sh` compatibility entry rather than to the engine.
- **What still ties GraphScene to the review loop after #416**, and so what "opt-in" would move:
  - the model: every `RoundNode` requires `writer`, `counter` and `converging_from`, and carries `plan` and `revision_note`; `DispatchNode.findings_folder` is still a model field (`graphscene/src/graphscene/model/flow_graph.py`);
  - the engine: a round's writer is dispatched with its round's number, a gate with a `converging` flag (`counter >= converging_from`), and a fail edge carries the closed round's gate records to its target (`graphscene/src/graphscene/engine/transitions.py` → `_dispatch`, `close_round`);
  - the static checks 8 and 9 (the main open question above).
- **Interrupts carry the closed round.** #416's skeptic review fixed an interrupt on a revision writer losing the closed round, so an `Interrupt` now carries `closed_round` and the resumed dispatch gets it back (`graphscene/src/graphscene/engine/walker.py`). Whether that stays generic engine behaviour or becomes part of the pattern is open. The held join (a held outcome waits for its siblings, the first held gate's edge is taken) is needed by any fan-out round, review loop or not.
- **`resumeOutcome` is not a declared outcome.** #416 settled that while an interrupt is pending `next` accepts exactly the binding's `resume_outcome` and never looks it up under `vocabulary.outcomes`. If the pattern defines its own interrupt (an `<ask>` on the writer), check it keeps that.
- **The walk state's JSON is versioned.** `graphscene/src/graphscene/adapters/walk_json.py` writes `"version": 1` and refuses any other version; a pending `Dispatch` stores `round_number`, `converging` and `closed_round`. Moving a key off `RoundNode` does not change that document, but changing what a `Dispatch` carries does, and saved state files of version 1 would then be refused.

## Depends on

#416
