`feat_graphscene_round_resume` lets a walk start inside a round, at round *n* with some of its gates' outcomes already recorded, so a host that keeps its own round records can resume a round instead of restarting it. Part of #376.

## Why

`flow-walker.sh start` resumes a planning round from the round files on disk. It takes the round number from them, records the gates whose file is present, and opens the set with only the gates still missing (`fw_round_evidence` in `cli/templates/scripts/lib/flow-walker-gates.sh`; the rules in `cli/templates/scripts/flow-walker.sh` → `STATE`). GraphScene's `Walker.start` always begins fresh: every counter at 0, every round number at 0, nothing recorded (`graphscene/src/graphscene/engine/walker.py` → `start`, `WalkDraft.fresh`). #418's `flow-walker.sh` compatibility entry needs the bash behaviour. Reading the files is DevScene's, but starting at a given point of a round is not.

## Decided (2026-11-22)

- **GraphScene gets a generic entry for this.** The host reads its own records and hands the engine the round, its number and the gate outcomes already recorded. GraphScene reads no file to decide any of it. LangGraph has the same idea in `update_state(config, values, as_node=…)`, which writes state as if a node had run so the next step resumes from there.
- **The DevScene side, reading the round files and the revision note into those arguments, is #418's**, in `devscene-runtime/`.

## Leads

_The leads below are starting points from #376 and the discussion that split it, not requirements. The planning session decides what holds when this branch is planned._

- **Shape:** an argument to `Walker.start`, or a method of its own.
- **What it carries:** the round node, its round number, and the recorded `GateRecord`s (gate, outcome, detail). Whether it also carries counter values is open: bash `start` sets every counter to 0 even on a resume, and keeps the round number apart from the counter.
- **The bash cases to reproduce, split between engine and host.** No round file: the whole set at round 0. Some files missing, the rest consistent: record the present gates, open only the missing ones. A complete round that is unreadable or has no FAIL: the whole set again at that round. A FAIL with the next revision note on disk: the next round's whole set. A FAIL without it: every verdict recorded and the round closed. Opening a set with some gates recorded, and closing at once when every gate is recorded, look like the engine's. Which round, and whether the files are consistent, look like the host's.
- **Refusals:** a recorded gate that is not a gate of that round, an outcome the gate does not declare, a second record for one gate, a round number below 0. Each refused as `start` refuses an unknown entry today.
- **Walk state JSON stays version 1** if the entry only builds a `WalkState` the existing document already holds: `round_numbers` and `open_round` (`OpenRound.number`, `due`, `records`) are already there (`graphscene/src/graphscene/model/walk_state.py`, `graphscene/src/graphscene/adapters/walk_json.py`).
- **A held record** (`error`, `blocker`) recorded on entry must join as it does today: the first held gate's edge is taken once the rest are in.
- **#423's "entry and resume decided by a host hook"** builds on this entry. This branch adds only the engine side.

## Depends on

#417
