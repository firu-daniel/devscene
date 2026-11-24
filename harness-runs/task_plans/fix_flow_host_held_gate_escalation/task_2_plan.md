### Task 2 — Record the held-gate order as the host's rule and move it to **Chosen** in the package README

**Goal:** Make `devscene-flow-host/README.md` state the held-gate order as the host's rule, not as a departure waiting for a GraphScene change. It goes in **Recording a gate.**, and in `## Differences from flow-walker.sh` it moves from **Still open** to **Chosen**, which is the list #419 reads when it hands `flow-walker.sh`'s callers to `devscene-flow-walker`.

**Depends on:** Task 1. Task 1 deletes the `TODO: @claude` marker at `host/round_gates.py` → `_redispatch` and states the rule in that module's docstring under *"The rule:"*, in the wording the story index `## Context` quotes. It leaves two cases in `tests/test_round_gates.py`, cited here by these exact names: `test_a_held_error_beside_a_refused_gate_re_dispatches_first` and `test_a_held_error_waits_while_its_refused_sibling_is_refused_again`. This task changes no code and no test. It writes the same rule in README prose, and the README cites the module and those two cases instead of the deleted marker.

### Targets

- `devscene-flow-host/README.md`: `## What it reads, answers and keeps` (**Recording a gate.**, and the paragraph and bullet after **Kept findings files.**) and `## Differences from flow-walker.sh` (**Chosen**, **Still open**).

**Work:**

- [ ] **Recording a gate.**: after the clause *"once no other gate is out every refused gate is re-dispatched as one set in the same round"*, state the rule as the host's own. A held gate at a join whose only gates out are refused ones does not escalate there. The refused gates are re-dispatched first, and the held gate escalates at the round's next join, once every re-dispatched gate has a verdict or is held, so the escalation carries the whole round's verdicts. Cite `host/round_gates.py` → *"The rule:"*. Do not call it a departure, and name no `TODO`.
- [ ] Delete the paragraph *"One departure from the bash walker remains, marked by a `TODO: @claude` at `_redispatch` in `host/round_gates.py`:"* and the bullet under it, **The held-gate escalation (#472).** **Kept findings files.** is followed directly by **Resuming a round.**
- [ ] `## Differences from flow-walker.sh` → **Still open**: delete the entry **The held-gate escalation — #472.** Leave the three #475 entries unchanged.
- [ ] `## Differences from flow-walker.sh` → **Chosen**: append an entry **The held-gate escalation.** in the section's own shape: what `flow-walker.sh` does, what the command does, and the suite.
  - **Bash:** at a join whose only gates out are refused, it escalates the held gate at once (`flow-walker.sh` → `ROUNDS`, `record_in_set`). The refused gate is reviewed again only on resume, because `start` reopens a round's missing gates when the evidence is consistent (`flow-walker.sh` → `STATE`; `cli/test/flow-walker-resume.test.mjs`). Open that suite and cite the case by its quoted title. If no case there exercises that reopening, cite `STATE` alone.
  - **Command:** it re-dispatches the refused gates as one set in the same round and escalates at the round's next join, carrying the whole round's verdicts (`host/round_gates.py` → *"The rule:"*). GraphScene gives a host no way to set a due gate aside in an open round, and no GraphScene change is made for this. Both orders review the refused gate again; they differ in when.
  - **Suite:** keep the existing sentence that no `flow-walker*` suite pins this combination, with its pointers: `flow-walker-fan-out.test.mjs` → *"(5) a gate's error with two verdicts recorded"*, *"(10) the third refusal of a gate escalates"*, and *"(7)"* to *"(9)"* and *"(11)"*. So #419 moves no suite. Add the host's own pins: `tests/test_round_gates.py` → `test_a_held_error_beside_a_refused_gate_re_dispatches_first` and `test_a_held_error_waits_while_its_refused_sibling_is_refused_again`.

**Verification:**

- `git grep -nE 'TODO|departure|#472|_redispatch' -- devscene-flow-host/README.md` hits no sentence that calls the held-gate order a departure, a **Still open** difference or a pending change, and no sentence that cites a `TODO` at `_redispatch`. Every remaining hit is ⊆ the story index's `## Scope register` rows 1 and 4 as rewritten here, or is one of the #475 `TODO` citations in **Still open**, which stay.
- Re-run the register's command entry verbatim (story index `## Scope register`). Every site it prints is a register row, and no hit falls outside the register.
- **Recording a gate.** and the **Chosen** entry state the same order as `host/round_gates.py`'s docstring bullet, read side by side: the refused gates first, escalation at the round's next join, and the whole round's verdicts.
- The two test names in the **Chosen** entry match `def` lines in `devscene-flow-host/tests/test_round_gates.py` (`git grep -n 'def test_a_held_error' -- devscene-flow-host/tests/test_round_gates.py`).
- `ROADMAP.md`'s GraphScene row and the README's `## The command line` still link `## Differences from flow-walker.sh` by that exact heading, which this task does not rename.
