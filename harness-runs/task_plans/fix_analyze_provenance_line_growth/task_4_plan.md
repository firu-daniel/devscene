### Task 4 — Add a static check holding the provenance-line wording aligned across the three files

**Goal:** Ship the static check that holds the one provenance-line rule aligned across the three plugin files that now state it: the writer's obligation, the reviewer's check (1), the command's (4a) restatement, and (4b)'s pointer to it, which must stay a pointer. Rewording it in one file without the others then fails a test instead of drifting silently. This is the ledger's rule *"When a change makes agent definitions state one rule in two places, such as a checklist and a table, the same change ships the static check that holds the two aligned."* (`harness-runs/lessons.md` → `## Agent prose`, taught by `feat_must_fix_definition`).

**Depends on:** Tasks 1, 2 and 3. This task asserts the exact phrases they write and edits none of the three files. **Why it ships last although `cli` is first in the configured layer order:** the suite reads text Tasks 1–3 produce, so landing it earlier would commit a failing test, and no task may depend on a later one. The phrases it asserts, each matched after collapsing runs of whitespace to one space (`plugin/commands/analyze.md` is hard-wrapped):

- in `plugin/agents/conventions-writer.md` → `## The document` (Task 1): `describing this pass only`, `it replaces the skeleton's footer`, `it replaces the previous provenance line`, `at directory or area level`, `never a per-file list`, `carries no earlier pass forward`, `edited by hand after #<number>`; and in `## The fix dispatch`: `A fix adds nothing to the provenance line`;
- in `plugin/agents/conventions-reviewer.md` → `## What to verify` (Task 2): `describing this pass only`, `at directory or area level`, `Concrete correction: cut the line down to this pass`;
- in `plugin/commands/analyze.md` → the (4a) slice (Task 3): `describing this pass only`, `at directory or area level`, `carrying no earlier pass forward`;
- in `plugin/commands/analyze.md` → the (4b) slice (Task 3): `the note replaces that section's previous note`, `bounded as (4a)'s provenance line is`, `whose per-section counterpart is the provenance note above`.

Absences it asserts: `Replace the skeleton's footer with a document-level provenance line` in the writer; `skeleton-footer replacement` in the whole of `analyze.md`; and, in the (4b) slice only, `describing this pass only`, `at directory or area level`, `never a per-file list`, `carries no earlier pass forward` and `carrying no earlier pass forward` — (4b) reaches the bound by pointer, so the writer stays its single owner and a copy written there fails here.

### Targets

- `cli/test/conventions-provenance-line.test.mjs` (new). This is the accompanying test, and the whole of this task.

**Work:**

- [ ] Header comment opening with the rule in the words *"The rule this test exists to enforce"* (`.claude/context/conventions.md` → `## The testing bar`). The rule: the conventions writer, the conventions reviewer and the analyze command state the document-level provenance line's bound in the same words, so a rewording in one of them fails here. The header also states:
  - **Not covered:** whether the prose around a phrase still means what it did, and whether any real conventions document's footer meets the bound. That is the reviewer's check (1) at run time, and the existing footers are trimmed by hand.
  - **Not a tree guard:** the suite reads three fixed files rather than a tree, so it owes no `treeGuards` entry (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8's boundary).
- [ ] Read the three files from `WORKSPACE_ROOT` (`cli/test/helpers/fixture.mjs`), as `cli/test/must-fix-triggers-corpus.test.mjs` does, with `node:fs` `readFileSync`. Write nothing and create no fixture. Slice the writer and the reviewer to the named section, from the heading line to the next `## ` heading, so a phrase found in the wrong section does not pass. (4a) and (4b) both sit inside `analyze.md`'s one `## Steps` section with no `## ` heading between them, so slice that file by its sub-step markers instead: the (4a) slice from the line opening `**(4a) The conventions documents**` to the line opening `**(4b) The \`project\` target`, and the (4b) slice from there to the line opening `**(4c) The review`. Fail the test, naming the marker, if any marker is missing. Collapse whitespace runs before matching.
- [ ] One `test(...)` per slice — writer, reviewer, `analyze.md` (4a), `analyze.md` (4b) — each asserting every listed phrase present and every listed absence absent with `node:assert/strict`, plus the whole-file `skeleton-footer replacement` absence for `analyze.md`. The failure message names the file, the section or slice and the phrase.

**Verification:**

- Run this task's own new file from the repository root as one plain foreground command: `npm test --workspace cli -- test/conventions-provenance-line.test.mjs`. It passes, and the TAP counts show every case ran.
- Re-point one phrase constant at a spelling none of the three files carries, run the file again and see it fail naming that file and phrase, then restore the constant. A suite that cannot fail is no check.
- The file follows the `cli/test/<kebab-case>.test.mjs` pattern (`.claude/CLAUDE.md` → `## File naming conventions`), and it imports nothing outside `node:` builtins and `./helpers/fixture.mjs`.
