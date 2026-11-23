### 1. `conventions-reviewer.md` says check (1) both does and does not run on the corpus pass's `project` member

**File:** `plugin/agents/conventions-reviewer.md` → `## The corpus pass — what to verify`, the paragraph opening "**The second of those exceptions is `.claude/CLAUDE.md` (`target: project`).**" and its bullet "- **(1)** — no skeleton contract"; also `## Invocation contract`, the sentence "checks (1) and (2) are document-pass checks and do not run here"

Task 2 added one sentence to the `(1)` bullet under the `project` member: *"Its provenance-line clause alone still applies, to each composed section's closing one-line provenance note"*. Three other statements in the same file still say check (1) does not run there, and none of them was changed:

1. `## Invocation contract`, the paragraph opening "**The three `prior_*` values are not sent on a corpus dispatch and are not owed:**", says *"checks (1) and (2) are document-pass checks and do not run here"*. It has no exception.
2. The `project` member paragraph lists what applies to that member: *"Over that member only, also apply checks **(3), (4), (7), (8), (9), (10), (12), (13), (14) and (15)**"*. Check (1) is not in the list.
3. The same paragraph then says *"Five do not apply to it, each for its own reason:"*, and `(1)` is the first of the five. Its new sentence says part of it does apply.

A reviewer that grades from the enumerated list, which is the sentence that says what to apply, never grades a `.claude/CLAUDE.md` section's provenance note. The note history Task 3 bounds in `plugin/commands/analyze.md` → (4b) is then never flagged. The story plan's second top risk says Tasks 2 and 3 cover the (4b) notes "on both the grading and the writing side", and this leaves the grading side covered only if the reviewer happens to give the bullet precedence over the list.

Confirmed by reading the file. No probe can exercise how an agent resolves the conflict.

**Fix:** state the exception at each of the three places, and keep the `(1)` bullet as the reason the rest of the check is skipped.

- In `## Invocation contract`, replace
  `checks (1) and (2) are document-pass checks and do not run here.`
  with
  `checks (1) and (2) are document-pass checks and do not run here, apart from check (1)'s provenance-line clause on a `project` member (`## The corpus pass — what to verify`).`
- In the `project` member paragraph, replace
  `Over that member only, also apply checks **(3), (4), (7), (8), (9), (10), (12), (13), (14) and (15)** — and over`
  with
  `Over that member only, also apply checks **(3), (4), (7), (8), (9), (10), (12), (13), (14) and (15)**, and check (1)'s provenance-line clause to each composed section's closing one-line provenance note (`${CLAUDE_PLUGIN_ROOT}/commands/analyze.md` → `(4b)`) — and over`
- Replace the bullet
  `- **(1)** — no skeleton contract: no banner, no seeded example, no `prior_prompts`. Its provenance-line clause alone still applies, to each composed section's closing one-line provenance note (`${CLAUDE_PLUGIN_ROOT}/commands/analyze.md` → `(4b)`).`
  with
  `- **(1)**, apart from its provenance-line clause — no skeleton contract: no banner, no seeded example, no `prior_prompts`.`

`cli/test/conventions-provenance-line.test.mjs` reads only `## What to verify` from this file, so none of these edits affects it. This fix creates and edits no test file, so it runs none. The full suite runs in the Run gates phase.
