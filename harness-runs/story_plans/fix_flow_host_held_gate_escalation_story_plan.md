# Story: Settle the flow host's held-gate escalation order (#472)

## Context

This branch settles one case in `devscene-flow-host`: a round where one gate's outcome is held (`error` or `blocker`) and every gate still out was refused. The bash walker escalates the held gate at once (`cli/templates/scripts/flow-walker.sh` → `ROUNDS`, *"With none out: a held gate escalates; otherwise every marked gate is dispatched again as one set"*; `record_in_set`). The host re-dispatches the refused gates first and escalates at the round's next join (`devscene-flow-host/src/devscene_flow_host/host/round_gates.py` → `_redispatch`). The task prompt records the decision, made on 2026-11-24 with #465: **the host's order is kept.** No GraphScene change is made for it. The escalation carries the whole round's verdicts. The refused gate is reviewed again under either order, because bash's `start` reopens a round's missing gates when the evidence is consistent (`flow-walker.sh` → `STATE`). The orders differ in when that review happens, not whether. So this branch changes no executable line. It turns the `TODO: @claude` marker at `_redispatch` into a stated rule, pins the rule with literal expectations, and moves the README's **Still open** entry under **Chosen**, where #419 reads it.

The work is two tasks in the `devscene-flow-host` layer, in ship order:

- **Task 1** — the code and its test. It states the rule in `round_gates.py`'s module docstring under *"The rule:"*. It removes the held-gate bullet from *"Deliberately not covered"* and deletes the `# TODO: @claude` comment at `_redispatch`. It rewrites `tests/test_round_gates.py`'s header and the existing case's docstring, which still describe a departure, and adds one case: a held gate stays held while its refused sibling is refused again.
- **Task 2** — the package README. It moves the rule into `## What it reads, answers and keeps` → **Recording a gate.** and removes the *"One departure from the bash walker remains"* paragraph. It moves the **Still open** entry *"The held-gate escalation — #472"* to **Chosen** in `## Differences from flow-walker.sh`, citing the two test cases Task 1 leaves.

**The rule's one wording, used by both tasks.** Task 1 writes this bullet into the module docstring, and Task 2 states the same rule in README prose:

> A held gate at a join whose only gates out are refused ones does not escalate there: the refused gates are re-dispatched as one set in the same round, and the held gate escalates at the round's next join, once every re-dispatched gate has a verdict or is held, so the escalation carries the whole round's verdicts. `flow-walker.sh` → `record_in_set` escalates at once instead (*"With none out: a held gate escalates"*); this order is the host's, chosen in #472, and GraphScene is not changed for it.

**What must keep working.** #465 added two things around `_redispatch`. `record_outcome` keeps a non-round reviewer's findings file in `RevisionFindingsStore` (`host/revision_findings.py`, under `RefusalStore`'s lock) and clears it when a round closes. The command renders the re-dispatched set and its `refused:` lines (`commands/render.py` → `_refused`). This branch leaves both unchanged, because it changes no executable code. The third refusal of a gate records `error` and escalates the same way in both walkers, and that is not affected either.

**Top risks:** The likeliest failure is an implementer who reads "settle the escalation" as a change to behaviour and edits `_redispatch`, `_settle` or `_record`. The decision keeps the host's order, so Task 1's Verification checks that its diff to `round_gates.py` touches only the docstring and the comment. The second risk is a new case whose literals were copied from the code's output rather than written from the rule. Task 1 states each expected `HostStep` from the rule above and from `flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar, and treats a mismatch as a finding to report, not a literal to copy. The third risk is drift between the docstring, the test header and the README, or a README that still calls this a departure or cites the deleted `TODO`. Task 2's Verification greps the package for `#472`, `_redispatch` and `TODO: @claude` against the register below.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom. **Only the committing role flips a marker to `[x]`.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets in the per-task files, are informational progress markers only. They are never the iteration source, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_flow_host_held_gate_escalation/task_<K>_plan.md`. Both tasks are in the `devscene-flow-host` layer, and code comes before the document that cites it.

1. [ ] **Task 1** — State the host's held-gate order in `round_gates.py` and pin it in `test_round_gates.py` _(layer: devscene-flow-host)_ _(points: 10)_
2. [ ] **Task 2** — Record the held-gate order as the host's rule and move it to **Chosen** in the package README _(layer: devscene-flow-host)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"settles what `devscene-flow-host` does at a round where one gate's outcome is held (`error` or `blocker`) and the only gates still out are refused ones, and removes the `TODO: @claude` marker #464 left for it."*

This register covers the plan's durable-corpus targets only, which are the prose of `devscene-flow-host/README.md`. Task 1's targets are source and test code, and their docstrings and comments are code-level documentation, so they are not register rows.

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root:

```
git grep -nE 'held gate|held-gate|#472|_redispatch|once no other gate is out|escalates at the join' -- '*.md' ':!harness-runs'
```

**Derivation entry — standing-artifact rows (procedure).** **First step, runnable:** `grep -nE 'held gate|held-gate|#472|_redispatch|refused gate|re-dispatch' harness-runs/lessons.md harness-runs/improvement_suggestions.md harness-runs/README.md`. **Artifact:** the standing artifacts under `harness-runs/`, which are the lessons ledger, the improvement-suggestions log and the directory README (per-branch run records under `harness-runs/` are records of earlier runs and are not standing). **Traversal:** each file in the order named, then its lines in file order. **Per-candidate decision rule:** a line is reached when it states which order the host or bash follows at a join whose only gates out are refused. When this plan was written, the first step printed nothing, so this entry adds no row.

**Closure invariant:** every site either derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `devscene-flow-host/README.md` → `## What it reads, answers and keeps` → **Recording a gate.** (*"once no other gate is out every refused gate is re-dispatched as one set in the same round"*) | — | command entry, `once no other gate is out` | `change` | Task 2: gains the held-gate rule as the host's rule |
| 2 | `devscene-flow-host/README.md` → `## What it reads, answers and keeps`, the paragraph *"One departure from the bash walker remains, marked by a `TODO: @claude` at `_redispatch`"* | — | command entry, `_redispatch` | `change` | Task 2: removed, because the marker is gone and the order is no longer a departure to remove |
| 3 | `devscene-flow-host/README.md` → `## What it reads, answers and keeps`, the bullet **The held-gate escalation (#472).** | — | command entry, `held-gate`, `#472` | `change` | Task 2: removed with row 2. Its content moves into **Recording a gate.** (row 1) |
| 4 | `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **Still open** → **The held-gate escalation — #472.** | — | command entry, `held-gate`, `#472`, `_redispatch` | `change` | Task 2: moved to **Chosen**, naming what bash does, what the command does, that no `flow-walker*` suite pins it, and the host suite that does |
| 5 | `docs/flow-graph-walker.md` → *Format 3* **Decision.** (*"the last is the join, which prints the first held gate's binding"*) | — | command entry, `held gate` | `no-change` | It describes the bash walker's held join with no gate refused. This branch changes neither walker's behaviour at that join, and the text says nothing about a refused gate |
