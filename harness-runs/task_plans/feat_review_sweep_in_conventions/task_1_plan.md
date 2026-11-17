### Task 1 — Write the `.claude/review-sweep.md` skeleton from `init` and reserve the `sweep` analyze target

**Goal:** Make `devscene init` write the adopter-owned sweep document as a `create-if-absent` skeleton at `.claude/review-sweep.md`. Make it carry the sweep row format and the two-part untouched-skeleton markers, and make `sweep` a reserved analyze target so the skeleton's footer can name `/devscene:analyze sweep`.

**Where this task stops.** It ships the skeleton and its generator only. Four later tasks consume them:
- the script that parses the rows (Task 2);
- the `doctor` check that reads `REVIEW_SWEEP_PATH` and grades the skeleton (Task 4);
- the analyze command's `sweep` target (Task 7);
- the documentation of record (Task 10).

It writes nothing under this repository's own `.claude/`, which is the user's after merge (story index, `Manual setup required:`).

### Targets

- `cli/templates/claude/review-sweep.md` (new) — the skeleton.
- `cli/src/generators/claudeContext.ts` — `REVIEW_SWEEP_PATH`, the enqueue, `RESERVED_ANALYZE_TARGETS`.
- `cli/src/core/writer.ts` — the re-run-contract table in the module header.
- `cli/templates/claude/README.md` — the directory's statement of what `init` copies.
- `cli/test/init.test.mjs` — the accompanying cases.

**Work:**

- [ ] `cli/templates/claude/review-sweep.md` (new). Mirror the shape of `cli/templates/claude/context/layer.md`: an H1, the `> **Read this when:** … **Skip when:** …` banner, a **Purpose** paragraph, the `**What belongs here**` block, a stack-independent rule block, the table, then a footer and the `<!-- devscene:unfilled -->` marker as its last line.
  - **Banner.** Read when you are the end-of-branch reviewer or the analyze pass filling it. Skip when you are a per-unit implementer or reviewer, who never load it.
  - **`**What belongs here**` items:** which escape classes this project has; for each, the regex that catches it, the layer paths it covers, the owner sites it exempts, and what a hit is a candidate for.
  - **Worked examples for a front-end adopter**, a **bullet list**, never a table. Carry the seven classes the current `plugin/agents/branch-reviewer.md` → `### Pass 0 — the deterministic sweep` table names, with each class's "What a hit is a candidate for" text: styling literal, timing literal, duplicated shared constant, raw console / print call, cast instead of mapping, invocation from the wrong layer, open literal set. State that they are examples, not defaults, and that a project's classes come from its own conventions.
  - **Rule block.** The row format below, stated verbatim. Then: a hit is a lead to verify in context, never a finding by itself. Rows are maintained by the user, by hand or with the command in the fenced block that follows that sentence. The block holds `{{analyzeInvocation}}` alone on one line, rendered `/devscene:analyze sweep`, and the sentence points at the block rather than naming the invocation inline. A lesson in the lessons ledger is not a row. The rows are read as `<default branch>` commits them.
  - **No inline invocation anywhere in the skeleton** (`harness-runs/lessons.md` → `## Adopter-facing documentation`: every command an adopter is meant to run sits in a fenced block, one command per line). Every command the skeleton tells an adopter to run sits in its own fenced block, one command per line, and no sentence carries one inline.
  - **Row format** (the story index's `## Context` wire, restated here so this task owns the skeleton's copy):
    - the rows sit in the one table directly under the exact heading `## Sweep rows`;
    - the header row is exactly `| Escape class | Regex | Covers | Exempts | A hit is a candidate for |`, then the separator row;
    - the table ends at the first line not beginning with `|`;
    - `Regex` is exactly one backtick code span holding a `grep -E` (POSIX ERE) pattern. A literal `|` is written `\|`, and no backtick can appear in it;
    - `Covers` is code-spanned repo-relative paths, each a `layers[].path` value or a path beneath one, separated by `, `, with `.` for the whole repository;
    - `Exempts` is code-spanned repo-relative paths or pathspec globs separated by `, `, or `—` for none.
  - **`## Sweep rows`** carries the header and separator rows and no data row.
  - **Footer.** The `layer.md` footer's meaning, adapted to the fenced form: a sentence saying to run the command in the block below, or to replace everything above by hand, then a fenced block holding `{{analyzeInvocation}}` alone on one line. Use `{{…}}` tokens only where `render` supplies a value.
- [ ] `claudeContext.ts`:
  - Export `REVIEW_SWEEP_PATH = \`${CLAUDE_DIR}/review-sweep.md\``, with a doc comment in the style of `TASK_OFFER_PATH`'s. The plugin dereferences the basename by name (`branch-reviewer`, the analyze command, `review-sweep.sh`), so renaming it is a breaking change. `doctor` imports it.
  - In `writeClaudeContext`, enqueue it on every run, gated on no phase: `create-if-absent`, label `review sweep skeleton`, content `render('review-sweep.md', { analyzeInvocation: \`${ANALYZE_COMMAND} sweep\` })`. Apply the same `forceOverride: 'never'` keep the conventions stubs get from `keepsRescuedBackup`, since it carries the same two markers.
  - Do **not** add it to `collectStubs` or `routingRows`. The routing table must not name it.
  - Add `'sweep'` to `RESERVED_ANALYZE_TARGETS`, with a `reservedMeaning` arm: "the review-sweep document".
  - Update the module header's first paragraph, the doc comment on `RESERVED_ANALYZE_TARGETS` ("the three" becomes the four it now lists), and the `writeClaudeContext` selection bullets.
- [ ] `writer.ts` header → `## The re-run contract, per artifact`: add a `.claude/review-sweep.md` row, `create-if-absent`. Its reason: `/devscene:analyze` fills it and the adopter maintains it; filled is the same two-part test as a conventions stub; and the `--force` keep as for a stub.
- [ ] `cli/templates/claude/README.md`: name the review-sweep skeleton among what `init` copies into `.claude/`, and say it is filled by `/devscene:analyze sweep` under the same marker contract.
- [ ] `init.test.mjs`. Grep the file for every assertion over the reserved-target list or its rendered text and extend it to the four names. Add cases:
  - a fresh `init` writes `.claude/review-sweep.md` carrying both `<!-- devscene:unfilled -->` and `**What belongs here**`, the exact `## Sweep rows` heading and the exact header row, and a footer naming `/devscene:analyze sweep`;
  - the rendered skeleton carries `/devscene:analyze sweep` only as a fenced line: every line containing it is exactly `/devscene:analyze sweep` and sits between a pair of fence lines, and no prose line contains it;
  - the generated `.claude/CLAUDE.md` does not name `review-sweep.md`;
  - a second unforced `init` leaves the file byte-identical;
  - `--force` over an adopter-edited copy takes a `.bak` first, beside the idempotence assertion, as `.claude/context/cli.md` → `## What "done" means here` requires of a `create-if-absent` artifact.

**Verification:**

- `npm test --workspace cli -- test/init.test.mjs` passes. It is this task's own edited test file.
- `bash scripts/typecheck.sh` exits zero.
- `git grep -n -F 'review-sweep' -- cli/src/generators/claudeContext.ts` shows the path only in `REVIEW_SWEEP_PATH`'s declaration and its uses, never in a routing row.
