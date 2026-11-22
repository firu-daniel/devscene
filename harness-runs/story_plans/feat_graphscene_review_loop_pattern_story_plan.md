# Story: GraphScene review-loop pattern

## Context

This branch makes GraphScene's review loop a pattern a graph opts into, so the engine stops applying it to every graph. Today every `RoundNode` must declare `writer`, `counter` and `convergingFrom`. Checks 8 (`gate-in-round`) and 9 (`round-fan-out`) apply their review-loop clauses to any graph with a round, and clause one of check 8 applies even to a graph with no round. After this branch a round is a plain fan-out and join unless it declares `writer`. A round that declares it is a **review loop**: write, then parallel gates, then the round, then a revision with the closed round's records, with a revision cap. The review-loop rules are checked only on such a round. Everything lands in `graphscene/` in seven `graphscene` tasks, ordered so that the whole-tree `mypy` run passes after each one. The catch-all task (`general`) comes last: it wires the new fixtures into the root `validate:graphscene-schema` scripts and updates the root documents of record.

**How a graph opts in: it declares `writer` on a round. The key set does not change, so the format stays 4.** The schema's `formatVersion` description says *"A change to the key set raises it"* (`graphscene/src/graphscene/schemas/flow-graph.schema.json` → `formatVersion`). So the opt-in reuses the round node's existing keys and moves none of them:
- `writer`, `counter` and `convergingFrom` leave the round node's `required` list. They become a group that is present together or absent together, through the schema's `dependencies`.
- `plan` and `revisionNote` are allowed only on a round that declares `writer`.
- Every graph format 4 accepts today stays valid, with the same meaning. That covers `valid_generic.json`, every negative fixture, and the harness's planning graph `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`, whose `plan_round` declares all three keys.
- So the harness graph opts in **with no edit**. `scripts/generate-flow-graph-v3.mjs` and both format-3 copies are untouched.
- A wire group such as `"review": { … }` was weighed and rejected for two reasons. It changes the key set, so it would force format 5 across the schema, the builder, `FlowGraph.format_version`, every fixture and the generator. It would also break the builder's rule that each serialized key maps to its own snake_case attribute (`.claude/context/graphscene.md` → `## The model and its wire form`).
- In the model, `RoundNode.writer`, `.counter` and `.converging_from` become `| None`, and are `None` together on a plain round.
- The lead *"expanding to plain nodes"* is not taken. The pattern is declared in place, so no expansion step exists. A later builder or YAML shorthand can still emit these same keys.

**The main open question: checks 8 and 9 are split by what the walk itself relies on.** A clause the engine needs in order to walk *any* round stays a **round rule** and is checked on every round. A clause that only shapes a review loop becomes a **review-loop rule**, checked only where the graph opts in. Each clause keeps its check id and its reason text byte for byte, so the cutover can still compare ids with `scripts/check-flow-graph.sh`:
- **Round rules (every round):**
  - check 8, *a gate is a dispatch node*. `open_round` asserts it (`graphscene/src/graphscene/engine/transitions.py` → `open_round`).
  - check 9 (i), *each of a gate's verdict outcomes is a route edge to the round*. `record_gate` records a verdict outcome and never follows its edge (`graphscene/src/graphscene/engine/rounds.py` → *"its edge's `to` is the round and is not followed"*), so a verdict edge aimed anywhere else would be dropped silently.
  - check 9 (iii), *each of a gate's skips goes to the round*. `open_round` skips a gate *"without following a skip's `to`"*.
- **Review-loop rules (only on a round that declares `writer`):**
  - check 8, *the writer is a dispatch node*;
  - check 9 (ii), *each gate declares a pass and a fail outcome*;
  - check 9 (iv), *the writer routes a route edge to the round*;
  - check 9 (v), *nothing but the gates' edges and the writer's edges targets the round*.
- **Check 8's first clause is graph-wide:** *a dispatch node routing a fail verdict with no increment is a gate of exactly one round*. It runs only when the graph declares at least one review loop. A graph without one may route a fail verdict anywhere, and check 3 (`fail-cycle-capped`) still refuses an uncapped fail cycle.
- On a graph that opts in, every clause fires exactly as today.

**The reference checks move with their keys.** `references.py` reports `writer` (`node-known`) and `counter` (`counter-known`) only when they are present. It already treats `plan` and `revisionNote` as optional. `prompt-known` is a generic edge rule and does not change.

**What the engine does for a review loop, and what stays generic.** The pattern lives in one new engine module, `graphscene/src/graphscene/engine/review_loop.py`. It is not public, and it is the only reader of the round's `writer` / `counter` / `convergingFrom` in the walk. A review loop's writer is dispatched with its round's number. A review loop's gate is dispatched with `converging` (`counter >= convergingFrom`). A plain round's gate gets its round's number and `converging` `None`. Four behaviours stay generic, because any fan-out round needs them:
- the held join;
- the round number advancing on a fail close;
- a round's closing edge carrying the closed round's gate records;
- an `Interrupt` carrying `closed_round` back to the resumed dispatch.

The pattern declares no interrupt of its own, so `Walker.next` still consumes an interrupt's `resume_outcome` without looking it up in `vocabulary.outcomes`. `Dispatch`'s fields do not change, so `graphscene/src/graphscene/adapters/walk_json.py` stays at `"version": 1`, and no task edits it or `graphscene/src/graphscene/model/walk_actions.py`.

**`findingsFolder` stays where it is.** It is an opaque host key the engine never reads, like `heartbeat`. The harness's `ui_review` carries one and is not a round gate (`cli/templates/scripts/flows/task_plan_writing.v4.graph.json` → `nodes.ui_review`). Tying the key to the pattern would therefore change the opted-in graph's behaviour.

**The task prompt's "Why" is out of reach of this branch.** Three rules live only in the bash walker `cli/templates/scripts/flow-walker.sh`: `FAIL` requiring `--findings`, `review_mode`, and the per-findings-file arguments. They belong to #418's compatibility entry, and nothing under `cli/` changes here.

**Ordering, because each unit runs the whole-tree `mypy` and no two tasks share a file:**
- Tasks 1–3 add the pattern module, then move every reader of the three keys onto helpers typed `str | None` / `int | None`. Those readers are the walk (Task 2) and the static stage (Task 3). The helpers type-check both before and after the model changes.
- Task 4 then makes the keys optional in the schema, the model and the builder, and adds the plain-round fixtures.
- Tasks 5 and 6 test the plain round, at the engine and then through the public surface.
- Task 7 updates the package README.
- Task 8 (`general`) wires the fixtures into the root scripts and updates the root documents.

**Top risks:** The first risk is that a graph which opts in silently loses a clause. Task 3 changes only *where* each clause runs: every reason string stays byte-identical and every existing static negative still fires. Task 5 plants each review-loop clause on a plain round, asserting it is silent there, and on a review loop, asserting it fires. It also plants each round rule on a plain round and asserts it still fires. The second risk is a mid-branch type break. Tasks 1–3 route every reader through `None`-tolerant helpers before Task 4 changes the field types, so each unit's whole-tree `mypy` run stays clean. The third risk is a silent change to the saved walk state. No task touches `Dispatch` or `walk_json.py`, and Task 6 walks the new plain-round fixture end to end through `Walker` and `FileStateStore`.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below from top to bottom, and the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker.** In every flow that runs the unit loop, that is the commit step, `commit-on-branch.sh --unit`. In the supervised flow, which runs no unit loop, it is the orchestrator itself. No implementer changes a marker here, or edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else, such as sub-step bullets inside per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_graphscene_review_loop_pattern/task_<K>_plan.md`. Entries are ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Add the review-loop pattern module `engine/review_loop.py` _(layer: graphscene)_ _(points: 10)_
2. [x] **Task 2** — Dispatch a round's writer and gates through the review-loop pattern _(layer: graphscene)_ _(points: 8)_
3. [x] **Task 3** — Split checks 8 and 9 into round rules and review-loop rules _(layer: graphscene)_ _(points: 18)_
4. [x] **Task 4** — Make a round's writer, counter and convergingFrom an optional group _(layer: graphscene)_ _(points: 20)_
5. [x] **Task 5** — Test the plain round in the static checks, references and transitions _(layer: graphscene)_ _(points: 20)_
6. [x] **Task 6** — Load and walk the plain-round fixture through the public surface _(layer: graphscene)_ _(points: 15)_
7. [x] **Task 7** — Describe the review-loop pattern in `graphscene/README.md` _(layer: graphscene)_ _(points: 8)_
8. [ ] **Task 8** — Wire the new fixtures into the root scripts and update the root documents _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt (`harness-runs/task_prompts/feat_graphscene_review_loop_pattern_task_prompt.md`): *"`feat_graphscene_review_loop_pattern` turns the review loop from rules the walker enforces on every graph into a pattern a graph opts into."* and *"Its rules checked only where a graph declares it."*

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root:

```
git grep -nE "gate-in-round|round-fan-out|RoundNode|convergingFrom|converging_from|review loop's rules|review-loop pattern" -- 'docs/*.md' 'ROADMAP.md' 'ARCHITECTURE.md' 'README.md' 'graphscene/README.md' 'schemas/**/*.md' '.claude/context/*.md' 'harness-runs/lessons.md'
```

`plugin/` and `cli/templates/` are outside the command. `git grep -il graphscene -- plugin/ cli/templates/` prints nothing, and their "review loop" prose names the harness's own loops, not GraphScene's. Module docstrings and comments under `graphscene/src/` and `graphscene/tests/` are code-level docs, so they are outside the register too: the tasks that edit those modules own them.

**Derivation entry — standing-artifact rows (procedure).** **First step, runnable:** `grep -nE '^## |^- ' harness-runs/lessons.md`. **Artifact:** the standing lessons ledger `harness-runs/lessons.md`. **Traversal:** its topic headings in file order, then the one-line rules under each heading, in order. **Decision rule:** a rule is reached when it names a flow graph, a check over a graph, a test-fixture helper, or a protection that a change withdraws.

**Closure invariant:** every site either entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `ROADMAP.md` → `## Scene products`, the GraphScene row (*"Left: the review loop's rules on the engine, the walker's port onto it, and the harness-side package"*) | — | command, `review loop's rules` | `change` | Task 8 |
| 2 | `docs/development.md` → `## 5. Verifying a change`, **Gate 3**, the paragraph opening *"The generic static checks live at `graphscene.engine.static_check.static_violations`"* | — | command, `gate-in-round` | `change` | Task 8 |
| 3 | `docs/flow-graph-walker.md` → `### Item 7 — every gate every round, closed by a round node`, **Decision.** | — | command, `gate-in-round` | `no-change` | A decision record of the bash walker's format-2 change; `scripts/check-flow-graph.sh` item 8 and format 3 do not change on this branch |
| 4 | `docs/flow-graph-walker.md` → `### Item 8 — a round's gates fan out, and the round node joins`, **Decision.** | — | command, `round-fan-out` | `no-change` | A decision record of the bash walker's format-3 change; `scripts/check-flow-graph.sh` item 9 does not change |
| 5 | `graphscene/README.md` → `## What it is`, the `src/graphscene/model/` row (lists `RoundNode`) | — | command, `RoundNode` | `no-change` | `RoundNode` keeps its name and stays public; the row lists names, not fields |
| 6 | `graphscene/README.md` → `## What it is`, the `src/graphscene/engine/` row (names `gate-in-round`, `round-fan-out`) | — | command, `gate-in-round` | `change` | Task 7 |
| 7 | `schemas/flow-graph-check/README.md` (*"`gate-in-round` — the graph with `architecture_review` dropped from round node `plan_round`'s `gates`"*) | — | command, `gate-in-round` | `no-change` | The bash checker's format-3 fixtures; unchanged until the cutover |
| 8 | `harness-runs/lessons.md` → `## Evidence and measurement` (*"When a check moves to reading a field one producer writes, the same change makes every path that stands in for that producer (a probe's setup, a fixture helper) write the field too."*) | — | procedure, rule names a check and a fixture helper | `no-change` | The plan complies: `build_flow_graph` (Task 4) is the one producer of a writer-less `RoundNode`, and every planted test graph (Tasks 1, 5, 6) goes through it rather than constructing model objects |
| 9 | `harness-runs/lessons.md` → `## Trust checks` (*"Never drop a protection because another route "can already" reach the same target until that route is measured…"*) | — | procedure, rule names a withdrawn protection | `no-change` | The plan complies. No clause is withdrawn from a graph that opts in. Each clause withdrawn from a plain round is one the walk does not rely on, argued clause by clause in `## Context`, and Task 5 asserts both sides |
