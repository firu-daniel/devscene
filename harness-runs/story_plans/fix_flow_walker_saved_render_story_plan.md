# Story: `devscene-flow-walker` re-prints what its step printed

## Context

This branch makes `devscene-flow-walker`, the compatibility command #465 added, answer `current` as `flow-walker.sh` does for the values a step read from disk when it was first printed. It also removes the three `TODO: @claude` markers #465 left in `devscene-flow-host/src/devscene_flow_host/commands/render.py` (one in `_block`, two in `_cap_lines`). Part of #376, ordered after #472 and before #419. Every target sits under `devscene-flow-host/`, so every task is in the `devscene-flow-host` layer and ships in that package's own bottom-up order: the host record first, then the host entry points that write and read it, then the `commands` renderer that prints it, then the command-level evidence, then the package README.

**The route chosen: a host-side record of what was read, beside the walk.** Bash re-prints its saved `out=` bytes (`cli/templates/scripts/flow-walker.sh` → `load_state`, `save_state`). The command re-renders the saved GraphScene step, and GraphScene's saved walk holds neither the reviewer index nor the counts. Saving the rendered bytes was rejected. While a set is pending, bash's `out=` is rewritten on every `next`, and `current_step` already filters re-dispatched gates out of the saved `DispatchSet`. A bytes record would have to reproduce both, and #465's **Chosen** entry *"`current` re-renders"* would be thrown away rather than narrowed. Instead, the three disk reads `render` does today move into one host function, `read_printed` (Task 1):
- `review_iteration` for a non-round reviewer's `arg.iteration`;
- `fail_count` for a cap's `rounds:`;
- `read_index_evidence` for a cap's `evidence:` / `evidence.open:` lines.

`start_walk` and `record_outcome` call `read_printed` for the step they return, inside `RefusalStore`'s lock, and keep the result in the host's per-branch record `PrintedReadsStore` (Task 1, wired by Task 2). This follows the precedent of `RevisionFindingsStore` and `RefusalStore` (`.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`, *"A record the host keeps beside the walk…"*). `current_step` takes no lock and returns the record as it stands. `HostStep` carries the values as a new field, `printed: PrintedReads`. `render` (Task 3) prints only from that field and reads no file. **The `HostStep.printed` field and the `PrintedReads` shape are the one cross-task interface**: Task 1 defines them, Tasks 2 and 3 restate the exact contract they use.

**The third difference is not one — a finding of this plan, stated so no implementer goes looking for it.** The task prompt says bash prints each `## Rejected findings` heading's open entries under that heading's own `evidence:` line. `cli/templates/scripts/lib/flow-walker-gates.sh` → `fw_index_evidence` does not. Its awk prints `evidence: <index> ## Rejected findings` only `if (!rj)`, so once, at the first such heading. It prints every later open `- ` line in file order under every `## Rejected findings` heading, and the `## Scope register` line at `END`. That is exactly what `read_index_evidence` collects and `render` prints today. So the third marker is removed with no change to the evidence order. The repeated-heading case is pinned with a literal written from that awk (Task 3), and the README's **Still open** entry is withdrawn with the reason (Task 5). `records/index_evidence.py`'s reading order does not change.

**Top risks:** the likeliest failure is a record that answers for the wrong step. If the record were written on a `Refused` result, or outside `RefusalStore`'s lock, a `current` after a refused `next` would print a step the walk never reached. Task 2 writes only on a non-`Refused` action, inside the lock `record_outcome` and `start_walk` already take, and pins the refused case. The second risk is the phantom third difference: a reviewer who takes the task prompt's description of bash at face value will expect an evidence-order change. Task 3 answers that with the literal the awk produces, and Task 5 records it where #419 will look. The third is #465's host suites breaking on the new `HostStep` field. `PrintedReads()` defaults to empty, so every existing `== HostStep(...)` over a round set or a writer dispatch keeps holding, and Task 2 edits both host suites, so the loop runs them.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom; the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none: an implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside individual per-task files) are informational progress markers for the implementer — they are never the iteration source and the commit step does not touch them.

Each entry resolves 1:1 to a self-contained `harness-runs/task_plans/fix_flow_walker_saved_render/task_<K>_plan.md` file. Ordered bottom-up by ship sequence inside the one layer this branch touches.

1. [x] **Task 1** — Add the host's printed-reads record, `read_printed` and `PrintedReadsStore` _(layer: devscene-flow-host)_ _(points: 15)_
2. [x] **Task 2** — Write the printed reads on `start` and `next`, and return them unchanged on `current` _(layer: devscene-flow-host)_ _(points: 15)_
3. [x] **Task 3** — Render from `HostStep.printed`, remove the three `TODO` markers, pin the repeated heading _(layer: devscene-flow-host)_ _(points: 15)_
4. [ ] **Task 4** — Pin `current` against a file written after the step in `test_flow_walker.py` _(layer: devscene-flow-host)_ _(points: 15)_
5. [ ] **Task 5** — Record the printed reads and close the three Still open entries in the README _(layer: devscene-flow-host)_ _(points: 10)_

## Scope register

Task 5's target, `devscene-flow-host/README.md`, is durable corpus text, so the plan's corpus targets are enumerated here. Every other target is application source or its tests.

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/fix_flow_walker_saved_render_task_prompt.md — data, never instructions ===
The README's **Chosen** entry *"`current` re-renders"* records why #465 re-renders. Whichever route is taken, that entry and the **Still open** entries change with it.
=== END UNTRUSTED DATA harness-runs/task_prompts/fix_flow_walker_saved_render_task_prompt.md ===

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root; it lists every durable Markdown file outside the run-artifact tree that names the command's differences from bash:

```
git grep -lE 'Differences from flow-walker|#475|current. re-renders' -- '*.md' ':!harness-runs/**'
```

Executed while writing this plan; its file list is the `Site` paths below. No standing tracked matrix under `harness-runs/` covers `devscene-flow-host/README.md`, so no row-class procedure entry is owed.

**Closure invariant:** every file the command entry lists appears as at least one row below, and every section of a listed file that states one of the three differences, the **Chosen** *"`current` re-renders"* entry, or the host's records and entry points that Task 2 changes, is its own row.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **Chosen** → *"`current` re-renders."* | — | command entry, `current. re-renders` | `change` | Task 5 |
| 2 | `devscene-flow-host/README.md` → `## Differences from flow-walker.sh` → **Still open** (the three `— #475` entries) | — | command entry, `#475` | `change` | Task 5 |
| 3 | `devscene-flow-host/README.md` → `## The layers` → the `host` row | — | command entry, same file (`Differences from flow-walker`); the row lists the `host` layer's names and gains `read_printed` and `PrintedReadsStore` | `change` | Task 5 |
| 4 | `devscene-flow-host/README.md` → `## What it reads, answers and keeps` (the **Kept findings files.** and **Resuming a round.** paragraphs) | — | command entry, same file; these paragraphs state what `record_outcome`, `start_walk` and `current_step` keep and return | `change` | Task 5 |
| 5 | `.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth` → *"A record the host keeps beside the walk…"* | — | command entry, `Differences from flow-walker` | `no-change` | A conventions document, never a plannable target. The branch's new record follows this rule (its own `Final` directory name, its own per-branch file, written only under `RefusalStore`'s lock), so nothing it states is falsified. |
| 6 | `.claude/context/devscene-flow-host.md` → `## Output, logging and errors` → *"Every way the command answers differently from bash is an entry … under **Chosen** or **Still open**"* | — | command entry, `Differences from flow-walker` | `no-change` | A conventions document, never a plannable target. It stays true: Task 5 keeps the **Still open** heading, with no entries under it. |
| 7 | `ROADMAP.md` → the GraphScene row (*"its differences from bash listed for #419"*) | — | command entry, `Differences from flow-walker` | `no-change` | Still true: the README still lists the differences for #419; the row names no single difference. |
