### 1. On a (4b) section `write`, nothing bounds the provenance note to this pass at directory or area level

**File:** `plugin/commands/analyze.md` → step 4 (4b), the paragraph opening "**(4b) The `project` target, `.claude/CLAUDE.md`.**", at "On `merge` the note replaces that section's previous note, and it is bounded as (4a)'s provenance line is"

The bound reaches the session that composes `.claude/CLAUDE.md`'s two sections through one sentence only, and that sentence is scoped to `merge`:

> On `merge` the note replaces that section's previous note, and it is bounded as (4a)'s provenance line is (`${CLAUDE_PLUGIN_ROOT}/agents/conventions-writer.md` → `## The document`).

"it is bounded" is the second half of the same clause, so it reads as part of the `merge` case. The `write` case is a section whose prompt line is still present ("write it without asking"). For that case the only wording left is the sentence before it: "Each filled section ends with its own one-line provenance note (the mode, and what the pass read)". That sentence does not mention directory or area level and does not forbid a per-file list.

The session cannot reach the bound through the writer's rules either. The paragraph opening "**The two sections this session composes are bound by the writer's own content rules, by reference.**" binds `## The document` "on `write` and on `merge` alike". Its "one adaptation" then removes "the document-level provenance line, whose per-section counterpart is the provenance note above" from what applies. So on a `write`, the session gets neither the writer's bullet nor the (4b) bound.

**What happens:** a first-time `existing`-mode fill of either section is free to write a per-file note. This repository's own `.claude/CLAUDE.md` project-paragraph note shows that shape. Its first clause, from a `write`, is "from `README.md`, `package.json`, `cli/package.json`, `cli/src/cli.ts`, `plugin/.claude-plugin/plugin.json`, …". The task prompt's recommendation 2 (no per-file list) and its closing line ("The same shape applies to the `project` target's per-section provenance notes") ask for the bound on every note. The story plan says Task 3 covers the (4b) notes "on both the grading and the writing side". Only the grading side covers the `write` case. The corpus reviewer's check (1) clause flags the per-file note, so the session pays for a corpus fix round. On `iteration: 2` that finding is applied with no further review.

The code review did not raise this. Its finding 2 covers corpus fixes adding to the note, not the bound on a first write.

Confirmed by reading `plugin/commands/analyze.md` → (4b) and the adaptation paragraph after it. No probe can show what a session composes.

**Fix:** in `plugin/commands/analyze.md` → (4b), replace the two lines

```
   On `merge` the note replaces that section's previous note, and it is bounded as (4a)'s provenance line is
   (`${CLAUDE_PLUGIN_ROOT}/agents/conventions-writer.md` → `## The document`).
```

with

```
   On `merge` the note replaces that section's previous note. On `write` and `merge` alike it is bounded as
   (4a)'s provenance line is (`${CLAUDE_PLUGIN_ROOT}/agents/conventions-writer.md` → `## The document`).
```

`cli/test/conventions-provenance-line.test.mjs` → the test `'analyze.md (4b) points at the bound rather than copying it'` collapses whitespace before matching. After the change its `present` phrases "the note replaces that section's previous note" and "bounded as (4a)'s provenance line is" both still match, and none of its `absent` phrases is introduced. This fix creates and edits no test file, so it runs none. The full suite runs in the Run gates phase.
