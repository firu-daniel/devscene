### Task 5 — Teach `conventions-writer` the `sweep` target and the sweep row format

**Goal:** Let one `conventions-writer` dispatch, `pass: document` with `target: sweep`, write `.claude/review-sweep.md`. Its escape classes and regexes come from the repository's real code and its stated conventions, not from the UI defaults the old in-agent stub carried.

**Depends on:** Task 1, whose skeleton is what this dispatch normally finds at `document_path`. The skeleton carries the `**What belongs here**` block, a stack-independent rule block stating the row format, and the empty `## Sweep rows` table, so the existing `prior_document` / `prior_prompts` / `prior_rule_block` machinery applies unchanged. The row format this writer emits is the wire that Task 2's script parses, and it is restated in full in the Work below.

**Where this task stops.** The dispatch that sends `target: sweep`, and when it is sent, is **Task 7's** (`plugin/commands/analyze.md`). The grading of what this writer emits is **Task 6's**. This task changes no return field: `shared_document_divergences` is `[]` on a `target: sweep` dispatch, so `plugin/schemas/conventions-writer.return.json` is unchanged.

### Targets

- `plugin/agents/conventions-writer.md`

**Work:**

- [ ] `## Resolved values`:
  - the `<layer_names>` row: "Your `target` is one of them, the reserved word `conventions`, or the reserved word `sweep`";
  - the paragraph under the table ("No row above resolves from a conventions document…"): add one sentence that on `target: sweep` the conventions documents are read as **evidence**, which `## The sweep document` states.
- [ ] `## Invocation contract`:
  - the write table's `target` row adds `sweep` for the review-sweep document `.claude/review-sweep.md`;
  - the `scope` row: the **repository root** when the target is `sweep`, as for the shared document.

  Keep the one-file rule of `## Scope` as it stands, since `document_path` is still the only file written. Edit the frontmatter `description:` only as far as naming that one dispatch may write the review-sweep document.
- [ ] Add `## The sweep document`, after `## The document`. It applies only on `target: sweep`, and every rule of `## The document`, `## The fix dispatch` and `## House rules` still applies to it except where this section says otherwise.
  - **Evidence:** the code in `scope` minus `excluded_paths`, plus every conventions document `<layer_path_map>` names and the shared cross-layer document, read as the project's stated rules.
  - **One row per escape class:** a construct the conventions documents make mandatory or give a single owner, written in the code where it should not be. Each class is derived from those documents and the code, never from the skeleton's worked examples. `<state_dir>` and its lessons ledger are never a row's source.
  - **Regex:** written against the project's real spelling of the construct. Before writing the row, grep-verify that it matches at least one real occurrence inside its `Covers`, an owner site in `Exempts` included.
  - **`Covers`:** the `layers[].path` values from `<layer_path_map>`, or paths beneath them, whose files the rule binds.
  - **`Exempts`:** the owner sites where the construct legitimately lives.
  - **Last cell:** what a hit is a candidate for, citing the conventions document and heading the class came from.
  - **The row format, stated verbatim as the wire a script parses:** the one table directly under the exact heading `## Sweep rows`; header row exactly `| Escape class | Regex | Covers | Exempts | A hit is a candidate for |`, then its separator row; the table ending at the first line not beginning with `|`; `Regex` exactly one backtick code span holding a `grep -E` (POSIX ERE) pattern, with a literal `|` written `\|` and no backtick; `Covers` code-spanned repo-relative paths separated by `, `, `.` for the whole repository; `Exempts` code-spanned paths or pathspec globs separated by `, `, or `—` for none. A class whose construct cannot be expressed within that format goes to `## Not determined` rather than into a malformed row.
  - **Per-row provenance:** the conventions document and heading the class came from, plus the file the regex was verified against.
  - **No commit-message probe and no shared-document divergence:** `shared_document_divergences` is `[]` on this target.
- [ ] `## House rules` → **Never require a write to a path a run may not write.**: leave it as it stands. The sweep document's own rows require no write. Read it once against the new section, and confirm that no sentence of the new section asks a run to write under `.claude/**`.

**Verification:**

- `git grep -n -F '| Escape class | Regex | Covers | Exempts | A hit is a candidate for |' -- plugin/agents/conventions-writer.md cli/templates/claude/review-sweep.md` prints the header row from both files, byte-identical.
- `git grep -n -F '## Sweep rows' -- plugin/agents/conventions-writer.md` resolves.
- `git grep -n -F 'shared_document_divergences' -- plugin/schemas/conventions-writer.return.json` is unchanged from `dev`. No return field was added or renamed.
