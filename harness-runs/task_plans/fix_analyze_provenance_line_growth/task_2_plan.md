### Task 2 — Have `conventions-reviewer.md` check (1) flag a provenance line carrying history

**Goal:** Make the conventions reviewer grade the provenance line's content as well as its presence. A line carrying an earlier pass's history, or a per-file list, is a finding with a concrete correction: cut the line down to this pass. Apply the same clause to the `project` target's per-section provenance notes in the corpus pass.

**Depends on:** Task 1, which rewrites `plugin/agents/conventions-writer.md` → `## The document` so that the provenance line is *"describing this pass only"*, names what the pass read *"at directory or area level"*, is *"never a per-file list"* and *"carries no earlier pass forward — no earlier mode, fix pass or hand-edit clause"*, while a hand editor may end it with one clause such as *"`edited by hand after #<number>`"*, which the next pass replaces. This task grades exactly that contract and restates those phrases byte-for-byte. It does not reword the writer's rule, which is Task 1's, and it does not touch `plugin/commands/analyze.md`, which is Task 3's. Task 4 adds a `cli/test` suite asserting `describing this pass only`, `at directory or area level` and `Concrete correction: cut the line down to this pass` inside this file's `## What to verify`, so keep them spelled exactly as given.

### Targets

- `plugin/agents/conventions-reviewer.md` — `## What to verify` check (1), and `## The corpus pass — what to verify` (the `target: project` exception's **(1)** bullet).

**Work:**

- [ ] `## What to verify`, check (1) ("**The document contract holds.**"). Replace the clause "a document-level provenance line is present" with a clause that grades presence and content, carrying this text:

  > a document-level provenance line is present, describing this pass only — one naming an earlier pass (a previous mode, a merge or fix pass, a hand-edit clause carried over from before this pass) or a per-file list of what was read is the finding. **Concrete correction: cut the line down to this pass — its mode and what it read at directory or area level.**

  Keep every other clause of check (1) unchanged: the banner, the example, the marker, `## Not determined`, and the `prior_prompts` clause with its `none` / `n/a` meanings. The reviewer grades a line this dispatch's pass has just written, so any `edited by hand after #<number>` clause on it was carried over from before the pass, and is the finding. The writer's rule admits that clause only between passes, added by a hand editor, and the next pass replaces it.
- [ ] `## The corpus pass — what to verify`, the `target: project` exception's list of checks that "do not apply". Amend the **(1)** bullet ("no skeleton contract: no banner, no seeded example, no `prior_prompts`.") so it ends by saying that check (1)'s provenance-line clause alone still applies, to each composed section's closing one-line provenance note (`${CLAUDE_PLUGIN_ROOT}/commands/analyze.md` → `(4b)`). Keep the bullet in that list, and do not add (1) to the list of checks the exception applies, since the rest of (1) still does not apply.
- [ ] Leave check (12)'s correction "or move the name into the provenance line" as it is. Moving an agent name into a rule's citation adds no history clause.

**Verification:**

- `grep -nF "describing this pass only" plugin/agents/conventions-reviewer.md` hits inside check (1), and the same phrase hits in `plugin/agents/conventions-writer.md`, so the reviewer grades the writer's own wording rather than a paraphrase.
- `grep -nF "at directory or area level" plugin/agents/conventions-reviewer.md` hits inside check (1), and the same phrase hits in `plugin/agents/conventions-writer.md`.
- `grep -nF "Concrete correction: cut the line down to this pass" plugin/agents/conventions-reviewer.md` hits once, inside check (1).
- The `target: project` exception still names exactly the checks it applied before this change, and its **(1)** bullet now names the provenance-note clause with the `(4b)` citation.
- Read check (1) against Task 1's writer bullet and confirm there is no case the writer is told to produce that the reviewer flags. A fresh `write` line, and a `merge` line that replaced its predecessor including any hand-edit clause, both pass.
