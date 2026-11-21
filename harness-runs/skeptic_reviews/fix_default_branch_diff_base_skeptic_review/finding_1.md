### 1. The suite's RED ONCE record locates its failing site by a line coordinate

**File:** `cli/test/diff-base-corpus.test.mjs` (the file's opening doc comment, the `RED ONCE (no-bare-base)` paragraph) — "`plugin/agents/skeptic-reviewer.md:90`"

**Problem.** The suite's header records its red run as listing `` `plugin/agents/skeptic-reviewer.md:90` ``. That is a line coordinate in a durable code comment. `plugin/instructions/finding_grades.md` → `## Should Fix` grades that a Should Fix whether or not it is stale. It resolves today: line 90 of `plugin/agents/skeptic-reviewer.md` is the `git diff origin/<default_branch>...HEAD --stat` line of `## Process` step 1. Any edit above that line in `plugin/agents/skeptic-reviewer.md` silently moves it, and the record then names the wrong line. No other suite under `cli/test/` writes a `<file>.md:<line>` coordinate into its header comment. Every other hit is fixture data inside a test body.

**Fix.** Edit the `RED ONCE (no-bare-base)` paragraph of the header comment only, and change no other text in the file. Replace:

```
 * only, then restored: `no-bare-base` failed its `deepEqual`, listing
 * `plugin/agents/skeptic-reviewer.md:90`.
```

with:

```
 * only, then restored: `no-bare-base` failed its `deepEqual`, listing
 * `plugin/agents/skeptic-reviewer.md` at the `--stat` line of `## Process` step 1.
```

This fix edits only this test file, so this file is the one test it runs.
