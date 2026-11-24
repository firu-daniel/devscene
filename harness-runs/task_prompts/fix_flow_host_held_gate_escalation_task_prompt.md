`fix_flow_host_held_gate_escalation` settles what `devscene-flow-host` does at a round where one gate's outcome is held (`error` or `blocker`) and the only gates still out are refused ones, and removes the `TODO: @claude` marker #464 left for it. Part of #376.

## Why

The bash walker escalates the held gate at once (`cli/templates/scripts/flow-walker.sh` → `ROUNDS`, *"With none out: a held gate escalates; otherwise every marked gate is dispatched again as one set"*). The host from #464 (#471) can't do that, because GraphScene gives a host no way to set a due gate aside in an open round. So the host re-dispatches the refused gates first, then escalates at that same round's next join, once they are back (`devscene-flow-host/src/devscene_flow_host/host/round_gates.py` → `_redispatch` and its `TODO: @claude`; `devscene-flow-host/README.md` → **Recording a gate.**). #419 retires the bash walker with no fallback, so the rule that ships has to be settled first.

## Decided (2026-11-24, with #465)

- **Where the host's way is better than bash's, the host's way wins** (#465 → **Decided**). Neither order here is a defect: this branch picks one and records it.
- **The host's order is kept** (2026-11-24). The host re-dispatches the refused gates and escalates at the round's next join. No GraphScene change is made for this. The escalation carries the whole round's verdicts. On resume, bash's `start` reopens only the round's missing gates when the evidence is consistent (`flow-walker.sh` → `STATE`; `cli/test/flow-walker-resume.test.mjs`), so the refused gate is reviewed again in either order. What differs is when, not whether.

## Leads

_Starting points from #464's and #465's runs and their reviews, not requirements. The planning session decides what holds._

- **Where the rule is recorded:**
  - `_redispatch`'s `TODO: @claude` marker gives way to a statement of the rule in `round_gates.py`'s module docstring.
  - `devscene-flow-host/README.md` → **Recording a gate.** states it as the host's rule.
  - `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → the **Still open** entry *"The held-gate escalation — #472"* moves to **Chosen**, as an entry naming what bash does, what the command does and the suite it moves. That section is #465's list for #419 (#465 merged it, and its `## The command line` section and `ROADMAP.md`'s GraphScene row link it).
- **What pins it today:** no `cli/test/flow-walker*.test.mjs` case pins this combination. This was checked on 2026-11-24 against the test bodies:
  - `flow-walker-fan-out.test.mjs` (5) holds an `error` with no gate refused.
  - (10) escalates on a gate's own third refusal with nothing else held.
  - (7)–(9) and (11) hold no gate.

  #465 corrected the README entry's suite pointer to say so. With no suite to move, the **Chosen** entry says that no suite pins it, and a case in `devscene-flow-host/tests/test_round_gates.py` (or the command's `tests/test_flow_walker.py`) pins the host's order with literal expectations.
- **What #465 added around `_redispatch`**, which a change here keeps working:
  - `record_outcome` now also keeps a non-round reviewer's findings file in `RevisionFindingsStore` (`host/revision_findings.py`, under `RefusalStore`'s lock) and clears it when a round closes, so a revision prints the closed round's `GateRecord` details.
  - The command renders the re-dispatched set and its `refused:` lines (`commands/render.py` → `_refused`).
- **Not affected:** the third refusal of a gate records `error` and escalates the same way in both walkers.

## Depends on

#464, #465. Ordered after #465, which also edits `host/round_gates.py`, and before #475 and #419.
