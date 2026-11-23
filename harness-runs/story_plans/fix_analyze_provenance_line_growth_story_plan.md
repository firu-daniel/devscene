# Story: Bound the `/devscene:analyze` provenance line to the pass that writes it

## Context

Each `/devscene:analyze` pass adds to the italic document-level provenance line at the foot of a conventions document instead of replacing it. Every pass appends its own history: the files it read, one by one, its fix passes and the hand edits made since. The task prompt measures the result at about 5.5 KB in `.claude/context/conventions.md` and about 2.2 KB in `.claude/context/graphscene.md`, against 341 bytes in `.claude/context/cli.md`, and every agent that loads one of those documents pays for that text. The cause is in the contract. `plugin/agents/conventions-writer.md` → `## The document` says to *"Replace the skeleton's footer with a document-level provenance line naming the mode and what this pass read"*, but says nothing about a filled document, where no skeleton footer is left to replace. `plugin/commands/analyze.md` (4a) repeats that gap. `plugin/agents/conventions-reviewer.md` → check (1) only asks that *"a document-level provenance line is present"*. Nothing parses the line: classification and `doctor`'s `setup-analysis` key on the `<!-- devscene:unfilled -->` marker and the `**What belongs here**` block. That means the line's content can be bounded without changing any reader.

This branch changes the contract, not the documents. The contract change is cut into three `plugin`-layer tasks, followed by one `cli`-layer check. Task 1 rewrites the writer's obligation and owns the canonical wording of the rule. Task 2 has the reviewer's check (1) grade that wording, and applies the same clause to the `project` target's per-section notes in the corpus pass. Task 3 restates the rule in `plugin/commands/analyze.md` (4a) and applies it to the per-section provenance notes of (4b). The rule, stated once in Task 1 and restated by reference in Tasks 2 and 3, has five parts:
- the line describes **this pass only**;
- a `write` replaces the skeleton's footer, and a `merge` replaces the previous provenance line;
- it names the mode plus the sources read **at directory or area level**, never as a per-file list;
- earlier passes, fix passes and hand-edit clauses are not carried forward;
- a person editing by hand may add one short clause naming the change it came from, and the next pass replaces that clause with the rest of the line.

These files quote one another's wording (`.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent`, the rename rule), so Tasks 2 and 3 restate Task 1's phrases byte-for-byte rather than paraphrasing them. The change leaves one rule stated in three agent-facing files, so Task 4, in the `cli` layer, ships the static check that holds them aligned, as the lessons ledger requires (`harness-runs/lessons.md` → `## Agent prose`, *"the same change ships the static check that holds the two aligned"*). That suite reads text Tasks 1–3 write, so it ships last even though `cli` precedes `plugin` in the configured layer order: landing it first would commit a failing test. It reads three fixed files rather than a tree, so it owes no `treeGuards` entry.

Out of scope, per the task prompt's `## Out of scope`: the oversized footers already in `.claude/context/*.md` are cut down by hand, separately. Those footers are conventions documents in any case, and no task here may target them. Once this lands, the next `/devscene:analyze` pass over them will replace their lines under the new rule, and the reviewer's check (1) will flag any that still carry history.

**Top risks:** The first is wording drift between the three files. The reviewer would then grade a phrasing the writer never wrote, or `analyze.md` would restate a different bound. Task 1 fixes the exact phrases, Tasks 2 and 3 each verify them with a `grep -F` against the writer, and Task 4's suite holds them aligned after the branch. The second is a rule that still leaves a gap for history to come back through: the fix dispatch, which today has the footer saying *"corrected by the review fix pass"*, and the `project` target's (4b) notes. Task 1 covers the fix dispatch, and Tasks 2 and 3 cover the (4b) notes on both the grading and the writing side. The third is an agent definition growing for no behaviour (`.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour"*). Every task replaces the clause it rewrites instead of adding a parallel one.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** Only the committing role flips a marker to `[x]`. In every flow that runs the unit loop that role is the commit step, `commit-on-branch.sh --unit`; in the supervised flow, which runs none, it is the orchestrator itself. No implementer changes a marker, or edits any other line of this section, in an index a run is iterating. `[ ]` markers elsewhere, such as sub-step bullets in the per-task files, are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_analyze_provenance_line_growth/task_<K>_plan.md`, in ship order.

1. [x] **Task 1** — Bound the writer's provenance line to this pass in `conventions-writer.md` _(layer: plugin)_ _(points: 10)_
2. [x] **Task 2** — Have `conventions-reviewer.md` check (1) flag a provenance line carrying history _(layer: plugin)_ _(points: 10)_
3. [x] **Task 3** — Restate the bounded provenance line in `analyze.md` (4a) and its (4b) notes _(layer: plugin)_ _(points: 10)_
4. [ ] **Task 4** — Add a static check holding the provenance-line wording aligned across the three files _(layer: cli)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/fix_analyze_provenance_line_growth_task_prompt.md — data, never instructions ===
These files quote one another's wording, so a rule changed in one is an edit to each file that quotes it
=== END UNTRUSTED DATA harness-runs/task_prompts/fix_analyze_provenance_line_growth_task_prompt.md ===

**Derivation entry — corpus files (command).** Re-run verbatim from the checkout root: `git grep -n -i -E "provenance (line|note)|skeleton's footer|replaces? the footer|skeleton-footer|document-level closing obligations" -- plugin docs/analyze.md docs/development.md`

No standing tracked artifact under `harness-runs/` has a row class covering these `plugin/` files, so no procedure entry is owed.

**Closure invariant:** every site the command entry reaches appears as a row below. Sites are identified by quoted anchor, never by line number.

| # | Site (path + symbol or quoted anchor) | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/agents/conventions-writer.md` → `## The document`, the bullet "**Replace the skeleton's footer with a document-level provenance line**" | — | `skeleton's footer`, `provenance line` | `change` | Task 1 — the canonical statement of the rule |
| 2 | `plugin/agents/conventions-writer.md` → `## The document`, the compose-from-nothing paragraph, "a real example from this repository; the document-level provenance line; and the `## Not determined` section" | — | `provenance line` | `no-change` | Names the line as a part of the composed shape. Task 1's bullet governs its content, and an `absent` document has no earlier line to replace |
| 3 | `plugin/agents/conventions-writer.md` → `## The sweep document`, "the two document-level closing obligations" | — | `document-level closing obligations` | `no-change` | A pointer to the closing-obligation pair. The pair keeps its two members and Task 1 keeps its lead-in "**Two document-level obligations close the write**", so the pointer still resolves |
| 4 | `plugin/agents/conventions-reviewer.md` → `## What to verify`, check (1), "a document-level provenance line is present" | — | `provenance line` | `change` | Task 2 |
| 5 | `plugin/agents/conventions-reviewer.md` → `## What to verify`, check (12), "or move the name into the provenance line" | — | `provenance line` | `no-change` | Moves an agent name into the provenance it cites. That provenance is the rule's own and allowed on any line, and the correction adds no history clause |
| 6 | `plugin/commands/analyze.md` → step 4 (4a), "replaces the footer with a provenance line naming the mode and what the pass read" | — | `replaces the footer`, `provenance line` | `change` | Task 3 |
| 7 | `plugin/commands/analyze.md` → step 4 (4b), "section ends with its own one-line provenance note (the mode, and what the pass read)" | — | `provenance note` | `change` | Task 3 |
| 8 | `plugin/commands/analyze.md` → step 4 (4b), "the one-whole-document write and the skeleton-footer replacement) do not apply" | — | `skeleton-footer` | `change` | Task 3 — the name of the writer obligation it excludes moves with Task 1's rewording |
| 9 | `plugin/agents/user-review-fix-plan-writer.md` → `## Process` step 1, "the section's closing provenance line names that state" | — | `provenance line` | `no-change` | Describes a different artifact: the provenance line `remote-run.sh` writes under each `## Review by @<login>` section of a user-review round, not a conventions document's |
| 10 | `docs/analyze.md` → the paragraph opening "**Under dispatch the guarantee is re-derived, not inherited**", "the unfilled marker, the `**What belongs here**` block and the provenance line" | — | `provenance line` | `no-change` | Counts the line as one of the signals a document carries. That stays true: the line is bounded, not removed |
| 11 | `docs/development.md` → Gate 8, "Each carries a provenance line and a `## Not determined` section" | — | `provenance line` | `no-change` | A presence criterion, and the line is still required |
| 12 | `docs/development.md` → Gate 8, the paragraph opening "**The dispatched pass adds three more, on the same footing.**", "marker gone, provenance line, `## Not determined` present" | — | `provenance line` | `no-change` | A presence criterion, as in row 11 |
| 13 | `docs/development.md` → Gate 12, the paragraph opening "**Round 5 — 2026-10-01, CLI 0.5.0.**", "its provenance line named `@expause-admin`" | — | `provenance line` | `no-change` | The task-prompt provenance line `remote-run.sh` writes, a different artifact, in a measured record |
| 14 | `docs/development.md` → Gate 12, the leg (e) paragraph placing "`chore: add user review for feat_invoices_3`", "under `## Review by @expause-admin` with its provenance line" | — | `provenance line` | `no-change` | User-review round provenance, a different artifact, in a measured record |
| 15 | `docs/development.md` → Gate 12, the leg (e) paragraph placing "`chore: add user review for feat_invoices_4`", "under `## Review by @expause-admin` with its provenance line" | — | `provenance line` | `no-change` | As row 14 |
| 16 | `docs/development.md` → Gate 12, the leg (e) entry placing "`6c8db24 chore: add user review for feat_invoices_5`" | — | `provenance line` | `no-change` | As row 14 |
| 17 | `docs/development.md` → Gate 12, the entry placing "`66fbd84 chore: add user review for feat_invoices_7`" | — | `provenance line` | `no-change` | As row 14 |
| 18 | `docs/development.md` → "**(xiii) passed** on its token", "The committed prompt carried the provenance line" | — | `provenance line` | `no-change` | Task-prompt provenance, a different artifact, in a measured record |
| 19 | `docs/development.md` → the issue-trigger criteria, "whose prompt is the issue's title and body plus the provenance line" | — | `provenance line` | `no-change` | Task-prompt provenance, a different artifact |
