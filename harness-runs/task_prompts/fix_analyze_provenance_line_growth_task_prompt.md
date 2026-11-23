## Problem

Every `/devscene:analyze` pass adds to the italic `_Written by /devscene:analyze …_` footer of a conventions document instead of replacing it. Each pass appends its own history: the files it read one by one, the fix passes, the hand edits. The footers have grown to about 5.5 KB in `.claude/context/conventions.md` and about 2.2 KB in `.claude/context/graphscene.md`, against 341 bytes in `.claude/context/cli.md`. Every agent that reads the document pays for that text in its context.

## What the contract asks for today

- `plugin/agents/conventions-writer.md` → `## The document`: "Replace the skeleton's footer with a document-level provenance line naming the mode and what this pass read. It is a different artifact from the per-rule provenance above." `plugin/commands/analyze.md` (4a) says the same.
- `plugin/agents/conventions-reviewer.md` → check 1 requires only that "a document-level provenance line is present".
- Nothing reads the line: classification and `doctor`'s `setup-analysis` use the `devscene:unfilled` HTML-comment marker and the `**What belongs here**` block, and nothing in `cli/src` or `plugin/` parses the footer.

So the line is required, but neither its history nor a file-by-file list is. The wording says "*this* pass" and "replace", yet it doesn't say what happens to an earlier pass's line on a filled document, where there is no skeleton footer left to replace. Writers have filled that gap by adding to the line. The per-rule provenance already carries the file citations the reviewer checks, and git history already records earlier passes.

## Recommendation

1. Rewrite the obligation in `conventions-writer.md` → `## The document`, and its restatement in `analyze.md` (4a), so it covers both cases: a write replaces the skeleton's footer, and a merge replaces the previous provenance line. In both cases the line describes **this pass only**, and earlier passes are not carried forward.
2. Bound its content: the mode, plus the sources **at directory or area level** (for example "from `graphscene/`: README, pyproject, `src/`, test headers"), and no per-file list. Per-file evidence belongs in the per-rule provenance and in the writer's `evidence` return field, which the run report prints.
3. Have `conventions-reviewer.md` check 1 flag a provenance line that carries an earlier pass's history. Give it a concrete correction: cut the line down to this pass.
4. Say who maintains the line after a hand edit, for example a short "edited by hand after #NNN" clause that the next pass replaces like the rest.

The same shape applies to the `project` target's per-section provenance notes in `.claude/CLAUDE.md` (analyze.md (4b)). They have grown the same way.

These files quote one another's wording, so a rule changed in one is an edit to each file that quotes it, and the tree guards over `plugin/**/*.md` should be run.

## Out of scope

Cutting down the footers that already exist is done by hand, separately.
